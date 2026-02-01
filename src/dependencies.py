"""Dependency injection for FastAPI."""

from typing import Annotated

from fastapi import Depends

from src.config import Settings, get_settings
from src.services.cache_service import CacheService
from src.services.swapi_client import SWAPIClient

# Settings dependency
SettingsDep = Annotated[Settings, Depends(get_settings)]


# SWAPI Client singleton
_swapi_client: SWAPIClient | None = None


def get_swapi_client() -> SWAPIClient:
    """Get SWAPI client singleton instance."""
    global _swapi_client
    if _swapi_client is None:
        settings = get_settings()
        _swapi_client = SWAPIClient(base_url=settings.swapi_base_url)
    return _swapi_client


SWAPIClientDep = Annotated[SWAPIClient, Depends(get_swapi_client)]


# Cache Service singleton
_cache_service: CacheService | None = None


def get_cache_service() -> CacheService:
    """Get cache service singleton instance."""
    global _cache_service
    if _cache_service is None:
        settings = get_settings()
        _cache_service = CacheService(
            enabled=settings.cache_enabled,
            default_ttl=settings.cache_ttl_seconds,
        )
    return _cache_service


CacheServiceDep = Annotated[CacheService, Depends(get_cache_service)]
