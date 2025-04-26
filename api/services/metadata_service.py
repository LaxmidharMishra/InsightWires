# api/services/metadata_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional, Type, Any
from api.core.cache import cache_response
from api.models import NewsMetadata

class MetadataService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def paginate_query(self, stmt, page: int, limit: int):
        total_count = await self.db.scalar(
            select(func.count()).select_from(stmt.subquery())
        )
        
        offset_stmt = stmt.offset((page - 1) * limit).limit(limit)
        results = await self.db.scalars(offset_stmt)

        return {
            "total_count": total_count,
            "page": page,
            "limit": limit,
            "prev_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if (page * limit) < total_count else None,
            "data": results.all(),
        }

    @cache_response()
    async def get_metadata(
        self, 
        model: Type[Any], 
        field: str, 
        value: Optional[str], 
        page: int = 1, 
        limit: int = 20
    ):
        stmt = select(model)
        if value:
            stmt = stmt.filter(getattr(model, field).ilike(f"%{value}%"))
        return await self.paginate_query(stmt, page, limit)

    @cache_response()
    async def get_all_metadata(
        self, 
        model: Type[Any], 
        field: str, 
        value: Optional[str]
    ):
        """
        Get all metadata without pagination
        """
        stmt = select(model)
        if value:
            stmt = stmt.filter(getattr(model, field).ilike(f"%{value}%"))
        results = await self.db.scalars(stmt)
        records = results.all()
        return {
            "total_count": len(records),
            "data": records
        }

    @cache_response()
    async def get_news_insights(self, **kwargs):
        stmt = select(NewsMetadata)
        
        # Apply filters
        for field, value in kwargs.items():
            if value is not None and hasattr(NewsMetadata, field):
                stmt = stmt.filter(getattr(NewsMetadata, field).ilike(f"%{value}%"))

        # Get paginated results
        page = kwargs.get('page', 1)
        limit = kwargs.get('limit', 20)
        return await self.paginate_query(stmt, page, limit)