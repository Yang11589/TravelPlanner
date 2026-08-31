from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to trips
    trips = relationship(
        "Trip",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Relationship to conversations
    conversations = relationship(
    "Conversation",
    back_populates="user",
    cascade="all, delete-orphan"
)