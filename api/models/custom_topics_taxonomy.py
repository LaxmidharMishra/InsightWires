from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class CustomTopicsTaxonomy(Base):
    __tablename__ = "custom_topics_taxonomy"

    custom_topic_id = Column(Integer, primary_key=True, nullable=False)
    custom_topic = Column(String, nullable=False, unique=True)
