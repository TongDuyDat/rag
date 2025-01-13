import re
import os
from typing import List, TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from router.semantic_router import SemanticRouter
from vector_database.index_qdrant import add_to_qdrant, create_collection, search_qdrant

from utils.pdf import PyPDFLoaderCustom
from prompts.prompt_template import *
from prompts.chitchat_samples import *
# os.environ["GOOGLE_API_KEY"] = "AIzaSyAmoDTzkD8v7G15Y8q7rfTzISZKSYtBktY"
# os.environ["PINECONE_API_KEY"] = "9126bd8c-0b55-44c5-ad19-fbc485c70ea7"





class Agents:
    def __init__(self, llm, embdding, vector_store=None, system=""):
        self.llm = llm
        self.embedding = embdding
        self.tools_name = ["rag_chat", "search"]
        self.tools = {
            "rag_chat": self.rag_chat,
            "search": self.search
        }
        self.vector_store = vector_store
        self.system = system
        self.chitchat_router = SemanticRouter(llm, sys= chitchat_prompt)
        self.history = [SystemMessage(content=self.system.format(tools=self.tools_name))]
        
    def rag_chat(self, question):
        documents = search_qdrant(question, self.vector_store, 5)
        context = ""
        if not documents:
            return 
        for i, doc in  enumerate(documents):
            text = doc.page_content.replace("\n", " ")
            metadata = " ".join([f"{k}: {v}" for k, v in doc.metadata.items()])
            context += f"Context:\n context {i}: {text}\nmetadata: {metadata}\n"
        print({
            "Questions: ": question,
            "Context: ": context
        })
        prompt = human_prompt.format(question=question, context=context)
        response = self.llm.stream([HumanMessage(content=prompt)])
        return response

    def extract_message(self, history_chat: list,  question:str):
        context = ""
        if history_chat:
            for message in history_chat:
                if isinstance(message, HumanMessage):
                    context += "HumanChat:\n" + message.content + "\n"
                if isinstance(message, AIMessage):
                    context += "AIChat:\n" + message.content + "\n"
        prompt = '''Base on the history chat and the provided question. Your task is rewrite the last human input to reflect what the human is actually asking and ensure similarity search engines can find relevant data.
        ### Emample:
        HumanChat: What is image captioning?
        AIChat: What is image captioning?
        HumanChat: further explanation.
        AIChat: Explains more information about Image captioning ?
        Humanchat: What is Transformer Model?
        AIChat: What is Transformer Model?
        Humanchat: Show more info
        AIChat: Give me more infomation about Transformer model?
        
        ### Rules:
        - Extract a question that fits the context of the previous chat.
        - The extracted question should as close to the previous question as possible.
        - If you can not extract a question, return the question that human asked.
        - When return only return the question.
        History Chat:{context}
        Question: {question}
        '''
        response = self.llm.invoke([HumanMessage(content=prompt.format(context=context, question=question))])
        return response
    
    def search(self, question):
        response = self.extract_message(self.history, question)
        return response
    
    def chat(self, message):
        # Tash classification
        if self.chitchat_router.is_chitchat(message):
            return self.llm.stream([HumanMessage(content=message)])
        self.history.append(HumanMessage(content=message))
        question_response = self.search(message)
        if question_response:
            self.history.append(AIMessage(content=question_response.content))
        else:
            self.history.append(HumanMessage(content=message))
        response = self.rag_chat(question_response.content)
        return response