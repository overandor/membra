from fastapi import APIRouter

router = APIRouter()

@router.post("/relay")
async def create_relay():
    return {"id": "new_relay"}

@router.get("/relay/{relay_id}")
async def get_relay(relay_id: str):
    return {"id": relay_id}
