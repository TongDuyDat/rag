import sys

sys.path.append("./")
from pydantic import BaseModel, Field
from typing import Literal, Optional, Tuple

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate


class ChitChatResponse(BaseModel):
    """ChitChatResponse model definition"""

    is_chitchat: bool = Field(
        ...,
        description="a boolean indicating success status",
    )
    context: Optional[str] = Field(
        ...,
        description="The response from the chat model. If query is a chichat query response is a str answer else respone is ''",
    )


class ChitChatDetector:
    def __init__(self, llm: BaseChatModel, sys_prompt):
        self.llm = llm.with_structured_output(ChitChatResponse)
        self.chit_chat_prompt = sys_prompt

    def invoke(self, query, history_chat) -> ChitChatResponse:
        """Invoke the ChitChatDetector model to detect whether a query is a chit-chat query
        Args:
        query (str): The query to be detected
        Returns:
        ChitChatResponse: A response containing a boolean indicating success status and a string message
        """
        context = ""
        if history_chat:
            history_chat = history_chat.load_memory_variables(history_chat.memory_key)
            context = history_chat.get("history")
        prompt = ChatPromptTemplate.from_template(self.chit_chat_prompt)
        chain = prompt | self.llm
        print({"input_query": query, "history_chat": context})
        response = chain.invoke({"input_query": query, "history_chat": context})
        return response


# if __name__ == "__main__":
#     from prompts import *
#     from langchain_groq import ChatGroq

#     llm = ChatGroq(model="llama-3.3-70b-versatile")
#     detector = ChitChatDetector(llm, chitchat_prompt)
#     print(detector.invoke("What is image captioning?"))
