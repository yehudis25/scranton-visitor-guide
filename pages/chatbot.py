# program to run openai on my app

import streamlit as st
from openai import OpenAI


st.title("Robotic Help🤖")
client = OpenAI(api_key=st.secrets[""])

# get open AI
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# save all history of messages asked
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# check for prompt
if prompt:= st.chat_input("Whats a good activity for a rainy day?🌧️"):
    with st.chat_message("user"):
        st.markdown(prompt)
    # give an openAI answer
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})