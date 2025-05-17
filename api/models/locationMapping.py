from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class LocationMapping(Base):
    __tablename__ = "location_mapping"
    insightwire_uuid = Column(Text, ForeignKey('insightwire.uuid'), nullable=False)
    location_id = Column(Integer, nullable=False)
    system_timestamp = Column(DateTime)

    insightwire = relationship("InsightWire", back_populates="locations")

    __table_args__ = (
        PrimaryKeyConstraint('insightwire_uuid', 'location_id'),
        Index('idx_location_mapping', 'location_id', 'insightwire_uuid'),
    )
