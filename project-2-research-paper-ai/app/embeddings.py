<<<<<<< HEAD
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def create_vector_store(documents):

    # Split documents into chunks
=======
import os
from dotenv import load_dotenv

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def create_vector_store(documents):
    # 1. Split documents into chunks
>>>>>>> b1714a8 (Day 2: Switched to HuggingFace embeddings for local RAG)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
<<<<<<< HEAD

    texts = text_splitter.split_documents(documents)

    # Convert text into embeddings
    embeddings = OpenAIEmbeddings()

    # Create vector database
    vectorstore = FAISS.from_documents(texts, embeddings)

    return vectorstore
=======
    texts = text_splitter.split_documents(documents)

    # 2. Convert text into embeddings using a FREE local model
    # This will download the model (~80MB) the first time you run it
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 3. Create vector database
    vectorstore = FAISS.from_documents(texts, embeddings)

    return vectorstore
>>>>>>> b1714a8 (Day 2: Switched to HuggingFace embeddings for local RAG)
