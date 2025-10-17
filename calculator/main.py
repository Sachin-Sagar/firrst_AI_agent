# calculator/main.py

# This script serves as the command-line interface (CLI) for the calculator.
# It allows a user to run the calculator from their terminal by providing
# a mathematical expression as an argument.

import sys
# Import the core Calculator class from the pkg module.
from pkg.calculator import Calculator
# Import the JSON formatting function.
from pkg.render import format_json_output


def main():
    """
    The main function for the calculator CLI.
    """
    # Instantiate the Calculator class, creating a new calculator object.
    calculator = Calculator()
    
    # --- Argument Parsing ---
    # Check if the user has provided an expression.
    # sys.argv is a list containing the script name and its command-line arguments.
    # If its length is 1 or less, no expression was given.
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    # Join all command-line arguments after the script name into a single string.
    # This handles expressions with spaces, like "3 + 5".
    expression = " ".join(sys.argv[1:])
    
    # --- Expression Evaluation ---
    try:
        # Call the evaluate method of the calculator object to compute the result.
        result = calculator.evaluate(expression)
        
        # Check if the result is valid (not None, which indicates an empty expression).
        if result is not None:
            # Format the output as a JSON string for clean, machine-readable output.
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            # Handle cases where the expression was empty or just whitespace.
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        # Catch any errors that occur during evaluation (e.g., invalid tokens, bad expressions)
        # and print a user-friendly error message.
        print(f"Error: {e}")


# Standard Python entry point to run the main function.
if __name__ == "__main__":
    main()