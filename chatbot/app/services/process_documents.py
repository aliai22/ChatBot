import fitz  # PyMuPDF for text extraction
import os
import re

# Store processed text in memory (can be replaced with a database)
processed_text_store = {}

def clean_text(text):
    """Cleans extracted text: removes extra spaces, newlines, and special characters."""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\n+', ' ', text)  # Remove excessive new lines
    text = text.strip()
    return text

def chunk_text(text, chunk_size=128):
    """Splits text into manageable chunks."""
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def process_pdfs(file_paths):
    """Extracts and processes text from one or multiple PDF files."""
    if isinstance(file_paths, str):  # If a single file is passed, convert to list
        file_paths = [file_paths]

    results = {}

    for file_path in file_paths:
        extracted_text = ""
        
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    extracted_text += page.get_text("text") + "\n"
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            continue

        cleaned_text = clean_text(extracted_text)
        text_chunks = chunk_text(cleaned_text)

        # Store processed text in memory
        processed_text_store[file_path] = text_chunks
        results[file_path] = text_chunks  # Return results for API response

    return results