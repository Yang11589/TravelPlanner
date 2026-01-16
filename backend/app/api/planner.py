from fastapi import APIRouter

router = APIRouter()

@router.post("/plan")
def plan(city: str, days: int):
    return {"city": city, "days": days, "plan": []}
