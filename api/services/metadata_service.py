# api/services/metadata_service.py
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, join, and_
from typing import Optional, Type, Any, Dict
from api.core.cache import cache_response
from api.models import InsightWire, IndustryMapping, BusinessActivityMapping, CompanyMapping, ContentTypeMapping, LocationMapping, SentimentMapping, SourceTypeMapping  
from sqlalchemy import String, Integer, DateTime
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetadataService:
    def __init__(self, db: AsyncSession):
        self.db = db
        # Define valid values for each filter type based on taxonomy files
        self.valid_values = {
            'sentiment_type_id': [-1, 0, 1],  # Sentiment values: negative, neutral, positive
            'business_activity_id': range(100, 135),  # Business activity IDs: 100-134
            'company_id': range(10000000, 10123992),  # Company IDs: 10000000-10123991
            'content_type_id': range(401, 438),  # Content type IDs: 401-437
            'industry_type_id': range(300, 422),  # Industry IDs: 300-421
            'location_id': range(300, 438),  # Location IDs: 300-437
            'source_type_id': range(900, 907),  # Source type IDs: 900-906
        }
        
        # Map plural filter names to their singular forms
        self.filter_name_mapping = {
            'company_ids': 'company_id',
            'business_activity_ids': 'business_activity_id',
            'content_type_ids': 'content_type_id',
            'industry_type_ids': 'industry_type_id',
            'location_ids': 'location_id',
            'source_type_ids': 'source_type_id',
            'sentiment_type_ids': 'sentiment_type_id'
        }

        # Define valid filter parameters
        self.valid_filters = set([
            'company_id', 'company_ids',
            'business_activity_id', 'business_activity_ids',
            'content_type_id', 'content_type_ids',
            'industry_type_id', 'industry_type_ids',
            'location_id', 'location_ids',
            'source_type_id', 'source_type_ids',
            'sentiment_type_id', 'sentiment_type_ids',
            'page', 'limit'
        ])

        # Define pagination parameters
        self.pagination_params = {'page', 'limit'}

    def validate_filter_value(self, filter_name: str, value: Any) -> tuple[bool, str]:
        """
        Validate if the filter value is valid for the given filter type.
        Returns (is_valid, error_message)
        """
        # Convert plural form to singular if needed
        actual_filter_name = self.filter_name_mapping.get(filter_name, filter_name)
        
        if actual_filter_name not in self.valid_values:
            return True, ""  # No validation for unknown filters
        
        try:
            value = int(value)  # Convert to integer for ID fields
            if value not in self.valid_values[actual_filter_name]:
                valid_values = list(self.valid_values[actual_filter_name])
                if len(valid_values) > 10:  # If there are too many values, show range instead
                    min_val = min(valid_values)
                    max_val = max(valid_values)
                    return False, f"Invalid {filter_name}. Valid values are between {min_val} and {max_val} inclusive."
                return False, f"Invalid {filter_name}. Valid values are: {valid_values}"
            return True, ""
        except ValueError:
            return False, f"Invalid {filter_name}. Must be a valid integer."

    async def paginate_query(self, stmt, page: int, limit: int):
        try:
            # Ensure page and limit are positive
            page = max(1, page)  # Ensure page is at least 1
            limit = max(1, min(100, limit))  # Ensure limit is between 1 and 100
            
            # Get total count
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total_count = await self.db.scalar(count_stmt)
            
            if total_count == 0:
                return {
                    "total_count": 0,
                    "page": page,
                    "limit": limit,
                    "prev_page": None,
                    "next_page": None,
                    "data": [],
                    "message": "No records found matching the specified criteria"
                }
            
            # Calculate offset
            offset = (page - 1) * limit
            
            # If offset is greater than total count, return empty result
            if offset >= total_count:
                return {
                    "total_count": total_count,
                    "page": page,
                    "limit": limit,
                    "prev_page": page - 1 if page > 1 else None,
                    "next_page": None,
                    "data": [],
                    "message": "No records found for the specified page"
                }
            
            # Get paginated results
            offset_stmt = stmt.offset(offset).limit(limit)
            results = await self.db.scalars(offset_stmt)
            records = results.all()

            return {
                "total_count": total_count,
                "page": page,
                "limit": limit,
                "prev_page": page - 1 if page > 1 else None,
                "next_page": page + 1 if (page * limit) < total_count else None,
                "data": records,
                "message": f"Found {total_count} records"
            }
        except Exception as e:
            logger.error(f"Error in paginate_query: {str(e)}")
            return {
                "total_count": 0,
                "page": page,
                "limit": limit,
                "prev_page": None,
                "next_page": None,
                "data": [],
                "message": f"Error retrieving records: {str(e)}"
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
        try:
            stmt = select(model)
            if value:
                stmt = stmt.filter(getattr(model, field).ilike(f"%{value}%"))
            results = await self.db.scalars(stmt)
            records = results.all()
            
            if not records:
                return {
                    "total_count": 0,
                    "data": [],
                    "message": "No records found matching the specified criteria"
                }
                
            return {
                "total_count": len(records),
                "data": records,
                "message": "Records found successfully"
            }
        except Exception as e:
            return {
                "total_count": 0,
                "data": [],
                "message": f"Error retrieving records: {str(e)}"
            }
    
    @cache_response()
    async def get_news_insights(self, **kwargs):
        try:
            # Check if any valid filter is provided (excluding pagination parameters)
            has_valid_filter = False
            for key, value in kwargs.items():
                if key in self.valid_filters and key not in self.pagination_params and value is not None:
                    has_valid_filter = True
                    break

            if not has_valid_filter:
                return {
                    "total_count": 0,
                    "page": kwargs.get('page', 1),
                    "limit": kwargs.get('limit', 20),
                    "prev_page": None,
                    "next_page": None,
                    "data": [],
                    "message": "At least one filter parameter is required. Valid filters are: company_id(s), business_activity_id(s), content_type_id(s), industry_type_id(s), location_id(s), source_type_id(s), sentiment_type_id(s)"
                }

            # Validate filter values first
            for key, value in kwargs.items():
                if value is not None and key not in self.pagination_params:
                    # Convert plural form to singular if needed
                    actual_key = self.filter_name_mapping.get(key, key)
                    if actual_key in self.valid_values:
                        is_valid, error_message = self.validate_filter_value(key, value)
                        if not is_valid:
                            return {
                                "total_count": 0,
                                "page": kwargs.get('page', 1),
                                "limit": kwargs.get('limit', 20),
                                "prev_page": None,
                                "next_page": None,
                                "data": [],
                                "message": error_message
                            }

            # Start with base query
            stmt = select(InsightWire)

            # Track joined tables to avoid duplicate joins
            joined_tables = set()
            
            # Handle business_activity_id filter
            if kwargs.get('business_activity_id') or kwargs.get('business_activity_ids'):
                value = kwargs.get('business_activity_id') or kwargs.get('business_activity_ids')
                if 'business_activity_mapping' not in joined_tables:
                    stmt = stmt.join(BusinessActivityMapping, InsightWire.uuid == BusinessActivityMapping.insightwire_uuid)
                    joined_tables.add('business_activity_mapping')
                stmt = stmt.filter(BusinessActivityMapping.business_activity_id == value)
            
            # Handle company_id filter
            if kwargs.get('company_id') or kwargs.get('company_ids'):
                value = kwargs.get('company_id') or kwargs.get('company_ids')
                if 'company_mapping' not in joined_tables:
                    stmt = stmt.join(CompanyMapping, InsightWire.uuid == CompanyMapping.insightwire_uuid)
                    joined_tables.add('company_mapping')
                stmt = stmt.filter(CompanyMapping.company_id == value)
                
            # Handle content_type_id filter
            if kwargs.get('content_type_id') or kwargs.get('content_type_ids'):
                value = kwargs.get('content_type_id') or kwargs.get('content_type_ids')
                if 'content_type_mapping' not in joined_tables:
                    stmt = stmt.join(ContentTypeMapping, InsightWire.uuid == ContentTypeMapping.insightwire_uuid)
                    joined_tables.add('content_type_mapping')
                stmt = stmt.filter(ContentTypeMapping.content_type_id == value)
            
            # Handle industry_type_id filter
            if kwargs.get('industry_type_id') or kwargs.get('industry_type_ids'):
                value = kwargs.get('industry_type_id') or kwargs.get('industry_type_ids')
                if 'industry_mapping' not in joined_tables:
                    stmt = stmt.join(IndustryMapping, InsightWire.uuid == IndustryMapping.insightwire_uuid)
                    joined_tables.add('industry_mapping')
                stmt = stmt.filter(IndustryMapping.industry_type_id == value)
            
            # Handle location_id filter
            if kwargs.get('location_id') or kwargs.get('location_ids'):
                value = kwargs.get('location_id') or kwargs.get('location_ids')
                if 'location_mapping' not in joined_tables:
                    stmt = stmt.join(LocationMapping, InsightWire.uuid == LocationMapping.insightwire_uuid)
                    joined_tables.add('location_mapping')
                stmt = stmt.filter(LocationMapping.location_id == value)            

            # Handle sentiment_type_id filter
            if kwargs.get('sentiment_type_id') or kwargs.get('sentiment_type_ids'):
                value = kwargs.get('sentiment_type_id') or kwargs.get('sentiment_type_ids')
                if 'sentiment_mapping' not in joined_tables:
                    stmt = stmt.join(SentimentMapping, InsightWire.uuid == SentimentMapping.insightwire_uuid)
                    joined_tables.add('sentiment_mapping')
                stmt = stmt.filter(SentimentMapping.sentiment_type_id == value)       
            
            # Handle source_type_id filter
            if kwargs.get('source_type_id') or kwargs.get('source_type_ids'):
                value = kwargs.get('source_type_id') or kwargs.get('source_type_ids')
                if 'source_type_mapping' not in joined_tables:
                    stmt = stmt.join(SourceTypeMapping, InsightWire.uuid == SourceTypeMapping.insightwire_uuid)
                    joined_tables.add('source_type_mapping')
                stmt = stmt.filter(SourceTypeMapping.source_type_id == value)

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
                            return {
                                "total_count": 0,
                                "page": kwargs.get('page', 1),
                                "limit": kwargs.get('limit', 20),
                                "prev_page": None,
                                "next_page": None,
                                "data": [],
                                "message": f"Invalid integer value for field '{field}'"
                            }
                    else:
                        stmt = stmt.filter(column == value)

            # Pagination
            page = max(1, kwargs.get('page', 1))  # Ensure page is at least 1
            limit = max(1, min(100, kwargs.get('limit', 20)))  # Ensure limit is between 1 and 100
            
            # Get results
            result = await self.paginate_query(stmt, page, limit)
            
            # If no records found, provide a more specific message
            if result["total_count"] == 0:
                filters = []
                for key, value in kwargs.items():
                    if value is not None and key not in self.pagination_params:
                        filters.append(f"{key}={value}")
                
                if filters:
                    result["message"] = f"No records found matching the following criteria: {', '.join(filters)}"
                else:
                    result["message"] = "No records found in the database"
            
            return result
            
        except Exception as e:
            logger.error(f"Error in get_news_insights: {str(e)}")
            return {
                "total_count": 0,
                "page": kwargs.get('page', 1),
                "limit": kwargs.get('limit', 20),
                "prev_page": None,
                "next_page": None,
                "data": [],
                "message": f"Error retrieving records: {str(e)}"
            }
