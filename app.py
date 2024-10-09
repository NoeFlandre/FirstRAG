import streamlit as st
from functions import load_pdf, split_documents, create_embeddings, create_vectorstore, query_relevant_data

# Streamlit UI
st.set_page_config(page_title="PDF Data Extraction and Analysis", layout="wide")
st.title("📄 PDF Data Extraction and Analysis")

# Sidebar for Instructions
st.sidebar.title("Instructions")
st.sidebar.info(
    "1. Upload a PDF document.\n"
    "2. The app will process the document and allow you to query its content.\n"
    "3. Enter a question related to the PDF content to extract relevant information."
)

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    try:
        with st.spinner("Processing the PDF document... ⏳"):
            # Process the PDF and extract data
            pages = load_pdf(uploaded_file)
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
    st.info("Please upload a PDF file to start.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by Loïc and Noé")
