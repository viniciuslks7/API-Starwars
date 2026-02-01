"""Planets API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from src.dependencies import get_swapi_client
from src.models.base import PaginatedResponse, SortOrder
from src.models.planets import Planet, PlanetFilter, PlanetSummary
from src.models.people import PersonSummary
from src.models.films import FilmSummary
from src.services.swapi_client import SWAPIError
from src.utils.pagination import paginate
from src.utils.sorting import sort_items, PLANET_SORT_KEYS

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedResponse[PlanetSummary],
    summary="List all planets",
    description="Get a paginated list of all planets with optional filtering and sorting.",
)
async def list_planets(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str | None = Query(None, description="Field to sort by (name, diameter, population)"),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort order"),
    climate: str | None = Query(None, description="Filter by climate (partial match)"),
    terrain: str | None = Query(None, description="Filter by terrain (partial match)"),
    min_population: int | None = Query(None, description="Minimum population"),
    max_population: int | None = Query(None, description="Maximum population"),
) -> PaginatedResponse[PlanetSummary]:
    """List all planets with filtering, sorting, and pagination."""
    swapi = get_swapi_client()
    
    try:
        all_planets_data = await swapi.get_all_planets()
        
        # Convert to Planet models
        planets = [Planet.from_swapi(data, data["id"]) for data in all_planets_data]
        
        # Apply filters
        planet_filter = PlanetFilter(
            climate=climate,
            terrain=terrain,
            min_population=min_population,
            max_population=max_population,
        )
        filtered = [p for p in planets if planet_filter.apply(p)]
        
        # Sort
        sorted_planets = sort_items(
            filtered,
            sort_by=sort_by,
            sort_order=sort_order,
            key_mapper=PLANET_SORT_KEYS,
        )
        
        # Convert to summaries
        summaries = [
            PlanetSummary(
                id=p.id,
                name=p.name,
                climate=p.climate,
                terrain=p.terrain,
                population=p.population,
            )
            for p in sorted_planets
        ]
        
        return paginate(summaries, page=page, page_size=page_size)
        
    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/search",
    response_model=list[PlanetSummary],
    summary="Search planets",
    description="Search for planets by name.",
)
async def search_planets(
    q: str = Query(..., min_length=1, description="Search query"),
) -> list[PlanetSummary]:
    """Search planets by name."""
    swapi = get_swapi_client()
    
    try:
        results = await swapi.search_planets(q)
        return [PlanetSummary.from_swapi(data, data["id"]) for data in results]
    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{planet_id}",
    response_model=Planet,
    summary="Get planet by ID",
    description="Get detailed information about a specific planet.",
)
async def get_planet(planet_id: int) -> Planet:
    """Get a single planet by ID."""
    swapi = get_swapi_client()
    
    try:
        data = await swapi.get_planet(planet_id)
        return Planet.from_swapi(data, planet_id)
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Planet with ID {planet_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{planet_id}/residents",
    response_model=list[PersonSummary],
    summary="Get planet's residents",
    description="Get all characters who live on this planet.",
)
async def get_planet_residents(planet_id: int) -> list[PersonSummary]:
    """Get all residents of a planet."""
    swapi = get_swapi_client()
    
    try:
        planet_data = await swapi.get_planet(planet_id)
        planet = Planet.from_swapi(planet_data, planet_id)
        
        if not planet.resident_ids:
            return []
        
        people_data = await swapi.get_multiple_by_ids("people", planet.resident_ids)
        return [
            PersonSummary.from_swapi(data, data.get("id", 0))
            for data in people_data
        ]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Planet with ID {planet_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{planet_id}/films",
    response_model=list[FilmSummary],
    summary="Get planet's films",
    description="Get all films that feature this planet.",
)
async def get_planet_films(planet_id: int) -> list[FilmSummary]:
    """Get all films featuring a planet."""
    swapi = get_swapi_client()
    
    try:
        planet_data = await swapi.get_planet(planet_id)
        planet = Planet.from_swapi(planet_data, planet_id)
        
        if not planet.film_ids:
            return []
        
        films_data = await swapi.get_multiple_by_ids("films", planet.film_ids)
        return [
            FilmSummary.from_swapi(data, data.get("id", 0))
            for data in films_data
        ]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Planet with ID {planet_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
