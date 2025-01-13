import asyncio
from typing import Any, Dict, List

from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackHandler
from langchain_core.messages import HumanMessage
from langchain_core.outputs import LLMResult

class CustomAsyncHandler(AsyncCallbackHandler):
    
    def __init__(self, websocket):
        super().__init__()
        self.websocket = websocket
    
    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        # print("Async model starting...")
        await asyncio.sleep(0.3)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        # print("Async model ending...")
        await asyncio.sleep(0.3)

    async def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[HumanMessage], **kwargs: Any
    ) -> None:
        print("Chat model is starting...")
        await asyncio.sleep(0.3)

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(token, end= " ")
        await self.websocket.send_text(token)
        await asyncio.sleep(0.05)

