from openai import OpenAI
import streamlit as st
from utils import get_assistant_response, upload_files

CHATBOT_NAME = st.secrets["CHATBOT_NAME"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
ASSISTANT_ID = st.secrets["ASST_ID"]
ACCEPTED_FILE_TYPES = ["pdf", "txt", "png", "jpeg", "jpg"]

client = OpenAI(api_key=OPENAI_API_KEY)
assistant = client.beta.assistants.retrieve(ASSISTANT_ID)

st.title(CHATBOT_NAME)

if "thread" not in st.session_state:
    st.session_state["thread"] = client.beta.threads.create()

if "messages" not in st.session_state:
    st.session_state.messages = []

# This will load initial messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Upload files form (this moves as chat messages adds up... You should fix it)
with st.form("Files form", clear_on_submit=True):
    uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True, type=ACCEPTED_FILE_TYPES)
    submitted = st.form_submit_button("Attach")

    if submitted:
        st.write("Files attached to next message! Type something!")

prompt = st.chat_input("Write your message here...")

if prompt:
    OpenAI_files = []
    if uploaded_files:
        OpenAI_files = upload_files(client, uploaded_files)

    st.session_state.messages.append({"role": "user", "content": prompt, "OpenAI_files": OpenAI_files})
    with st.chat_message("user"):
        st.markdown(prompt)
        st.write(f"Attached files: {', '.join([OpenAI_file.filename for OpenAI_file in OpenAI_files])}")

    with st.chat_message("assistant"):
        file_ids = [OpenAI_file.id for OpenAI_file in OpenAI_files]
        response = get_assistant_response(prompt, client, assistant, st.session_state.thread, file_ids)
        st.markdown(response)

    # The assistant never outputs files
    st.session_state.messages.append({"role": "assistant", "content": response, "file_ids": []})

    # Reset uploaded_files to None after processing the user's message
    st.session_state.uploaded_files = None
