import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

from memory.sqlite_actions import get_num_messages_by_id
from parsers.create_prompt import create_system_prompt
from utils.enums import Role

def google_gemini_provider(message, rag, previous_messages=[]):
    api_key = os.getenv("GOOGLE_API_KEY")
    model_id = os.getenv("GOOGLE_MODEL_ID", "gemini-1.5-flash")

    if not api_key:
        raise ValueError("API key for Google AI is not set in environment variables")
    if not message:
        raise ValueError("Message cannot be empty")

    # Configure the Gemini API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_id)

    try:
        history = []
        # Ensure chronological order: oldest first
        for msg, role, _ in sorted(previous_messages, key=lambda x: x[2]):
            if msg and msg.strip():
                gemini_role = "user" if role == Role.USER.value else "model"
                history.append({
                    "role": gemini_role,
                    "parts": [{"text": msg.strip()}]
                })

        # Create chat with history
        chat = model.start_chat(history=history)

        # Prepare the current message with system prompt for first message
        system_prompt = create_system_prompt(rag)
        final_message = f"{system_prompt}\n\n{message}"

        # Send the final message and get response
        response = chat.send_message(final_message)
        
        if not response or not response.text:
            raise ValueError("Empty response from Gemini")
            
        return response.text.strip()
        
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise ValueError(f"Failed to get response from Gemini: {str(e)}")

if __name__ == "__main__":
    try:
        response = google_gemini_provider("Hello!", "", "test-id")
        print(response)
    except Exception as e:
        print(f"Error: {e}")