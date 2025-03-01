from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "news_articles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String, nullable=False)
    lead_paragraph = Column(String)
    url = Column(String, nullable=False, unique=True)
    date_published = Column(DateTime, nullable=False)
    companies = Column(String)
    topics = Column(String)
    business_events = Column(String)
    themes = Column(String)
    custom_topics = Column(String)
    industries = Column(String)
    type_of_source = Column(String)
    type_of_content = Column(String)
    sources = Column(String)
    locations = Column(String)
    content_languages = Column(String)
    image_url = Column(String)
