import streamlit as st
import requests
import pandas as pd
import numpy as np
import time

st.title("Industrial RAG Agent")
st.header("An Agentic RAG system designed to process and query industrial technical documentation.")

st.file_uploader("Load the manual you want to query")

with st.spinner("Wait while the manual is processed...", show_time=True):
    time.sleep(5)
    #here add a dynamic circular loading and then write done when finished
st.success("Manual processed successfully")
st.error("Uploading or processing failed. Retry!")



st.header("What do you want to ask about the manual?")
st.text_input("")
st.button("Send")

st.header("Response:")
st.text_area("")