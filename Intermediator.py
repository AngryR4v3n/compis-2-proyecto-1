#Intermediate code generator class

from DecafParser import DecafParser


class Intermediator:
    def __init__(self, file) -> None:
        self.file = file
        self.f = open(file, 'w')
        self.sizes = {'int': 4, 'char': 1, 'boolean': 1}
        

    def writeLine(self, line, tabs=0):
        ident = tabs * '\t'
        self.f.write(f'{ident}{line}\n')

    def write(self, line, tabs=0):
        ident = tabs * '\t'
        self.f.write(f'{ident}{line}')

    def getVariableCode(self, var, scope, obj=None, fullCall=None, isStruct=False, isArray=False, num=0):
        if scope == 'global':
            return f'G[{var.offset}]'
        #para los t's
        elif var.decafType == 'tempVar':
            return var.name
        #variables normales, solo el offset
        elif not isArray and not isStruct: 
            return f'vArr[{var.offset}]'
        
        #esto no funcionara con arrays de structs
        elif isArray and not isStruct:
            return f'vArr[{var.offset + int(num) * self.sizes[var.varType]}]'

        elif isStruct:

            offset = obj.getStructPropertyOffset(fullCall, var)

            return f'vArr[{offset}]'



    def getOperators(self, obj, op1, op2):
        #3 casos por operador: Variable, literal y expresion
        res1 = None
        res2 = None
        #TODO IDENTIFICAR STRUCTS
        if isinstance(op1, DecafParser.LocationExpContext) or isinstance(op1, DecafParser.LocationContext):
            
            if isinstance(op1, DecafParser.LocationExpContext):
                #Si el hijo del op tiene mas de 1 hijo, es un struct.
                if op1.getChild(0).getChildCount() > 1:
                    res1, scope = obj.findSymbolTableEntry(op1.getChild(0).getChild(0).getText(), obj.currentScope)

                    #Determinamos si es ARRAY
                    if res1.isArray:
                        num = op1.getChild(2).getText()
                        res1 = self.getVariableCode(res1, scope, isArray=True, num=num)
                    else:
                        res1 = self.getVariableCode(res1, scope, fullCall=op1.getChild(0).getText(), obj=obj, isStruct=True)
            else:
                #Aqui el conteo no tiene que ser sobre el hijo si no sobre directamente el objeto
                if op1.getChildCount() > 1:
                    res1, scope = obj.findSymbolTableEntry(op1.getChild(0).getText(), obj.currentScope)


                    #Determinamos si es ARRAY
                    if res1.isArray:
                        num = op1.getChild(2).getText()
                        res1 = self.getVariableCode(res1, scope, isArray=True, num=num)
                    else:
                        res1 = self.getVariableCode(res1, scope, fullCall=op1.getText(), obj=obj, isStruct=True)


                else:
                    res1, scope = obj.findSymbolTableEntry(op1.getChild(0).getText(), obj.currentScope)

                    #Determinamos si es ARRAY
                    if res1.isArray:
                        #cambia el codigo de offset
                        num = op1.getChild(2).getText()
                        res1 = self.getVariableCode(res1, scope, isArray=True, num=num)
                    else:
                        res1 = self.getVariableCode(res1, scope)


        #si son literales
        elif isinstance(op1, DecafParser.LiteralExpContext):
            res1 = op1.getChild(0).getText()

        elif isinstance(op1, DecafParser.LiteralContext):
            res1 = op1.getChild(0).getText()
        #si es method call
        elif isinstance(op1, DecafParser.MethodCallExpContext):
            targetName = obj.nodeTempVars[op1.getChild(0)]
            targetTemp, scope = obj.findSymbolTableEntry(targetName, obj.currentScope)
            res1 = self.getVariableCode(targetTemp, scope)

        
        if isinstance(op2, DecafParser.LocationExpContext) or isinstance(op2, DecafParser.LocationContext):
            res2, scope = obj.findSymbolTableEntry(op2.getChild(0).getText(), obj.currentScope)
            #Determinamos si es ARRAY
            if res2.isArray:
                #cambia el codigo de offset
                num = op2.getChild(2).getText()
                res2 = self.getVariableCode(res2, scope, isArray=True, num=num)
            else:
                res2 = self.getVariableCode(res2, scope)

        elif isinstance(op2, DecafParser.LiteralExpContext):
            res2 = op2.getChild(0).getText()

        elif isinstance(op2, DecafParser.LiteralContext):
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
        
        elif isinstance(parentCtx, DecafParser.WhileContext):
            self.writeLine(f'IF_TRUE_{obj.nest-1}', obj.nest-1)

    def getTails(self, obj, parentCtx, ctx):

        if isinstance(ctx, DecafParser.WhileContext):
            self.writeLine(f'GOTO WHILE_{obj.nest-1}', obj.nest+1)
            self.writeLine(f'END WHILE_{obj.nest-1}', obj.nest)

        elif isinstance(ctx, DecafParser.MethodDeclarationContext):
            self.writeLine(f'END {ctx.getChild(1).getText()}')


        

