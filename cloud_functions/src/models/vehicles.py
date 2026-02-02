"""Vehicles models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class VehicleSummary(BaseModel):
    """Summary model for vehicle (used in lists)."""

    id: int = Field(..., description="Vehicle ID")
    name: str = Field(..., description="Vehicle name")
    model: str = Field(..., description="Vehicle model")
    vehicle_class: str = Field(..., description="Vehicle class")
    manufacturer: str = Field(..., description="Manufacturer")

    @classmethod
    def from_swapi(cls, data: dict, vehicle_id: int) -> "VehicleSummary":
        """Create from SWAPI response."""
        return cls(
            id=vehicle_id,
            name=data["name"],
            model=data.get("model", "Unknown"),
            vehicle_class=data.get("vehicle_class", "Unknown"),
            manufacturer=data.get("manufacturer", "Unknown"),
        )


class Vehicle(BaseModel):
    """Full vehicle model with all details."""

    id: int = Field(..., description="Vehicle ID")
    name: str = Field(..., description="Vehicle name")
    model: str = Field(..., description="Vehicle model")
    vehicle_class: str = Field(..., description="Vehicle class")
    manufacturer: str = Field(..., description="Manufacturer")
    cost_in_credits: int | None = Field(None, description="Cost in credits")
    length: float | None = Field(None, description="Length in meters")
    crew: str = Field(..., description="Number of crew required")
    passengers: str = Field(..., description="Number of passengers")
    max_atmosphering_speed: int | None = Field(None, description="Max atmospheric speed")
    cargo_capacity: int | None = Field(None, description="Cargo capacity in kg")
    consumables: str = Field(..., description="Consumables duration")
    pilot_ids: list[int] = Field(default_factory=list, description="Pilot IDs")
    film_ids: list[int] = Field(default_factory=list, description="Film IDs")
    created: datetime | None = Field(None, description="Created timestamp")
    edited: datetime | None = Field(None, description="Last edited timestamp")

    @field_validator("cost_in_credits", "cargo_capacity", mode="before")
    @classmethod
    def parse_int_field(cls, v: Any) -> int | None:
        """Parse integer fields from string."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            return int(str(v).replace(",", ""))
        except ValueError:
            return None

    @field_validator("length", mode="before")
    @classmethod
    def parse_length(cls, v: Any) -> float | None:
        """Parse length from string to float."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            return float(str(v).replace(",", ""))
        except ValueError:
            return None

    @field_validator("max_atmosphering_speed", mode="before")
    @classmethod
    def parse_speed(cls, v: Any) -> int | None:
        """Parse max speed from string to int."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            # Handle cases like "30" or "1000km"
            speed_str = str(v).lower().replace("km", "").strip()
            return int(speed_str)
        except ValueError:
            return None

    @classmethod
    def _extract_ids(cls, urls: list[str]) -> list[int]:
        """Extract IDs from SWAPI URLs."""
        ids = []
        for url in urls:
            try:
                id_str = url.rstrip("/").split("/")[-1]
                ids.append(int(id_str))
            except (ValueError, IndexError):
                continue
        return ids

    @classmethod
    def from_swapi(cls, data: dict, vehicle_id: int) -> "Vehicle":
        """Create from SWAPI response."""
        created = None
        if data.get("created"):
            try:
                created = datetime.fromisoformat(data["created"].replace("Z", "+00:00"))
            except ValueError:
                pass

        edited = None
        if data.get("edited"):
            try:
                edited = datetime.fromisoformat(data["edited"].replace("Z", "+00:00"))
            except ValueError:
                pass

        return cls(
            id=vehicle_id,
            name=data["name"],
            model=data.get("model", "Unknown"),
            vehicle_class=data.get("vehicle_class", "Unknown"),
            manufacturer=data.get("manufacturer", "Unknown"),
            cost_in_credits=data.get("cost_in_credits"),
            length=data.get("length"),
            crew=data.get("crew", "Unknown"),
            passengers=data.get("passengers", "Unknown"),
            max_atmosphering_speed=data.get("max_atmosphering_speed"),
            cargo_capacity=data.get("cargo_capacity"),
            consumables=data.get("consumables", "Unknown"),
            pilot_ids=cls._extract_ids(data.get("pilots", [])),
            film_ids=cls._extract_ids(data.get("films", [])),
            created=created,
            edited=edited,
        )
