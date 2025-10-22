# call_function.py

# This script acts as the central dispatcher for all function calls.
# It is called by main.py and uses tool_registry.py to
# execute the correct function.

import logging
import json
import tool_registry # Import our new tool registry

def call_function(tool_call):
    """
    Executes a tool call requested by the Groq model.

    Args:
        tool_call (obj): The tool_call object from the Groq response.
                         It contains the function name and arguments.

    Returns:
        dict: A dictionary formatted as a "tool" message for the
              OpenAI/Groq API, containing the result of the function call.
    """
    # Get the shared logger instance
    logger = logging.getLogger("agent_logger")

    function_name = tool_call.function.name
    function_args_str = tool_call.function.arguments
    tool_call_id = tool_call.id
    
    # We log the request here, as this is the dispatch layer
    logger.info(f"Dispatching function call: {function_name} with args: {function_args_str}")

    try:
        # Parse the JSON string of arguments
        function_args = json.loads(function_args_str)
        
        # Call the tool using our registry
        # This one line replaces the need for a giant if/elif block
        result_content = tool_registry.call_tool(function_name, **function_args)
        
        logger.info(f"Function Result ({function_name}): {result_content}")

        # Return the formatted result dictionary
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": function_name,
            "content": result_content
        }

    except json.JSONDecodeError:
        logger.error(f"Failed to decode function arguments: {function_args_str}")
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": function_name,
            "content": f"Error: Invalid arguments JSON: {function_args_str}"
        }
    except Exception as e:
        logger.error(f"Error calling tool {function_name}: {str(e)}")
        # Return an error message for the model
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": function_name,
            "content": f"Error executing function: {str(e)}"
        }