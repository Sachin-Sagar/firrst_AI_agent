# functions/execute_dynamic_python.py

import os
import subprocess
import datetime
import logging

# Set a timeout for all dynamic script executions
EXECUTION_TIMEOUT = 30

def execute_dynamic_python(working_directory, script_code: str, script_input: str = None):
    """
    Executes a string of Python code in a sandboxed subprocess.
    This tool is for complex logic that other tools cannot handle.
    
    CRITICAL: The script_code should read data from standard input
    (sys.stdin) to process the 'script_input' argument safely.

    Args:
        working_directory (str): The agent's CWD (sandbox).
        script_code (str): The Python code to execute as a string.
        script_input (str, optional): Data to be piped into the
                                      script's standard input.

    Returns:
        str: A formatted string containing the script's STDOUT and STDERR.
    """
    logger = logging.getLogger("agent_logger")
    
    # --- Audit Logging ---
    # Create a dedicated, gitignored directory for these logs.
    audit_log_dir = os.path.join("logs", "executed_code")
    os.makedirs(audit_log_dir, exist_ok=True)
    
    # Create a unique, timestamped filename for this execution
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    base_filename = os.path.join(audit_log_dir, f"exec_{timestamp}")
    code_log_path = f"{base_filename}_code.py"
    input_log_path = f"{base_filename}_input.txt"

    try:
        # Log the code to be executed
        with open(code_log_path, 'w', encoding='utf-8') as f:
            f.write(script_code)
        logger.info(f"Dynamic script saved to: {code_log_path}")
        
        # Log the input data if it exists
        if script_input:
            with open(input_log_path, 'w', encoding='utf-8') as f:
                f.write(script_input)
            logger.info(f"Dynamic script input saved to: {input_log_path}")

    except Exception as e:
        logger.error(f"Failed to write audit logs for dynamic script: {e}")
        return f"Error: Failed to write audit logs before execution. Aborting. {e}"

    # --- Sandboxed Execution ---
    abs_working_dir = os.path.abspath(working_directory)
    logger.info(f"Executing dynamic script: {code_log_path}. CWD: {abs_working_dir}")

    try:
        # Use 'python' for compatibility.
        # '-c' runs the following string as code.
        process = subprocess.run(
            ['python', '-c', script_code],
            cwd=abs_working_dir,    # Sandbox: Set CWD
            input=script_input,     # Pipe data to stdin
            text=True,
            capture_output=True,    # Capture stdout/stderr
            timeout=EXECUTION_TIMEOUT, # Enforce timeout
            check=True              # Raise error on non-zero exit
        )
        
        logger.info(f"Dynamic script finished. STDOUT: {process.stdout[:200]}... STDERR: {process.stderr[:200]}...")
        
        return f"STDOUT:\n{process.stdout}\n\nSTDERR:\n{process.stderr}"

    except subprocess.CalledProcessError as e:
        # Script ran but returned a non-zero (error) exit code
        logger.warn(f"Dynamic script failed with exit code {e.returncode}.")
        return f"Error: Script failed with exit code {e.returncode}.\nSTDOUT:\n{e.stdout}\n\nSTDERR:\n{e.stderr}"
        
    except subprocess.TimeoutExpired as e:
        # Script took too long
        logger.warn(f"Dynamic script timed out after {EXECUTION_TIMEOUT}s.")
        return f"Error: Execution timed out after {EXECUTION_TIMEOUT} seconds.\nSTDOUT:\n{e.stdout}\n\nSTDERR:\n{e.stderr}"
        
    except Exception as e:
        # Any other exception (e.g., 'python' not found)
        logger.error(f"Failed to execute dynamic script: {e}")
        return f"Error: Failed to execute script. {e}"


# --- OpenAI/Groq Function Declaration (as a dict) ---
schema_execute_dynamic_python = {
    "type": "function",
    "function": {
        "name": "execute_dynamic_python",
        "description": "Executes a string of Python code in a sandboxed environment. Use this for custom logic or tasks not covered by other tools. The code MUST read data from 'sys.stdin' to safely process the 'script_input' argument.",
        "parameters": {
            "type": "object",
            "properties": {
                "script_code": {
                    "type": "string",
                    "description": "The string of Python code to execute. Must be valid Python. Example: 'import sys; data = sys.stdin.read(); print(len(data.split()))'",
                },
                "script_input": {
                    "type": "string",
                    "description": "The data (e.g., file content) to be piped into the script's standard input (sys.stdin).",
                }
            },
            "required": ["script_code"], # 'script_input' is optional
        },
    }
}