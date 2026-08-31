import json
from app.services.generate_plan import call_gemini, safe_json

def build_modify_prompt(city: str, days: int, current_itinerary: list, history: list, user_message: str):
    return f"""
You are a strict travel planner.

Return ONLY valid JSON.

RULES:
- Keep exactly {days} days
- Each day must have 3 to 5 places
- Each day must include at least 2 food places and 2 attractions
- Respect the user request exactly
- Use the current itinerary and chat history for context

City: {city}
Days: {days}

Current itinerary:
{json.dumps(current_itinerary, ensure_ascii=False)}

Chat history:
{json.dumps(history, ensure_ascii=False)}

User request:
{user_message}

Output format:
{{
  "assistant_reply": "short friendly response",
  "is_valid_topic": 1,
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

def generate_modified_plan(city: str, days: int, current_itinerary: list, history: list, user_message: str):
    prompt = build_modify_prompt(city, days, current_itinerary, history, user_message)
    response = call_gemini(prompt)
    data = safe_json(response.text)

    if "itinerary" not in data:
        raise ValueError("AI response missing itinerary")

    return {
        "assistant_reply": data.get("assistant_reply", "I updated your itinerary."),
        "is_valid_topic": int(data.get("is_valid_topic", 1)),
        "itinerary": data["itinerary"]
    }