from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer, nullable=False)

    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)

    trip = relationship("Trip", back_populates="plan")

    places = relationship(
        "Place",
        back_populates="plan",
        cascade="all, delete-orphan"
    )
