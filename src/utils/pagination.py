"""Pagination utilities."""

from typing import TypeVar

from src.models.base import PaginatedResponse

T = TypeVar("T")


def paginate(
    items: list[T],
    page: int = 1,
    page_size: int = 10,
) -> PaginatedResponse[T]:
    """
    Paginate a list of items.

    Args:
        items: Full list of items to paginate
        page: Page number (1-indexed)
        page_size: Number of items per page

    Returns:
        PaginatedResponse with the requested page of items
    """
    # Ensure valid values
    page = max(1, page)
    page_size = max(1, min(100, page_size))  # Cap at 100 items per page

    total_count = len(items)
    total_pages = max(1, (total_count + page_size - 1) // page_size)

    # Adjust page if out of range
    page = min(page, total_pages)

    # Calculate slice indices
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    return PaginatedResponse(
        count=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
        results=items[start_idx:end_idx],
    )


def get_pagination_params(
    page: int | None = None,
    page_size: int | None = None,
    default_page_size: int = 10,
    max_page_size: int = 100,
) -> tuple[int, int]:
    """
    Normalize and validate pagination parameters.

    Args:
        page: Requested page number
        page_size: Requested page size
        default_page_size: Default page size if not specified
        max_page_size: Maximum allowed page size

    Returns:
        Tuple of (page, page_size) with validated values
    """
    validated_page = max(1, page or 1)
    validated_size = max(1, min(max_page_size, page_size or default_page_size))
    return validated_page, validated_size
