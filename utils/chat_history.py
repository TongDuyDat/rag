import json
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def load_chat_history_from_json(file_path, session_id):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Lấy lịch sử chat của session cụ thể
    chat_history_cache =  data.get(session_id, [])
    
    memory = ConversationBufferMemory()

    for chat in chat_history_cache:
        human_msg = HumanMessage(content=chat["HumanChat"])
        ai_msg = AIMessage(content=chat["AIChat"])

        # Sử dụng chat_memory.add_message để lưu hội thoại đúng cách
        memory.chat_memory.add_message(human_msg)
        memory.chat_memory.add_message(ai_msg)
    return memory

# load_chat_history_from_json("chat_history.json", "session_research")
def load_chat_history_from_json_file(file_path, session_id):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Lấy lịch sử chat của session cụ thể
    chat_history_cache =  data.get(session_id, [])
    history_chat = []
    for chat in chat_history_cache:
        human_msg = HumanMessage(content=chat["HumanChat"])
        ai_msg = AIMessage(content=chat["AIChat"])
        history_chat.extend([human_msg, ai_msg])
    return history_chat
        # Sử dụng chat_memory.add_message để lưu hội thoại đúng cách