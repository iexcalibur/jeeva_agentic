"""Configuration management using Pydantic Settings"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    DATABASE_URL: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "chatbot_user"
    POSTGRES_PASSWORD: str = "chatbot_pass"
    POSTGRES_DB: str = "chatbot_db"
    
    # Anthropic API
    ANTHROPIC_API_KEY: str
    
    # Application Settings
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

