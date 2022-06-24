class NumberNode:
    def __init__(self, token) -> None:
        self.token = token
    
    def __repr__(self):
        return f'{self.token}'

class BinaryOperationNode:
    def __init__(self, left, operator, right) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f'({self.left}, {self.operator}, {self.right})'

class VariableAssignNode:
    def __init__(self, token, node) -> None:
        self.token = token
        self.node = node

class VariableAccessNode:
    def __init__(self, token: str) -> None:
        self.token = token

class IfNode:
    def __init__(self, cases, elseCase) -> None:
        self.cases = cases
        self.elseCase = elseCase
        
class WhileNode:
    def __init__(self, condition, body) -> None:
        self.condition = condition
        self.body = body

class FunctionAssignNode:
    def __init__(self, token, arguments, body):
        self.token = token
        self.arguments = arguments
        self.body = body

class FunctionCallNode:
    def __init__(self, node, arguments):
        self.node = node
        self.arguments = arguments