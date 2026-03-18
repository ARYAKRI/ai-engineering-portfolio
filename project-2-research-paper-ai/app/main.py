from fastapi import FastAPI, UploadFile, File
import shutil
import os

# Updated imports to work from within the app folder
from pdf_loader import load_pdf
from embeddings import create_vector_store
from rag_pipeline import generate_answer
app = FastAPI()

# This will hold our vector database in memory
vectorstore = None

@app.get("/")
def home():
    return {"message": "AI Research Assistant API is Online"}

@app.post("/upload-paper")
async def upload_paper(file: UploadFile = File(...)):
    # Save the uploaded PDF temporarily
    file_location = os.path.join(os.getcwd(), file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Load the PDF
    docs = load_pdf(file_location)

    # 2. Create the Vector Store
    global vectorstore
    vectorstore = create_vector_store(docs)

    # Clean up the temp file
    os.remove(file_location)

    return {"message": f"Paper '{file.filename}' processed and indexed successfully!"}

@app.get("/ask")
def ask_question(question: str):
    if vectorstore is None:
        return {"error": "Please upload a paper first using /upload-paper"}

    # 3. Search for the context
    results = vectorstore.similarity_search(question)
    context = results[0].page_content

    # 4. Generate the AI answer
    answer = generate_answer(context, question)

    return {
        "question": question, 
        "answer": answer,
        "source_chunk": context[:200] + "..." # Show a snippet of where the AI found it
    } 
