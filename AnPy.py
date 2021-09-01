import sys
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from CustomListeners import CustomListener



def main(argv):
    input_stream = FileStream("./tests/fact_array.txt")
    lexer = DecafLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = DecafParser(stream)
    tree = parser.program()
    walker = ParseTreeWalker()
    Customlisteners = CustomListener()
    walker.walk(Customlisteners, tree)

    for elem in Customlisteners.errors:
        print(elem)


def traverse(tree):
    if tree.getText() == "<EOF>":
        return None
    else:
        print(tree.getText())

if __name__ == '__main__':
    main(sys.argv)
