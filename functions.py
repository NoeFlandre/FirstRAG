# Import Langchain modules
from langchain.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings
import openai

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# Other modules and packages
import tempfile
import uuid


def load_pdf(uploaded_file):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        # Write the uploaded file's bytes to the temporary file
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Load the PDF using PDFPlumberLoader with the file path
    loader = PDFPlumberLoader(temp_file_path)
    return loader.load()


def split_documents(pages):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50, separators=["\n\n", "\n", " "])
    return text_splitter.split_documents(pages)


def create_embeddings():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings


def create_vectorstore(chunks, embedding_function, vectorstore_path="vectorstore"):
    ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in chunks]
    unique_ids = set()
    unique_chunks = []
    for chunk, id in zip(chunks, ids):
        if id not in unique_ids:
            unique_ids.add(id)
            unique_chunks.append(chunk)
    vectorstore = Chroma.from_documents(unique_chunks, ids=list(unique_ids), embedding=embedding_function,
                                        persist_directory=vectorstore_path)
    return vectorstore


def query_relevant_data(vectorstore, question):
    retriever = vectorstore.as_retriever(search_type="similarity")
    prompt_template = ChatPromptTemplate.from_template("""
        You are an assistant for question-answering tasks.
        Use the following pieces of retrieved context to
        answer the question. If you don't know the answer,
        just say that you don't know, don't try to make up
        an answer. 
        Rephrase the context especially the accents which can be parsed poorly.

        Here is the context: {context}

        Here is the question: {question}
    """)

    # Retrieve relevant chunks and format output
    relevant_chunks = retriever.invoke(question)
    context_text = "\n\n---\n\n".join([chunk.page_content for chunk in relevant_chunks])

    # Use format_messages() to get a list of messages
    messages = prompt_template.format_messages(context=context_text, question=question)

    # Pass the list of messages to the language model
    llm = ChatOllama(model="llama3.2")  # Initialize the model
    result = llm(messages)

    return result.content


# OpenAI Embeddings and Querying
def create_embeddings_openai(api_key):
    openai.api_key = api_key
    # Return an instance of OpenAIEmbeddings
    return OpenAIEmbeddings()


def query_relevant_data_openai(vectorstore, question, api_key):
    openai.api_key = api_key
    retriever = vectorstore.as_retriever(search_type="similarity")
    relevant_chunks = retriever.invoke(question)
    context_text = "\n\n---\n\n".join([chunk.page_content for chunk in relevant_chunks])

    # Use OpenAI for querying
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """You are an assistant for question-answering tasks.
        Use the following pieces of retrieved context to
        answer the question. If you don't know the answer,
        just say that you don't know, don't try to make up
        an answer. 
        Rephrase the context especially the accents which can be parsed poorly."""},
            {"role": "user",
             "content": f"Here is the context: {context_text}. Answer the following question: {question}"}
        ]
    )

    return response['choices'][0]['message']['content']
