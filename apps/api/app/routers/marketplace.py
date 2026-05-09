from fastapi import APIRouter

router = APIRouter()

@router.get("/marketplace")
async def get_marketplace():
    return {"listings": []}

@router.post("/marketplace")
async def create_listing():
    return {"id": "new_listing"}
