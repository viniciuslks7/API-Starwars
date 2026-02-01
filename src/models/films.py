"""Films models."""

from datetime import date, datetime

from pydantic import BaseModel, Field


class FilmSummary(BaseModel):
    """Summary model for film (used in lists)."""

    id: int = Field(..., description="Film ID (episode_id for sorting)")
    episode_id: int = Field(..., description="Episode number")
    title: str = Field(..., description="Film title")
    director: str = Field(..., description="Director name")
    release_date: date | None = Field(None, description="Release date")

    @classmethod
    def from_swapi(cls, data: dict, film_id: int) -> "FilmSummary":
        """Create from SWAPI response."""
        release_date = None
        if data.get("release_date"):
            try:
                release_date = date.fromisoformat(data["release_date"])
            except ValueError:
                pass

        return cls(
            id=film_id,
            episode_id=data.get("episode_id", film_id),
            title=data["title"],
            director=data.get("director", "Unknown"),
            release_date=release_date,
        )


class Film(BaseModel):
    """Full film model with all details."""

    id: int = Field(..., description="Film ID")
    episode_id: int = Field(..., description="Episode number")
    title: str = Field(..., description="Film title")
    opening_crawl: str = Field(..., description="Opening crawl text")
    director: str = Field(..., description="Director name")
    producer: str = Field(..., description="Producer name(s)")
    release_date: date | None = Field(None, description="Release date")
    character_ids: list[int] = Field(default_factory=list, description="Character IDs")
    planet_ids: list[int] = Field(default_factory=list, description="Planet IDs")
    starship_ids: list[int] = Field(default_factory=list, description="Starship IDs")
    vehicle_ids: list[int] = Field(default_factory=list, description="Vehicle IDs")
    species_ids: list[int] = Field(default_factory=list, description="Species IDs")
    created: datetime | None = Field(None, description="Created timestamp")
    edited: datetime | None = Field(None, description="Last edited timestamp")

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
    def from_swapi(cls, data: dict, film_id: int) -> "Film":
        """Create from SWAPI response."""
        release_date = None
        if data.get("release_date"):
            try:
                release_date = date.fromisoformat(data["release_date"])
            except ValueError:
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
            id=film_id,
            episode_id=data.get("episode_id", film_id),
            title=data["title"],
            opening_crawl=data.get("opening_crawl", ""),
            director=data.get("director", "Unknown"),
            producer=data.get("producer", "Unknown"),
            release_date=release_date,
            character_ids=cls._extract_ids(data.get("characters", [])),
            planet_ids=cls._extract_ids(data.get("planets", [])),
            starship_ids=cls._extract_ids(data.get("starships", [])),
            vehicle_ids=cls._extract_ids(data.get("vehicles", [])),
            species_ids=cls._extract_ids(data.get("species", [])),
            created=created,
            edited=edited,
        )
