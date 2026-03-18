from sqlalchemy.orm import Session, joinedload
from app.models.trip import Trip
from app.models.plan import Plan


def get_trip_by_id(db: Session, trip_id: int) -> Trip | None:
    return (
        db.query(Trip)
        .options(
            joinedload(Trip.plans)
            .joinedload(Plan.places)
        )
        .filter(Trip.id == trip_id)
        .first()
    )