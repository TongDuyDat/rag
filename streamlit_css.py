import streamlit as st


def custom_css():
    st.markdown(
        """
        <style>
        /* Adjust button width to fit the sidebar */
        .stButton > button {
            width: 100%;
            text-align: left;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
            background-color: auto;
            color: white;
            font-size: 16px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #d1e7dd;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>
        /* Style for user messages (right-aligned) */
        .user-message {
            text-align: right;
            background-color: auto
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 100%;
            margin-left: auto;
            float: right;
        }

        /* Style for assistant messages (left-aligned) */
        .assistant-message {
            text-align: left;
            background-color: auto
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 100%;
            margin-right: auto;
        }

        /* Align avatars properly */
        .stChatMessage[data-baseweb="chat-message"] {
            display: flex;
            flex-direction: row;
        }

        /* User avatar on the right */
        .stChatMessage.user {
            justify-content: flex-end;
        }

        /* Assistant avatar on the left */
        .stChatMessage.assistant {
            justify-content: flex-start;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
