from typing import Union
from Interpreter.context import Context

class Number:
    """ The Number class contains all data and all the functions which can be applied to a number. """

    def __init__(self, value: Union[int, float], context: Context = None) -> None:
        """ Store the passed value and context. 
        
        Parameters:
            value (int, float) : The value for the number.
            context (Context)  : The existing context.
        """
        self.value = value
        self.context = context

    def __repr__(self) -> str:
        return f'{self.value}'

    def __str__(self) -> str:
        return f'{self.value}'

    def Plus(self, other):
        """ This function adds other.value with self.value. 
        
        Parameters:
            other (Number) : The other number to add with.

        Returns:
            number (Number): The result of the operation.
        """
        return Number(self.value + other.value, self.context)

    def Minus(self, other):
        """ This function subtracts other.value with self.value. 
        
        Parameters:
            other (Number) : The other number to subtract with.

        Returns:
            number (Number): The result of the operation.
        """
        return Number(self.value - other.value, self.context)

    def Multiply(self, other):
        """ This function multiplies self.value with other.value. 
        
        Parameters:
            other (Number) : The other number to multiply with.

        Returns:
            number (Number): The result of the operation.
        """
        return Number(self.value * other.value, self.context)

    def Divide(self, other):
        """ This function divides self.value with other.value. 
        
        Parameters:
            other (Number) : The other number to divide with.

        Returns:
            number (Number): The result of the operation.
        """
        return Number(self.value / other.value, self.context)

    def Equals(self, other):
        """ This function checks whether self.value is equal compared with other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value == other.value), self.context)
    
    def NotEquals(self, other):
        """ This function checks whether self.value is not equal compared to other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value != other.value), self.context)

    def GreaterThan(self, other):
        """ This function checks whether self.value is greater than other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value > other.value), self.context)

    def GreaterThanEquals(self, other):
        """ This function checks whether self.value is greater than or equal to other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value >= other.value), self.context)

    def LessThan(self, other):
        """ This function checks whether self.value is less than other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value < other.value), self.context)

    def LessThanEquals(self, other):
        """ This function checks whether self.value is less than or equal to other.value. 
        
        Parameters:
            other (Number) : The other number to compare with.

        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value <= other.value), self.context)

    def And(self, other):
        """ This function checks whether self.value and other.value are true. 
        
        Parameters:
            other (Number) : The other number to compare with.

        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value and other.value), self.context)

    def Or(self, other):
        """ This function checks whether self.value or other.value are true. 
        
        Parameters:
            other (Number) : The other number to compare with.

        Returns:
            number (Number): The result of the operation. This can be either 1 (true) or 0 (false)
        """
        return Number(int(self.value or other.value), self.context)

    def IsTrue(self) -> bool:
        """ This function checks whether self.value is true. 
        
        Returns:
            number (Number): The result of the check. This can be either 1 (true) or 0 (false)
        """
        return self.value != 0

Number.null = Number(0)
Number.true = Number(1)
Number.false = Number(0)