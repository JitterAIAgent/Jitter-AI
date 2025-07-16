from parsers.parse_being_json import load_being_json


being = load_being_json()

def create_system_prompt(rag):
    system = being["system"]
    name = being['name']
    bio = being['bio']
    personality = being['personality']

    prompt = (
        f"Your system instructions:\n {system}"
        f"You are {name}. "
        f"Your purpose is to be {bio}. "
        f"You are specifically designed to be {personality}.\n\n"
        f"{rag if rag else ''}"
    )

    # Return the generated prompt
    return prompt