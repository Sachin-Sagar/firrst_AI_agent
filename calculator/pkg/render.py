# calculator/pkg/render.py

# This script provides a helper function to format the output of the calculator
# into a structured and machine-readable JSON format.

import json


def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    """
    Formats the calculator's expression and result into a JSON string.

    Args:
        expression (str): The original mathematical expression that was evaluated.
        result (float): The numerical result of the evaluation.
        indent (int, optional): The number of spaces to use for JSON indentation,
                                making it human-readable. Defaults to 2.

    Returns:
        str: A JSON formatted string containing the expression and result.
    """
    # --- Smart Number Formatting ---
    # This logic checks if the result is a float that represents a whole number
    # (e.g., 8.0). If it is, it converts it to an integer (8) for cleaner output.
    # Otherwise, it keeps it as a float.
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    # --- JSON Structure ---
    # Create a Python dictionary that will be converted to JSON.
    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    
    # Use the json.dumps function to convert the dictionary into a string,
    # applying the specified indentation for pretty-printing.
    return json.dumps(output_data, indent=indent)