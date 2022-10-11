# Blogic
A basic implementation of a boolean algebra enumerator in Python.

## Operators
The following operators are supported:
| Operator | Description |
|----------|-------------|
| `AND`    | Logical AND |
| `OR`     | Logical OR  |
| `XOR`    | Logical XOR |
| `-`    | NOTs the next variable |
| `(`      | Starts a new group |
| `)`      | Ends a group |
| `'`      | Marks start of variable name |
| `"`      | Marks start of variable name |
| `\\`     | Escapes the next character |

### Example
The following expression:
```python
# Import the truth table generator
import blogic.evaluator.evaluate_all

# Evaluate the expression
blogic.evaluator.evaluate_all("""'A' AND "B" OR - ("C" XOR "D")""", True)

"""
(Such that the inputs are on the left and the output is on the right)

Output:
[
    [{'A': False, 'B': False, 'C': False, 'D': False}, True],
    [{'A': False, 'B': False, 'C': False, 'D': True},  False],
    [{'A': False, 'B': False, 'C': True,  'D': False}, False],
    [{'A': False, 'B': False, 'C': True,  'D': True},  True],
    [{'A': False, 'B': True,  'C': False, 'D': False}, True],
    [{'A': False, 'B': True,  'C': False, 'D': True},  False],
    [{'A': False, 'B': True,  'C': True,  'D': False}, False],
    [{'A': False, 'B': True,  'C': True,  'D': True},  True],
    [{'A': True,  'B': False, 'C': False, 'D': False}, True],
    [{'A': True,  'B': False, 'C': False, 'D': True},  False],
    [{'A': True,  'B': False, 'C': True,  'D': False}, False],
    [{'A': True,  'B': False, 'C': True,  'D': True},  True],
    [{'A': True,  'B': True,  'C': False, 'D': False}, True],
    [{'A': True,  'B': True,  'C': False, 'D': True},  True],
    [{'A': True,  'B': True,  'C': True,  'D': False}, True],
    [{'A': True,  'B': True,  'C': True,  'D': True},  True]
]
"""

``` 

## Features
- String variable names
- Truth table generation