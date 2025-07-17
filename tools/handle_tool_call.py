import re
import ast # Keep ast for literal_eval for this specific format
import sys
import os

# Adjust sys.path.append if necessary based on your project structure and how you run the script
# If you run `python server.py` from `agent_light/`, then `lightai/` is on the path.
# If you run from `agent_light/lightai/tools/`, then `../` is needed for `tool_registry`.
# sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # Keeping this as per your original file structure

# Import get_tool_function to retrieve the actual callable tool function
from tools.tool_registry import get_tool_function 

# Regex to match FUNCTION: <tool_name> PARAMS: { ... }
TOOL_CALL_REGEX = r"FUNCTION:\s*(\w+)\s*PARAMS:\s*(\{.*\})"


def is_tool_call(message: str) -> bool:
    """
    Returns True if the message contains a valid tool call in the FUNCTION: PARAMS: format, else False.
    """
    match = re.search(TOOL_CALL_REGEX, message)
    return bool(match)


def parse_tool_call(message: str):
    """
    Checks if a tool call is present in the message and extracts tool name and params.
    Returns (tool_name, params_dict) or (None, None) if not found.
    """
    match = re.search(TOOL_CALL_REGEX, message)
    if not match:
        return None, None
    tool_name = match.group(1)
    params_str = match.group(2)
    try:
        # Safely evaluate the params dict string
        params = ast.literal_eval(params_str)
        # Ensure params is actually a dictionary, as literal_eval can parse other types
        if not isinstance(params, dict):
            raise ValueError("Parsed parameters are not a dictionary.")
    except Exception as e:
        print(f"[ERROR] Failed to parse tool call parameters string '{params_str}': {e}")
        return None, None
    return tool_name, params


def run_tool(tool_name: str, params: dict):
    """
    Executes the tool if registered. Returns the result or error message.
    """
    # Use get_tool_function from tool_registry to get the actual callable function
    tool_function = get_tool_function(tool_name)

    if tool_function is None:
        return f"Tool '{tool_name}' not found in registry or is not a callable function."

    try:
        # Call the actual Python function with unpacked parameters
        result = tool_function(**params)
        print(f"[TOOL EXECUTION] Successfully ran '{tool_name}' with params {params}. Result: {result}")
        return result
    except TypeError as e:
        # This usually means missing parameters or incorrect parameter types for the tool function
        print(f"[ERROR] Error executing tool '{tool_name}': Invalid parameters or missing required arguments. Details: {e}")
        return f"Error executing tool '{tool_name}': Invalid parameters or missing required arguments. Ensure all required parameters are provided and are of the correct type. Details: {e}"
    except Exception as e:
        # Catch any other unexpected errors during tool execution
        print(f"[ERROR] An unexpected error occurred while running tool '{tool_name}': {e}")
        return f"An unexpected error occurred while running tool '{tool_name}': {e}"
