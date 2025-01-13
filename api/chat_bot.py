from fastapi import APIRouter, WebSocket
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

from agents.bot import Bot
from agents.handler_streaming import CustomAsyncHandler
from vector_database.index_qdrant import create_collection
_ = load_dotenv()
chat_bot  = APIRouter()
@chat_bot.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    callbacks = [CustomAsyncHandler(websocket)]
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", callbacks=callbacks)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = create_collection("langchain", embeddings)
    bot = Bot (model, embeddings, vector_store)
    bot.start()
    
    await websocket.send_text("Hello WebSocket!")
    while True:
        data = await websocket.receive_text()
        await bot.answer(data)
        # await websocket.send_text(f"Received: {data}")
