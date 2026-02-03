"""Species API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from src.dependencies import get_swapi_client
from src.models.base import PaginatedResponse, SortOrder
from src.models.people import PersonSummary
from src.models.species import Species, SpeciesSummary
from src.services.swapi_client import SWAPIError
from src.utils.pagination import paginate
from src.utils.sorting import sort_items

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedResponse[SpeciesSummary],
    summary="List all species",
    description="Get a paginated list of all species.",
)
async def list_species(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str | None = Query(None, description="Field to sort by (name, classification)"),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort order"),
    classification: str | None = Query(None, description="Filter by classification"),
    designation: str | None = Query(
        None, description="Filter by designation (sentient/non-sentient)"
    ),
) -> PaginatedResponse[SpeciesSummary]:
    """List all species with pagination."""
    swapi = get_swapi_client()

    try:
        all_species_data = await swapi.get_all_species()

        # Convert to Species models
        species_list = [Species.from_swapi(data, data["id"]) for data in all_species_data]

        # Apply filters
        filtered = species_list
        if classification:
            filtered = [s for s in filtered if classification.lower() in s.classification.lower()]
        if designation:
            filtered = [s for s in filtered if designation.lower() in s.designation.lower()]

        # Sort
        sorted_species = sort_items(filtered, sort_by=sort_by, sort_order=sort_order)

        # Convert to summaries
        summaries = [
            SpeciesSummary(
                id=s.id,
                name=s.name,
                classification=s.classification,
                designation=s.designation,
                language=s.language,
            )
            for s in sorted_species
        ]

        return paginate(summaries, page=page, page_size=page_size)

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{species_id}",
    response_model=Species,
    summary="Get species by ID",
    description="Get detailed information about a specific species.",
)
async def get_species_by_id(species_id: int) -> Species:
    """Get a single species by ID."""
    swapi = get_swapi_client()

    try:
        data = await swapi.get_species(species_id)
        return Species.from_swapi(data, species_id)
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Species with ID {species_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{species_id}/people",
    response_model=list[PersonSummary],
    summary="Get species' people",
    description="Get all characters of this species.",
)
async def get_species_people(species_id: int) -> list[PersonSummary]:
    """Get all people of a species."""
    swapi = get_swapi_client()

    try:
        species_data = await swapi.get_species(species_id)
        species = Species.from_swapi(species_data, species_id)

        if not species.people_ids:
            return []

        people_data = await swapi.get_multiple_by_ids("people", species.people_ids)
        return [PersonSummary.from_swapi(data, data.get("id", 0)) for data in people_data]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Species with ID {species_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
