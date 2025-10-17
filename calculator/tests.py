# calculator/tests.py

# This script contains unit tests for the Calculator class.
# It uses Python's built-in 'unittest' framework to systematically test
# the functionality of the calculator's evaluation logic.

import unittest
# Import the Calculator class that we want to test.
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    """
    A test suite for the Calculator class.
    """

    def setUp(self):
        """
        This method is called before each test function is executed.
        It's used to set up a clean state for every test.
        Here, we create a new instance of the Calculator for each test.
        """
        self.calculator = Calculator()

    # --- Test Cases for Valid Expressions ---

    def test_addition(self):
        """Tests a simple addition operation."""
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        """Tests a simple subtraction operation."""
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        """Tests a simple multiplication operation."""
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        """Tests a simple division operation."""
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        """Tests an expression with multiple operators to check precedence."""
        # Note: Based on the custom precedence in calculator.py, this will be 17.
        # If precedence were standard (e.g., + and * same level), this might be different.
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        """Tests a more complex expression with multiple operators."""
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    # --- Test Cases for Edge Cases and Errors ---

    def test_empty_expression(self):
        """Tests that an empty string returns None."""
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        """Tests that an expression with an unknown operator raises a ValueError."""
        # 'with self.assertRaises(ValueError)' checks that the code inside this
        # block correctly raises a ValueError. The test fails if it doesn't.
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        """Tests that an expression with a missing operand raises a ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")


# Standard Python entry point to run the tests when the script is executed.
if __name__ == "__main__":
    unittest.main()