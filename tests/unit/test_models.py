"""Tests for Pydantic models."""

import pytest
from datetime import date, datetime

from src.models.people import Person, PersonFilter, PersonSummary
from src.models.films import Film, FilmSummary
from src.models.starships import Starship, StarshipFilter
from src.models.planets import Planet, PlanetFilter


class TestPersonModel:
    """Tests for Person model."""

    def test_from_swapi(self):
        """Test creating Person from SWAPI data."""
        data = {
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "skin_color": "fair",
            "eye_color": "blue",
            "birth_year": "19BBY",
            "gender": "male",
            "homeworld": "https://swapi.dev/api/planets/1/",
            "films": ["https://swapi.dev/api/films/1/", "https://swapi.dev/api/films/2/"],
            "species": [],
            "vehicles": ["https://swapi.dev/api/vehicles/14/"],
            "starships": ["https://swapi.dev/api/starships/12/"],
            "created": "2014-12-09T13:50:51.644000Z",
            "edited": "2014-12-20T21:17:56.891000Z",
        }
        
        person = Person.from_swapi(data, 1)
        
        assert person.id == 1
        assert person.name == "Luke Skywalker"
        assert person.height == 172
        assert person.mass == 77.0
        assert person.gender == "male"
        assert person.homeworld_id == 1
        assert person.film_ids == [1, 2]
        assert person.vehicle_ids == [14]
        assert person.starship_ids == [12]

    def test_from_swapi_unknown_values(self):
        """Test handling of unknown values."""
        data = {
            "name": "Unknown Character",
            "height": "unknown",
            "mass": "unknown",
            "hair_color": "n/a",
            "skin_color": "unknown",
            "eye_color": "unknown",
            "birth_year": "unknown",
            "gender": "n/a",
            "homeworld": None,
            "films": [],
            "species": [],
            "vehicles": [],
            "starships": [],
        }
        
        person = Person.from_swapi(data, 99)
        
        assert person.height is None
        assert person.mass is None
        assert person.homeworld_id is None

    def test_height_with_comma(self):
        """Test parsing height with comma separator."""
        data = {
            "name": "Tall Character",
            "height": "1,000",
            "mass": "100",
            "hair_color": "black",
            "skin_color": "green",
            "eye_color": "red",
            "birth_year": "unknown",
            "gender": "male",
            "homeworld": None,
            "films": [],
            "species": [],
            "vehicles": [],
            "starships": [],
        }
        
        person = Person.from_swapi(data, 1)
        assert person.height == 1000


class TestPersonFilter:
    """Tests for PersonFilter."""

    def test_filter_by_gender(self):
        """Test filtering by gender."""
        person = Person(
            id=1,
            name="Luke",
            height=172,
            mass=77,
            hair_color="blond",
            skin_color="fair",
            eye_color="blue",
            birth_year="19BBY",
            gender="male",
        )
        
        filter_male = PersonFilter(gender="male")
        filter_female = PersonFilter(gender="female")
        
        assert filter_male.apply(person) is True
        assert filter_female.apply(person) is False

    def test_filter_by_height_range(self):
        """Test filtering by height range."""
        person = Person(
            id=1,
            name="Luke",
            height=172,
            mass=77,
            hair_color="blond",
            skin_color="fair",
            eye_color="blue",
            birth_year="19BBY",
            gender="male",
        )
        
        filter_ok = PersonFilter(min_height=150, max_height=200)
        filter_too_short = PersonFilter(min_height=180)
        filter_too_tall = PersonFilter(max_height=170)
        
        assert filter_ok.apply(person) is True
        assert filter_too_short.apply(person) is False
        assert filter_too_tall.apply(person) is False


class TestFilmModel:
    """Tests for Film model."""

    def test_from_swapi(self):
        """Test creating Film from SWAPI data."""
        data = {
            "title": "A New Hope",
            "episode_id": 4,
            "opening_crawl": "It is a period of civil war...",
            "director": "George Lucas",
            "producer": "Gary Kurtz, Rick McCallum",
            "release_date": "1977-05-25",
            "characters": ["https://swapi.dev/api/people/1/"],
            "planets": ["https://swapi.dev/api/planets/1/"],
            "starships": ["https://swapi.dev/api/starships/2/"],
            "vehicles": [],
            "species": [],
        }
        
        film = Film.from_swapi(data, 1)
        
        assert film.id == 1
        assert film.title == "A New Hope"
        assert film.episode_id == 4
        assert film.director == "George Lucas"
        assert film.release_date == date(1977, 5, 25)
        assert film.character_ids == [1]
        assert film.planet_ids == [1]
        assert film.starship_ids == [2]


class TestStarshipModel:
    """Tests for Starship model."""

    def test_from_swapi(self):
        """Test creating Starship from SWAPI data."""
        data = {
            "name": "X-wing",
            "model": "T-65 X-wing",
            "manufacturer": "Incom Corporation",
            "cost_in_credits": "149999",
            "length": "12.5",
            "max_atmosphering_speed": "1050",
            "crew": "1",
            "passengers": "0",
            "cargo_capacity": "110",
            "consumables": "1 week",
            "hyperdrive_rating": "1.0",
            "MGLT": "100",
            "starship_class": "Starfighter",
            "pilots": ["https://swapi.dev/api/people/1/"],
            "films": ["https://swapi.dev/api/films/1/"],
        }
        
        starship = Starship.from_swapi(data, 12)
        
        assert starship.id == 12
        assert starship.name == "X-wing"
        assert starship.cost_in_credits == 149999
        assert starship.length == 12.5
        assert starship.hyperdrive_rating == 1.0
        assert starship.mglt == 100
        assert starship.pilot_ids == [1]

    def test_mglt_with_unit(self):
        """Test parsing MGLT with unit suffix."""
        data = {
            "name": "Test Ship",
            "model": "Test",
            "manufacturer": "Test",
            "cost_in_credits": "unknown",
            "length": "unknown",
            "max_atmosphering_speed": "n/a",
            "crew": "1",
            "passengers": "0",
            "cargo_capacity": "unknown",
            "consumables": "unknown",
            "hyperdrive_rating": "unknown",
            "MGLT": "100 MGLT",
            "starship_class": "Test",
            "pilots": [],
            "films": [],
        }
        
        starship = Starship.from_swapi(data, 1)
        assert starship.mglt == 100


class TestStarshipFilter:
    """Tests for StarshipFilter."""

    def test_filter_by_manufacturer(self):
        """Test filtering by manufacturer."""
        starship = Starship(
            id=12,
            name="X-wing",
            model="T-65 X-wing",
            starship_class="Starfighter",
            manufacturer="Incom Corporation",
            crew="1",
            passengers="0",
            max_atmosphering_speed="1050",
            consumables="1 week",
        )
        
        filter_match = StarshipFilter(manufacturer="Incom")
        filter_no_match = StarshipFilter(manufacturer="Sienar")
        
        assert filter_match.apply(starship) is True
        assert filter_no_match.apply(starship) is False


class TestPlanetModel:
    """Tests for Planet model."""

    def test_from_swapi(self):
        """Test creating Planet from SWAPI data."""
        data = {
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
        }
        
        planet = Planet.from_swapi(data, 1)
        
        assert planet.id == 1
        assert planet.name == "Tatooine"
        assert planet.diameter == 10465
        assert planet.population == 200000
        assert planet.climate == "arid"
        assert planet.resident_ids == [1]


class TestPlanetFilter:
    """Tests for PlanetFilter."""

    def test_filter_by_climate(self):
        """Test filtering by climate."""
        planet = Planet(
            id=1,
            name="Tatooine",
            gravity="1 standard",
            climate="arid",
            terrain="desert",
        )
        
        filter_match = PlanetFilter(climate="arid")
        filter_no_match = PlanetFilter(climate="temperate")
        
        assert filter_match.apply(planet) is True
        assert filter_no_match.apply(planet) is False

    def test_filter_by_population_range(self):
        """Test filtering by population range."""
        planet = Planet(
            id=1,
            name="Tatooine",
            gravity="1 standard",
            climate="arid",
            terrain="desert",
            population=200000,
        )
        
        filter_ok = PlanetFilter(min_population=100000, max_population=500000)
        filter_too_small = PlanetFilter(min_population=1000000)
        
        assert filter_ok.apply(planet) is True
        assert filter_too_small.apply(planet) is False
