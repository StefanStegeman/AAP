from tokens import *
from typing import List

def Lex(text: str = None, filename: str = None) -> List[Token]:
    if text == None:
        text = ReadFile(filename)
    return AssignTokens(CreateTokens(SplitLine, text))

def SplitLine(line) -> List[str]:
    if not line:
        return [""]
    head, *tail = line
    lst = SplitLine(tail)
    if head in " \t\r\n":
        lst = [""] + lst
    else:
        word = head + lst[0]
        lst[0] = word
    return lst

def CreateTokens(f, text) -> List[Token]:
    if not text:
        return []
    return CreateTokens(f, text[:-1]) + f(text[-1])

def ReadFile(filename: str) -> List[str]:
    with open(filename, "r") as file:
        return file.read().splitlines(True)

def IsFloat(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def AssignTokens(lst: List[str], tokens: List[Token] = []) -> List[Token]:
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