from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.schemas.trip import TripRequest,TripResponse
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.generate_plan import generate_plan
from app.services.save_trip import save_trip

from app.schemas.trip_list import TripListResponse
from app.services.get_trip import get_trips

from app.services.get_trip_by_id import get_trip_by_id
from app.services.delete_trip import delete_trip

from app.services.mapper import trips_to_response
from app.services.mapper import trip_to_response

from app.api.user_deps import get_current_user
from app.models.user import User
from typing import Optional



router = APIRouter()

@router.post("/plan",response_model = TripResponse)
def plan(req: TripRequest, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user)):
    trip_data = generate_plan(req.city, req.days)
    if current_user:
        trip_data.user_id = current_user.id
        save_trip(db, trip_data)
        trip_data.is_saved = True
    else:
            trip_data.is_saved = False
            
    return trip_data

@router.get("/trips", response_model=TripListResponse)
def list_trips(
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated"
        )
    total, trips = get_trips(db, user_id=current_user.id, limit=limit, offset=offset)
    items = trips_to_response(trips)

    return {
        "total": total,
        "items": items
    }

@router.get("/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated"
        )
    trip = get_trip_by_id(db, trip_id)

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    return trip_to_response(trip)

@router.delete("/trips/{trip_id}")
def remove_trip(trip_id: int, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated"
        )
    success = delete_trip(db, trip_id)

    if not success:
        raise HTTPException(status_code=404, detail="Trip not found")

    return {"message": "Trip deleted successfully"}