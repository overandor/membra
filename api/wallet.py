"""
MEMBRA Wallet/Payment API Endpoints

Wallet layer for credits, earnings, deposits, refunds, rewards, and proof receipts.
Handles transparent payment splits between multiple participants.
"""
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel, Field
from models.membra import Wallet, WalletTransaction
from datetime import datetime
from uuid import uuid4

router = APIRouter(prefix="/wallet", tags=["Wallet"])


class CreateWalletRequest(BaseModel):
    """Request to create a wallet for a user"""
    user_id: str


class AddFundsRequest(BaseModel):
    """Request to add funds to wallet"""
    wallet_id: str
    amount_usd: float
    payment_method: str  # stripe, paypal, bank_transfer
    reference_id: Optional[str] = None


class WithdrawRequest(BaseModel):
    """Request to withdraw funds"""
    wallet_id: str
    amount_usd: float
    destination: str  # bank_account, paypal, debit_card


class PaymentSplitRequest(BaseModel):
    """Request to calculate payment split for a transaction"""
    total_price_usd: float
    tool_hero_payout_usd: float
    skill_hero_payout_usd: float
    alpha_hub_payout_usd: float
    delivery_hero_payout_usd: float
    user_credit_usd: float
    platform_fee_usd: float


@router.post("/create")
async def create_wallet(request: CreateWalletRequest) -> dict:
    """Create a wallet for a user"""
    wallet_id = str(uuid4())
    
    # In production, this would:
    # 1. Check if wallet already exists
    # 2. Create wallet record
    # 3. Initialize with signup bonus credits
    # 4. Link to user account
    
    return {
        "wallet_id": wallet_id,
        "user_id": request.user_id,
        "balance_credits": 100,  # Signup bonus
        "balance_usd": 0.0,
        "loyalty_level": "bronze",
        "created_at": datetime.utcnow().isoformat(),
    }


@router.get("/wallet/{wallet_id}")
async def get_wallet(wallet_id: str) -> dict:
    """Get wallet details and balance"""
    return {
        "wallet_id": wallet_id,
        "user_id": str(uuid4()),
        "balance_credits": 150,
        "balance_usd": 247.50,
        "total_earnings_usd": 3240.0,
        "total_spent_usd": 2992.50,
        "referral_rewards_credits": 50,
        "cashback_credits": 25,
        "deposit_balance_usd": 0.0,
        "loyalty_level": "silver",
        "reputation_score": 4.9,
        "created_at": datetime.utcnow().isoformat(),
    }


@router.post("/add-funds")
async def add_funds(request: AddFundsRequest) -> dict:
    """
    Add funds to wallet.
    
    Users can add USD for purchases or deposits.
    """
    transaction_id = str(uuid4())
    
    # In production, this would:
    # 1. Process payment via Stripe/PayPal
    # 2. Add funds to wallet
    # 3. Record transaction
    # 4. Send confirmation
    
    return {
        "transaction_id": transaction_id,
        "wallet_id": request.wallet_id,
        "amount_usd": request.amount_usd,
        "payment_method": request.payment_method,
        "status": "completed",
        "new_balance_usd": 247.50 + request.amount_usd,
        "created_at": datetime.utcnow().isoformat(),
    }


@router.post("/withdraw")
async def withdraw_funds(request: WithdrawRequest) -> dict:
    """
    Withdraw funds from wallet.
    
    Heroes can withdraw earnings to bank or PayPal.
    """
    transaction_id = str(uuid4())
    
    # In production, this would:
    # 1. Validate sufficient balance
    # 2. Process withdrawal
    # 3. Deduct from wallet
    # 4. Record transaction
    # 5. Initiate transfer
    
    return {
        "transaction_id": transaction_id,
        "wallet_id": request.wallet_id,
        "amount_usd": request.amount_usd,
        "destination": request.destination,
        "status": "processing",
        "estimated_arrival": "1-3 business days",
        "created_at": datetime.utcnow().isoformat(),
    }


@router.get("/wallet/{wallet_id}/transactions")
async def get_wallet_transactions(
    wallet_id: str,
    transaction_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """Get transaction history for a wallet"""
    return {
        "wallet_id": wallet_id,
        "transactions": [
            {
                "transaction_id": str(uuid4()),
                "transaction_type": "payout",
                "amount": 7.00,
                "currency": "USD",
                "description": "Power Drill Rental",
                "reference_id": str(uuid4()),
                "status": "completed",
                "created_at": datetime.utcnow().isoformat(),
            },
            {
                "transaction_id": str(uuid4()),
                "transaction_type": "credit_earn",
                "amount": 10,
                "currency": "CREDITS",
                "description": "Listing created",
                "reference_id": str(uuid4()),
                "status": "completed",
                "created_at": datetime.utcnow().isoformat(),
            },
        ],
        "total": 2,
        "limit": limit,
        "offset": offset,
        "type_filter": transaction_type,
    }


@router.post("/calculate-split")
async def calculate_payment_split(request: PaymentSplitRequest) -> dict:
    """
    Calculate payment split for a transaction.
    
    Transparent breakdown of how payment is distributed.
    """
    total_payout = (
        request.tool_hero_payout_usd +
        request.skill_hero_payout_usd +
        request.alpha_hub_payout_usd +
        request.delivery_hero_payout_usd
    )
    
    return {
        "total_price_usd": request.total_price_usd,
        "payment_split": {
            "user_pays": request.total_price_usd,
            "tool_hero": request.tool_hero_payout_usd,
            "skill_hero": request.skill_hero_payout_usd,
            "alpha_hub": request.alpha_hub_payout_usd,
            "delivery_hero": request.delivery_hero_payout_usd,
            "user_credit": request.user_credit_usd,
            "membra_fee": request.platform_fee_usd,
        },
        "total_payout_usd": total_payout,
        "platform_fee_percentage": round((request.platform_fee_usd / request.total_price_usd) * 100, 1),
        "breakdown_valid": (request.total_price_usd == total_payout + request.user_credit_usd + request.platform_fee_usd),
    }


@router.post("/credit/earn")
async def earn_credits(
    wallet_id: str,
    amount: int,
    reason: str,
    reference_id: Optional[str] = None,
) -> dict:
    """
    Award MEMBRA credits to a user.
    
    Credits are earned through: signup, listings, scans, referrals, rentals, etc.
    """
    transaction_id = str(uuid4())
    
    # In production, this would:
    # 1. Validate credit amount
    # 2. Add to wallet
    # 3. Record transaction
    # 4. Check for loyalty level upgrade
    
    return {
        "transaction_id": transaction_id,
        "wallet_id": wallet_id,
        "amount": amount,
        "reason": reason,
        "reference_id": reference_id,
        "new_balance_credits": 150 + amount,
        "status": "completed",
        "created_at": datetime.utcnow().isoformat(),
    }


@router.post("/credit/spend")
async def spend_credits(
    wallet_id: str,
    amount: int,
    reason: str,
    reference_id: Optional[str] = None,
) -> dict:
    """
    Spend MEMBRA credits.
    
    Credits can be used for purchases or fee discounts.
    """
    transaction_id = str(uuid4())
    
    # In production, this would:
    # 1. Validate sufficient credits
    # 2. Deduct from wallet
    # 3. Record transaction
    
    return {
        "transaction_id": transaction_id,
        "wallet_id": wallet_id,
        "amount": amount,
        "reason": reason,
        "reference_id": reference_id,
        "new_balance_credits": 150 - amount,
        "status": "completed",
        "created_at": datetime.utcnow().isoformat(),
    }


@router.get("/wallet/{wallet_id}/credits")
async def get_credit_balance(wallet_id: str) -> dict:
    """Get credit balance and breakdown"""
    return {
        "wallet_id": wallet_id,
        "balance_credits": 150,
        "breakdown": {
            "signup_bonus": 100,
            "listing_rewards": 30,
            "referral_rewards": 50,
            "cashback_earned": 25,
            "credits_spent": -55,
        },
        "loyalty_level": "silver",
        "next_level": "gold",
        "credits_to_next_level": 350,
    }


@router.post("/deposit")
async def create_deposit(
    wallet_id: str,
    amount_usd: float,
    reference_id: str,  # listing_id or transaction_id
    reason: str,
) -> dict:
    """
    Create a deposit for a high-value item.
    
    Deposits are held as security and returned upon successful completion.
    """
    transaction_id = str(uuid4())
    
    # In production, this would:
    # 1. Process payment
    # 2. Hold in escrow
    # 3. Link to transaction
    # 4. Set return conditions
    
    return {
        "transaction_id": transaction_id,
        "wallet_id": wallet_id,
        "amount_usd": amount_usd,
        "reference_id": reference_id,
        "reason": reason,
        "status": "held",
        "return_conditions": ["item_returned", "no_damage", "on_time"],
        "created_at": datetime.utcnow().isoformat(),
    }


@router.post("/deposit/return")
async def return_deposit(
    deposit_transaction_id: str,
    proof_photo_url: str,
) -> dict:
    """
    Return a deposit after successful transaction completion.
    
    Requires proof of item return and condition.
    """
    return {
        "deposit_transaction_id": deposit_transaction_id,
        "status": "returning",
        "proof_photo_url": proof_photo_url,
        "estimated_return_days": "1-3 business days",
        "processed_at": datetime.utcnow().isoformat(),
    }


@router.get("/wallet/{wallet_id}/deposits")
async def get_wallet_deposits(wallet_id: str) -> dict:
    """Get all deposits for a wallet"""
    return {
        "wallet_id": wallet_id,
        "deposits": [
            {
                "transaction_id": str(uuid4()),
                "amount_usd": 50.0,
                "reference_id": str(uuid4()),
                "reason": "Camera rental",
                "status": "held",
                "created_at": datetime.utcnow().isoformat(),
            },
        ],
        "total_held": 50.0,
    }


@router.get("/user/{user_id}/wallet")
async def get_user_wallet(user_id: str) -> dict:
    """Get wallet for a user (by user_id instead of wallet_id)"""
    return {
        "user_id": user_id,
        "wallet_id": str(uuid4()),
        "balance_credits": 150,
        "balance_usd": 247.50,
        "loyalty_level": "silver",
    }


@router.get("/loyalty-levels")
async def get_loyalty_levels() -> dict:
    """Get loyalty level requirements and benefits"""
    return {
        "levels": [
            {
                "level": "bronze",
                "credits_required": 0,
                "benefits": ["Basic marketplace access", "Standard support"],
            },
            {
                "level": "silver",
                "credits_required": 150,
                "benefits": ["Reduced fees", "Priority support", "Early access to features"],
            },
            {
                "level": "gold",
                "credits_required": 500,
                "benefits": ["Further reduced fees", "Dedicated support", "Beta access"],
            },
            {
                "level": "platinum",
                "credits_required": 1000,
                "benefits": ["Lowest fees", "VIP support", "Feature requests", "Revenue share"],
            },
        ],
    }


@router.post("/referral")
async def create_referral(
    referrer_wallet_id: str,
    referred_user_id: str,
) -> dict:
    """
    Create a referral and award credits to referrer.
    
    Referral program: Users earn credits for inviting new users.
    """
    referral_id = str(uuid4())
    
    # In production, this would:
    # 1. Create referral record
    # 2. Award credits to referrer
    # 3. Give signup bonus to referred user
    # 4. Track conversion
    
    return {
        "referral_id": referral_id,
        "referrer_wallet_id": referrer_wallet_id,
        "referred_user_id": referred_user_id,
        "credits_awarded": 50,
        "status": "completed",
        "created_at": datetime.utcnow().isoformat(),
    }
