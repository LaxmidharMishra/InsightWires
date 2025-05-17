from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class SourceTypeMapping(Base):
    __tablename__ = "source_type_mapping"
    insightwire_uuid = Column(Text, ForeignKey('insightwire.uuid'), nullable=False)
    source_type_id = Column(Integer, nullable=False)
    system_timestamp = Column(DateTime)

    insightwire = relationship("InsightWire", back_populates="source_types")

    __table_args__ = (
        PrimaryKeyConstraint('insightwire_uuid', 'source_type_id'),
        Index('idx_source_type_mapping', 'source_type_id', 'insightwire_uuid'),
    )
