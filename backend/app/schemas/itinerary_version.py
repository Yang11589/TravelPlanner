from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.plan import Plan


class ItineraryVersionResponse(BaseModel):
    id: int
    message_id: int
    version_number: int
    itinerary: List[Plan]
    created_at: datetime

    class Config:
        from_attributes = True