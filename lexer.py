from tokens import *
from typing import List

def Lex(text) -> List[Token]:
    return CreateTokens(SplitText(text))

def SplitText(text) -> List[str]:
    return text.split(' ')

def IsFloat(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def CreateTokens(lst: List[str]) -> List[Token]:
    tokens = []
    if not lst:
        return tokens
    i = 0
    while i < len(lst):
        current_word = lst[i]
        if current_word.isdigit():
            tokens.append(Int(current_word))
        elif IsFloat(current_word):
            tokens.append(Float(current_word))
        else:
            try:
                tokens.append(TokenValues[current_word]())
            except:
                tokens.append(Identifier(current_word))
        i += 1
    tokens.append(EOF())
    return tokens