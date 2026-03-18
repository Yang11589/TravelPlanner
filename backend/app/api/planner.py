from fastapi import APIRouter, Depends, Query, HTTPException
from app.schemas.trip import TripRequest,TripResponse
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.generate_plan import generate_plan
from app.services.save_trip import save_trip

from app.schemas.trip_list import TripListResponse
from app.services.get_trip import get_trips

from app.services.get_trip_by_id import get_trip_by_id


router = APIRouter()

@router.post("/plan",response_model = TripResponse)
def plan(req: TripRequest, db: Session = Depends(get_db)):
    trip_data = generate_plan(req.city, req.days)
    save_trip(db, trip_data)
    return trip_data

@router.get("/trips", response_model=TripListResponse)
def list_trips(
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    total, trips = get_trips(db, limit=limit, offset=offset)

    return {
        "total": total,
        "items": trips
    }

@router.get("/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = get_trip_by_id(db, trip_id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    return trip