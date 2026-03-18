from sqlalchemy.orm import Session
from app.models.trip import Trip

def delete_trip(db: Session, trip_id: int) -> bool:
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        return False

    db.delete(trip)
    db.commit()

    return True