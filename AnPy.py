from DecafListener import Overrider
import sys
from antlr4 import *
from DecafLexer import DecafLexer
from DecafParser import DecafParser
 
"""
Symbol Table:
{Entry.uid: {...} }
"""
class SymbolTable():
    def __init__(self):
        self.table = {}
    def add_entry():
        pass

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
        self.symbolType  = symbolType



def main(argv):
    input_stream = FileStream(argv[1])
    lexer = DecafLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()
    printer = Overrider()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
 
if __name__ == '__main__':
    main(sys.argv)