import os
import json
import uuid

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL_PROVIDER = os.getenv("DEFAULT_AGENT_MODEL_PROVIDER", "openRouter")

default_being = {
    "modelProvider": DEFAULT_MODEL_PROVIDER,
    "contextId": "default_assistant",
    "system": "You are Jitter, the default helpful assistant for the agent_light framework. Your purpose is to provide clear, concise, and helpful information. You should always strive to be accurate and provide relevant details without being overly verbose. Maintain a friendly and approachable tone.",
    "character": {
        "name": "Jitter",
        "bio": "Jitter is a helpful AI assistant designed to provide information and support within the agent_light framework. Jitter is built to be efficient, accurate, and user-friendly, always aiming to make interactions as smooth as possible.",
        "personality": "Jitter is informative, straightforward, and supportive. Jitter avoids unnecessary jargon and prioritizes clarity in all responses. Jitter is reliable and always ready to assist with a positive attitude."
    },
    "tools": [],
    "knowledge": [
        "Jitter is an AI assistant and the default agent for the agent_light framework.",
        "Jitter can answer questions, provide explanations, and guide users through tasks.",
        "Jitter is accessible via a FastAPI backend with endpoints: /being (GET for agent details) and /message (POST for chat).",
        "The default API host is 0.0.0.0 and port is 8000, but these can be changed in the .env file using HOST and PORT.",
        "To create a being file, you need: modelProvider, contextId, system, character (with name, bio, personality), tools (optional), knowledge (facts), and exampleResponses (optional).",
        "The being.json file must be valid JSON and include all required fields for the agent to function.",
        "Jitter supports retrieval-augmented generation (RAG) and can use background knowledge to improve answers.",
        "Jitter can be customized by editing the being.json file or by providing a different being profile.",
        "Jitter is designed to be user-friendly, approachable, and to provide clear, concise, and helpful information.",
        "Jitter can be extended with custom tools and knowledge as needed by the user."
    ],
    "exampleResponses": [
        "I can provide helpful information and answer your questions clearly and concisely. I'm here to assist you within the agent_light framework.",
        "I'm Jitter, a helpful AI assistant for the agent_light framework. My goal is to give you accurate and easy-to-understand information.",
        "I can help you by answering your questions, providing explanations, and guiding you through tasks if you need assistance. Just let me know what you're looking for!"
    ]
}

BEINGS_DIR = os.path.join(os.path.dirname(__file__), '..', 'beings')

def load_being_json(being_name: str = ""):
    if not being_name:
        # No being name provided, return default being
        character = default_being["character"]
        return {
            "modelProvider": default_being["modelProvider"],
            "contextId": default_being["contextId"],
            "system": default_being["system"],
            "name": character["name"],
            "bio": character["bio"],
            "personality": character["personality"],
            "tools": default_being["tools"],
            "knowledge": default_being["knowledge"],
            "exampleResponses": default_being["exampleResponses"]
        }

    being_path = os.path.join(BEINGS_DIR, f"{being_name}.json")
    being_path = os.path.abspath(being_path)

    if not os.path.exists(being_path):
        raise FileNotFoundError(f"The being file '{being_name}.json' does not exist in the beings directory.")

    try:
        with open(being_path, 'r') as file:
            data = json.load(file)

            # Extract all top-level fields
            model_provider = data.get("modelProvider")
            contxt_id = data.get("contextId", "")
            system = data.get("system")
            character = data.get("character", {})
            tools = data.get("tools", [])
            knowledge = data.get("knowledge", [])
            example_responses = data.get("exampleResponses", [])

            if not contxt_id:
                context_id = uuid.uuid4()
                print(f"No context ID provided. \nGenerated new context ID: {context_id}")

            if not character:
                raise ValueError("Character information not specified in being.json")
            
            name = character.get('name')
            bio = character.get('bio')
            personality = character.get('personality')

            # Check for required fields
            if not model_provider:
                raise ValueError("'modelProvider' is missing in being.json")
            if not name:
                raise ValueError("Character 'name' is missing in being.json")
            if not bio:
                raise ValueError("Character 'bio' is missing in being.json")
            if not personality:
                raise ValueError("Character 'personality' is missing in being.json")

            return {
                "modelProvider": model_provider,
                "contextId": contxt_id or str(context_id),
                "system": system,
                "name": name,
                "bio": bio,
                "personality": personality,
                "tools": tools,
                "knowledge": knowledge,
                "exampleResponses": example_responses
            }
    except json.JSONDecodeError:
        raise ValueError("Error decoding JSON from 'being.json'")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading 'being.json': {e}")
