"""Films API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from src.dependencies import get_swapi_client
from src.models.base import PaginatedResponse, SortOrder
from src.models.films import Film, FilmSummary
from src.models.people import PersonSummary
from src.models.planets import PlanetSummary
from src.models.starships import StarshipSummary
from src.services.swapi_client import SWAPIError
from src.utils.pagination import paginate
from src.utils.sorting import FILM_SORT_KEYS, sort_items

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedResponse[FilmSummary],
    summary="List all films",
    description="Get a paginated list of all Star Wars films.",
)
async def list_films(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str | None = Query(
        "episode_id", description="Field to sort by (title, episode_id, release_date)"
    ),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort order"),
) -> PaginatedResponse[FilmSummary]:
    """List all films with sorting."""
    swapi = get_swapi_client()

    try:
        all_films_data = await swapi.get_all_films()

        # Convert to Film models
        films = [
            Film.from_swapi(data, data.get("id", i + 1)) for i, data in enumerate(all_films_data)
        ]

        # Sort
        sorted_films = sort_items(
            films,
            sort_by=sort_by,
            sort_order=sort_order,
            key_mapper=FILM_SORT_KEYS,
        )

        # Convert to summaries
        summaries = [
            FilmSummary(
                id=f.id,
                episode_id=f.episode_id,
                title=f.title,
                director=f.director,
                release_date=f.release_date,
                characters_count=len(f.character_ids),
            )
            for f in sorted_films
        ]

        return paginate(summaries, page=page, page_size=page_size)

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{film_id}",
    response_model=Film,
    summary="Get film by ID",
    description="Get detailed information about a specific film.",
)
async def get_film(film_id: int) -> Film:
    """Get a single film by ID."""
    swapi = get_swapi_client()

    try:
        data = await swapi.get_film(film_id)
        return Film.from_swapi(data, film_id)
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Film with ID {film_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{film_id}/characters",
    response_model=list[PersonSummary],
    summary="Get film's characters",
    description="Get all characters that appear in a film.",
)
async def get_film_characters(film_id: int) -> list[PersonSummary]:
    """Get all characters in a film."""
    swapi = get_swapi_client()

    try:
        film_data = await swapi.get_film(film_id)
        film = Film.from_swapi(film_data, film_id)

        if not film.character_ids:
            return []

        people_data = await swapi.get_multiple_by_ids("people", film.character_ids)
        return [PersonSummary.from_swapi(data, data.get("id", 0)) for data in people_data]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Film with ID {film_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{film_id}/planets",
    response_model=list[PlanetSummary],
    summary="Get film's planets",
    description="Get all planets that appear in a film.",
)
async def get_film_planets(film_id: int) -> list[PlanetSummary]:
    """Get all planets in a film."""
    swapi = get_swapi_client()

    try:
        film_data = await swapi.get_film(film_id)
        film = Film.from_swapi(film_data, film_id)

        if not film.planet_ids:
            return []

        planets_data = await swapi.get_multiple_by_ids("planets", film.planet_ids)
        return [PlanetSummary.from_swapi(data, data.get("id", 0)) for data in planets_data]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Film with ID {film_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{film_id}/starships",
    response_model=list[StarshipSummary],
    summary="Get film's starships",
    description="Get all starships that appear in a film.",
)
async def get_film_starships(film_id: int) -> list[StarshipSummary]:
    """Get all starships in a film."""
    swapi = get_swapi_client()

    try:
        film_data = await swapi.get_film(film_id)
        film = Film.from_swapi(film_data, film_id)

        if not film.starship_ids:
            return []

        starships_data = await swapi.get_multiple_by_ids("starships", film.starship_ids)
        return [StarshipSummary.from_swapi(data, data.get("id", 0)) for data in starships_data]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Film with ID {film_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
