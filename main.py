# main.py

# This is the main entry point for the AI coding agent.
# It orchestrates the entire process: loading the API key, getting user input,
# communicating with the Gemini API, and managing the conversation loop.

import os
import sys
import time # Import the time module
from dotenv import load_dotenv
from google import genai
from google.genai import types
# Import the function schemas that the AI will be able to call.
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_contnet
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.web_search import schema_web_search
# Import the central function dispatcher.
from call_function import call_function
# Import the model name from the config file.
from config import GEMINI_MODEL


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
    You are a helpful AI assistant. While your primary expertise is in coding and interacting with the local file system, you can also answer general questions.

    Primary Capabilities (Coding Tasks):
    - When a user asks a question about the code project, they are referring to the working directory.
    - You can list files, read their contents, write new code, and run python scripts to fulfill requests.
    - Start by understanding the project structure before making changes.
    - After any code modification, you should run tests to verify that everything works as expected.
    - All file paths should be relative to the working directory.

    General Conversation:
    - If the user asks a general question not related to coding, provide a helpful and direct answer.
    - You have access to a web search tool for up-to-date information.
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
            schema_write_file,
            schema_web_search
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
            model = GEMINI_MODEL, # Using the model defined in config.py.
            contents = messages,
            config = config,
        )

        if response is None or response.usage_metadata is None:
            print("No response or usage metadata available.")
            return

        # Print token usage for debugging costs and performance.
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
                # Add a delay to stay within the free tier rate limits
                time.sleep(2)
        else:
            # If there are no function calls, it means the AI has its final answer.
            # Print the text response and exit the loop.
            print(response.text)
            return

# Standard Python entry point.
if __name__ == "__main__":
    main()
