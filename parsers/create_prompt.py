from parsers.parse_being_json import load_being_json


being = load_being_json()

def create_system_prompt(rag):
    system = being["system"]
    name = being['name']
    bio = being['bio']
    personality = being['personality']
    example_responses = being["exampleResponses"]

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

    # Return the generated prompt
    # print(f"Generated system prompt: {prompt}")
    return prompt