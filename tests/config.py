"""Test configuration settings"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'insightwiredb'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

# Test data configuration
TEST_DATA = {
    'taxonomies': [
        'business_events',
        'industries',
        'locations',
        'languages',
        'sources'
    ],
    'sample_size': 3
}

# Test API configuration
API_CONFIG = {
    'base_url': os.getenv('API_BASE_URL', 'http://localhost:8000'),
    'api_key': os.getenv('API_KEY', ''),
    'timeout': 30
} 