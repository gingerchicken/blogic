import re

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
    Xor.symbol: Xor
}
BRACKETS = ["(", ")"]
STRING_OPENERS = ['"', "'"]

def capture_strings(expression : str, place_holder_prefix = '%s', escape_chars = ['\\']) -> tuple:
    """Gets all strings in a given expression, and replaces them with a placeholder"""

    strings = []
    string = ""
    in_string = False
    escape = False
    start_pos = 0
    open_char = None

    replace_poses = []

    pos = 0
    for char in expression:
        # Increment position
        pos += 1

        # Handle escapes
        if escape:
            string += char
            escape = False
            continue
        
        if char in escape_chars:
            escape = True
            continue
        
        # Handle strings (i.e. remove them)
        
        opener = char in STRING_OPENERS # Is it an opener?
        rel_opener = not (in_string and char != open_char) # Is it a relevant opener?

        if opener and rel_opener:
            # Open the string
            if not in_string:
                # Start capturing the string, ignore the first character
                in_string = True
                open_char = char
                start_pos = pos - 1 # -1 to ignore the first character
                continue # Done
            
            # Otherwise close it ...
            # Add the string
            strings.append(string)

            # Reset the string
            string = ""
            in_string = False
            open_char = None

            # Place the start and end in the replace_poses
            replace_poses.append((start_pos, pos))
            continue # Done

        # If we are in a string, add the character to the string
        if in_string:
            string += char

    if in_string:
        raise ValueError("Unclosed string")   
    
    # Replace the strings with placeholders
    offset = 0
    for start, end in replace_poses:
        # Anonymise the string
        expression = expression[:start + offset] + place_holder_prefix + expression[end + offset:]

        # Increment the offset
        offset += len(place_holder_prefix) - (end - start)
    
    return strings, expression
    
def tokenise(expression : str, str_holder : str = '%s') -> list:
    """Tokenize a given expression"""

    # TODO cache the strings

    # Remove all strings
    strings, anond = capture_strings(expression)

    # Reverse the strings so that the first string is the last one
    # This way we can pop them off the list
    strings.reverse()

    # Remove all whitespace
    anond = anond.replace(" ", "")

    # Generate some regexes for the different tokens
    res = [
        re.compile(r"[\(\)]"),                        # Brackets
        re.compile(r"(" + "|".join(OPERATORS) + ")"), # Operators
        re.compile(r"(" + str_holder + ")"),          # Strings
        re.compile(r"(" + Not.symbol + ")"),          # Not
        re.compile(r"[a-zA-Z0-9_]+")                  # Other
    ]

    # Add them all together into one regex
    regex = re.compile("|".join([i.pattern for i in res]))

    # Tokenise
    tokens = []
    for match in regex.finditer(anond):
        val = str(match.group())
        
        # Brackets
        if val in BRACKETS:
            tokens.append(Bracket(val))
            continue
        
        # Operators
        if val in OPERATORS:
            op = OPERATORS[val] # Get the operator's class
            
            # Create an instance of the operator and add it to the tokens
            tokens.append(op())
            continue

        # Not special case
        if val == Not.symbol:
            # Create a Not instance and add it to the tokens
            tokens.append(Not())
            continue

        # Strings/Vars
        if val == str_holder:
            # Make sure that there is a string to replace it with
            # We could of course check this before we tokenise but this would require a further pass
            if len(strings) == 0:
                raise ValueError("Too many placeholders")

            # Get the string from the list
            val = strings.pop()

            # Add it to the tokens
            tokens.append(Variable(val))
            continue
        
        # Unknown
        raise ValueError("Invalid token: " + val)

    return tokens

def shunt(tokens : list) -> list:
    """Shunt the tokens into reverse polish notation"""

    output = []
    stack = []

    for token in tokens:
        # Handle variables
        if isinstance(token, Variable):
            output.append(token)
            continue

        # Handle brackets
        if isinstance(token, Bracket):
            # Open bracket
            if token.is_left():
                stack.append(token)
                continue
            
            # This should be a right bracket
            if token.is_right():
                while stack and (not isinstance(stack[-1], Bracket) or not stack[-1].is_left()):
                    output.append(stack.pop())
                
                if not stack:
                    raise ValueError("Mismatched brackets")
                
                stack.pop()
                continue
            
            # Unknown bracket
            raise ValueError("Unknown bracket")
        
        # Handle operators (in this case they all have the same precedence)
        if isinstance(token, Operator):
            # Peek
            peek = stack[-1] if stack else None

            while peek and isinstance(peek, Operator) and peek.precedence >= token.precedence:
                output.append(stack.pop())

                # Get the next peek
                peek = stack[-1] if stack else None
            
            stack.append(token)
            continue

        raise ValueError("Invalid token: " + str(token))

    # Pop the rest of the stack
    while stack:
        if isinstance(stack[-1], Bracket):
            raise ValueError("Mismatched brackets")
        
        output.append(stack.pop())
    
    # Return the output
    return output