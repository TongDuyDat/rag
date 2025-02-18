import sys

sys.path.append("./")
from pydantic import BaseModel, Field
from typing import Literal, Optional, Tuple, List, Union

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate


class TranslationResponse(BaseModel):
    queries: List[str] = Field(
        ...,
        description="A list of translated queries. Each item represents a possible translation of the input text.",
    )


class ChitChatResponse(BaseModel):
    """ChitChatResponse model definition"""

    is_chitchat: bool = Field(
        ...,
        description="A boolean indicating whether the question is chitchat.",
    )
    context: Optional[Union[TranslationResponse, str]] = Field(
        ...,
        description=(
            "If the question is chitchat, this contains a direct answer as a string."
            "Otherwise, it contains a TranslationResponse object with a list of search queries."
        ),
    )


class ChitChatDetector:
    def __init__(self, llm: BaseChatModel, sys_prompt):
        # self.llm = llm.with_structured_output(ChitChatResponse)
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
            context = history_chat.get("chat_history")
        prompt = ChatPromptTemplate.from_template(self.chit_chat_prompt)
        chain = prompt | self.llm
        response = chain.invoke({"question": query, "chat_history": context})
        return response


# if __name__ == "__main__":
#     from prompts import *
#     from langchain_groq import ChatGroq

#     llm = ChatGroq(model="llama-3.3-70b-versatile")
#     detector = ChitChatDetector(llm, re_write_all_prompt)
#     print(detector.invoke("What is image captioning?"))
