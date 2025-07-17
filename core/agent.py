from memory.sqlite_actions import add_message, get_num_messages_by_id
from parsers.parse_being_json import load_being_json
from core.providers.open_router import open_router_provider
from core.providers.google import google_gemini_provider
from tools.handle_tool_call import is_tool_call, parse_tool_call, run_tool
from utils.enums import AI_Providers, Numbers, Role

def call_model(model_provider, message, rag_context, previous_messages):
    if model_provider == AI_Providers.OPENROUTER.value:
        return open_router_provider(message, rag_context, previous_messages)
    elif model_provider == AI_Providers.GOOGLE.value:
        return google_gemini_provider(message, rag_context, previous_messages)
    else:
        raise ValueError(f"Unsupported model provider specified: {model_provider}")

def get_ai_response(being, rag_context, message, max_iterations=5):
    context_id = being["contextId"]
    
    if not message:
        raise ValueError("Message cannot be empty")
    
    try:
        model_provider = being["modelProvider"]
        
        if not model_provider:
            raise ValueError("Model provider not specified in being.json")
        
        import datetime
        # Get previous messages from database for context
        previous_messages = get_num_messages_by_id(context_id, Numbers.MAX_MESSAGES.value)

        # Track messages for this conversation turn as list of tuples (msg, role, created_at)
        conversation_messages = [
            (msg, role, created_at) for *_, msg, role, created_at in previous_messages
        ] if previous_messages else []

        # Add current user message to database and to conversation
        now = datetime.datetime.now().isoformat()
        add_message(context_id, message, Role.USER.value)
        conversation_messages.append((message, Role.USER.value, now))

        # Handle tool calling loop with iteration limit
        for iteration in range(max_iterations):
            ai_response = call_model(model_provider, message, rag_context, conversation_messages)

            if not ai_response:
                raise ValueError("Received empty response from AI provider")

            # Add AI response to conversation
            now = datetime.datetime.now().isoformat()
            conversation_messages.append((ai_response, Role.ASSISTANT.value, now))

            # Check if this is a tool call
            if is_tool_call(ai_response):
                tool_name, params = parse_tool_call(ai_response)

                if tool_name:
                    tool_result = run_tool(tool_name, params)

                    # Add tool result to conversation
                    now = datetime.datetime.now().isoformat()
                    conversation_messages.append((tool_result, Role.TOOL.value, now))

                    # Continue the loop with the tool result as the new "message"
                    message = tool_result

                    return get_ai_response(being, rag_context, message, max_iterations - iteration - 1)
                else:
                    add_message(context_id, ai_response, Role.ASSISTANT.value)
                    return ai_response
            else:
                add_message(context_id, ai_response, Role.ASSISTANT.value)
                return ai_response

        # If we hit max iterations, return the last response
        add_message(context_id, ai_response, Role.ASSISTANT.value)
        return ai_response
        
    except Exception as e:
        print(f"AI Error: {str(e)}")
        raise  # Re-raise the exception to be handled by the caller

if __name__ == "__main__":
    # Example usage
    being = load_being_json()  # Load your being configuration
    response = get_ai_response(being, "", "what is my name")
    print(response)