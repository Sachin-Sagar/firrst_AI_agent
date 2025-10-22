# tool_registry.py

# This new module acts as a centralized registry for all agent tools.
# Its responsibilities are:
# 1. Import all available tool functions and their schemas.
# 2. Store them in an organized way (dictionaries, lists).
# 3. Provide a simple dispatcher function (`call_tool`) to execute a tool by name.
# 4. Provide a function (`get_openai_tools`) to format the schemas for the API.
#
# This de-couples main.py from knowing about every specific tool.

import json
# Import all our functions and their new dictionary-based schemas
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file
from functions.web_search import web_search, schema_web_search

# The working directory is set here.
# In a more advanced implementation, this could be passed around
# or set in the config.py file.
working_directory = "calculator"

# --- Tool Mapping ---

# A dictionary mapping the tool's name (string) to the
# actual callable Python function.
_tool_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
    "web_search": web_search,
}

# A list containing all the schema dictionaries.
# These are now in the correct OpenAI/Groq format.
_tool_schemas = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
    schema_web_search,
]

# --- NEW: Tool Descriptions for Prompt Grounding ---
# This string is imported by config.py to be injected directly
# into the system prompts, reminding the model of its capabilities.
TOOL_DESCRIPTIONS = """
- `get_files_info(directory: str)`: Lists files and directories in a specified path relative to the `calculator/` working directory.
- `get_file_content(file_path: str)`: Reads the text content of a file relative to the `calculator/` working directory.
- `run_python_file(file_path: str, args: list[str])`: Executes a Python file (like `main.py` or `tests.py`) relative to the `calculator/` working directory.
- `write_file(file_path: str, content: str, change_log: str)`: Writes new content to a file relative to the `calculator/` working directory.
- `web_search(queries: list[str])`: Performs a Google web search for up-to-date information or error solutions.
"""

# --- Helper Function (REMOVED) ---
# We no longer need the _convert_schemas_to_openai function
# as our schemas are now defined as plain dictionaries.


# --- Public Functions ---

def get_openai_tools():
    """
    Returns the list of all tool schemas, which are already
    formatted for an OpenAI-compatible API (like Groq).
    """
    # Just return the list directly.
    return _tool_schemas

def call_tool(name: str, **kwargs):
    """
    Calls a tool by its name and passes arguments to it.

    This function automatically injects the 'working_directory'
    argument required by the file-system tools.

    Args:
        name (str): The name of the function to call (e.g., "write_file").
        **kwargs: The arguments to pass to that function (e.g., file_path="...").

    Returns:
        str: The string result from the executed tool.
    """
    if name not in _tool_map:
        return f"Error: Unknown function: {name}"

    # Get the actual function to call from our map
    func_to_call = _tool_map[name]

    # All file-system tools expect 'working_directory' as the first
    # argument. Web search doesn't, so we check.
    # A more robust way would be to inspect the function signature,
    # but for now, this works.
    if name in ["get_files_info", "get_file_content", "run_python_file", "write_file"]:
        # Inject the working_directory as the first argument
        return func_to_call(working_directory, **kwargs)
    else:
        # For other tools like 'web_search'
        return func_to_call(**kwargs)