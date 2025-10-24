# AI Coding Agent

This project is a Python-based AI coding agent powered by multiple LLM APIs. It is designed to be a powerful and safe assistant for developers, capable of intelligently interacting with your file system. It follows a "Plan-then-Execute" model to first create a detailed plan and then execute it step-by-step.

The agent can perform actions like reading and writing code, listing directory contents, running Python scripts, and searching the web, all while maintaining a secure and transparent record of its actions.

⭐ Key Features

    ⚡ **Multi-Provider LLM Support**: Flexibly switch between LLM providers. Currently supports:
        - **Groq API**: Near-instantaneous model responses via Groq's LPU architecture.
        - **Cerebras API**: Access to Cerebras models via their OpenAI-compatible endpoint.

    🧠 **Plan-then-Execute Model**: The agent first analyzes the user's request to create a step-by-step plan (without using tools), then follows that plan in an execution phase, leading to more robust and logical outcomes.

    📂 **File System Access**: Can read, write, and list files to perform coding tasks directly.

    🤖 **Script Execution**: Ability to run Python scripts (e.g., running tests, builds) and analyze their STDOUT and STDERR.

    🌐 **Web Searching**: Can search the web using the Google Custom Search API to find documentation, install guides, or error solutions.

    🛡️ **Safe & Secure**:
        - **Sandboxed**: All file operations are constrained to a specific working directory (`calculator/` by default).
        - **Automated Backups**: Automatically creates a timestamped backup of any file before modification.
        - **Change-logs**: Saves an accompanying change-log file for any modifications.

    📝 **Comprehensive Logging**: Every agent run—including the initial prompt, the generated plan, all model thoughts, function calls, and results—is saved to a timestamped file in the `logs/` directory.

    🔧 **Easily Extensible**: Designed with a clean "registry" pattern. Adding new tools is as simple as creating a function and adding it to `tool_registry.py`.

🏛️ How it Works: Plan-then-Execute

This agent operates in two distinct phases, managed by `main.py`:

1.  **Planning Phase**
    * The user runs `main.py` with a prompt.
    * `main.py` sends this prompt to the selected LLM API (Groq or Cerebras) using a special `PLANNER_SYSTEM_PROMPT_TEMPLATE`.
    * In this phase, the agent has **no tools enabled**. Its only job is to think and produce a step-by-step plan to solve the user's task.
    * The agent's plan is logged and printed to the console.

2.  **Execution Phase**
    * `main.py` initializes a new conversation history. This history includes the main `SYSTEM_PROMPT_TEMPLATE`, the original user prompt, and the plan the agent just created.
    * `main.py` gets the complete list of available tools from `tool_registry.py`.
    * The agent now enters a loop, instructed to follow its own plan.
    * When the agent needs to act, it sends a `tool_call` request.
    * `main.py` passes the `tool_call` to `call_function.py`, which uses `tool_registry.py` to find and execute the correct function.
    * The function's result (e.g., file content, or a script's output) is appended to the history and sent back to the LLM API.
    * This loop (think, act, observe) continues until the agent determines the plan is complete and provides a final answer.

🚀 Getting Started

1.  **Prerequisites**
    * Python 3.10 or higher.

2.  **Installation**
    * Clone the repository:
        ```bash
        git clone <repository-url>
        ```
    * Navigate to the project directory:
        ```bash
        cd first_ai_agent
        ```
    * Install the required dependencies: We recommend using a virtual environment.
        ```bash
        # Create and activate a virtual environment
        python3 -m venv .venv
        source .venv/bin/activate
        
        # Install dependencies from pyproject.toml
        pip install -e .
        ```

3.  **Configuration**
    * Create a `.env` file in the root of the project.
    * Add your API keys and select your provider in the `.env` file:

        ```dotenv
        # --- Provider Selection (REQUIRED) ---
        # Choose your LLM provider. Must be "groq" or "cerebras".
        # Defaults to "groq" if not set.
        LLM_PROVIDER="groq"
        
        # --- Groq API Key (REQUIRED if LLM_PROVIDER="groq") ---
        GROQ_API_KEY="your-groq-api-key"
        
        # --- Cerebras API Key (REQUIRED if LLM_PROVIDER="cerebras") ---
        CEREBRAS_API_KEY="your-cerebras-api-key"
        
        # --- Optional (for Web Search tool) ---
        GOOGLE_API_KEY="your-google-cloud-api-key"
        SEARCH_ENGINE_ID="your-programmable-search-engine-id"
        ```

        * `GROQ_API_KEY`: Get this from the [Groq Console](https://console.groq.com/).
        * `CEREBRAS_API_KEY`: Get this from the [Cerebras Developer Portal](https://inference-docs.cerebras.ai/quickstart).
        * `GOOGLE_API_KEY`: Required for the `web_search` tool. Get this from the Google Cloud Console.
        * `SEARCH_ENGINE_ID`: Required for the `web_search` tool. Get this from the Programmable Search Engine control panel.

4.  **Dependencies**
    This project's dependencies are managed in `pyproject.toml`. The core requirements are:
    ```toml
    [project]
    name = "agent-tst"
    version = "0.1.0"
    ...
    requires-python = ">=3.10"
    dependencies = [
        # Note: google-generativeai and google-cloud-aiplatform are NOT used
        "python-dotenv",
        "google-api-python-client", # For Google Custom Search API
        "groq",                     # For the Groq LLM API
        "openai",                   # For Cerebras (OpenAI-compatible) API
    ]
    ```

🛠️ Usage & Tools

**Running the Agent**

You can run the AI agent from the command line by passing a prompt as an argument:
```bash
python main.py "Your prompt here"

# Example:
python main.py "Use the calculator app to compute 3 * (4 + 5)"
To see a detailed, real-time log of the agent's plan, thoughts, and actions, use the --verbose flag:

Bash

python main.py "Refactor calculator/main.py to improve readability" --verbose
Available Tools

The agent has access to the following tools, which are managed by tool_registry.py:

get_files_info(directory: str): Lists files and directories in a specified path relative to the calculator/ working directory.

get_file_content(file_path: str): Reads the text content of a file relative to the calculator/ working directory.

run_python_file(file_path: str, args: list[str]): Executes a Python file (like main.py or tests.py) relative to the calculator/ working directory and captures its output.

write_file(file_path: str, content: str, change_log: str): Writes new content to a file relative to the calculator/ working directory. Automatically creates backups and change-logs.

web_search(queries: list[str]): Performs a Google web search for up-to-date information or error solutions.

🧪 Testing

This project includes two separate test files:

Unit Tests (for the calculator app):

File: calculator/tests.py

Purpose: This is a standard unittest suite that tests the logic of the Calculator class in pkg/calculator.py.

Usage: You can (and should!) instruct the agent to run these tests to verify its changes to the calculator logic (e.g., run_python_file("tests.py")).

Manual: python calculator/tests.py

Integration Tests (for the Agent's Tools):

File: tests.py (in the project root)

Purpose: This is a functional integration test suite that verifies all core agent tools (e.g., write_file, get_file_content, run_python_file, web_search) are working correctly against the live calculator/ directory. It also tests the security boundaries.

Usage: This file is for you (the developer) to run, not for the agent.

Manual: python tests.py (Note: This requires a valid .env file for the web_search test).

⚙️ Project Architecture

main.py: The main entry point. Reads the LLM_PROVIDER config, initializes the correct client, and manages the Plan-then-Execute loop.

call_function.py: The central dispatcher. main.py passes all tool_call requests here for execution.

tool_registry.py: The "switchboard" for all tools. It imports all tool functions and their schemas, maps them by name, and injects the working_directory.

config.py: Centralized configuration. Stores API settings (like CEREBRAS_API_BASE), model names, and the system prompt templates.

logger_config.py: A simple module that sets up the timestamped file logging and verbose console logging.

functions/: A directory containing the raw Python code for each individual tool (e.g., write_file.py, get_files_info.py).

logs/: This directory is automatically created and stores the detailed log file for every agent run.

backups/: This directory is automatically created and stores file backups and change-logs generated by the write_file tool.

calculator/: The self-contained example project (a command-line calculator) that the agent interacts with.

🔧 How to Add a New Tool

Create the Tool Function: Create a new file in functions/my_new_tool.py.

Python

# functions/my_new_tool.py

def my_new_tool(some_argument: str):
    """A description of what my tool does."""
    try:
        # ... do something ...
        return f"Success: {some_argument}"
    except Exception as e:
        return f"Error: {str(e)}"

# Define its schema in OpenAI/Groq format
schema_my_new_tool = {
    "type": "function",
    "function": {
        "name": "my_new_tool",
        "description": "A description of what my tool does.",
        "parameters": {
            "type": "object",
            "properties": {
                "some_argument": {
                    "type": "string",
                    "description": "The argument for the tool."
                }
            },
            "required": ["some_argument"]
        }
    }
}
Register the Tool: Open tool_registry.py and make two changes:

Python

# tool_registry.py

# ... other imports
from functions.web_search import web_search, schema_web_search
# 1. Import your new function and schema
from functions.my_new_tool import my_new_tool, schema_my_new_tool

# ...

_tool_map = {
    # ... other tools
    "web_search": web_search,
    # 2. Add your tool to the map...
    "my_new_tool": my_new_tool,
}

_tool_schemas = [
    # ... other schemas
    schema_web_search,
    # ...and to the schema list
    schema_my_new_tool,
]

# 3. (IMPORTANT) Add its description to TOOL_DESCRIPTIONS
#    so the agent's prompts are updated.
TOOL_DESCRIPTIONS = """
...
- `web_search(queries: list[str])`: ...
- `my_new_tool(some_argument: str)`: A description of what my tool does.
"""

# ... rest of the file