import os
import json

def load_being_json():
    being_path = os.path.join(os.path.dirname(__file__), '..', 'being.json')
    being_path = os.path.abspath(being_path)

    if not os.path.exists(being_path):
        raise FileNotFoundError("The 'being.json' file does not exist")
    
    try:
        with open(being_path, 'r') as file:
            data = json.load(file)
            
            # Extract all top-level fields
            model_provider = data.get("modelProvider")
            system = data.get("system")
            character = data.get("character", {})
            tools = data.get("tools", [])
            knowlege = data.get("knowlege", [])
            example_responses = data.get("exampleResponses", [])

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
                "system": system,
                "character": character,
                "name": name,
                "bio": bio,
                "personality": personality,
                "tools": tools,
                "knowlege": knowlege,
                "exampleResponses": example_responses
            }
    except json.JSONDecodeError:
        raise ValueError("Error decoding JSON from 'being.json'")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading 'being.json': {e}")
