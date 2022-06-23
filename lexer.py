from tokens import *
from typing import List

class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text

    def SplitText(self) -> List[str]:
        return self.text.split(' ')

    def IsFloat(self, string: str) -> bool:
        try:
            float(string)
            return True
        except ValueError:
            return False

    def CreateTokens(self, lst: List[str]) -> List[Token]:
        tokens = []
        if not lst:
            return tokens
        i = 0
        while i < len(lst):
            current_word = lst[i]
            if current_word.isdigit():
                tokens.append(Int(current_word))
            elif self.IsFloat(current_word):
                tokens.append(Float(current_word))
            else:
                try:
                    tokens.append(TokenValues[current_word]())
                except:
                    tokens.append(Identifier(current_word))
            i += 1
        tokens.append(EOF())
        return tokens