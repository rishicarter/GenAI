import streamlit as st

def pdf_uploader():
    st.sidebar.title("Upload PDF")
    return st.sidebar.file_uploader("Choose PDF file(s)", type=["pdf"], accept_multiple_files=True, help="Upload one or more PDF files for processing.")

