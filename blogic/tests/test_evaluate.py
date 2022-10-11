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