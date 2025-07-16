from parsers.parse_being_json import load_being_json

being = load_being_json()

def create_message_prompt(message):
    if not message:
        raise ValueError("Message cannot be empty")
    
    system = being["system"]
    name = being['name']
    bio = being['bio']
    personality = being['personality']

            
    prompt = (
        f"Your system instructions:\n {system}"
        f"You are {name}. "
        f"Your purpose is to be {bio}. "
        f"You are specifically designed to be {personality}.\n\n"
        f"User: {message}\n"
        f"{name}:"
    )

    print(prompt)  # Debugging line to see the generated prompt
    # Return the generated prompt
    return prompt