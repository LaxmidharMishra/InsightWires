from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class LocationsTaxonomy(Base):
    __tablename__ = "locations_taxonomy"

    location_id = Column(Integer, primary_key=True, nullable=False)
    location = Column(String, nullable=False, unique=True)
