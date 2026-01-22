from pydantic import BaseModel
from typing import List
from app.schemas.place import Place

class Plan(BaseModel):
    day: int
    places: List[Place]
