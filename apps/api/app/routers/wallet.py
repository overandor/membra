from fastapi import APIRouter

router = APIRouter()

@router.get("/wallet")
async def get_wallet():
    return {"balance_usd": 0, "credits": 0}

@router.post("/wallet/withdraw")
async def withdraw():
    return {"status": "pending"}
