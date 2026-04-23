import streamlit as st
import requests
import pandas as pd
import numpy as np

st.title("Industrial RAG Agent")
st.header("test header")


dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
