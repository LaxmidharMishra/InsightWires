from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class ContentTypeMapping(Base):
    __tablename__ = "content_type_mapping"
    insightwire_uuid = Column(Text, ForeignKey('insightwire.uuid'), nullable=False)
    content_type_id = Column(Integer, nullable=False)
    system_timestamp = Column(DateTime)

    insightwire = relationship("InsightWire", back_populates="content_types")

    __table_args__ = (
        PrimaryKeyConstraint('insightwire_uuid', 'content_type_id'),
        Index('idx_content_type_mapping', 'content_type_id', 'insightwire_uuid'),
    )
