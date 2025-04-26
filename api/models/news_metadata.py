from sqlalchemy import Column, String, DateTime, Text, Integer, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()
   
class NewsMetadata(Base):
    __tablename__ = "news_metadata"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    lead_paragraph = Column(Text)
    news_url = Column(String, nullable=False, unique=True)
    published_date = Column(DateTime, nullable=False)
    companies = Column(Text)
    business_activities = Column(Text)
    custom_topics = Column(Text)
    industries = Column(Text)
    sentiment = Column(String)
    type_of_source = Column(String)
    type_of_content = Column(String)
    sources = Column(Text)
    story = Column(Text)
    locations = Column(Text)
    content_languages = Column(Text)
    image_url = Column(String)
    system_timestamp = Column(DateTime, nullable=False)

    business_activity_id = Column(Integer)
    language_id = Column(Integer)
    location_id = Column(ARRAY(Integer))  
    source_type_id = Column(Integer)
    theme_id = Column(ARRAY(Integer))
    topic_id = Column(ARRAY(Integer))
    content_id = Column(ARRAY(Integer))