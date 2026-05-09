"""
MEMBRA CameraLink API
Cross-platform camera bridge for inventory scanning and assetification
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from uuid import uuid4
import secrets
import qrcode
import io
import base64

from models.membra import (
    CameraLinkMode, CameraLinkStatus, CameraLinkSession
)

router = APIRouter(tags=["CameraLink"])
sessions_db = {}
detections_db = {}


class CreateSessionRequest(BaseModel):
    desktop_user_id: str
    mode: CameraLinkMode = CameraLinkMode.SNAPSHOT
    expires_in_minutes: int = 15


class JoinSessionRequest(BaseModel):
    session_id: str
    phone_device_id: str


@router.post("/camera-sessions/create")
async def create_session(request: CreateSessionRequest):
    session_id = str(uuid4())
    qr_token = secrets.token_urlsafe(16)
    expires_at = datetime.utcnow() + timedelta(minutes=request.expires_in_minutes)
    
    session = CameraLinkSession(
        session_id=session_id,
        desktop_user_id=request.desktop_user_id,
        mode=request.mode,
        expires_in_minutes=request.expires_in_minutes,
        qr_code_token=qr_token,
        qr_code_url=f"https://membra.app/camera/join/{qr_token}",
        expires_at=expires_at,
        status=CameraLinkStatus.QR_GENERATED
    )
    
    sessions_db[session_id] = session
    
    return {
        "session_id": session_id,
        "qr_token": qr_token,
        "qr_code_url": session.qr_code_url,
        "expires_at": expires_at.isoformat(),
        "status": session.status
    }


@router.get("/camera-sessions/{session_id}/qr")
async def get_qr_code(session_id: str):
    session = sessions_db.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Generate QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(session.qr_code_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        "session_id": session_id,
        "qr_token": session.qr_code_token,
        "qr_code_url": session.qr_code_url,
        "qr_code_image": f"data:image/png;base64,{img_str}",
        "expires_at": session.expires_at.isoformat() if session.expires_at else None
    }


@router.post("/camera-sessions/{session_id}/join")
async def join_session(request: JoinSessionRequest):
    session = sessions_db.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.phone_device_id = request.phone_device_id
    session.status = CameraLinkStatus.JOINED
    session.joined_at = datetime.utcnow()
    
    return {"session_id": request.session_id, "status": "joined"}


@router.post("/camera-sessions/{session_id}/photo")
async def upload_photo(session_id: str, photo: UploadFile = File(...)):
    session = sessions_db.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.photos_uploaded += 1
    session.status = CameraLinkStatus.PROCESSING
    
    # Mock AI detection
    detection = mock_detect_items(photo.filename)
    
    return {
        "session_id": session_id,
        "photo_count": session.photos_uploaded,
        "detection": detection
    }


@router.get("/camera-sessions/{session_id}/detections")
async def get_detections(session_id: str):
    session = sessions_db.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "detections": session.detections,
        "status": session.status
    }


@router.post("/camera-sessions/{session_id}/approve")
async def approve_listings(session_id: str, detection_ids: List[str]):
    session = sessions_db.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.status = CameraLinkStatus.APPROVED
    
    return {
        "session_id": session_id,
        "approved_count": len(detection_ids),
        "status": "approved"
    }


@router.post("/camera-sessions/{session_id}/end")
async def end_session(session_id: str):
    session = sessions_db.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.status = CameraLinkStatus.ENDED
    session.ended_at = datetime.utcnow()
    
    return {"session_id": session_id, "status": "ended"}


def mock_detect_items(photo_name: str) -> dict:
    """Mock AI detection - replace with real vision model in production"""
    # Simulate AI vision detection based on photo context
    # In production, this would call OpenAI Vision, GPT-4 Vision, or similar
    
    detected_items = []
    
    # Simulate detecting common household items
    mock_inventory = [
        {"name": "Power drill", "category": "tools", "confidence": 0.92, "suggested_price": {"rent_per_hour": 10, "deposit": 25}},
        {"name": "Extension cord", "category": "electronics", "confidence": 0.88, "suggested_price": {"rent_per_hour": 3, "deposit": 10}},
        {"name": "Ladder", "category": "tools", "confidence": 0.95, "suggested_price": {"rent_per_hour": 8, "deposit": 20}},
        {"name": "Ring light", "category": "lighting", "confidence": 0.89, "suggested_price": {"rent_per_hour": 8, "deposit": 15}},
        {"name": "Tripod", "category": "camera", "confidence": 0.91, "suggested_price": {"rent_per_hour": 12, "deposit": 30}},
        {"name": "Storage bin", "category": "storage", "confidence": 0.87, "suggested_price": {"rent_per_week": 3, "sale_price": 8}},
        {"name": "Desk lamp", "category": "lighting", "confidence": 0.85, "suggested_price": {"rent_per_hour": 5, "deposit": 10}},
        {"name": "Screwdriver set", "category": "tools", "confidence": 0.93, "suggested_price": {"rent_per_hour": 5, "deposit": 15}},
    ]
    
    # Randomly select 2-4 items to simulate detection
    import random
    num_items = random.randint(2, 4)
    selected_items = random.sample(mock_inventory, num_items)
    
    for item in selected_items:
        detected_items.append({
            "item_id": str(uuid4()),
            "name": item["name"],
            "category": item["category"],
            "confidence": item["confidence"],
            "suggested_price": item["suggested_price"],
            "condition_estimate": "good",
            "risk_level": "low",
            "needs_approval": True
        })
    
    return {
        "detection_id": str(uuid4()),
        "detected_items": detected_items,
        "total_items": len(detected_items),
        "overall_confidence": sum(item["confidence"] for item in detected_items) / len(detected_items),
        "ai_model": "gpt-4-vision-preview (mock)",
        "processing_time_ms": 1250
    }
