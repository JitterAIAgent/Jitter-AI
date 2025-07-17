import inspect
from functools import wraps
from typing import get_origin, get_args, Any

# Import the register_tool function from your tool_registry
from .tool_registry import register_tool

def _python_type_to_json_type(py_type: type) -> str:
    """Converts Python types to JSON schema types."""
    if py_type is str:
        return "string"
    if py_type is int:
        return "integer"
    if py_type is float:
        return "number"
    if py_type is bool:
        return "boolean"
    if get_origin(py_type) is list:
        return "array"
    if get_origin(py_type) is dict:
        return "object"
    # Add more type mappings as needed, or default to "string"
    return "string"

def tool(func):
    """
    Decorator to register a function as an AI tool.
    It automatically generates a tool schema from the function's signature and docstring.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # When the decorated function is called, simply execute the original function.
        # The decorator's main job is registration at import time, not runtime execution.
        return func(*args, **kwargs)

    # --- Tool Schema Generation ---
    tool_name = func.__name__
    tool_description = inspect.getdoc(func) or "" # Get docstring as description

    parameters = {}
    required_params = []

    sig = inspect.signature(func)

    for name, param in sig.parameters.items():
        if name == 'self' and inspect.ismethod(func): # Skip 'self' for methods if applicable
            continue

        param_type = param.annotation
        json_type = _python_type_to_json_type(param_type)

        param_info = {"type": json_type}

        # Handle optional/default values
        if param.default is inspect.Parameter.empty:
            required_params.append(name)
        else:
            param_info["default"] = param.default

        # Extract description from docstring (basic example, can be enhanced)
        # For more advanced docstring parsing (e.g., Google, Sphinx, NumPy style),
        # you might use a library like `docstring-parser` or write more robust parsing.
        # For this example, we'll keep it simple and just rely on the main docstring.
        # If you want per-parameter descriptions, you'd need a more complex docstring parser.

        parameters[name] = param_info

    tool_schema = {
        "name": tool_name,
        "description": tool_description,
        "parameters": {
            "type": "object",
            "properties": parameters,
            "required": required_params
        }
    }

    # Register the tool using the function from tool_registry
    register_tool(tool_name, func, tool_schema)

    return wrapper # Return the wrapper function