"""
MEMBRA Marketplace API Endpoints

Core commerce layer: listings, transactions, matching, and fulfillment.
Turns approved inventory into rentable, buyable, splittable, storable,
accessible, movable, or bookable offers.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel, Field
from models.membra import (
    Listing, Transaction, Item, Space, Skill, ItemMode, DeliveryMode, RiskLevel
)
from datetime import datetime
from uuid import uuid4

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])


class CreateListingRequest(BaseModel):
    """Request to create a new listing"""
    host_id: str
    mode: ItemMode
    price_usd: float
    price_unit: str  # per_item, per_hour, per_minute, flat
    latitude: float
    longitude: float
    address: str
    item: Optional[Item] = None
    space: Optional[Space] = None
    skill: Optional[Skill] = None
    delivery_modes: List[DeliveryMode] = [DeliveryMode.PICKUP]
    risk_level: RiskLevel = RiskLevel.LOW
    proof_required: bool = True
    deposit_required: bool = False
    deposit_usd: Optional[float] = None
    visibility: str = "public"


class CreateTransactionRequest(BaseModel):
    """Request to create a transaction (booking/purchase)"""
    listing_id: str
    requester_id: str
    mode: ItemMode
    delivery_mode: DeliveryMode
    quantity: int = 1
    duration_minutes: Optional[int] = None
    special_instructions: Optional[str] = None


@router.post("/listings")
async def create_listing(request: CreateListingRequest) -> dict:
    """
    Create a new marketplace listing.
    
    Converts approved inventory into public offers.
    """
    listing_id = str(uuid4())
    
    # In production, this would:
    # 1. Validate listing data
    # 2. Check host permissions
    # 3. Calculate platform fees
    # 4. Store in database
    # 5. Index for search
    # 6. Notify nearby users if relevant
    
    return {
        "listing_id": listing_id,
        "host_id": request.host_id,
        "mode": request.mode,
        "price_usd": request.price_usd,
        "price_unit": request.price_unit,
        "status": "active",
        "created_at": datetime.utcnow().isoformat(),
    }


@router.get("/listings")
async def search_listings(
    category: Optional[str] = None,
    mode: Optional[ItemMode] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_miles: float = 2.0,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """
    Search marketplace listings.
    
    Users find what they need nearby.
    """
    # In production, this would:
    # 1. Query database with filters
    # 2. Calculate distances
    # 3. Apply ranking algorithm
    # 4. Return paginated results
    
    # Mock results for MVP
    mock_listings = [
        {
            "listing_id": str(uuid4()),
            "title": "Power Drill",
            "mode": "rent",
            "price_usd": 7.0,
            "price_unit": "per_hour",
            "distance_miles": 0.2,
            "rating": 4.9,
            "reviews": 23,
            "category": "tools",
        },
        {
            "listing_id": str(uuid4()),
            "title": "Couch Seat + Wi-Fi",
            "mode": "rent",
            "price_usd": 8.0,
            "price_unit": "per_hour",
            "distance_miles": 0.1,
            "rating": 4.8,
            "reviews": 12,
            "category": "household",
        },
        {
            "listing_id": str(uuid4()),
            "title": "Closet Shelf Space",
            "mode": "store",
            "price_usd": 15.0,
            "price_unit": "per_month",
            "distance_miles": 0.3,
            "rating": 4.7,
            "reviews": 8,
            "category": "storage",
        },
    ]
    
    return {
        "listings": mock_listings,
        "total": len(mock_listings),
        "limit": limit,
        "offset": offset,
        "filters": {
            "category": category,
            "mode": mode,
            "latitude": latitude,
            "longitude": longitude,
            "radius_miles": radius_miles,
        },
    }


@router.get("/listings/{listing_id}")
async def get_listing(listing_id: str) -> dict:
    """Get details of a specific listing"""
    return {
        "listing_id": listing_id,
        "title": "Power Drill",
        "description": "Cordless power drill, good condition",
        "mode": "rent",
        "price_usd": 7.0,
        "price_unit": "per_hour",
        "host_id": str(uuid4()),
        "host_rating": 4.9,
        "host_reviews": 47,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "address": "123 Main St, Apt 4B",
        "delivery_modes": ["pickup", "meet_halfway", "local_delivery"],
        "risk_level": "low",
        "proof_required": True,
        "deposit_required": False,
        "availability": {
            "start": "08:00",
            "end": "22:00",
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "rules": ["Must return in same condition", "No commercial use"],
        "created_at": datetime.utcnow().isoformat(),
    }


@router.put("/listings/{listing_id}")
async def update_listing(
    listing_id: str,
    price_usd: Optional[float] = None,
    visibility: Optional[str] = None,
    status: Optional[str] = None,
) -> dict:
    """Update a listing"""
    return {
        "listing_id": listing_id,
        "updated_fields": [],
        "status": "updated",
    }


@router.delete("/listings/{listing_id}")
async def delete_listing(listing_id: str) -> dict:
    """Delete a listing"""
    return {
        "listing_id": listing_id,
        "status": "deleted",
    }


@router.get("/listings/{listing_id}/availability")
async def get_listing_availability(listing_id: str) -> dict:
    """Get availability calendar for a listing"""
    return {
        "listing_id": listing_id,
        "availability": [
            {"date": "2026-05-09", "slots": ["08:00-10:00", "14:00-16:00"]},
            {"date": "2026-05-10", "slots": ["09:00-11:00", "15:00-17:00"]},
        ],
    }


@router.post("/transactions")
async def create_transaction(request: CreateTransactionRequest) -> dict:
    """
    Create a transaction (booking/purchase).
    
    User pays → payment splits → booking confirmed → fulfillment begins.
    """
    transaction_id = str(uuid4())
    
    # In production, this would:
    # 1. Validate listing availability
    # 2. Calculate total price with fees
    # 3. Calculate payment split
    # 4. Create transaction record
    # 5. Initiate payment
    # 6. Notify host
    # 7. Schedule fulfillment
    
    # Mock payment split calculation
    total_price = 40.0
    payment_split = {
        "user_pays": total_price,
        "tool_hero": 6.0,
        "skill_hero": 22.0,
        "alpha_hub": 3.0,
        "delivery_hero": 4.0,
        "user_credit": 1.0,
        "membra_fee": 4.0,
    }
    
    return {
        "transaction_id": transaction_id,
        "listing_id": request.listing_id,
        "requester_id": request.requester_id,
        "mode": request.mode,
        "delivery_mode": request.delivery_mode,
        "total_price_usd": total_price,
        "payment_split": payment_split,
        "status": "pending_payment",
        "created_at": datetime.utcnow().isoformat(),
    }


@router.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: str) -> dict:
    """Get details of a specific transaction"""
    return {
        "transaction_id": transaction_id,
        "status": "confirmed",
        "total_price_usd": 40.0,
        "payment_split": {
            "tool_hero": 6.0,
            "skill_hero": 22.0,
            "alpha_hub": 3.0,
            "delivery_hero": 4.0,
            "user_credit": 1.0,
            "membra_fee": 4.0,
        },
        "created_at": datetime.utcnow().isoformat(),
        "confirmed_at": datetime.utcnow().isoformat(),
    }


@router.put("/transactions/{transaction_id}/status")
async def update_transaction_status(
    transaction_id: str,
    status: str,
    proof_photo_url: Optional[str] = None,
) -> dict:
    """
    Update transaction status.
    
    Used for: confirmed, in_progress, completed, cancelled, disputed
    """
    return {
        "transaction_id": transaction_id,
        "status": status,
        "updated_at": datetime.utcnow().isoformat(),
    }


@router.get("/transactions")
async def get_user_transactions(
    user_id: str,
    role: str = "all",  # requester, host, all
    status: Optional[str] = None,
    limit: int = 20,
) -> dict:
    """Get transactions for a user"""
    return {
        "user_id": user_id,
        "role": role,
        "transactions": [],
        "total": 0,
        "limit": limit,
    }


@router.post("/transactions/{transaction_id}/proof")
async def submit_transaction_proof(
    transaction_id: str,
    proof_type: str,  # pickup, return, condition
    proof_photo_url: str,
    notes: Optional[str] = None,
) -> dict:
    """
    Submit proof for transaction (pickup, return, condition).
    
    Proof is required for settlement and dispute resolution.
    """
    return {
        "transaction_id": transaction_id,
        "proof_type": proof_type,
        "proof_photo_url": proof_photo_url,
        "status": "submitted",
        "submitted_at": datetime.utcnow().isoformat(),
    }


@router.get("/categories")
async def get_marketplace_categories() -> dict:
    """Get all marketplace categories"""
    return {
        "categories": [
            {"id": "rent", "name": "Rent", "description": "Tools, vacuums, ring lights, appliances"},
            {"id": "buy", "name": "Buy", "description": "Sealed supplies, chargers, unused goods"},
            {"id": "split", "name": "Split", "description": "Bulk quantities, pantry items"},
            {"id": "store", "name": "Store", "description": "Closet shelves, package holding"},
            {"id": "access", "name": "Access", "description": "Wi-Fi, charging, desk use"},
            {"id": "move", "name": "Move", "description": "Delivery, hauling, pickup"},
            {"id": "book", "name": "Book", "description": "Cleaning, setup, repair"},
            {"id": "supply", "name": "Supply", "description": "Cables, batteries, essentials"},
        ]
    }


@router.get("/featured")
async def get_featured_listings(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_miles: float = 2.0,
) -> dict:
    """Get featured listings nearby"""
    return {
        "featured": [
            {
                "listing_id": str(uuid4()),
                "title": "Power Drill",
                "price": "$7/hr",
                "distance": "0.2 mi",
                "rating": 4.9,
                "reviews": 23,
                "category": "Rent",
            },
            {
                "listing_id": str(uuid4()),
                "title": "Couch Seat + Wi-Fi",
                "price": "$8/hr",
                "distance": "0.1 mi",
                "rating": 4.8,
                "reviews": 12,
                "category": "Access",
            },
        ],
    }


@router.get("/requests/nearby")
async def get_nearby_requests(
    latitude: float,
    longitude: float,
    radius_miles: float = 2.0,
) -> dict:
    """Get live requests from nearby users"""
    return {
        "requests": [
            {
                "request_id": str(uuid4()),
                "content": "Need a drill for 20 minutes",
                "category": "tools",
                "distance": "0.1 mi",
                "created_at": "2 minutes ago",
            },
            {
                "request_id": str(uuid4()),
                "content": "Looking for package holding until 8 PM",
                "category": "storage",
                "distance": "0.3 mi",
                "created_at": "5 minutes ago",
            },
        ],
    }
