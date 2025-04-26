from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class ThemesTaxonomy(Base):
    __tablename__ = "themes_taxonomy"

    theme_id = Column(Integer, primary_key=True, nullable=False)
    theme = Column(String, nullable=False, unique=True)
