import sys
from number import Number
from lexer import Lex
from Parser.parser import Parse
from interpreter import VisitNode
from context import Context, SymbolDictionary

# Apes Among Programmers

def ReadFile(filename: str):
    tokens = Lex(filename=filename)
    ast = Parse(tokens, index=0)
    result = VisitNode(ast, context)
    if len(result.elements) == 1:
        return result.elements[0]
    else:
        return result.elements

def Shell():
    while True:
        text = input('Speak up ape> ')
        if text.strip() == "": 
            continue
        tokens = Lex(text=[text])
        ast = Parse(tokens, index=0)
        result = VisitNode(ast, context)
        if result:
            if len(result.elements) == 1:
                print(result.elements[0])
            else:
                print(result)

if __name__ == '__main__':
    symbols = SymbolDictionary()
    context = Context()
    context.symbolDictionary = symbols
    symbols.SetValue("NULL", Number.null)
    symbols.SetValue("TRUE", Number.true)
    symbols.SetValue("FALSE", Number.false)

    print(ReadFile("main.AAP"))
    # if len(sys.argv) == 2:
    #     print(ReadFile(sys.argv[1]))
    # else:
    #     Shell()