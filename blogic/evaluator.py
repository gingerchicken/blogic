from .tokeniser import *

def evaluate_postfix(postfix_tokens : list, variables : dict) -> bool:
    """Evaluate the postfix tokens"""
    
    stack = []
    
    for token in postfix_tokens:
        # Handle variables
        if isinstance(token, Variable):
            # Get the variable's value
            val = variables[token.name]

            # Push the value
            stack.append(val)

            continue
        
        # Handle not
        if isinstance(token, Not):
            # Get the argument
            arg = stack.pop()

            # Evaluate
            stack.append(not arg)

            continue

        # Handle operators
        if isinstance(token, Operator):
            # Get the arguments
            arg2 = stack.pop()
            arg1 = stack.pop()

            # Evaluate
            stack.append(token.perform(arg1, arg2))

            continue
        
        # Failure
        raise ValueError("Invalid token")

    return stack.pop()

def evaluate(expression : str, variables : dict) -> bool:
    """Evaluate the expression"""
    
    # Tokenise
    tokens = tokenise(expression)
    
    # Shunt
    postfix_tokens = shunt(tokens)
    
    # Evaluate
    return evaluate_postfix(postfix_tokens, variables)

def evaluate_all(expressions : str, sort_vars : bool = False) -> list:
    """Generates a truth table for the expressions"""
    
    # Tokenise
    tokens = tokenise(expressions)

    # Shunt
    postfix_tokens = shunt(tokens)

    # Get the variables
    variables = set()

    # Get the variables
    for token in tokens:
        if not isinstance(token, Variable):
            continue

        variables.add(token.name)
    
    # Get the number of variables
    num_variables = len(variables)

    # Get the number of rows (i.e. 2^num_variables)
    num_rows = 2 ** num_variables

    # Get the variable names
    variables = list(variables)

    # Sort the variables
    if sort_vars:
        variables.sort()

    # Truth table
    truth_table = []

    # Iterate over the rows
    for row in range(num_rows):
        # Convert the row to a binary string
        binary = bin(row)[2:].zfill(num_variables)

        # Create the variables with their values
        variables_dict = {}

        # Iterate over the variables
        for i, var in enumerate(variables):
            # Get the value
            val = binary[i] == "1"

            # Add it to the variables dict
            variables_dict[var] = val
        
        # Evaluate
        result = evaluate_postfix(postfix_tokens, variables_dict)

        # Add the row to the truth table
        truth_table.append([variables_dict, result])
    
    # Return the truth table
    return truth_table