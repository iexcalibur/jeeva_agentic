"""Configuration management using Pydantic Settings"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    DATABASE_TYPE: str = "sqlite"  # "sqlite" or "postgresql"
    
    # PostgreSQL Configuration (for Docker mode)
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "chatbot_user"
    POSTGRES_PASSWORD: str = "chatbot_pass"
    POSTGRES_DB: str = "chatbot_db"
    
    # SQLite Configuration (for Dev mode)
    SQLITE_DB_PATH: str = "chatbot.db"
    
    # Cache Configuration
    CACHE_TYPE: str = "memory"  # "memory" or "redis"
    
    # Redis Configuration (for Docker mode)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # Anthropic API
    ANTHROPIC_API_KEY: str
    
    # Application Settings
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Auto-detect mode based on environment
        if os.getenv("USE_DOCKER", "").lower() == "true" or os.getenv("DATABASE_TYPE") == "postgresql":
            self.DATABASE_TYPE = "postgresql"
            self.CACHE_TYPE = "redis"
            if not self.DATABASE_URL:
                self.DATABASE_URL = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        else:
            # Dev mode: SQLite + in-memory cache
            self.DATABASE_TYPE = "sqlite"
            self.CACHE_TYPE = "memory"
            if not self.DATABASE_URL:
                self.DATABASE_URL = f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

