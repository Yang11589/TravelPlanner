from pydantic import BaseModel
from typing import List

from app.schemas.trip import TripResponse


class TripListResponse(BaseModel):
    total: int
    items: List[TripResponse]
    
