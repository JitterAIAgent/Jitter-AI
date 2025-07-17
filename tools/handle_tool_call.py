def is_tool_call(message):
    """
    Returns True if the message contains a valid tool call, else False.
    """
    match = re.search(TOOL_CALL_REGEX, message)
    return bool(match)
import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.tool_registry import TOOL_REGISTRY

# Regex to match FUNCTION: <tool_name> PARAMS: { ... }
TOOL_CALL_REGEX = r"FUNCTION:\s*(\w+)\s*PARAMS:\s*(\{.*\})"

def parse_tool_call(message):
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
        # Safely evaluate the params dict
        import ast
        params = ast.literal_eval(params_str)
    except Exception:
        params = None
    return tool_name, params

def run_tool(tool_name, params):
    """
    Executes the tool if registered. Returns the result or error message.
    """
    if tool_name not in [v['name'] for v in TOOL_REGISTRY.values()]:
        return f"Tool '{tool_name}' not found in registry."
    
    if tool_name == 'weather':
        location = params.get('location')
        if not location:
            return "Missing required parameter: location."
        # Here you would call a real weather API
        return weather_tool(location)
    return f"Tool '{tool_name}' is recognized but not implemented."

def weather_tool(location):
    """
    Example tool function for weather. Returns dummy weather info.
    """
    norm_location = location.lower().strip()

    print(f"[DEBUG] Running weather tool for location: {norm_location}")

    if not norm_location:
        return "Location cannot be empty."

    if norm_location == "montreal":
        return "The weather in Montreal is currently sunny and 25°C."
    else:
        return f"The weather in {norm_location} is currently cloudy and 25°C."