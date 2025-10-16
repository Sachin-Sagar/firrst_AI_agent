import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside'

    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found'

    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        output = subprocess.run(
            ['python3', abs_file_path] + args,
            timeout=30,
            check=True,
            capture_output=True,
            text=True,
            cwd=abs_working_dir
        )
        final_string = f"""
STDOUT: {output.stdout}
STDERR: {output.stderr}
"""

        if output.returncode != 0:
            final_string +=f"Process exited with code {output.returncode}\n"
        
        return final_string
        
    except subprocess.CalledProcessError as e:
        return f'Error running file "{file_path}": {e.stderr.strip()}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the python3 interpreter, constrained to the working directory. Accepts additional CLI args as an optional array.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),

            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optionsal array of strings to be used as a CLI args for the python file.",
                items = types.Schema(
                    type = types.Type.STRING,
                )
            ),
        },
    ),
)