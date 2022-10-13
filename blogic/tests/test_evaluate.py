import unittest

from ..evaluator import *

class TestEvaluate(unittest.TestCase):
    def test_simple(self):
        """Works with simple formula"""
        
        expression = "'True' AND 'False'"

        # get the result
        result = evaluate(expression, {
            'True': True,
            'False': False
        })

        self.assertEqual(result, False)
    
    def test_brackets(self):
        """Works with simple brackets"""
        
        expression = "('True' AND 'False') OR 'True'"

        # get the result
        result = evaluate(expression, {
            'True': True,
            'False': False
        })

        self.assertEqual(result, True)
    
    def test_nested_brackets(self):
        """Works with nested brackets"""
        
        expression = "('True' AND ('False' OR 'True')) OR 'False'"

        # get the result
        result = evaluate(expression, {
            'True': True,
            'False': False
        })

        self.assertEqual(result, True)
    
    def test_same_line(self):

        expression = "'A' AND 'B' OR 'C'"

        self.assertEqual(evaluate(expression, {
            'A': True,
            'B': False,
            'C': True
        }), True)

        self.assertEqual(evaluate(expression, {
            'A': True,
            'B': False,
            'C': False
        }), False)

        self.assertEqual(evaluate(expression, {
            'A': False,
            'B': True,
            'C': False
        }), False)
    
    def test_negated(self):
        """Works with negated variables"""
        
        expression = "-'A'"

        # get the result
        result = evaluate(expression, {
            'A': True
        })
        
        self.assertEqual(result, False)

        # get the result
        result = evaluate(expression, {
            'A': False
        })

        self.assertEqual(result, True)
    
    def test_negated_brackets(self):
        """Works with negated variables"""
        
        expression = "-('A' AND 'B')"

        # get the result
        result = evaluate(expression, {
            'A': True,
            'B': True
        })
        
        self.assertEqual(result, False)

        # get the result
        result = evaluate(expression, {
            'A': True,
            'B': False
        })

        self.assertEqual(result, True)
    
    def test_mixed_negation(self):
        """Works with negated variables"""
        
        expression = "-('A' AND -'B')"

        self.assertEqual(evaluate(expression, {
            'A': True,
            'B': True
        }), True)

        self.assertEqual(evaluate(expression, {
            'A': True,
            'B': False
        }), False)

        self.assertEqual(evaluate(expression, {
            'A': False,
            'B': True
        }), True)

        self.assertEqual(evaluate(expression, {
            'A': False,
            'B': False
        }), True)
    
    def test_mixed_negation_var(self):
        """Works with negated variables"""
        
        expression = "'A' AND 'B' OR -'C'"

        self.assertEqual(evaluate(expression, {
            'A': True,
            'B': True,
            'C': True
        }), True)

        self.assertEqual(evaluate(expression, {
            'A': True,
            'B': False,
            'C': True
        }), False)

        self.assertEqual(evaluate(expression, {
            'A': False,
            'B': True,
            'C': False
        }), True)

        self.assertEqual(evaluate(expression, {
            'A': False,
            'B': False,
            'C': False
        }), True)
    
    def test_no_variables(self):
        """Works with no variables"""
        
        expression = "()"

        # get the result
        result = evaluate(expression, {})
        
        self.assertEqual(result, None)
    
    def test_no_variables_excessive_brackets(self):
        """Doesn't break with excessive brackets"""
        
        expression = "(" * 100 + "()" + ")" * 100

        # get the result
        result = evaluate(expression, {})
        
        self.assertEqual(result, None)
    
    def test_excessive_brackets(self):
        """Doesn't break with excessive brackets"""
        amount = 10 ** 5 # 100,000 brackets (each side)
        expression = "(" * (amount) + "'A'" + ")" * (amount)

        self.assertTrue(evaluate(expression, {
            'A': True
        }))

        self.assertFalse(evaluate(expression, {
            'A': False
        }))

class TestEvaluateAll(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_simple(self):
        """A AND B OR C"""

        expression = "'A' AND 'B' OR 'C'"

        # get the result
        rows = evaluate_all(expression, sort_vars=True)

        self.assertEqual(rows, [
            [{'A': False,  'B': False,  'C': False}, False],
            [{'A': False,  'B': False,  'C': True},  True],
            [{'A': False,  'B': True,   'C': False}, False],
            [{'A': False,  'B': True,   'C': True},  True],
            [{'A': True,   'B': False,  'C': False}, False],
            [{'A': True,   'B': False,  'C': True},  True],
            [{'A': True,   'B': True,   'C': False}, True],
            [{'A': True,   'B': True,   'C': True},  True]
        ])

    def test_brackets(self):
        """A AND (B OR C)"""

        expression = "'A' AND ('B' OR 'C')"

        # get the result
        rows = evaluate_all(expression, sort_vars=True)

        self.assertEqual(rows, [
            [{'A': False,  'B': False,  'C': False}, False],
            [{'A': False,  'B': False,  'C': True},  False],
            [{'A': False,  'B': True,   'C': False}, False],
            [{'A': False,  'B': True,   'C': True},  False],
            [{'A': True,   'B': False,  'C': False}, False],
            [{'A': True,   'B': False,  'C': True},  True],
            [{'A': True,   'B': True,   'C': False}, True],
            [{'A': True,   'B': True,   'C': True},  True]
        ])
    
    def test_negated(self):
        """-A"""

        expression = "-'A'"

        # get the result
        rows = evaluate_all(expression, sort_vars=True)

        self.assertEqual(rows, [
            [{'A': False}, True],
            [{'A': True},  False]
        ])
    
    def test_negated_brackets(self):
        """-(A AND B)"""

        expression = "-('A' AND 'B')"

        # get the result
        rows = evaluate_all(expression, sort_vars=True)

        self.assertEqual(rows, [
            [{'A': False,  'B': False}, True],
            [{'A': False,  'B': True},  True],
            [{'A': True,   'B': False}, True],
            [{'A': True,   'B': True},  False]
        ])
    
    def test_mixed_negation(self):
        """-(A AND -B) OR C"""

        expression = "-('A' AND -'B') OR 'C'"

        # get the result
        rows = evaluate_all(expression, sort_vars=True)

        self.assertEqual(rows, [
            [{'A': False,  'B': False,  'C': False}, True],
            [{'A': False,  'B': False,  'C': True},  True],
            [{'A': False,  'B': True,   'C': False}, True],
            [{'A': False,  'B': True,   'C': True},  True],
            [{'A': True,   'B': False,  'C': False}, False],
            [{'A': True,   'B': False,  'C': True},  True],
            [{'A': True,   'B': True,   'C': False}, True],
            [{'A': True,   'B': True,   'C': True},  True]
        ])
    
    def test_xor(self):
        """A XOR B"""

        expression = "'A' XOR 'B'"

        # get the result
        rows = evaluate_all(expression, sort_vars=True)

        self.assertEqual(rows, [
            [{'A': False,  'B': False}, False],
            [{'A': False,  'B': True},  True],
            [{'A': True,   'B': False}, True],
            [{'A': True,   'B': True},  False]
        ])
    
    def test_all(self):
        expression = """'A' AND "B" OR - ("C" XOR "D")"""

        # get the result
        rows = evaluate_all(expression, sort_vars=True)

        self.assertEqual(rows, [
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
        ])

    def test_implication(self):
        expression = "'A' IMP 'B'"

        # get the result
        rows = evaluate_all(expression, sort_vars=True)

        self.assertEqual(rows, [
            [{'A': False, 'B': False}, True],
            [{'A': False, 'B': True},  True],
            [{'A': True,  'B': False}, False],
            [{'A': True,  'B': True},  True]
        ])
    
    def test_equivalence(self):
        expression = "'A' IFF 'B'"

        # get the result
        rows = evaluate_all(expression, sort_vars=True)

        self.assertEqual(rows, [
            [{'A': False, 'B': False}, True],
            [{'A': False, 'B': True},  False],
            [{'A': True,  'B': False}, False],
            [{'A': True,  'B': True},  True]
        ])