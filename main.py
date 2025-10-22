# main.py

# This is the main entry point for the AI coding agent.
# It has been refactored to first create a plan, and then
# execute that plan.

import os
import sys
import logging
from dotenv import load_dotenv
from groq import Groq

# Import our centralized modules
import tool_registry
from call_function import call_function # Import our new dispatcher
# --- FIX ---
# Import the TEMPLATE names from config
from config import GROQ_MODEL, SYSTEM_PROMPT_TEMPLATE, PLANNER_SYSTEM_PROMPT_TEMPLATE
# --- END FIX ---
from logger_config import setup_logger

def main():

    # --- Initialization ---
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY not found in .env file.")
        sys.exit(1)
        
    # Initialize the Groq client
    client = Groq(api_key=api_key)

    # --- Command-Line Argument Parsing ---
    if len(sys.argv) < 2:
        print("Need a prompt to run")
        sys.exit(1)
        return

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    # --- Logger Setup ---
    setup_logger(verbose=verbose_flag)
    logger = logging.getLogger("agent_logger")

    prompt = sys.argv[1]
    logger.info("--- STARTING AGENT RUN (Plan-then-Execute) ---")
    logger.info(f"Using model: {GROQ_MODEL}")
    logger.info(f"Initial User Prompt: {prompt}")

    # --- FIX: Format Prompts ---
    # We format the prompts here *after* importing tool_registry
    # to avoid the circular import.
    tool_descriptions = tool_registry.TOOL_DESCRIPTIONS
    SYSTEM_PROMPT = SYSTEM_PROMPT_TEMPLATE.format(tool_descriptions=tool_descriptions)
    PLANNER_SYSTEM_PROMPT = PLANNER_SYSTEM_PROMPT_TEMPLATE.format(tool_descriptions=tool_descriptions)
    # --- END FIX ---

    # --- 1. PLANNING PHASE ---
    # In this phase, the model has no tools and can only create a plan.
    plan_text = ""
    try:
        logger.info("--- STARTING PLANNING PHASE ---")
        # Create a temporary message list just for planning
        planning_messages = [
            # Use the formatted planner prompt
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        # Call the API with NO TOOLS
        plan_response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=planning_messages,
            tools=None, # No tools allowed
            tool_choice="none" # Explicitly set to "none"
        )
        
        plan_text = plan_response.choices[0].message.content
        
        # Log and print the plan as requested
        logger.info("--- AGENT PLAN ---")
        logger.info(plan_text)
        logger.info("--- END OF PLAN ---")
        
        print("\n--- AGENT PLAN ---")
        print(plan_text)
        print("--- END OF PLAN ---\n")

    except Exception as e:
        logger.error(f"Error during planning phase: {str(e)}")
        print(f"An error occurred during planning: {str(e)}")
        return
        
    # --- 2. EXECUTION PHASE ---
    # The model now gets its tools and is instructed to follow the plan.
    logger.info("--- STARTING EXECUTION PHASE ---")

    # --- Conversation History ---
    # Initialize the real message history, including the plan
    # The agent will now follow its own plan.
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}, # Use the formatted executor prompt
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": plan_text}, # The plan it just created
        # This new message prompts the model to start the *first step* of its plan.
        {"role": "user", "content": "Great, please proceed with the first step of your plan."}
    ]

    # --- Tool Configuration ---
    # Get all available tools from our new tool registry
    available_tools = tool_registry.get_openai_tools()

    # --- Main Agent Loop (Unchanged) ---
    max_iters = 20
    for i in range(max_iters):
        logger.info(f"--- Iteration {i+1} / {max_iters} ---")
        
        # --- Status message for thinking ---
        print("🤖 Model is thinking...")
        
        try:
            # --- API Call ---
            response = client.chat.completions.create(
                model = GROQ_MODEL,
                messages = messages,
                tools = available_tools,
                tool_choice = "auto"
            )

            response_message = response.choices[0].message
            messages.append(response_message) # Add model's response to history
            
            # --- Log Token Usage ---
            if response.usage:
                logger.info(f"Prompt tokens: {response.usage.prompt_tokens}")
                logger.info(f"Response tokens: {response.usage.completion_tokens}")

            # --- Function Call Handling ---
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    # --- Status message for tool call ---
                    print(f"🛠️  Calling tool: {tool_call.function.name}({tool_call.function.arguments})")

                    # Delegate the entire tool call to our dispatcher
                    tool_result_message = call_function(tool_call)
                    
                    # Append the tool's result to the message history
                    messages.append(tool_result_message)

            else:
                # If no tool calls, it's the final answer.
                final_answer = response_message.content
                logger.info(f"LLM Response (Final Answer): {final_answer}")
                logger.info("--- AGENT RUN FINISHED ---")
                
                # --- Clear header for final answer ---
                print("\n--- AGENT'S FINAL ANSWER ---")
                print(final_answer)
                return # Exit the loop and program

        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            print(f"An error occurred: {str(e)}")
            return

# Standard Python entry point.
if __name__ == "__main__":
    main()