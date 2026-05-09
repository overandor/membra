from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

class InventoryItem(BaseModel):
    id: Optional[str] = None
    name: str
    category: str
    condition: str
    price_per_hour: Optional[float] = None
    price_per_day: Optional[float] = None
    available: bool = True

class CreateInventoryRequest(BaseModel):
    name: str
    category: str
    condition: str
    price_per_hour: Optional[float] = None
    price_per_day: Optional[float] = None

@router.get("/v1/inventory")
async def get_inventory():
    """Get all inventory items for the current user"""
    # Mock data for now
    mock_items = [
        {
            "id": "item_1",
            "name": "Power Drill",
            "category": "tools",
            "condition": "excellent",
            "price_per_hour": 7.0,
            "available": True,
            "earnings_this_month": 42.0
        },
        {
            "id": "item_2",
            "name": "Tripod",
            "category": "electronics",
            "condition": "good",
            "price_per_hour": 5.0,
            "available": True,
            "earnings_this_month": 15.0
        }
    ]
    return {"items": mock_items, "total": len(mock_items)}

@router.post("/v1/inventory")
async def create_inventory(request: CreateInventoryRequest):
    """Create a new inventory item"""
    item_id = f"item_{uuid.uuid4().hex[:8]}"
    new_item = {
        "id": item_id,
        "name": request.name,
        "category": request.category,
        "condition": request.condition,
        "price_per_hour": request.price_per_hour,
        "price_per_day": request.price_per_day,
        "available": True,
        "earnings_this_month": 0.0
    }
    return {"item": new_item, "status": "created"}

@router.get("/v1/inventory/{item_id}")
async def get_inventory_item(item_id: str):
    """Get a specific inventory item"""
    # Mock item
    mock_item = {
        "id": item_id,
        "name": "Power Drill",
        "category": "tools",
        "condition": "excellent",
        "price_per_hour": 7.0,
        "available": True,
        "earnings_this_month": 42.0
    }
    return {"item": mock_item}
