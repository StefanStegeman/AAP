from lexer import Lexer

if __name__ == '__main__':
    while True:
        text = input('>')
        lexer = Lexer(text)
        tokens = lexer.CreateTokens(lexer.SplitText())
        print(tokens)