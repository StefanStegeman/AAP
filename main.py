import sys
from Interpreter.number import Number
from Interpreter.lexer import Lex
from Interpreter.parser import Parse
from Interpreter.interpreter import VisitNode, Function
from Interpreter.context import Context, SymbolDictionary
from typing import List
# Apes Among Programmers

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
    try:
        if len(result) == 1:
            return result[0]
        else:
            result = list(filter(lambda element: type(element) != Function, result))
            return result
    except:
        return result

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

    print(RunFile("main.AAP"))
    # if len(sys.argv) == 2:
    #     print(RunFile(sys.argv[1]))
    # else:
    #     Shell()