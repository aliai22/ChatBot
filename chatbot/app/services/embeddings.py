from sentence_transformers import SentenceTransformer

# Load an optimized sentence embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Fast & accurate

def get_text_embedding(text):
    """Converts text into a numerical vector embedding."""
    return embedding_model.encode(text, convert_to_numpy=True)