class Token:
    def __str__(self) -> str:
        return f'{self.__class__.__name__}:{self.value}'

class Int(Token):
    def __init__(self, value) -> None:
        self.value = int(value)

class Float(Token):
    def __init__(self, value) -> None:
        self.value = float(value)

class Identifier(Token):
    def __init__(self, value) -> None:
        self.value = value

class Plus(Token):
    value = "+"

class Minus(Token):
    value = "-"

class Multiply(Token):
    value = "*"

class Divide(Token):
    value = "/"

class LPar(Token):
    value = "OpenBanane"

class RPar(Token):
    value = "CloseBanane"

class EOF(Token):
    value = ""

class Variable(Token):
    value = "Ape"

class Comma(Token):
    value = ","

class Arrow(Token):
    value = "->"

class FunctionDef(Token):
    value = "Wife"
    
class Assign(Token):
    value = "Is"

class Equals(Token):
    value = "=="

class NotEquals(Token):
    value = "!="

class GreaterThan(Token):
    value = ">"

class GreaterThanEquals(Token):
    value = ">="

class LessThan(Token):
    value = "<"

class LessThanEquals(Token):
    value = "<="

class And(Token):
    value = "And"

class Or(Token):
    value = "Or"

class If(Token):
    value = "If"

class Elif(Token):
    value = "Elif"

class Else(Token):
    value = "Else"

class Then(Token):
    value = "Then"

class While(Token):
    value = "SpinWhile"

class Run(Token):
    value = "Run"

class Return(Token):
    value = "Throw"

class NewLine(Token):
    value = "\n"

class EndFunction(Token):
    value = "StopWife"

class EndIf(Token):
    value = "StopIf"

class EndWhile(Token):
    value = "StopSpinning"

TokenValues = {Plus.value: Plus, Minus.value: Minus, Multiply.value: Multiply, Divide.value: Divide, LPar.value: LPar, RPar.value: RPar, Assign.value: Assign, Variable.value: Variable, Equals.value: Equals, NotEquals.value: NotEquals, GreaterThan.value: GreaterThan, GreaterThanEquals.value: GreaterThanEquals, LessThan.value: LessThan, LessThanEquals.value: LessThanEquals, And.value: And, Or.value: Or, If.value: If, Elif.value: Elif, Else.value: Else, Then.value: Then, While.value: While, Comma.value: Comma, FunctionDef.value: FunctionDef, Arrow.value: Arrow, Run.value : Run, Return.value: Return, NewLine.value: NewLine, EndFunction.value : EndFunction, EndIf.value : EndIf, EndWhile.value : EndWhile}