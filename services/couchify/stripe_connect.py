"""Stripe Connect integration for host onboarding and payments."""

import os
import uuid
import stripe
from typing import Optional, Dict, Any

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

STRIPE_CONNECT_REDIRECT_URI = os.getenv(
    "STRIPE_CONNECT_REDIRECT_URI",
    "https://fancy-pans-take.loca.lt/stripe/connect/callback"
)


def create_connect_link(host_id: str) -> str:
    account_link = stripe.AccountLink.create(
        account=create_stripe_account(host_id),
        refresh_url=STRIPE_CONNECT_REDIRECT_URI,
        return_url=STRIPE_CONNECT_REDIRECT_URI,
        type="account_onboarding",
    )
    return account_link.url


def create_stripe_account(host_id: str) -> str:
    account = stripe.Account.create(
        type="express",
        capabilities={
            "transfers": {"requested": True},
            "card_payments": {"requested": True},
        },
        business_type="individual",
        metadata={"host_id": host_id},
    )
    return account.id


def retrieve_account(account_id: str) -> Dict[str, Any]:
    account = stripe.Account.retrieve(account_id)
    return {
        "id": account.id,
        "charges_enabled": account.charges_enabled,
        "payouts_enabled": account.payouts_enabled,
        "details_submitted": account.details_submitted,
    }


def create_payment_intent(
    amount_cents: int,
    booking_id: str,
    host_stripe_account_id: str,
    guest_email: str,
) -> Dict[str, Any]:
    payment_intent = stripe.PaymentIntent.create(
        amount=amount_cents,
        currency="usd",
        metadata={"booking_id": booking_id},
        transfer_data={"destination": host_stripe_account_id},
        receipt_email=guest_email,
    )
    return {
        "client_secret": payment_intent.client_secret,
        "payment_intent_id": payment_intent.id,
    }


def calculate_payout_amount(total_cents: int) -> Dict[str, int]:
    PLATFORM_FEE_PERCENT = 0.10
    platform_fee_cents = int(total_cents * PLATFORM_FEE_PERCENT)
    host_payout_cents = total_cents - platform_fee_cents
    return {
        "platform_fee_cents": platform_fee_cents,
        "host_payout_cents": host_payout_cents,
    }


def create_transfer(
    host_stripe_account_id: str,
    amount_cents: int,
    booking_id: str,
) -> Dict[str, Any]:
    transfer = stripe.Transfer.create(
        amount=amount_cents,
        currency="usd",
        destination=host_stripe_account_id,
        metadata={"booking_id": booking_id},
    )
    return {"transfer_id": transfer.id}


def refund_payment(payment_intent_id: str, reason: str = "requested_by_customer") -> Dict[str, Any]:
    refund = stripe.Refund.create(
        payment_intent=payment_intent_id,
        reason=reason,
    )
    return {"refund_id": refund.id, "amount": refund.amount}
