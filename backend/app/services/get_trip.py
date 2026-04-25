from sqlalchemy.orm import Session, joinedload
from app.models.trip import Trip
from app.models.plan import Plan
from sqlalchemy import desc


def get_trips(db: Session, user_id: int, limit: int = 10, offset: int = 0):
    query = db.query(Trip).filter(Trip.user_id == user_id)


    total = query.count()

    trips = (
        query
        .options(
            joinedload(Trip.plans)
            .joinedload(Plan.places)
        )
        .order_by(desc(Trip.id))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, trips