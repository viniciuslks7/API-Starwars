"""People/Characters API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from src.dependencies import get_swapi_client
from src.models.base import PaginatedResponse, SortOrder
from src.models.films import FilmSummary
from src.models.people import Person, PersonFilter, PersonSummary
from src.models.starships import StarshipSummary
from src.services.swapi_client import SWAPIError
from src.utils.pagination import paginate
from src.utils.sorting import PEOPLE_SORT_KEYS, sort_items

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedResponse[PersonSummary],
    summary="List all characters",
    description="Get a paginated list of all Star Wars characters with optional filtering and sorting.",
)
async def list_people(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str | None = Query(None, description="Field to sort by (name, height, mass)"),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort order"),
    gender: str | None = Query(None, description="Filter by gender"),
    eye_color: str | None = Query(None, description="Filter by eye color"),
    min_height: int | None = Query(None, description="Minimum height in cm"),
    max_height: int | None = Query(None, description="Maximum height in cm"),
) -> PaginatedResponse[PersonSummary]:
    """List all characters with pagination, filtering, and sorting."""
    swapi = get_swapi_client()

    try:
        # Fetch all people
        all_people_data = await swapi.get_all_people()

        # Convert to Person models for filtering
        people = [Person.from_swapi(data, data["id"]) for data in all_people_data]

        # Apply filters
        person_filter = PersonFilter(
            gender=gender,
            eye_color=eye_color,
            hair_color=None,
            homeworld_id=None,
            min_height=min_height,
            max_height=max_height,
            min_mass=None,
            max_mass=None,
        )
        filtered_people = [p for p in people if person_filter.apply(p)]

        # Sort
        sorted_people = sort_items(
            filtered_people,
            sort_by=sort_by,
            sort_order=sort_order,
            key_mapper=PEOPLE_SORT_KEYS,
        )

        # Convert to summaries
        summaries = [
            PersonSummary(
                id=p.id,
                name=p.name,
                gender=p.gender,
                birth_year=p.birth_year,
                homeworld_id=p.homeworld_id,
                films_count=len(p.film_ids),
            )
            for p in sorted_people
        ]

        # Paginate
        return paginate(summaries, page=page, page_size=page_size)

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/search",
    response_model=list[PersonSummary],
    summary="Search characters",
    description="Search for characters by name.",
)
async def search_people(
    q: str = Query(..., min_length=1, description="Search query"),
) -> list[PersonSummary]:
    """Search characters by name."""
    swapi = get_swapi_client()

    try:
        results = await swapi.search_people(q)
        return [PersonSummary.from_swapi(data, data["id"]) for data in results]
    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Get character by ID",
    description="Get detailed information about a specific character.",
)
async def get_person(person_id: int) -> Person:
    """Get a single character by ID."""
    swapi = get_swapi_client()

    try:
        data = await swapi.get_person(person_id)
        person = Person.from_swapi(data, person_id)

        # Optionally fetch homeworld name
        if person.homeworld_id:
            try:
                planet_data = await swapi.get_planet(person.homeworld_id)
                person.homeworld_name = planet_data.get("name")
            except SWAPIError:
                pass  # Keep homeworld_name as None

        return person
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Character with ID {person_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{person_id}/films",
    response_model=list[FilmSummary],
    summary="Get character's films",
    description="Get all films that a character appears in.",
)
async def get_person_films(person_id: int) -> list[FilmSummary]:
    """Get all films for a character."""
    swapi = get_swapi_client()

    try:
        person_data = await swapi.get_person(person_id)
        person = Person.from_swapi(person_data, person_id)

        if not person.film_ids:
            return []

        films_data = await swapi.get_multiple_by_ids("films", person.film_ids)
        return [FilmSummary.from_swapi(data, data.get("id", 0)) for data in films_data]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Character with ID {person_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{person_id}/starships",
    response_model=list[StarshipSummary],
    summary="Get character's starships",
    description="Get all starships piloted by a character.",
)
async def get_person_starships(person_id: int) -> list[StarshipSummary]:
    """Get all starships piloted by a character."""
    swapi = get_swapi_client()

    try:
        person_data = await swapi.get_person(person_id)
        person = Person.from_swapi(person_data, person_id)

        if not person.starship_ids:
            return []

        starships_data = await swapi.get_multiple_by_ids("starships", person.starship_ids)
        return [StarshipSummary.from_swapi(data, data.get("id", 0)) for data in starships_data]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Character with ID {person_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
