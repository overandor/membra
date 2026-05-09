from fastapi import APIRouter

router = APIRouter()

@router.get("/trust")
async def get_trust():
    return {"reputation": 0, "verified": False}

@router.post("/trust/verify")
async def verify():
    return {"status": "pending"}
