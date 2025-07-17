from parsers.parse_being_json import load_being_json
import sys
import os
from tools.built_in_tools import get_built_in_tools
from tools.tool_registry import TOOL_REGISTRY

built_in_tools_list = get_built_in_tools()

being = load_being_json()

def create_system_prompt(rag):
    system = being["system"]
    name = being['name']
    bio = being['bio']
    personality = being['personality']
    example_responses = being["exampleResponses"]
    tools = being["tools"]

    all_tools = built_in_tools_list + tools

    # Format RAG facts as background knowledge
    rag_facts = ""
    if rag:
        rag_lines = [line.strip() for line in rag.split('\n') if line.strip()]
        if rag_lines:
            rag_facts = "\nBackground knowledge you should use naturally in your answers:\n"
            for fact in rag_lines:
                rag_facts += f"- {fact}\n"

    prompt = (
        f"Your system instructions:\n{system}\n\n"
        f"IMPORTANT GUIDELINES:\n"
        f"1. You are {name}. You must ALWAYS respond in character, reflecting the personality and background described below.\n"
        f"2. Your background: {bio}\n"
        f"3. Your personality: {personality}\n"
        f"4. Use any provided knowledge to inform your answers, but do not state or imply that you are referencing external context.\n"
        f"5. Stay consistently in character for ALL responses.\n"
        f"{rag_facts}"
    )

    if example_responses:
        prompt += "\nEXAMPLE RESPONSES (for style and reference):\n"
        for ex in example_responses:
            prompt += f"- {ex}\n"
    
    if all_tools:
        prompt += "\nTOOLS AVAILABLE:\n"
        # Iterate through tools and format them
        for tool_key in all_tools:
            # If tool is a string, look up in registry
            if isinstance(tool_key, str) and tool_key in TOOL_REGISTRY:
                tool_data = TOOL_REGISTRY[tool_key]  # tool_data is {'function': <callable>, 'schema': {...}}
                
                # Access the schema from tool_data
                schema = tool_data['schema']
                
                # Get tool information from schema
                tool_name = schema.get('name', tool_key)
                tool_description = schema.get('description', 'No description available')
                
                prompt += f"- {tool_name}: {tool_description}\n"
                
                # Add parameters if they exist
                if 'parameters' in schema and 'properties' in schema['parameters']:
                    parameters = schema['parameters']['properties']
                    required_params = schema['parameters'].get('required', [])
                    
                    prompt += "  Parameters:\n"
                    for param_name, param_info in parameters.items():
                        param_type = param_info.get('type', 'string')
                        param_desc = param_info.get('description', 'No description')
                        is_required = "(REQUIRED)" if param_name in required_params else "(OPTIONAL)"
                        
                        prompt += f"    - {param_name} ({param_type}) {is_required}: {param_desc}\n"
                        
                        # Add default value if present
                        if 'default' in param_info:
                            prompt += f"      Default: {param_info['default']}\n"
                
            # If tool is a dict, use its info directly
            elif isinstance(tool_key, dict):
                tool_name = tool_key.get('name', 'Unknown')
                tool_description = tool_key.get('description', 'No description available')
                prompt += f"- {tool_name}: {tool_description}\n"
                
                # Add parameters if they exist in the dict
                if 'parameters' in tool_key:
                    prompt += f"  Parameters: {tool_key['parameters']}\n"
            else:
                prompt += f"- {str(tool_key)}: Tool not found in registry\n"
        
        prompt += ("\nINSTRUCTION: To use a tool, reply with the following format on a single line:\n"
                "FUNCTION: <tool_name> PARAMS: { 'param1': 'value1', 'param2': 'value2' }\n"
                "Example: FUNCTION: weather PARAMS: { 'location': 'New York' }\n"
                "I will handle the tool execution for you.\n")

    # Return the generated prompt
    print(f"Generated system prompt: {prompt}")
    return prompt

if __name__ == "__main__":
    create_system_prompt("")