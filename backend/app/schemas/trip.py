from pydantic import BaseModel, Field
from typing import List
from app.schemas.plan import Plan

class TripRequest(BaseModel):
    city: str
    days: int

class TripResponse(BaseModel):
    city: str
    days: int
    itinerary: List[Plan] = Field(alias="plans")
