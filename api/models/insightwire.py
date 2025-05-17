from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class InsightWire(Base):
    __tablename__ = "insightwire"
    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    rss_id = Column(Integer)
    title = Column(Text)
    lead_paragraph = Column(Text)
    news_url = Column(Text)
    published_date = Column(Text)
    custom_topics = Column(Text)
    sentiment = Column(Text)
    type_of_source = Column(Text)
    type_of_content = Column(Text)
    sources = Column(Text)
    story = Column(Text)
    locations = Column(Text)
    content_languages = Column(Text)
    image_url = Column(Text)
    
    # Relationships
    # business_activities = relationship("BusinessActivityMapping", back_populates="insightwire", cascade="all, delete-orphan")
    # companies = relationship("CompanyMapping", back_populates="insightwire", cascade="all, delete-orphan")
    # industry_types = relationship(IndustryMapping, back_populates="insightwire", cascade="all, delete-orphan")
    # content_types = relationship("ContentTypeMapping", back_populates="insightwire", cascade="all, delete-orphan")
    # source_types = relationship("SourceTypeMapping", back_populates="insightwire", cascade="all, delete-orphan")
    # sentiment_types = relationship("SentimentTypeMapping", back_populates="insightwire", cascade="all, delete-orphan")
