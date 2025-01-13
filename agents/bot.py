from dotenv import load_dotenv

_ = load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from agents.agents import Agents
from vector_database.index_qdrant import create_collection
from prompts.prompt_template import *
from agents.handler_streaming import CustomAsyncHandler

class Bot:
    def __init__(self, llm, embedding, vector_store):
        self.llm = llm
        self.embeddings = embedding 
        self.vector_store = vector_store

    def start(self):
        self.agents = Agents(self.llm, self.embeddings, self.vector_store)

    async def answer(self, questions):
        response = self.agents.chat(questions)
        for chunk in response:
            chunk

