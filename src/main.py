"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.health import router as health_router
from src.api.v1.router import router as api_v1_router
from src.api.v1.rankings import router as rankings_router
from src.api.v1.timeline import router as timeline_router
from src.config import get_settings
from src.middleware import (
    RateLimitMiddleware,
    RequestTrackingMiddleware,
    SecurityHeadersMiddleware,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    print(f"Starting {settings.project_name} v{settings.version}")
    print(f"Environment: {settings.environment}")
    print(f"SWAPI Base URL: {settings.swapi_base_url}")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middlewares (ordem importa: último adicionado = primeiro executado)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestTrackingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle uncaught exceptions globally."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if settings.debug else "An unexpected error occurred",
        },
    )


# Include routers
app.include_router(health_router)
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)
app.include_router(rankings_router)  # Rankings/Top N endpoints
app.include_router(timeline_router)  # Timeline endpoints


# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": settings.project_name,
        "version": settings.version,
        "docs": "/docs",
        "health": "/health",
        "api": settings.api_v1_prefix,
    }
