import sys

sys.path.append("/app")
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import asyncpg
import csv
from io import StringIO
from datetime import datetime
import uuid
import re

from util.database import get_async_db  # Use async session
from util.models import NewsArticle

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("InsightWiresFastApi")

router = APIRouter()

# Database Connection
DATABASE_URL = "postgresql://user:password@db:5432/news_analytics"

# Expected columns in normalized format
EXPECTED_COLUMNS = [
    "title", "lead_paragraph", "url", "date_published", "companies", "topics",
    "business_events", "themes", "custom_topics", "industries",
    "type_of_source", "type_of_content", "sources", "locations",
    "content_languages", "uuid", "image_url"
]

# Mapping for renaming columns from CSV to match database schema
COLUMN_MAPPING = {
    "Title": "title",
    "Lead Paragraph": "lead_paragraph",
    "URL": "url",
    "Date Published": "date_published",
    "Companies": "companies",
    "Topics": "topics",
    "Business Events": "business_events",
    "Themes": "themes",
    "Custom Topics": "custom_topics",
    "Industries": "industries",
    "Type of Source": "type_of_source",
    "Type of Content": "type_of_content",
    "Sources": "sources",
    "Locations": "locations",
    "Content Languages": "content_languages",
    "UUID": "uuid",
    "Image URL": "image_url"
}

# Table creation SQL
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS news_articles (
    title TEXT,
    lead_paragraph TEXT,
    url TEXT UNIQUE,
    date_published TEXT,
    companies TEXT,
    topics TEXT,
    business_events TEXT,
    themes TEXT,
    custom_topics TEXT,
    industries TEXT,
    type_of_source TEXT,
    type_of_content TEXT,
    sources TEXT,
    locations TEXT,
    content_languages TEXT,
    uuid UUID PRIMARY KEY,
    image_url TEXT
);
"""
def parse_date(date_str):
    """Try multiple date formats and return a valid datetime object."""
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d"]  # Add other formats if needed
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}")  # Log and handle invalid dates

def validate_uuid(uuid_str):
    """Ensure the UUID is valid, otherwise generate a new one."""
    uuid_str = uuid_str.strip()  # Remove extra spaces

    # Check if it's a valid UUID pattern (8-4-4-4-12)
    uuid_pattern = re.compile(r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$")

    if uuid_pattern.match(uuid_str):
        return uuid_str  # Return if valid

    new_uuid = str(uuid.uuid4())  # Generate a new valid UUID
    logger.warning(f"Replacing invalid UUID '{uuid_str}' with '{new_uuid}'")
    return new_uuid

# Fetch data by Business Events
@router.get("/business-events", tags=["Business Events"])
async def get_news_by_events(business_events: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.business_events.ilike(f"%{business_events}%"))
    result = await db.scalars(stmt)  # Use scalars() for async query execution
    return result.all()


# Fetch data by Company
@router.get("/search-company", tags=["Company"])
async def get_news_by_company(companies: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.companies.ilike(f"%{companies}%"))
    result = await db.scalars(stmt)
    return result.all()


# Fetch data by Industry
@router.get("/industries", tags=["Industry"])
async def get_news_by_industries(industries: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.industries.ilike(f"%{industries}%"))
    result = await db.scalars(stmt)
    return result.all()


# Fetch data by Language
@router.get("/language", tags=["Language"])
async def get_news_by_language(language: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.language.ilike(f"%{language}%"))
    result = await db.scalars(stmt)
    return result.all()


# Fetch data by Location
@router.get("/location", tags=["Location"])
async def get_news_by_location(location: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.location.ilike(f"%{location}%"))
    result = await db.scalars(stmt)
    return result.all()


# Fetch data by Source
@router.get("/source", tags=["Source"])
async def get_news_by_source(source: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.source.ilike(f"%{source}%"))
    result = await db.scalars(stmt)
    return result.all()


# Fetch data by Themes
@router.get("/themes", tags=["Themes"])
async def get_news_by_themes(themes: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.themes.ilike(f"%{themes}%"))
    result = await db.scalars(stmt)
    return result.all()


# Fetch data by Topics
@router.get("/topics", tags=["Topics"])
async def get_news_by_topics(topics: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.topics.ilike(f"%{topics}%"))
    result = await db.scalars(stmt)
    return result.all()


# Fetch data by Custom Topics
@router.get("/custom_topics", tags=["Topics"])
async def get_news_by_custom_topics(custom_topics: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.custom_topics.ilike(f"%{custom_topics}%"))
    result = await db.scalars(stmt)
    return result.all()


# Fetch data by Type of Content
@router.get("/type_of_content", tags=["Type Of Content"])
async def get_news_by_type_of_content(type_of_content: str, db: AsyncSession = Depends(get_async_db)):
    stmt = select(NewsArticle).filter(NewsArticle.type_of_content.ilike(f"%{type_of_content}%"))
    result = await db.scalars(stmt)
    return result.all()


# CSV Upload Endpoint
@router.post("/upload", tags=["Data Upload"])
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload CSV data to PostgreSQL. If the table does not exist, create it first.
    """
    try:
        # Read CSV file content
        csv_content = await file.read()
        csv_text = csv_content.decode("utf-8", errors="ignore")

        # Parse CSV content
        csv_reader = csv.reader(StringIO(csv_text))
        headers = next(csv_reader, None)  # Extract headers
        records = [row for row in csv_reader if row]  # Filter empty rows

        if not records:
            raise HTTPException(status_code=400, detail="CSV file is empty or invalid format.")

        # Validate column headers (case-insensitive comparison)
        cleaned_headers = [h.strip().lower().replace(" ", "_") for h in headers]
        expected_cleaned = [col.lower() for col in EXPECTED_COLUMNS]

        if cleaned_headers != expected_cleaned:
            raise HTTPException(status_code=400, detail=f"CSV columns do not match expected format: {EXPECTED_COLUMNS}")

        # Convert records (fix date format & UUID)
        processed_records = []
        for row in records:
            try:
                # row[3] = stparse_date(row[3])  # Convert `date_published`
                row[15] = validate_uuid(row[15])  # Validate & replace `uuid`
                processed_records.append(tuple(row))  # Convert to tuple for asyncpg
            except ValueError as e:
                logger.error(str(e))
                raise HTTPException(status_code=400, detail=str(e))
        # Connect to PostgreSQL
        conn = await asyncpg.connect(DATABASE_URL)

        try:
            # Ensure table exists before inserting
            await conn.execute(CREATE_TABLE_SQL)

            # Create a temporary table to hold new records
            await conn.execute("""
                CREATE TEMP TABLE temp_news_articles AS 
                SELECT * FROM news_articles WITH NO DATA;
            """)

            # Use COPY FROM STDIN to load data into the temporary table
            async with conn.transaction():
                await conn.copy_records_to_table("temp_news_articles", records=records, columns=EXPECTED_COLUMNS)

                # Insert into the actual table, ignoring duplicates
                insert_query = f"""
                        INSERT INTO news_articles ({', '.join(EXPECTED_COLUMNS)})
                        SELECT {', '.join(EXPECTED_COLUMNS)}
                        FROM temp_news_articles
                        ON CONFLICT (url) DO NOTHING;
                    """
                await conn.execute(insert_query)

                return {"message": "CSV uploaded successfully. Duplicates ignored."}

        finally:
            await conn.close()

    except ValueError as ve:
        logger.error(f"Invalid data format: {ve}")
        raise HTTPException(status_code=400, detail=f"Invalid data format: {ve}")

    except Exception as e:
        logger.error(f"CSV upload failed: {e}")
        raise HTTPException(status_code=500, detail="Error during CSV upload")