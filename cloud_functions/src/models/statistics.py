"""Statistics models."""

from pydantic import BaseModel, Field


class UniverseOverview(BaseModel):
    """Overview statistics of the Star Wars universe."""

    total_characters: int = Field(..., description="Total number of characters")
    total_planets: int = Field(..., description="Total number of planets")
    total_starships: int = Field(..., description="Total number of starships")
    total_vehicles: int = Field(..., description="Total number of vehicles")
    total_species: int = Field(..., description="Total number of species")
    total_films: int = Field(..., description="Total number of films")
    most_populated_planet: str | None = Field(None, description="Name of most populated planet")
    largest_starship: str | None = Field(None, description="Name of largest starship")
    tallest_character: str | None = Field(None, description="Name of tallest character")


class FilmStatistics(BaseModel):
    """Statistics about films."""

    total_films: int = Field(..., description="Total number of films")
    total_characters_across_films: int = Field(
        ..., description="Sum of characters across all films"
    )
    average_characters_per_film: float = Field(..., description="Average characters per film")
    film_with_most_characters: str | None = Field(None, description="Film with most characters")
    film_with_most_planets: str | None = Field(None, description="Film with most planets")
    earliest_film: str | None = Field(None, description="Earliest released film")
    latest_film: str | None = Field(None, description="Latest released film")


class CharacterStatistics(BaseModel):
    """Demographics and statistics about characters."""

    total_characters: int = Field(..., description="Total number of characters")
    gender_distribution: dict[str, int] = Field(..., description="Count by gender")
    eye_color_distribution: dict[str, int] = Field(..., description="Count by eye color")
    average_height: float | None = Field(None, description="Average height in cm")
    average_mass: float | None = Field(None, description="Average mass in kg")
    tallest_character: str | None = Field(None, description="Name of tallest character")
    heaviest_character: str | None = Field(None, description="Name of heaviest character")


class PlanetStatistics(BaseModel):
    """Statistics about planets."""

    total_planets: int = Field(..., description="Total number of planets")
    climate_distribution: dict[str, int] = Field(..., description="Count by climate type")
    terrain_distribution: dict[str, int] = Field(..., description="Count by terrain type")
    total_population: int = Field(..., description="Sum of all planet populations")
    average_population: float | None = Field(None, description="Average planet population")
    most_populated_planet: str | None = Field(None, description="Most populated planet")
    largest_planet: str | None = Field(None, description="Largest planet by diameter")


class ComparisonResult(BaseModel):
    """Result of comparing multiple entities."""

    entity_type: str = Field(..., description="Type of entities being compared")
    entities: list[dict] = Field(..., description="List of entities with their attributes")
    comparison_fields: list[str] = Field(..., description="Fields used for comparison")
