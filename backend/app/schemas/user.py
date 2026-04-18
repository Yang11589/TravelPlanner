from pydantic import BaseModel
from datetime import datetime

class UserRegister(BaseModel):
    username: str  
    password: str  

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "password123"
            }
        }

class UserLogin(BaseModel):
    """User login request"""
    username: str  
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "password123"
            }
        }

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str
    user_id: int
    username: str  

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": 1,
                "username": "john_doe"
            }
        }

class UserResponse(BaseModel):
    """User info response"""
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True