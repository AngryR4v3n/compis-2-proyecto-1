#Intermediate code generator class

from DecafParser import DecafParser


class Intermediator:
    def __init__(self, file) -> None:
        self.file = file
        self.f = open(file, 'w')
        

    def writeLine(self, line, tabs=0):
        ident = tabs * '\t'
        self.f.write(f'{ident}{line}\n')

    def write(self, line, tabs=0):
        ident = tabs * '\t'
        self.f.write(f'{ident}{line}')

    def getVariableCode(self, var, scope):
        if scope == 'global':
            return f'G[{var.offset}]'

        elif var.decafType == 'tempVar':
            return var.name
        else: 
            return f'vArr[{var.offset}]'

    def getOperators(self, obj, op1, op2):
        #3 casos por operador: Variable, literal y expresion

        if isinstance(op1, DecafParser.LocationExpContext) or isinstance(op1, DecafParser.LocationContext):
            res1, scope = obj.findSymbolTableEntry(op1.getChild(0).getText(), obj.currentScope)
            res1 = self.getVariableCode(res1, scope)

        elif isinstance(op1, DecafParser.LiteralExpContext):
            res1 = op1.getChild(0).getText()

        elif isinstance(op1, DecafParser.MethodCallExpContext):
            targetName = obj.nodeTempVars[op1.getChild(0)]
            targetTemp, scope = obj.findSymbolTableEntry(targetName, obj.currentScope)
            res1 = self.getVariableCode(targetTemp, scope)

        if isinstance(op2, DecafParser.LocationExpContext) or isinstance(op2, DecafParser.LocationContext):
            res2, scope = obj.findSymbolTableEntry(op2.getChild(0).getText(), obj.currentScope)
            res2 = self.getVariableCode(res2, scope)

        elif isinstance(op2, DecafParser.LiteralExpContext):
            res2 = op2.getChild(0).getText()

        elif isinstance(op2, DecafParser.MethodCallExpContext) or isinstance(op2, DecafParser.OtherIntOpContext) or isinstance(op2, DecafParser.SumOpContext):
            targetName = obj.nodeTempVars[op2]
            targetTemp, scope = obj.findSymbolTableEntry(targetName, obj.currentScope)
            res2 = self.getVariableCode(targetTemp, scope)

        return res1, res2

    
    def getCallers(self, obj, parentCtx, ctx):

        #TODO WHILE CASE
        if isinstance(parentCtx, DecafParser.IfContext):
            for i, child in enumerate(parentCtx.children):
                if child == ctx:
                    idx = i
                    break
            #Si es el ultimo bloque y la cantidad de Block context es mayor a 1, es el false
            blockNumber = parentCtx.block()

            if len(blockNumber) > 1 and idx == len(parentCtx.children) - 1:
                #ELSE
                self.writeLine(f'IF_FALSE_{obj.nest-1}', obj.nest-1)
            else:
                #TRUE
                self.writeLine(f'IF_TRUE_{obj.nest-1}', obj.nest-1)



