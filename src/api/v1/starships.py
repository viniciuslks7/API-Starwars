"""Starships API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from src.dependencies import get_swapi_client
from src.models.base import PaginatedResponse, SortOrder
from src.models.starships import Starship, StarshipFilter, StarshipSummary
from src.models.people import PersonSummary
from src.services.swapi_client import SWAPIError
from src.utils.pagination import paginate
from src.utils.sorting import sort_items, STARSHIP_SORT_KEYS

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedResponse[StarshipSummary],
    summary="List all starships",
    description="Get a paginated list of all starships with optional filtering and sorting.",
)
async def list_starships(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str | None = Query(None, description="Field to sort by (name, length, cost_in_credits, hyperdrive_rating)"),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort order"),
    manufacturer: str | None = Query(None, description="Filter by manufacturer (partial match)"),
    starship_class: str | None = Query(None, description="Filter by starship class (partial match)"),
    min_cost: int | None = Query(None, description="Minimum cost in credits"),
    max_cost: int | None = Query(None, description="Maximum cost in credits"),
    min_length: float | None = Query(None, description="Minimum length in meters"),
    max_length: float | None = Query(None, description="Maximum length in meters"),
) -> PaginatedResponse[StarshipSummary]:
    """List all starships with filtering, sorting, and pagination."""
    swapi = get_swapi_client()
    
    try:
        all_starships_data = await swapi.get_all_starships()
        
        # Convert to Starship models
        starships = [Starship.from_swapi(data, data["id"]) for data in all_starships_data]
        
        # Apply filters
        starship_filter = StarshipFilter(
            manufacturer=manufacturer,
            starship_class=starship_class,
            min_cost=min_cost,
            max_cost=max_cost,
            min_length=min_length,
            max_length=max_length,
        )
        filtered = [s for s in starships if starship_filter.apply(s)]
        
        # Sort
        sorted_starships = sort_items(
            filtered,
            sort_by=sort_by,
            sort_order=sort_order,
            key_mapper=STARSHIP_SORT_KEYS,
        )
        
        # Convert to summaries
        summaries = [
            StarshipSummary(
                id=s.id,
                name=s.name,
                model=s.model,
                starship_class=s.starship_class,
                manufacturer=s.manufacturer,
            )
            for s in sorted_starships
        ]
        
        return paginate(summaries, page=page, page_size=page_size)
        
    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/search",
    response_model=list[StarshipSummary],
    summary="Search starships",
    description="Search for starships by name or model.",
)
async def search_starships(
    q: str = Query(..., min_length=1, description="Search query"),
) -> list[StarshipSummary]:
    """Search starships by name or model."""
    swapi = get_swapi_client()
    
    try:
        results = await swapi.search_starships(q)
        return [StarshipSummary.from_swapi(data, data["id"]) for data in results]
    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{starship_id}",
    response_model=Starship,
    summary="Get starship by ID",
    description="Get detailed information about a specific starship.",
)
async def get_starship(starship_id: int) -> Starship:
    """Get a single starship by ID."""
    swapi = get_swapi_client()
    
    try:
        data = await swapi.get_starship(starship_id)
        return Starship.from_swapi(data, starship_id)
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Starship with ID {starship_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{starship_id}/pilots",
    response_model=list[PersonSummary],
    summary="Get starship's pilots",
    description="Get all pilots who have piloted this starship.",
)
async def get_starship_pilots(starship_id: int) -> list[PersonSummary]:
    """Get all pilots of a starship."""
    swapi = get_swapi_client()
    
    try:
        starship_data = await swapi.get_starship(starship_id)
        starship = Starship.from_swapi(starship_data, starship_id)
        
        if not starship.pilot_ids:
            return []
        
        people_data = await swapi.get_multiple_by_ids("people", starship.pilot_ids)
        return [
            PersonSummary.from_swapi(data, data.get("id", 0))
            for data in people_data
        ]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Starship with ID {starship_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
