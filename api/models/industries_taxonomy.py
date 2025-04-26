from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class IndustriesTaxonomy(Base):
    __tablename__ = "industries_taxonomy"

    industry_id = Column(Integer, primary_key=True, nullable=False)
    industry_name= Column(String, nullable=False, unique=True)
