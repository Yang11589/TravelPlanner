from fastapi import APIRouter
from app.services.planner_service import generate_plan

router = APIRouter()

@router.post("/plan")
def plan(city: str, days: int):
    return generate_plan(city,days)
