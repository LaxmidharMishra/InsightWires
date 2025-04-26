# api/routers/topics.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from api.core.security import verify_api_key
from api.services.metadata_service import MetadataService
from util.database import get_async_db
from api.models import TopicsTaxonomy

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/")
async def get_topics(
    topics: Optional[str] = Query(None, description="Filter by topics"),
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Depends(verify_api_key)
):
    service = MetadataService(db)
    return await service.get_all_metadata(TopicsTaxonomy, "topics", topics)