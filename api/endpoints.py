import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from util.database import get_async_db  # Use async session
from sqlalchemy import func
from typing import Optional
from api.models import *
# from api.models import (
#     BusinessEventsMetadata,
#     CompaniesMetadata,
#     ContentsMetadata,
#     IndustriesMetadata,
#     LanguageMetadata,
#     LocationsMetadata,
#     NewsMetadata,
#     SourcesMetadata,
# )  # Ensure these ORM models exist


# Logging configuration
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("InsightWiresFastApi")

router = APIRouter()

# Pagination function
async def paginate_query(stmt, page: int, limit: int, db: AsyncSession):
    total_count = await db.scalar(select(func.count()).select_from(stmt.subquery()))
    offset_stmt = stmt.offset((page - 1) * limit).limit(limit)
    results = await db.scalars(offset_stmt)

    return {
        "total_count": total_count,
        "page": page,
        "limit": limit,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if (page * limit) < total_count else None,
        "data": results.all(),
    }

# Generic function to fetch data from any metadata table
async def fetch_metadata_data(metadata_model, field: str, value: Optional[str] | None, page: int, limit: int, db: AsyncSession):
    stmt = select(metadata_model)
    
    if value:  # Apply filtering if a value is provided
        stmt = stmt.filter(getattr(metadata_model, field).ilike(f"%{value}%"))

    return await paginate_query(stmt, page, limit, db)

# Fetch all records from the metadata table without pagination
async def fetch_all_metadata_data(metadata_model, field: str, value: Optional[str] | None, db: AsyncSession):
    stmt = select(metadata_model)
    
    try:
        if value:  # Apply filtering if a value is provided
            stmt = stmt.filter(getattr(metadata_model, field).ilike(f"%{value}%"))
    except AttributeError:
        logger.error(f"Field '{field}' does not exist in the model '{metadata_model.__tablename__}'.")
        raise HTTPException(status_code=400, detail=f"Invalid value for Business Activity: {value}")
    
    results = await db.scalars(stmt)
    records = results.all()

    return {
        "total_count": len(records),
        "data": records
    }


# Endpoints
@router.get("/search-company", tags=["Company"])
async def get_companies(
    companies: str | None = Query(None, description="Filter by company"),
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
):
    return await fetch_metadata_data(CompaniesMetadata, "companies", companies, page, limit, db)

@router.get("/industries", tags=["Industry"])
async def get_industries(
    industries: str | None = Query(None, description="Filter by industry"),
    db: AsyncSession = Depends(get_async_db),
):
    return await fetch_all_metadata_data(IndustriesTaxonomy, "industries", industries, db)

@router.get("/language", tags=["Language"])
async def get_languages(
    content_languages: str | None = Query(None, description="Filter by language"),
    db: AsyncSession = Depends(get_async_db),
):
    return await fetch_all_metadata_data(LanguageTaxonomy, "content_languages", content_languages, db)

@router.get("/location", tags=["Location"])
async def get_locations(
    locations: str | None = Query(None, description="Filter by location"),
    db: AsyncSession = Depends(get_async_db),
):
    return await fetch_all_metadata_data(LocationsTaxonomy, "locations", locations, db)

@router.get("/source", tags=["Source"])
async def get_sources(
    sources: str | None = Query(None, description="Filter by source"),
    db: AsyncSession = Depends(get_async_db),
):
    return await fetch_all_metadata_data(SourcesTaxonomy, "sources", sources, db)

@router.get("/themes", tags=["Themes"])
async def get_themes(
    themes: str | None = Query(None, description="Filter by themes"),
    db: AsyncSession = Depends(get_async_db),
):
    return await fetch_all_metadata_data(ThemesMetadata, "themes", themes, db)

@router.get("/topics", tags=["Topics"])
async def get_topics(
    topics: str | None = Query(None, description="Filter by topics"),
    db: AsyncSession = Depends(get_async_db),
):
    return await fetch_all_metadata_data(TopicsMetadata, "topics", topics, db)

@router.get("/custom_topics", tags=["Topics"])
async def get_custom_topics(
    custom_topics: str | None = Query(None, description="Filter by custom topics"),
    db: AsyncSession = Depends(get_async_db),
):
    return await fetch_metadata_data(CustomTopicsMetadata, "custom_topics", custom_topics, page, limit, db)

@router.get("/type_of_content", tags=["Type Of Content"])
async def get_type_of_content(
    type_of_content: str | None = Query(None, description="Filter by type of content"),
    db: AsyncSession = Depends(get_async_db),
):
    return await fetch_all_metadata_data(TypeOfContentMetadata, "type_of_content", type_of_content, db)

@router.get("/new_insight", tags=["News Search"])
async def new_insight(
    uuid: Optional[str] = None,
    company_id: Optional[str] = None,
    title: Optional[str] = None,
    published_date: Optional[str] = None,
    companies: Optional[str] = None,
    business_events: Optional[str] = None,
    custom_topics: Optional[str] = None,
    industries: Optional[str] = None,
    sentiment: Optional[str] = None,
    type_of_source: Optional[str] = None,
    type_of_content: Optional[str] = None,
    sources: Optional[str] = None,
    story: Optional[str] = None,
    locations: Optional[str] = None,
    content_languages: Optional[str] = None,
    image_url: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
):
    stmt = select(NewsMetadata)
    filters = {
        "uuid": uuid,
        "company_id": company_id,
        "title": title,
        "published_date": published_date,
        "companies": companies,
        "business_events": business_events,
        "custom_topics": custom_topics,
        "industries": industries,
        "sentiment": sentiment,
        "type_of_source": type_of_source,
        "type_of_content": type_of_content,
        "sources": sources,
        "story": story,
        "locations": locations,
        "content_languages": content_languages,
        "image_url": image_url
    }

    for field, value in filters.items():
        if value is not None:
            try:
                stmt = stmt.filter(getattr(NewsMetadata, field).ilike(f"%{value}%"))
            except AttributeError:
                raise HTTPException(status_code=400, detail=f"Field '{field}' is not valid.")

    return await paginate_query(stmt, page, limit, db)