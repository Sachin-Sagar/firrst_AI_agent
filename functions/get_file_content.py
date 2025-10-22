# functions/get_file_content.py

import os
from config import MAX_CHARACTERS
# We no longer need: from google.genai import types

def get_file_content(working_directory, file_path):
    """
    Reads the content of a specified file within the project's working directory.

    Args:
        working_directory (str): The absolute path of the agent's working directory.
                                 This is used as a security boundary.
        file_path (str): The relative path to the file that needs to be read.

    Returns:
        str: The content of the file as a string, or an error message if the file
             cannot be accessed, is too large, or is outside the working directory.
    """

    # --- Security Check ---
    # Construct the absolute paths for the working directory and the target file.
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Ensure the requested file is within the allowed working directory.
    # This prevents directory traversal attacks (e.g., trying to access '../../etc/passwd').
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error:{file_path} is not in the working deirectory: {abs_working_dir}'

    # --- File Validation ---
    # Check if the path points to an actual file.
    if not os.path.isfile(abs_file_path):
        return f'Error: {file_path} is not a file or does not exist'

    # --- File Reading ---
    file_content_string = ""
    try:
        # Open the file in read mode with UTF-8 encoding.
        with open(abs_file_path, 'r', encoding='utf-8') as file:
            # Read up to MAX_CHARACTERS to avoid memory issues with large files.
            file_content_string = file.read(MAX_CHARACTERS)
            # If the file is larger than the limit, append a truncation message.
            if len(file_content_string) >= MAX_CHARACTERS:
                file_content_string += (
                    f'[... File "{file_path}" trunkated at {MAX_CHARACTERS} characters ...]'
                )
            return file_content_string
    except Exception as e:
        # Handle potential file reading errors (e.g., permission denied).
        return f'Error reading file {file_path}: {str(e)}'


# --- OpenAI/Groq Function Declaration (as a dict) ---
# Replaced the google.genai.types.FunctionDeclaration
# with a plain Python dictionary in the format Groq expects.
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets file content of the given file as a string, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file, from the working directory.",
                }
            },
            "required": ["file_path"], # 'file_path' is required
        },
    }
}