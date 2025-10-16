AI Coding Agent
This project is a Python-based AI coding agent that can interact with your file system. It's designed to help you with various coding tasks by understanding your requests and performing actions like listing files, reading and writing code, and even running Python scripts. The agent is powered by Google's Gemini API.

Overview
The AI Coding Agent is a command-line tool that takes a prompt from the user and uses the Gemini API to determine the best course of action. It can perform a variety of file-based operations, making it a versatile and helpful tool for any developer.

The agent is designed to be extensible, so you can easily add new functions and capabilities to suit your needs. It also includes a simple calculator module as an example of a self-contained sub-project that the agent can interact with.

Features
File and Directory Listing: The agent can list the files and directories in your project, giving you a quick overview of your codebase.

File Content Reading: You can ask the agent to read the contents of a specific file, and it will return the content as a string.

File Writing: The agent can write new code to a file or update existing ones. It can even create new directories if they don't exist.

Python Script Execution: One of the most powerful features of the agent is its ability to run Python scripts. This allows you to test your code, run scripts, and see the output in real-time.

Extensible Function Set: The agent's capabilities are defined in the functions directory. You can easily add new Python scripts to this directory to extend the agent's functionality.

Pre-built Calculator: The project comes with a pre-built command-line calculator that can evaluate mathematical expressions.

Project Structure
Here is a brief overview of the key files and directories in this project:

main.py: This is the main entry point for the AI agent. It takes a user's prompt, interacts with the Gemini API, and orchestrates the function calls.

call_function.py: This module is responsible for calling the appropriate function based on the name of the function returned by the AI.

functions/: This directory contains all the functions that the AI agent can call.

get_files_info.py: Lists the files in a specified directory.

get_file_content.py: Reads the content of a given file.

write_file.py: Writes content to a specified file.

run_python_file.py: Executes a Python file and returns its output.

calculator/: This directory contains a simple command-line calculator.

main.py: The main entry point for the calculator.

pkg/calculator.py: The Calculator class, which handles the evaluation of mathematical expressions.

pkg/render.py: A helper function to format the calculator's output as a JSON string.

tests.py: Unit tests for the calculator.

config.py: This file contains configuration variables, such as the maximum number of characters to read from a file.

tests.py: This file contains a simple test for the run_python_file function.

Getting Started
To get started with the AI Coding Agent, you'll need to have Python 3.10 or higher installed.

Installation
Clone the repository:

Bash

git clone <repository-url>
Navigate to the project directory:

Bash

cd first_ai_agent
Install the required dependencies:

Bash

pip install -r requirements.txt
Note: You may need to create a requirements.txt file first. Based on the imports, you'll need google-generativeai and python-dotenv.

Configuration
Create a .env file in the root of the project.

Add your Gemini API key to the .env file:

GEMINI_API_KEY="your-api-key"
Usage
You can run the AI agent from the command line by passing a prompt as an argument:

Bash

python main.py "Your prompt here"
For example, to list all the files in the current directory, you would run:

Bash

python main.py "List all the files in the project"
You can also add the --verbose flag to see more detailed output, including the number of tokens used for the prompt and response:

Bash

python main.py "Your prompt here" --verbose
Calculator Module
The calculator/ directory contains a simple command-line calculator that the AI agent can interact with.

How to Run the Calculator
You can run the calculator directly from the command line:

Bash

python calculator/main.py "3 + 5"
This will output the result in JSON format:

JSON

{
  "expression": "3 + 5",
  "result": 8
}
The calculator supports addition, subtraction, multiplication, and division. It can also handle more complex expressions with multiple operators.

Testing
The project includes a tests.py file in the root directory that you can use to test the run_python_file function. To run the test, simply execute the file:

Bash

python tests.py
The calculator/ directory also has its own tests.py file for testing the calculator's functionality. To run these tests, you can use the unittest module:

Bash

python -m unittest calculator/tests.py