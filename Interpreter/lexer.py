from Interpreter.tokens import *
from typing import Callable, List

def Lex(text: str = None, filename: str = None) -> List[Token]:
    """ Lex the file or text which has been passed into the function.
    Parameters:
        text (str)     : A line of text which can be lexed into tokens.
        filename (str) : The filename which contains the text which can be lexed into tokens.
    
    Returns:
        tokens (Lst) : A list with all the tokens.
    """
    if text == None:
        text = ReadFile(filename)
    return AssignTokens(CreateTokens(SplitLine, text))

def SplitLine(line: str) -> List[str]:
    """ Split the passed line into tokens.
    Parameters:
        line (str)   : The line which will be split into tokens.
    
    Returns:
        tokens (Lst) : The list with all the tokens.
    """
    if not line:
        return [""]
    head, *tail = line
    lst = SplitLine(tail)
    if head in " \t\r":
        lst = [""] + lst
    elif head in "\n":
        lst = [head[:-1]] + [head[-1]] + lst
    elif head in ":":
        lst = ["\n"] + lst
    else:
        word = head + lst[0]
        lst[0] = word
    return lst

def CreateTokens(f: Callable, text) -> List[Token]:
    """ Create tokens by calling a function on all elements of the list.
    Parameters:
        f (Callable) : The function which get's called on all elements of the 
    Returns:
    
    """
    if not text:
        return []
    return CreateTokens(f, text[:-1]) + f(text[-1])

def ReadFile(filename: str) -> List[str]:
    """ Read file and convert it to a list with strings.
    Parameters:
        filename (str) : The filename of the file which will be read.
    
    Returns:
        list (lst)     : A list filled with all lines from the file.
    """
    with open(filename, "r") as file:
        return file.read().splitlines(True)

def IsFloat(string: str) -> bool:
    """ Check if the passed string is a float.
    Parameters:
        string (str) : The string which will be checked.

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
        lst (Lst)    : List filled with strings which will be converted.
        tokens (Lst) : List filled with all tokens.

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