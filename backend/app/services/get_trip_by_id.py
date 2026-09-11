from sqlalchemy.orm import Session, joinedload
from app.models.trip import Trip
from app.models.plan import Plan
from app.models.conversation import Conversation
from app.models.itinerary_version import ItineraryVersion
from app.models.message import Message

def get_trip_by_id(
    db: Session,
    trip_id: int,
    user_id: int,
) -> Trip | None:
    return (
        db.query(Trip)
        .options(
            joinedload(Trip.plans).joinedload(Plan.places),
            joinedload(Trip.conversation)
                .joinedload(Conversation.messages)
                .joinedload(Message.itinerary_version),
        )
        .filter(
            Trip.id == trip_id,
            Trip.user_id == user_id,
        )
        .first()
    )