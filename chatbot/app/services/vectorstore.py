import faiss
import numpy as np
from app.services.embeddings import get_text_embedding

# Initialize FAISS index
embedding_size = 384  # Based on MiniLM model
index = faiss.IndexFlatL2(embedding_size)  # L2 distance for similarity search
document_store = {}  # Maps vector IDs to text chunks

def add_to_vector_store(text_chunks):
    """Stores processed text chunks in FAISS vector storage."""
    global document_store

    embeddings = [get_text_embedding(chunk) for chunk in text_chunks]
    embeddings = np.array(embeddings, dtype=np.float32)

    index.add(embeddings)  # Add embeddings to FAISS index

    # Store chunks in memory
    for i, chunk in enumerate(text_chunks):
        document_store[len(document_store)] = chunk

def search_similar_texts(query, top_n=3):
    """Finds the most relevant text chunks for a given query."""
    query_embedding = get_text_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_embedding, top_n)

    # Retrieve relevant text chunks
    results = [document_store[idx] for idx in indices[0] if idx in document_store]
    return results