from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False)
    days = Column(Integer, nullable=False)

    day_plans = relationship(
        "Plan",
        back_populates="trip",
        cascade="all, delete-orphan"
    )
