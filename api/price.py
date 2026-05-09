"""
MEMBRA PriceOS API
Local pricing suggestion engine for marketplace listings
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
import uuid

router = APIRouter(prefix="/price", tags=["Price"])


class PricingMode(str, Enum):
    """Pricing modes"""
    RENT = "rent"
    SELL = "sell"
    SPLIT = "split"
    STORAGE = "storage"
    ON_SITE_USE = "on_site_use"


class PricingRequest(BaseModel):
    """Request for pricing suggestion"""
    item_name: str
    category: str
    condition: str = "good"
    mode: PricingMode
    location_latitude: float
    location_longitude: float
    quantity: int = 1
    brand: Optional[str] = None
    original_price: Optional[float] = None
    age_months: Optional[int] = None


class PricingSuggestion(BaseModel):
    """Pricing suggestion for an item"""
    item_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_name: str
    category: str
    suggested_price: Dict[str, float] = Field(default_factory=dict)
    price_range: Dict[str, float] = Field(default_factory=dict)
    confidence: float = Field(ge=0.0, le=1.0, default=0.8)
    reasoning: str
    local_demand: str = "medium"
    competitor_prices: List[Dict[str, float]] = Field(default_factory=list)
    depreciation_factor: float = 1.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BulkPricingRequest(BaseModel):
    """Request for bulk pricing suggestions"""
    items: List[PricingRequest]
    location_latitude: float
    location_longitude: float


@router.post("/suggest")
async def suggest_price(request: PricingRequest):
    """
    Get pricing suggestion for a single item
    
    PriceOS analyzes local market data, condition, demand, and competitor prices
    to suggest optimal pricing for rent, sale, or split.
    """
    # Mock pricing logic - in production, this would use real market data
    suggestion = generate_pricing_suggestion(request)
    return suggestion


@router.post("/suggest/bulk")
async def suggest_bulk_prices(request: BulkPricingRequest):
    """
    Get pricing suggestions for multiple items
    
    Efficiently price entire inventory batches.
    """
    suggestions = []
    for item in request.items:
        suggestion = generate_pricing_suggestion(item)
        suggestions.append(suggestion)
    
    return {
        "total_items": len(suggestions),
        "total_value_estimate": sum(
            (next(iter(s.suggested_price.values()), 0) for s in suggestions)
        ),
        "suggestions": suggestions
    }


@router.get("/market-data")
async def get_market_data(
    category: str,
    latitude: float,
    longitude: float,
    radius_miles: float = 10.0
):
    """
    Get market data for a category in a location
    
    Returns competitor prices, demand levels, and market trends.
    """
    # Mock market data
    return {
        "category": category,
        "location": {"latitude": latitude, "longitude": longitude},
        "radius_miles": radius_miles,
        "demand_level": "medium",
        "average_rent_price": 15.0,
        "average_sale_price": 45.0,
        "price_volatility": "low",
        "seasonal_trend": "neutral",
        "competitor_count": 12,
        "recent_transactions": 45
    }


@router.post("/optimize")
async def optimize_pricing(
    item_id: str,
    current_price: float,
    days_listed: int,
    views: int
):
    """
    Optimize pricing based on performance
    
    Suggests price adjustments if an item isn't getting traction.
    """
    # Mock optimization logic
    if days_listed > 30 and views < 50:
        suggested_reduction = current_price * 0.15
        return {
            "item_id": item_id,
            "current_price": current_price,
            "suggested_price": current_price - suggested_reduction,
            "reduction_amount": suggested_reduction,
            "reason": "Low engagement after 30 days",
            "confidence": 0.75
        }
    
    return {
        "item_id": item_id,
        "current_price": current_price,
        "suggested_price": current_price,
        "reason": "Current price is optimal",
        "confidence": 0.85
    }


@router.get("/categories")
async def get_pricing_categories():
    """Get all categories with pricing data"""
    return {
        "categories": [
            {"id": "electronics", "name": "Electronics", "avg_rent": 12.0, "avg_sale": 45.0},
            {"id": "furniture", "name": "Furniture", "avg_rent": 8.0, "avg_sale": 35.0},
            {"id": "tools", "name": "Tools", "avg_rent": 10.0, "avg_sale": 30.0},
            {"id": "camera", "name": "Camera Equipment", "avg_rent": 25.0, "avg_sale": 120.0},
            {"id": "lighting", "name": "Lighting", "avg_rent": 8.0, "avg_sale": 25.0},
            {"id": "storage", "name": "Storage", "avg_rent": 3.0, "avg_sale": 8.0},
            {"id": "sports", "name": "Sports Equipment", "avg_rent": 15.0, "avg_sale": 50.0},
            {"id": "books", "name": "Books & Games", "avg_rent": 2.0, "avg_sale": 10.0}
        ]
    }


# Mock pricing data
CATEGORY_PRICING = {
    "electronics": {"rent_hour": 8, "rent_day": 25, "sale": 45, "storage_week": 5},
    "furniture": {"rent_hour": 5, "rent_day": 15, "sale": 35, "storage_week": 8},
    "tools": {"rent_hour": 10, "rent_day": 30, "sale": 30, "storage_week": 4},
    "camera": {"rent_hour": 25, "rent_day": 75, "sale": 120, "storage_week": 10},
    "lighting": {"rent_hour": 8, "rent_day": 20, "sale": 25, "storage_week": 3},
    "storage": {"rent_hour": 2, "rent_day": 5, "sale": 8, "storage_week": 3},
    "sports": {"rent_hour": 15, "rent_day": 40, "sale": 50, "storage_week": 6},
    "creator_equipment": {"rent_hour": 15, "rent_day": 45, "sale": 80, "storage_week": 8},
    "bags": {"rent_hour": 3, "rent_day": 10, "sale": 25, "storage_week": 4}
}

CONDITION_MULTIPLIERS = {
    "excellent": 1.2,
    "good": 1.0,
    "fair": 0.7,
    "poor": 0.4
}

DEPRECIATION_BY_AGE = {
    0: 1.0,      # New
    6: 0.9,      # 6 months
    12: 0.8,     # 1 year
    24: 0.6,     # 2 years
    36: 0.5,     # 3 years
    48: 0.4,     # 4+ years
    60: 0.3      # 5+ years
}


def generate_pricing_suggestion(request: PricingRequest) -> PricingSuggestion:
    """Generate pricing suggestion for an item"""
    category_key = request.category.lower().replace(" ", "_")
    base_prices = CATEGORY_PRICING.get(category_key, CATEGORY_PRICING["electronics"])
    
    # Apply condition multiplier
    condition_mult = CONDITION_MULTIPLIERS.get(request.condition.lower(), 1.0)
    
    # Apply depreciation if age is known
    age_months = request.age_months or 0
    if age_months >= 60:
        depreciation = DEPRECIATION_BY_AGE[60]
    else:
        depreciation = DEPRECIATION_BY_AGE.get(
            (age_months // 6) * 6,
            DEPRECIATION_BY_AGE[0]
        )
    
    # Calculate suggested prices
    suggested_price = {}
    if request.mode == PricingMode.RENT:
        suggested_price["rent_per_hour"] = round(base_prices["rent_hour"] * condition_mult * depreciation, 2)
        suggested_price["rent_per_day"] = round(base_prices["rent_day"] * condition_mult * depreciation, 2)
        suggested_price["deposit"] = round(suggested_price["rent_per_day"] * 0.5, 2)
    elif request.mode == PricingMode.SELL:
        suggested_price["sale_price"] = round(base_prices["sale"] * condition_mult * depreciation, 2)
    elif request.mode == PricingMode.STORAGE:
        suggested_price["storage_per_week"] = round(base_prices["storage_week"] * condition_mult, 2)
    elif request.mode == PricingMode.ON_SITE_USE:
        suggested_price["on_site_per_hour"] = round(base_prices["rent_hour"] * condition_mult * depreciation * 0.8, 2)
    elif request.mode == PricingMode.SPLIT:
        suggested_price["split_unit_price"] = round(base_prices["sale"] * 0.3 * condition_mult, 2)
    
    # Calculate price range
    price_range = {
        "min": round(next(iter(suggested_price.values())) * 0.7, 2),
        "max": round(next(iter(suggested_price.values())) * 1.3, 2)
    }
    
    # Generate reasoning
    reasoning_parts = []
    reasoning_parts.append(f"Base price for {request.category}: ${next(iter(base_prices.values()))}")
    if condition_mult != 1.0:
        reasoning_parts.append(f"Condition adjustment: {condition_mult}x")
    if depreciation != 1.0:
        reasoning_parts.append(f"Age depreciation: {depreciation}x")
    reasoning = " | ".join(reasoning_parts)
    
    return PricingSuggestion(
        item_name=request.item_name,
        category=request.category,
        suggested_price=suggested_price,
        price_range=price_range,
        confidence=0.85,
        reasoning=reasoning,
        local_demand="medium",
        competitor_prices=[
            {"price": round(next(iter(suggested_price.values())) * 0.9, 2), "source": "competitor_a"},
            {"price": round(next(iter(suggested_price.values())) * 1.1, 2), "source": "competitor_b"}
        ],
        depreciation_factor=depreciation
    )
