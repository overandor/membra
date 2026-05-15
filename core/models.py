from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Any



def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class Asset:
    asset_id: str
    tenant_id: str
    owner_name: str
    asset_type: str
    title: str
    description: str
    city: str
    permission_status: str
    verification_status: str
    risk_level: str
    visibility_score: int
    foot_traffic_score: int
    source: str = "user"


@dataclass(slots=True)
class Campaign:
    campaign_id: str
    tenant_id: str
    asset_id: str
    buyer_name: str
    campaign_name: str
    status: str
    monthly_budget: float


@dataclass(slots=True)
class WalletRecord:
    wallet_id: str
    tenant_id: str
    owner_name: str
    payout_eligibility_status: str
    available_balance: float
    pending_balance: float


@dataclass(slots=True)
class ProofEvent:
    event_id: str
    tenant_id: str
    entity_type: str
    entity_id: str
    event_type: str
    payload: dict[str, Any]
    previous_hash: str
    event_hash: str
    created_at: str
