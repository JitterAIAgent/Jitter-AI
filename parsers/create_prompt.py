from parsers.parse_being_json import load_being_json

import sys

import os

from tools.built_in_tools import get_built_in_tools

from tools.tool_registry import TOOL_REGISTRY



built_in_tools_list = get_built_in_tools()



# being = load_being_json()



def create_system_prompt(rag, being):

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

        f"=== SYSTEM INSTRUCTIONS ===\n"

        f"{system}\n\n"



        f"=== CHARACTER GUIDELINES ===\n"

        f"- You are playing the role of: **{name}**\n"

        f"- Always respond **in character**, maintaining the tone, behavior, and background of this persona.\n"

        f"- EXCEPTION: When processing tool results, focus on using the data to answer the user's question accurately while maintaining your character's voice.\n\n"



        f"BACKGROUND:\n"

        f"{bio}\n\n"



        f"PERSONALITY TRAITS:\n"

        f"{personality}\n\n"



        f"KNOWLEDGE USAGE:\n"

        f"- Use any provided knowledge or facts naturally in conversation.\n"

        f"- Never say or imply that you are referencing external context.\n"

        f"- Weave information seamlessly into your responses.\n\n"



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

        

    prompt += (

        "\n=== TOOL USAGE INSTRUCTIONS ===\n"

        "WORKFLOW:\n"

        "1. If a user question requires a tool, call it using this format:\n"

        "   FUNCTION: <tool_name> PARAMS: { 'param1': 'value1', 'param2': 'value2' }\n"

        "   Example: FUNCTION: weather PARAMS: { 'location': 'New York' }\n\n"

        

        "2. When you receive tool results, IMMEDIATELY use them to answer the user's ORIGINAL question.\n"

        "   - The tool result is data for YOU to use, not something to acknowledge or comment on\n"

        "   - Integrate the information naturally into your character's response\n"

        "   - Do NOT say things like 'thanks for the data' or 'I already knew that'\n"

        "   - Focus on answering what the user actually asked\n\n"

        

        "3. CRITICAL: Tool results are meant to help you provide accurate, helpful answers.\n"

        "   Use them to inform your response, don't treat them as conversation.\n"

    )



    # Return the generated prompt

    # print(f"Generated system prompt: {prompt}")

    return prompt