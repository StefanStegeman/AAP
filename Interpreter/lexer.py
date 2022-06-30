from Interpreter.tokens import *
from typing import Callable, List, TypeVar

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def Lex(text: str = None, filename: str = None) -> List[Token]:
    """ Lex the file or text which has been passed into the function.
    Parameters:
        text (str): A line of text which can be lexed into tokens.
        filename (str): The filename which contains the text which can be lexed into tokens.
    Returns:
        tokens (lst): A list with all the tokens.
    """
    if text == None:
        text = ReadFile(filename)
    return AssignTokens(CreateTokens(SplitLine, text))

def SplitLine(line: str) -> List[str]:
    """ Split the passed line into seperate strings.
    NewLines are important to add to the list of strings since
    they otherwise won't be recognized into a NewLine token.
    Parameters:
        line (str): The line which will be split into tokens.
    Returns:
        elements (lst): The list with all seperated strings.
    """
    if not line:
        return [""]
    head, *tail = line
    elements = SplitLine(tail)
    if head in " \t\r":
        elements = [""] + elements
    elif head in "\n":
        elements = [head[:-1]] + [head[-1]] + elements
    else:
        word = head + elements[0]
        elements[0] = word
    return elements

def CreateTokens(f: Callable[[A, B], C], text) -> List[Token]:
    """ Create tokens by calling a function on all elements of the list.
    Parameters:
        f (Callable): The function which get's called on all elements.
    Returns:
        tokens (lst): ALl the tokens which have been created.
    """
    if not text:
        return []
    return CreateTokens(f, text[:-1]) + f(text[-1])

def ReadFile(filename: str) -> List[str]:
    """ Read file and convert it to a list with strings.
    Parameters:
        filename (str): The name of the file which will be read.
    Returns:
        lines (lst): A list filled with all lines from the file.
    """
    with open(filename, "r") as file:
        return file.read().splitlines(True)

def IsFloat(string: str) -> bool:
    """ Check if the passed string is a float.
    Parameters:
        string (str): The string which will be checked.
    Returns:
        float (bool) : Whether the passed string is a float.    
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def AssignTokens(lst: List[str], tokens: List[Token] = []) -> List[Token]:
    """ Assign tokens from the list of strings to the tokens list.
    Parameters:
        lst (Lst): List filled with strings which will be converted.
        tokens (Lst): List filled with all tokens.
    Returns:
        tokens (Lst) : List filled with all tokens.
    """
    if not lst:
        return tokens + [EOF()]
    head, *tail = lst
    if head.isdigit():
        return AssignTokens(tail, tokens + [Int(head)])
    elif IsFloat(head):
        return AssignTokens(tail, tokens + [Float(head)])
    else:
        try:
            tokens.append(TokenValues[head]())
        except:
            if head == "":
                return AssignTokens(tail, tokens)
            tokens.append(Identifier(head))
        return AssignTokens(tail, tokens)