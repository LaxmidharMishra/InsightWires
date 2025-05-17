from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class SentimentMapping(Base):
    __tablename__ = "sentiment_mapping"
    insightwire_uuid = Column(Text, ForeignKey('insightwire.uuid'), nullable=False)
    sentiment_type_id = Column(Integer, nullable=False)
    system_timestamp = Column(DateTime)

    insightwire = relationship("InsightWire", back_populates="sentiments")

    __table_args__ = (
        PrimaryKeyConstraint('insightwire_uuid', 'sentiment_type_id'),
        Index('idx_sentiment_mapping', 'sentiment_type_id', 'insightwire_uuid'),
    )
