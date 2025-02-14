import json
import sys

from langchain_openai import OpenAIEmbeddings


sys.path.append("./")
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from router.chitchatDetector import ChitChatDetector
from router.reflection import ReflectionRouter
from router.semantic_router import TranslationRouter
from utils.chat_history import load_chat_history_from_json

_ = load_dotenv()
from typing import List
from pydantic import BaseModel, Field
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from prompts import *
from actor.rag_chatbot import Retrieval_LLM
from vector_database.index_qdrant import (
    create_collection,
    search_qdrant,
    asearch_qdrant,
)
from langchain_groq import ChatGroq


class ChatBot:
    def __init__(self, chitchat_llm, retrieval_llm):
        self.chitchat_llm = chitchat_llm
        self.retrieval_llm = retrieval_llm

    def start_chat(self, chat_db, chat_session):
        # Load chat history from database
        chat_history = load_chat_history_from_json(chat_db, chat_session)
        # Initialize chatbot with loaded chat history
        self.chat_session = chat_session
        self.chat_history = chat_history
        self.chat_db = chat_db

    def get_answer(self, query):
        chitchat_response = self.chitchat_llm.invoke(query, self.chat_history)
        if chitchat_response.is_chitchat:
            self.save_chat_cache(query, chitchat_response.context)
            print(chitchat_response)
            return chitchat_response.context
        response = self.retrieval_llm.invoke(query, self.chat_history)
        output = f'{response.page_content}\n{"source: " + response.metadata.get("source", "") if "source" in response.metadata else ""} {"page: "+str(response.metadata["page"]) if "page" in response.metadata else ""}'
        self.save_chat_cache(query, output)
        return output

    def save_chat_cache(self, input, output):
        # Save chat history to database
        human_msg = HumanMessage(content=input)
        ai_msg = AIMessage(content=output)
        # Sử dụng chat_memory.add_message để lưu hội thoại đúng cách
        self.chat_history.chat_memory.add_message(human_msg)
        self.chat_history.chat_memory.add_message(ai_msg)

    def save_on_disk(self):
        # Save chat history to disk
        history = [
            {
                "HumanChat": msg.content,
                "AIChat": self.chat_history.chat_memory.messages[i + 1].content,
            }
            for i, msg in enumerate(self.chat_history.chat_memory.messages[:-1])
            if isinstance(msg, HumanMessage)
        ]
        try:
            with open(self.chat_db, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data[self.chat_session] = history
        with open(self.chat_db, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


# if __name__ == "__main__":


#     llm = ChatGroq(model="llama-3.3-70b-specdec")
#     llm_final = ChatGroq(model="llama-3.3-70b-versatile")
#     # final_llm = ChatGroq(model="llama-3.3-70b-vers")
#     reflection_llm = ReflectionRouter(llm, sys=rewrite_prompt)
#     translation_llm = TranslationRouter(llm, sys=translation_prompt)
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#     vector_store = create_collection("langchain", embeddings)
#     retrieval_chat = Retrieval_LLM(
#         final_llm=llm_final,
#         translation_llm=translation_llm,
#         reflection_llm=reflection_llm,
#         retrieval=vector_store,
#         sys_prompt=human_prompt,
#     )
#     chitchat_llm = ChitChatDetector(llm, chitchat_prompt)
#     chatbot = ChatBot(chitchat_llm=chitchat_llm, retrieval_llm=retrieval_chat)
#     chatbot.start_chat("chat_history.json", "session_3")
#     print(chatbot.get_answer("MultiHead⁡Attention là gì"))
#     chatbot.save_on_disk()
#     # chat_history = load_chat_history_from_json("chat_history.json", "session_1")
def create_chatbot() -> ChatBot:
    llm = ChatGroq(model="llama-3.3-70b-specdec", temperature=0)
    llm_final = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
    # final_llm = ChatGroq(model="llama-3.3-70b-vers")
    reflection_llm = ReflectionRouter(llm, sys=rewrite_prompt)
    translation_llm = TranslationRouter(llm, sys=translation_prompt)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector_store = create_collection("langchain", embeddings)
    retrieval_chat = Retrieval_LLM(
        final_llm=llm_final,
        translation_llm=translation_llm,
        reflection_llm=reflection_llm,
        retrieval=vector_store,
        sys_prompt=human_prompt,
    )
    chitchat_llm = ChitChatDetector(llm, chitchat_prompt)
    chatbot = ChatBot(chitchat_llm=chitchat_llm, retrieval_llm=retrieval_chat)
    return chatbot
