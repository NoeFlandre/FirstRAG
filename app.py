import streamlit as st
import os
import tempfile
from functions import load_pdf, split_documents, create_embeddings, create_vectorstore, query_relevant_data

# Streamlit UI
st.set_page_config(page_title="PDF Data Extraction and Analysis", layout="wide")
st.title("📄 PDF Data Extraction and Analysis")

# Sidebar for Instructions
st.sidebar.title("Instructions")
st.sidebar.info(
    "1. Select a preloaded PDF document or upload a new one.\n"
    "2. The app will process the document and allow you to query its content.\n"
    "3. Enter a question related to the PDF content to extract relevant information."
)
# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by Loïc and Noé")

# Define the available PDF options
pdf_files = ["NoeFlandre.pdf", "LoicLaine.pdf"]
pdf_folder = "data/"

# File uploader
uploaded_file = st.file_uploader("Upload a new PDF file (optional)", type="pdf")

# PDF file selector
selected_pdf = st.selectbox("Or select a preloaded PDF file:", pdf_files)

# Determine which file to process
if uploaded_file is not None:
    # Process the uploaded file directly
    pdf_path = uploaded_file
    st.write(f"Processing uploaded file: **{uploaded_file.name}**...")
else:
    # Process the selected preloaded file
    pdf_path = os.path.join(pdf_folder, selected_pdf)
    st.write(f"Processing preloaded file: **{selected_pdf}**...")

if pdf_path:
    try:
        with st.spinner("Processing the PDF document... ⏳"):
            # Load the pages correctly based on whether it's uploaded or preloaded
            if isinstance(pdf_path, str):  # if it's a string, it's the path to the preloaded file
                # Open the preloaded PDF file to load it
                with open(pdf_path, "rb") as file:
                    pages = load_pdf(file)  # Pass the file-like object to load_pdf
            else:
                pages = load_pdf(pdf_path)  # This handles the uploaded file

            chunks = split_documents(pages)

            st.success("PDF document loaded and split successfully!")

            # Caching embeddings and vectorstore creation for efficiency
            @st.cache_resource
            def generate_embeddings_and_store():
                embedding_function = create_embeddings()
                vectorstore = create_vectorstore(chunks, embedding_function)
                return vectorstore

            vectorstore = generate_embeddings_and_store()

        st.success("Document processed successfully! You can now query the data. ✅")

        # User query input
        st.write("### Query the Document")
        question = st.text_input("Enter your question:")

        if question:
            with st.spinner("Fetching relevant information... 🧠"):
                result = query_relevant_data(vectorstore, question)
                if result:
                    st.write("### Extracted Information")
                    st.write(result)
                else:
                    st.warning("No relevant information found. Please try a different question.")

    except Exception as e:
        st.error(f"Something went wrong while processing the document: {str(e)}")
else:
    st.info("Please upload a PDF file or select a preloaded file to start.")


