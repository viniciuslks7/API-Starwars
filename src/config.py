"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = True

    # API Configuration
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Star Wars API Platform"
    project_description: str = (
        "A REST API for exploring the Star Wars universe with advanced filtering, "
        "sorting, and correlated queries."
    )
    version: str = "1.0.0"

    # SWAPI Configuration
    swapi_base_url: str = "https://swapi.dev/api"

    # Cache Configuration
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600  # 1 hour default

    # GCP Configuration
    gcp_project_id: str = ""

    # Firebase Configuration
    firebase_project_id: str = ""
    firebase_credentials_path: str = ""

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
