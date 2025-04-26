# api/routers/themes.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from api.core.security import verify_api_key
from api.services.metadata_service import MetadataService
from util.database import get_async_db
from api.models import ThemesTaxonomy

router = APIRouter(prefix="/themes", tags=["Themes"])

@router.get("/")
async def get_themes(
    themes: Optional[str] = Query(None, description="Filter by themes"),
    db: AsyncSession = Depends(get_async_db),
    api_key: str = Depends(verify_api_key)
):
    service = MetadataService(db)
    return await service.get_all_metadata(ThemesTaxonomy, "themes", themes)