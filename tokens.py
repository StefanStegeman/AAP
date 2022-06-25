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
    value = "("

class RPar(Token):
    value = ")"

class EOF(Token):
    value = ""

class Variable(Token):
    value = "MONKE"

class Comma(Token):
    value = ","

class Arrow(Token):
    value = "->"

class FunctionDef(Token):
    value = "WIFE"
    
class Assign(Token):
    value = "="

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
    value = "AND"

class Or(Token):
    value = "OR"

class If(Token):
    value = "IF"

class Elif(Token):
    value = "ELIF"

class Else(Token):
    value = "ELSE"

class Then(Token):
    value = "THEN"

class While(Token):
    value = "WHILE"

class Run(Token):
    value = "RUN"

class Return(Token):
    value = "RETURN"

class ListOpen(Token):
    value = "["

class ListClose(Token):
    value = "]"

class NewLine(Token):
    value = "\n"

class End(Token):
    value = "HOME"

TokenValues = {Plus.value: Plus, Minus.value: Minus, Multiply.value: Multiply, Divide.value: Divide, LPar.value: LPar, RPar.value: RPar, Assign.value: Assign, Variable.value: Variable, Equals.value: Equals, NotEquals.value: NotEquals, GreaterThan.value: GreaterThan, GreaterThanEquals.value: GreaterThanEquals, LessThan.value: LessThan, LessThanEquals.value: LessThanEquals, And.value: And, Or.value: Or, If.value: If, Elif.value: Elif, Else.value: Else, Then.value: Then, While.value: While, Comma.value: Comma, FunctionDef.value: FunctionDef, Arrow.value: Arrow, Run.value : Run, Return.value: Return, ListOpen.value: ListOpen, ListClose.value: ListClose, NewLine.value: NewLine, End.value: End}