from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class LanguageTaxonomy(Base):
    __tablename__ = "language_taxonomy"

    language_id = Column(Integer, primary_key=True, nullable=False)
    language = Column(String, nullable=False, unique=True)
