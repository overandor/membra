"""Email and SMS notification service using Twilio."""

import os
from typing import Optional, Dict, Any
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_sms(phone: str, message: str) -> Dict[str, Any]:
    """Send SMS notification via Twilio."""
    if not twilio_client:
        return {"success": False, "error": "Twilio not configured"}
    try:
        message_obj = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone
        )
        return {"success": True, "message_id": message_obj.sid}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_booking_confirmation_sms(phone: str, booking_id: str, check_in_code: str, space_title: str) -> Dict[str, Any]:
    message = f"Your Couchify booking is confirmed! Space: {space_title}. Check-in code: {check_in_code}. Booking ID: {booking_id}"
    return send_sms(phone, message)


def send_check_in_reminder_sms(phone: str, check_in_code: str, start_time: str) -> Dict[str, Any]:
    message = f"Reminder: Your Couchify booking starts at {start_time}. Check-in code: {check_in_code}"
    return send_sms(phone, message)


def send_check_out_reminder_sms(phone: str) -> Dict[str, Any]:
    message = "Your Couchify booking is ending soon. Please check out to complete your session."
    return send_sms(phone, message)


def send_host_new_booking_sms(phone: str, guest_name: str, space_title: str, amount: float) -> Dict[str, Any]:
    message = f"New booking! Guest: {guest_name} booked {space_title} for ${amount:.2f}. Check your dashboard."
    return send_sms(phone, message)


def send_host_payout_sms(phone: str, amount: float) -> Dict[str, Any]:
    message = f"Payout processed: ${amount:.2f} will arrive in your account within 2-3 business days."
    return send_sms(phone, message)


def send_booking_confirmation_email(email: str, booking_id: str, check_in_code: str, space_title: str) -> Dict[str, Any]:
    return {"success": True, "message": "Email notification would be sent here"}
