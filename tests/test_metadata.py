"""Test suite for metadata service"""

import pytest
from api.services.metadata_service import MetadataService
from api.core.metadata_config import VALID_VALUES, FILTER_NAME_MAPPING
from tests.config import DB_CONFIG, TEST_DATA
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Create test database engine
TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture
async def db_session():
    """Create a test database session"""
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
def metadata_service(db_session):
    """Create a metadata service instance"""
    return MetadataService(db_session)

@pytest.mark.asyncio
async def test_validate_filter_value(metadata_service):
    """Test filter value validation"""
    # Test valid values
    for filter_name, valid_values in VALID_VALUES.items():
        for value in valid_values:
            is_valid, message = metadata_service.validate_filter_value(filter_name, value)
            assert is_valid, f"Valid value {value} for {filter_name} was rejected"
            assert message == "", f"Unexpected message for valid value: {message}"

    # Test invalid values
    invalid_tests = [
        ('sentiment_type_id', 2),
        ('business_activity_id', 99),
        ('company_id', 9999999),
        ('content_type_id', 400),
        ('industry_type_id', 299),
        ('location_id', 299),
        ('source_type_id', 899)
    ]
    
    for filter_name, value in invalid_tests:
        is_valid, message = metadata_service.validate_filter_value(filter_name, value)
        assert not is_valid, f"Invalid value {value} for {filter_name} was accepted"
        assert message != "", f"No error message for invalid value"

@pytest.mark.asyncio
async def test_standardize_response_schema(metadata_service):
    """Test response schema standardization"""
    # Create test data
    test_data = [type('TestItem', (), {
        'uuid': 'test-uuid',
        'title': 'Test Title',
        'lead_paragraph': 'Test Lead',
        'story': 'Test Story',
        'published_date': '2024-01-01',
        'news_url': 'http://test.com',
        'image_url': 'http://test.com/image.jpg',
        'type_of_content': 'News',
        'type_of_source': 'Website',
        'sources': 'Test Source',
        'locations': 'Test Location',
        'content_languages': 'en',
        'sentiment': 'positive'
    })]

    # Test standardization
    result = metadata_service._standardize_response_schema(test_data)
    assert len(result) == 1
    assert result[0]['story_id'] == 'test-uuid'
    assert result[0]['title'] == 'Test Title'
    assert result[0]['lead_paragraph'] == 'Test Lead'
    assert result[0]['story'] == 'Test Story'
    assert result[0]['published_date'] == '2024-01-01'
    assert result[0]['news_url'] == 'http://test.com'
    assert result[0]['image_url'] == 'http://test.com/image.jpg'
    assert result[0]['type_of_content'] == 'News'
    assert result[0]['type_of_source'] == 'Website'
    assert result[0]['sources'] == 'Test Source'
    assert result[0]['locations'] == 'Test Location'
    assert result[0]['content_languages'] == 'en'
    assert result[0]['sentiment'] == 'positive'

@pytest.mark.asyncio
async def test_paginate_query(metadata_service):
    """Test query pagination"""
    # Test with empty result
    empty_result = await metadata_service.paginate_query(
        metadata_service.db.query(metadata_service.db.query().filter(False)),
        1, 10
    )
    assert empty_result['total_count'] == 0
    assert empty_result['data'] == []
    assert empty_result['message'] == "No records found matching the specified criteria"

    # Test with invalid page
    invalid_page = await metadata_service.paginate_query(
        metadata_service.db.query(),
        0, 10
    )
    assert invalid_page['page'] == 1  # Should be normalized to 1

    # Test with invalid limit
    invalid_limit = await metadata_service.paginate_query(
        metadata_service.db.query(),
        1, 0
    )
    assert invalid_limit['limit'] == 1  # Should be normalized to 1

    invalid_limit = await metadata_service.paginate_query(
        metadata_service.db.query(),
        1, 101
    )
    assert invalid_limit['limit'] == 100  # Should be normalized to 100 