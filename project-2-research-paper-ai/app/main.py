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
        return {"error": "Please upload a paper first!"}
    
    # To this (The "Diversity" Filter):
    results = vectorstore.similarity_search(question, k=10) # Get more chunks
    unique_chunks = []
    seen_text = set()

    for doc in results:
        content = doc.page_content[:200] # Check the first 200 chars for duplicates
        if content not in seen_text:
            unique_chunks.append(doc)
            seen_text.add(content)
        if len(unique_chunks) == 3: # Stop once we have 3 DIFFERENT ones
            break

    context = "\n\n".join([d.page_content for d in unique_chunks])

    # 1. Get more results to account for footers
        
    # 2. Use a 'set' to remove duplicate text chunks
    unique_contents = list(dict.fromkeys([doc.page_content for doc in results]))
    
    # 3. Take the first 3 truly unique chunks
    final_context = "\n\n".join(unique_contents[:3])

    answer = generate_answer(final_context, question)

    return {
        "question": question, 
        "answer": answer,
        "sources": [text[:150] + "..." for text in unique_contents[:3]]
    }