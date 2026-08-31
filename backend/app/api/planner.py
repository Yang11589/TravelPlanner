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

from app.services.modify_plan import generate_modified_plan
from app.services.create_conversation import create_trip_for_user, get_or_create_conversation, append_message, update_trip_itinerary



router = APIRouter(prefix="/planner", tags=["planner"])

@router.post("/plan",response_model = TripResponse)
def plan(req: TripRequest, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_user)):
    trip_data = generate_plan(req.city, req.days)
    if current_user:
        trip_data.user_id = current_user.id
        save_trip(db, trip_data)
        trip_data.is_saved = True
        trip, conversation = create_trip_for_user(db, trip_data, current_user.id)
        trip_data.conversation_id = conversation.id
    else:
            trip_data.is_saved = False
            trip_data.conversation_id = None
            
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

@router.post("/plan/chat")
def chat_plan(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    message = payload.get("message", "")
    history = payload.get("history", [])
    current_itinerary = payload.get("current_itinerary", [])

    if not current_user:
        result = generate_modified_plan(
            city=payload.get("city"),
            days=payload.get("days"),
            current_itinerary=current_itinerary,
            history=history,
            user_message=message,
        )

        return {
            "assistant_reply": result["assistant_reply"],
            "itinerary": result["itinerary"],
            "is_valid_topic": result["is_valid_topic"],
            "is_saved": False,
            "user_id": None,
            "conversation_id": None,
        }

    trip_id = payload.get("trip_id")
    if not trip_id:
        raise HTTPException(status_code=400, detail="trip_id is required for logged-in chat")

    trip = (
        db.query(Trip)
        .filter(Trip.id == trip_id, Trip.user_id == current_user.id)
        .first()
    )
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    conversation = get_or_create_conversation(db, trip.id, current_user.id)
    append_message(db, conversation.id, "user", message, 1)

    result = generate_modified_plan(
        city=trip.city,
        days=trip.days,
        current_itinerary=current_itinerary,
        history=history,
        user_message=message,
    )

    update_trip_itinerary(db, trip, result["itinerary"])
    append_message(
        db,
        conversation.id,
        "assistant",
        result["assistant_reply"],
        result["is_valid_topic"],
    )

    return {
        "assistant_reply": result["assistant_reply"],
        "itinerary": result["itinerary"],
        "is_valid_topic": result["is_valid_topic"],
        "is_saved": True,
        "user_id": current_user.id,
        "conversation_id": conversation.id,
    }