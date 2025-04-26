# api/routers/news.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from api.core.security import verify_api_key
from api.services.metadata_service import MetadataService
from util.database import get_async_db

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/insight")
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
    api_key: str = Depends(verify_api_key)
):
    service = MetadataService(db)
    return await service.get_news_insights(
        uuid=uuid,
        company_id=company_id,
        title=title,
        published_date=published_date,
        companies=companies,
        business_events=business_events,
        custom_topics=custom_topics,
        industries=industries,
        sentiment=sentiment,
        type_of_source=type_of_source,
        type_of_content=type_of_content,
        sources=sources,
        story=story,
        locations=locations,
        content_languages=content_languages,
        image_url=image_url,
        page=page,
        limit=limit
    )