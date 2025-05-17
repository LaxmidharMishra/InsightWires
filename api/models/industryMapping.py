from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class IndustryMapping(Base):
    __tablename__ = "industry_mapping"
    insightwire_uuid = Column(Text, ForeignKey('insightwire.uuid'), nullable=False)
    industry_type_id = Column(Integer, nullable=False)
    system_timestamp = Column(DateTime)

    insightwire = relationship("InsightWire", back_populates="industry_types")

    __table_args__ = (
        PrimaryKeyConstraint('insightwire_uuid', 'industry_type_id'),
        Index('idx_industry_mapping', 'industry_type_id', 'insightwire_uuid'),
    )
