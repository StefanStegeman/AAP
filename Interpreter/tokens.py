class Token:
    """ Base token class. """
    def __str__(self) -> str:
        """ Represent Token as str.
        Returns:
            token (str) : The name of the class and the value of the token. """
        return f'{self.__class__.__name__}:{self.value}'

class Int(Token):
    """ Class for an integer token. """
    def __init__(self, value: str) -> None:
        self.value = int(value)

class Float(Token):
    """ Class for a float token. """
    def __init__(self, value: str) -> None:
        self.value = float(value)

class Identifier(Token):
    """ Class for an identifier token. """
    def __init__(self, value: str) -> None:
        self.value = value

class Plus(Token):
    """ Class which contains the plus token value. """
    value = "+"

class Minus(Token):
    """ Class which contains the minus token value. """
    value = "-"

class Multiply(Token):
    """ Class which contains the multiply token value. """
    value = "*"

class Divide(Token):
    """ Class which contains the divide token value. """
    value = "/"

class LPar(Token):
    """ Class which contains the left parantheses token value. """
    value = "OpenBanane"

class RPar(Token):
    """ Class which contains the left parantheses token value. """
    value = "CloseBanane"

class EOF(Token):
    """ Class for the left EndOfFile token. """
    value = ""

class Variable(Token):
    """ Class which contains the variable token value. """
    value = "Ape"

class Comma(Token):
    """ Class which contains the comma token value. """
    value = ","

class FunctionDef(Token):
    """ Class which contains the function defenition token value. """
    value = "Wife"
    
class Assign(Token):
    """ Class which contains the assign token value. """
    value = "Is"

class Equals(Token):
    """ Class which contains the equal token value. """
    value = "=="

class NotEquals(Token):
    """ Class which contains the not equal token value. """
    value = "!="

class GreaterThan(Token):
    """ Class which contains the greater than token value. """
    value = ">"

class GreaterThanEquals(Token):
    """ Class which contains the greater or equals token value. """
    value = ">="

class LessThan(Token):
    """ Class which contains the less than token value. """
    value = "<"

class LessThanEquals(Token):
    """ Class which contains the less or equals token value. """
    value = "<="

class And(Token):
    """ Class which contains the and token value. """
    value = "And"

class Or(Token):
    """ Class which contains the or token value. """
    value = "Or"

class If(Token):
    """ Class which contains the if token value. """
    value = "If"

class Else(Token):
    """ Class which contains the else token value. """
    value = "Else"

class Then(Token):
    """ Class which contains the then token value. """
    value = "Then"

class While(Token):
    """ Class which contains the while token value. """
    value = "SpinWhile"

class Run(Token):
    """ Class which contains the run token value. """
    value = "Run"

class Return(Token):
    """ Class which contains the return token value. """
    value = "Throw"

class NewLine(Token):
    """ Class which contains the new line token value. """
    value = "\n"

class EndFunction(Token):
    """ Class which contains the end of a function token value. """
    value = "StopWife"

class EndIf(Token):
    """ Class which contains the end of an if statement token value. """
    value = "StopIf"

class EndWhile(Token):
    """ Class which contains the end of a while loop token value. """
    value = "StopSpinning"

TokenValues = {Plus.value: Plus, Minus.value: Minus, Multiply.value: Multiply, Divide.value: Divide, LPar.value: LPar, RPar.value: RPar, Assign.value: Assign, Variable.value: Variable, Equals.value: Equals, NotEquals.value: NotEquals, GreaterThan.value: GreaterThan, GreaterThanEquals.value: GreaterThanEquals, LessThan.value: LessThan, LessThanEquals.value: LessThanEquals, And.value: And, Or.value: Or, If.value: If, Else.value: Else, Then.value: Then, While.value: While, Comma.value: Comma, FunctionDef.value: FunctionDef, Run.value : Run, Return.value: Return, NewLine.value: NewLine, EndFunction.value : EndFunction, EndIf.value : EndIf, EndWhile.value : EndWhile}