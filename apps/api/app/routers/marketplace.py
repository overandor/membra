from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

class Listing(BaseModel):
    id: Optional[str] = None
    title: str
    category: str
    mode: str  # rent, buy, split, store, access, move, book, supply
    price: str
    risk_level: str
    location: str
    hero_id: str
    available: bool = True

class CreateListingRequest(BaseModel):
    title: str
    category: str
    mode: str
    price: str
    risk_level: str
    location: str
    hero_id: str

@router.get("/v1/marketplace")
async def get_marketplace():
    """Get all marketplace listings"""
    # Mock listings
    mock_listings = [
        {
            "id": "listing_1",
            "title": "Couch Seat + Wi-Fi",
            "category": "space",
            "mode": "rent",
            "price": "$8/hour",
            "risk_level": "low",
            "location": "Brooklyn, NY",
            "hero_id": "hero_123",
            "available": True,
            "distance": "0.2 miles",
            "rating": 4.8
        },
        {
            "id": "listing_2",
            "title": "Power Drill",
            "category": "tools",
            "mode": "rent",
            "price": "$7/hour",
            "risk_level": "low",
            "location": "Brooklyn, NY",
            "hero_id": "hero_456",
            "available": True,
            "distance": "0.5 miles",
            "rating": 4.9
        },
        {
            "id": "listing_3",
            "title": "Package Holding",
            "category": "service",
            "mode": "store",
            "price": "$3/day",
            "risk_level": "low",
            "location": "Brooklyn, NY",
            "hero_id": "hero_789",
            "available": True,
            "distance": "0.1 miles",
            "rating": 4.7
        }
    ]
    return {"listings": mock_listings, "total": len(mock_listings)}

@router.post("/v1/marketplace")
async def create_listing(request: CreateListingRequest):
    """Create a new marketplace listing"""
    listing_id = f"listing_{uuid.uuid4().hex[:8]}"
    new_listing = {
        "id": listing_id,
        "title": request.title,
        "category": request.category,
        "mode": request.mode,
        "price": request.price,
        "risk_level": request.risk_level,
        "location": request.location,
        "hero_id": request.hero_id,
        "available": True,
        "distance": "0.0 miles",
        "rating": 0.0
    }
    return {"listing": new_listing, "status": "created"}

@router.get("/v1/marketplace/{listing_id}")
async def get_listing(listing_id: str):
    """Get a specific listing"""
    # Mock listing
    mock_listing = {
        "id": listing_id,
        "title": "Couch Seat + Wi-Fi",
        "category": "space",
        "mode": "rent",
        "price": "$8/hour",
        "risk_level": "low",
        "location": "Brooklyn, NY",
        "hero_id": "hero_123",
        "available": True,
        "distance": "0.2 miles",
        "rating": 4.8,
        "description": "Comfortable couch seat with high-speed Wi-Fi. Perfect for remote work or study sessions."
    }
    return {"listing": mock_listing}
