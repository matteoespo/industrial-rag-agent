'''
chat interface
'''

import streamlit as st

def render_chat_window():
    prompt = st.chat_input("Ask something")

    if prompt:
        st.write(prompt)
