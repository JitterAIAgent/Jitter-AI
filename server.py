import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

from ai import get_ai_response
from memory.sqlite_setup import setup_database
from parsers.parse_being_json import load_being_json
from utils.rag_system import get_rag_context

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

being = load_being_json()

def print_being_details():
    print("\n" + "="*50)
    print("             BEING CONFIGURATION")
    print("="*50)
    
    print("\n" + "-"*20 + " PROVIDER " + "-"*20)
    print(f"Model Provider: {being['modelProvider']}")
    print(f"System Prompt: {being['system']}")
    
    print("\n" + "-"*20 + " CHARACTER " + "-"*20)
    print(f"Name: {being['name']}")
    print(f"Bio: {being['bio']}")
    print(f"Personality: {being['personality']}")
    print(f"Context ID: {being['contextId']}")
    
    print("\n" + "-"*20 + " KNOWLEDGE " + "-"*20)
    print(f"Knowledge Documents: {len(being['knowledge'])}")
    print(f"Example Responses: {len(being['exampleResponses'])}")
    print("\n" + "="*50 + "\n")

class Message(BaseModel):
    content: str

@app.get("/")
def root():
    return {"message": "Welcome to the Light Ai Framework!"}

@app.post("/message")
def get_message_response(message: Message):
    if not message.content:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        rag_context = get_rag_context(message.content, top_k=3)
        response = get_ai_response(being, rag_context, message.content)
        if not response:
            raise ValueError("AI response was empty")
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
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        print("Server will not start.")
        exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Server will not start.")
        exit(1)
