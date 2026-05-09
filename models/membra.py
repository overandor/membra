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


class Intent(BaseModel):
    """User intent as inventory (MEMBRA Intent-as-Inventory)"""
    intent_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    intent_type: str  # supply_intent, demand_intent, permission, boundary, preference, recurring_need
    content: str  # "I am willing to rent my vacuum", "I need groceries after 8 PM"
    category: Optional[str] = None
    conditions: List[str] = []  # ["verified_users_only", "pickup_only", "no_entry"]
    availability_windows: List[dict] = []  # [{"start": "18:00", "end": "22:00", "days": ["Mon", "Fri"]}]
    location_latitude: Optional[float] = None
    location_longitude: Optional[float] = None
    radius_miles: Optional[float] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class HeroHouse(BaseModel):
    """Home as business node (MEMBRA House)"""
    house_id: str = Field(default_factory=lambda: str(uuid4()))
    host_id: str
    address: str
    latitude: float
    longitude: float
    house_type: str  # apartment, house, condo, townhouse
    capabilities: List[str] = []  # ["pickup", "storage", "service", "inventory", "fulfillment"]
    storage_capacity_items: int = 0
    storage_volume_cubic_ft: Optional[float] = None
    pickup_window_start: str = "08:00"
    pickup_window_end: str = "22:00"
    pickup_days: List[str] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rules: List[str] = []
    amenities: List[str] = []
    status: str = "active"  # active, inactive, suspended
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AlphaHub(HeroHouse):
    """High-trust, high-volume Hero House (MEMBRA Alpha Hub)"""
    hub_level: int = 1  # 1-5 based on volume and trust
    inventory_for_others: List[str] = []  # listing_ids
    hub_fee_percentage: float = 12.0  # percentage of transactions
    monthly_volume_usd: float = 0.0
    total_earnings_usd: float = 0.0
    supported_heroes: List[str] = []  # hero_ids
    compliance_level: str = "standard"  # standard, enhanced, premium
    insurance_coverage_usd: float = 0.0
    verified_at: Optional[datetime] = None


class SplitOrder(BaseModel):
    """Split bulk purchases into fractional units (MEMBRA SplitOrder)"""
    split_order_id: str = Field(default_factory=lambda: str(uuid4()))
    initiator_id: str
    item_name: str
    item_url: Optional[str] = None
    total_quantity: int
    total_cost_usd: float
    unit_type: str  # pieces, cups, eggs, pods, items
    units_available: int
    units_reserved: int = 0
    price_per_unit_usd: float
    location_latitude: float
    location_longitude: float
    fulfillment_location: str  # "hero_house", "alpha_hub", "meet_halfway"
    fulfillment_house_id: Optional[str] = None
    status: str = "open"  # open, partial, full, cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


class SplitReservation(BaseModel):
    """Individual reservation within a SplitOrder"""
    reservation_id: str = Field(default_factory=lambda: str(uuid4()))
    split_order_id: str
    user_id: str
    quantity: int
    cost_usd: float
    pickup_window_start: str
    pickup_window_end: str
    status: str = "reserved"  # reserved, picked_up, cancelled, refunded
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SplitPulse(BaseModel):
    """Local demand signal for group buying (MEMBRA SplitPulse)"""
    pulse_id: str = Field(default_factory=lambda: str(uuid4()))
    item_name: str
    item_url: Optional[str] = None
    interest_count: int
    anonymous_users: bool = True
    location_latitude: float
    location_longitude: float
    radius_miles: float = 2.0
    urgency: str = "normal"  # low, normal, high
    category: Optional[str] = None
    suggested_split_quantity: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None


class Wallet(BaseModel):
    """MEMBRA Wallet (credits, earnings, deposits, rewards)"""
    wallet_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    balance_credits: int = 0
    balance_usd: float = 0.0
    total_earnings_usd: float = 0.0
    total_spent_usd: float = 0.0
    referral_rewards_credits: int = 0
    cashback_credits: int = 0
    deposit_balance_usd: float = 0.0
    loyalty_level: str = "bronze"  # bronze, silver, gold, platinum
    reputation_score: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WalletTransaction(BaseModel):
    """Individual wallet transaction"""
    transaction_id: str = Field(default_factory=lambda: str(uuid4()))
    wallet_id: str
    transaction_type: str  # credit_earn, credit_spend, deposit, withdrawal, payout, cashback, refund
    amount: float
    currency: str = "USD"  # USD or CREDITS
    reference_id: Optional[str] = None  # listing_id, transaction_id, etc.
    description: str
    status: str = "pending"  # pending, completed, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DemandSignal(BaseModel):
    """Local demand intelligence signal"""
    signal_id: str = Field(default_factory=lambda: str(uuid4()))
    item_name: str
    category: str
    request_count: int
    failed_match_count: int
    average_budget_usd: float
    urgency_distribution: dict  # {"low": 10, "normal": 50, "high": 30, "urgent": 10}
    time_of_day_distribution: dict  # {"morning": 20, "afternoon": 40, "evening": 30, "night": 10}
    location_latitude: float
    location_longitude: float
    radius_miles: float = 2.0
    trend_score: float = 0.0  # -1.0 to 1.0, negative = declining, positive = growing
    suggested_action: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class OpportunityRecommendation(BaseModel):
    """Supply creation recommendation based on demand"""
    recommendation_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    item_name: str
    category: str
    buy_cost_usd: float
    estimated_rent_price_usd: Optional[float] = None
    estimated_sale_price_usd: Optional[float] = None
    monthly_earnings_estimate_usd: float
    demand_score: float  # 0-100
    time_to_sale_days: Optional[int] = None
    risk_level: RiskLevel = RiskLevel.LOW
    fulfillment_option: str  # "self", "alpha_hub", "both"
    alpha_hub_distance_miles: Optional[float] = None
    confidence_score: float = 0.0  # 0-1
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Relay models for MEMBRA Relay logistics layer
class RelayMode(str, Enum):
    """Relay fulfillment modes"""
    PICKUP_ONLY = "pickup_only"
    MEET_HALFWAY = "meet_halfway"
    LOCAL_DELIVERY = "local_delivery"
    RETURN_RUN = "return_run"
    HUB_TRANSFER = "hub_transfer"
    ERRAND_RELAY = "errand_relay"
    BATCH_ROUTE = "batch_route"
    STORAGE_TO_DELIVERY = "storage_to_delivery"
    ON_DEMAND_COURIER = "on_demand_courier"


class NodeType(str, Enum):
    """Network node types"""
    HERO_HOUSE = "hero_house"
    ALPHA_HUB = "alpha_hub"
    STORE = "store"
    COURIER_HUB = "courier_hub"


class RelayRequest(BaseModel):
    """Relay fulfillment request"""
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    item_description: str
    pickup_location_latitude: float
    pickup_location_longitude: float
    pickup_address: str
    delivery_location_latitude: Optional[float] = None
    delivery_location_longitude: Optional[float] = None
    delivery_address: Optional[str] = None
    mode: RelayMode
    risk_level: RiskLevel = RiskLevel.LOW
    heavy: bool = False
    fragile: bool = False
    high_value: bool = False
    special_instructions: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RelayOffer(BaseModel):
    """Relay agent's offer for a request"""
    offer_id: str = Field(default_factory=lambda: str(uuid4()))
    request_id: str
    agent_id: str
    estimated_price_usd: float
    estimated_duration_minutes: Optional[int] = None
    available_at: datetime
    expires_at: Optional[datetime] = None
    vehicle_type: Optional[str] = None
    message: Optional[str] = None


class RelayBatch(BaseModel):
    """Batched Relay route for efficiency"""
    batch_id: str = Field(default_factory=lambda: str(uuid4()))
    requests: List[str]  # request_ids
    agent_id: str
    estimated_price_usd: float
    estimated_duration_minutes: int
    route_sequence: List[str]  # addresses in order


class RelayProof(BaseModel):
    """Proof of pickup or delivery"""
    proof_id: str = Field(default_factory=lambda: str(uuid4()))
    relay_id: str
    proof_type: str  # pickup, delivery
    photo_url: str
    location_latitude: float
    location_longitude: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    signature: Optional[str] = None
    notes: Optional[str] = None


# CameraLink models for cross-platform camera bridge
class CameraLinkMode(str, Enum):
    """CameraLink scan modes"""
    SNAPSHOT = "snapshot"
    LIVE = "live"


class CameraLinkStatus(str, Enum):
    """CameraLink session status"""
    CREATED = "created"
    QR_GENERATED = "qr_generated"
    JOINED = "joined"
    SCANNING = "scanning"
    PROCESSING = "processing"
    READY_FOR_APPROVAL = "ready_for_approval"
    APPROVED = "approved"
    ENDED = "ended"
    EXPIRED = "expired"


class CameraLinkSession(BaseModel):
    """CameraLink scanning session"""
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    desktop_user_id: str
    phone_device_id: Optional[str] = None
    mode: CameraLinkMode = CameraLinkMode.SNAPSHOT
    pairing_method: str = "qr"
    expires_in_minutes: int = 15
    camera_permission: bool = False
    owner_approval_required: bool = True
    status: CameraLinkStatus = CameraLinkStatus.CREATED
    qr_code_token: Optional[str] = None
    qr_code_url: Optional[str] = None
    photos_uploaded: int = 0
    detections: List[dict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    joined_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


class CameraLinkDetection(BaseModel):
    """AI detection from camera scan"""
    detection_id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str
    photo_url: str
    detected_items: List[Item] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    suggested_categories: List[str] = Field(default_factory=list)
    suggested_prices: dict = Field(default_factory=dict)
    risk_levels: List[RiskLevel] = Field(default_factory=list)
    needs_approval: bool = True
    approved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
