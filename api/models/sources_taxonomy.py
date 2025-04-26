from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class SourcesTaxonomy(Base):
    __tablename__ = "sources_taxonomy"

    source_id = Column(Integer, primary_key=True, nullable=False)
    source = Column(String, nullable=False, unique=True)
