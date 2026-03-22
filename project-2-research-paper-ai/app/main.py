from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# Updated imports to work from within the app folder
from pdf_loader import load_pdf
from embeddings import create_vector_store
from rag_pipeline import generate_answer
app = FastAPI()

# ADD THIS PART:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This tells the browser "It's okay to accept requests from React"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    # 1. Search for the context
    results = vectorstore.similarity_search(question)
    
    # We take the full content of the most relevant chunk
    context = results[0].page_content

    # 2. Generate the AI answer
    answer = generate_answer(context, question)

    # 3. Return full details for the Frontend
    return {
        "question": question, 
        "answer": answer,
        "source": context  # Changed from source_chunk to source for React consistency
    }  
    