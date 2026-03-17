from fastapi import APIRouter, Depends
from app.schemas.trip import TripRequest,TripResponse
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.generate_plan import generate_plan
from app.services.save_trip import save_trip

router = APIRouter()

@router.post("/plan",response_model = TripResponse)
def plan(req: TripRequest, db: Session = Depends(get_db)):
    trip_data = generate_plan(req.city, req.days)
    save_trip(db, trip_data)
    return trip_data

