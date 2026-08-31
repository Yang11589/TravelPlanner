from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.message import Message

class ConversationResponse(BaseModel):       
    id: int    
    trip_id: int    
    user_id: int    
    messages: List[Message]  
    created_at: datetime    
    updated_at: datetime

    class Config:        
        from_attributes = True