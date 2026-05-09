from fastapi import APIRouter

router = APIRouter()

@router.get("/hero")
async def get_hero_dashboard():
    return {"listings": [], "earnings": 0}
