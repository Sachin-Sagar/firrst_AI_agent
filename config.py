# config.py

# This file holds configuration variables that are used across the project.
# Centralizing them here makes it easy to change key values without
# having to search through multiple files.

# --- REMOVED IMPORT TO BREAK CYCLE ---
# from tool_registry import TOOL_DESCRIPTIONS

# --- File System ---
# MAX_CHARACTERS: Defines the maximum number of characters to read from a file.
# This is a safeguard to prevent loading excessively large files into memory.
MAX_CHARACTERS = 10000

# --- API Configuration ---

# GROQ_MODEL: Specifies the name of the Groq model to be used by the agent.
# Using a fast, free model like Llama 3.1 8B is a good choice.
GROQ_MODEL = 'llama-3.1-8b-instant'

# --- Agent Configuration ---

# SYSTEM_PROMPT_TEMPLATE: This is the core instruction set for the AI agent
# during the "Execution Phase". It defines its role and capabilities.
# It is now a template, waiting to be formatted in main.py.
SYSTEM_PROMPT_TEMPLATE = """
You are a helpful AI assistant. While your primary expertise is in coding and interacting with the local file system, you can also answer general questions.

You will be given a user's task and the plan you created to solve it.
Follow your plan step-by-step.

Your "working directory" is `calculator/`. All file system operations MUST be relative to this directory.
For example, to read `calculator/pkg/calculator.py`, you must call `get_file_content("pkg/calculator.py")`.

YOU HAVE ACCESS TO THE FOLLOWING TOOLS:
{tool_descriptions}

Only call the functions listed above. Do not hallucinate or invent new functions.
"""

# --- NEW: Planner Prompt Template ---
# PLANNER_SYSTEM_PROMPT_TEMPLATE: This prompt is used for the initial "Planning Phase"
# where the model is not allowed to use any tools.
PLANNER_SYSTEM_PROMPT_TEMPLATE = """
You are an expert AI software developer and project planner.
The user will give you a task. Your ONLY job is to create a clear, step-by-step plan to solve the task.

- Your "working directory" is `calculator/`. All file paths in your plan must be relative to this.
- Do NOT write any code.
- Do NOT call any functions.
- Your plan should be a bulleted list.
- For each step, briefly mention any of the *only* available tools you anticipate using.

HERE ARE THE ONLY TOOLS YOU CAN USE IN YOUR PLAN:
{tool_descriptions}

Output ONLY the plan and nothing else.
"""