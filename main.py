from Compiler.compiler import Compile
from Compiler.number import Number
from Interpreter.context import Context, SymbolDictionary
from Interpreter.interpreter import VisitNode
from Interpreter.lexer import Lex
from Interpreter.parser import Parse
from Interpreter.nodes import *
import sys
from typing import List

def InterpretFile(filename: str) -> List[Number]:
    """ Read and interpret a .AAP file.
    Haskell:
        InterpretFile :: String -> [Number]
    This contains three steps:
        - Create tokens with the Lexer.
        - Create an AST from the tokens with the Parser.
        - Interpret the AST with the Interpreter.
    Parameters:
        filename (str): The name of the file which needs to be interpreted.
    Returns:
        result (Lst): List filled with all returned values.
    """
    tokens = Lex(filename=filename)
    ast = Parse(tokens, index=0)
    result = VisitNode(ast, context)
    return result

def CompileFile(input: str, output: str) -> None:
    """ Read and compile a .AAP file.
    Haskell:
        CompileFile :: String -> String -> None
    This contains three steps:
        - Create tokens with the Lexer.
        - Create an AST from the tokens with the Parser.
        - Compile the AST with the Compiler.
    Parameters:
        input (str): The name of the file which needs to be interpreted.
        output (str): The name of the file where the assembler code will be written to.
    """
    tokens = Lex(filename=input)
    ast = Parse(tokens, index=0)
    print(VisitNode(ast, context))
    node = ast.elements[0]
    Compile(output, node, ast)

if __name__ == '__main__':
    symbols = SymbolDictionary()
    context = Context()
    context.symbolDictionary = symbols

    if len(sys.argv) == 2:
        print(InterpretFile(sys.argv[1]))
    elif len(sys.argv) == 3:
        CompileFile(sys.argv[1], sys.argv[2])
    else:
        print("Expected atleast an inputfile.\n")
        print(InterpretFile("main.AAP"))