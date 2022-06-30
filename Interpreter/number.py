from typing import Union
from Interpreter.context import Context

class Number:
    def __init__(self, value: Union[int, float], context: Context = None) -> None:
        """ Store the passed value and context. 
        Parameters:
            value (int, float): The value for the number.
            context (Context): The existing context.
        """
        self.value = value
        self.context = context

    def __str__(self) -> str:
        """ Represents self.value as a string. """
        return f'{self.value}'

    def Plus(self, other: 'Number') -> 'Number':
        """ This function adds other.value with self.value. 
        Parameters:
            other (Number): The other number to add with.
        Returns:
            number (Number): The result of the operation as a new Number.
        """
        return Number(self.value + other.value, self.context)

    def Minus(self, other: 'Number') -> 'Number':
        """ This function subtracts other.value with self.value. 
        Parameters:
            other (Number): The other number to subtract with.
        Returns:
            number (Number): The result of the operation as a new Number.
        """
        return Number(self.value - other.value, self.context)

    def Multiply(self, other: 'Number') -> 'Number':
        """ This function multiplies self.value with other.value. 
        Parameters:
            other (Number): The other number to multiply with.
        Returns:
            number (Number): The result of the operation as a new Number.
        """
        return Number(self.value * other.value, self.context)

    def Divide(self, other: 'Number') -> 'Number':
        """ This function divides self.value with other.value. 
        Parameters:
            other (Number): The other number to divide with.
        Returns:
            number (Number): The result of the operation as a new Number.
        """
        return Number(self.value / other.value, self.context)

    def Equals(self, other: 'Number') -> 'Number':
        """ This function checks whether self.value is equal compared with other.value. 
        Parameters:
            other (Number): The other number to compare with.
        Returns:
            number (Number): The result of the operation as a new Number. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value == other.value), self.context)
    
    def NotEquals(self, other: 'Number') -> 'Number':
        """ This function checks whether self.value is not equal compared to other.value. 
        Parameters:
            other (Number): The other number to compare with.
        Returns:
            number (Number): The result of the operation as a new Number. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value != other.value), self.context)

    def GreaterThan(self, other: 'Number') -> 'Number':
        """ This function checks whether self.value is greater than other.value. 
        Parameters:
            other (Number): The other number to compare with.
        Returns:
            number (Number): The result of the operation as a new Number. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value > other.value), self.context)

    def GreaterThanEquals(self, other: 'Number') -> 'Number':
        """ This function checks whether self.value is greater than or equal to other.value. 
        Parameters:
            other (Number): The other number to compare with.
        Returns:
            number (Number): The result of the operation as a new Number. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value >= other.value), self.context)

    def LessThan(self, other: 'Number') -> 'Number':
        """ This function checks whether self.value is less than other.value. 
        Parameters:
            other (Number): The other number to compare with.
        Returns:
            number (Number): The result of the operation as a new Number. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value < other.value), self.context)

    def LessThanEquals(self, other: 'Number') -> 'Number':
        """ This function checks whether self.value is less than or equal to other.value. 
        Parameters:
            other (Number): The other number to compare with.
        Returns:
            number (Number): The result of the operation as a new Number. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value <= other.value), self.context)

    def And(self, other: 'Number') -> 'Number':
        """ This function checks whether self.value and other.value are true. 
        Parameters:
            other (Number): The other number to compare with.
        Returns:
            number (Number): The result of the operation as a new Number. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value and other.value), self.context)

    def Or(self, other: 'Number') -> 'Number':
        """ This function checks whether self.value or other.value are true. 
        Parameters:
            other (Number): The other number to compare with.
        Returns:
            number (Number): The result of the operation as a new Number. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value or other.value), self.context)

    def IsTrue(self) -> bool:
        """ This function checks whether self.value is true. 
        Returns:
            number (Number): The result of the check. This can be either 1 (true) or 0 (false)
        """
        return self.value != 0