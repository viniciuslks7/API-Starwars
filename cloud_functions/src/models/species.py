"""Species models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class SpeciesSummary(BaseModel):
    """Summary model for species (used in lists)."""

    id: int = Field(..., description="Species ID")
    name: str = Field(..., description="Species name")
    classification: str = Field(..., description="Classification")
    designation: str = Field(..., description="Designation (sentient/non-sentient)")
    language: str = Field(..., description="Language spoken")

    @classmethod
    def from_swapi(cls, data: dict, species_id: int) -> "SpeciesSummary":
        """Create from SWAPI response."""
        return cls(
            id=species_id,
            name=data["name"],
            classification=data.get("classification", "Unknown"),
            designation=data.get("designation", "Unknown"),
            language=data.get("language", "Unknown"),
        )


class Species(BaseModel):
    """Full species model with all details."""

    id: int = Field(..., description="Species ID")
    name: str = Field(..., description="Species name")
    classification: str = Field(..., description="Classification")
    designation: str = Field(..., description="Designation")
    average_height: int | None = Field(None, description="Average height in cm")
    average_lifespan: int | None = Field(None, description="Average lifespan in years")
    eye_colors: str = Field(..., description="Common eye colors")
    hair_colors: str = Field(..., description="Common hair colors")
    skin_colors: str = Field(..., description="Common skin colors")
    language: str = Field(..., description="Language spoken")
    homeworld_id: int | None = Field(None, description="Homeworld planet ID")
    people_ids: list[int] = Field(default_factory=list, description="People IDs of this species")
    film_ids: list[int] = Field(default_factory=list, description="Film IDs")
    created: datetime | None = Field(None, description="Created timestamp")
    edited: datetime | None = Field(None, description="Last edited timestamp")

    @field_validator("average_height", "average_lifespan", mode="before")
    @classmethod
    def parse_int_field(cls, v: Any) -> int | None:
        """Parse integer fields from string."""
        if v is None or v == "unknown" or v == "n/a" or v == "indefinite":
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
    def _extract_id(cls, url: str | None) -> int | None:
        """Extract single ID from SWAPI URL."""
        if not url:
            return None
        try:
            return int(url.rstrip("/").split("/")[-1])
        except (ValueError, IndexError):
            return None

    @classmethod
    def from_swapi(cls, data: dict, species_id: int) -> "Species":
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
            id=species_id,
            name=data["name"],
            classification=data.get("classification", "Unknown"),
            designation=data.get("designation", "Unknown"),
            average_height=data.get("average_height"),
            average_lifespan=data.get("average_lifespan"),
            eye_colors=data.get("eye_colors", "Unknown"),
            hair_colors=data.get("hair_colors", "Unknown"),
            skin_colors=data.get("skin_colors", "Unknown"),
            language=data.get("language", "Unknown"),
            homeworld_id=cls._extract_id(data.get("homeworld")),
            people_ids=cls._extract_ids(data.get("people", [])),
            film_ids=cls._extract_ids(data.get("films", [])),
            created=created,
            edited=edited,
        )
