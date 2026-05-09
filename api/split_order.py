"""
MEMBRA SplitOrder API Endpoints

Split bulk purchases into fractional units.
Neighbors split costs and share bulk items.
Two flows: post-purchase splitting and pre-purchase co-ordering.
"""
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel, Field
from models.membra import SplitOrder, SplitReservation
from datetime import datetime
from uuid import uuid4

router = APIRouter(prefix="/split-order", tags=["SplitOrder"])


class CreateSplitOrderRequest(BaseModel):
    """Request to create a new SplitOrder"""
    initiator_id: str
    item_name: str
    item_url: Optional[str] = None
    total_quantity: int
    total_cost_usd: float
    unit_type: str  # pieces, cups, eggs, pods, items
    units_available: int
    location_latitude: float
    location_longitude: float
    fulfillment_location: str  # "hero_house", "alpha_hub", "meet_halfway"
    fulfillment_house_id: Optional[str] = None
    expires_hours: Optional[int] = 24


class ReserveUnitsRequest(BaseModel):
    """Request to reserve units from a SplitOrder"""
    split_order_id: str
    user_id: str
    quantity: int
    pickup_window_start: str
    pickup_window_end: str


@router.post("/create")
async def create_split_order(request: CreateSplitOrderRequest) -> dict:
    """
    Create a new SplitOrder.
    
    Flow: User has bulk item → Creates SplitOrder → Neighbors reserve units → Item divided → Pickup
    """
    split_order_id = str(uuid4())
    price_per_unit = request.total_cost_usd / request.total_quantity
    
    # In production, this would:
    # 1. Validate quantity and cost
    # 2. Calculate price per unit
    # 3. Check fulfillment location availability
    # 4. Store in database
    # 5. Notify nearby users with SplitPulse
    # 6. Start expiry timer
    
    return {
        "split_order_id": split_order_id,
        "initiator_id": request.initiator_id,
        "item_name": request.item_name,
        "total_quantity": request.total_quantity,
        "units_available": request.units_available,
        "units_reserved": 0,
        "price_per_unit_usd": round(price_per_unit, 2),
        "fulfillment_location": request.fulfillment_location,
        "status": "open",
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": datetime.utcnow().isoformat(),
    }


@router.get("/orders")
async def list_split_orders(
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius_miles: float = 2.0,
    status: Optional[str] = None,
    limit: int = 20,
) -> dict:
    """List available SplitOrders nearby"""
    # In production, this would query database with geospatial search
    
    return {
        "orders": [
            {
                "split_order_id": str(uuid4()),
                "item_name": "Party Cups (200-pack)",
                "total_quantity": 200,
                "units_available": 150,
                "units_reserved": 50,
                "price_per_unit_usd": 0.05,
                "distance_miles": 0.3,
                "status": "open",
                "expires_in": "18 hours",
            },
            {
                "split_order_id": str(uuid4()),
                "item_name": "Laundry Pods (48-pack)",
                "total_quantity": 48,
                "units_available": 30,
                "units_reserved": 18,
                "price_per_unit_usd": 0.15,
                "distance_miles": 0.5,
                "status": "open",
                "expires_in": "6 hours",
            },
        ],
        "total": 2,
        "filters": {
            "latitude": latitude,
            "longitude": longitude,
            "radius_miles": radius_miles,
            "status": status,
        },
    }


@router.get("/orders/{split_order_id}")
async def get_split_order(split_order_id: str) -> dict:
    """Get details of a specific SplitOrder"""
    return {
        "split_order_id": split_order_id,
        "initiator_id": str(uuid4()),
        "item_name": "Party Cups (200-pack)",
        "item_url": "https://amazon.com/example",
        "total_quantity": 200,
        "total_cost_usd": 10.00,
        "unit_type": "pieces",
        "units_available": 150,
        "units_reserved": 50,
        "price_per_unit_usd": 0.05,
        "location_latitude": 40.7128,
        "location_longitude": -74.0060,
        "fulfillment_location": "alpha_hub",
        "fulfillment_house_id": str(uuid4()),
        "status": "open",
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": datetime.utcnow().isoformat(),
        "reservations": [
            {
                "reservation_id": str(uuid4()),
                "user_id": str(uuid4()),
                "quantity": 20,
                "cost_usd": 1.00,
                "status": "reserved",
            },
        ],
    }


@router.post("/reserve")
async def reserve_units(request: ReserveUnitsRequest) -> dict:
    """
    Reserve units from a SplitOrder.
    
    User claims quantity → Payment authorized → Reservation confirmed → Pickup scheduled
    """
    reservation_id = str(uuid4())
    
    # In production, this would:
    # 1. Check availability
    # 2. Calculate cost
    # 3. Authorize payment
    # 4. Create reservation
    # 5. Update SplitOrder status
    # 6. Notify initiator
    
    return {
        "reservation_id": reservation_id,
        "split_order_id": request.split_order_id,
        "user_id": request.user_id,
        "quantity": request.quantity,
        "cost_usd": request.quantity * 0.05,  # Mock calculation
        "pickup_window_start": request.pickup_window_start,
        "pickup_window_end": request.pickup_window_end,
        "status": "reserved",
        "created_at": datetime.utcnow().isoformat(),
    }


@router.get("/orders/{split_order_id}/reservations")
async def get_split_order_reservations(split_order_id: str) -> dict:
    """Get all reservations for a SplitOrder"""
    return {
        "split_order_id": split_order_id,
        "reservations": [],
        "total_reserved": 0,
        "total_available": 0,
    }


@router.put("/reservations/{reservation_id}")
async def update_reservation(
    reservation_id: str,
    quantity: Optional[int] = None,
    pickup_window_start: Optional[str] = None,
    pickup_window_end: Optional[str] = None,
    status: Optional[str] = None,
) -> dict:
    """Update a reservation"""
    return {
        "reservation_id": reservation_id,
        "updated_fields": [],
        "status": "updated",
    }


@router.delete("/reservations/{reservation_id}")
async def cancel_reservation(reservation_id: str, reason: Optional[str] = None) -> dict:
    """Cancel a reservation and refund payment"""
    return {
        "reservation_id": reservation_id,
        "status": "cancelled",
        "refund_status": "processed",
        "cancelled_at": datetime.utcnow().isoformat(),
    }


@router.post("/orders/{split_order_id}/complete")
async def complete_split_order(split_order_id: str) -> dict:
    """
    Complete a SplitOrder when all units are reserved or expiry reached.
    
    Triggers: Item division → Pickup scheduling → Notifications
    """
    return {
        "split_order_id": split_order_id,
        "status": "completed",
        "total_reservations": 0,
        "fulfillment_scheduled": True,
        "completed_at": datetime.utcnow().isoformat(),
    }


@router.get("/user/{user_id}/orders")
async def get_user_split_orders(
    user_id: str,
    role: str = "all",  # initiator, reserver, all
    status: Optional[str] = None,
) -> dict:
    """Get SplitOrders for a user (as initiator or reserver)"""
    return {
        "user_id": user_id,
        "role": role,
        "orders": [],
        "total": 0,
    }


@router.get("/user/{user_id}/reservations")
async def get_user_reservations(
    user_id: str,
    status: Optional[str] = None,
) -> dict:
    """Get all reservations for a user"""
    return {
        "user_id": user_id,
        "reservations": [],
        "total": 0,
        "status_filter": status,
    }


@router.post("/calculate")
async def calculate_split(
    item_name: str,
    total_quantity: int,
    total_cost_usd: float,
    desired_quantity: int,
) -> dict:
    """
    Calculate split cost and savings.
    
    Shows users how much they save by splitting vs buying individually.
    """
    price_per_unit = total_cost_usd / total_quantity
    split_cost = price_per_unit * desired_quantity
    individual_cost = total_cost_usd  # Assume individual purchase would be full price
    
    return {
        "item_name": item_name,
        "total_quantity": total_quantity,
        "total_cost_usd": total_cost_usd,
        "desired_quantity": desired_quantity,
        "price_per_unit_usd": round(price_per_unit, 2),
        "split_cost_usd": round(split_cost, 2),
        "individual_cost_usd": individual_cost,
        "savings_usd": round(individual_cost - split_cost, 2),
        "savings_percentage": round(((individual_cost - split_cost) / individual_cost) * 100, 1),
    }


@router.get("/categories")
async def get_split_categories() -> dict:
    """Get categories suitable for splitting"""
    return {
        "categories": [
            {"id": "party_supplies", "name": "Party Supplies", "examples": ["cups", "plates", "napkins"]},
            {"id": "pantry", "name": "Pantry Items", "examples": ["detergent pods", "trash bags", "paper towels"]},
            {"id": "bulk_food", "name": "Bulk Food", "examples": ["rice", "pasta", "oats"]},
            {"id": "household", "name": "Household", "examples": ["batteries", "light bulbs", "cleaning supplies"]},
        ],
        "safety_note": "Only sealed, non-perishable items should be split. Food splitting requires compliance controls.",
    }


@router.post("/amazon-import")
async def import_from_amazon(
    user_id: str,
    amazon_order_id: str,
) -> dict:
    """
    Import Amazon order to create SplitOrder.
    
    For post-purchase splitting: User already bought bulk → MEMBRA helps split locally.
    """
    # In production, this would:
    # 1. Connect to Amazon API
    # 2. Fetch order details
    # 3. Identify splittable items
    # 4. Suggest split quantities
    # 5. Create SplitOrder draft
    
    return {
        "import_id": str(uuid4()),
        "user_id": user_id,
        "amazon_order_id": amazon_order_id,
        "splittable_items": [
            {
                "item_name": "Party Cups (200-pack)",
                "quantity": 200,
                "cost_usd": 10.00,
                "suggested_split_quantity": 20,
                "estimated_savings_per_split": 0.50,
            },
        ],
        "status": "imported",
    }
