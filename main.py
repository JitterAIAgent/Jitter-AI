from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import typer
import asyncio
import threading

import uvicorn
from core.agent import get_ai_response
from parsers.parse_being_json import load_being_json
from utils.print_details import print_being_details
from utils.rag_system import get_index_model, get_rag_context
from utils.tool_importer import import_tools

server_app = FastAPI()
app = typer.Typer()

# Add CORS middleware
server_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

being = load_being_json()

model_index = get_index_model(being)

class Message(BaseModel):
    content: str

@server_app.get("/being")
async def get_being_details():
   return being


@server_app.post("/message")
async def get_message_response(message: Message):
    if not message.content:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        rag_context = get_rag_context(being,model_index[0],model_index[1],message.content, top_k=3)
        response = get_ai_response(being, rag_context, message.content)
        if not response:
            raise ValueError("AI response was empty")
        return {"response": response}
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

async def start_server():
    config = uvicorn.Config(app=server_app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

async def tweet_genertor(wait_time: int):
    """
    Simulate a tweet generator that runs in the background.
    """
    while True:
        rag_context = get_rag_context(being,model_index[0],model_index[1],"tweet something in the style of your personality don't repeat any tweets", top_k=3)
        response = get_ai_response(being, rag_context, "tweet something in the style of your personality")

        print(f"Generated Tweet: {response}")
        
        await asyncio.sleep(wait_time * 60)

async def main_loop():
    """
    Main loop that runs the tweet generator and handles other tasks.
    """
    await asyncio.gather(
        start_server(),
        tweet_genertor(1),  # Generate a tweet every minute
    )

@app.command()
def start(name: str = typer.Argument("being", help="Name of the application")):
    """
    Start the application with its orchestrator and input handlers.
    """
    typer.echo(f"Welcome to Agent Light Framework!\nStarting...")
    try:
        asyncio.run(main_loop())
    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()