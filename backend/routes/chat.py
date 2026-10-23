from fastapi import APIRouter, HTTPException, Depends
from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.rag_engine import RAGEngine

router = APIRouter(prefix="/api/chat", tags=["Chat & Voice Assistant"])

rag_engine = RAGEngine()

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Core conversational and voice QA endpoint.
    Retrieves official AIET knowledge base chunks, synthesizes a grounded answer,
    cites source documents, and suggests contextual follow-up questions.
    """
    try:
        response = await rag_engine.answer_question(
            question=request.question,
            history=request.history,
            session_id=request.session_id or "default_session",
            language=request.language or "en"
        )
        return response
    except Exception as e:
        print(f"Error in chat_endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")
