# main.py

# This is the main entry point for the AI coding agent.
# It orchestrates the entire process: loading the API key, getting user input,
# communicating with the Gemini API, and managing the conversation loop.

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
# Import the function schemas that the AI will be able to call.
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_contnet
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
# Import the central function dispatcher.
from call_function import call_function

def main():

    # --- Initialization ---
    # Load environment variables from a .env file (e.g., GEMINI_API_KEY).
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    # Initialize the Gemini client with the API key.
    client = genai.Client(api_key=api_key)

    # --- System Prompt ---
    # This prompt provides the AI with its core instructions, defining its role,
    # capabilities, and constraints. It's crucial for guiding the AI's behavior.
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read the contents of a file
    - Write to a file (create or update)
    - Run a python file 

    When the user asks about the code project, they are refeering to the working directory.
    Start by looking at the project files and figuring out how to run the project and the tests.
    After every code edit, run the tests to ensure that the code is working as expected.


    All paths you provide should be relative to the working directory. 
    You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    # --- Command-Line Argument Parsing ---
    # Check if a prompt was provided by the user.
    if len(sys.argv) < 2:
        print("Need a prompt to run")
        sys.exit(1)
        return

    # Check for the optional '--verbose' flag for debugging.
    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    # The user's prompt is the first command-line argument.
    prompt = sys.argv[1]   
    
    # --- Conversation History ---
    # 'messages' stores the entire conversation history. It starts with the user's first prompt.
    # It will be appended with the AI's responses and the results of tool calls.
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    # --- Tool Configuration ---
    # The 'Tool' object bundles all the function declarations (schemas)
    # that the AI is allowed to use.
    available_functions = types.Tool(
        function_declarations = [
            schema_get_files_info,
            schema_get_file_contnet,
            schema_run_python_file,
            schema_write_file
        ]
    )

    # The GenerateContentConfig ties the tools and system prompt to the API request.
    config = types.GenerateContentConfig(
        tools = [available_functions],
        system_instruction = system_prompt
    )

    # --- Main Agent Loop ---
    # This loop allows the agent to make multiple function calls to solve a complex problem.
    # It's limited to 'max_iters' to prevent infinite loops.
    max_iters = 20
    for i in range(max_iters):

        # Send the conversation history and configuration to the Gemini model.
        response = client.models.generate_content(
            model = 'gemini-1.5-pro-latest', # Using the recommended powerful model.
            contents = messages,
            config = config,
        )

        if response is None or response.usage_metadata is None:
            print("No response or usage metadata available.")
            return

        # Print token usage if in verbose mode for debugging costs and performance.
        if verbose_flag:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Append the AI's response to the conversation history.
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)
                
        # --- Function Call Handling ---
        # Check if the AI's response includes a request to call a function.
        if response.function_calls:
            for function_call_part in response.function_calls:
                # Use the dispatcher to execute the requested function.
                result = call_function(function_call_part, verbose_flag)
                # Append the function's result to the history so the AI knows what happened.
                messages.append(result)
                
        else:
            # If there are no function calls, it means the AI has its final answer.
            # Print the text response and exit the loop.
            print(response.text)
            return

# Standard Python entry point.
if __name__ == "__main__":
    main()