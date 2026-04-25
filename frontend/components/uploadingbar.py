'''
file upload
'''
import streamlit as st
import requests
import time

@st.fragment
def render_uploadingbar():

    is_ready = st.session_state.get("pdf_uploaded", False)

    # info
    if st.session_state["pdf_uploaded"] == True:
        st.metric(label="Status", value="Ready")
    else:
        st.metric(label="Status", value="Waiting")
    st.metric("History", f"{len(st.session_state.get('messages', []))} msgs")
    st.metric("Memory", "1 doc" if is_ready else "0 docs")


    if st.session_state.get("pdf_uploaded", False):
        st.success("PDF uploaded in the DB. Agent is ready!")
        if st.button("Load another file"):
            st.session_state["pdf_uploaded"] = False
            st.rerun(scope="fragment")
        return
    
    uploaded_file = st.file_uploader("Load the PDF file", type=[".pdf"])

    if uploaded_file is not None:
        with st.spinner("Wait until the file is processed...", show_time=True):
            file_packet = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
            }

            try:
                response = requests.post("http://api:8000/api/upload", files=file_packet)

                if response.status_code == 200:
                    st.session_state["pdf_uploaded"]= True
                    st.rerun(scope="fragment")
                else:
                    st.error(f"Uploading failed with error: {response.status_code}. Retry!")
            except Exception as e:
                st.error(f"Connection error: {e}")

