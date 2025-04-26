from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class TypeOfContentTaxonomy(Base):
    __tablename__ = "type_of_content_taxonomy"

    type_of_content_id = Column(Integer, primary_key=True, nullable=False)
    type_of_content = Column(String, nullable=False, unique=True)
