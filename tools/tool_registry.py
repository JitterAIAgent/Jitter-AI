TOOL_REGISTRY = {}

# Example structure for an entry:
# TOOL_REGISTRY = {
#     "tool_name_1": {
#         "function": <python_callable_for_tool_1>,
#         "schema": {
#             "name": "tool_name_1",
#             "description": "...",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "param1": {"type": "string"},
#                     "param2": {"type": "number"}
#                 },
#                 "required": ["param1"]
#             }
#         }
#     },
#     "tool_name_2": { ... }
# }

def register_tool(tool_name: str, tool_function, tool_schema: dict):
    """Registers a tool with its function and schema."""
    if tool_name in TOOL_REGISTRY:
        print(f"[WARNING] Tool '{tool_name}' is already registered. Overwriting.")
    TOOL_REGISTRY[tool_name] = {
        "function": tool_function,
        "schema": tool_schema
    }
    print(f"[INFO] Tool '{tool_name}' registered successfully.")

def get_tool_function(tool_name: str):
    """Retrieves the callable function for a registered tool."""
    tool_info = TOOL_REGISTRY.get(tool_name)
    return tool_info["function"] if tool_info else None

def get_tool_schema(tool_name: str):
    """Retrieves the schema for a registered tool."""
    tool_info = TOOL_REGISTRY.get(tool_name)
    return tool_info["schema"] if tool_info else None

def get_all_tool_schemas():
    """Returns a list of all registered tool schemas."""
    return [info["schema"] for info in TOOL_REGISTRY.values()]