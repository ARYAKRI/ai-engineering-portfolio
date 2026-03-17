import ssl
# Keeping the SSL fix just in case the model download triggers the same error
ssl._create_default_https_context = ssl._create_unverified_context

from app.pdf_loader import load_pdf
from app.embeddings import create_vector_store
from app.rag_pipeline import generate_answer

print("--- Starting RAG System ---")
print("Loading PDF...")
docs = load_pdf("sample_paper.pdf")

print("Creating vector database (this may take a moment)...")
vectorstore = create_vector_store(docs)

query = input("\nAsk a question about the paper: ")

print("Searching for relevant sections...")
results = vectorstore.similarity_search(query)

# We take the most relevant chunk found
context = results[0].page_content

print("Generating answer...")
answer = generate_answer(context, query)

print("\n" + "="*20)
print(f"QUESTION: {query}")
print(f"ANSWER: {answer}")
print("="*20)