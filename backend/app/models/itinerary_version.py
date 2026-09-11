from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class ItineraryVersion(Base):
    __tablename__ = "itinerary_versions"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(
        Integer,
        ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    version_number = Column(Integer, nullable=False)
    itinerary = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    message = relationship(
        "Message",
        back_populates="itinerary_version",
    )