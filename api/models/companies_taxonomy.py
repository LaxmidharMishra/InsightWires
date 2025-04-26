from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class CompaniesTaxonomy(Base):
    __tablename__ = "companies_taxonomy"

    company_id = Column(Integer, primary_key=True, nullable=False)
    company_name = Column(String, nullable=False, unique=True)
    company_url = Column(String, nullable=False, unique=True)
