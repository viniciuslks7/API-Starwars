"""People/Characters models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class PersonSummary(BaseModel):
    """Summary model for person (used in lists)."""

    id: int = Field(..., description="Person ID")
    name: str = Field(..., description="Person name")
    gender: str = Field(..., description="Person gender")
    birth_year: str = Field(..., description="Birth year (BBY/ABY)")
    homeworld_id: int | None = Field(None, description="Homeworld planet ID")
    films_count: int = Field(0, description="Number of films appeared in")

    @classmethod
    def from_swapi(cls, data: dict, person_id: int) -> "PersonSummary":
        """Create from SWAPI response."""
        homeworld_id = None
        if data.get("homeworld"):
            try:
                homeworld_id = int(data["homeworld"].rstrip("/").split("/")[-1])
            except (ValueError, IndexError):
                pass

        return cls(
            id=person_id,
            name=data["name"],
            gender=data.get("gender", "unknown"),
            birth_year=data.get("birth_year", "unknown"),
            homeworld_id=homeworld_id,
            films_count=len(data.get("films", [])),
        )


class Person(BaseModel):
    """Full person model with all details."""

    id: int = Field(..., description="Person ID")
    name: str = Field(..., description="Person name")
    height: int | None = Field(None, description="Height in centimeters")
    mass: float | None = Field(None, description="Mass in kilograms")
    hair_color: str = Field(..., description="Hair color")
    skin_color: str = Field(..., description="Skin color")
    eye_color: str = Field(..., description="Eye color")
    birth_year: str = Field(..., description="Birth year (BBY/ABY)")
    gender: str = Field(..., description="Gender")
    homeworld_id: int | None = Field(None, description="Homeworld planet ID")
    homeworld_name: str | None = Field(None, description="Homeworld planet name")
    film_ids: list[int] = Field(default_factory=list, description="Film IDs")
    species_ids: list[int] = Field(default_factory=list, description="Species IDs")
    vehicle_ids: list[int] = Field(default_factory=list, description="Vehicle IDs")
    starship_ids: list[int] = Field(default_factory=list, description="Starship IDs")
    created: datetime | None = Field(None, description="Created timestamp")
    edited: datetime | None = Field(None, description="Last edited timestamp")

    @field_validator("height", mode="before")
    @classmethod
    def parse_height(cls, v: Any) -> int | None:
        """Parse height from string to int."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            return int(str(v).replace(",", ""))
        except ValueError:
            return None

    @field_validator("mass", mode="before")
    @classmethod
    def parse_mass(cls, v: Any) -> float | None:
        """Parse mass from string to float."""
        if v is None or v == "unknown" or v == "n/a":
            return None
        try:
            return float(str(v).replace(",", ""))
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
    def from_swapi(cls, data: dict, person_id: int) -> "Person":
        """Create from SWAPI response."""
        homeworld_id = None
        if data.get("homeworld"):
            try:
                homeworld_id = int(data["homeworld"].rstrip("/").split("/")[-1])
            except (ValueError, IndexError):
                pass

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
            id=person_id,
            name=data["name"],
            height=data.get("height"),
            mass=data.get("mass"),
            hair_color=data.get("hair_color", "unknown"),
            skin_color=data.get("skin_color", "unknown"),
            eye_color=data.get("eye_color", "unknown"),
            birth_year=data.get("birth_year", "unknown"),
            gender=data.get("gender", "unknown"),
            homeworld_id=homeworld_id,
            homeworld_name=None,  # Will be populated separately if needed
            film_ids=cls._extract_ids(data.get("films", [])),
            species_ids=cls._extract_ids(data.get("species", [])),
            vehicle_ids=cls._extract_ids(data.get("vehicles", [])),
            starship_ids=cls._extract_ids(data.get("starships", [])),
            created=created,
            edited=edited,
        )


class PersonFilter(BaseModel):
    """Filter parameters for people queries."""

    gender: str | None = Field(None, description="Filter by gender")
    eye_color: str | None = Field(None, description="Filter by eye color")
    hair_color: str | None = Field(None, description="Filter by hair color")
    homeworld_id: int | None = Field(None, description="Filter by homeworld ID")
    min_height: int | None = Field(None, description="Minimum height in cm")
    max_height: int | None = Field(None, description="Maximum height in cm")
    min_mass: float | None = Field(None, description="Minimum mass in kg")
    max_mass: float | None = Field(None, description="Maximum mass in kg")

    def apply(self, person: Person) -> bool:
        """Check if a person matches this filter."""
        if self.gender and person.gender.lower() != self.gender.lower():
            return False
        if self.eye_color and person.eye_color.lower() != self.eye_color.lower():
            return False
        if self.hair_color and person.hair_color.lower() != self.hair_color.lower():
            return False
        if self.homeworld_id and person.homeworld_id != self.homeworld_id:
            return False
        if self.min_height and (person.height is None or person.height < self.min_height):
            return False
        if self.max_height and (person.height is None or person.height > self.max_height):
            return False
        if self.min_mass and (person.mass is None or person.mass < self.min_mass):
            return False
        if self.max_mass and (person.mass is None or person.mass > self.max_mass):
            return False
        return True
