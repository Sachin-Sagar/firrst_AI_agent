# tests.py

# This script contains a basic integration test for the agent's functions.
# Its main purpose is to verify that the core functionality of executing a Python script
# works as expected. This is not a comprehensive test suite but rather a quick check.

from functions.run_python_file import run_python_file

def main():
    """
    Runs the integration test.
    """

    # --- Test Case: run_python_file ---
    # This test checks if the run_python_file function can correctly execute
    # the 'calculate.py' script and capture its standard output.
    print("Running test for: run_python_file with calculate.py")
    
    # Execute the script. The working_directory is '.' (the root of the project).
    result = run_python_file(working_directory=".", file_path="calculate.py")

    # The result from run_python_file is a string containing STDOUT and STDERR.
    # For debugging, it's helpful to print the captured result.
    print(f"Captured output from calculate.py: {result}")

    # --- Assertion ---
    # The 'calculate.py' script is designed to print "17".
    # This assertion checks if the string "17" is present in the captured output.
    # If it is, the test passes. If not, the assert will raise an AssertionError,
    # indicating that something is wrong with the file execution function.
    assert "17" in result, f"Assertion Failed: Expected '17' in result, but got '{result}'"
    
    print("Test passed successfully!")

    # The commented-out lines below are examples of how other functions could be tested
    # or how the run_python_file function could be used with different arguments.
    # They are left here for demonstration and debugging purposes.
    #print(run_python_file("calculator", "main.py"))
    #print(run_python_file("calculator", "main.py", ["3 + 5"]))
    #print(run_python_file("calculator", "tests.py"))
    #print(run_python_file("calculator", "../main.py")) # This would test the security boundary.
    #print(run_python_file("calculator", "nonexistent.py")) # This would test error handling.
    #print(run_python_file("calculator", "lorem.txt")) # This tests the .py file check.

# Standard Python entry point.
if __name__ == "__main__":
    main()