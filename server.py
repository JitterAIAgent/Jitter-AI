import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ai import get_ai_response
from memory.sqlite_setup import setup_database
from parsers.parse_being_json import load_being_json

app = FastAPI()

being = load_being_json()

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
        response = get_ai_response(message.content)
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
        setup_database()
    except Exception as e:
        print(f"Database setup failed: {e}")
        print("Server will not start.")
        exit(1)
    uvicorn.run(app, host="127.0.0.1", port=8000)
    print("Server is running on http://localhost:8000")
    print("Use Ctrl+C to stop the server")