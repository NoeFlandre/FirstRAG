# app.py

import streamlit as st
from functions import load_pdf, split_documents, create_embeddings, create_vectorstore, query_relevant_data

# Streamlit UI
st.title("PDF Data Extraction and Analysis")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    st.write("Processing the PDF document...")

    # Process the PDF and extract data
    pages = load_pdf(uploaded_file)
    chunks = split_documents(pages)
    embedding_function = create_embeddings()
    vectorstore = create_vectorstore(chunks, embedding_function)

    st.write("PDF document processed successfully. You can now query the data.")

    # User query input
    question = st.text_input("Enter your question:")
    if question:
        result = query_relevant_data(vectorstore, question)
        st.write("### Extracted Information")
        st.write(result)
