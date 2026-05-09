"""
MEMBRA Core Data Models
"""
from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class ItemMode(str, Enum):
    """Item transaction modes"""
    SELL = "sell"
    RENT = "rent"
    SPLIT = "split"
    SHARE = "share"
    STORE = "store"


class DeliveryMode(str, Enum):
    """Delivery fulfillment modes"""
    PICKUP = "pickup"
    MEET_HALFWAY = "meet_halfway"
    HOST_DELIVERY = "host_delivery"
    RUNNER_DELIVERY = "runner_delivery"
    VENDOR_DELIVERY = "vendor_delivery"
    COURIER = "courier"


class RiskLevel(str, Enum):
    """Risk level for items"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    FRAGILE = "fragile"
    HIGH_VALUE = "high_value"


class ItemCategory(str, Enum):
    """Item categories"""
    TOOLS = "tools"
    ELECTRONICS = "electronics"
    CABLES = "cables"
    CHARGERS = "chargers"
    PARTY_SUPPLIES = "party_supplies"
    OFFICE_SUPPLIES = "office_supplies"
    PROPS = "props"
    CAMERA_GEAR = "camera_gear"
    HOUSEHOLD = "household"
    KITCHEN = "kitchen"
    FRIDGE = "fridge"
    INGREDIENTS = "ingredients"
    STORAGE = "storage"
    OTHER = "other"


class Item(BaseModel):
    """Household item that can be monetized"""
    item_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    category: ItemCategory
    condition: str = "good"  # new, good, fair, poor
    quantity: int = 1
    weight_lb: Optional[float] = None
    dimensions: Optional[str] = None  # e.g., "12x8x4"
    value_usd: Optional[float] = None
    fragile: bool = False
    perishable: bool = False
    restricted: bool = False
    opened: bool = False
    expiration_date: Optional[datetime] = None
    image_url: Optional[str] = None
    barcode: Optional[str] = None
    sku: Optional[str] = None


class Space(BaseModel):
    """Rentable space (MEMBRA Spaces / Couchify layer)"""
    space_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    space_type: str  # couch_seat, desk, living_room_corner, photo_corner, shelf, closet, fridge_shelf, storage_corner
    capacity_seats: int = 1
    price_per_minute_usd: float
    minimum_minutes: int = 15
    maximum_minutes: int = 240
    privacy_level: str = "private"  # private, semi_private, shared
    host_presence_mode: str = "flexible"  # flexible, present, absent
    approval_mode: str = "auto"  # auto, manual
    amenities: List[str] = []
    rules: List[str] = []
    image_url: Optional[str] = None
    latitude: float
    longitude: float
    address: str


class Skill(BaseModel):
    """Capability as a service (MEMBRA Skills)"""
    skill_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    category: str  # delivery, setup, cleaning, inventory, organizing, repair, photography, livestream, moving, staging
    hourly_rate_usd: Optional[float] = None
    fixed_price_usd: Optional[float] = None
    estimated_duration_minutes: Optional[int] = None
    tools_provided: List[str] = []
    certifications: List[str] = []
    image_url: Optional[str] = None


class Request(BaseModel):
    """User request (MEMBRA Requests)"""
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    item_name: str
    description: Optional[str] = None
    category: ItemCategory
    quantity: int = 1
    mode: ItemMode
    urgency: str = "normal"  # low, normal, high, urgent
    delivery_mode: DeliveryMode = DeliveryMode.PICKUP
    location_latitude: float
    location_longitude: float
    radius_miles: float = 2.0
    budget_max_usd: Optional[float] = None
    duration_minutes: Optional[int] = None
    special_instructions: Optional[str] = None
    substitutes_allowed: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


class Listing(BaseModel):
    """Public listing of an item/space/skill"""
    listing_id: str = Field(default_factory=lambda: str(uuid4()))
    host_id: str
    item: Optional[Item] = None
    space: Optional[Space] = None
    skill: Optional[Skill] = None
    mode: ItemMode
    price_usd: float
    price_unit: str  # per_item, per_hour, per_minute, flat
    availability_start: datetime
    availability_end: Optional[datetime] = None
    delivery_modes: List[DeliveryMode] = [DeliveryMode.PICKUP]
    risk_level: RiskLevel = RiskLevel.LOW
    proof_required: bool = True
    deposit_required: bool = False
    deposit_usd: Optional[float] = None
    latitude: float
    longitude: float
    address: str
    visibility: str = "public"  # private, public
    status: str = "active"  # active, inactive, pending, rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Transaction(BaseModel):
    """Completed transaction"""
    transaction_id: str = Field(default_factory=lambda: str(uuid4()))
    listing_id: str
    requester_id: str
    host_id: str
    mode: ItemMode
    delivery_mode: DeliveryMode
    total_price_usd: float
    delivery_fee_usd: float = 0.0
    platform_fee_usd: float = 0.0
    host_payout_usd: float
    deposit_usd: Optional[float] = None
    deposit_returned_usd: Optional[float] = None
    proof_required: bool = True
    proof_photo_url: Optional[str] = None
    proof_signature: Optional[str] = None
    status: str = "pending"  # pending, confirmed, in_progress, completed, cancelled, disputed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    confirmed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Credit(BaseModel):
    """MEMBRA Credits (internal rewards)"""
    credit_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    amount: int
    reason: str  # signup, listing, upload_receipt, scan_room, referral, rental, delivery, return, review, fulfill_request
    reference_id: Optional[str] = None  # transaction_id, listing_id, etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


class Assessment(BaseModel):
    """Belongings assessment (MEMBRA Assess)"""
    assessment_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    input_type: str  # room_photo, shelf_photo, fridge_photo, amazon_link, amazon_order, receipt, manual, video
    input_data: Optional[str] = None  # URL, text, etc.
    detected_items: List[Item] = []
    suggested_skus: List[str] = []
    suggested_prices: List[float] = []
    risk_levels: List[RiskLevel] = []
    monthly_earning_estimate_usd: Optional[float] = None
    bundle_suggestions: List[List[str]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AdAgentCampaign(BaseModel):
    """LLM advertising campaign (MEMBRA AdAgent)"""
    campaign_id: str = Field(default_factory=lambda: str(uuid4()))
    listing_id: str
    listing_titles: List[str] = []
    ad_copy: List[str] = []
    bundle_suggestions: List[List[str]] = []
    target_audience: List[str] = []
    suggested_price_adjustments: List[float] = []
    status: str = "active"  # active, paused, completed
    created_at: datetime = Field(default_factory=datetime.utcnow)
