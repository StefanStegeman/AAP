from Compiler.compiler import Compile
from Interpreter.context import Context, SymbolDictionary
from Interpreter.interpreter import VisitNode, Function
from Interpreter.lexer import Lex
from Interpreter.number import Number
from Interpreter.parser import Parse
import sys
from typing import List

def RunFile(filename: str) -> List[int]:
    """ Run and interpret an .AAP file.
    This contains three steps:
        - Create tokens with the Lexer.
        - Create an AST from the tokens with the Parser.
        - Interpret the AST with the Interpreter.
    Parameters:
        filename (str) : The name of the file which needs to be interpreted.

    Returns:
        result (Lst)   : List filled with all returned values.
    """
    tokens = Lex(filename=filename)
    ast = Parse(tokens, index=0)
    result = VisitNode(ast, context)
    # result = list(filter(lambda element: type(element) != Function, result))
    return result
    # try:
    #     if len(result) == 1:
    #         return result[0]
    #     else:
    # except:
    #     return result

def Shell() -> None:
    """ Run the AAP shell. 
    Run the AAP shell which allows you to program in AAP inside of a terminal shell.
    """
    while True:
        text = input('Speak up ape> ')
        if text.strip() == "": 
            continue
        tokens = Lex(text=[text])
        ast = Parse(tokens, index=0)
        result = VisitNode(ast, context)
        print(result)

def CompileFile(inputFilename, outputFilename):
    tokens = Lex(filename=inputFilename)
    ast = Parse(tokens, 0)
    print(VisitNode(ast, context))
    node = ast.elements[0]
    Compile(outputFilename, node, ast)

if __name__ == '__main__':
    symbols = SymbolDictionary()
    context = Context()
    context.symbolDictionary = symbols

    # Compile(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 2:
        print(RunFile(sys.argv[1]))
    elif len(sys.argv) == 3:
        print(CompileFile(sys.argv[1], sys.argv[2]))
    else:
        # CompileFile("main.AAP", "yoghurt.asm")
        Shell()