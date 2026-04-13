from app.schemas.plan import Plan
from app.schemas.place import Place
from app.schemas.trip import TripResponse

def generate_plan(city: str, days: int):
    itinerary = []

    for d in range(days):
        itinerary.append(
            Plan(
                day = d + 1,
                places = [
                    Place(name = f"Spot {d*2+1}", type = "sight"),
                    Place(name = f"Spot {d*2+2}", type = "food"),
                ]
            )
        )

    return TripResponse(
        city = city,
        days = days,
        itinerary = itinerary)
    
