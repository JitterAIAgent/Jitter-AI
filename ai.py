from memory.sqlite_actions import add_message
from parsers.parse_being_json import load_being_json
from providers.open_router import open_router_provider
from utils.enums import AI_Providers, Role

being = load_being_json()
context_id = being["contextId"]

def get_ai_response(message):

    if not message:
        raise ValueError("Message cannot be empty")
    
    try:
        model_provider = being["modelProvider"]

        if not model_provider:
            raise ValueError("Model provider not specified in being.json")
            
        if model_provider == AI_Providers.OPENROUTER.value:

            ai_response = open_router_provider(message, context_id)

            add_message(context_id, message, Role.USER.value)
            add_message(context_id, ai_response, Role.ASSISTANT.value)

            return ai_response
        else:
            raise ValueError("Unsupported model provider specified.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    response = get_ai_response("what is my name")
    print(response)
