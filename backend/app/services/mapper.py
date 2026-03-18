from app.models.trip import Trip
from app.schemas.trip import TripResponse
from app.schemas.plan import Plan as PlanSchema
from app.schemas.place import Place as PlaceSchema


def trip_to_response(trip: Trip) -> TripResponse:
    return TripResponse(
        city=trip.city,
        days=trip.days,
        itinerary=[
            PlanSchema(
                day=dp.day,
                places=[
                    PlaceSchema(
                        name=p.name,
                        type=p.type
                    )
                    for p in dp.places
                ]
            )
            for dp in trip.plans
        ]
    )


def trips_to_response(trips: list[Trip]) -> list[TripResponse]:
    return [trip_to_response(t) for t in trips]