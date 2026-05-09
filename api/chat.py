"""
MEMBRA Chat/Ask API Endpoints

Core chat interface where users ask for what they need or want to earn.
Routes natural language requests to appropriate MEMBRA modules.
"""
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
import os
from openai import OpenAI

router = APIRouter(prefix="/chat", tags=["Chat"])

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))


class ChatIntent(str, Enum):
    """Detected intent from user message"""
    NEED_ITEM = "need_item"
    NEED_SERVICE = "need_service"
    NEED_STORAGE = "need_storage"
    NEED_DELIVERY = "need_delivery"
    EARN_FROM_HOME = "earn_from_home"
    SCAN_ROOM = "scan_room"
    IMPORT_AMAZON = "import_amazon"
    STOCK_RECOMMENDATION = "stock_recommendation"
    SPLIT_ORDER = "split_order"
    ALPHA_HUB_INFO = "alpha_hub_info"
    WALLET_INFO = "wallet_info"
    TRUST_INFO = "trust_info"
    GENERAL = "general"


class ChatRequest(BaseModel):
    """User chat message"""
    user_id: str
    message: str
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    """AI response to user message"""
    response: str
    intent: ChatIntent
    action_suggested: Optional[str] = None
    module: Optional[str] = None
    parameters: Optional[dict] = None
    follow_up_questions: Optional[List[str]] = None


@router.post("/ask")
async def ask_membra(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint - Ask MEMBRA anything nearby.
    
    User asks: "What do I need nearby?" or "What can I earn from my apartment?"
    MEMBRA routes to appropriate module and returns structured response.
    """
    # In production, this would:
    # 1. Send message to LLM
    # 2. Detect intent and extract parameters
    # 3. Route to appropriate module
    # 4. Generate response with action suggestions
    
    message_lower = request.message.lower()
    
    # Simple intent detection (replace with LLM in production)
    if "need" in message_lower or "looking for" in message_lower:
        if "drill" in message_lower or "tool" in message_lower:
            return ChatResponse(
                response="I found 3 power drills nearby. The closest is 0.2 miles away at $7/hour. Would you like to see all options?",
                intent=ChatIntent.NEED_ITEM,
                action_suggested="show_listings",
                module="marketplace",
                parameters={"category": "tools", "item": "drill"},
                follow_up_questions=["What's your budget?", "When do you need it by?"]
            )
        elif "storage" in message_lower or "store" in message_lower:
            return ChatResponse(
                response="I found 5 storage options nearby including closet shelves ($15/month) and package holding ($3/day). Alpha Hub 0.4 miles away has space available.",
                intent=ChatIntent.NEED_STORAGE,
                action_suggested="show_listings",
                module="marketplace",
                parameters={"category": "storage"},
            )
        elif "deliver" in message_lower or "pickup" in message_lower:
            return ChatResponse(
                response="I found 8 delivery agents nearby. Local delivery starts at $5.50 for pickup-only or $8.00 for door-to-door.",
                intent=ChatIntent.NEED_DELIVERY,
                action_suggested="show_agents",
                module="relay",
            )
        else:
            return ChatResponse(
                response="I can help you find what you need nearby. What are you looking for? (tools, storage, delivery, services)",
                intent=ChatIntent.NEED_ITEM,
                action_suggested="clarify",
                follow_up_questions=["What item do you need?", "What's your budget?", "When do you need it?"]
            )
    
    elif "earn" in message_lower or "make money" in message_lower or "monetize" in message_lower:
        if "room" in message_lower or "scan" in message_lower:
            return ChatResponse(
                response="I can scan your room to detect monetizable assets. Upload a photo of your room and I'll identify items you can rent, sell, or split.",
                intent=ChatIntent.SCAN_ROOM,
                action_suggested="upload_photo",
                module="inventory",
            )
        elif "amazon" in message_lower:
            return ChatResponse(
                response="I can import your Amazon order history to find items you can rent, sell, or split. Connect your Amazon account to get started.",
                intent=ChatIntent.IMPORT_AMAZON,
                action_suggested="connect_amazon",
                module="inventory",
            )
        else:
            return ChatResponse(
                response="Based on your location, the best earning opportunities nearby are: USB-C chargers, laundry pods, package holding, and delivery help after 6 PM. Estimated monthly earnings: $80-210.",
                intent=ChatIntent.EARN_FROM_HOME,
                action_suggested="show_opportunities",
                module="opportunity",
            )
    
    elif "stock" in message_lower or "sell" in message_lower or "offer" in message_lower:
        return ChatResponse(
            response="Based on local demand, I recommend stocking: USB-C cables ($2-4 each), laundry pods ($5-8/pack), batteries ($3-5/pack), and trash bags ($4-6/pack). Estimated profit margin: 40-60%.",
            intent=ChatIntent.STOCK_RECOMMENDATION,
            action_suggested="show_recommendations",
            module="demand",
        )
    
    elif "split" in message_lower:
        return ChatResponse(
            response="MEMBRA SplitOrder lets you split bulk purchases with neighbors. Upload a bulk item link or tell me what you want to split, and I'll find nearby users who want parts of it.",
            intent=ChatIntent.SPLIT_ORDER,
            action_suggested="create_split_order",
            module="split_order",
        )
    
    elif "alpha hub" in message_lower:
        return ChatResponse(
            response="Alpha Hubs are high-trust Hero Houses that store inventory, fulfill orders, and earn hub fees. You're 65% of the way to Alpha Hub eligibility. Complete 5 more bookings and reach $1,000 in earnings to qualify.",
            intent=ChatIntent.ALPHA_HUB_INFO,
            action_suggested="show_hub_requirements",
            module="hero",
        )
    
    elif "wallet" in message_lower or "balance" in message_lower:
        return ChatResponse(
            response="Your wallet balance is $247.50 USD and 150 MEMBRA credits. You've earned $847 this month from 128 bookings. Your loyalty level is Silver.",
            intent=ChatIntent.WALLET_INFO,
            action_suggested="show_wallet",
            module="wallet",
        )
    
    else:
        return ChatResponse(
            response="I'm MEMBRA, a marketplace you talk to. You can ask me to find what you need nearby, discover what you can earn from your home, split bulk purchases, or get local recommendations. What would you like to do?",
            intent=ChatIntent.GENERAL,
            follow_up_questions=[
                "What do you need nearby?",
                "What can your home earn?",
                "Should I split a bulk purchase?",
                "What should I stock in my area?"
            ]
        )


@router.post("/intent")
async def detect_intent(request: ChatRequest) -> dict:
    """
    Detect intent from user message without generating full response.
    Used for routing to specific modules.
    """
    message_lower = request.message.lower()
    
    if "need" in message_lower:
        return {"intent": "need", "module": "marketplace"}
    elif "earn" in message_lower or "make money" in message_lower:
        return {"intent": "earn", "module": "opportunity"}
    elif "scan" in message_lower:
        return {"intent": "scan", "module": "inventory"}
    elif "split" in message_lower:
        return {"intent": "split", "module": "split_order"}
    elif "stock" in message_lower:
        return {"intent": "stock", "module": "demand"}
    else:
        return {"intent": "general", "module": "chat"}


@router.get("/suggestions")
async def get_suggestions(user_id: str, location_latitude: float, location_longitude: float) -> dict:
    """
    Get suggested questions/prompts based on user location and context.
    """
    return {
        "suggestions": [
            "What do I need nearby?",
            "What can my apartment earn?",
            "Should I stock USB-C chargers?",
            "Can I split this bulk order?",
            "How do I become an Alpha Hub?",
            "What's my wallet balance?",
        ]
    }


@router.post("/follow-up")
async def get_follow_up(request: ChatRequest, intent: str) -> dict:
    """
    Get follow-up questions based on detected intent.
    """
    follow_ups = {
        "need_item": ["What's your budget?", "When do you need it?", "Do you need delivery?"],
        "need_service": ["What type of service?", "How long will it take?", "Any special requirements?"],
        "earn_from_home": ["What rooms do you have?", "What items do you own?", "How much time can you invest?"],
        "stock_recommendation": ["What's your budget?", "How much storage space?", "What categories interest you?"],
    }
    
    return {
        "follow_up_questions": follow_ups.get(intent, ["How can I help you further?"])
    }
