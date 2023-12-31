# use st.session_state to store the user's name, age, and height

import streamlit as st
from openai import OpenAI

st.title("ChatGPT-like clone")

# Set OpenAI API key from Streamlit secrets
api = "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"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""


for response in client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    ):
        full_response += (response.choices[0].delta.content or "")
        message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
st.session_state.messages.append({"role": "assistant", "content": full_response})