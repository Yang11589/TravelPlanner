from pydantic import BaseModel, Field
from typing import List
from app.schemas.plan import Plan
from typing import Optional

class TripRequest(BaseModel):
    city: str
    days: int

class TripResponse(BaseModel):
    city: str
    days: int
    itinerary: List[Plan] 
    user_id: Optional[int] = None
    is_saved: Optional[bool] = None 

    class Config:
        from_attributes = True 
