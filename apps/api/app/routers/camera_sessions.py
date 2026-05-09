from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime, timedelta

router = APIRouter()

# In-memory session storage (replace with database in production)
sessions = {}

class CreateSessionRequest(BaseModel):
    desktop_user_id: str
    mode: str = "snapshot"  # "snapshot" or "live_scan"

class JoinSessionRequest(BaseModel):
    phone_device_id: str

class PhotoUploadRequest(BaseModel):
    photo_data: str  # base64 encoded

class FrameUploadRequest(BaseModel):
    frame_data: str  # base64 encoded

class ApprovalRequest(BaseModel):
    approved_listings: list
    rejected_listings: list

@router.post("/v1/camera-sessions/create")
async def create_camera_session(request: CreateSessionRequest):
    session_id = f"scan_{uuid.uuid4().hex[:12]}"
    session = {
        "scan_session_id": session_id,
        "desktop_user_id": request.desktop_user_id,
        "phone_device_id": None,
        "mode": request.mode,
        "pairing_method": "qr_code",
        "expires_at": datetime.utcnow() + timedelta(minutes=10),
        "camera_permission": False,
        "owner_approval_required": True,
        "status": "waiting_for_pairing",
        "photos": [],
        "detections": [],
        "created_at": datetime.utcnow(),
    }
    sessions[session_id] = session
    return {"session_id": session_id, "qr_code_url": f"/v1/camera-sessions/{session_id}/qr"}

@router.get("/v1/camera-sessions/{session_id}/qr")
async def get_qr_code(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "qr_data": f"membra://camera/{session_id}"}

@router.post("/v1/camera-sessions/{session_id}/join")
async def join_session(session_id: str, request: JoinSessionRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    if datetime.utcnow() > session["expires_at"]:
        raise HTTPException(status_code=410, detail="Session expired")
    session["phone_device_id"] = request.phone_device_id
    session["status"] = "connected"
    session["camera_permission"] = True
    return {"status": "connected", "mode": session["mode"]}

@router.post("/v1/camera-sessions/{session_id}/photo")
async def upload_photo(session_id: str, request: PhotoUploadRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    if session["mode"] != "snapshot":
        raise HTTPException(status_code=400, detail="Session not in snapshot mode")
    photo_id = f"photo_{uuid.uuid4().hex[:8]}"
    session["photos"].append({
        "photo_id": photo_id,
        "data": request.photo_data,
        "timestamp": datetime.utcnow().isoformat(),
    })
    return {"photo_id": photo_id, "status": "uploaded"}

@router.post("/v1/camera-sessions/{session_id}/frame")
async def upload_frame(session_id: str, request: FrameUploadRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    if session["mode"] != "live_scan":
        raise HTTPException(status_code=400, detail="Session not in live scan mode")
    frame_id = f"frame_{uuid.uuid4().hex[:8]}"
    session["photos"].append({
        "frame_id": frame_id,
        "data": request.frame_data,
        "timestamp": datetime.utcnow().isoformat(),
    })
    return {"frame_id": frame_id, "status": "received"}

@router.get("/v1/camera-sessions/{session_id}/detections")
async def get_detections(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    # Mock detections - replace with actual vision + LLM pipeline
    detections = [
        {"object": "power_drill", "confidence": 0.92, "suggested_price": "$7/hour"},
        {"object": "tripod", "confidence": 0.88, "suggested_price": "$5/hour"},
        {"object": "ring_light", "confidence": 0.95, "suggested_price": "$6/hour"},
    ]
    session["detections"] = detections
    return {"detections": detections}

@router.post("/v1/camera-sessions/{session_id}/approve-listings")
async def approve_listings(session_id: str, request: ApprovalRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    session["approved_listings"] = request.approved_listings
    session["rejected_listings"] = request.rejected_listings
    session["status"] = "completed"
    return {"status": "approved", "count": len(request.approved_listings)}

@router.post("/v1/camera-sessions/{session_id}/end")
async def end_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    session["status"] = "ended"
    session["ended_at"] = datetime.utcnow().isoformat()
    return {"status": "ended", "session_id": session_id}
