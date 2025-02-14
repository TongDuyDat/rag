import sys

sys.path.append("./")
from pydantic import BaseModel, Field
from typing import Literal, Optional, Tuple

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from prompts import *
from utils.chat_history import load_chat_history_from_json


class ReflectionResponse(BaseModel):
    """Response from a chat model reflecting on the input message."""

    is_rewrite: bool = Field(
        ...,
        description="Indicates whether the message has been rewritten. Returns True if rewritten, otherwise False.",
    )
    rewrite_mes: str = Field(
        ...,
        description="The rewritten message if is_rewrite is True. If False, this contains the original user query.",
    )


class ReflectionRouter:
    def __init__(self, llm: BaseChatModel, sys=""):
        self.llm = llm.with_structured_output(ReflectionResponse)
        promt = ChatPromptTemplate.from_template(sys)
        self.chain = promt | self.llm

    def rewrite(self, history_chat, question: str)->ReflectionResponse:
        context = ""
        if history_chat:
            history_chat = history_chat.load_memory_variables(history_chat.memory_key)
            context = history_chat.get("history")
        response = self.chain.invoke({"context": context, "question": question})
        return response


# if __name__ == "__main__":
#     from prompts import *
#     from langchain_groq import ChatGroq

#     llm = ChatGroq(model="llama-3.3-70b-versatile")
#     detector = ReflectionRouter(llm, sys=rewrite_prompt)
#     chat_history = load_chat_history_from_json("chat_history.json", "session_1")
#     print(chat_history)
#     print(detector.rewrite(chat_history, "Xử lý ảnh là gì?"))
