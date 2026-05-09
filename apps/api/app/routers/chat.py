from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: list[str]

@router.post("/v1/chat")
async def chat(request: ChatRequest):
    """Process user chat message and return AI response"""
    suggestions = [
        "What items can I rent from my apartment?",
        "How much can I earn from my unused tools?",
        "Who needs help nearby right now?",
        "What should I list for sale?"
    ]
    
    return ChatResponse(
        response=f"I understand you're asking about: {request.message}. MEMBRA can help you turn your household items into income. Would you like to scan your home to see what you can offer?",
        suggestions=suggestions
    )
