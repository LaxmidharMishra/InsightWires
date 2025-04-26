from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class ContentsTaxonomy(Base):
    __tablename__ = "contents_taxonomy"

    content_id = Column(Integer, primary_key=True, nullable=False)
    content= Column(String, nullable=False, unique=True)
