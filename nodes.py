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