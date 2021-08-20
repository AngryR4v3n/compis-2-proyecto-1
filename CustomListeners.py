from DecafListener import DecafListener
from DecafParser import DecafParser
from antlr4 import TerminalNode


"""
Symbol Table:
{Entry.name: {...} }
"""


class SymbolTable():
    def __init__(self):
        self.table = {"global": {}}
        self.scope = "global"

    # Hay que hacer validaciones no?
    def add_entry(self, entry):

        obj = {
            entry.name: {
                "uid": entry.uid,
                "varType": entry.varType, 
                "name": entry.name, 
                "value": entry.value
            }
        }

        try:
            prevValues = {**self.table[self.scope]}
            print("updating scope")
            add = prevValues | obj
            self.table[self.scope] = prevValues | obj

        except KeyError:
            print("Unexisting scope")
            self.table[self.scope] = { 
                entry.name:{
                    "uid": entry.uid, 
                    "varType": entry.varType, 
                    "value": entry.value
                }
            }

        print(self.table)


"""
Single Entry...
{uid: 13414141, varType: "int", name: "num", value: "1" scope: "global"}
"""


class SymbolTableEntry():
    def __init__(self, uid, varType, name, value, symbolType, scope="global"):
        self.uid = hash(uid)
        self.varType = varType
        self.name = name
        self.scope = scope
        self.value = value
        self.symbolType = symbolType


class CustomListener(DecafListener):
    def __init__(self) -> None:
        self.table = SymbolTable()
        super().__init__()

    def typeValidation(self, varType, varValue):
        pass

    def textExtractor(self, toExtract):
        if toExtract:
            if isinstance(toExtract, TerminalNode):
                return toExtract.symbol.text
            else:
                toExtract = toExtract.getChild(0)
                final = self.textExtractor(toExtract)
                return final
        else:
            return None

    def enterVarDeclaration(self, ctx: DecafParser.VarDeclarationContext):
        varType = self.textExtractor(ctx.getChild(0))
        varName = self.textExtractor(ctx.getChild(1))

        # si se declaro un int a[numero]
        num = self.textExtractor(ctx.NUM())
        if num:
            if int(num) < 0:
                raise Exception("IndexError: Please provide a valid number")

        if len(ctx.children) > 2:
            print("Arr declaration!")
            entry = SymbolTableEntry(
                varName, varType, varName, "Array", "var", scope=self.table.scope)
        else:
            varValue = ctx.getChild(2)
            entry = SymbolTableEntry(
                varName, varType, varName, varValue, "var", scope=self.table.scope)

        self.table.add_entry(entry)

        return super().enterVarDeclaration(ctx)

    def enterMethodDeclaration(self, ctx: DecafParser.MethodDeclarationContext):
        methodReturnType = self.textExtractor(ctx.getChild(0))
        methodName = self.textExtractor(ctx.getChild(1))
        self.table.scope = methodName
        return super().enterMethodDeclaration(ctx)
