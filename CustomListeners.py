from DecafListener import DecafListener
from DecafParser import DecafParser
from antlr4 import TerminalNode


"""
Symbol Table:
{Entry.name: {...} }
"""
class SymbolTable():
    def __init__(self):
        self.scopes = ["global"]
        self.currentScope = self.scopes[0]
        self.parentScope = ""
        self.table = {self.currentScope: {"parentScope": ""}}
        self.types = {"int": [38], "char": [40, 37], "boolean": [41, 42]}
        self.inverseTypes = {38: "int", 40: "char",
                             37: "char", 41: "boolean", 42: "boolean"}

    def add_entry(self, entry) -> None:
        #self.isCorrect(entry)
        obj = {
            entry.id: entry
        }

        try:
            prevValues = {**self.table[self.currentScope]}
            self.table[self.currentScope] = prevValues | obj

        except KeyError:
            self.table[self.currentScope] = {
                entry.id: entry
            }

    def get_entry(self, entryQuery):
        try:
            return self.table[entryQuery["scope"]][hash(entryQuery["name"])]
        except KeyError:
            pass


    """
    entryQuery: {"scope": foo, "index": 1}
    """
    def get_entry_by_idx(self, entryQuery):
        try:
            variables = self.table[entryQuery["scope"]]
            keys = variables.keys()
            for elem in keys:
                if self.table[entryQuery["scope"]][elem].arrIndex == entryQuery["index"]:
                    return self.table[entryQuery["scope"]][elem]
        except KeyError:
            pass



    def update_entry(self, entry, typeNode) -> bool:
        if not self.checkTypeError(entry, typeNode):
            self.table[self.currentScope][entry.id] = entry
            return True
        else:
            return False

    
    def checkTypeError(self, entry, varType) -> bool:
        if entry.varType == varType:
            return False
        else:
            return True

    """
    Metodo utilizado para entrar a un nuevo ambito.
    """

    def nest_scope(self, newScope) -> None:
        self.scopes.append(newScope)
        self.parentScope = self.currentScope
        self.currentScope = newScope

    """
    Metodo utilizado para salir del ambito.
    """

    def exit_scope(self) -> None:
        self.scopes.pop()

        self.scope = self.scopes[len(self.scopes)-1]

        if len(self.scopes) >= 2:
            self.parentScope = self.scopes[len(self.scopes)-2]
        else:
            self.parentScope = "global"


    """
    Checks if the variable that is being added exists in a the same scope
    """

    def check_existing_same_scope(self, entry) -> bool:
        try:
            existingDictionary = self.table[entry.scope]
            existingDictionary[entry.id]
            return True

        except KeyError:

            return False


"""
Forma de una entrada en un symbol table
{uid: 13414141, varType: "int", name: "num", value: "1" scope: "global"}
"""
class SymbolTableEntry():
    def __init__(self, varType, name, value, symbolType, parentScope, arrIndex=None, scope="global"):
        self.id = hash(name+str(arrIndex)) if arrIndex else hash(name)
        self.varType = varType
        self.name = name
        self.value = value
        self.symbolType = symbolType
        self.parentScope = parentScope
        self.scope = scope
        self.arrIndex = arrIndex


class CustomListener(DecafListener):
    def __init__(self) -> None:
        self.table = SymbolTable()
        self.nodeTypes = {}
        self.errors = []
        super().__init__()

    def add_errors(self, errorTitle,entry, line):
        self.errors.append(f"{errorTitle}: {entry}, at line {line}")

    def enterNormalVar(self, ctx: DecafParser.NormalVarContext):
        varType = ctx.getChild(0).getText()
        id = ctx.getChild(1).getText()
        entry = SymbolTableEntry(
            varType, id, "", "var", self.table.parentScope, scope=self.table.currentScope)

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
        self.table.add_entry(entry)

    def enterParamMethod(self, ctx: DecafParser.ParamMethodContext):
        methodReturnType = ctx.getChild(0).getChild(0).getText()
        methodName = ctx.getChild(1).getText()
        self.table.nest_scope(methodName)
        entry = SymbolTableEntry(methodReturnType, methodName, None,
                                 "function", self.table.parentScope, scope=self.table.currentScope)
        self.table.add_entry(entry)

    def enterParamsMethod(self, ctx: DecafParser.ParamsMethodContext):
        methodReturnType = ctx.getChild(0).getChild(0).getText()
        methodName = ctx.getChild(1).getText()
        self.table.nest_scope(methodName)
        entry = SymbolTableEntry(methodReturnType, methodName, None,
                                 "function", self.table.parentScope, scope=self.table.currentScope)
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
            self.add_errors("Undeclared variable", "no existing variable", ctx.start.line)

        if not updated:
            self.add_errors("Type error", "check type declaration and assignment", ctx.start.line)

    def exitReturnSt(self, ctx: DecafParser.ReturnStContext):
        varToReturn = ctx.getChild(1).getChild(0)
        self.nodeTypes[ctx] = self.nodeTypes[varToReturn]
    
    
    def exitParamMethod(self, ctx: DecafParser.ParamMethodContext):
        block = ctx.getChild(ctx.getChildCount()-1)
        lastSt = block.getChild(block.getChildCount()-2)
        exprRet = lastSt.getChild(1).getChild(0)
        retTxt = lastSt.getChild(0).getText()
        methodtype = ctx.getChild(0)
        methodtype = self.nodeTypes[methodtype]
        if retTxt == 'return' and methodtype != 'void':
            typeRet = self.nodeTypes[exprRet]
            typeRet = self.nodeTypes[exprRet]
            
            if methodtype != typeRet:
                self.add_errors("Type error", "return type and method type must be the same", ctx.start.line)

        elif retTxt != 'return' and methodtype != 'void':
            self.add_errors("Type error", "non void methods must have a return statement", ctx.start.line)
        
        elif retTxt == 'return' and methodtype == 'void':
            self.add_errors("Type error", "unexpected return in void method", ctx.start.line)

        self.table.exit_scope()

        

    def exitParamsMethod(self, ctx: DecafParser.ParamsMethodContext):
        block = ctx.getChild(ctx.getChildCount()-1)
        lastSt = block.getChild(block.getChildCount()-2)
        exprRet = lastSt.getChild(1).getChild(0)
        retTxt = lastSt.getChild(0).getText() 
        params = ctx.parameter()
        
        #asignamos en for loop que indice es ese metodo para identificar facilmente.
        for index, elem in enumerate(params):
            varName = elem.getChild(1).getText()
            target = self.table.get_entry({"scope":self.table.currentScope, "name": varName})
            target.arrIndex = index
            print("")

        methodtype = ctx.getChild(0)
        methodtype = self.nodeTypes[methodtype]
        if retTxt == 'return' and methodtype != 'void':
            typeRet = self.nodeTypes[exprRet]
            typeRet = self.nodeTypes[exprRet]
            
            if methodtype != typeRet:
                self.add_errors("Type error", "return type and method type must be the same", ctx.start.line)

        elif retTxt != 'return' and methodtype != 'void':
            self.add_errors("Type error", "non void methods must have a return statement", ctx.start.line)
        
        elif retTxt == 'return' and methodtype == 'void':
            self.add_errors("Type error", "unexpected return in void method", ctx.start.line)
        
        self.table.exit_scope()

    
    def exitParameter(self, ctx: DecafParser.ParameterContext):
        paramType = ctx.getChild(0).getChild(0).getText()
        paramName = ctx.getChild(1).getText()
        entry = SymbolTableEntry(paramType, paramName, "", 'param', self.table.parentScope, scope=self.table.currentScope)
        self.table.add_entry(entry)
        print("")
    
    def exitEmptyMethod(self, ctx: DecafParser.EmptyMethodContext):
        block = ctx.getChild(ctx.getChildCount()-1)
        lastSt = block.getChild(block.getChildCount()-2)
        exprRet = lastSt.getChild(1).getChild(0)
        retTxt = lastSt.getChild(0).getText()
        methodtype = ctx.getChild(0)
        methodtype = self.nodeTypes[methodtype]
        if retTxt == 'return' and methodtype != 'void':
            typeRet = self.nodeTypes[exprRet]
            typeRet = self.nodeTypes[exprRet]
            
            if methodtype != typeRet:
                self.add_errors("Type error", "return type and method type must be the same", ctx.start.line)

        elif retTxt != 'return' and methodtype != 'void':
            self.add_errors("Type error", "non void methods must have a return statement", ctx.start.line)
        
        elif retTxt == 'return' and methodtype == 'void':
            self.add_errors("Type error", "unexpected return in void method", ctx.start.line)
        
        self.table.exit_scope()

    #TODO: REPLICAR ESTO PARA EL RESTO DE FUNCIONES :)
    def exitMethodCallParams(self, ctx: DecafParser.MethodCallParamsContext):
        methodName = ctx.getChild(0).getText()
        exps = ctx.expression()
        for index, elem in enumerate(exps):
            val = elem.getChild(0).getChild(0)
            typeVar = self.nodeTypes[val]
            targetVar = self.table.get_entry_by_idx({"scope": methodName, "index": index})
            if targetVar.varType != typeVar:
                self.add_errors("Type error", f"non matching types in method call variable {targetVar.name}", ctx.start.line)
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

        if self.nodeTypes[op1] != "int" and self.nodeTypes[op2] != "int":
            self.add_errors("Type error", "operands must be int type", ctx.start.line)
        
        self.nodeTypes[ctx] = "int"

    def exitRelOp(self, ctx: DecafParser.Rel_opContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        if self.nodeTypes[op1] != "int" and self.nodeTypes[op2] != "int":
            self.add_errors("Type error", "operands must be int type", ctx.start.line)
        
        self.nodeTypes[ctx] = "boolean"

    def exitEqOp(self, ctx: DecafParser.Eq_opContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        if self.nodeTypes[op1] not in ["int", "boolean", "char"] and self.nodeTypes[op2] not in ["int", "boolean", "char"]:
            self.add_errors("Type error", "operands must be primitive type", ctx.start.line)
        
        self.nodeTypes[ctx] = "boolean"

    def exitCondOp(self, ctx: DecafParser.Cond_opContext):
        op1 = ctx.getChild(0).getChild(0)
        op2 = ctx.getChild(2).getChild(0)

        if self.nodeTypes[op1] != "boolean" and self.nodeTypes[op2] != "boolean":
            self.add_errors("Type error", "operands must be bool type", ctx.start.line)
        
        self.nodeTypes[ctx] = "boolean"


    def exitLocation(self, ctx: DecafParser.LocationContext):
        child = ctx.getChild(0).getText()
        val = self.table.get_entry({"name": child, "scope": self.table.currentScope})
        self.nodeTypes[ctx] = val.varType
    
    def exitProgram(self, ctx: DecafParser.ProgramContext):
        scopes = self.table.table.keys()
        if "main" not in scopes:
            self.add_errors("Missing method", "missing main() method", ctx.start.line)


