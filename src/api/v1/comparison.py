"""Comparison API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from src.dependencies import get_swapi_client
from src.models.people import Person
from src.models.starships import Starship
from src.models.planets import Planet
from src.models.statistics import ComparisonResult
from src.services.swapi_client import SWAPIError

router = APIRouter()


@router.get(
    "/characters",
    response_model=ComparisonResult,
    summary="Compare characters",
    description="Compare multiple characters side by side.",
)
async def compare_characters(
    ids: list[int] = Query(..., min_length=2, max_length=5, description="Character IDs to compare"),
) -> ComparisonResult:
    """Compare multiple characters."""
    swapi = get_swapi_client()

    try:
        people_data = await swapi.get_multiple_by_ids("people", ids)

        if len(people_data) < 2:
            raise HTTPException(
                status_code=400, detail="Need at least 2 valid character IDs to compare"
            )

        people = [Person.from_swapi(data, data["id"]) for data in people_data]

        entities = []
        for p in people:
            entities.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "height": p.height,
                    "mass": p.mass,
                    "hair_color": p.hair_color,
                    "eye_color": p.eye_color,
                    "birth_year": p.birth_year,
                    "gender": p.gender,
                    "films_count": len(p.film_ids),
                    "starships_count": len(p.starship_ids),
                }
            )

        return ComparisonResult(
            entity_type="characters",
            entities=entities,
            comparison_fields=["height", "mass", "films_count", "starships_count"],
        )

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/starships",
    response_model=ComparisonResult,
    summary="Compare starships",
    description="Compare multiple starships side by side.",
)
async def compare_starships(
    ids: list[int] = Query(..., min_length=2, max_length=5, description="Starship IDs to compare"),
) -> ComparisonResult:
    """Compare multiple starships."""
    swapi = get_swapi_client()

    try:
        starships_data = await swapi.get_multiple_by_ids("starships", ids)

        if len(starships_data) < 2:
            raise HTTPException(
                status_code=400, detail="Need at least 2 valid starship IDs to compare"
            )

        starships = [Starship.from_swapi(data, data["id"]) for data in starships_data]

        entities = []
        for s in starships:
            entities.append(
                {
                    "id": s.id,
                    "name": s.name,
                    "model": s.model,
                    "manufacturer": s.manufacturer,
                    "starship_class": s.starship_class,
                    "cost_in_credits": s.cost_in_credits,
                    "length": s.length,
                    "crew": s.crew,
                    "passengers": s.passengers,
                    "hyperdrive_rating": s.hyperdrive_rating,
                    "mglt": s.mglt,
                    "cargo_capacity": s.cargo_capacity,
                }
            )

        return ComparisonResult(
            entity_type="starships",
            entities=entities,
            comparison_fields=[
                "cost_in_credits",
                "length",
                "hyperdrive_rating",
                "mglt",
                "cargo_capacity",
            ],
        )

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/planets",
    response_model=ComparisonResult,
    summary="Compare planets",
    description="Compare multiple planets side by side.",
)
async def compare_planets(
    ids: list[int] = Query(..., min_length=2, max_length=5, description="Planet IDs to compare"),
) -> ComparisonResult:
    """Compare multiple planets."""
    swapi = get_swapi_client()

    try:
        planets_data = await swapi.get_multiple_by_ids("planets", ids)

        if len(planets_data) < 2:
            raise HTTPException(
                status_code=400, detail="Need at least 2 valid planet IDs to compare"
            )

        planets = [Planet.from_swapi(data, data["id"]) for data in planets_data]

        entities = []
        for p in planets:
            entities.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "diameter": p.diameter,
                    "rotation_period": p.rotation_period,
                    "orbital_period": p.orbital_period,
                    "gravity": p.gravity,
                    "population": p.population,
                    "climate": p.climate,
                    "terrain": p.terrain,
                    "surface_water": p.surface_water,
                    "residents_count": len(p.resident_ids),
                    "films_count": len(p.film_ids),
                }
            )

        return ComparisonResult(
            entity_type="planets",
            entities=entities,
            comparison_fields=["diameter", "population", "surface_water", "residents_count"],
        )

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
