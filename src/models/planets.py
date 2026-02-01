"""Planets models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class PlanetSummary(BaseModel):
    """Summary model for planet (used in lists)."""

    id: int = Field(..., description="Planet ID")
    name: str = Field(..., description="Planet name")
    climate: str = Field(..., description="Climate type(s)")
    terrain: str = Field(..., description="Terrain type(s)")
    population: int | None = Field(None, description="Population")

    @classmethod
    def from_swapi(cls, data: dict, planet_id: int) -> "PlanetSummary":
        """Create from SWAPI response."""
        population = None
        pop_str = data.get("population", "unknown")
        if pop_str and pop_str != "unknown":
            try:
                population = int(pop_str)
            except ValueError:
                pass

        return cls(
            id=planet_id,
            name=data["name"],
            climate=data.get("climate", "Unknown"),
            terrain=data.get("terrain", "Unknown"),
            population=population,
        )


class Planet(BaseModel):
    """Full planet model with all details."""

    id: int = Field(..., description="Planet ID")
    name: str = Field(..., description="Planet name")
    diameter: int | None = Field(None, description="Diameter in kilometers")
    rotation_period: int | None = Field(None, description="Rotation period in hours")
    orbital_period: int | None = Field(None, description="Orbital period in days")
    gravity: str = Field(..., description="Gravity relative to standard")
    population: int | None = Field(None, description="Population")
    climate: str = Field(..., description="Climate type(s)")
    terrain: str = Field(..., description="Terrain type(s)")
    surface_water: int | None = Field(None, description="Surface water percentage")
    resident_ids: list[int] = Field(default_factory=list, description="Resident character IDs")
    film_ids: list[int] = Field(default_factory=list, description="Film IDs")
    created: datetime | None = Field(None, description="Created timestamp")
    edited: datetime | None = Field(None, description="Last edited timestamp")

    @field_validator("diameter", "rotation_period", "orbital_period", mode="before")
    @classmethod
    def parse_int_field(cls, v: Any) -> int | None:
        """Parse integer fields from string."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            return int(str(v).replace(",", ""))
        except ValueError:
            return None

    @field_validator("population", mode="before")
    @classmethod
    def parse_population(cls, v: Any) -> int | None:
        """Parse population from string to int."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            return int(str(v).replace(",", ""))
        except ValueError:
            return None

    @field_validator("surface_water", mode="before")
    @classmethod
    def parse_surface_water(cls, v: Any) -> int | None:
        """Parse surface water percentage from string."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            return int(float(str(v)))
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
    def from_swapi(cls, data: dict, planet_id: int) -> "Planet":
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
            id=planet_id,
            name=data["name"],
            diameter=data.get("diameter"),
            rotation_period=data.get("rotation_period"),
            orbital_period=data.get("orbital_period"),
            gravity=data.get("gravity", "Unknown"),
            population=data.get("population"),
            climate=data.get("climate", "Unknown"),
            terrain=data.get("terrain", "Unknown"),
            surface_water=data.get("surface_water"),
            resident_ids=cls._extract_ids(data.get("residents", [])),
            film_ids=cls._extract_ids(data.get("films", [])),
            created=created,
            edited=edited,
        )


class PlanetFilter(BaseModel):
    """Filter parameters for planet queries."""

    climate: str | None = Field(None, description="Filter by climate (partial match)")
    terrain: str | None = Field(None, description="Filter by terrain (partial match)")
    min_population: int | None = Field(None, description="Minimum population")
    max_population: int | None = Field(None, description="Maximum population")
    min_diameter: int | None = Field(None, description="Minimum diameter in km")
    max_diameter: int | None = Field(None, description="Maximum diameter in km")

    def apply(self, planet: Planet) -> bool:
        """Check if a planet matches this filter."""
        if self.climate:
            if self.climate.lower() not in planet.climate.lower():
                return False
        if self.terrain:
            if self.terrain.lower() not in planet.terrain.lower():
                return False
        if self.min_population and (
            planet.population is None or planet.population < self.min_population
        ):
            return False
        if self.max_population and (
            planet.population is None or planet.population > self.max_population
        ):
            return False
        if self.min_diameter and (planet.diameter is None or planet.diameter < self.min_diameter):
            return False
        if self.max_diameter and (planet.diameter is None or planet.diameter > self.max_diameter):
            return False
        return True
