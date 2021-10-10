"""
Symbol Table:
{Entry.name: {...} }
"""
class TableItem():
    """
    name: nombre de la variable.
    varType: Tipo de variable.
    num: cantidad de veces a ser declarado.
    isParam: True si es parametro, False si no lo es.
    size: Tamaño de la variable.
    offset: offset de memoria para proyecto 2.
    scope: Ambito de la variable
    isArray: Si es un array o no, True, false.
    """
    def __init__(self, varType, name, num, decafType, size, isArray, offset):
        self.varType = varType
        self.name = name 
        self.value = None
        self.num = num
        self.decafType = decafType
        self.size = size
        self.isArray = isArray
        self.offset = offset
        
        

class StructTableItem():
    def __init__(self, structId, structMembers):
        self.structId = structId
        self.structMembers = structMembers
        self.size = 0

class ScopeTableItem():
    def __init__(self, parentKey, symbolTable, returnType):
        self.parent = parentKey
        self.returnType = returnType
        self.symbolTable = symbolTable



