class Token:
    """Base class for all tokens"""

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return self.value

class Bracket(Token):
    def __init__(self, value):
        if value not in ("(", ")"):
            raise ValueError("Invalid bracket")
        
        super().__init__(value)

    def is_left(self):
        return self.value == "("
    
    def is_right(self):
        return self.value == ")"

class Operator(Token):
    precedence = 1

    def perform(self, a : bool, b : bool) -> bool:
        raise NotImplementedError()

class And(Operator):
    symbol = "AND"

    def __init__(self):
        super().__init__(And.symbol)

    def perform(self, a: bool, b: bool) -> bool:
        return a and b

class Or(Operator):
    symbol = "OR"

    def __init__(self):
        super().__init__(Or.symbol)

    def perform(self, a: bool, b: bool) -> bool:
        return a or b

class Xor(Operator):
    symbol = "XOR"

    def __init__(self):
        super().__init__(Xor.symbol)

    def perform(self, a: bool, b: bool) -> bool:
        return a ^ b

class Not(Operator):
    symbol = "-"

    # Please note that this is not a typical operator, it just needs
    # to be sorted with higher precedence than the other operators

    precedence = 2

    def __init__(self):
        super().__init__(self.symbol)
    
    def perform(self, a: bool) -> bool:
        return not a

class IfAndOnlyIf(Operator):
    symbol = "IFF"

    def __init__(self):
        super().__init__(self.symbol)
    
    def perform(self, a: bool, b: bool) -> bool:
        return a == b

class Implies(Operator):
    symbol = "IMP"

    def __init__(self):
        super().__init__(self.symbol)
    
    def perform(self, a: bool, b: bool) -> bool:
        return not a or b

class Variable(Token):
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
BRACKETS = ["(", ")"]
STRING_OPENERS = ['"', "'"]