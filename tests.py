# tests.py

# This script runs integration tests for all functions
# available to the agent in the tool_registry.py.
# It's designed to be run from the root of the project.

import os
import json
from dotenv import load_dotenv

# Import all the functions we need to test
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.web_search import web_search
from functions.execute_dynamic_python import execute_dynamic_python # <-- ADDED

# Get the agent's working directory from the tool registry
# In a real scenario, this would be more robust, but we know it's "calculator"
from tool_registry import working_directory

# --- Constants ---
WORKING_DIR = working_directory
TEST_FILE_NAME = "_agent_test_file.txt"
TEST_FILE_CONTENT = "This is a test file created by tests.py.\nLine 2."


def main():
    """
    Runs the integration test suite for all agent functions.
    """
    
    # Load .env file to get API keys for web_search
    print("Loading .env file...")
    load_dotenv()
    print("---------------------------------\n")

    # --- 1. Test write_file (and its security) ---
    print("--- 1. Testing write_file ---")
    try:
        result = write_file(WORKING_DIR, TEST_FILE_NAME, TEST_FILE_CONTENT, "Automated test run")
        print(f"Result: {result}")
        assert "Successfully wrote" in result
        assert os.path.isfile(os.path.join(WORKING_DIR, TEST_FILE_NAME))
        print("write_file test passed.")
    except Exception as e:
        print(f"write_file test FAILED: {e}")
    
    print("\n--- 1b. Testing write_file (Security Boundary) ---")
    try:
        # Try to write a file *outside* the working directory
        result_secure = write_file(WORKING_DIR, f"../{TEST_FILE_NAME}", "test", "test")
        print(f"Result: {result_secure}")
        assert "is not in the permitted working directory" in result_secure
        assert not os.path.isfile(f"../{TEST_FILE_NAME}")
        print("write_file security test passed.")
    except Exception as e:
        print(f"write_file security test FAILED: {e}")

    print("\n---------------------------------\n")

    # --- 2. Test get_files_info ---
    print("--- 2. Testing get_files_info ---")
    try:
        result = get_files_info(WORKING_DIR, directory=".")
        print(f"Result:\n{result}")
        # Check if the file we just wrote is listed
        assert TEST_FILE_NAME in result
        # Check if it also sees the calculator's 'pkg' directory
        assert "pkg" in result
        print("get_files_info test passed.")
    except Exception as e:
        print(f"get_files_info test FAILED: {e}")

    print("\n---------------------------------\n")

    # --- 3. Test get_file_content (and its security) ---
    print("--- 3. Testing get_file_content ---")
    try:
        result = get_file_content(WORKING_DIR, TEST_FILE_NAME)
        print(f"Result:\n{result}")
        assert result == TEST_FILE_CONTENT
        print("get_file_content test passed.")
    except Exception as e:
        print(f"get_file_content test FAILED: {e}")
    
    print("\n--- 3b. Testing get_file_content (Security Boundary) ---")
    try:
        # Try to read a file *outside* the working dir (e.g., this test file)
        result_secure = get_file_content(WORKING_DIR, "../tests.py")
        print(f"Result: {result_secure}")
        assert "is not in the working deirectory" in result_secure
        print("get_file_content security test passed.")
    except Exception as e:
        print(f"get_file_content security test FAILED: {e}")

    print("\n---------------------------------\n")

    # --- 4. Test run_python_file ---
    print("--- 4. Testing run_python_file ---")
    try:
        # We'll run the calculator's main.py with a known expression
        file_to_run = "main.py"
        args_to_pass = ["5 * 3 + 10"] # Expected result: 25
        result = run_python_file(WORKING_DIR, file_to_run, args_to_pass)
        print(f"Result:\n{result}")
        # The calculator outputs JSON, so we check for key parts
        assert '"expression": "5 * 3 + 10"' in result
        assert '"result": 25' in result
        print("run_python_file test passed.")
    except Exception as e:
        print(f"run_python_file test FAILED: {e}")

    print("\n---------------------------------\n")

    # --- 5. Test web_search ---
    print("--- 5. Testing web_search ---")
    print("Note: This test requires GOOGLE_API_KEY and SEARCH_ENGINE_ID in .env")
    try:
        result = web_search(queries=["what is a python function"])
        print(f"Result (first 150 chars):\n{result[:150]}...")
        
        # Check if the result is a valid JSON list
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        
        # If results were returned, check their structure
        if len(parsed_result) > 0:
            assert "title" in parsed_result[0]
            assert "link" in parsed_result[0]
            assert "snippet" in parsed_result[0]
        
        print("web_search test passed (ran and received valid JSON).")
    except Exception as e:
        # This can fail due to API keys not being set
        print(f"web_search test FAILED (or SKIPPED): {e}")

    print("\n---------------------------------\n")
    
    # --- 6. Testing execute_dynamic_python (NEW) ---
    print("--- 6. Testing execute_dynamic_python ---")
    try:
        # This script checks stdout, stderr, stdin, and CWD
        script_code = """
import sys
import os
print("Hello from dynamic STDOUT")
print(f"CWD: {os.getcwd()}", file=sys.stderr)
data = sys.stdin.read()
print(f"Input: {data}")
"""
        script_input = "TestInput"
        result = execute_dynamic_python(WORKING_DIR, script_code, script_input)
        print(f"Result:\n{result}")

        # Check for STDOUT
        assert "Hello from dynamic STDOUT" in result
        # Check for STDIN processing
        assert "Input: TestInput" in result
        # Check for STDERR and CWD (sandbox)
        assert f"CWD: {os.path.abspath(WORKING_DIR)}" in result
        
        print("execute_dynamic_python test passed.")
    except Exception as e:
        print(f"execute_dynamic_python test FAILED: {e}")

    print("\n---------------------------------\n")

    # --- 7. Cleanup (Renumbered) ---
    print(f"--- 7. Cleaning up {TEST_FILE_NAME} ---")
    try:
        os.remove(os.path.join(WORKING_DIR, TEST_FILE_NAME))
        print(f"Successfully removed {TEST_FILE_NAME}.")
        
        # Verify it's gone with get_files_info
        result = get_files_info(WORKING_DIR, directory=".")
        assert TEST_FILE_NAME not in result
        print("Cleanup verified.")
        
    except Exception as e:
        print(f"Could not remove test file: {e}")

    print("\n--- ALL TESTS FINISHED ---")


# Standard Python entry point.
if __name__ == "__main__":
    main()