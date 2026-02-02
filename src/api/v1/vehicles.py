"""Vehicles API endpoints."""

from fastapi import APIRouter, HTTPException, Query

from src.dependencies import get_swapi_client
from src.models.base import PaginatedResponse, SortOrder
from src.models.vehicles import Vehicle, VehicleSummary
from src.models.people import PersonSummary
from src.services.swapi_client import SWAPIError
from src.utils.pagination import paginate
from src.utils.sorting import sort_items

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedResponse[VehicleSummary],
    summary="List all vehicles",
    description="Get a paginated list of all vehicles.",
)
async def list_vehicles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: str | None = Query(None, description="Field to sort by (name, model)"),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort order"),
    vehicle_class: str | None = Query(None, description="Filter by vehicle class"),
    manufacturer: str | None = Query(None, description="Filter by manufacturer"),
) -> PaginatedResponse[VehicleSummary]:
    """List all vehicles with pagination."""
    swapi = get_swapi_client()

    try:
        all_vehicles_data = await swapi.get_all_vehicles()

        # Convert to Vehicle models
        vehicles = [Vehicle.from_swapi(data, data["id"]) for data in all_vehicles_data]

        # Apply filters
        filtered = vehicles
        if vehicle_class:
            filtered = [v for v in filtered if vehicle_class.lower() in v.vehicle_class.lower()]
        if manufacturer:
            filtered = [v for v in filtered if manufacturer.lower() in v.manufacturer.lower()]

        # Sort
        sorted_vehicles = sort_items(filtered, sort_by=sort_by, sort_order=sort_order)

        # Convert to summaries
        summaries = [
            VehicleSummary(
                id=v.id,
                name=v.name,
                model=v.model,
                vehicle_class=v.vehicle_class,
                manufacturer=v.manufacturer,
            )
            for v in sorted_vehicles
        ]

        return paginate(summaries, page=page, page_size=page_size)

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{vehicle_id}",
    response_model=Vehicle,
    summary="Get vehicle by ID",
    description="Get detailed information about a specific vehicle.",
)
async def get_vehicle(vehicle_id: int) -> Vehicle:
    """Get a single vehicle by ID."""
    swapi = get_swapi_client()

    try:
        data = await swapi.get_vehicle(vehicle_id)
        return Vehicle.from_swapi(data, vehicle_id)
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Vehicle with ID {vehicle_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/{vehicle_id}/pilots",
    response_model=list[PersonSummary],
    summary="Get vehicle's pilots",
    description="Get all pilots who have piloted this vehicle.",
)
async def get_vehicle_pilots(vehicle_id: int) -> list[PersonSummary]:
    """Get all pilots of a vehicle."""
    swapi = get_swapi_client()

    try:
        vehicle_data = await swapi.get_vehicle(vehicle_id)
        vehicle = Vehicle.from_swapi(vehicle_data, vehicle_id)

        if not vehicle.pilot_ids:
            return []

        people_data = await swapi.get_multiple_by_ids("people", vehicle.pilot_ids)
        return [PersonSummary.from_swapi(data, data.get("id", 0)) for data in people_data]
    except SWAPIError as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Vehicle with ID {vehicle_id} not found")
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
