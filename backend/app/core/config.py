"""
Configuration module for ProfitPilot AI Pro.
Loads environment variables and provides application settings.
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings class.
    Loads configuration from environment variables with defaults.
    """
    
    # Application settings
    APP_NAME: str = Field(default="ProfitPilot AI Pro", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    DEBUG: bool = Field(default=True, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # MongoDB settings
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        env="MONGODB_URL"
    )
    MONGODB_DB_NAME: str = Field(default="profitpilot_db", env="MONGODB_DB_NAME")
    
    # JWT Security settings
    SECRET_KEY: str = Field(
        default="your-super-secret-key-change-this-in-production-min-32-characters",
        env="SECRET_KEY"
    )
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ORIGINS"
    )
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="app.log", env="LOG_FILE")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Create a singleton instance of settings
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency injection function to get settings.
    
    Returns:
        Settings: Application settings instance
    """
    return settings