"""
MEMBRA TrustOS API
Identity, proof, disputes, category approvals, deposits, and compliance gates
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid

router = APIRouter(prefix="/trust", tags=["Trust"])


class ProofType(str, Enum):
    """Types of proof"""
    PHOTO = "photo"
    VIDEO = "video"
    SIGNATURE = "signature"
    RECEIPT = "receipt"
    GPS = "gps"
    TIMESTAMP = "timestamp"


class ProofStatus(str, Enum):
    """Proof verification status"""
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    DISPUTED = "disputed"


class DisputeStatus(str, Enum):
    """Dispute resolution status"""
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class ProofRequest(BaseModel):
    """Request to submit proof"""
    user_id: str
    transaction_id: str
    proof_type: ProofType
    proof_data: dict = Field(default_factory=dict)
    metadata: Optional[dict] = None


class Proof(BaseModel):
    """Proof record"""
    proof_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    transaction_id: str
    proof_type: ProofType
    proof_data: dict
    status: ProofStatus = ProofStatus.PENDING
    verified_by: Optional[str] = None
    verified_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[dict] = None


class DisputeRequest(BaseModel):
    """Request to open a dispute"""
    user_id: str
    transaction_id: str
    reason: str
    description: str
    evidence: List[str] = Field(default_factory=list)


class Dispute(BaseModel):
    """Dispute record"""
    dispute_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    transaction_id: str
    reason: str
    description: str
    evidence: List[str]
    status: DisputeStatus = DisputeStatus.OPEN
    resolution: Optional[str] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TrustScore(BaseModel):
    """User trust score"""
    user_id: str
    score: int = Field(ge=0, le=100, default=50)
    completed_transactions: int = 0
    successful_returns: int = 0
    disputes_won: int = 0
    disputes_lost: int = 0
    on_time_deliveries: float = 1.0
    compliance_score: int = Field(ge=0, le=100, default=100)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class DepositRequest(BaseModel):
    """Request to place a deposit"""
    user_id: str
    transaction_id: str
    amount_usd: float
    deposit_type: str = "security"


class Deposit(BaseModel):
    """Deposit record"""
    deposit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    transaction_id: str
    amount_usd: float
    deposit_type: str
    status: str = "held"
    released_at: Optional[datetime] = None
    forfeited: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


@router.post("/proof/submit")
async def submit_proof(request: ProofRequest):
    """
    Submit proof for a transaction
    
    Users submit photos, videos, or other evidence to prove pickup,
    delivery, return, or condition of items.
    """
    proof = Proof(
        user_id=request.user_id,
        transaction_id=request.transaction_id,
        proof_type=request.proof_type,
        proof_data=request.proof_data,
        metadata=request.metadata
    )
    
    # Mock verification logic
    proof.status = ProofStatus.VERIFIED
    proof.verified_by = "system"
    proof.verified_at = datetime.utcnow()
    
    return proof


@router.get("/proof/{proof_id}")
async def get_proof(proof_id: str):
    """Get proof details"""
    return {
        "proof_id": proof_id,
        "status": "verified",
        "verified_at": datetime.utcnow(),
        "proof_type": "photo"
    }


@router.post("/dispute/open")
async def open_dispute(request: DisputeRequest):
    """
    Open a dispute for a transaction
    
    Users can dispute item condition, delivery issues, or other problems.
    """
    dispute = Dispute(
        user_id=request.user_id,
        transaction_id=request.transaction_id,
        reason=request.reason,
        description=request.description,
        evidence=request.evidence
    )
    
    return dispute


@router.get("/dispute/{dispute_id}")
async def get_dispute(dispute_id: str):
    """Get dispute details"""
    return {
        "dispute_id": dispute_id,
        "status": "investigating",
        "created_at": datetime.utcnow()
    }


@router.put("/dispute/{dispute_id}/resolve")
async def resolve_dispute(
    dispute_id: str,
    resolution: str,
    resolved_by: str
):
    """Resolve a dispute"""
    return {
        "dispute_id": dispute_id,
        "status": "resolved",
        "resolution": resolution,
        "resolved_by": resolved_by,
        "resolved_at": datetime.utcnow()
    }


@router.get("/score/{user_id}")
async def get_trust_score(user_id: str):
    """
    Get user trust score
    
    Trust score is calculated from completed transactions, successful returns,
    dispute outcomes, on-time deliveries, and compliance.
    """
    return TrustScore(
        user_id=user_id,
        score=94,
        completed_transactions=47,
        successful_returns=42,
        disputes_won=2,
        disputes_lost=0,
        on_time_deliveries=0.96,
        compliance_score=98
    )


@router.post("/deposit/hold")
async def hold_deposit(request: DepositRequest):
    """
    Hold a deposit for a transaction
    
    Deposits are held for high-value items or new users until
    successful completion or proof of condition.
    """
    deposit = Deposit(
        user_id=request.user_id,
        transaction_id=request.transaction_id,
        amount_usd=request.amount_usd,
        deposit_type=request.deposit_type
    )
    
    return deposit


@router.put("/deposit/{deposit_id}/release")
async def release_deposit(deposit_id: str):
    """Release a held deposit"""
    return {
        "deposit_id": deposit_id,
        "status": "released",
        "released_at": datetime.utcnow(),
        "forfeited": False
    }


@router.put("/deposit/{deposit_id}/forfeit")
async def forfeit_deposit(deposit_id: str, reason: str):
    """Forfeit a deposit due to violation"""
    return {
        "deposit_id": deposit_id,
        "status": "forfeited",
        "forfeited": True,
        "reason": reason
    }


@router.get("/compliance/{user_id}")
async def get_compliance_status(user_id: str):
    """
    Get user compliance status
    
    Shows which categories the user is approved for and which
    require additional verification or deposits.
    """
    return {
        "user_id": user_id,
        "compliance_score": 98,
        "approved_categories": [
            "tools", "electronics", "furniture", "storage", "lighting",
            "camera", "bags", "books", "games", "decor"
        ],
        "restricted_categories": [
            {"category": "high_value", "requirement": "deposit_required"},
            {"category": "overnight_stays", "requirement": "identity_verification"}
        ],
        "blocked_categories": [
            "food", "chemicals", "weapons", "alcohol", "medicine"
        ]
    }


@router.post("/category/request")
async def request_category_approval(
    user_id: str,
    category: str,
    evidence: List[str]
):
    """
    Request approval for a restricted category
    
    Users can request approval for restricted categories by
    providing evidence of compliance (licenses, insurance, etc.).
    """
    return {
        "user_id": user_id,
        "category": category,
        "status": "pending_review",
        "submitted_at": datetime.utcnow(),
        "evidence_count": len(evidence)
    }


@router.get("/identity/{user_id}")
async def get_identity_verification(user_id: str):
    """
    Get user identity verification status
    
    Shows verification level and required documents.
    """
    return {
        "user_id": user_id,
        "verification_level": "verified",
        "verified_at": datetime.utcnow(),
        "documents_on_file": [
            "government_id",
            "phone_verified",
            "email_verified"
        ],
        "required_for": [
            "overnight_stays",
            "unsupervised_access",
            "high_value"
        ]
    }
