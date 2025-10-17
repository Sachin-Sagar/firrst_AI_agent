# call_function.py

# This script acts as a central dispatcher for all function calls made by the AI.
# When the Gemini model decides to call a function (e.g., "get_files_info"),
# this script is responsible for executing the corresponding Python function
# and returning the result in a format the model can understand.

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.web_search import web_search  # Import the new web_search function
from google.genai import types

# The working directory is set here to ensure all file operations are sandboxed.
working_directory = "."

def call_function(function_call_part, verbose = False):
    """
    Executes the appropriate function based on the name provided by the Gemini model.

    Args:
        function_call_part (genai.types.FunctionCall): The function call object from the model,
                                                      containing the name and arguments.
        verbose (bool, optional): If True, prints detailed information about the function call.
                                  Defaults to False.

    Returns:
        genai.types.Content: A Content object containing the result of the function call,
                             formatted for the Gemini model's conversational history.
    """
    # The verbose flag is useful for debugging to see what the AI is trying to do.
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")

    result = ""
    # --- Function Routing ---
    # Use if statements to match the function name from the AI to the actual Python function.
    if function_call_part.name == "get_files_info":
        # The **function_call_part.args unpacks the arguments from the model
        # and passes them as keyword arguments to the Python function.
        result = get_files_info(working_directory, **function_call_part.args)

    if function_call_part.name == "get_file_content":
        result = get_file_content(working_directory, **function_call_part.args)

    if function_call_part.name == "run_python_file":
        result = run_python_file(working_directory, **function_call_part.args)

    if function_call_part.name == "write_file":
        result = write_file(working_directory, **function_call_part.args)

    # Add the new web_search function to the dispatcher
    if function_call_part.name == "web_search":
        result = web_search(**function_call_part.args)

    # --- Response Formatting ---
    # If no function matched, return an error.
    if result == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    else:
        # If a function was successfully called, wrap its result in a Content object.
        # This is the standard way to provide tool output back to the Gemini model.
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": result},
                )
            ],
        )