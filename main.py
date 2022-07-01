from Compiler.compiler import Compiler
from Compiler.number import Number
from Interpreter.context import Context, SymbolDictionary
from Interpreter.interpreter import VisitNode
from Interpreter.lexer import Lex
from Interpreter.number import Number
from Interpreter.parser import Parse
from Interpreter.nodes import *
from typing import List
import Interpreter.function
import sys

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
    try:
        if len(result) > 1:
            result = list(filter(lambda element: type(element) != Interpreter.function.Function, result))
            if len(result) > 0:
                print(result)
    except:
        if type(result) == Interpreter.function.Function:
            return
        print(result)

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
    node = ast.elements[0]
    compiler = Compiler(node)
    compiler.Compile(ast, output)

if __name__ == '__main__':
    symbols = SymbolDictionary()
    context = Context()
    context.symbolDictionary = symbols

    if len(sys.argv) == 2:
        InterpretFile(sys.argv[1])
    elif len(sys.argv) == 3:
        CompileFile(sys.argv[1], sys.argv[2])
    else:
        InterpretFile("main.AAp")
        # CompileFile("main.AAP", "main.asm")
        print("I need an input file to do anything..")