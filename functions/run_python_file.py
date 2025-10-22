# functions/run_python_file.py

import os
import subprocess
# We no longer need: from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    """
    Executes a specified Python file in a sandboxed environment and captures its output.

    Args:
        working_directory (str): The agent's working directory, used as a security boundary.
        file_path (str): The relative path to the Python file to be executed.
        args (list, optional): A list of command-line arguments to pass to the script. Defaults to [].

    Returns:
        str: A string containing the STDOUT and STDERR from the script's execution,
             or an error message if the execution fails or violates security constraints.
    """

    # --- Security and Path Validation ---
    # Construct absolute paths for the working directory and the target file.
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security Check 1: Ensure the file is within the working directory.
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'

    # Validation Check 1: Ensure the file path actually exists.
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found'

    # Validation Check 2: Ensure the file is a Python script.
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    # --- Script Execution ---
    try:
        # The subprocess.run command executes the Python script.
        # - ['python3', abs_file_path] + args: Constructs the full command.
        # - timeout=30: Sets a 30-second limit to prevent long-running scripts.
        # - check=True: Raises a CalledProcessError if the script returns a non-zero exit code.
        # - capture_output=True: Captures STDOUT and STDERR.
        # - text=True: Decodes STDOUT and STDERR as text.
        # - cwd=abs_working_dir: Sets the current working directory for the script.
        output = subprocess.run(
            ['python3', abs_file_path] + args,
            timeout=30,
            check=True,
            capture_output=True,
            text=True,
            cwd=abs_working_dir
        )
        
        # Format the output for clarity.
        final_string = f"""
STDOUT: {output.stdout}
STDERR: {output.stderr}
"""
        # Append the exit code if it's not 0 (success).
        if output.returncode != 0:
            final_string +=f"Process exited with code {output.returncode}\n"
        
        return final_string
        
    except subprocess.CalledProcessError as e:
        # This error is caught if check=True and the script has a non-zero exit code.
        # It usually means the script itself had an error.
        return f'Error running file "{file_path}": {e.stderr.strip()}'
    except subprocess.TimeoutExpired:
        # Handle cases where the script runs for longer than the 30-second timeout.
        return f'Error: Execution of "{file_path}" timed out.'
    except Exception as e:
        # Catch any other unexpected errors during subprocess execution.
        return f'An unexpected error occurred while running "{file_path}": {str(e)}'


# --- OpenAI/Groq Function Declaration (as a dict) ---
# Replaced the google.genai.types.FunctionDeclaration
# with a plain Python dictionary in the format Groq expects.
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file with the python3 interpreter, constrained to the working directory. Accepts additional CLI args as an optional array.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file to run, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "description": "An optional array of strings to be used as CLI args for the python file.",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["file_path"], # 'file_path' is required, 'args' is optional
        },
    }
}