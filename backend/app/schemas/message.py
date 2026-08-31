from pydantic import BaseModel
from typing import List
from datetime import datetime

class Message(BaseModel):
    id: int
    role: str  
    content: str
    is_valid_topic: int  
    created_at: datetime

    class Config:
        from_attributes = True

class MessageRequest(BaseModel):
    content: str


class MessageResponse(BaseModel):
    role: str  # Always "assistant"
    content: str  # The AI's answer
    is_valid_topic: int  
    created_at: datetime

    class Config:
        from_attributes = True