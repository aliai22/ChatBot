import time
from fastapi import APIRouter, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
import shutil
import os
from typing import List, Union
from app.services.process_documents import process_pdfs, processed_text_store
from app.services.vectorstore import add_to_vector_store

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

knowledge_base_ready = False  # Track knowledge base status

def process_and_store_text(file_paths: Union[str, List[str]]):
    """Runs text extraction and processing in the background."""
    process_pdfs(file_paths)  # Extract text

def create_knowledge_base():
    """Creates a vector store for chatbot after text extraction is complete."""
    global knowledge_base_ready
    time.sleep(2)  # Simulate processing delay

    if processed_text_store:
        for text_chunks in processed_text_store.values():
            add_to_vector_store(text_chunks)  # Store extracted text in FAISS
        knowledge_base_ready = True  # Mark as complete

@router.post("/upload/")
async def upload_pdfs(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    uploaded_files = []
    file_paths = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(file.filename)
        file_paths.append(file_path)

    # Start processing text first
    background_tasks.add_task(process_and_store_text, file_paths if len(file_paths) > 1 else file_paths[0])

    # After text is processed, create knowledge base
    background_tasks.add_task(create_knowledge_base)

    return JSONResponse(content={"uploaded_files": uploaded_files, "message": "Files uploaded successfully! Text processing started."})

@router.get("/processed_text/{filename}")
async def get_processed_text(filename: str):
    """Waits dynamically until processed text is available."""
    file_path = os.path.join(UPLOAD_DIR, filename)

    max_wait_time = 300  # Maximum wait time (5 minutes)
    wait_time = 2  # Start with 2 seconds wait
    total_waited = 0

    while total_waited < max_wait_time:
        if file_path in processed_text_store:
            return {"filename": filename, "message": "Text processing complete!"}
        
        time.sleep(wait_time)  # Wait before checking again
        total_waited += wait_time
        wait_time = min(wait_time * 2, 10)  # Exponential backoff

    return {"error": "Text processing took too long. Please try again later."}

@router.get("/knowledge_base_status/")
async def get_knowledge_base_status():
    """Checks if the knowledge base is ready."""
    if knowledge_base_ready:
        return {"status": "complete", "message": "Knowledge base is ready! Chatbot is now available."}
    else:
        return {"status": "processing", "message": "Building knowledge base... Please wait."}