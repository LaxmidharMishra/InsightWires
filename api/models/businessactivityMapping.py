from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class BusinessActivityMapping(Base):
    __tablename__ = "business_activity_mapping"

    insightwire_uuid = Column(Text, ForeignKey('insightwire.uuid'), nullable=False)
    business_activity_id = Column(Integer, nullable=False)
    system_timestamp = Column(DateTime)

    insightwire = relationship("InsightWire", back_populates="business_activities")

    __table_args__ = (
        PrimaryKeyConstraint('insightwire_uuid', 'business_activity_id'),
        Index('idx_business_activity_mapping', 'business_activity_id', 'insightwire_uuid'),
    )
