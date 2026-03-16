from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def create_vector_store(documents):

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    texts = text_splitter.split_documents(documents)

    # Convert text into embeddings
    embeddings = OpenAIEmbeddings()

    # Create vector database
    vectorstore = FAISS.from_documents(texts, embeddings)

    return vectorstore
