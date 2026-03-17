import ssl
import os
from dotenv import load_dotenv

ssl._create_default_https_context = ssl._create_unverified_context

from app.pdf_loader import load_pdf
from app.embeddings import create_vector_store

print("Loading PDF...")
docs = load_pdf("sample_paper.pdf")

print("Creating vector store...")
vectorstore = create_vector_store(docs)

print("Vector store created successfully!")

query = "What is this paper about?"

results = vectorstore.similarity_search(query)

print("Top Result:")
print(results[0].page_content[:500])

