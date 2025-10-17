# calculator/pkg/calculator.py

# This script contains the core logic for the calculator.
# It uses an infix evaluation algorithm, often referred to as Shunting-yard,
# to correctly handle mathematical expressions with operator precedence.

class Calculator:
    def __init__(self):
        """
        Initializes the Calculator instance.
        """
        # A dictionary mapping operator symbols to their corresponding lambda functions.
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        # A dictionary defining the precedence for each operator.
        # Higher numbers indicate higher precedence (e.g., '*' is done before '+').
        # Note: In a standard shunting-yard, '+' and '-' would have the same precedence.
        # This implementation has a slight variation.
        self.precedence = {
            "+": 3, 
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        """
        Public method to evaluate a mathematical expression given as a string.

        Args:
            expression (str): The mathematical expression to evaluate (e.g., "3 + 5 * 2").

        Returns:
            float: The result of the calculation.
            None: If the expression is empty or just whitespace.
        """
        # Guard clause to handle empty input.
        if not expression or expression.isspace():
            return None
        # Tokenize the expression by splitting it by spaces.
        tokens = expression.strip().split()
        # Call the private method that contains the core evaluation logic.
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        """
        Evaluates a list of tokens using an infix algorithm.
        """
        # Two stacks are used: one for numerical values and one for operators.
        values = []
        operators = []

        # Process each token in the expression.
        for token in tokens:
            if token in self.operators:
                # This token is an operator.
                # Before adding it to the operator stack, process any operators
                # already on the stack that have a higher or equal precedence.
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                # If the token is not an operator, it must be a number.
                try:
                    # Convert the token to a float and add it to the values stack.
                    values.append(float(token))
                except ValueError:
                    # If conversion fails, the token is invalid.
                    raise ValueError(f"invalid token: {token}")

        # After processing all tokens, apply any remaining operators on the stack.
        while operators:
            self._apply_operator(operators, values)

        # At the end, the values stack should contain exactly one number: the final result.
        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        """
        Applies a single operator from the stack to the top two values on the values stack.
        """
        if not operators:
            return

        # Pop the operator and the top two operands.
        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop() # The second operand
        a = values.pop() # The first operand
        
        # Perform the calculation and push the result back onto the values stack.
        values.append(self.operators[operator](a, b))