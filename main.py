# main.py

# This is the main entry point for the AI coding agent.
# It has been refactored to first create a plan, and then
# execute that plan.

import os
import sys
import logging
from dotenv import load_dotenv # <-- Keep this top-level import
from groq import Groq 
from openai import OpenAI 

# --- FIX: ALL local project imports are MOVED from here ---
# We will import them INSIDE main() AFTER load_dotenv() runs
# to prevent a pre-emptive import of config.py

def main():

    # --- Initialization ---
    
    # --- FIX: load_dotenv() MUST be the first thing called ---
    # This loads your .env file *before* any other project file.
    load_dotenv(override=True)
    
    # --- FIX: All local imports are now INSIDE main() ---
    # This prevents the pre-emptive import bug.
    import tool_registry
    from call_function import call_function 
    from logger_config import setup_logger
    from config import (
        LLM_PROVIDER, 
        GROQ_MODEL, 
        CEREBRAS_MODEL, 
        CEREBRAS_API_BASE,
        SYSTEM_PROMPT_TEMPLATE, 
        PLANNER_SYSTEM_PROMPT_TEMPLATE
    )
    # --- END FIX ---
    
    # --- DEBUG: Print the LLM_PROVIDER value ---
    # This will now correctly show 'cerebras'
    print(f"[DEBUG] LLM_PROVIDER string read from config: '{LLM_PROVIDER}'")
    # --- END DEBUG ---
    
    # --- LLM Provider Factory (The "Switch") ---
    client = None
    model_name = ""

    if LLM_PROVIDER == "groq":
        # --- DEBUG ---
        print("[DEBUG] Initializing GROQ client...")
        # --- END DEBUG ---
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("Error: LLM_PROVIDER is 'groq' but GROQ_API_KEY not found in .env file.")
            sys.exit(1)
        client = Groq(api_key=api_key)
        model_name = GROQ_MODEL
        
    elif LLM_PROVIDER == "cerebras":
        # --- DEBUG ---
        print("[DEBUG] Initializing CEREBRAS client...")
        # --- END DEBUG ---
        api_key = os.environ.get("CEREBRAS_API_KEY")
        if not api_key:
            print("Error: LLM_PROVIDER is 'cerebras' but CEREBRAS_API_KEY not found in .env file.")
            sys.exit(1)
        # Use the OpenAI client, but point it to Cerebras's API endpoint
        client = OpenAI(
            api_key=api_key,
            base_url=CEREBRAS_API_BASE
        )
        model_name = CEREBRAS_MODEL
        
    else:
        # --- DEBUG ---
        print(f"[DEBUG] Unknown LLM_PROVIDER: '{LLM_PROVIDER}'")
        # --- END DEBUG ---
        print(f"Error: Unknown LLM_PROVIDER '{LLM_PROVIDER}' in .env file. Must be 'groq' or 'cerebras'.")
        sys.exit(1)
    
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
    
    # This log will now correctly show the provider
    logger.info(f"Using Provider: {LLM_PROVIDER}") 
    logger.info(f"Using Model: {model_name}")
    
    logger.info(f"Initial User Prompt: {prompt}")

    # --- Format Prompts ---
    tool_descriptions = tool_registry.TOOL_DESCRIPTIONS
    SYSTEM_PROMPT = SYSTEM_PROMPT_TEMPLATE.format(tool_descriptions=tool_descriptions)
    PLANNER_SYSTEM_PROMPT = PLANNER_SYSTEM_PROMPT_TEMPLATE.format(tool_descriptions=tool_descriptions)
    # --- END ---

    # --- 1. PLANNING PHASE ---
    plan_text = ""
    try:
        logger.info("--- STARTING PLANNING PHASE ---")
        planning_messages = [
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        plan_response = client.chat.completions.create(
            model=model_name,
            messages=planning_messages,
            tools=None, 
            tool_choice="none" 
        )
        
        plan_text = plan_response.choices[0].message.content
        
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
    logger.info("--- STARTING EXECUTION PHASE ---")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": plan_text}, 
        {"role": "user", "content": "Great, please proceed with the first step of your plan."}
    ]

    available_tools = tool_registry.get_openai_tools()

    max_iters = 20
    for i in range(max_iters):
        logger.info(f"--- Iteration {i+1} / {max_iters} ---")
        
        print("🤖 Model is thinking...")
        
        try:
            response = client.chat.completions.create(
                model = model_name,
                messages = messages,
                tools = available_tools,
                tool_choice = "auto"
            )

            response_message = response.choices[0].message
            messages.append(response_message) 
            
            if response.usage:
                logger.info(f"Prompt tokens: {response.usage.prompt_tokens}")
                logger.info(f"Response tokens: {response.usage.completion_tokens}")

            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    tool_result_message = call_function(tool_call)
                    messages.append(tool_result_message)
            else:
                final_answer = response_message.content
                logger.info(f"LLM Response (Final Answer): {final_answer}")
                logger.info("--- AGENT RUN FINISHED ---")
                
                print("\n--- AGENT'S FINAL ANSWER ---")
                print(final_answer)
                return 

        except Exception as e:
            logger.error(f"Error calling LLM API: {str(e)}")
            print(f"An error occurred: {str(e)}")
            return

# Standard Python entry point.
if __name__ == "__main__":
    main()