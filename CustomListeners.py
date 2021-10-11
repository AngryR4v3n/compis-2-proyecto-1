from DecafListener import DecafListener
from DecafParser import DecafParser
from SymbolTable import StructTableItem, TableItem, ScopeTableItem

class CustomListener(DecafListener):
    def __init__(self) -> None:

        #sizes management
        self.primitives = ['int', 'char', 'boolean', 'struct', 'void']
        self.sizes = {'int': 4, 'char': 1, 'boolean': 1}
        self.offset = 0

        #Symbol table
        self.currentMethodName = ''
        self.currentScope = 'global'
        
        self.previousScope = None
        self.scopes = {}
        self.structs = {}
        self.structStack = []
        self.nest = 1
        self.addScope('global')
        #type and return management
        self.nodeTypes = {}
        #error management
        self.errors = []

    #ERRORS
    def add_errors(self, errorTitle, entry, line):
        self.errors.append(f"{errorTitle}: {entry}, at line {line}")

    #MEMORY MANAGEMENT
    def getSize(self, num, tipo):
        
        try:
            if tipo in self.primitives:
                return int(num) * self.sizes[tipo]
            else:
                #offset struct.
                return 0
        except KeyError:
            pass

    #TABLE MANAGEMENT
    def addScope(self, pastScope, methodType=None):
        canAdd = False
        if self.currentScope not in self.scopes:
            self.scopes[self.currentScope] = ScopeTableItem(parentKey=pastScope, returnType=methodType, symbolTable={})
            canAdd = True
        else:
            canAdd = False

        return canAdd


    def pushScope(self, scope):
        self.previousScope = self.currentScope
        self.currentScope = scope


    def isGlobal(self, name):
        isGlobal = False
        table = self.scopes['global'].symbolTable

        if name in table:
            isGlobal = True

        return isGlobal


    def addVar(self, varType, name, decafType, num, isArray):
        if (num == None): 
            num = 1
        
        canAdd = False
        currentVarSize = self.getSize(num, varType)

        # Gets the SymbolTable from the current scope
        tempSymbolTable = self.scopes[self.currentScope].symbolTable

        if name not in tempSymbolTable:
            tempSymbolTable[name] = TableItem(varType, name, num, decafType, currentVarSize, isArray, 0)
            self.offset += currentVarSize
            canAdd = True
        else:
            canAdd = False

        self.scopes[self.currentScope].symbolTable = tempSymbolTable
        return canAdd

    #STRUCT MANAGEMENT
    def addStruct(self, structId):
        name = structId
        structId = "struct"+structId
        if structId not in self.structs:
            self.structs[structId] = StructTableItem(structId=structId, structMembers={})
        
    """
    varType: Tipo de variable
    structName: Nombre de estructura a la que se le agrega la variable
    varName: Nombre de la variable
    varContext: tipo de variable
    num: Cantidad de variables que se van a crear > 1 si es un array
    isArray: Bandera que indica si algo es un array
    """
    def addStructProperty(self, varType, structName, varName, varContext, num, isArray):
        if not num: 
            num = 1

        added = False
        currentVarSize = self.getSize(num, varType)

        structId = "struct"+structName
        structProperties = self.structs[structId].structMembers
        tempStructSize = self.structs[structId].size

        if varName not in structProperties:
            structProperties[varName] = TableItem(varType, varName, num, varContext, currentVarSize, isArray, self.offset)
            tempStructSize += currentVarSize
            added = True
        else:
            added = False

        self.structs[structId].structMembers = structProperties
        self.structs[structId].size = tempStructSize
        return added

    def searchStruct(self, name):
        target = None
        if name in self.structs.keys():
            target = self.structs[name]

        return target
    
    def enterVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        value = None 
        isArray = False
        varType = ctx.getChild(0).getText()
        varId = ctx.getChild(1).getText()

        if 'struct' in varType:
            found = self.searchStruct(varType)
            if not found: 
                self.nodeTypes[ctx] = '-1'
                self.add_errors('Undeclared struct', 'struct has not been defined', ctx.start.line)
            else:
                #TODO: Revisar que exista array de structs..
                self.addVar(varType, varId, 'structVar', 1, isArray)
        else:

            added = self.addVar(varType, varId, "var", value, isArray)

            if added:
                self.nodeTypes[ctx] = 'void'
            else:
                self.nodeTypes[ctx] = '-1'
                self.add_errors("Scope error", "variable already exists!", ctx.start.line)


    def enterMethodDeclaration(self, ctx: DecafParser.MethodDeclarationContext):
        methodType = ctx.getChild(0).getText()
        methodName = ctx.getChild(1).getText()

        self.currentMethodName = methodName
        self.pushScope(methodName)


        #Se crea el scope
        added = self.addScope(self.previousScope, methodType)

        if (added):
            self.nodeTypes[ctx] = methodType
        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors("Method declaration error","Method already exists!",ctx.start.line )

    
    def enterParameter(self, ctx: DecafParser.ParameterContext):
        isArray = False
        if (ctx.getChildCount() > 2): 
            isArray=True

        paramType = ctx.getChild(0).getText()

        if paramType != 'void':
            paramId = ctx.getChild(1).getText()

            added = self.addVar(paramType, paramId, "param", None, isArray)
            if (added):
                self.nodeTypes[ctx] = paramType
            else:
                self.nodeTypes[ctx] = '-1'
                errorMsg = f"{paramId} parameter already exists!"
                self.addError("ParamError", errorMsg, ctx.start.line)


    def enterStructDeclaration(self, ctx: DecafParser.StructDeclarationContext):
        structId = ctx.getChild(1).getText()
        self.addStruct(structId)

        #populamos el struct 
        for dec in ctx.varDeclaration():
            varType = dec.getChild(0).getText()
            varId = dec.getChild(1).getText()
            value = ''

            isArray = dec.NUM()
            if not isArray:
                isArray = False
                num = 1
            else:
                isArray = True
                #TODO: Mejorar obtener el numero del array...
                num = int(dec.getChild(3).getText())
                
            added = self.addStructProperty(varType, structId, varId, "structVar", num, isArray)
            
            if added:
                self.nodeTypes[ctx] = 'void'
            else:
                self.nodeTypes[ctx] = '-1'
                self.add_errors('Scope error', 'variable already exists!', ctx.start.line)




    def enterLocation(self, ctx: DecafParser.LocationContext):
         if (ctx.location()):
            varId = ctx.getChild(0).getText()
            #si no estamos buscando dentro de un struct..
            if (self.structStack == []):
                structVarType = self.findSymbolTableEntry(varId, self.currentScope)
                structToUse = self.searchStruct(structVarType.varType)
                self.structStack.append(structToUse)
            else:
                #si no buscamos en el ultimo, la variable del struct y si esta en su def

                try:
                    structVarType = self.structStack[-1].structMembers[varId]
                except:
                    self.add_errors('Unexisting property', f'struct missing {varId} property', ctx.start.line)
                structToUse = self.searchStruct(structVarType.varType)
                self.structStack.append(structToUse)

    def enterBlock(self, ctx: DecafParser.BlockContext):
        parentCtx = ctx.parentCtx
        first = parentCtx.getChild(0).getText()

        if first not in self.primitives:
            blockname = self.currentMethodName + str(self.nest)
            self.nest += 1
            self.pushScope(blockname)

        add = self.addScope(self.previousScope)
        if add:
            self.nodeTypes[ctx] = 'void'

        else:
            self.nodeTypes[ctx] = '-1'
            
    
    def exitBlock(self, ctx: DecafParser.BlockContext):
        #Se sale de un scope.
        current = self.methodFinder(self.currentScope)
        self.pushScope(current.parent)

    def exitMethodDeclaration(self, ctx: DecafParser.MethodDeclarationContext):
        methodName = ctx.getChild(1).getText()
        if (methodName == 'main'):
            self.mainFound = True

        self.nestedCounter = 1
        self.currentMethodName = "global"

        self.pushScope("global")
    def exitMethodCall(self, ctx: DecafParser.MethodCallContext):
        name = ctx.getChild(0).getText()
        args = ctx.getChild(2).getText()

        methodRef = self.methodFinder(name)
        if methodRef:
            calls = []

            for i in range(2, len(ctx.children)-1):
                if(ctx.getChild(i).getText() != ','):
                    calls.append(self.nodeTypes[ctx.getChild(i)])
            
            #Checkeo si esta bien llamada la firma del metodo
            methodSig = self.paramCheck(methodRef, args, calls)

            if methodSig:
                self.nodeTypes[ctx] = methodRef.returnType

            else:
                self.nodeTypes[ctx] = '-1'
                self.add_errors('Method call error', 'param missmatch, check method call', ctx.start.line)
    
    def exitMethodCallExp(self, ctx: DecafParser.MethodCallExpContext):
        self.nodeTypes[ctx] = self.nodeTypes[ctx.methodCall()]

    def exitReturnSt(self, ctx: DecafParser.ReturnStContext):
        if ctx.getChild(0).getText() == 'return':
            method = self.getParentMethod(self.currentScope)
            varRet = ctx.getChild(1)

            if ctx.getChild(1).getText() == '':
                if method.returnType == 'void':
                    self.nodeTypes[ctx] = 'void'
                else:
                    self.nodeTypes[ctx] = '-1'
                    self.add_errors('Return type error', f'check method definition', ctx.start.line)

            else:
                exprType = self.nodeTypes[varRet.getChild(0)]

                if exprType == method.returnType:
                    self.nodeTypes[ctx] = method.returnType

                else:
                    self.nodeTypes[ctx] = '-1'
                    self.add_errors('Return type error', f'check method return type and returning entity', ctx.start.line)
    
    
    def exitSumOp(self, ctx: DecafParser.SumOpContext):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)

        if(self.nodeTypes[op1] == 'int' and self.nodeTypes[op2] == 'int'):
            self.nodeTypes[ctx] = 'int'
        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors('Entity type error', 'arithmetic operator expected integer entities', ctx.start.line)
    
    def exitRelOp(self, ctx: DecafParser.RelOpContext):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)

        if(self.nodeTypes[op1] == 'int' and self.nodeTypes[op2] == 'int'):
            self.nodeTypes[ctx] = 'int'
        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors('Entity type error', 'arithmetic operator expected integer entities', ctx.start.line)
    def exitOtherIntOp(self, ctx: DecafParser.OtherIntOpContext):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)

        if(self.nodeTypes[op1] == 'int' and self.nodeTypes[op2] == 'int'):
            self.nodeTypes[ctx] = 'int'
        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors('Entity type error', 'arithmetic operator expected integer entities', ctx.start.line)
    
    def exitLiteralExp(self, ctx: DecafParser.LiteralExpContext):
        self.nodeTypes[ctx] = self.nodeTypes[ctx.getChild(0)]

    def exitEqOp(self, ctx: DecafParser.EqOpContext):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)
        typeOp = self.nodeTypes[op1]
        typeOp2 = self.nodeTypes[op2]

        if typeOp == typeOp2:
            self.nodeTypes[ctx] = 'boolean'

        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors('Entity type error', 'comparison operator expected integer entities', ctx.start.line)


    def exitRel_op(self, ctx: DecafParser.Rel_opContext):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)

        if(self.nodeTypes[op1] == 'int' and self.nodeTypes[op2] == 'int'):
            self.nodeTypes[ctx] = 'int'
        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors('Entity type error', 'arithmetic operator expected integer entities', ctx.start.line)

    def exitCond_op(self, ctx: DecafParser.Cond_opContext):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)

        if(self.nodeTypes[op1] == 'boolean' and self.nodeTypes[op2] == 'boolean'):
            self.nodeTypes[ctx] = 'boolean'
        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors('Entity type error', 'logical operator expected boolean entities', ctx.start.line)

    def exitMinusOp(self, ctx: DecafParser.MinusOpContext):
        op1 = ctx.getChild(1)
        if(self.nodeTypes[op1] == 'int'):
            self.nodeTypes[ctx] = 'int'
        else:
            self.nodeTypes[ctx] = 'error'
            self.add_errors('Entity type error', "minus operator expected an int typed operator", ctx.start.line)
    
    def exitNotOp(self, ctx: DecafParser.NotOpContext):
        op1 = ctx.getChild(0)

        if self.nodeTypes[op1] == 'boolean':
            self.nodeTypes[ctx] = 'boolean'
        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors('Entity type error', 'logical operator expected boolean entity', ctx.start.line)

    #basic inputs
    def exitParensOp(self, ctx: DecafParser.ParensOpContext):
        self.nodeTypes[ctx] = self.nodeTypes[ctx.expression()] 

    def exitInt_literal(self, ctx: DecafParser.Int_literalContext):
        self.nodeTypes[ctx] = 'int'

    def exitChar_literal(self, ctx: DecafParser.Char_literalContext):
        self.nodeTypes[ctx] = 'char'

    def exitBool_literal(self, ctx: DecafParser.Bool_literalContext):
        self.nodeTypes[ctx] = 'boolean'


    def exitLocationExp(self, ctx: DecafParser.LocationExpContext):
        self.nodeTypes[ctx] = self.nodeTypes[ctx.getChild(0)]

    
    def exitLocation(self, ctx: DecafParser.LocationContext):
        var = None
        if ctx.location() != None:
            if self.structStack != []:
                currentTable = self.structStack.pop()

                if currentTable: 
                    var = currentTable.structMembers[ctx.getChild(0).getText()]

                    if var:
                        self.nodeTypes[ctx] = self.nodeTypes[ctx.location()]
                    else:
                        self.nodeTypes[ctx] = '-1'
                        self.add_errors('Struct definition error', 'non existing property', ctx.start.line)
                else:
                    self.nodeTypes[ctx] = '-1'
                    self.add_errors('Struct definition error', 'property is not a struct', ctx.start.line)
            else:
                var = self.findSymbolTableEntry(ctx.getChild(0).getText(), self.currentScope)
                if var:
                    self.nodeTypes[ctx] = self.nodeTypes[ctx.location()]
                else:
                    self.nodeTypes[ctx] = '-1'
                    self.add_errors('Location error', 'undefined location', ctx.start.line)
        elif isinstance(ctx.parentCtx, DecafParser.LocationContext) and not ctx.location():
            if self.structStack != []:
                currentTable = self.structStack.pop()

                if currentTable:
                    var = currentTable.structMembers[ctx.getChild(0).getText()]
                    if var:  
                        self.nodeTypes[ctx] = var.varType
                    else:
                        self.nodeTypes[ctx] = '-1'
                else:
                    self.nodeTypes[ctx] = '-1'
                    self.add_errors('Struct definition error', "Property not found on struct.", ctx.start.line)   
            #could delete
       

                
            else:
                self.nodeTypes[ctx] = '-1'
                self.addError(ctx.start.line, "Parent struct doesn't have this property.")
                
        else:
            var = self.findSymbolTableEntry(ctx.getChild(0).getText(), self.currentScope)
            if var:
                self.nodeTypes[ctx] = var.varType

            else:
                self.nodeTypes[ctx] = '-1'
                self.add_errors('No existing var',f'Var {ctx.getChild(0).getText()} is not defined', ctx.start.line)

            #acceso a array
            if ctx.expression():
                if self.nodeTypes[ctx.expression()] != 'int':
                    self.nodeTypes[ctx] = '-1'
                    self.add_errors('Location error', 'access expression must return an int', ctx.start.line)
                if var:
                    self.nodeTypes[ctx] = var.varType
                    if not var.isArray:
                        self.nodeTypes[ctx] = '-1'
                        self.add_errors('Location error', 'variable is not an array', ctx.start.line)

            else:
                if var:
                    self.nodeTypes[ctx] = var.varType

                    if var.isArray:
                        self.nodeTypes[ctx] = '-1'
                        self.add_errors('Access error', 'index needs to be provided', ctx.start.line)

    def exitVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        varType = ctx.getChild(0).getText()
        self.nodeTypes[ctx] = varType

    def exitLiteral(self, ctx: DecafParser.LiteralContext):
        varType = ctx.getChild(0)
        self.nodeTypes[ctx] = self.nodeTypes[varType]

    def exitLiteralExp(self, ctx: DecafParser.LiteralExpContext):
        self.nodeTypes[ctx] = self.nodeTypes[ctx.getChild(0)]

    def exitMethodCallExp(self, ctx: DecafParser.MethodCallExpContext):
        self.nodeTypes[ctx] = self.nodeTypes[ctx.getChild(0)]
        
    def exitAssignSt(self, ctx: DecafParser.AssignStContext):
        op1 = ctx.getChild(0)
        op2 = ctx.getChild(2)

        if self.nodeTypes[op1] == self.nodeTypes[op2]:
            self.nodeTypes[ctx] = self.nodeTypes[op1]

        else:
            self.nodeTypes = '-1'
            self.add_errors('Assignment error', 'variable and value are not the same', ctx.start.line)

        
    def exitIf(self, ctx: DecafParser.IfContext):
        #lo que esta dentro
        expr = ctx.getChild(2)
        
        if self.nodeTypes[expr] == 'boolean':
            self.nodeTypes[ctx] = 'boolean'

        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors('Type error', 'if expression must return boolean', ctx.start.line)


    def exitWhile(self, ctx: DecafParser.WhileContext):
        #lo que esta dentro
        expr = ctx.getChild(2)
        
        if self.nodeTypes[expr] == 'boolean':
            self.nodeTypes[ctx] = 'boolean'

        else:
            self.nodeTypes[ctx] = '-1'
            self.add_errors('Type error', 'while expression must return boolean', ctx.start.line)
            
    def exitProgram(self, ctx: DecafParser.ProgramContext):
        
        if "main" not in self.scopes:
            self.add_errors("Missing method",
                            "missing main() method", ctx.start.line)

    def findSymbolTableEntry(self, name, scope):
        targetSymbolTable = self.scopes[scope].symbolTable
        search = None

        if name in targetSymbolTable:
            search = targetSymbolTable[name]
        else:

            if scope == 'global' and not search:
                self.add_errors('Entity not found', 'var has not been declared', None)
                return 
            else:                
                otherScope = self.scopes.get(scope).parent

            #busca recursivamente hacia arriba
            if otherScope:
                search = self.findSymbolTableEntry(name,otherScope)

        return search

    def methodFinder(self, methodId):
        obj = self.scopes[methodId]
        return obj


    def getParentMethod(self, scope):
        targetParent = self.scopes[scope]
        if targetParent.parent != 'global':
            targetParent = self.getParentMethod(targetParent.parent)

        return targetParent
    def updateSymbolTableEntry(self, name, scope):
        pass

    def findMethod(self, name):
        method = self.scopes.get(name)
        return method

    def paramCheckMethod(self, scope, check):
        isCorrect = False
        parent = self.getParentMethod(scope)
        parentSymbolT = parent.symbolTable
        params = []

        for name, varObj in parentSymbolT.items():
            if varObj.decafType == 'param':
                params.append(varObj.name)
        
        if check in params:
            isCorrect = True
        
        return isCorrect

    
    def paramCheck(self, methodObj, arg, callTypes):
        symbol = methodObj.symbolTable
        methodTypes = []
        for varId, varItem in symbol.items():
            if varItem.decafType == "param":
                methodTypes.append(varItem.varType)

        if (callTypes == methodTypes):
            return True 
        else:
            return False