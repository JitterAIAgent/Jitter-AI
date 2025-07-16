from parsers.create_prompt import create_message_prompt
from parsers.parse_being_json import load_being_json
from providers.open_router import open_router_provider

being = load_being_json()

def get_ai_response(message):

    if not message:
        raise ValueError("Message cannot be empty")
    
    prompt = create_message_prompt(message)

    if not prompt:
        raise ValueError("Failed to create prompt from message")
    
    try:
        model_provider = being["modelProvider"]

        if not model_provider:
            raise ValueError("Model provider not specified in being.json")
            
        if model_provider == "openRouter":
            return open_router_provider(prompt)
        else:
            raise ValueError("Unsupported model provider specified.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    response = get_ai_response("Whos is Ray J")
    print(response)
