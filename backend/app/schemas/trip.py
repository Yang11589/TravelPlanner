from pydantic import BaseModel, Field
from typing import List
from app.schemas.plan import Plan
from typing import Optional
from app.schemas.message import Message

class TripRequest(BaseModel):
    city: str
    days: int

class TripResponse(BaseModel):
    city: str
    days: int
    itinerary: List[Plan] 
    user_id: Optional[int] = None
    is_saved: Optional[bool] = None 
    conversation_id: Optional[int] = None
    id: Optional[int] = None
    messages: List[Message] = Field(default_factory=list)


    class Config:
        from_attributes = True 
