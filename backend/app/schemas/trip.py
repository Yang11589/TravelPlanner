from pydantic import BaseModel
from typing import List
from app.schemas.plan import Plan

class TripRequest(BaseModel):
    city: str
    days: int

class TripResponse(BaseModel):
    city: str
    days: int
    itinerary: List[Plan]
