from number import Number
from lexer import Lex
from Parser.parser import Parse
from interpreter import VisitNode
from context import Context, SymbolDictionary

def Print(result, tokens = None, ast = None):
    if tokens == None and ast == None:
        print(result)
    elif tokens != None and ast == None:
        print("Tokens:")
        print(tokens, '\n')
        print("Result:", result)
    elif tokens != None and ast != None:
        print("Tokens:")
        print(tokens, '\n')
        print("AST:")
        print(ast, '\n')
        print("Result:", result)

if __name__ == '__main__':
    symbols = SymbolDictionary()
    context = Context()
    context.symbolDictionary = symbols
    symbols.SetValue("True", Number(1))
    symbols.SetValue("False", Number(0))

    tokens = Lex(filename="main.AAP")
    ast = Parse(tokens, index=0)
    print(VisitNode(ast, context))
    # while True:
    #     text = input('>')
    #     tokens = Lex(text)
    #     print(tokens)
        # ast = Parse(tokens, index=0)
        # result = VisitNode(ast, context)
        # if result:
        #     Print(result, tokens, ast)