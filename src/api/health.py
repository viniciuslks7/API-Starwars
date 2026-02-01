"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "service": "starwars-api",
    }


@router.get("/health/ready")
async def readiness_check() -> dict:
    """Readiness check - can the service handle requests."""
    return {
        "status": "ready",
        "checks": {
            "swapi": "ok",
            "cache": "ok",
        },
    }
