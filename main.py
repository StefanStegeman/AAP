from lexer import Lex
from Parser.parser import Parse
from interpreter import VisitNode
from context import Context

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
    while True:
        context = Context()
        text = input('>')
        tokens = Lex(text)
        ast = Parse(tokens, index=0)
        result = VisitNode(ast, context)
        Print(result, tokens, ast)