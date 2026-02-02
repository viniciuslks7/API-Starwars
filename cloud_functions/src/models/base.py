"""Base models for API responses."""

from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SortOrder(str, Enum):
    """Sort order enum."""

    ASC = "asc"
    DESC = "desc"


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""

    count: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_previous: bool = Field(..., description="Whether there is a previous page")
    results: list[T] = Field(..., description="List of items")


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: dict | None = Field(None, description="Additional error details")


class SuccessResponse(BaseModel):
    """Simple success response."""

    success: bool = True
    message: str = Field(..., description="Success message")
