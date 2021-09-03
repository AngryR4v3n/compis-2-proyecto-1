from antlr4.tree.Tree import TerminalNodeImpl
from DecafListener import DecafListener
from DecafParser import DecafParser
from SymbolTable import SymbolTable
from SymbolTableEntry import SymbolTableEntry


class CustomListener(DecafListener):
    def __init__(self) -> None:
        self.table = SymbolTable()
        self.nodeTypes = {}
        self.errors = []
        #method_obj: {true/false}
        self.nonVoid = {}
        super().__init__()

    def add_errors(self, errorTitle, entry, line):
        self.errors.append(f"{errorTitle}: {entry}, at line {line}")

    def enterNormalVar(self, ctx: DecafParser.NormalVarContext):
        varType = ctx.getChild(0).getText()

        if varType.find("struct") != -1:
            varType = ctx.getChild(0).getChild(1).getText()
            definition = self.table.get_entry({"name": varType, "scope": varType})
            if not definition:
                
                self.add_errors("Struct declaration error",
                                    "Struct type does not exist", ctx.start.line)

        id = ctx.getChild(1).getText()
        entry = SymbolTableEntry(
            varType, id, "", "var", self.table.parentScope, scope=self.table.currentScope)

        self.nodeTypes[ctx] = varType
        self.table.add_entry(entry)
        return super().enterNormalVar(ctx)

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
                                 self.table.parentScope, arrIndex=0, scope=self.table.currentScope)

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
                                     self.table.parentScope, arrIndex=index, scope=self.table.currentScope)
            self.table.add_entry(param)
        if methodReturnType != "void":
            self.nonVoid[ctx] = {"isOk": False, "obj": ctx}
        self.table.add_entry(entry)

    def exitAssignSt(self, ctx: DecafParser.AssignStContext):
        location = ctx.location().getText()
        expression = ctx.expression().getText()
        expr = ctx.expression()

        searchQuery = {"name": location, "scope": self.table.currentScope}
        registry = self.table.get_entry(searchQuery)
        updated = True
        if registry:
            registry.value = expression
            typeNode = self.nodeTypes[expr]
            updated = self.table.update_entry(registry, typeNode)
        else:
            self.add_errors("Undeclared variable",
                            "no existing variable", ctx.start.line)

        if not updated:
            self.add_errors(
                "Type error", "check type declaration and assignment", ctx.start.line)

    def exitReturnSt(self, ctx: DecafParser.ReturnStContext):
        varToReturn = ctx.getChild(1).getChild(0)
        self.nodeTypes[ctx] = self.nodeTypes[varToReturn]
        functParent = self.getAncestor(ctx)
        if not (isinstance(functParent, (DecafParser.ParamMethodContext, DecafParser.ParamsMethodContext, DecafParser.EmptyMethodContext))):
            self.add_errors("Unexpected return",
                            "return outside function", ctx.start.line)
        else:
            typeFunct = functParent.getChild(0).getChild(0).getText()

            if typeFunct == "void":
                self.add_errors("Unexpected return",
                                "return in void function", ctx.start.line)
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

    def exitLiteralExp(self, ctx: DecafParser.LiteralExpContext):
        child = ctx.getChild(0)
        self.nodeTypes[ctx] = self.nodeTypes[child]

    def exitLiteral(self, ctx: DecafParser.LiteralContext):
        child = ctx.getChild(0)
        self.nodeTypes[ctx] = self.nodeTypes[child]

    def exitSumOp(self, ctx: DecafParser.SumOpContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        if self.nodeTypes[op1] != "int" or self.nodeTypes[op2] != "int":
            self.add_errors(
                "Type error", "operands must be int type", ctx.start.line)

        self.nodeTypes[ctx] = "int"

    def exitRelOp(self, ctx: DecafParser.Rel_opContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        if self.nodeTypes[op1] != "int" or self.nodeTypes[op2] != "int":
            self.add_errors(
                "Type error", "operands must be int type", ctx.start.line)

        self.nodeTypes[ctx] = "boolean"

    def exitEqOp(self, ctx: DecafParser.Eq_opContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        if self.nodeTypes[op1] not in ["int", "boolean", "char"] or self.nodeTypes[op2] not in ["int", "boolean", "char"]:
            self.add_errors(
                "Type error", "operands must be primitive type", ctx.start.line)

        self.nodeTypes[ctx] = "boolean"

    def exitCondOp(self, ctx: DecafParser.Cond_opContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        if self.nodeTypes[op1] != "boolean" or self.nodeTypes[op2] != "boolean":
            self.add_errors(
                "Type error", "operands must be bool type", ctx.start.line)

        self.nodeTypes[ctx] = "boolean"

    def exitOtherIntOp(self, ctx: DecafParser.OtherIntOpContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)
        if self.nodeTypes[op1] != "int" or self.nodeTypes[op2] != "int":
            self.add_errors(
                "Type error", "operands must be int type", ctx.start.line)
        self.nodeTypes[ctx] = "int"

    def exitNotOp(self, ctx: DecafParser.NotOpContext):
        op1 = ctx.getChild(1).getChild(0)
        if self.nodeTypes[op1] != "bool":
            self.add_errors(
                "Type error", "operand must be bool type", ctx.start.line)
        self.nodeTypes[ctx] = "bool"

    def exitParensOp(self, ctx: DecafParser.ParensOpContext):
        op1 = ctx.getChild(1).getChild(0)
        if self.nodeTypes[op1] == "void":
            self.add_errors(
                "Type error", "operand must not be void type", ctx.start.line)
        self.nodeTypes[ctx] = self.nodeTypes[op1]

    def exitLocation(self, ctx: DecafParser.LocationContext):
        child = ctx.getChild(0).getText()

        #encuentra la variable a la cual se refiere, en el current scope
        val = self.table.get_entry(
            {"name": child, "scope": self.table.currentScope})

        # si no esta en el actual, buscamos en globales
        if not val:
            val = self.table.get_entry({"name": child, "scope": child})
        
        #si viene de una expresion la evaluamos
        expr = ctx.expression()

        if expr:
            typeExpr = self.nodeTypes[expr]
            if typeExpr != "int":
                self.add_errors(
                    "Index error", "expression must return int type", ctx.start.line)

        #si viene location?
        loc = ctx.location()

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
        name = ctx.getChild(1).getText()
        self.table.nest_scope(name)
        entry = SymbolTableEntry("struct", name, "", "struct",
                                 self.table.parentScope, scope=self.table.currentScope)
        self.table.add_entry(entry)
        declarations = ctx.varDeclaration()
        for index, elem in enumerate(declarations):
            typeDec = elem.getChild(0).getChild(0).getText()

            if typeDec == "struct":
                typeVar = elem.getChild(0).getChild(1).getText()
                # check if exists
                exists = self.table.get_entry(
                    {"name": typeVar, "scope": typeVar})
                if not exists:
                    self.add_errors("Struct declaration error",
                                    "Struct type does not exist", elem.start.line)
            else:
                typeVar = elem.getChild(0).getChild(0).getText()

            name = elem.getChild(1).getText()

            entry = SymbolTableEntry(typeVar, name, "", "structParam",
                                     self.table.parentScope, arrIndex=index, scope=self.table.currentScope)
            self.table.add_entry(entry)


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
