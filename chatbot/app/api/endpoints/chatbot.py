from fastapi import APIRouter
from app.services.vectorstore import search_similar_texts
from app.services.llm import generate_response

router = APIRouter()

@router.get("/chatbot/")
async def chatbot(query: str):
    """Handles user queries & generates responses using AI."""
    
    retrieved_chunks = search_similar_texts(query)  # Retrieve text from FAISS
    
    if not retrieved_chunks:
        return {"query": query, "answer": "Sorry, I don't have that detail."}

    context = " ".join(retrieved_chunks)  # Merge retrieved text
    answer = generate_response(query, context)

    return {"query": query, "answer": answer}