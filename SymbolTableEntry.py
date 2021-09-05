"""
Forma de una entrada en un symbol table
{uid: 13414141, varType: "int", name: "num", value: "1" scope: "global"}
"""
class SymbolTableEntry():
    def __init__(self, varType, name, value, symbolType, parentScope, arrIndex=None, scope="global", isParam=False):
        if not isParam:
            self.id = name+str(arrIndex) if arrIndex else name
        else:
            self.id = name
        self.varType = varType
        self.name = name
        self.value = value
        self.symbolType = symbolType
        self.parentScope = parentScope
        self.scope = scope
        self.arrIndex = arrIndex

    def __repr__(self) -> str:
        return f"{self.varType} {self.name}"