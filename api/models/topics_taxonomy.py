from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class TopicsTaxonomy(Base):
    __tablename__ = "topics_taxonomy"

    topic_id = Column(Integer, primary_key=True, nullable=False)
    topic = Column(String, nullable=False, unique=True)
