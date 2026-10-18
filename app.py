import streamlit as st
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from functions import load_pdf, split_documents, create_vectorstore, query_relevant_data_openai, query_relevant_data, \
    create_embeddings, create_embeddings_openai

st.set_page_config(page_title="PDF Data Extraction and Analysis", layout="wide")
st.title("📄 PDF Data Extraction and Analysis")

st.sidebar.title("Instructions")
st.sidebar.info(
    "1. Select a preloaded PDF document or upload a new one.\n"
    "2. Choose between Ollama and OpenAI for querying the PDF content.\n"
    "3. If OpenAI is selected, enter your OpenAI API key."
)

api_choice = st.sidebar.radio("Select the API to use for processing:", ("Ollama", "OpenAI"))


st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by Loïc and Noé")

pdf_files = ["NoeFlandre.pdf", "LoicLaine.pdf"]
pdf_folder = "data/"

uploaded_file = st.file_uploader("Upload a new PDF file (optional)", type="pdf")

selected_pdf = st.selectbox("Or select a preloaded PDF file:", pdf_files)

openai_api_key = None
if api_choice == "OpenAI":
    openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    if not openai_api_key:
        st.warning("Please enter your OpenAI API key to proceed.")
        st.stop()

if uploaded_file is not None:
    pdf_path = uploaded_file
    st.write(f"Processing uploaded file: **{uploaded_file.name}**...")
else:
    pdf_path = os.path.join(pdf_folder, selected_pdf)
    st.write(f"Processing preloaded file: **{selected_pdf}**...")

if pdf_path:
    try:
        with st.spinner("Processing the PDF document... ⏳"):
            if isinstance(pdf_path, str):
                with open(pdf_path, "rb") as file:
                    pages = load_pdf(file)
            else:
                pages = load_pdf(pdf_path)

            chunks = split_documents(pages)

            st.success("PDF document loaded and split successfully!")


            @st.cache_resource
            def generate_embeddings_and_store(api_choice):
                if api_choice == "Ollama":
                    embedding_function = create_embeddings()
                else:
                    embedding_function = create_embeddings_openai(openai_api_key)

                vectorstore = create_vectorstore(chunks, embedding_function)
                return vectorstore


            vectorstore = generate_embeddings_and_store(api_choice)

        st.success(f"Document processed successfully with {api_choice}! You can now query the data. ✅")

        st.write("### Query the Document")
        question = st.text_input("Enter your question:")

        if question:
            with st.spinner(f"Fetching relevant information using {api_choice}... 🧠"):
                if api_choice == "Ollama":
                    result = query_relevant_data(vectorstore, question)
                else:
                    result = query_relevant_data_openai(vectorstore, question, openai_api_key)

                if result:
                    st.write("### Extracted Information")
                    st.write(result)
                else:
                    st.warning("No relevant information found.")

    except Exception as e:
        st.error(f"Error while processing the PDF: {str(e)}")
