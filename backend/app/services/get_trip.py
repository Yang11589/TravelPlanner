from sqlalchemy.orm import Session, joinedload
from app.models.trip import Trip
from app.models.plan import Plan
from sqlalchemy import desc
from app.models.conversation import Conversation
from app.models.message import Message

def get_trips(db: Session, user_id: int, limit: int = 10, offset: int = 0):
    query = db.query(Trip).filter(Trip.user_id == user_id)


    total = query.count()

    trips = (
        query
        .options(
            joinedload(Trip.plans).joinedload(Plan.places),
            joinedload(Trip.conversation)
                .joinedload(Conversation.messages)
                .joinedload(Message.itinerary_version),
        )
        .order_by(desc(Trip.id))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, trips