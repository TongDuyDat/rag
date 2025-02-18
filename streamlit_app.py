from pathlib import Path
import re
import streamlit as st
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import json
import os
import PyPDF2  # Thêm thư viện để đọc file PDF
from dotenv import load_dotenv

from actor.chatbot import create_chatbot
from streamlit_css import custom_css
from utils.chat_history import load_chat_history_from_json_file
from utils.read_docs import process_file

# Load environment variables
load_dotenv()

chatbot, embeddings = create_chatbot()

# Function to generate response from the model
def generate_response(prompt):
    model = ChatGroq(model="llama-3.3-70b-specdec")
    response = model.invoke(prompt)
    return response


# Function to save chat history to JSON file
def save_chat_history_to_json_file(file_path, session_id, chat_history):
    if not os.path.exists(file_path):
        data = {"sessions": {}}
    else:
        with open(file_path, "r") as f:
            data = json.load(f)
    sessions = data.get("sessions", {})
    sessions[session_id] = chat_history
    data["sessions"] = sessions
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


# Streamlit app layout
st.title("Chat Application with File Upload and Session Management")


# Main Streamlit app
def main():
    # Define the path to the chat history JSON file
    chat_history_file = "chat_history.json"
    custom_css()
    # Sidebar for session management and file upload
    with st.sidebar:
        st.title("💬 ChatGPT-like App")

        # Load existing sessions
        if os.path.exists(chat_history_file):
            with open(chat_history_file, "r", encoding="utf-8") as file:
                data = json.load(file)
            sessions = data
            session_ids = list(sessions.keys())
        else:
            session_ids = []

        # Display existing sessions
        if st.session_state.get("session_id", None) is None:
            st.session_state.session_id = str(datetime.now())
        if st.button("New Chat"):
            st.session_state.session_id = str(datetime.now())
        st.subheader("History Chat")
        # selected_session = None
        for session_id in session_ids:
            if st.button(session_id):
                st.session_state.session_id = session_id
        if "session_id" in st.session_state:
            chatbot.start_chat(chat_history_file, st.session_state.session_id)
            st.session_state.chat_history = load_chat_history_from_json_file(
                chat_history_file, st.session_state.session_id
            )

        st.subheader("File Upload")
        uploaded_file = st.file_uploader(
            "Upload a file (.txt, .pdf)", type=["txt", "pdf"]
        )
        if uploaded_file is not None:
            if st.button("Submit"):
                process_file(uploaded_file, st, embeddings)
            
        # st.session_state.session_id = session_id
    # Main chat interface
    st.title("Chat with AI 🤖")
    st.caption("Type your message below and press Enter to chat.")

    # Initialize chat history in session state
    # Display chat history
    for message in st.session_state.get("chat_history", []):
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(
                    f'<div class="user-message">{message.content}</div>',
                    unsafe_allow_html=True,
                )
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                # Tìm đường dẫn file PDF trong phản hồi
                match = re.search(r"source:\s*(.*?\.pdf)", message.content)
                # Loại bỏ đường dẫn khỏi nội dung để tránh trùng lặp
                content_cleaned = re.sub(r"source:\s*(.*?\.pdf)", "", message.content).strip() if match else message.content
                # Hiển thị nội dung tin nhắn của AI
                st.markdown(
                    f'<div class="assistant-message"> {content_cleaned}</div>',
                    unsafe_allow_html=True,
                )
                pattern = r"source:\s*(.+?)\s*page:\s*(\d+)"
                matches = re.findall(pattern, message.content)
                # Nếu có file PDF, hiển thị link tải
                # txt_source = ""
                for match in matches:
                    file_path = match[0]
                    file_url = Path(file_path).as_uri()
                    txt_source = f"[file]({file_url})"
                    st.markdown(f"📄 **Page: {match[1]}** {txt_source}")
    # User input for chat
    user_input = st.chat_input("Type your message here...")
    model_response = ""
    if user_input:
        # Display user message
        with st.chat_message("user"):
                st.markdown(
                    f'<div class="user-message">{user_input}</div>',
                    unsafe_allow_html=True,
                )
        # Tạo và hiển thị phản hồi của AI
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                model_response = chatbot.get_answer(user_input)
                # Tìm đường dẫn file PDF trong phản hồi
                match = re.search(r"source:\s*(.*?\.pdf)", model_response)
                # Loại bỏ đường dẫn khỏi nội dung gốc để tránh trùng lặp
                if match:
                    file_path = match.group(1)

                    model_response = re.sub(r"source:\s*(.*?\.pdf)", "", model_response).strip()
                    file_url = Path(file_path).as_uri()
                # Hiển thị nội dung phản hồi
                st.markdown(model_response)
                # Nếu tìm thấy file, hiển thị link tải
                pattern = r"source:\s*(.+?)\s*page:\s*(\d+)"
                matches = re.findall(pattern, model_response)
                # Nếu có file PDF, hiển thị link tải
                # txt_source = ""
                for match in matches:
                    try:
                        file_path = match[0]
                        file_url = Path(file_path).as_uri()
                        txt_source = f"[file]({file_url})"
                        st.markdown(f"📄 **Page: {match[1]}** {txt_source}")
                    except:
                        continue
                    
        st.session_state.chat_history.append(model_response)
        chatbot.save_on_disk()
        # Save chat history to JSON file
        # save_chat_history_to_json_file(
        #     chat_history_file, session_id, st.session_state.chat_history
        # )
if __name__ == "__main__":
    main()
