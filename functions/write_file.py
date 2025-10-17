# functions/write_file.py

import os
import shutil
import datetime
from google.genai import types

def write_file(working_directory, file_path, content, change_log=""):
    """
    Writes or overwrites content to a file. If overwriting, it first creates a
    timestamped backup and saves an accompanying change-log.

    Args:
        working_directory (str): The agent's working directory.
        file_path (str): The relative path to the file to be written.
        content (str): The string content to write to the file.
        change_log (str, optional): A markdown string detailing the changes. Defaults to "".

    Returns:
        str: A success or error message.
    """

    # --- Security Check ---
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # --- Backup and Change-Log Logic ---
    backup_message = ""
    # Check if the file already exists, which means we are overwriting it.
    if os.path.isfile(abs_file_path):
        try:
            # Define the backups directory.
            backup_dir = os.path.join(abs_working_dir, "backups")
            # Create the directory if it doesn't exist.
            os.makedirs(backup_dir, exist_ok=True)
            
            # Create a timestamp string (e.g., "20231027_154501").
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.basename(abs_file_path)

            # Create the backup file path.
            backup_path = os.path.join(backup_dir, f"{base_name}_{timestamp}.bak")
            # Copy the original file to the backup location.
            shutil.copy2(abs_file_path, backup_path)
            backup_message = f'Backup of original file created at "{backup_path}".'

            # If change-log content is provided, save it.
            if change_log:
                changelog_path = os.path.join(backup_dir, f"changelog_{base_name}_{timestamp}.md")
                with open(changelog_path, 'w', encoding='utf-8') as log_file:
                    log_file.write(change_log)
                backup_message += f' Change-log saved to "{changelog_path}".'

        except Exception as e:
            return f'Error creating backup for {file_path}: {str(e)}'

    # --- Directory and File Writing ---
    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f'Error creating directory {parent_dir}: {str(e)}'

    try:
        with open(abs_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        success_message = f'Successfully wrote to "{file_path}". {len(content)} characters written.'
        # Append the backup message to the final success message.
        return f"{success_message} {backup_message}".strip()
    except Exception as e:
        return f'Error writing to file {file_path}: {str(e)}'


# --- Gemini Function Declaration ---
# Updated to include the new optional 'change_log' parameter.
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes to a new file. When overwriting, it automatically creates a timestamped backup.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to the file as a string.",
            ),
            "change_log": types.Schema(
                type=types.Type.STRING,
                description="A comprehensive markdown string detailing the changes, required when overwriting a file.",
            ),
        },
    ),
)