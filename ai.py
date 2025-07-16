from memory.sqlite_actions import add_message
from parsers.parse_being_json import load_being_json
from providers.open_router import open_router_provider
from providers.google import google_gemini_provider
from utils.enums import AI_Providers, Role 

def get_ai_response(being, rag_context, message):
    context_id = being["contextId"]

    if not message:
        raise ValueError("Message cannot be empty")
    
    try:
        model_provider = being["modelProvider"]

        if not model_provider:
            raise ValueError("Model provider not specified in being.json")
            
        if model_provider == AI_Providers.OPENROUTER.value:
            ai_response = open_router_provider(message, rag_context, context_id)
        elif model_provider == AI_Providers.GOOGLE.value:
            ai_response = google_gemini_provider(message, rag_context, context_id)
        else:
            raise ValueError(f"Unsupported model provider specified: {model_provider}")

        if not ai_response:
            raise ValueError("Received empty response from AI provider")

        add_message(context_id, message, Role.USER.value)
        add_message(context_id, ai_response, Role.ASSISTANT.value)

        return ai_response
        
    except Exception as e:
        print(f"AI Error: {str(e)}")
        raise  # Re-raise the exception to be handled by the caller

if __name__ == "__main__":
    # Example usage
    response = get_ai_response("what is my name")
    print(response)
