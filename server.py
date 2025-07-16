import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai import get_ai_response
from memory.sqlite_setup import setup_database
from parsers.parse_being_json import load_being_json
from utils.rag_system import get_rag_context

app = FastAPI()

being = load_being_json()

def print_being_details():
    print("\n=== Being Configuration ===")
    print(f"Name: {being['name']}")
    print(f"Bio: {being['bio']}")
    print(f"Personality: {being['personality']}")
    print(f"Model Provider: {being['modelProvider']}")
    print(f"Context ID: {being['contextId']}")
    print(f"System Prompt: {being['system']}")
    print(f"Number of Knowledge Documents: {len(being['knowledge'])}")
    print(f"Number of Example Responses: {len(being['exampleResponses'])}")
    print("========================\n")

class Message(BaseModel):
    content: str

@app.get("/")
def root():
    return {"message": "Welcome to the Light Ai Framework!"}

@app.post("/message")
def get_message_response(message: Message):
    if not message.content:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    rag_context = get_rag_context(message.content, top_k=3)

    try:
        response = get_ai_response(being, rag_context, message.content)
        return {"response": response}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

@app.get("/being")
def get_being_details():
   return being

if __name__ == "__main__":

    try:
        if not being:
            raise ValueError("Being configuration is not loaded properly.")
        setup_database()
        print_being_details()
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"Database setup failed: {e}")
        print("Server will not start.")
        exit(1)
