"""
Endpoint de Timeline cronológica do universo Star Wars.

Funcionalidades:
- Cronologia de filmes por data de lançamento
- Cronologia de filmes por ordem dos episódios (in-universe)
- Eventos significativos do universo
"""

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_swapi_client
from src.services.swapi_client import SWAPIClient

router = APIRouter(prefix="/api/v1/timeline", tags=["Timeline"])


def _extract_id(url: str) -> int:
    """Extrai ID numérico de uma URL SWAPI."""
    parts = url.rstrip("/").split("/")
    return int(parts[-1])


@router.get(
    "/films/release-order",
    summary="Filmes por ordem de lançamento",
    description="Retorna os filmes ordenados por data de lançamento real.",
)
async def get_films_release_order(
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna filmes em ordem de lançamento."""
    all_films = await swapi.get_all_films()

    films_data = []
    for f in all_films:
        episode_id = f.get("episode_id", 0)
        films_data.append(
            {
                "id": _extract_id(f.get("url", "")),
                "episode_id": episode_id,
                "title": f.get("title"),
                "release_date": f.get("release_date"),
                "director": f.get("director"),
                "era": _get_film_era(episode_id),
            }
        )

    # Ordenar por data de lançamento
    return sorted(
        films_data,
        key=lambda x: x["release_date"] or "9999-99-99",
    )


@router.get(
    "/films/chronological",
    summary="Filmes em ordem cronológica (in-universe)",
    description="Retorna os filmes na ordem cronológica da história Star Wars.",
)
async def get_films_chronological_order(
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> list[dict]:
    """Retorna filmes em ordem cronológica do universo."""
    all_films = await swapi.get_all_films()

    films_data = []
    for f in all_films:
        episode_id = f.get("episode_id", 0)
        films_data.append(
            {
                "id": _extract_id(f.get("url", "")),
                "episode_id": episode_id,
                "title": f.get("title"),
                "release_date": f.get("release_date"),
                "director": f.get("director"),
                "era": _get_film_era(episode_id),
                "chronological_order": _get_chronological_order(episode_id),
            }
        )

    # Ordenar por ordem cronológica (episódio)
    return sorted(films_data, key=lambda x: x["chronological_order"])


@router.get(
    "/eras",
    summary="Eras do universo Star Wars",
    description="Retorna informações sobre as diferentes eras do universo Star Wars.",
)
async def get_star_wars_eras() -> list[dict]:
    """Retorna as eras do universo Star Wars."""
    return [
        {
            "name": "Prequel Era",
            "description": "A ascensão e queda da República Galáctica",
            "episodes": [1, 2, 3],
            "key_events": [
                "Descoberta de Anakin Skywalker",
                "Guerras Clônicas",
                "Queda da República",
                "Nascimento de Luke e Leia",
            ],
        },
        {
            "name": "Original Trilogy Era",
            "description": "A Rebelião contra o Império Galáctico",
            "episodes": [4, 5, 6],
            "key_events": [
                "Destruição de Alderaan",
                "Batalha de Yavin (Death Star I)",
                "Revelação 'Eu sou seu pai'",
                "Batalha de Endor (Death Star II)",
                "Redenção de Darth Vader",
            ],
        },
        {
            "name": "Sequel Era",
            "description": "A resistência contra a Primeira Ordem",
            "episodes": [7, 8, 9],
            "key_events": [
                "Despertar de Rey",
                "Destruição da Starkiller Base",
                "Retorno de Palpatine",
            ],
            "note": "Episódios 7-9 não estão disponíveis na SWAPI",
        },
    ]


@router.get(
    "/character-journey/{character_id}",
    summary="Jornada de um personagem",
    description="Retorna a linha do tempo de aparições de um personagem nos filmes.",
)
async def get_character_journey(
    character_id: int,
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> dict:
    """Retorna a jornada de um personagem através dos filmes."""
    try:
        person = await swapi.get_person(character_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Personagem não encontrado") from None

    all_films = await swapi.get_all_films()

    # Extrair IDs dos filmes do personagem
    person_film_urls = person.get("films", [])
    person_film_ids = [_extract_id(url) for url in person_film_urls]

    # Filtrar filmes em que o personagem aparece
    character_films = [f for f in all_films if _extract_id(f.get("url", "")) in person_film_ids]

    # Ordenar por episódio
    character_films.sort(key=lambda x: x.get("episode_id", 0))

    journey = []
    for film in character_films:
        episode_id = film.get("episode_id", 0)
        journey.append(
            {
                "episode_id": episode_id,
                "title": film.get("title"),
                "release_date": film.get("release_date"),
                "era": _get_film_era(episode_id),
            }
        )

    return {
        "character": {
            "id": character_id,
            "name": person.get("name"),
            "birth_year": person.get("birth_year"),
            "homeworld": person.get("homeworld"),
        },
        "total_films": len(journey),
        "journey": journey,
    }


def _get_film_era(episode_id: int) -> str:
    """Retorna a era do filme baseado no episódio."""
    if episode_id in [1, 2, 3]:
        return "Prequel Era"
    elif episode_id in [4, 5, 6]:
        return "Original Trilogy"
    elif episode_id in [7, 8, 9]:
        return "Sequel Era"
    return "Unknown"


def _get_chronological_order(episode_id: int) -> int:
    """Retorna a ordem cronológica do episódio."""
    # Ordem cronológica: 1, 2, 3, 4, 5, 6 (SWAPI só tem os 6 primeiros)
    return episode_id
