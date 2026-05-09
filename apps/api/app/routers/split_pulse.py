from fastapi import APIRouter

router = APIRouter()

@router.get("/split-pulse")
async def get_split_pulse():
    return {"pulses": []}

@router.post("/split-pulse")
async def create_split_pulse():
    return {"id": "new_pulse"}
