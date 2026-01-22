from fastapi import APIRouter
from app.services.planner_service import generate_plan
from app.schemas.trip import TripRequest,TripResponse

router = APIRouter()

@router.post("/plan",response_model = TripResponse)
def plan(req: TripRequest):
    return generate_plan(req.city,req.days)
