from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

    # Project
    PROJECT_NAME: str = 'Expense Tracker'
    VERSION: str = '0.1.0'
    DEBUG: bool = False

    # Database
    DATABAE_URL: str = Field(
        ...,
        description='Async PostgreSQL URL: e.g. postgresql+asyncpg://user:password@localhost:5432/expense_tracker'
    )

    # Security / JWT
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()