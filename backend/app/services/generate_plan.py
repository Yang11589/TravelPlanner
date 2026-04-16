import os
import json
import time
from dotenv import load_dotenv
from google import genai

from app.schemas.plan import Plan
from app.schemas.place import Place
from app.schemas.trip import TripResponse
import random

load_dotenv()

client = genai.Client()

#Prompt
def build_prompt(city: str, days: int):
    return f"""
You are a strict travel planner.

Return ONLY valid JSON.

RULES:
- Each day must have 3 to 5 places
- Each day must include at least 2 food place and 2 attractions

City: {city}
Days: {days}

Output format:
{{
  "city": "{city}",
  "days": {days},
  "itinerary": [
    {{
      "day": 1,
      "places": [
        {{"name": "Sky Tower", "type": "attraction"}},
        {{"name": "Depot Eatery", "type": "food"}}
      ]
    }}
  ]
}}
"""

#Call AI
def call_gemini(prompt: str):
    try:
        return client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    except Exception as e:
        print("Gemini error:", e)
        time.sleep(12) 
        raise


# JSON Secure Parsing
def safe_json(text: str):
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    data = json.loads(text)

    if isinstance(data, str):
        data = json.loads(data)

    return data



def generate_plan(city: str, days: int) -> TripResponse:

    response = call_gemini(build_prompt(city, days))
    data = safe_json(response.text)

    itinerary = []

    for i, d in enumerate(data.get("itinerary", [])):
        places = []

        for p in d.get("places", []):
            name = p.get("name", "Unknown")
            ptype = p.get("type", "attraction")

            if ptype not in ["attraction", "food"]:
                ptype = "attraction"

            places.append(Place(name=name, type=ptype))

        itinerary.append(
            Plan(
                day=d.get("day", i + 1),
                places=places
            )
        )

    return TripResponse(
        city=data.get("city", city),
        days=data.get("days", days),
        itinerary=itinerary
    )




# from app.schemas.plan import Plan
# from app.schemas.place import Place
# from app.schemas.trip import TripResponse

# def generate_plan(city: str, days: int):
#     itinerary = []

#     for d in range(days):
#         itinerary.append(
#             Plan(
#                 day = d + 1,
#                 places = [
#                     Place(name = f"Spot {d*2+1}", type = "sight"),
#                     Place(name = f"Spot {d*2+2}", type = "food"),
#                 ]
#             )
#         )

#     return TripResponse(
#         city = city,
#         days = days,
#         itinerary = itinerary)