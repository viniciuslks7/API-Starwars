"""Starships models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class StarshipSummary(BaseModel):
    """Summary model for starship (used in lists)."""

    id: int = Field(..., description="Starship ID")
    name: str = Field(..., description="Starship name")
    model: str = Field(..., description="Starship model")
    starship_class: str = Field(..., description="Starship class")
    manufacturer: str = Field(..., description="Manufacturer")

    @classmethod
    def from_swapi(cls, data: dict, starship_id: int) -> "StarshipSummary":
        """Create from SWAPI response."""
        return cls(
            id=starship_id,
            name=data["name"],
            model=data.get("model", "Unknown"),
            starship_class=data.get("starship_class", "Unknown"),
            manufacturer=data.get("manufacturer", "Unknown"),
        )


class Starship(BaseModel):
    """Full starship model with all details."""

    id: int = Field(..., description="Starship ID")
    name: str = Field(..., description="Starship name")
    model: str = Field(..., description="Starship model")
    starship_class: str = Field(..., description="Starship class")
    manufacturer: str = Field(..., description="Manufacturer")
    cost_in_credits: int | None = Field(None, description="Cost in credits")
    length: float | None = Field(None, description="Length in meters")
    crew: str = Field(..., description="Number of crew required")
    passengers: str = Field(..., description="Number of passengers")
    max_atmosphering_speed: str = Field(..., description="Max atmospheric speed")
    hyperdrive_rating: float | None = Field(None, description="Hyperdrive rating")
    mglt: int | None = Field(None, description="Max Megalights per hour")
    cargo_capacity: int | None = Field(None, description="Cargo capacity in kg")
    consumables: str = Field(..., description="Consumables duration")
    pilot_ids: list[int] = Field(default_factory=list, description="Pilot IDs")
    film_ids: list[int] = Field(default_factory=list, description="Film IDs")
    created: datetime | None = Field(None, description="Created timestamp")
    edited: datetime | None = Field(None, description="Last edited timestamp")

    @field_validator("cost_in_credits", mode="before")
    @classmethod
    def parse_cost(cls, v: Any) -> int | None:
        """Parse cost from string to int."""
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

    @field_validator("hyperdrive_rating", mode="before")
    @classmethod
    def parse_hyperdrive(cls, v: Any) -> float | None:
        """Parse hyperdrive rating from string to float."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            return float(str(v))
        except ValueError:
            return None

    @field_validator("mglt", mode="before")
    @classmethod
    def parse_mglt(cls, v: Any) -> int | None:
        """Parse MGLT from string to int."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            # Handle cases like "10 MGLT"
            return int(str(v).split()[0].replace(",", ""))
        except (ValueError, IndexError):
            return None

    @field_validator("cargo_capacity", mode="before")
    @classmethod
    def parse_cargo(cls, v: Any) -> int | None:
        """Parse cargo capacity from string to int."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            return int(str(v).replace(",", ""))
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
    def from_swapi(cls, data: dict, starship_id: int) -> "Starship":
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
            id=starship_id,
            name=data["name"],
            model=data.get("model", "Unknown"),
            starship_class=data.get("starship_class", "Unknown"),
            manufacturer=data.get("manufacturer", "Unknown"),
            cost_in_credits=data.get("cost_in_credits"),
            length=data.get("length"),
            crew=data.get("crew", "Unknown"),
            passengers=data.get("passengers", "Unknown"),
            max_atmosphering_speed=data.get("max_atmosphering_speed", "Unknown"),
            hyperdrive_rating=data.get("hyperdrive_rating"),
            mglt=data.get("MGLT"),
            cargo_capacity=data.get("cargo_capacity"),
            consumables=data.get("consumables", "Unknown"),
            pilot_ids=cls._extract_ids(data.get("pilots", [])),
            film_ids=cls._extract_ids(data.get("films", [])),
            created=created,
            edited=edited,
        )


class StarshipFilter(BaseModel):
    """Filter parameters for starship queries."""

    manufacturer: str | None = Field(None, description="Filter by manufacturer")
    starship_class: str | None = Field(None, description="Filter by starship class")
    min_cost: int | None = Field(None, description="Minimum cost in credits")
    max_cost: int | None = Field(None, description="Maximum cost in credits")
    min_length: float | None = Field(None, description="Minimum length in meters")
    max_length: float | None = Field(None, description="Maximum length in meters")
    min_hyperdrive: float | None = Field(None, description="Minimum hyperdrive rating")
    max_hyperdrive: float | None = Field(None, description="Maximum hyperdrive rating")

    def apply(self, starship: Starship) -> bool:
        """Check if a starship matches this filter."""
        if self.manufacturer:
            if self.manufacturer.lower() not in starship.manufacturer.lower():
                return False
        if self.starship_class:
            if self.starship_class.lower() not in starship.starship_class.lower():
                return False
        if self.min_cost and (
            starship.cost_in_credits is None or starship.cost_in_credits < self.min_cost
        ):
            return False
        if self.max_cost and (
            starship.cost_in_credits is None or starship.cost_in_credits > self.max_cost
        ):
            return False
        if self.min_length and (starship.length is None or starship.length < self.min_length):
            return False
        if self.max_length and (starship.length is None or starship.length > self.max_length):
            return False
        if self.min_hyperdrive and (
            starship.hyperdrive_rating is None or starship.hyperdrive_rating < self.min_hyperdrive
        ):
            return False
        if self.max_hyperdrive and (
            starship.hyperdrive_rating is None or starship.hyperdrive_rating > self.max_hyperdrive
        ):
            return False
        return True
