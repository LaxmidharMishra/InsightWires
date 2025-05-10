from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
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
    companies = Column(Text)
    business_activities = Column(Text)
    custom_topics = Column(Text)
    industries = Column(Text)
    sentiment = Column(Text)
    type_of_source = Column(Text)
    type_of_content = Column(Text)
    sources = Column(Text)
    story = Column(Text)
    locations = Column(Text)
    content_languages = Column(Text)
    image_url = Column(Text)
    business_activity_id = Column(Text)
    industry_type_id = Column(Integer)
    content_type_id = Column(Integer)
    source_type_id = Column(Integer)
    sentiment_type_id = Column(Integer)
    location_ids = Column(ARRAY(Text))
    company_ids = Column(ARRAY(Text))
    system_timestamp = Column(Text)