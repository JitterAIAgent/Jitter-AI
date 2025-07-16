import os
import requests
import json

def open_router_provider(message):
    model = os.getenv("OPENROUTER_MODEL_ID", "moonshotai/kimi-k2:free")
    api_key = os.getenv("OPENROUTER_API_KEY")

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
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            
        })
    )

    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

if __name__ == "__main__":
    # Example usage
    api_key = os.getenv("OPENROUTER_API_KEY")
    test_response = open_router_provider("hello", "moonshotai/kimi-k2:free", api_key, "You are a helpful assistant.")
    print(test_response)  # Should print the response from the model