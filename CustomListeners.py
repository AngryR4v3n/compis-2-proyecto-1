from antlr4.tree.Tree import TerminalNodeImpl
from DecafListener import DecafListener
from DecafParser import DecafParser
from SymbolTable import SymbolTable
from SymbolTableEntry import SymbolTableEntry
from random import randint


class CustomListener(DecafListener):
    def __init__(self) -> None:
        self.table = SymbolTable()
        self.nodeTypes = {}
        self.errors = []
        self.paramError = []
        #method_obj: {true/false}
        self.nonVoid = {}
        #name: {var: {EntryObj, EntryObj}}
        self.structs = {}
        self.structsStack = []
        super().__init__()

    def add_errors(self, errorTitle, entry, line):
        self.errors.append(f"{errorTitle}: {entry}, at line {line}")

    def enterNormalVar(self, ctx: DecafParser.NormalVarContext):
        varType = ctx.getChild(0).getText()
        if isinstance(ctx.getChild(0), DecafParser.StructTypeContext):
            varType = ctx.getChild(0).getChild(1).getText()
        id = ctx.getChild(1).getText()
        
        entry = SymbolTableEntry(
            varType, id, "", "var", self.table.parentScope, scope=self.table.currentScope)

        self.nodeTypes[ctx] = varType
        self.table.add_entry(entry)

    def enterArrVar(self, ctx: DecafParser.ArrVarContext):
        varType = ctx.getChild(0).getText()
        id = ctx.getChild(1).getText()
        num = ctx.NUM()
        numVal = num.getText()
        for i in range(0, int(numVal)):

            entry = SymbolTableEntry(
                varType, id, "Array", "var", self.table.parentScope, arrIndex=i, scope=self.table.currentScope)

            self.table.add_entry(entry)

    def enterEmptyMethod(self, ctx: DecafParser.EmptyMethodContext):
        methodReturnType = ctx.getChild(0).getChild(0).getText()
        methodName = ctx.getChild(1).getText()
        self.table.nest_scope(methodName)
        entry = SymbolTableEntry(methodReturnType, methodName, None,
                                 "function", self.table.parentScope, scope=self.table.currentScope)
        if methodReturnType != "void":
            self.nonVoid[ctx] = {"isOk": False, "obj": ctx}
        self.table.add_entry(entry)

    def enterParamMethod(self, ctx: DecafParser.ParamMethodContext):
        methodReturnType = ctx.getChild(0).getChild(0).getText()
        methodName = ctx.getChild(1).getText()
        self.table.nest_scope(methodName)
        entry = SymbolTableEntry(methodReturnType, methodName, None,
                                 "function", self.table.parentScope, scope=self.table.currentScope)

        varName = ctx.parameter().getChild(1).getText()
        varType = ctx.parameter().getChild(0).getText()
        param = SymbolTableEntry(varType, varName, "", 'param',
                                 self.table.parentScope, arrIndex=0, scope=self.table.currentScope, isParam=True)

        self.table.add_entry(param)

        if methodReturnType != "void":
            self.nonVoid[ctx] = {"isOk": False, "obj": ctx}
        self.table.add_entry(entry)

    def enterParamsMethod(self, ctx: DecafParser.ParamsMethodContext):
        methodReturnType = ctx.getChild(0).getChild(0).getText()
        methodName = ctx.getChild(1).getText()
        self.table.nest_scope(methodName)
        entry = SymbolTableEntry(methodReturnType, methodName, None,
                                 "function", self.table.parentScope, scope=self.table.currentScope)

        params = ctx.parameter()
        # asignamos en for loop que indice es ese metodo para identificar facilmente.
        for index, elem in enumerate(params):
            varName = elem.getChild(1).getText()
            paramType = elem.getChild(0).getText()
            param = SymbolTableEntry(paramType, varName, "", 'param',
                                     self.table.parentScope, arrIndex=index, scope=self.table.currentScope, isParam=True)
            self.table.add_entry(param)
        if methodReturnType != "void":
            self.nonVoid[ctx] = {"isOk": False, "obj": ctx}
        self.table.add_entry(entry)

    def exitAssignSt(self, ctx: DecafParser.AssignStContext):


        #si child count location es igual a 1 -> variable normal

        if ctx.location().getChildCount() == 1:
            location = ctx.location().getText()
            
            expression = ctx.expression().getText()
            expr = ctx.expression()
            updated = True
            i=0
            registry = None
            while not registry and i < len(self.table.scopes):
                    registry = self.table.get_entry({"name": location, "scope": self.table.scopes[i]})
                    i+=1
            
            if registry:
                registry.value = expression
                typeNode = self.nodeTypes[expr]
                #updated = self.table.update_entry(registry, typeNode)
            else:
                #buscamos en los otros scopes...
                
                self.add_errors("Undeclared variable",
                                "no existing variable", ctx.start.line)
            if not updated:
                self.add_errors(
                    "Type error", "check type declaration and assignment", ctx.start.line)
        #array, tiene que ser el resultado de la expression un int.
        elif ctx.location().expression() != None:
            expr = ctx.location().expression()

            if isinstance(expr, DecafParser.MinusOpContext):
                self.add_errors("Negative index", "array index must be a positive int", ctx.start.line)
                return 
            typeExpr = self.nodeTypes[expr]
            if typeExpr != 'int':
                self.add_errors("Unexpected index", "index must be type int", ctx.start.line)

            #buscamos para ver si existe..
            number = ctx.location().expression().getChild(0)
            if isinstance(number, DecafParser.LiteralContext):
                number = number.getChild(0).getText()
                name = ctx.location().getChild(0).getText()
                target = self.table.get_entry({"name": name+number, "scope": self.table.currentScope})

                if not target:
                    self.add_errors("Non existing index", "index provided does not exist", ctx.start.line)

        #struct?
        elif ctx.location().getChildCount() > 2:
            varName = ctx.location().getChild(0).getText()
            propertyStruct = ctx.location()
            
            while propertyStruct.location() != None:
                propertyStruct = propertyStruct.location()
            #array dentro de struct assign..
            if propertyStruct.expression() != None:
                x = propertyStruct.expression().getChild(0).getChild(0)
                propName = propertyStruct.getChild(0).getText()
                if isinstance(x, DecafParser.Int_literalContext):
                    numb = propertyStruct.expression().getChild(0).getText()
                    obj = self.table.get_entry({"name": varName, "scope": self.table.currentScope})
                    objStruct = self.table.get_entry({"name": str(propName+numb), "scope": obj.varType})
                    
                    if objStruct == None:
                        self.add_errors("Non existing index", "index provided does not exist", ctx.start.line)
                        return

                    if objStruct.varType != self.nodeTypes[ctx.expression()]:
                        self.add_errors(
                    "Type error", "check type declaration and assignment", ctx.start.line)


                    
            #normal call de un struct ... hay que hacer smh esto recursivo..
            else:
                #aqui se identifica el tipo de propiedad 
                varToSearch = propertyStruct.getChild(0).getText()
               
                obj = None
                i = 0
                while not obj and i < len(self.table.scopes):
                    obj = self.table.get_entry({"name": varName, "scope": self.table.scopes[i]})
                    i+=1

                availableProps = self.structs[obj.varType].value
                targetType = None
                
                
                #si no lo encontramos en el contexto actual.. 
                newLookout = []
                for elem in availableProps:
                    if varToSearch == elem.name:
                        targetType = elem.varType
                        break
                    #es un struct!
                    if elem.varType not in ["int", "char", "boolean"]:
                        newLookout.append(elem.varType)

                if newLookout != []:
                    targetType = self.propSearcher(varToSearch, newLookout)


                #aqui a lo que se asigna
                contextExp = ctx.expression()
                setType = self.nodeTypes[contextExp]
                if setType != targetType:
                    self.add_errors("Unexpected assignment in struct property", f"expected {targetType}, got {setType}", ctx.start.line)
                

    def propSearcher(self, varToSearch, availableProps):
        targetType = None
        iterat = 0
        
        while not targetType and iterat < 35 and availableProps != []:
            newLookout = []
            x = self.structs[availableProps.pop()].value
            for elem in x:
                if varToSearch == elem.name:
                    targetType = elem.varType
                    break
                #es un struct!
                if elem.varType not in ["int", "char", "boolean"]:
                    newLookout.append(elem.varType)
                #si encontramos algo nuevo, vamonooos.
            if newLookout != []:
                availableProps = newLookout
            iterat += 1
        return targetType


    def exitReturnSt(self, ctx: DecafParser.ReturnStContext):
        varToReturn = ctx.getChild(1).getChild(0)
        #revisamos struct case
        while isinstance(varToReturn.getChild(varToReturn.getChildCount()-1), DecafParser.LocationContext):
            varToReturn = varToReturn.getChild(varToReturn.getChildCount()-1)
        
        functParent = self.getAncestor(ctx)
        if not (isinstance(functParent, (DecafParser.ParamMethodContext, DecafParser.ParamsMethodContext, DecafParser.EmptyMethodContext))):
            self.add_errors("Unexpected return",
                            "return outside function", ctx.start.line)
        else:
            typeFunct = functParent.getChild(0).getChild(0).getText()

            if typeFunct == "void":
                self.add_errors("Unexpected return",
                                "return in void function", ctx.start.line)
                return
            elif self.nodeTypes[varToReturn] != typeFunct:
                self.add_errors(
                    "Type error", "return type and method type must be the same", ctx.start.line)
            self.nonVoid[functParent]["isOk"] = True

    def getAncestor(self, ctx, ancestorType="func"):
        parent = ctx.parentCtx
        if ancestorType == "func":
            if(isinstance(parent, (DecafParser.ParamMethodContext, DecafParser.ParamsMethodContext, DecafParser.EmptyMethodContext))):
                return parent
            else:
                parent = self.getAncestor(parent)
        else:
            if(isinstance(parent, ancestorType)):
                return parent
            else:
                parent = self.getAncestor(parent, ancestorType)

        return parent

    def exitMethodCallExp(self, ctx: DecafParser.MethodCallExpContext):
        child = ctx.getChild(0)
        self.nodeTypes[ctx] = self.nodeTypes[child]

    def exitParamMethod(self, ctx: DecafParser.ParamMethodContext):
        methodtype = ctx.getChild(0)
        methodtype = self.nodeTypes[methodtype]
        self.nodeTypes[ctx] = methodtype
        self.table.exit_scope()

    def exitParamsMethod(self, ctx: DecafParser.ParamsMethodContext):
        methodtype = ctx.getChild(0)
        methodtype = self.nodeTypes[methodtype]

        self.nodeTypes[ctx] = methodtype
        self.table.exit_scope()

    def exitEmptyMethod(self, ctx: DecafParser.EmptyMethodContext):
        methodName = ctx.getChild(1).getText()
        methodtype = ctx.getChild(0)

        if methodName != "main":
            methodtype = self.nodeTypes[methodtype]
            self.nodeTypes[ctx] = methodtype
        self.table.exit_scope()

    def exitMethodCallParams(self, ctx: DecafParser.MethodCallParamsContext):
        methodName = ctx.getChild(0).getText()

        methodObj = self.table.get_entry(
            {"name": methodName, "scope": methodName})
        if methodObj:
            typeVar = methodObj.varType
            self.nodeTypes[ctx] = typeVar
        else:
            self.add_errors("Unexisting method call",
                            "Non defined method call", ctx.start.line)
            return
        exps = ctx.expression()
        for index, elem in enumerate(exps):

            val = elem.getChild(0)
            typeVar = self.nodeTypes[val]
            targetVar = self.table.get_entry_by_idx(
                {"scope": methodName, "index": index})
            try:
                if targetVar.varType != typeVar:
                    self.add_errors(
                        "Type error", f"non matching types in method call variable {targetVar.name}", ctx.start.line)
                else:
                    targetVar.value = val.getText()
            except AttributeError:
                self.add_errors("Method call error",
                                "Invalid method call", ctx.start.line)

    def exitMethodCallNoParam(self, ctx: DecafParser.MethodCallNoParamContext):
        methodName = ctx.getChild(0).getText()
        methodObj = self.table.get_entry(
            {"name": methodName, "scope": methodName})
        if methodObj:
            typeVar = methodObj.varType
            self.nodeTypes[ctx] = typeVar
        else:
            self.add_errors("Unexisting method call",
                            "Non defined method call", ctx.start.line)
            return

        scope = self.table.get_scope({"scope": methodName})
        for elem in scope.keys():
            if scope[elem].symbolType == "param":
                self.add_errors(
                    "Method call error", f"Invalid method call, missing param {scope[elem].name}", ctx.start.line)

    def exitMethodCallParam(self, ctx: DecafParser.MethodCallParamContext):
        methodName = ctx.getChild(0).getText()
        methodObj = self.table.get_entry(
            {"name": methodName, "scope": methodName})
        if methodObj:
            typeVar = methodObj.varType
            self.nodeTypes[ctx] = typeVar
        else:
            self.add_errors("Unexisting method call",
                            "Non defined method call", ctx.start.line)
            return
        exps = ctx.expression()
        val = exps.getChild(0)

        
         #revisamos struct case
        while isinstance(val.getChild(val.getChildCount()-1), DecafParser.LocationContext):
            val = val.getChild(val.getChildCount()-1)

        typeVar = self.nodeTypes[val]
        targetVar = self.table.get_entry_by_idx(
            {"scope": methodName, "index": 0})
        try:
            if targetVar.varType != typeVar:
                self.add_errors(
                    "Type error", f"non matching types in method call variable {targetVar.name}", ctx.start.line)
            else:
                targetVar.value = val.getText()
        except AttributeError:
            self.add_errors("Method call error",
                            "Invalid method call", ctx.start.line)

    def exitMethod(self, ctx: DecafParser.MethodCallParamContext):
        methodName = ctx.getChild(0).getText()
        exps = ctx.expression()
        for index, elem in enumerate(exps):
            val = elem.getChild(0)
            typeVar = self.nodeTypes[val]
            targetVar = self.table.get_entry_by_idx(
                {"scope": methodName, "index": index})
            if targetVar.varType != typeVar:
                self.add_errors(
                    "Type error", f"non matching types in method call variable {targetVar.name}", ctx.start.line)
            else:
                targetVar.value = val.getText()

    def exitMethodType(self, ctx: DecafParser.MethodTypeContext):
        child = ctx.getChild(0).getText()
        self.nodeTypes[ctx] = child

    def exitInt_literal(self, ctx: DecafParser.Int_literalContext):
        self.nodeTypes[ctx] = 'int'

    def exitChar_literal(self, ctx: DecafParser.Char_literalContext):
        self.nodeTypes[ctx] = 'char'

    def exitBool_literal(self, ctx: DecafParser.Bool_literalContext):
        self.nodeTypes[ctx] = 'boolean'

    def exitMinusOp(self, ctx: DecafParser.MinusOpContext):
        self.nodeTypes[ctx] = 'int'

    def exitLiteralExp(self, ctx: DecafParser.LiteralExpContext):
        child = ctx.getChild(0)
        self.nodeTypes[ctx] = self.nodeTypes[child]

    def exitLiteral(self, ctx: DecafParser.LiteralContext):
        child = ctx.getChild(0)
        self.nodeTypes[ctx] = self.nodeTypes[child]

    def exitSumOp(self, ctx: DecafParser.SumOpContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        while isinstance(op1.getChild(op1.getChildCount()-1), DecafParser.LocationContext):
            op1 = op1.getChild(op1.getChildCount()-1)

        while isinstance(op2.getChild(op2.getChildCount()-1), DecafParser.LocationContext):
            op2 = op2.getChild(op2.getChildCount()-1)

        if self.nodeTypes[op1] != "int" or self.nodeTypes[op2] != "int":
            self.add_errors(
                "Type error", "operands must be int type", ctx.start.line)

        self.nodeTypes[ctx] = "int"

    def exitRelOp(self, ctx: DecafParser.Rel_opContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)
        
        while isinstance(op1.getChild(op1.getChildCount()-1), DecafParser.LocationContext):
            op1 = op1.getChild(op1.getChildCount()-1)

        while isinstance(op2.getChild(op2.getChildCount()-1), DecafParser.LocationContext):
            op2 = op2.getChild(op2.getChildCount()-1)
        
        if self.nodeTypes[op1] != "int" or self.nodeTypes[op2] != "int":
            self.add_errors(
                "Type error", "operands must be int type", ctx.start.line)

        self.nodeTypes[ctx] = "boolean"

    def exitEqOp(self, ctx: DecafParser.Eq_opContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)
        
        while isinstance(op1.getChild(op1.getChildCount()-1), DecafParser.LocationContext):
            op1 = op1.getChild(op1.getChildCount()-1)

        while isinstance(op2.getChild(op2.getChildCount()-1), DecafParser.LocationContext):
            op2 = op2.getChild(op2.getChildCount()-1)
        tyOp1 = self.nodeTypes[op1]
        tyOp2 = self.nodeTypes[op2]
        
        if tyOp1 not in ["int", "boolean", "char"] or tyOp2 not in ["int", "boolean", "char"]:
            self.add_errors(
                "Type error", "operands must be primitive type", ctx.start.line)

        self.nodeTypes[ctx] = "boolean"

    def exitCondOp(self, ctx: DecafParser.Cond_opContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        while isinstance(op1.getChild(op1.getChildCount()-1), DecafParser.LocationContext):
            op1 = op1.getChild(op1.getChildCount()-1)

        while isinstance(op2.getChild(op2.getChildCount()-1), DecafParser.LocationContext):
            op2 = op2.getChild(op2.getChildCount()-1)

        if self.nodeTypes[op1] != "boolean" or self.nodeTypes[op2] != "boolean":
            self.add_errors(
                "Type error", "operands must be bool type", ctx.start.line)

        self.nodeTypes[ctx] = "boolean"

    def exitOtherIntOp(self, ctx: DecafParser.OtherIntOpContext):

        
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        if isinstance(op1.parentCtx, DecafParser.ParensOpContext):
            op1 = ctx.getChild(0)
        
        if isinstance(op2.parentCtx, DecafParser.ParensOpContext):
            op2 = ctx.getChild(2)
        

        while isinstance(op1.getChild(op1.getChildCount()-1), DecafParser.LocationContext):
            op1 = op1.getChild(op1.getChildCount()-1)

        while isinstance(op2.getChild(op2.getChildCount()-1), DecafParser.LocationContext):
            op2 = op2.getChild(op2.getChildCount()-1)

        if self.nodeTypes[op1] != "int" or self.nodeTypes[op2] != "int":
            self.add_errors(
                "Type error", "operands must be int type", ctx.start.line)
        self.nodeTypes[ctx] = "int"

    def exitNotOp(self, ctx: DecafParser.NotOpContext):
        op1 = ctx.getChild(1).getChild(0)
        while isinstance(op1.getChild(op1.getChildCount()-1), DecafParser.LocationContext):
            op1 = op1.getChild(op1.getChildCount()-1)

        if self.nodeTypes[op1] != "bool":
            self.add_errors(
                "Type error", "operand must be bool type", ctx.start.line)
        self.nodeTypes[ctx] = "bool"

    def exitParensOp(self, ctx: DecafParser.ParensOpContext):
        op1 = ctx.getChild(1).getChild(0)
        while isinstance(op1.getChild(op1.getChildCount()-1), DecafParser.LocationContext):
            op1 = op1.getChild(op1.getChildCount()-1)

        if self.nodeTypes[op1] == "void":
            self.add_errors(
                "Type error", "operand must not be void type", ctx.start.line)
        self.nodeTypes[ctx] = self.nodeTypes[op1]

    def enterIf(self, ctx: DecafParser.IfContext):
        num = randint(1, 10)
        string = self.table.currentScope + "if" + str(num)
        self.table.nest_scope(string)

    def exitIf(self, ctx: DecafParser.IfContext):
        self.table.exit_scope()

    def enterWhile(self, ctx: DecafParser.WhileContext):
        num = randint(1, 10)
        string = self.table.currentScope + "while" + str(num)
        self.table.nest_scope(string)

    def exitWhile(self, ctx: DecafParser.WhileContext):
        self.table.exit_scope()

    def enterLocation(self, ctx: DecafParser.LocationContext):
        # si aun no, debe ser un struct..
        location = ctx.getChildCount()
        # es un struct
        if location == 3 and self.structsStack == []:
            # variable del struct...
            nameVar = ctx.getChild(0).getText()
            #si no la encuentra deberia buscar en parent
            varObj = None
            i = 0
            while not varObj and i < len(self.table.scopes):
                varObj = self.table.get_entry({"name": nameVar, "scope": self.table.scopes[i]})
                i+=1
            #si no encuentra, y el padre es un location ... fresh
            if not varObj and isinstance(ctx.parentCtx, DecafParser.LocationContext):
                return
            try:
                definition = self.structs[varObj.varType]
            except KeyError:
                self.add_errors("Unexisting struct", "non defined struct type", ctx.start.line)
                return

            # agregamos..
            self.structsStack.insert(0, varObj.varType)

        elif location == 3:
            toSearch = self.structsStack[0]
            # definicion del struct
            definition = self.table.table[toSearch]
            # variableToLook
            var = ctx.getChild(0).getText()
            try:
                obj = definition[var]
                self.structsStack.insert(0, obj.varType)

            except KeyError:
                self.add_errors("Unexisting property in struct",
                                "check the property", ctx.start.line)
                self.paramError.append(var)
        elif location == 1 and self.structsStack != []:
            toSearch = self.structsStack[0]
            definition = self.table.table[toSearch]
            var = ctx.getChild(0).getText()
            try:
                obj = definition[var]
                self.structsStack = []
                self.nodeTypes[ctx] = obj.varType
                val = obj
            except KeyError:
                self.add_errors("Unexisting property in struct",
                                "check the property", ctx.start.line)
                self.paramError.append(var)
            self.structsStack = []

    def exitLocation(self, ctx: DecafParser.LocationContext):
        #aqui deberiamos revisar si el ultimo hijo es un loc
        if ctx.getChild(ctx.getChildCount()-1).getText() == "]":
            entry = ctx.getChild(0)
        else:
            entry = ctx.getChild(ctx.getChildCount()-1)
        while(isinstance(entry, DecafParser.LocationContext) and entry.location()):
            entry = entry.getChild(entry.getChildCount()-1)

        child = ctx.getChild(0).getText()
        #child = entry.getText()
        if child in self.paramError:
            return
        # encuentra la variable a la cual se refiere, en el current scope
        val = self.table.get_entry(
            {"name": child, "scope": self.table.currentScope})

        # si no esta en el actual, buscamos en el contexto anterior
        i=0
        while not val and i < len(self.table.scopes):
            val = self.table.get_entry({"name": child, "scope": self.table.scopes[i]})
            i+=1


        # si no, podria ser un param de struct..
        if not val:
            for elem in self.structs.keys():
                for index, var in enumerate(self.structs[elem].value):
                    if var.name == child:
                        val = self.structs[elem].value[index]
                        break
                    

        # si viene de una expresion la evaluamos
        
        
        expr = ctx.expression()

        if expr:
            typeExpr = self.nodeTypes[expr]
            if typeExpr != "int":
                self.add_errors(
                    "Index error", "expression must return int type", ctx.start.line)

        #estamos en el head. obtenemos hijo derecho, si es struct
            
        self.nodeTypes[ctx] = val.varType

    def exitLocationExp(self, ctx: DecafParser.LocationExpContext):
        self.nodeTypes[ctx] = self.nodeTypes[ctx.getChild(0)]

    def exitIf(self, ctx: DecafParser.IfContext):
        expr = ctx.expression()
        typeExpr = self.nodeTypes[expr]
        if typeExpr != "boolean":
            self.add_errors(
                "Type error", "expression must return bool type", ctx.start.line)

    def exitWhile(self, ctx: DecafParser.WhileContext):
        expr = ctx.expression()
        typeExpr = self.nodeTypes[expr]
        if typeExpr != "boolean":
            self.add_errors(
                "Type error", "expression must return bool type", ctx.start.line)

    def enterStructDeclaration(self, ctx: DecafParser.StructDeclarationContext):
        nameStruct = ctx.getChild(1).getText()
        self.table.nest_scope(nameStruct)
        entry = SymbolTableEntry("struct", nameStruct, [], "struct",
                                 self.table.parentScope, scope=self.table.currentScope)
        self.structs[nameStruct] = entry
        declarations = ctx.varDeclaration()
        for index, elem in enumerate(declarations):
            typeDec = elem.getChild(0).getChild(0).getText()

            if typeDec == "struct":
                typeVar = elem.getChild(0).getChild(1).getText()
                name = elem.getChild(1).getText()
                # check if exists
                try:
                    exists = self.structs[typeVar]

                except KeyError:
                    exists = None
                if not exists:
                    self.add_errors("Struct declaration error",
                                    "Struct type does not exist", elem.start.line)
                else:
                    entry = SymbolTableEntry(
                    typeVar, name, "", "structParam", self.table.parentScope, arrIndex=index, scope=self.table.currentScope)
                    lista = self.structs[nameStruct].value
                    lista.append(entry)
            else:
                typeVar = elem.getChild(0).getChild(0).getText()

                name = elem.getChild(1).getText()

                entry = SymbolTableEntry(
                    typeVar, name, "", "structParam", self.table.parentScope, arrIndex=index, scope=self.table.currentScope)

                
                lista = self.structs[nameStruct].value
                lista.append(entry)
                

    def exitStructDeclaration(self, ctx: DecafParser.StructDeclarationContext):
        self.table.exit_scope()

    def exitProgram(self, ctx: DecafParser.ProgramContext):
        scopes = self.table.table.keys()
        if "main" not in scopes:
            self.add_errors("Missing method",
                            "missing main() method", ctx.start.line)
        for key in self.nonVoid.keys():
            if not self.nonVoid[key]["isOk"]:
                self.add_errors(
                    "Missing return", "Non void method is missing a return statement", self.nonVoid[key]["obj"].start.line)
