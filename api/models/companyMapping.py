from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
import uuid

class CompanyMapping(Base):
    __tablename__ = "company_mapping"
    insightwire_uuid = Column(Text, ForeignKey('insightwire.uuid'), nullable=False)
    company_id = Column(Integer, nullable=False)
    system_timestamp = Column(DateTime)

    insightwire = relationship("InsightWire", back_populates="companies")

    __table_args__ = (
        PrimaryKeyConstraint('insightwire_uuid', 'company_id'),
        Index('idx_company_mapping', 'company_id', 'insightwire_uuid'),
    )
