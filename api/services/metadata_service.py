# api/services/metadata_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, join
from typing import Optional, Type, Any
from api.core.cache import cache_response
from api.models import InsightWire, IndustryMapping, BusinessActivityMapping, CompanyMapping, ContentTypeMapping, LocationMapping, SentimentMapping, SourceTypeMapping  
from sqlalchemy import String, Integer, DateTime
from fastapi import HTTPException


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
        # Start with base query
        stmt = select(InsightWire)

        # Track joined tables to avoid duplicate joins
        joined_tables = set()
        
        # Handle business_activity_id filter
        if kwargs.get('business_activity_id'):
            if 'business_activity_mapping' not in joined_tables:
                stmt = stmt.join(BusinessActivityMapping, InsightWire.uuid == BusinessActivityMapping.insightwire_uuid)
                joined_tables.add('business_activity_mapping')
            stmt = stmt.filter(BusinessActivityMapping.business_activity_id == kwargs['business_activity_id'])
        
        # Handle company_id filter
        if kwargs.get('company_id'):
            if 'company_mapping' not in joined_tables:
                stmt = stmt.join(CompanyMapping, InsightWire.uuid == CompanyMapping.insightwire_uuid)
                joined_tables.add('company_mapping')
            stmt = stmt.filter(CompanyMapping.company_id == kwargs['company_id'])
            
        # Handle content_type_id filter
        if kwargs.get('content_type_id'):
            if 'content_type_mapping' not in joined_tables:
                stmt = stmt.join(ContentTypeMapping, InsightWire.uuid == ContentTypeMapping.insightwire_uuid)
                joined_tables.add('content_type_mapping')
            stmt = stmt.filter(ContentTypeMapping.content_type_id == kwargs['content_type_id']) 
        
        # Handle industry_type_id filter
        if kwargs.get('industry_type_id'):
            if 'industry_mapping' not in joined_tables:
                stmt = stmt.join(IndustryMapping, InsightWire.uuid == IndustryMapping.insightwire_uuid)
                joined_tables.add('industry_mapping')
            stmt = stmt.filter(IndustryMapping.industry_type_id == kwargs['industry_type_id'])
        
        # Handle location_id filter
        if kwargs.get('location_id'):
            if 'location_mapping' not in joined_tables:
                stmt = stmt.join(LocationMapping, InsightWire.uuid == LocationMapping.insightwire_uuid)
                joined_tables.add('location_mapping')
            stmt = stmt.filter(LocationMapping.location_id == kwargs['location_id'])            

        # Handle sentiment_type_id filter
        if kwargs.get('sentiment_type_id'):
            if 'sentiment_mapping' not in joined_tables:
                stmt = stmt.join(SentimentMapping, InsightWire.uuid == SentimentMapping.insightwire_uuid)
                joined_tables.add('sentiment_mapping')
            stmt = stmt.filter(SentimentMapping.sentiment_type_id == kwargs['sentiment_type_id'])       
        
        # Handle source_type_id filter
        if kwargs.get('source_type_id'):
            if 'source_type_mapping' not in joined_tables:
                stmt = stmt.join(SourceTypeMapping, InsightWire.uuid == SourceTypeMapping.insightwire_uuid)
                joined_tables.add('source_type_mapping')
            stmt = stmt.filter(SourceTypeMapping.source_type_id == kwargs['source_type_id'])


           # Apply other InsightWire table filters dynamically
        for field, value in kwargs.items():
            if value is not None and hasattr(InsightWire, field) and field not in ['industry_type_id', 'company_id', 'business_activity_id']:
                column = getattr(InsightWire, field)
                if isinstance(column.type, String):
                    stmt = stmt.filter(column.ilike(f"%{value}%"))
                elif isinstance(column.type, Integer):
                    try:
                        stmt = stmt.filter(column == int(value))
                    except ValueError:
                        raise HTTPException(status_code=400, detail=f"Invalid integer value for field '{field}'")
                else:
                    stmt = stmt.filter(column == value)

        # Pagination
        page = kwargs.get('page', 1)
        limit = kwargs.get('limit', 20)
        return await self.paginate_query(stmt, page, limit)
