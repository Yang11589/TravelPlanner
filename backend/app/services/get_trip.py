from sqlalchemy.orm import Session, joinedload
from app.models.trip import Trip
from app.models.plan import Plan


def get_trips(db: Session, limit: int = 10, offset: int = 0):
    query = db.query(Trip)

    total = query.count()

    trips = (
        query
        .options(
            joinedload(Trip.plans)
            .joinedload(Plan.places)
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, trips