from .tool_decorator import tool

from datetime import datetime

tools = [
    "get_current_time",
]

def get_built_in_tools():
    """
    Returns a list of built-in tools available for the AI agent.
    
    Each tool is represented as a dictionary with 'name', 'description', and 'function'.
    """
    return tools

@tool
def weather(location: str) -> str:
    """
    Fetches the current weather for a given location.
    
    Args:
        location (str): The name of the location to get the weather for.
    
    Returns:
        str: A string describing the current weather conditions.
    """

    return f"The current weather in {location} is sunny with a temperature of 25°C."

@tool
def get_current_time() -> str:
    """
    Returns the current time in ISO format.
    
    Returns:
        str: The current time as an ISO formatted string.
    """
    
    return datetime.now().isoformat()