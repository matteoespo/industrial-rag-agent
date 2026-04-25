'''
chat interface
'''
import streamlit as st
import requests

def render_chat_window():
    history = st.session_state["messages"]
    with st.container(border=True, height=500):
        for message in history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    prompt = st.chat_input("Ask something")
    if prompt:
        with st.chat_message("user"):
            st.session_state["messages"].append({
                "role": "user",
                "content": prompt
            })
            st.write(prompt)
            
        with st.chat_message("assistant"):
            st.session_state["messages"].append({
                "role": "assistant",
                "content": "Here the LLM answer"
            })
            st.write("Here the LLM answer")
