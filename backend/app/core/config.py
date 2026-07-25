"""
Configuration module for ProfitPilot AI Pro.
Loads environment variables and provides application settings.
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings.
    """

    # =========================
    # Application
    # =========================
    APP_NAME: str = Field(default="ProfitPilot AI Pro", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    DEBUG: bool = Field(default=True, env="DEBUG")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")

    # =========================
    # Server
    # =========================
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")

    # =========================
    # MongoDB
    # =========================
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        env="MONGODB_URL"
    )

    MONGODB_DB_NAME: str = Field(
        default="profitpilot_db",
        env="MONGODB_DB_NAME"
    )

    # =========================
    # JWT
    # =========================
    SECRET_KEY: str = Field(
        default="your-super-secret-key-change-this-in-production-min-32-characters",
        env="SECRET_KEY"
    )

    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        env="REFRESH_TOKEN_EXPIRE_DAYS"
    )

    # =========================
    # CORS
    # =========================
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://profitpilot-ai-pro.netlify.app",
        ],
        env="CORS_ORIGINS"
    )

    # =========================
    # Logging
    # =========================
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="app.log", env="LOG_FILE")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()


def get_settings() -> Settings:
    return settings
