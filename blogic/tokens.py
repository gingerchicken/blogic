# This file is used to declare what tokens are used in the "language" and how they are handled.

class Token:
    """Base class for all tokens"""

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value

class Bracket(Token):
    """Represents a bracket, either ( or )"""

    def __init__(self, value):
        if value not in ("(", ")"):
            raise ValueError("Invalid bracket")
        
        super().__init__(value)

    def is_left(self):
        return self.value == "("
    
    def is_right(self):
        return self.value == ")"

class Operator(Token):
    """Base class for all operators"""

    precedence = 1

    def perform(self, a : bool, b : bool) -> bool:
        raise NotImplementedError()

class And(Operator):
    """Represents the AND operator"""

    symbol = "AND"

    def __init__(self):
        super().__init__(And.symbol)

    def perform(self, a: bool, b: bool) -> bool:
        return a and b

class Or(Operator):
    """Represents the OR operator"""

    symbol = "OR"

    def __init__(self):
        super().__init__(Or.symbol)

    def perform(self, a: bool, b: bool) -> bool:
        return a or b

class Xor(Operator):
    """Represents the "exclusive or" operator"""

    symbol = "XOR"

    def __init__(self):
        super().__init__(Xor.symbol)

    def perform(self, a: bool, b: bool) -> bool:
        return a ^ b

class Not(Operator):
    """Represents a NOT prefix operator"""

    symbol = "-"

    # Please note that this is not a typical operator, it just needs
    # to be sorted with higher precedence than the other operators

    precedence = 2

    def __init__(self):
        super().__init__(self.symbol)
    
    def perform(self, a: bool) -> bool:
        return not a

class IfAndOnlyIf(Operator):
    """Represents the "if and only if" operator"""

    symbol = "IFF"

    def __init__(self):
        super().__init__(self.symbol)
    
    def perform(self, a: bool, b: bool) -> bool:
        return a == b

class Implies(Operator):
    """Represents an implies/entails operator"""

    symbol = "IMP"

    def __init__(self):
        super().__init__(self.symbol)
    
    def perform(self, a: bool, b: bool) -> bool:
        return not a or b

class Variable(Token):
    """Represents a variable and stores its value"""

    @property
    def name(self):
        return self.value
    
    def __init__(self, name):
        super().__init__(name)

# Define the operators
OPERATORS = {
    And.symbol: And,
    Or.symbol: Or,
    Xor.symbol: Xor,
    IfAndOnlyIf.symbol: IfAndOnlyIf,
    Implies.symbol: Implies
}

# Define what brackets we support
BRACKETS = ["(", ")"]

# Define the quotes we support
STRING_OPENERS = ['"', "'"]