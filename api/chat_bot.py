from fastapi import APIRouter, WebSocket
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

from vector_database.index_qdrant import create_collection
_ = load_dotenv()
chat_bot  = APIRouter()
@chat_bot.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    await websocket.send_text("Hello WebSocket!")
    while True:
        data = await websocket.receive_text()
        
        # await websocket.send_text(f"Received: {data}")
