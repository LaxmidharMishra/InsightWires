# api/routers/news.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from api.core.security import verify_api_key
from api.services.metadata_service import MetadataService
from util.database import get_async_db

router = APIRouter(prefix="/insight", tags=["Insight"])

@router.get("/")
async def news_insight(
    # uuid: Optional[str] = None, 
    # lead_paragraph: Optional[str] = None,
    # news_url: Optional[str] = None,
    published_date: Optional[str] = None,
    # companies: Optional[str] = None,
    # business_activities: Optional[str] = None,
    # custom_topics: Optional[str] = None,
    # industries: Optional[str] = None,
    # sentiment: Optional[str] = None,
    # type_of_source: Optional[str] = None,
    # type_of_content: Optional[str] = None,
    # sources: Optional[str] = None,
    # story: Optional[str] = None,
    # locations: Optional[str] = None,
    # content_languages: Optional[str] = None,
    # image_url: Optional[str] = None,
    business_activity_id: Optional[str] = None,
    industry_type_id: Optional[int] = None,
    content_type_id: Optional[int] = None,
    source_type_id: Optional[int] = None,
    sentiment_type_id: Optional[int] = None,
    location_ids: Optional[str] = None,
    company_ids: Optional[str] = None,
    system_timestamp: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Depends(verify_api_key)
):
    service = MetadataService(db)
    return await service.get_news_insights(
        # uuid=uuid,  
        # lead_paragraph=lead_paragraph,
        # news_url=news_url,
        published_date=published_date,
        # companies=companies,
        # business_activities=business_activities,
        # custom_topics=custom_topics,
        # industries=industries,
        # sentiment=sentiment,
        # type_of_source=type_of_source,
        # type_of_content=type_of_content,
        # sources=sources,
        # story=story,
        # locations=locations,
        # content_languages=content_languages,
        # image_url=image_url
        business_activity_id=business_activity_id,
        industry_type_id=industry_type_id,
        content_type_id=content_type_id,
        source_type_id=source_type_id,
        sentiment_type_id=sentiment_type_id,
        location_ids=location_ids,
        company_ids=company_ids,
        system_timestamp=system_timestamp,
        page=page,
        limit=limit
    )