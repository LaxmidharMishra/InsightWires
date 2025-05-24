"""Configuration settings for metadata service"""

# Valid values for filters
VALID_VALUES = {
    'sentiment_type_id': [-1, 0, 1],
    'business_activity_id': range(100, 135),
    'company_id': range(10000000, 10123992),
    'content_type_id': range(401, 438),
    'industry_type_id': range(300, 422),
    'location_id': range(300, 438),
    'source_type_id': range(900, 907),
}

# Filter name mappings
FILTER_NAME_MAPPING = {
    'company_ids': 'company_id',
    'business_activity_ids': 'business_activity_id',
    'content_type_ids': 'content_type_id',
    'industry_type_ids': 'industry_type_id',
    'location_ids': 'location_id',
    'source_type_ids': 'source_type_id',
    'sentiment_type_ids': 'sentiment_type_id'
}

# Valid filters
VALID_FILTERS = {
    'company_id', 'company_ids',
    'business_activity_id', 'business_activity_ids',
    'content_type_id', 'content_type_ids',
    'industry_type_id', 'industry_type_ids',
    'location_id', 'location_ids',
    'source_type_id', 'source_type_ids',
    'sentiment_type_id', 'sentiment_type_ids',
    'start_date', 'end_date',
    'page', 'limit'
}

# Pagination parameters
PAGINATION_PARAMS = {'page', 'limit'}

# Cache configuration
CACHE_CONFIG = {
    'ttl': 3600,  # 1 hour
    'version': '1.0',
    'max_size': 1000
}

# Response schema fields
RESPONSE_SCHEMA_FIELDS = [
    'uuid',
    'title',
    'lead_paragraph',
    'story',
    'published_date',
    'news_url',
    'image_url',
    'type_of_content',
    'type_of_source',
    'sources',
    'locations',
    'content_languages',
    'sentiment'
] 