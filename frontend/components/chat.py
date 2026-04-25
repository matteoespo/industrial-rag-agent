'''
chat interface
'''
import streamlit as st
import requests

@st.fragment
def render_chat_window():
    history = st.session_state["messages"]
    with st.container(border=True, height=500):
        for message in history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        if history and history[-1]["role"] == "user":
            with st.spinner("I'm thinking..."):
                response = requests.post(url="http://api:8000/api/chat", json={"query": history[-1]["content"]})
                #st.error(f"Status: {response.status_code}")
                #st.error(f"Text: {response.text}")
                content = response.json()
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": content["answer"]
                })
            st.rerun(scope="fragment")
    prompt = st.chat_input("Ask something")
    if prompt:
        st.session_state["messages"].append({
            "role": "user",
            "content": prompt
        })
        st.rerun(scope="fragment")
