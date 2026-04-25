from sqlalchemy.orm import Session
from app.models.trip import Trip
from app.models.plan import Plan
from app.models.place import Place
from app.schemas.trip import TripResponse


def save_trip(db: Session, trip_data: TripResponse):
    trip = Trip(
        city=trip_data.city,
        days=trip_data.days,
        user_id=trip_data.user_id
    )

    for plan in trip_data.itinerary:
        dp = Plan(day=plan.day)

        for place in plan.places:
            dp.places.append(
                Place(
                    name=place.name,
                    type=place.type
                )
            )

        trip.plans.append(dp)

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return trip
