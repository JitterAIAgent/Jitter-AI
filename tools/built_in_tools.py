import os
from typing import Any, Dict, List, Union
from .tool_decorator import tool
from tavily import TavilyClient

import datetime
import math
import random

tools = [
    "get_current_datetime",
    "perform_calculation",
    "convert_units",
    "generate_random_number",
    "flip_coin",
]

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

if not TAVILY_API_KEY:
    tools.append("search_web")

def get_built_in_tools():
    """
    Returns a list of built-in tools available for the AI agent.
    
    Each tool is represented as a dictionary with 'name', 'description', and 'function'.
    """
    return tools

@tool
def get_current_datetime() -> str:
    """Retrieves the current date and time.

    This tool provides the current date and time in a human-readable format.
    It does not require any parameters.

    Returns:
        str: A string representing the current date and time (e.g., "July 17, 2025 04:17 PM EDT").
    """
    now = datetime.datetime.now()
    # Format the datetime object into a user-friendly string
    formatted_datetime = now.strftime("%B %d, %Y %I:%M %p %Z")
    print(f"[TOOL EXECUTION] get_current_datetime: {formatted_datetime}")
    return f"The current date and time is {formatted_datetime}."

@tool
def perform_calculation(expression: str) -> str:
    """Performs a simple arithmetic calculation based on a provided string expression.
    Supports addition (+), subtraction (-), multiplication (*), division (/), and parentheses.

    Args:
        expression (str): The arithmetic expression to calculate (e.g., "5 + 3 * 2", "(10 - 4) / 2").

    Returns:
        float: The numerical result of the calculation.
    """
    print(f"[TOOL EXECUTION] perform_calculation: {expression}")
    try:
        # Using eval() is generally unsafe for untrusted input in production systems
        # due to potential code injection. For a controlled environment with an LLM
        # where inputs are somewhat constrained, it can be used for demonstration.
        # For a robust production system, consider a safer math expression parser library.
        result = eval(expression)
        return f"{float(result)}"
    except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
        print(f"[ERROR] Calculation error: {e}")
        return f"Error performing calculation: Invalid expression or operation. Details: {e}"
    except Exception as e:
        print(f"[ERROR] Unexpected calculation error: {e}")
        return f"An unexpected error occurred during calculation: {e}"

@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Converts a numerical value from one common unit to another.
    Supports basic length (meters, feet, inches, cm, km, miles),
    temperature (celsius, fahrenheit, kelvin), and weight (grams, kilograms, pounds, ounces).

    Args:
        value (float): The numerical value to convert.
        from_unit (str): The unit to convert from (e.g., "meters", "celsius", "pounds").
        to_unit (str): The unit to convert to (e.g., "feet", "fahrenheit", "kilograms").

    Returns:
        str: A string representing the converted value and units, or an error message.
    """
    print(f"[TOOL EXECUTION] convert_units: {value} {from_unit} to {to_unit}")

    # Normalize units to a common base for conversion
    unit_map = {
        'meter': {'type': 'length', 'base_to_meter': 1.0},
        'meters': {'type': 'length', 'base_to_meter': 1.0},
        'foot': {'type': 'length', 'base_to_meter': 0.3048},
        'feet': {'type': 'length', 'base_to_meter': 0.3048},
        'inch': {'type': 'length', 'base_to_meter': 0.0254},
        'inches': {'type': 'length', 'base_to_meter': 0.0254},
        'cm': {'type': 'length', 'base_to_meter': 0.01},
        'centimeter': {'type': 'length', 'base_to_meter': 0.01},
        'centimeters': {'type': 'length', 'base_to_meter': 0.01},
        'km': {'type': 'length', 'base_to_meter': 1000.0},
        'kilometer': {'type': 'length', 'base_to_meter': 1000.0},
        'kilometers': {'type': 'length', 'base_to_meter': 1000.0},
        'mile': {'type': 'length', 'base_to_meter': 1609.34},
        'miles': {'type': 'length', 'base_to_meter': 1609.34},

        'celsius': {'type': 'temperature'},
        'fahrenheit': {'type': 'temperature'},
        'kelvin': {'type': 'temperature'},

        'gram': {'type': 'weight', 'base_to_gram': 1.0},
        'grams': {'type': 'weight', 'base_to_gram': 1.0},
        'kilogram': {'type': 'weight', 'base_to_gram': 1000.0},
        'kilograms': {'type': 'weight', 'base_to_gram': 1000.0},
        'pound': {'type': 'weight', 'base_to_gram': 453.592},
        'pounds': {'type': 'weight', 'base_to_gram': 453.592},
        'ounce': {'type': 'weight', 'base_to_gram': 28.3495},
        'ounces': {'type': 'weight', 'base_to_gram': 28.3495},
    }

    from_unit_norm = from_unit.lower().strip()
    to_unit_norm = to_unit.lower().strip()

    if from_unit_norm not in unit_map or to_unit_norm not in unit_map:
        return f"Unknown unit(s) provided. Supported units: {', '.join(unit_map.keys())}"

    from_info = unit_map[from_unit_norm]
    to_info = unit_map[to_unit_norm]

    if from_info['type'] != to_info['type']:
        return f"Cannot convert between {from_info['type']} and {to_info['type']}."

    converted_value = 0.0
    if from_info['type'] == 'length':
        # Convert to base (meters) then to target unit
        value_in_meters = value * from_info['base_to_meter']
        converted_value = value_in_meters / to_info['base_to_meter']
    elif from_info['type'] == 'weight':
        # Convert to base (grams) then to target unit
        value_in_grams = value * from_info['base_to_gram']
        converted_value = value_in_grams / to_info['base_to_gram']
    elif from_info['type'] == 'temperature':
        # Temperature conversions are non-linear
        if from_unit_norm == 'celsius':
            if to_unit_norm == 'fahrenheit':
                converted_value = (value * 9/5) + 32
            elif to_unit_norm == 'kelvin':
                converted_value = value + 273.15
            else: # celsius to celsius
                converted_value = value
        elif from_unit_norm == 'fahrenheit':
            if to_unit_norm == 'celsius':
                converted_value = (value - 32) * 5/9
            elif to_unit_norm == 'kelvin':
                converted_value = (value - 32) * 5/9 + 273.15
            else: # fahrenheit to fahrenheit
                converted_value = value
        elif from_unit_norm == 'kelvin':
            if to_unit_norm == 'celsius':
                converted_value = value - 273.15
            elif to_unit_norm == 'fahrenheit':
                converted_value = (value - 273.15) * 9/5 + 32
            else: # kelvin to kelvin
                converted_value = value
    
    return f"{value} {from_unit} is approximately {converted_value:.2f} {to_unit}."

@tool
def generate_random_number(min_val: int = 1, max_val: int = 100) -> int:
    """Generates a random integer within a specified range (inclusive).

    Args:
        min_val (int, optional): The minimum possible value. Defaults to 1.
        max_val (int, optional): The maximum possible value. Defaults to 100.

    Returns:
        int: A random integer between min_val and max_val.
    """
    if min_val > max_val:
        return "Error: Minimum value cannot be greater than maximum value."
    
    random_num = random.randint(min_val, max_val)
    print(f"[TOOL EXECUTION] generate_random_number: {random_num} (between {min_val} and {max_val})")
    return f"{random_num}"

@tool
def flip_coin() -> str:
    """Simulates a coin flip and returns either 'Heads' or 'Tails'.

    This tool does not require any parameters.

    Returns:
        str: "Heads" or "Tails".
    """
    result = random.choice(["Heads", "Tails"])
    print(f"[TOOL EXECUTION] flip_coin: {result}")
    return result

@tool
def search_web(query: str)-> Union[str, List[Dict[str, Any]]]:
    """Performs a web search using the Tavily API.

    Args:
        query: The search query string.

    Returns:
        A list of dictionaries, where each dictionary represents a search result,
        or a string message if no results were found.
    """
    
    print(f"[TOOL EXECUTION] search_web: {query}")

    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(query, num_results=5)

    search_results = response.get("results", [])
    
    if not search_results:
        return "No results found for the query."

    return search_results