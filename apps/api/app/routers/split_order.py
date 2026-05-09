from fastapi import APIRouter

router = APIRouter()

@router.post("/split-order")
async def create_split_order():
    return {"id": "new_split_order"}

@router.get("/split-order/{order_id}")
async def get_split_order(order_id: str):
    return {"id": order_id}
