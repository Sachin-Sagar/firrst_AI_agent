# functions/get_files_info.py

import os
# We no longer need: from google.genai import types

def get_files_info(working_directory, directory="."):
    """
    Lists the contents of a specified directory within the agent's working directory.

    Args:
        working_directory (str): The absolute path of the agent's working directory.
                                 This acts as a security sandbox.
        directory (str, optional): The relative path of the directory to inspect.
                                   Defaults to the working directory itself (".").

    Returns:
        str: A formatted string listing each item in the directory, its size,
             whether it's a directory, or an error message if access is denied.
    """

    # --- Security Check ---
    # Construct absolute paths for the security boundary and the target directory.
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))

    # Ensure the target directory is inside the working directory to prevent
    # unauthorized file system access.
    if not abs_dir.startswith(abs_working_dir):
        return f'Error:{directory} is not in the working deirectory'

    # --- Directory Listing ---
    try:
        # Get a list of all items (files and directories) in the target directory.
        contents = os.listdir(abs_dir)
    except FileNotFoundError:
        return f"Error: Directory '{directory}' not found."
    except Exception as e:
        return f"Error listing files in '{directory}': {str(e)}"

    final_response = ""

    # Loop through each item to gather details.
    for content in contents:
        content_path = os.path.join(abs_dir, content)
        try:
            # Check if the item is a directory.
            is_dir = os.path.isdir(content_path)
            # Get the size of the item in bytes.
            size = os.path.getsize(content_path)
            # Append the formatted details to the response string.
            final_response += f"- {content}: file size: {size} bytes, is_dir = {is_dir}\n"
        except OSError:
            # Handle cases where file info can't be accessed (e.g., broken symlinks).
            final_response += f"- {content}: Error accessing file info\n"
    
    return final_response


# --- OpenAI/Groq Function Declaration (as a dict) ---
# We are replacing the google.genai.types.FunctionDeclaration
# with a plain Python dictionary in the format Groq expects.
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in the specified directory along with their sizes, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                }
            },
            "required": [], # 'directory' is optional
        },
    }
}