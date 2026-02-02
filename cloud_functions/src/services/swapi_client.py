"""Async HTTP client for SWAPI with caching support."""

import asyncio
from typing import Any

import httpx

from src.services.cache_service import CacheService


class SWAPIError(Exception):
    """SWAPI client error."""

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class SWAPIClient:
    """
    Async HTTP client for the Star Wars API.

    Features:
    - Async HTTP requests with httpx
    - Automatic caching with configurable TTL
    - Pagination support for fetching all resources
    - Error handling and retries
    """

    RESOURCES = ["people", "films", "starships", "planets", "vehicles", "species"]

    def __init__(
        self,
        base_url: str = "https://swapi.dev/api",
        cache: CacheService | None = None,
        timeout: float = 30.0,
    ):
        self._base_url = base_url.rstrip("/")
        self._cache = cache or CacheService()
        self._timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=self._timeout,
                headers={"Accept": "application/json"},
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def _fetch(self, url: str) -> dict[str, Any]:
        """
        Fetch URL with caching.

        Checks cache first, then fetches from SWAPI if not cached.
        """
        # Check cache
        cache_key = f"swapi:{url}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        # Fetch from SWAPI
        client = await self._get_client()
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            # Cache the response
            # Use longer TTL for single resources, shorter for lists
            ttl = CacheService.TTL_LONG if "/films/" in url else CacheService.TTL_MEDIUM
            self._cache.set(cache_key, data, ttl)

            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise SWAPIError(f"Resource not found: {url}", 404)
            raise SWAPIError(f"HTTP error: {e.response.status_code}", e.response.status_code)
        except httpx.RequestError as e:
            raise SWAPIError(f"Request error: {str(e)}")

    def _extract_id_from_url(self, url: str) -> int:
        """Extract resource ID from SWAPI URL."""
        return int(url.rstrip("/").split("/")[-1])

    # ==================== People ====================

    async def get_people_page(self, page: int = 1) -> dict[str, Any]:
        """Get a page of people."""
        url = f"{self._base_url}/people/?page={page}"
        return await self._fetch(url)

    async def get_person(self, person_id: int) -> dict[str, Any]:
        """Get a single person by ID."""
        url = f"{self._base_url}/people/{person_id}/"
        data = await self._fetch(url)
        data["id"] = person_id
        return data

    async def get_all_people(self) -> list[dict[str, Any]]:
        """Fetch all people across all pages."""
        return await self._get_all_resources("people")

    async def search_people(self, query: str) -> list[dict[str, Any]]:
        """Search people by name."""
        url = f"{self._base_url}/people/?search={query}"
        data = await self._fetch(url)
        results = data.get("results", [])
        # Add IDs to results
        for item in results:
            if "url" in item:
                item["id"] = self._extract_id_from_url(item["url"])
        return results

    # ==================== Films ====================

    async def get_films_page(self, page: int = 1) -> dict[str, Any]:
        """Get a page of films."""
        url = f"{self._base_url}/films/?page={page}"
        return await self._fetch(url)

    async def get_film(self, film_id: int) -> dict[str, Any]:
        """Get a single film by ID."""
        url = f"{self._base_url}/films/{film_id}/"
        data = await self._fetch(url)
        data["id"] = film_id
        return data

    async def get_all_films(self) -> list[dict[str, Any]]:
        """Fetch all films."""
        return await self._get_all_resources("films")

    # ==================== Starships ====================

    async def get_starships_page(self, page: int = 1) -> dict[str, Any]:
        """Get a page of starships."""
        url = f"{self._base_url}/starships/?page={page}"
        return await self._fetch(url)

    async def get_starship(self, starship_id: int) -> dict[str, Any]:
        """Get a single starship by ID."""
        url = f"{self._base_url}/starships/{starship_id}/"
        data = await self._fetch(url)
        data["id"] = starship_id
        return data

    async def get_all_starships(self) -> list[dict[str, Any]]:
        """Fetch all starships."""
        return await self._get_all_resources("starships")

    async def search_starships(self, query: str) -> list[dict[str, Any]]:
        """Search starships by name or model."""
        url = f"{self._base_url}/starships/?search={query}"
        data = await self._fetch(url)
        results = data.get("results", [])
        for item in results:
            if "url" in item:
                item["id"] = self._extract_id_from_url(item["url"])
        return results

    # ==================== Planets ====================

    async def get_planets_page(self, page: int = 1) -> dict[str, Any]:
        """Get a page of planets."""
        url = f"{self._base_url}/planets/?page={page}"
        return await self._fetch(url)

    async def get_planet(self, planet_id: int) -> dict[str, Any]:
        """Get a single planet by ID."""
        url = f"{self._base_url}/planets/{planet_id}/"
        data = await self._fetch(url)
        data["id"] = planet_id
        return data

    async def get_all_planets(self) -> list[dict[str, Any]]:
        """Fetch all planets."""
        return await self._get_all_resources("planets")

    async def search_planets(self, query: str) -> list[dict[str, Any]]:
        """Search planets by name."""
        url = f"{self._base_url}/planets/?search={query}"
        data = await self._fetch(url)
        results = data.get("results", [])
        for item in results:
            if "url" in item:
                item["id"] = self._extract_id_from_url(item["url"])
        return results

    # ==================== Vehicles ====================

    async def get_vehicles_page(self, page: int = 1) -> dict[str, Any]:
        """Get a page of vehicles."""
        url = f"{self._base_url}/vehicles/?page={page}"
        return await self._fetch(url)

    async def get_vehicle(self, vehicle_id: int) -> dict[str, Any]:
        """Get a single vehicle by ID."""
        url = f"{self._base_url}/vehicles/{vehicle_id}/"
        data = await self._fetch(url)
        data["id"] = vehicle_id
        return data

    async def get_all_vehicles(self) -> list[dict[str, Any]]:
        """Fetch all vehicles."""
        return await self._get_all_resources("vehicles")

    # ==================== Species ====================

    async def get_species_page(self, page: int = 1) -> dict[str, Any]:
        """Get a page of species."""
        url = f"{self._base_url}/species/?page={page}"
        return await self._fetch(url)

    async def get_species(self, species_id: int) -> dict[str, Any]:
        """Get a single species by ID."""
        url = f"{self._base_url}/species/{species_id}/"
        data = await self._fetch(url)
        data["id"] = species_id
        return data

    async def get_all_species(self) -> list[dict[str, Any]]:
        """Fetch all species."""
        return await self._get_all_resources("species")

    # ==================== Generic Methods ====================

    async def _get_all_resources(self, resource: str) -> list[dict[str, Any]]:
        """
        Fetch all resources of a type across all pages.

        Uses concurrent requests for better performance.
        """
        cache_key = f"all:{resource}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached

        # Get first page to know total count
        first_page = await self._fetch(f"{self._base_url}/{resource}/")
        all_results = first_page.get("results", [])

        # Add IDs to first page results
        for item in all_results:
            if "url" in item:
                item["id"] = self._extract_id_from_url(item["url"])

        # Calculate remaining pages
        count = first_page.get("count", 0)
        page_size = len(all_results)
        if page_size == 0:
            return []

        total_pages = (count + page_size - 1) // page_size

        # Fetch remaining pages concurrently
        if total_pages > 1:
            tasks = [
                self._fetch(f"{self._base_url}/{resource}/?page={page}")
                for page in range(2, total_pages + 1)
            ]
            pages = await asyncio.gather(*tasks, return_exceptions=True)

            for page_data in pages:
                if isinstance(page_data, dict):
                    results = page_data.get("results", [])
                    for item in results:
                        if "url" in item:
                            item["id"] = self._extract_id_from_url(item["url"])
                    all_results.extend(results)

        # Cache the combined results
        self._cache.set(cache_key, all_results, CacheService.TTL_MEDIUM)

        return all_results

    async def get_multiple_by_ids(self, resource: str, ids: list[int]) -> list[dict[str, Any]]:
        """
        Fetch multiple resources by their IDs concurrently.

        Args:
            resource: Resource type (people, films, etc.)
            ids: List of resource IDs

        Returns:
            List of resource data
        """
        get_method = getattr(self, f"get_{resource.rstrip('s')}", None)
        if get_method is None:
            # Handle special cases
            if resource == "species":
                get_method = self.get_species
            elif resource == "people":
                get_method = self.get_person
            else:
                raise ValueError(f"Unknown resource: {resource}")

        tasks = [get_method(id_) for id_ in ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out errors
        return [r for r in results if isinstance(r, dict)]
