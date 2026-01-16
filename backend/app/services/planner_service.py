def generate_plan(city: str, days: int):
    itinerary = []

    for d in range(days):
        itinerary.append({
            "day": d + 1,
            "places": [
                {"name": f"{city} Spot {d*2+1}", "type": "sight"},
                {"name": f"{city} Spot {d*2+2}", "type": "food"},
            ]
        })

    return {
        "city": city,
        "days": days,
        "itinerary": itinerary
    }
