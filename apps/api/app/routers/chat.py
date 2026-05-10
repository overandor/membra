from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, AsyncGenerator
import json
import asyncio

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: list[str]

async def generate_response(message: str) -> AsyncGenerator[str, None]:
    """Generate streaming response with simulated thinking"""
    
    # Map message intent to suggestions
    message_lower = message.lower()
    suggestions = []
    response_text = ""
    
    if "rent" in message_lower or "borrow" in message_lower or "need" in message_lower:
        response_text = f"I understand you're looking to rent or borrow something related to: {message}.\n\nMEMBRA can help you find items nearby in seconds. Here are popular nearby rentals:\n\n• Power Drill - $7/hr (0.2 miles away)\n• USB-C Charger - $2/hr (0.3 miles away)\n• Storage Space - $15/month (0.5 miles away)\n\nWould you like me to show you more options?"
        suggestions = [
            "Show me power tools nearby",
            "What's the cheapest rental?",
            "How do I rent an item?",
            "What categories are available?"
        ]
    elif "earn" in message_lower or "sell" in message_lower or "list" in message_lower:
        response_text = f"Great! You're interested in earning from your items: {message}.\n\nMEMBRA helps you turn unused items into income. Here's what you can do:\n\n1. Scan your room to see what you can rent out\n2. Get instant valuations for your items\n3. List items and start earning in minutes\n4. MEMBRA handles payments and logistics\n\nYour home could earn $50-500/month on average!"
        suggestions = [
            "Scan my room for items",
            "How much can I earn?",
            "What's the commission rate?",
            "Show me top earning items"
        ]
    elif "delivery" in message_lower or "shipping" in message_lower or "relay" in message_lower:
        response_text = f"I found local delivery options for you: {message}.\n\nMEMBRA's Relay network offers:\n\n• Local Delivery: $5.50-$15 depending on distance\n• Same-day pickup available\n• Insured packages\n• 20+ drivers nearby\n\nWould you like to schedule a pickup or see delivery estimates?"
        suggestions = [
            "Schedule a pickup",
            "What's the delivery cost?",
            "How fast can you deliver?",
            "Show delivery coverage map"
        ]
    else:
        response_text = f"I'm MEMBRA, a marketplace you talk to. You asked: \"{message}\"\n\nI can help you:\n\n• Find items to rent nearby\n• Earn money from your unused home items\n• Connect with local services\n• Get instant recommendations\n\nWhat would you like to explore?"
        suggestions = [
            "What items can I rent nearby?",
            "How can I earn from my home?",
            "Show me local services",
            "What's new this week?"
        ]
    
    # Stream the response word by word for a natural effect
    words = response_text.split()
    for i, word in enumerate(words):
        # Yield chunks of 3-4 words at a time
        if i % 3 == 0 and i > 0:
            await asyncio.sleep(0.01)  # Small delay for streaming effect
        yield word + " "
    
    # Yield final newline
    yield "\n"
    
    # Yield suggestions as JSON
    yield json.dumps(suggestions)

@router.post("/v1/chat")
async def chat(request: ChatRequest):
    """Process user chat message and return streaming AI response with suggestions"""
    return StreamingResponse(generate_response(request.message), media_type="text/event-stream")

@router.post("/v1/chat/ask")
async def chat_ask(request: ChatRequest):
    """Non-streaming chat endpoint for backward compatibility"""
    message_lower = request.message.lower()
    suggestions = []
    response = ""
    
    if "rent" in message_lower or "borrow" in message_lower or "need" in message_lower:
        response = f"I understand you're looking to rent or borrow something related to: {request.message}.\n\nMEMBRA can help you find items nearby in seconds. Here are popular nearby rentals:\n\n• Power Drill - $7/hr (0.2 miles away)\n• USB-C Charger - $2/hr (0.3 miles away)\n• Storage Space - $15/month (0.5 miles away)\n\nWould you like me to show you more options?"
        suggestions = [
            "Show me power tools nearby",
            "What's the cheapest rental?",
            "How do I rent an item?",
            "What categories are available?"
        ]
    elif "earn" in message_lower or "sell" in message_lower or "list" in message_lower:
        response = f"Great! You're interested in earning from your items: {request.message}.\n\nMEMBRA helps you turn unused items into income. Here's what you can do:\n\n1. Scan your room to see what you can rent out\n2. Get instant valuations for your items\n3. List items and start earning in minutes\n4. MEMBRA handles payments and logistics\n\nYour home could earn $50-500/month on average!"
        suggestions = [
            "Scan my room for items",
            "How much can I earn?",
            "What's the commission rate?",
            "Show me top earning items"
        ]
    elif "delivery" in message_lower or "shipping" in message_lower or "relay" in message_lower:
        response = f"I found local delivery options for you: {request.message}.\n\nMEMBRA's Relay network offers:\n\n• Local Delivery: $5.50-$15 depending on distance\n• Same-day pickup available\n• Insured packages\n• 20+ drivers nearby\n\nWould you like to schedule a pickup or see delivery estimates?"
        suggestions = [
            "Schedule a pickup",
            "What's the delivery cost?",
            "How fast can you deliver?",
            "Show delivery coverage map"
        ]
    else:
        response = f"I'm MEMBRA, a marketplace you talk to. You asked: \"{request.message}\"\n\nI can help you:\n\n• Find items to rent nearby\n• Earn money from your unused home items\n• Connect with local services\n• Get instant recommendations\n\nWhat would you like to explore?"
        suggestions = [
            "What items can I rent nearby?",
            "How can I earn from my home?",
            "Show me local services",
            "What's new this week?"
        ]
    
    return {
        "response": response,
        "suggestions": suggestions
    }
