import os
import requests
import json

from memory.sqlite_actions import get_num_messages_by_id
from parsers.create_prompt import create_system_prompt

def open_router_provider(message):
    model = os.getenv("OPENROUTER_MODEL_ID", "moonshotai/kimi-k2:free")
    api_key = os.getenv("OPENROUTER_API_KEY")

    system_prompt = create_system_prompt()

    previous_messages = get_num_messages_by_id("kim-kardashian", 10)

    messages = [{"role": "system", "content": system_prompt}]
    # Add previous messages to the array
    for msg, role, created_at in reversed(previous_messages):
        messages.append({"role": role, "content": msg})
    # Add the current user message
    messages.append({"role": "user", "content": message})

    if not api_key:
        raise ValueError("API key for OpenRouter is not set in environment variables")
    if not message:
        raise ValueError("Message cannot be empty")
    if not model:
        raise ValueError("Model ID is not specified in environment variables or defaults")
    
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": model,
            "messages": messages,
            
        })
    )

    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

if __name__ == "__main__":
    # Example usage
    api_key = os.getenv("OPENROUTER_API_KEY")
    test_response = open_router_provider("hello", "moonshotai/kimi-k2:free", api_key, "You are a helpful assistant.")
    print(test_response)  # Should print the response from the model