"""
Endpoints avançados para Rankings e Analytics.

Funcionalidades:
- Top N personagens por altura/massa
- Top N naves por velocidade/custo
- Top N planetas por população
- Timeline cronológica dos filmes
"""

from fastapi import APIRouter, Depends, Query

from src.dependencies import get_swapi_client
from src.services.swapi_client import SWAPIClient

router = APIRouter(prefix="/api/v1/rankings", tags=["Rankings"])


def _parse_int(value: str | None) -> int | None:
    """Parse string para int, tratando valores 'unknown'."""
    if value is None or value == "unknown" or value == "n/a":
        return None
    try:
        # Remove vírgulas e espaços
        clean = str(value).replace(",", "").replace(" ", "")
        return int(float(clean))
    except (ValueError, TypeError):
        return None


def _parse_float(value: str | None) -> float | None:
    """Parse string para float, tratando valores 'unknown'."""
    if value is None or value == "unknown" or value == "n/a":
        return None
    try:
        clean = str(value).replace(",", "").replace(" ", "")
        return float(clean)
    except (ValueError, TypeError):
        return None


def _extract_id(url: str) -> int:
    """Extrai ID numérico de uma URL SWAPI."""
    parts = url.rstrip("/").split("/")
    return int(parts[-1])


@router.get(
    "/tallest-characters",
    summary="Top personagens mais altos",
    description="Retorna os N personagens mais altos do universo Star Wars.",
)
async def get_tallest_characters(
    limit: int = Query(10, ge=1, le=50, description="Número de resultados"),
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna os personagens mais altos."""
    all_people = await swapi.get_all_people()

    # Filtrar e ordenar por altura (trabalhando com dicts)
    with_height = []
    for p in all_people:
        height = _parse_int(p.get("height"))
        if height is not None:
            with_height.append(
                {
                    "id": _extract_id(p.get("url", "")),
                    "name": p.get("name"),
                    "height": height,
                    "gender": p.get("gender"),
                }
            )

    sorted_by_height = sorted(with_height, key=lambda x: x["height"], reverse=True)
    return sorted_by_height[:limit]


@router.get(
    "/heaviest-characters",
    summary="Top personagens mais pesados",
    description="Retorna os N personagens mais pesados do universo Star Wars.",
)
async def get_heaviest_characters(
    limit: int = Query(10, ge=1, le=50, description="Número de resultados"),
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna os personagens mais pesados."""
    all_people = await swapi.get_all_people()

    # Filtrar e ordenar por massa
    with_mass = []
    for p in all_people:
        mass = _parse_float(p.get("mass"))
        if mass is not None:
            with_mass.append(
                {
                    "id": _extract_id(p.get("url", "")),
                    "name": p.get("name"),
                    "mass": mass,
                    "gender": p.get("gender"),
                }
            )

    sorted_by_mass = sorted(with_mass, key=lambda x: x["mass"], reverse=True)
    return sorted_by_mass[:limit]


@router.get(
    "/fastest-starships",
    summary="Top naves mais rápidas",
    description="Retorna as N naves com maior velocidade (MGLT).",
)
async def get_fastest_starships(
    limit: int = Query(10, ge=1, le=50, description="Número de resultados"),
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna as naves mais rápidas por MGLT."""
    all_starships = await swapi.get_all_starships()

    # Filtrar e ordenar por MGLT
    with_speed = []
    for s in all_starships:
        mglt = _parse_int(s.get("MGLT"))
        if mglt is not None:
            with_speed.append(
                {
                    "id": _extract_id(s.get("url", "")),
                    "name": s.get("name"),
                    "model": s.get("model"),
                    "mglt": mglt,
                    "starship_class": s.get("starship_class"),
                }
            )

    sorted_by_speed = sorted(with_speed, key=lambda x: x["mglt"], reverse=True)
    return sorted_by_speed[:limit]


@router.get(
    "/most-expensive-starships",
    summary="Top naves mais caras",
    description="Retorna as N naves mais caras em créditos.",
)
async def get_most_expensive_starships(
    limit: int = Query(10, ge=1, le=50, description="Número de resultados"),
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna as naves mais caras."""
    all_starships = await swapi.get_all_starships()

    # Filtrar e ordenar por custo
    with_cost = []
    for s in all_starships:
        cost = _parse_int(s.get("cost_in_credits"))
        if cost is not None:
            with_cost.append(
                {
                    "id": _extract_id(s.get("url", "")),
                    "name": s.get("name"),
                    "model": s.get("model"),
                    "cost_in_credits": cost,
                    "manufacturer": s.get("manufacturer"),
                }
            )

    sorted_by_cost = sorted(with_cost, key=lambda x: x["cost_in_credits"], reverse=True)
    return sorted_by_cost[:limit]


@router.get(
    "/largest-starships",
    summary="Top maiores naves",
    description="Retorna as N maiores naves por comprimento.",
)
async def get_largest_starships(
    limit: int = Query(10, ge=1, le=50, description="Número de resultados"),
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna as maiores naves."""
    all_starships = await swapi.get_all_starships()

    # Filtrar e ordenar por comprimento
    with_length = []
    for s in all_starships:
        length = _parse_float(s.get("length"))
        if length is not None:
            with_length.append(
                {
                    "id": _extract_id(s.get("url", "")),
                    "name": s.get("name"),
                    "model": s.get("model"),
                    "length": length,
                    "starship_class": s.get("starship_class"),
                }
            )

    sorted_by_length = sorted(with_length, key=lambda x: x["length"], reverse=True)
    return sorted_by_length[:limit]


@router.get(
    "/most-populated-planets",
    summary="Top planetas mais populosos",
    description="Retorna os N planetas com maior população.",
)
async def get_most_populated_planets(
    limit: int = Query(10, ge=1, le=50, description="Número de resultados"),
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna os planetas mais populosos."""
    all_planets = await swapi.get_all_planets()

    # Filtrar e ordenar por população
    with_population = []
    for p in all_planets:
        population = _parse_int(p.get("population"))
        if population is not None:
            with_population.append(
                {
                    "id": _extract_id(p.get("url", "")),
                    "name": p.get("name"),
                    "population": population,
                    "climate": p.get("climate"),
                    "terrain": p.get("terrain"),
                }
            )

    sorted_by_population = sorted(with_population, key=lambda x: x["population"], reverse=True)
    return sorted_by_population[:limit]


@router.get(
    "/largest-planets",
    summary="Top maiores planetas",
    description="Retorna os N maiores planetas por diâmetro.",
)
async def get_largest_planets(
    limit: int = Query(10, ge=1, le=50, description="Número de resultados"),
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna os maiores planetas."""
    all_planets = await swapi.get_all_planets()

    # Filtrar e ordenar por diâmetro
    with_diameter = []
    for p in all_planets:
        diameter = _parse_int(p.get("diameter"))
        if diameter is not None:
            with_diameter.append(
                {
                    "id": _extract_id(p.get("url", "")),
                    "name": p.get("name"),
                    "diameter": diameter,
                    "climate": p.get("climate"),
                    "terrain": p.get("terrain"),
                }
            )

    sorted_by_diameter = sorted(with_diameter, key=lambda x: x["diameter"], reverse=True)
    return sorted_by_diameter[:limit]


@router.get(
    "/films-with-most-characters",
    summary="Filmes com mais personagens",
    description="Retorna os filmes ordenados por número de personagens.",
)
async def get_films_by_character_count(
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna filmes ordenados por número de personagens."""
    all_films = await swapi.get_all_films()

    films_data = []
    for f in all_films:
        films_data.append(
            {
                "id": _extract_id(f.get("url", "")),
                "episode_id": f.get("episode_id"),
                "title": f.get("title"),
                "character_count": len(f.get("characters", [])),
                "planet_count": len(f.get("planets", [])),
                "starship_count": len(f.get("starships", [])),
                "release_date": f.get("release_date"),
            }
        )

    return sorted(films_data, key=lambda x: x["character_count"], reverse=True)
