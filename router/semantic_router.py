import sys

sys.path.append("./")
from pydantic import BaseModel, Field
from typing import Literal, Optional, Tuple, List

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from prompts import *
from utils.chat_history import load_chat_history_from_json


class TranslationResponse(BaseModel):
    queries: List[str] = Field(
        ...,
        description="A list of translated queries. Each item represents a possible translation of the input text.",
    )

class TranslationRouter:
    def __init__(self, llm: BaseChatModel, sys=""):
        self.llm = llm.with_structured_output(TranslationResponse)
        prompt = ChatPromptTemplate.from_template(
            sys
        )
        self.chain = prompt| self.llm
    def invoke(self, query: str)->TranslationResponse:
        response = self.chain.invoke({
            "question":query
        })
        return response

# if __name__ == "__main__":
#     from prompts import *
#     from langchain_groq import ChatGroq

#     llm = ChatGroq(model="llama-3.3-70b-versatile")
#     detector = TranslationRouter(llm, sys=translation_prompt)
#     chat_history = load_chat_history_from_json("chat_history.json", "session_1")
#     print(chat_history)
#     print(detector.invoke("Xử lý ảnh là gì?"))

