import unittest

from ..tokeniser import capture_strings, tokenise, shunt, And, Or, Xor

class TestCaptureStrings(unittest.TestCase):
    def test_extracts_strings(self):
        """Extracts correct strings"""

        expression = '"Hello" "World"'
        strings, anond = capture_strings(expression)
        self.assertEqual(strings, ['Hello', 'World'])
    
    def test_extracts_strings_inverted_comma(self):
        """Extracts correct strings"""

        expression = "'Hello' 'World'"
        strings, anond = capture_strings(expression)
        self.assertEqual(strings, ['Hello', 'World'])
    
    def test_extracts_strings_with_spaces(self):
        """Extracts correct strings"""

        expression = '"Hello World" "Hello World"'
        strings, anond = capture_strings(expression)
        self.assertEqual(strings, ['Hello World', 'Hello World'])
    
    def test_extracts_strings_containing_quotes(self):
        """Extracts correct strings"""

        expression = '"I\'m a string"'
        strings, anond = capture_strings(expression)
        self.assertEqual(strings, ["I'm a string"])
        self.assertEqual(anond, '%s')
    
    def test_removes_strings(self):
        """Removes strings"""

        expression = '"Hello" "World"'
        strings, anond = capture_strings(expression)
        self.assertEqual(anond, '%s %s')
    
    def test_removes_strings_inverted_comma(self):
        """Removes strings"""

        expression = "'Hello' 'World'"
        strings, anond = capture_strings(expression)
        self.assertEqual(anond, '%s %s')
    
    def test_leaves_non_strings(self):
        """Leaves non strings"""

        expression = '"Hello" AND "World"'
        strings, anond = capture_strings(expression)
        self.assertEqual(anond, '%s AND %s')
        self.assertEqual(strings, ['Hello', 'World'])
    
    def test_strings_next_to_each_other(self):
        """Extracts neighboring strings"""

        expression = '"Hello""World"'
        strings, anond = capture_strings(expression)
        self.assertEqual(anond, '%s%s')
        self.assertEqual(strings, ['Hello', 'World'])
    
    def test_change_place_holder(self):
        """Changes place holder"""

        expression = '"Hello" AND "World"'
        strings, anond = capture_strings(expression, 'test')
        self.assertEqual(anond, 'test AND test')
        self.assertEqual(strings, ['Hello', 'World'])
    
    def test_escape(self):
        """Handles escapes"""

        expression = '"Hello\\"World"'
        strings, anond = capture_strings(expression)
        self.assertEqual(anond, '%s')
        self.assertEqual(strings, ['Hello"World'])
    
    def test_multiple_escapes(self):
        """Handles multiple escapes"""

        expression = '"Hello\\\\World"'
        strings, anond = capture_strings(expression)
        self.assertEqual(anond, '%s')
        self.assertEqual(strings, ['Hello\\World'])

class TestTokenise(unittest.TestCase):
    def test_tokenise(self):
        """Tokenises correctly"""

        expression = "('Hello' AND 'World') OR \"World\""
        tokens = tokenise(expression)

        self.assertEqual([str(i) for i in tokens], ['(', 'Hello', 'AND', 'World', ')', 'OR', 'World'])
    
    def test_tokenise_ignore_whitespace(self):
        """Tokenises correctly"""

        expression = "('Hello'AND'World')OR\"World\""
        tokens = tokenise(expression)

        self.assertEqual([str(i) for i in tokens], ['(', 'Hello', 'AND', 'World', ')', 'OR', 'World'])

class TestShunt(unittest.TestCase):
    def test_shunt(self):
        """Shunts correctly"""

        expression = "('Hello' AND 'World') OR \"World\""
        tokens = tokenise(expression)
        output = shunt(tokens)

        self.assertEqual([str(i) for i in output], ['Hello', 'World', 'AND', 'World', 'OR'])
    
    def test_shunt_ignore_whitespace(self):
        """Shunts correctly"""

        expression = "('Hello'AND'World')OR\"World\""
        tokens = tokenise(expression)
        output = shunt(tokens)

        self.assertEqual([str(i) for i in output], ['Hello', 'World', 'AND', 'World', 'OR'])
    
    def test_shunt_nested_brackets(self):
        """Shunts correctly"""

        expression = "'Hello' AND ('World' OR 'World')"
        tokens = tokenise(expression)
        output = shunt(tokens)

        self.assertEqual([str(i) for i in output], ['Hello', 'World', 'World', 'OR', 'AND'])
    
    def test_raise_invalid_brackets(self):
        """Raises InvalidBrackets"""

        expression = "'Hello' AND ('World' OR 'World'"
        tokens = tokenise(expression)

        with self.assertRaises(ValueError):
            shunt(tokens)
    
    def test_flat(self):

        expression = "'A' AND 'B' OR 'C'"

        tokens = tokenise(expression)
        output = shunt(tokens)

        self.assertEqual([str(i) for i in output], ['A', 'B', 'AND', 'C', 'OR'])
    
    def test_flat_var(self):
        expression = "'A' AND ('B' OR 'C')"

        tokens = tokenise(expression)
        output = shunt(tokens)

        self.assertEqual([str(i) for i in output], ['A', 'B', 'C', 'OR', 'AND'])

class Operators(unittest.TestCase):
    def test_and(self):
        """AND works"""
    
        a = And()

        self.assertTrue(a.perform(True, True))
        self.assertFalse(a.perform(True, False))
        self.assertFalse(a.perform(False, True))
        self.assertFalse(a.perform(False, False))

    def test_or(self):
        """OR works"""
    
        o = Or()

        self.assertTrue(o.perform(True, True))
        self.assertTrue(o.perform(True, False))
        self.assertTrue(o.perform(False, True))
        self.assertFalse(o.perform(False, False))

    def test_xor(self):
        """XOR works"""
    
        x = Xor()

        self.assertFalse(x.perform(True, True))
        self.assertTrue(x.perform(True, False))
        self.assertTrue(x.perform(False, True))
        self.assertFalse(x.perform(False, False))