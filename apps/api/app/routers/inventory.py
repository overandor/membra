from fastapi import APIRouter

router = APIRouter()

@router.get("/inventory")
async def get_inventory():
    return {"items": []}

@router.post("/inventory")
async def create_inventory():
    return {"id": "new_inventory"}
