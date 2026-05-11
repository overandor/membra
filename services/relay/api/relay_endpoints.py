"""
MEMBRA Relay API Endpoints
"""
from fastapi import APIRouter
from typing import Optional
from models.relay import (
    RelayRequest, RelayOffer, RelayBatch, RelayProof,
    RelayMode, RiskLevel, NodeType
)

router = APIRouter(prefix="/relay", tags=["relay"])


@router.post("/request")
async def create_relay_request(request: RelayRequest):
    """
    Create a new Relay fulfillment request.
    
    User needs item → MEMBRA finds local inventory → MEMBRA checks pickup/delivery options
    """
    return {"request_id": request.request_id, "status": "created"}


@router.get("/request/{request_id}")
async def get_relay_request(request_id: str):
    """Get details of a specific Relay request"""
    return {"request_id": request_id, "status": "pending"}


@router.post("/offer")
async def create_relay_offer(offer: RelayOffer):
    """
    Relay agent accepts a Relay request.
    """
    return {"offer_id": offer.offer_id, "status": "created"}


@router.get("/offers/{request_id}")
async def get_relay_offers(request_id: str):
    """Get all offers for a specific request"""
    return {"request_id": request_id, "offers": []}


@router.post("/accept-offer/{offer_id}")
async def accept_relay_offer(offer_id: str):
    """User accepts a Relay agent's offer"""
    return {"offer_id": offer_id, "status": "accepted"}


@router.get("/active/{agent_id}")
async def get_active_relays(agent_id: str):
    """Get all active Relay routes for an agent"""
    return {"agent_id": agent_id, "relays": []}


@router.post("/pickup/{relay_id}")
async def record_pickup(relay_id: str, proof: RelayProof):
    """Record item pickup with proof."""
    return {"relay_id": relay_id, "status": "picked_up"}


@router.post("/deliver/{relay_id}")
async def record_delivery(relay_id: str, proof: RelayProof):
    """Record item delivery with proof."""
    return {"relay_id": relay_id, "status": "delivered"}


@router.get("/quote")
async def get_relay_quote(
    mode: RelayMode,
    distance_miles: float,
    risk_level: RiskLevel = RiskLevel.LOW,
    heavy: bool = False,
    fragile: bool = False,
    high_value: bool = False,
):
    """Get pricing quote for a Relay route."""
    base_pricing = {
        RelayMode.PICKUP_ONLY: 0,
        RelayMode.MEET_HALFWAY: 3.5,
        RelayMode.LOCAL_DELIVERY: 5.5,
        RelayMode.RETURN_RUN: 8,
        RelayMode.HUB_TRANSFER: 6,
        RelayMode.ERRAND_RELAY: 12,
        RelayMode.BATCH_ROUTE: 10,
        RelayMode.STORAGE_TO_DELIVERY: 8,
        RelayMode.ON_DEMAND_COURIER: 15,
    }
    base = base_pricing.get(mode, 10)
    if distance_miles < 0.5:
        distance_multiplier = 1.0
    elif distance_miles < 2:
        distance_multiplier = 1.5
    elif distance_miles < 5:
        distance_multiplier = 2.5
    else:
        distance_multiplier = 4.0
    risk_surcharge = 0
    if risk_level == RiskLevel.MEDIUM:
        risk_surcharge = 2
    elif risk_level == RiskLevel.HIGH:
        risk_surcharge = 5
    elif risk_level == RiskLevel.FRAGILE:
        risk_surcharge = 3
    elif risk_level == RiskLevel.HIGH_VALUE:
        risk_surcharge = 5
    surcharges = 0
    if heavy:
        surcharges += 5
    if fragile:
        surcharges += 3
    if high_value:
        surcharges += 5
    total = (base * distance_multiplier) + risk_surcharge + surcharges
    agent_payout = total * 0.67
    platform_fee = total * 0.17
    insurance = total * 0.04
    hub_fee = total * 0.12
    return {
        "total_price": round(total, 2),
        "agent_payout": round(agent_payout, 2),
        "platform_fee": round(platform_fee, 2),
        "insurance_reserve": round(insurance, 2),
        "hub_fee": round(hub_fee, 2),
    }


@router.get("/nearby-agents")
async def find_nearby_agents(
    latitude: float,
    longitude: float,
    radius_miles: float = 2.0,
    vehicle_type: Optional[str] = None,
):
    """Find available Relay agents near a location."""
    return {"latitude": latitude, "longitude": longitude, "radius_miles": radius_miles, "agents": []}


@router.post("/batch")
async def create_batch_route(batch: RelayBatch):
    """Create a batched Relay route for efficiency."""
    return {"batch_id": batch.batch_id, "status": "created"}


@router.get("/earnings/{agent_id}")
async def get_agent_earnings(agent_id: str, period: str = "week"):
    """Get earnings breakdown for a Relay agent"""
    return {"agent_id": agent_id, "period": period, "total_earnings": 0, "completed_relays": 0}


@router.get("/status/{relay_id}")
async def get_relay_status(relay_id: str):
    """Get real-time status of a Relay route"""
    return {"relay_id": relay_id, "status": "pending"}


@router.post("/cancel/{relay_id}")
async def cancel_relay(relay_id: str, reason: Optional[str] = None):
    """Cancel a Relay request or active route"""
    return {"relay_id": relay_id, "status": "cancelled"}
