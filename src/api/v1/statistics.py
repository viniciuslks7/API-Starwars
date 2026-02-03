"""Statistics API endpoints."""

from collections import Counter

from fastapi import APIRouter, HTTPException

from src.dependencies import get_swapi_client
from src.models.films import Film
from src.models.people import Person
from src.models.planets import Planet
from src.models.statistics import (
    CharacterStatistics,
    FilmStatistics,
    PlanetStatistics,
    UniverseOverview,
)
from src.services.swapi_client import SWAPIError

router = APIRouter()


@router.get(
    "/overview",
    response_model=UniverseOverview,
    summary="Universe overview",
    description="Get general statistics about the Star Wars universe.",
)
async def get_universe_overview() -> UniverseOverview:
    """Get overview statistics of the Star Wars universe."""
    swapi = get_swapi_client()

    try:
        # Fetch all resources
        people_data = await swapi.get_all_people()
        planets_data = await swapi.get_all_planets()
        starships_data = await swapi.get_all_starships()
        vehicles_data = await swapi.get_all_vehicles()
        species_data = await swapi.get_all_species()
        films_data = await swapi.get_all_films()

        # Find most populated planet
        most_populated_planet = None
        max_population = 0
        for data in planets_data:
            pop = data.get("population", "unknown")
            if pop != "unknown":
                try:
                    pop_int = int(pop)
                    if pop_int > max_population:
                        max_population = pop_int
                        most_populated_planet = data.get("name")
                except ValueError:
                    pass

        # Find largest starship
        largest_starship = None
        max_length = 0
        for data in starships_data:
            length = data.get("length", "unknown")
            if length != "unknown":
                try:
                    length_float = float(str(length).replace(",", ""))
                    if length_float > max_length:
                        max_length = length_float
                        largest_starship = data.get("name")
                except ValueError:
                    pass

        # Find tallest character
        tallest_character = None
        max_height = 0
        for data in people_data:
            height = data.get("height", "unknown")
            if height != "unknown":
                try:
                    height_int = int(str(height).replace(",", ""))
                    if height_int > max_height:
                        max_height = height_int
                        tallest_character = data.get("name")
                except ValueError:
                    pass

        return UniverseOverview(
            total_characters=len(people_data),
            total_planets=len(planets_data),
            total_starships=len(starships_data),
            total_vehicles=len(vehicles_data),
            total_species=len(species_data),
            total_films=len(films_data),
            most_populated_planet=most_populated_planet,
            largest_starship=largest_starship,
            tallest_character=tallest_character,
        )

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/films",
    response_model=FilmStatistics,
    summary="Film statistics",
    description="Get statistics about Star Wars films.",
)
async def get_film_statistics() -> FilmStatistics:
    """Get statistics about films."""
    swapi = get_swapi_client()

    try:
        films_data = await swapi.get_all_films()
        films = [Film.from_swapi(data, data.get("id", i + 1)) for i, data in enumerate(films_data)]

        # Calculate statistics
        total_characters = sum(len(f.character_ids) for f in films)
        avg_characters = total_characters / len(films) if films else 0

        # Film with most characters
        film_most_chars = max(films, key=lambda f: len(f.character_ids)) if films else None

        # Film with most planets
        film_most_planets = max(films, key=lambda f: len(f.planet_ids)) if films else None

        # Earliest and latest films
        films_with_dates = [f for f in films if f.release_date is not None]
        earliest = min(films_with_dates, key=lambda f: f.release_date) if films_with_dates else None  # type: ignore[arg-type,return-value]
        latest = max(films_with_dates, key=lambda f: f.release_date) if films_with_dates else None  # type: ignore[arg-type,return-value]

        return FilmStatistics(
            total_films=len(films),
            total_characters_across_films=total_characters,
            average_characters_per_film=round(avg_characters, 1),
            film_with_most_characters=film_most_chars.title if film_most_chars else None,
            film_with_most_planets=film_most_planets.title if film_most_planets else None,
            earliest_film=earliest.title if earliest else None,
            latest_film=latest.title if latest else None,
        )

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/characters",
    response_model=CharacterStatistics,
    summary="Character statistics",
    description="Get demographics and statistics about characters.",
)
async def get_character_statistics() -> CharacterStatistics:
    """Get statistics about characters."""
    swapi = get_swapi_client()

    try:
        people_data = await swapi.get_all_people()
        people = [Person.from_swapi(data, data["id"]) for data in people_data]

        # Gender distribution
        gender_counts = Counter(p.gender for p in people)

        # Eye color distribution
        eye_color_counts = Counter(p.eye_color for p in people)

        # Height statistics
        heights = [p.height for p in people if p.height is not None]
        avg_height = sum(heights) / len(heights) if heights else None

        # Mass statistics
        masses = [p.mass for p in people if p.mass is not None]
        avg_mass = sum(masses) / len(masses) if masses else None

        # Tallest and heaviest
        tallest = max(people, key=lambda p: p.height or 0) if people else None
        heaviest = max(people, key=lambda p: p.mass or 0) if people else None

        return CharacterStatistics(
            total_characters=len(people),
            gender_distribution=dict(gender_counts),
            eye_color_distribution=dict(eye_color_counts),
            average_height=round(avg_height, 1) if avg_height else None,
            average_mass=round(avg_mass, 1) if avg_mass else None,
            tallest_character=tallest.name if tallest and tallest.height else None,
            heaviest_character=heaviest.name if heaviest and heaviest.mass else None,
        )

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)


@router.get(
    "/planets",
    response_model=PlanetStatistics,
    summary="Planet statistics",
    description="Get statistics about planets.",
)
async def get_planet_statistics() -> PlanetStatistics:
    """Get statistics about planets."""
    swapi = get_swapi_client()

    try:
        planets_data = await swapi.get_all_planets()
        planets = [Planet.from_swapi(data, data["id"]) for data in planets_data]

        # Climate distribution (split by comma)
        climate_counter: Counter = Counter()
        for p in planets:
            for climate in p.climate.split(","):
                climate_counter[climate.strip()] += 1

        # Terrain distribution (split by comma)
        terrain_counter: Counter = Counter()
        for p in planets:
            for terrain in p.terrain.split(","):
                terrain_counter[terrain.strip()] += 1

        # Population statistics
        populations = [p.population for p in planets if p.population is not None]
        total_pop = sum(populations)
        avg_pop = total_pop / len(populations) if populations else None

        # Most populated
        most_populated = max(planets, key=lambda p: p.population or 0) if planets else None

        # Largest by diameter
        largest = max(planets, key=lambda p: p.diameter or 0) if planets else None

        return PlanetStatistics(
            total_planets=len(planets),
            climate_distribution=dict(climate_counter),
            terrain_distribution=dict(terrain_counter),
            total_population=total_pop,
            average_population=round(avg_pop, 0) if avg_pop else None,
            most_populated_planet=most_populated.name
            if most_populated and most_populated.population
            else None,
            largest_planet=largest.name if largest and largest.diameter else None,
        )

    except SWAPIError as e:
        raise HTTPException(status_code=e.status_code or 500, detail=e.message)
