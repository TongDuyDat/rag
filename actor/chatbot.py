import json
from dotenv import load_dotenv
from pathlib import Path
import sys

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
sys.path.append("./")
_ = load_dotenv()

from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from router.chitchatDetector import ChitChatDetector
from router.reflection import ReflectionRouter
from router.semantic_router import TranslationRouter
from utils.chat_history import load_chat_history_from_json

from prompts import *
from actor.rag_chatbot import Retrieval_LLM

from vector_database.index_qdrant import (
    create_collection,
)


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
        print('*'*100)
        print(chitchat_response)
        print('*'*100)
        if chitchat_response.is_chitchat:
            print(chitchat_response)
            self.save_chat_cache(query, chitchat_response.context)
            return chitchat_response.context
        # if isinstance(chitchat_response.context, str):
        #     print(chitchat_response)
        #     self.save_chat_cache(query, chitchat_response.context)
        #     return chitchat_response.context
        response = self.retrieval_llm.invoke(query, chitchat_response.context)
        output = f"{response.page_content} "
        metadata = ", ".join(
            [
                f"source: {Path(r.source)} page: {r.page}"
                for r in response.metadata
            ]
        )

        metadata = metadata.replace("\\\\", "\\")
        self.save_chat_cache(query, output + metadata)
        return output + metadata

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


def create_chatbot() -> ChatBot:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
    llm_final = ChatGroq(model="llama-3.3-70b-specdec", temperature=0)
    # llm = ChatOpenAI(model="gpt-4o",
    #             temperature=0.5,
    #             max_tokens=None,
    #             timeout=None,
    #             max_retries=2,
    #             # api_key="...",
    #             # base_url="...",
    #             # organization="...",
    #             # other params...
    # )
    # llm_final = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=1)
    reflection_llm = ReflectionRouter(llm, sys=rewrite_prompt)
    translation_llm = TranslationRouter(llm, sys=translation_prompt)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=1024)
    vector_store = create_collection("langchain", embeddings, vector_size=1024)
    retrieval_chat = Retrieval_LLM(
        final_llm=llm_final,
        translation_llm=translation_llm,
        reflection_llm=reflection_llm,
        retrieval=vector_store,
        sys_prompt=human_prompt_v1,
    )
    chitchat_llm = ChitChatDetector(llm, re_write_all_prompt)
    chatbot = ChatBot(chitchat_llm=chitchat_llm, retrieval_llm=retrieval_chat)
    return chatbot, embeddings
