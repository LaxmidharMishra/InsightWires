# api/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional, Dict
from pydantic import Field, field_validator, ValidationInfo

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Insight Wires API"
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None

    # Security
    SECRET_KEY: str
    API_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    # Cache Configuration
    CACHE_CONFIG: Dict[str, int] = Field(
        default={
            'default_ttl': 300,  # 5 minutes
            'short_ttl': 60,     # 1 minute
            'medium_ttl': 300,   # 5 minutes
            'long_ttl': 3600,    # 1 hour
            'max_size': 1000
        },
        description="Cache configuration settings"
    )
    
    # Legacy cache TTL (will be converted to CACHE_CONFIG)
    CACHE_TTL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in environment variables

    @field_validator('CACHE_CONFIG', mode='after')
    def convert_cache_ttl(cls, v: Dict[str, int], info: ValidationInfo) -> Dict[str, int]:
        """Convert legacy CACHE_TTL to new CACHE_CONFIG format if present"""
        if hasattr(info.context, 'CACHE_TTL') and info.context.CACHE_TTL:
            try:
                ttl = int(info.context.CACHE_TTL)
                v['default_ttl'] = ttl
                v['medium_ttl'] = ttl
            except (ValueError, TypeError):
                pass
        return v

    def model_post_init(self, _context):
        # Move the DATABASE_URL construction to post_init
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        # Convert ALLOWED_ORIGINS string to list
        self.ALLOWED_ORIGINS = [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# For testing
if __name__ == "__main__":
    print(settings.dict())