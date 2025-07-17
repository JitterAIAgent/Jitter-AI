from parsers.parse_being_json import load_being_json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from tools.tool_registry import TOOL_REGISTRY


being = load_being_json()

def create_system_prompt(rag):
    system = being["system"]
    name = being['name']
    bio = being['bio']
    personality = being['personality']
    example_responses = being["exampleResponses"]
    tools = being["tools"]

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
    
    if len(tools) > 0:
        prompt += "\nTOOLS AVAILABLE:\n"
        # Iterate through tools and format them
        for tool_key in tools:
            # If tool is a string, look up in registry
            if isinstance(tool_key, str) and tool_key in TOOL_REGISTRY:
                reg = TOOL_REGISTRY[tool_key]
                prompt += f"- {reg['name']}: {reg['description']}\n"
                if 'parameters' in reg:
                    prompt += f"  Parameters: {reg['parameters']}\n"
            # If tool is a dict, use its info directly
            elif isinstance(tool_key, dict):
                prompt += f"- {tool_key.get('name', 'Unknown')}: {tool_key.get('description', '')}\n"
            else:
                prompt += f"- {str(tool_key)}\n"
        prompt += ("\nINSTRUCTION: To use a tool, reply with the following format on a single line:\n"
                   "FUNCTION: <tool_name> PARAMS: { 'param1': 'value1', 'param2': 'value2' }\n"
                   "Example: FUNCTION: weather PARAMS: { 'location': 'New York' }\n"
                   "I will handle the tool execution for you.\n")

    # Return the generated prompt
    # print(f"Generated system prompt: {prompt}")
    return prompt

if __name__ == "__main__":
    create_system_prompt("")