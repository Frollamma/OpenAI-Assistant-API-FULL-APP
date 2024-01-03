from openai import OpenAI
import streamlit as st
from utils import get_assistant_response

CHATBOT_NAME = st.secrets["CHATBOT_NAME"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
ASSISTANT_ID = st.secrets["ASST_ID"]

client = OpenAI(api_key=OPENAI_API_KEY)
assistant = client.beta.assistants.retrieve(ASSISTANT_ID)

st.title(CHATBOT_NAME)

if "thread" not in st.session_state:
    st.session_state["thread"] = client.beta.threads.create()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Write your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = get_assistant_response(prompt, client, assistant, st.session_state.thread)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})