"""
MEMBRA ScanOS API
AI-powered photo scanning for zero-form listing creation
"""
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid

router = APIRouter(prefix="/scan", tags=["Scan"])


class ScanType(str, Enum):
    """Types of scans supported"""
    CLOSET = "closet"
    SHELF = "shelf"
    ROOM = "room"
    GARAGE = "garage"
    DESK = "desk"
    TOOLBOX = "toolbox"
    STORAGE_BINS = "storage_bins"
    AMAZON_PILE = "amazon_pile"
    RECEIPT = "receipt"
    BARCODE = "barcode"


class ApprovalStatus(str, Enum):
    """Approval status for AI-generated listings"""
    READY_TO_APPROVE = "ready_to_approve"
    NEEDS_CONFIRMATION = "needs_confirmation"
    COMPLIANCE_REVIEW = "compliance_review"
    BLOCKED = "blocked"


class FoodSafetyStatus(str, Enum):
    """Food safety classification for food items"""
    SEALED_PACKAGED_ONLY = "sealed_packaged_only"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"
    NOT_FOOD = "not_food"


class GeneratedListing(BaseModel):
    """AI-generated listing from photo scan"""
    listing_id: str = Field(default_factory=lambda: f"draft_{uuid.uuid4().hex[:8]}")
    owner_id: str
    source: str  # closet_photo, fridge_photo, shelf_photo, etc.
    detected_item: str
    title: str
    description: str
    category: str
    modes: List[str] = Field(default_factory=lambda: ["rent"])
    suggested_price: dict = Field(default_factory=dict)
    quantity: int = 1
    condition_estimate: str = "good"
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)
    risk_level: str = "low"
    fulfillment_options: List[str] = Field(default_factory=lambda: ["pickup"])
    owner_approval_required: bool = True
    status: ApprovalStatus = ApprovalStatus.READY_TO_APPROVE
    food_safety_status: Optional[FoodSafetyStatus] = None
    requires_expiration_confirmation: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ScanRequest(BaseModel):
    """Request to initiate a scan"""
    user_id: str
    scan_type: ScanType
    location_latitude: float
    location_longitude: float
    radius_miles: float = 2.0


class ScanResponse(BaseModel):
    """Response from scan operation"""
    scan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    scan_type: str
    status: str = "processing"
    detected_items_count: int = 0
    generated_listings_count: int = 0
    ready_to_approve: int = 0
    needs_confirmation: int = 0
    compliance_review: int = 0
    blocked: int = 0
    estimated_monthly_earnings_min: float = 0.0
    estimated_monthly_earnings_max: float = 0.0
    message: str = "Scanning in progress..."
    generated_listings: List[GeneratedListing] = Field(default_factory=list)


@router.post("/photo")
async def scan_photo(
    user_id: str,
    scan_type: str,
    location_latitude: float,
    location_longitude: float,
    photo: UploadFile = File(...)
):
    """
    Upload photo for AI-powered inventory scanning
    
    User takes a photo of their closet, shelf, room, or garage.
    MEMBRA's vision model detects items and creates draft listings.
    Human only approves, edits, or rejects - no form filling.
    """
    # Mock AI processing - in production, this would call vision models
    mock_detected_items = get_mock_detected_items(scan_type)
    
    generated_listings = []
    ready_count = 0
    needs_confirm_count = 0
    compliance_count = 0
    blocked_count = 0
    
    for item in mock_detected_items:
        listing = create_ai_listing(user_id, scan_type, item)
        generated_listings.append(listing)
        
        if listing.status == ApprovalStatus.READY_TO_APPROVE:
            ready_count += 1
        elif listing.status == ApprovalStatus.NEEDS_CONFIRMATION:
            needs_confirm_count += 1
        elif listing.status == ApprovalStatus.COMPLIANCE_REVIEW:
            compliance_count += 1
        elif listing.status == ApprovalStatus.BLOCKED:
            blocked_count += 1
    
    # Calculate estimated earnings
    earnings_min = sum(listing.get("suggested_price", {}).get("rent_per_hour", 0) * 40 for listing in generated_listings if "rent_per_hour" in listing.get("suggested_price", {}))
    earnings_max = earnings_min * 3  # Conservative multiplier
    
    return ScanResponse(
        user_id=user_id,
        scan_type=scan_type,
        status="completed",
        detected_items_count=len(mock_detected_items),
        generated_listings_count=len(generated_listings),
        ready_to_approve=ready_count,
        needs_confirmation=needs_confirm_count,
        compliance_review=compliance_count,
        blocked=blocked_count,
        estimated_monthly_earnings_min=earnings_min,
        estimated_monthly_earnings_max=earnings_max,
        message=f"MEMBRA found local earning opportunities. I created {len(generated_listings)} draft listings. Nothing is public yet.",
        generated_listings=generated_listings
    )


@router.post("/confirm")
async def confirm_ambiguous_item(
    listing_id: str,
    confirmation: str
):
    """
    Handle user confirmation for ambiguous items
    
    AI asks minimal questions when needed:
    - "Is it working?" → Works / Not sure / Parts only / Do not list
    - "Are they unused?" → Unused / Used / Do not list
    """
    return {
        "listing_id": listing_id,
        "status": "updated",
        "message": f"Listing updated based on confirmation: {confirmation}"
    }


@router.post("/approve")
async def approve_listings(
    user_id: str,
    listing_ids: List[str]
):
    """
    Approve draft listings for publication
    
    Owner approval required before anything goes public.
    This creates the permissioned local asset graph.
    """
    return {
        "user_id": user_id,
        "approved_count": len(listing_ids),
        "status": "published",
        "message": f"{len(listing_ids)} listings are now visible in the local marketplace"
    }


@router.post("/reject")
async def reject_listings(
    user_id: str,
    listing_ids: List[str],
    reason: Optional[str] = None
):
    """
    Reject draft listings
    """
    return {
        "user_id": user_id,
        "rejected_count": len(listing_ids),
        "status": "rejected",
        "message": f"{len(listing_ids)} listings removed from draft"
    }


@router.get("/scan-types")
async def get_scan_types():
    """Get available scan types"""
    return {
        "scan_types": [
            {"type": "closet", "name": "Scan Closet", "icon": "👕", "priority": 1},
            {"type": "shelf", "name": "Scan Shelf", "icon": "📚", "priority": 2},
            {"type": "room", "name": "Scan Room", "icon": "🏠", "priority": 3},
            {"type": "garage", "name": "Scan Garage", "icon": "🚗", "priority": 4},
            {"type": "desk", "name": "Scan Desk", "icon": "💻", "priority": 5},
            {"type": "toolbox", "name": "Scan Toolbox", "icon": "🔧", "priority": 6},
            {"type": "storage_bins", "name": "Scan Storage Bins", "icon": "📦", "priority": 7},
            {"type": "amazon_pile", "name": "Import Amazon", "icon": "📦", "priority": 8},
            {"type": "receipt", "name": "Upload Receipt", "icon": "🧾", "priority": 9},
            {"type": "barcode", "name": "Scan Barcode", "icon": "📱", "priority": 10}
        ]
    }


# Mock data functions (replace with real AI/vision models in production)
def get_mock_detected_items(scan_type: str) -> List[dict]:
    """Mock detected items based on scan type - MVP-safe categories only"""
    if scan_type == "closet":
        return [
            {"name": "Winter coat", "category": "Clothing", "condition": "good", "mvp_safe": False},
            {"name": "Backpack", "category": "Bags", "condition": "good", "mvp_safe": True},
            {"name": "Foldable chair", "category": "Furniture", "condition": "good", "mvp_safe": True},
            {"name": "Extension cord", "category": "Electronics", "condition": "good", "mvp_safe": True},
            {"name": "Vacuum attachment", "category": "Home", "condition": "good", "mvp_safe": True},
            {"name": "Storage bins", "category": "Storage", "condition": "good", "mvp_safe": True},
            {"name": "Camera tripod", "category": "Camera", "condition": "good", "mvp_safe": True},
            {"name": "Ring light", "category": "Lighting", "condition": "good", "mvp_safe": True},
            {"name": "Extra hangers", "category": "Storage", "condition": "good", "mvp_safe": True}
        ]
    elif scan_type == "shelf":
        return [
            {"name": "Books", "category": "Books", "condition": "good", "mvp_safe": True},
            {"name": "Board games", "category": "Games", "condition": "good", "mvp_safe": True},
            {"name": "Decorative items", "category": "Decor", "condition": "good", "mvp_safe": True},
            {"name": "Small speakers", "category": "Electronics", "condition": "good", "mvp_safe": True}
        ]
    elif scan_type == "garage":
        return [
            {"name": "Power drill", "category": "Tools", "condition": "good", "mvp_safe": True},
            {"name": "Ladder", "category": "Tools", "condition": "good", "mvp_safe": True},
            {"name": "Bike pump", "category": "Sports", "condition": "good", "mvp_safe": True},
            {"name": "Extension ladder", "category": "Tools", "condition": "good", "mvp_safe": True}
        ]
    elif scan_type == "desk":
        return [
            {"name": "Phone charger", "category": "Electronics", "condition": "good", "mvp_safe": True},
            {"name": "Laptop charger", "category": "Electronics", "condition": "good", "mvp_safe": True},
            {"name": "USB cables", "category": "Electronics", "condition": "good", "mvp_safe": True},
            {"name": "Desk lamp", "category": "Lighting", "condition": "good", "mvp_safe": True}
        ]
    elif scan_type == "toolbox":
        return [
            {"name": "Screwdriver set", "category": "Tools", "condition": "good", "mvp_safe": True},
            {"name": "Wrench set", "category": "Tools", "condition": "good", "mvp_safe": True},
            {"name": "Hammer", "category": "Tools", "condition": "good", "mvp_safe": True},
            {"name": "Tape measure", "category": "Tools", "condition": "good", "mvp_safe": True}
        ]
    else:
        return [
            {"name": "Generic item", "category": "Other", "condition": "unknown", "mvp_safe": False}
        ]


def create_ai_listing(user_id: str, scan_type: str, item: dict) -> GeneratedListing:
    """Create AI-generated listing from detected item"""
    name = item["name"]
    category = item["category"]
    
    # Generate appropriate title and description
    title, description, modes, price = generate_listing_content(name, category)
    
    # Determine risk level
    risk_level = determine_risk_level(category)
    
    # Determine approval status
    status = determine_approval_status(category, risk_level)
    
    return GeneratedListing(
        owner_id=user_id,
        source=f"{scan_type}_photo",
        detected_item=name,
        title=title,
        description=description,
        category=category,
        modes=modes,
        suggested_price=price,
        condition_estimate=item.get("condition", "good"),
        confidence=0.85,
        risk_level=risk_level,
        fulfillment_options=["pickup", "meet_halfway", "relay_delivery"],
        owner_approval_required=True,
        status=status
    )


def generate_listing_content(name: str, category: str) -> tuple:
    """Generate title, description, modes, and price based on item"""
    # Mock content generation - in production, use LLM
    if "ring light" in name.lower():
        return (
            "Ring Light for Creator Setup",
            "Borrow this ring light for video calls, streaming, photos, or product shots.",
            ["rent", "on_site_access"],
            {"rent_per_hour": 8, "deposit": 15}
        )
    elif "storage bin" in name.lower():
        return (
            "Storage Bin for Moving or Organization",
            "Use this storage bin for moving, closet organization, or temporary storage.",
            ["rent", "sell"],
            {"rent_per_week": 3, "sale_price": 8}
        )
    elif "drill" in name.lower():
        return (
            "Power Drill for DIY Projects",
            "Borrow this power drill for home repairs, DIY projects, or assembly tasks.",
            ["rent"],
            {"rent_per_hour": 10, "deposit": 25}
        )
    else:
        return (
            f"{name}",
            f"A {name.lower()} available for local use.",
            ["rent"],
            {"rent_per_hour": 5, "deposit": 10}
        )


def determine_risk_level(category: str) -> str:
    """Determine risk level based on category - MVP compliance gates"""
    # High-risk categories (blocked or require special compliance)
    high_risk = [
        "food", "food_prep", "chemicals", "flammables", "weapons", "alcohol", 
        "nicotine", "medicine", "childcare", "elder_care", "medical", 
        "licensed_trades", "transport_people", "overnight_stays", 
        "unsupervised_access", "high_value"
    ]
    
    # MVP-safe categories (low risk)
    mvp_safe = [
        "chargers", "party_supplies", "tools", "vacuums", "tripods", 
        "ring_lights", "extension_cords", "storage_bins", "package_holding", 
        "desk_access", "couch_access", "local_delivery", "return_runs", 
        "basic_setup", "books", "games", "decor", "electronics", "lighting",
        "camera", "furniture", "bags", "storage", "sports"
    ]
    
    category_lower = category.lower().replace(" ", "_")
    
    if any(risk in category_lower for risk in high_risk):
        return "high"
    elif any(safe in category_lower for safe in mvp_safe):
        return "low"
    else:
        return "medium"


def determine_approval_status(category: str, risk_level: str) -> ApprovalStatus:
    """Determine approval status based on category and risk"""
    if risk_level == "high":
        return ApprovalStatus.COMPLIANCE_REVIEW
    if category.lower() in ["food", "medical"]:
        return ApprovalStatus.NEEDS_CONFIRMATION
    return ApprovalStatus.READY_TO_APPROVE
