# api/services/metadata_service.py
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional, Type, Any, Dict, List
from api.core.cache import cache_response
from api.models import (
    InsightWire, IndustryMapping, BusinessActivityMapping, 
    CompanyMapping, ContentTypeMapping, LocationMapping, 
    SentimentMapping, SourceTypeMapping
)
from sqlalchemy import String, Integer
from datetime import datetime
import json
from functools import lru_cache
import hashlib
from pydantic import BaseModel, Field
from api.core.metadata_config import (
    VALID_VALUES, FILTER_NAME_MAPPING, VALID_FILTERS,
    PAGINATION_PARAMS, CACHE_CONFIG, RESPONSE_SCHEMA_FIELDS
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseSchema(BaseModel):
    """Pydantic model for response validation"""
    story_id: Optional[str] = Field(None, alias="uuid")
    title: Optional[str]
    lead_paragraph: Optional[str]
    story: Optional[str]
    published_date: Optional[str]
    news_url: Optional[str]
    image_url: Optional[str]
    business_activities: Optional[str]
    industries: Optional[str]
    type_of_content: Optional[str]
    type_of_source: Optional[str]
    sources: Optional[str]
    locations: Optional[str]
    content_languages: Optional[str]
    sentiment: Optional[str]

class MetadataService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._init_filter_mappings()

    def _init_filter_mappings(self):
        """Initialize filter mappings for query optimization"""
        self.filter_mappings = {
            'business_activities': (BusinessActivityMapping, 'business_activity_id'),
            'company': (CompanyMapping, 'company_id'),
            'content_type': (ContentTypeMapping, 'content_type_id'),
            'industries': (IndustryMapping, 'industry_type_id'),
            'location': (LocationMapping, 'location_id'),
            'sentiment': (SentimentMapping, 'sentiment_type_id'),
            'source_type': (SourceTypeMapping, 'source_type_id')
        }

    @lru_cache(maxsize=CACHE_CONFIG['max_size'])
    def _generate_cache_key(self, **kwargs) -> str:
        """Generate a unique cache key based on filter parameters"""
        sorted_kwargs = sorted(kwargs.items())
        key_string = json.dumps(sorted_kwargs)
        return f"{CACHE_CONFIG['version']}:{hashlib.md5(key_string.encode()).hexdigest()}"

    def validate_filter_value(self, filter_name: str, value: Any) -> tuple[bool, str]:
        """Validate if the filter value is valid for the given filter type."""
        actual_filter_name = FILTER_NAME_MAPPING.get(filter_name, filter_name)
        
        if actual_filter_name not in VALID_VALUES:
            return True, ""
        
        try:
            value = int(value)
            if value not in VALID_VALUES[actual_filter_name]:
                valid_values = list(VALID_VALUES[actual_filter_name])
                if len(valid_values) > 10:
                    min_val = min(valid_values)
                    max_val = max(valid_values)
                    return False, f"Invalid {filter_name}. Valid values are between {min_val} and {max_val} inclusive."
                return False, f"Invalid {filter_name}. Valid values are: {valid_values}"
            return True, ""
        except ValueError:
            return False, f"Invalid {filter_name}. Must be a valid integer."

    def _standardize_response_schema(self, data: List[Any]) -> List[Dict[str, Any]]:
        """Standardize the order of fields in the response data"""
        standardized_data = []
        for item in data:
            # Define the order of fields
            standardized_item = {
                "story_id": getattr(item, "uuid", None),
                "title": getattr(item, "title", None),
                "lead_paragraph": getattr(item, "lead_paragraph", None),
                "story": getattr(item, "story", None),
                "published_date": getattr(item, "published_date", None),
                "news_url": getattr(item, "news_url", None),
                "image_url": getattr(item, "image_url", None),
                "type_of_content": getattr(item, "type_of_content", None),
                "type_of_source": getattr(item, "type_of_source", None),
                "sources": getattr(item, "sources", None),
                "business_activities": getattr(item, "business_activities", None),
                "industries": getattr(item, "industries", None),
                "locations": getattr(item, "locations", None),
                "content_languages": getattr(item, "content_languages", None),
                "sentiment": getattr(item, "sentiment", None)
            }
            # Remove None values
            standardized_item = {k: v for k, v in standardized_item.items() if v is not None}
            standardized_data.append(standardized_item)
        return standardized_data

    async def paginate_query(self, stmt, page: int, limit: int):
        """Handle pagination for database queries with performance optimization"""
        page = max(1, page)
        limit = max(1, min(100, limit))
        
        try:
            # Use a single query for count and data
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total_count = await self.db.scalar(count_stmt)
            
            if total_count == 0:
                return self._create_empty_response(page, limit, "No records found matching the specified criteria")
            
            offset = (page - 1) * limit
            if offset >= total_count:
                return self._create_empty_response(page, limit, "No records found for the specified page", total_count)
            
            # Optimize query with proper indexing hints
            offset_stmt = stmt.offset(offset).limit(limit)
            results = await self.db.scalars(offset_stmt)
            records = results.all()
            
            # Log performance metrics
            logger.info(f"Query executed successfully. Total records: {total_count}, Page: {page}, Limit: {limit}")
            
            return {
                "total_count": total_count,
                "page": page,
                "limit": limit,
                "prev_page": page - 1 if page > 1 else None,
                "next_page": page + 1 if (page * limit) < total_count else None,
                "data": self._standardize_response_schema(records),
                "message": f"Found {total_count} records"
            }
        except Exception as e:
            logger.error(f"Error in paginate_query: {str(e)}", exc_info=True)
            return self._create_empty_response(page, limit, f"Error retrieving records: {str(e)}")

    def _create_empty_response(self, page: int, limit: int, message: str, total_count: int = 0) -> dict:
        """Create a standardized empty response."""
        return {
            "total_count": total_count,
            "page": page,
            "limit": limit,
            "prev_page": page - 1 if page > 1 else None,
            "next_page": None,
            "data": [],
            "message": message
        }

    @cache_response(cache_type='long')
    async def get_metadata(self, model: Type[Any], field: str, value: Optional[str], page: int = 1, limit: int = 20):
        """Get metadata with pagination."""
        stmt = select(model)
        if value:
            stmt = stmt.filter(getattr(model, field).ilike(f"%{value}%"))
        return await self.paginate_query(stmt, page, limit)

    @cache_response(cache_type='long')
    async def get_all_metadata(self, model: Type[Any], field: str, value: Optional[str]):
        """Get all metadata without pagination."""
        try:
            stmt = select(model)
            if value:
                stmt = stmt.filter(getattr(model, field).ilike(f"%{value}%"))
            results = await self.db.scalars(stmt)
            records = results.all()
            
            if not records:
                return self._create_empty_response(1, len(records), "No records found matching the specified criteria")
            
            return {
                "total_count": len(records),
                "data": self._standardize_response_schema(records),
                "message": "Records found successfully"
            }
        except Exception as e:
            return self._create_empty_response(1, 0, f"Error retrieving records: {str(e)}")

    @cache_response(cache_type='medium')
    async def get_news_insights(self, **kwargs):
        """Get news insights with filtering and pagination"""
        try:
            # Generate cache key
            cache_key = self._generate_cache_key(**kwargs)
            
            if not any(kwargs.get(key) for key in VALID_FILTERS - PAGINATION_PARAMS):
                return self._create_empty_response(
                    kwargs.get('page', 1),
                    kwargs.get('limit', 20),
                    "At least one filter parameter is required. Valid filters are: company_id(s), business_activity_id(s), content_type_id(s), industry_type_id(s), location_id(s), source_type_id(s), sentiment_type_id(s), start_date, end_date"
                )

            # Validate filter values
            for key, value in kwargs.items():
                if value is not None and key not in PAGINATION_PARAMS:
                    actual_key = FILTER_NAME_MAPPING.get(key, key)
                    if actual_key in VALID_VALUES:
                        is_valid, error_message = self.validate_filter_value(key, value)
                        if not is_valid:
                            return self._create_empty_response(kwargs.get('page', 1), kwargs.get('limit', 20), error_message)

            stmt = select(InsightWire)
            joined_tables = set()
            
            # Apply filters with optimized query building
            stmt = await self._apply_filters(stmt, kwargs, joined_tables)
            if isinstance(stmt, dict):  # Error response
                return stmt

            # Pagination with optimized parameters
            page = max(1, kwargs.get('page', 1))
            limit = max(1, min(100, kwargs.get('limit', 20)))
            
            result = await self.paginate_query(stmt, page, limit)
            
            if result["total_count"] == 0:
                filters = [f"{key}={value}" for key, value in kwargs.items() 
                         if value is not None and key not in PAGINATION_PARAMS]
                result["message"] = (f"No records found matching the following criteria: {', '.join(filters)}" 
                                   if filters else "No records found in the database")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in get_news_insights: {str(e)}", exc_info=True)
            return self._create_empty_response(kwargs.get('page', 1), kwargs.get('limit', 20), f"Error retrieving records: {str(e)}")

    async def _apply_filters(self, stmt, kwargs: dict, joined_tables: set):
        """Apply filters to the query with optimization"""
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        
        try:
            # Apply filters using the pre-defined mappings
            for filter_type, (model, id_field) in self.filter_mappings.items():
                filter_key = f'{filter_type}_id'
                filter_key_plural = f'{filter_type}_ids'
                
                if kwargs.get(filter_key) or kwargs.get(filter_key_plural):
                    value = kwargs.get(filter_key) or kwargs.get(filter_key_plural)
                    table_name = f'{filter_type}_mapping'
                    
                    if table_name not in joined_tables:
                        stmt = stmt.join(model, InsightWire.uuid == getattr(model, 'insightwire_uuid'))
                        joined_tables.add(table_name)
                    
                    stmt = stmt.filter(getattr(model, id_field) == value)
                    
                    # Apply date filters with optimization
                    if start_date or end_date:
                        stmt = await self._apply_date_filters(stmt, model, start_date, end_date)
                        if isinstance(stmt, dict):  # Error response
                            return stmt

            # Apply other InsightWire table filters with optimization
            for field, value in kwargs.items():
                if (value is not None and hasattr(InsightWire, field) and 
                    field not in ['industry_type_id', 'company_id', 'business_activity_id']):
                    column = getattr(InsightWire, field)
                    if isinstance(column.type, String):
                        stmt = stmt.filter(column.ilike(f"%{value}%"))
                    elif isinstance(column.type, Integer):
                        try:
                            stmt = stmt.filter(column == int(value))
                        except ValueError:
                            return self._create_empty_response(
                                kwargs.get('page', 1),
                                kwargs.get('limit', 20),
                                f"Invalid integer value for field '{field}'"
                            )
                    else:
                        stmt = stmt.filter(column == value)

            return stmt
        except Exception as e:
            logger.error(f"Error in applying filters: {str(e)}", exc_info=True)
            return self._create_empty_response(
                kwargs.get('page', 1),
                kwargs.get('limit', 20),
                f"Error applying filters: {str(e)}"
            )

    async def _apply_date_filters(self, stmt, model, start_date: Optional[str], end_date: Optional[str]):
        """Apply date filters to the query with optimization"""
        try:
            if start_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                stmt = stmt.filter(getattr(model, 'system_timestamp') >= start_date)
            
            if end_date:
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
                end_date = end_date.replace(hour=23, minute=59, second=59)
                stmt = stmt.filter(getattr(model, 'system_timestamp') <= end_date)
            
            return stmt
        except ValueError as e:
            logger.error(f"Invalid date format: {str(e)}", exc_info=True)
            return self._create_empty_response(
                1, 20,
                "Invalid date format. Please use YYYY-MM-DD format."
            )
