"""Test configuration and fixtures."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.services.cache_service import CacheService
from src.services.swapi_client import SWAPIClient


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def mock_cache():
    """Create a mock cache service."""
    return CacheService(enabled=True, default_ttl=60)


@pytest.fixture
def mock_swapi_client():
    """Create a mock SWAPI client."""
    mock = MagicMock(spec=SWAPIClient)

    # Sample person data
    mock.get_person = AsyncMock(
        return_value={
            "id": 1,
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "skin_color": "fair",
            "eye_color": "blue",
            "birth_year": "19BBY",
            "gender": "male",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "films": ["https://swapi.dev/api/films/1/"],
            "species": [],
            "vehicles": [],
            "starships": ["https://swapi.dev/api/starships/12/"],
            "created": "2014-12-09T13:50:51.644000Z",
            "edited": "2014-12-20T21:17:56.891000Z",
            "url": "https://swapi.dev/api/people/1/",
        }
    )

    mock.get_all_people = AsyncMock(
        return_value=[
            {
                "id": 1,
                "name": "Luke Skywalker",
                "height": "172",
                "mass": "77",
                "hair_color": "blond",
                "skin_color": "fair",
                "eye_color": "blue",
                "birth_year": "19BBY",
                "gender": "male",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": ["https://swapi.dev/api/films/1/"],
                "species": [],
                "vehicles": [],
                "starships": [],
                "url": "https://swapi.dev/api/people/1/",
            },
            {
                "id": 2,
                "name": "C-3PO",
                "height": "167",
                "mass": "75",
                "hair_color": "n/a",
                "skin_color": "gold",
                "eye_color": "yellow",
                "birth_year": "112BBY",
                "gender": "n/a",
                "homeworld": "https://swapi.dev/api/planets/1/",
                "films": ["https://swapi.dev/api/films/1/"],
                "species": ["https://swapi.dev/api/species/2/"],
                "vehicles": [],
                "starships": [],
                "url": "https://swapi.dev/api/people/2/",
            },
        ]
    )

    # Sample film data
    mock.get_film = AsyncMock(
        return_value={
            "id": 1,
            "title": "A New Hope",
            "episode_id": 4,
            "opening_crawl": "It is a period of civil war...",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
            "characters": ["https://swapi.dev/api/people/1/"],
            "planets": ["https://swapi.dev/api/planets/1/"],
            "starships": [],
            "vehicles": [],
            "species": [],
            "created": "2014-12-10T14:23:31.880000Z",
            "edited": "2014-12-20T19:49:45.256000Z",
            "url": "https://swapi.dev/api/films/1/",
        }
    )

    mock.get_all_films = AsyncMock(
        return_value=[
            {
                "id": 1,
                "title": "A New Hope",
                "episode_id": 4,
                "opening_crawl": "It is a period of civil war...",
                "director": "George Lucas",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1977-05-25",
                "characters": ["https://swapi.dev/api/people/1/"],
                "planets": ["https://swapi.dev/api/planets/1/"],
                "starships": [],
                "vehicles": [],
                "species": [],
                "url": "https://swapi.dev/api/films/1/",
            }
        ]
    )

    # Sample planet data
    mock.get_planet = AsyncMock(
        return_value={
            "id": 1,
            "name": "Tatooine",
            "rotation_period": "23",
            "orbital_period": "304",
            "diameter": "10465",
            "climate": "arid",
            "gravity": "1 standard",
            "terrain": "desert",
            "surface_water": "1",
            "population": "200000",
            "residents": ["https://swapi.dev/api/people/1/"],
            "films": ["https://swapi.dev/api/films/1/"],
            "url": "https://swapi.dev/api/planets/1/",
        }
    )

    mock.get_all_planets = AsyncMock(
        return_value=[
            {
                "id": 1,
                "name": "Tatooine",
                "diameter": "10465",
                "climate": "arid",
                "terrain": "desert",
                "population": "200000",
                "residents": [],
                "films": [],
                "url": "https://swapi.dev/api/planets/1/",
            }
        ]
    )

    mock.get_all_starships = AsyncMock(
        return_value=[
            {
                "id": 12,
                "name": "X-wing",
                "model": "T-65 X-wing",
                "manufacturer": "Incom Corporation",
                "starship_class": "Starfighter",
                "cost_in_credits": "149999",
                "length": "12.5",
                "hyperdrive_rating": "1.0",
                "MGLT": "100",
                "cargo_capacity": "110",
                "consumables": "1 week",
                "crew": "1",
                "passengers": "0",
                "max_atmosphering_speed": "1050",
                "pilots": ["https://swapi.dev/api/people/1/"],
                "films": ["https://swapi.dev/api/films/1/"],
                "url": "https://swapi.dev/api/starships/12/",
            }
        ]
    )

    mock.get_all_vehicles = AsyncMock(return_value=[])
    mock.get_all_species = AsyncMock(return_value=[])

    mock.get_multiple_by_ids = AsyncMock(return_value=[])
    mock.search_people = AsyncMock(return_value=[])

    return mock


# Sample test data
SAMPLE_PERSON = {
    "id": 1,
    "name": "Luke Skywalker",
    "height": "172",
    "mass": "77",
    "hair_color": "blond",
    "skin_color": "fair",
    "eye_color": "blue",
    "birth_year": "19BBY",
    "gender": "male",
    "homeworld": "https://swapi.dev/api/planets/1/",
    "films": ["https://swapi.dev/api/films/1/"],
    "species": [],
    "vehicles": [],
    "starships": [],
    "created": "2014-12-09T13:50:51.644000Z",
    "edited": "2014-12-20T21:17:56.891000Z",
    "url": "https://swapi.dev/api/people/1/",
}

SAMPLE_FILM = {
    "id": 1,
    "title": "A New Hope",
    "episode_id": 4,
    "opening_crawl": "It is a period of civil war...",
    "director": "George Lucas",
    "producer": "Gary Kurtz, Rick McCallum",
    "release_date": "1977-05-25",
    "characters": ["https://swapi.dev/api/people/1/"],
    "planets": ["https://swapi.dev/api/planets/1/"],
    "starships": [],
    "vehicles": [],
    "species": [],
    "url": "https://swapi.dev/api/films/1/",
}
