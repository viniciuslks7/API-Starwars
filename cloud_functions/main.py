"""
Cloud Function entry point para Star Wars API Platform.

Esta Cloud Function serve como wrapper HTTP para a API FastAPI,
permitindo deploy no Google Cloud Functions com API Gateway.

Abordagem: Usar FastAPI diretamente via starlette com adaptação ASGI-to-WSGI.
"""

from __future__ import annotations

import asyncio
import json
import json as json_lib
import sys
import urllib.request
from pathlib import Path
from typing import Any

import functions_framework  # type: ignore
from flask import Request, Response, jsonify  # type: ignore

# Adicionar o diretório raiz ao path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Imports do projeto (necessários para runtime)
# isort: off
from src.services.cache_service import CacheService  # noqa: E402  # type: ignore
from src.services.swapi_client import SWAPIClient  # noqa: E402  # type: ignore
# isort: on


# ============================================================================
# EVENT LOOP GLOBAL (reutilizado entre invocações)
# ============================================================================


def get_or_create_event_loop() -> asyncio.AbstractEventLoop:
    """Obtém ou cria um event loop para execução de coroutines."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


def run_async(coro):
    """Executa uma coroutine de forma segura."""
    loop = get_or_create_event_loop()
    return loop.run_until_complete(coro)


# ============================================================================
# CLIENTE SWAPI GLOBAL (reutilizado entre invocações)
# ============================================================================

_swapi_client: SWAPIClient | None = None
_cache_service: CacheService | None = None


def get_swapi_client() -> SWAPIClient:
    """Retorna cliente SWAPI singleton."""
    global _swapi_client, _cache_service

    if _cache_service is None:
        _cache_service = CacheService()

    if _swapi_client is None:
        _swapi_client = SWAPIClient(cache=_cache_service)

    return _swapi_client


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================


def parse_int(value: str | None, default: int | None = None) -> int | None:
    """Parse string para int com fallback."""
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def extract_id(url: str) -> int:
    """Extrai ID numérico de uma URL SWAPI."""
    parts = url.rstrip("/").split("/")
    return int(parts[-1])


def make_response(data: Any, status: int = 200) -> tuple:
    """Cria resposta JSON padronizada."""
    return jsonify(data), status


def make_error(message: str, status: int = 400) -> tuple:
    """Cria resposta de erro padronizada."""
    return jsonify({"error": message, "status": status}), status


# ============================================================================
# PROXY DE IMAGENS
# ============================================================================

# Cache de imagens em memória (para evitar requisições repetidas)
_image_cache: dict = {}

# Cache do mapeamento de personagens Akabab (ID -> URL da imagem)
_character_images: dict | None = None

# Mapeamento manual de personagens que não têm imagem no Akabab (ID SWAPI -> nome correto)
_MANUAL_CHARACTER_MAPPING = {
    "18": "Wedge Antilles",
    "26": "Lobot",
    "28": "Mon Mothma",
    "36": "Roos Tarpals",
    "37": "Rugor Nass",
    "43": "Shmi Skywalker",
    "48": "Ratts Tyerell",
    "49": "Gasgano",
    "50": "Ben Quadinaros",
    "51": "Mace Windu",
    "55": "Adi Gallia",
    "56": "Saesee Tiin",
    "57": "Yarael Poof",
    "66": "Cordé",
    "64": "Luminara Unduli",
    "74": "Dormé",
    "71": "Dexter Jettster",
    "77": "San Hill",
    "79": "Grievous",
    "82": "Sly Moore",
    "83": "Tion Medon",
}

# Pôsteres dos filmes (URLs do TMDB)
_FILM_POSTERS = {
    "1": "https://image.tmdb.org/t/p/w500/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg",  # A New Hope
    "2": "https://image.tmdb.org/t/p/w500/nNAeTmF4CtdSgMDplXTDPOpYzsX.jpg",  # Empire Strikes Back
    "3": "https://image.tmdb.org/t/p/w500/mDCBQNhR6R0PVFucJAkeWrHNfa.jpg",  # Return of the Jedi
    "4": "https://image.tmdb.org/t/p/w500/6wkfovpn7Eq8dYNKaG5PY3q2oq6.jpg",  # The Phantom Menace
    "5": "https://image.tmdb.org/t/p/w500/oZNPzxqM2s5DyVWab09NTQScDQt.jpg",  # Attack of the Clones
    "6": "https://image.tmdb.org/t/p/w500/xfSAoBEm9MNBjmlNcDYLvLSMlnq.jpg",  # Revenge of the Sith
}

# Imagens de naves (URLs do Fandom/Wookieepedia)
_STARSHIP_IMAGES = {
    "2": "https://static.wikia.nocookie.net/starwars/images/3/3a/CR90_corvette.png",  # CR90
    "3": "https://static.wikia.nocookie.net/starwars/images/e/e0/ImperialI-class_SD.png",  # Star Destroyer
    "5": "https://static.wikia.nocookie.net/starwars/images/0/00/Sentinel_LC.png",  # Sentinel
    "9": "https://static.wikia.nocookie.net/starwars/images/b/be/Death_Star_I.png",  # Death Star
    "10": "https://static.wikia.nocookie.net/starwars/images/4/48/Millenniumfalcon2.jpg",  # Millennium Falcon
    "11": "https://static.wikia.nocookie.net/starwars/images/7/72/Ywing.jpg",  # Y-wing
    "12": "https://static.wikia.nocookie.net/starwars/images/4/48/X-wing_Schematics.gif",  # X-wing
    "13": "https://static.wikia.nocookie.net/starwars/images/4/41/TIE_Advanced_x1_starfighter.png",  # TIE Advanced
    "15": "https://static.wikia.nocookie.net/starwars/images/7/7b/Executor_BF2.png",  # Executor
    "17": "https://static.wikia.nocookie.net/starwars/images/e/e8/RebelTransportShip-DB.png",  # Rebel transport
    "21": "https://static.wikia.nocookie.net/starwars/images/f/f8/Slave_I_DICE.png",  # Slave I
    "22": "https://static.wikia.nocookie.net/starwars/images/5/5e/Lambda-class_T-4a_shuttle.png",  # Imperial shuttle
    "23": "https://static.wikia.nocookie.net/starwars/images/3/31/Efoil-TCG.jpg",  # EF76 Nebulon-B
    "27": "https://static.wikia.nocookie.net/starwars/images/d/d4/Calamari_cruiser.png",  # Calamari Cruiser
    "28": "https://static.wikia.nocookie.net/starwars/images/1/1c/A-wing-SWCT.png",  # A-wing
    "29": "https://static.wikia.nocookie.net/starwars/images/6/6e/B-wing-SWCT.png",  # B-wing
    "31": "https://static.wikia.nocookie.net/starwars/images/a/a2/Republic_Cruiser.png",  # Republic Cruiser
    "32": "https://static.wikia.nocookie.net/starwars/images/5/5a/Droidfightership.jpg",  # Vulture Droid
    "39": "https://static.wikia.nocookie.net/starwars/images/1/1d/Naboo_Royal_Starship.png",  # Naboo Royal
    "40": "https://static.wikia.nocookie.net/starwars/images/7/7e/N-1_Starfighter.png",  # N-1 Starfighter
    "41": "https://static.wikia.nocookie.net/starwars/images/3/32/Jedi_Starfighter.png",  # Jedi Starfighter
    "43": "https://static.wikia.nocookie.net/starwars/images/c/c3/H-type_Nubian_yacht.png",  # J-type Diplomatic
    "48": "https://static.wikia.nocookie.net/starwars/images/e/e9/Jedi_Interceptor.png",  # Jedi Interceptor
    "49": "https://static.wikia.nocookie.net/starwars/images/4/47/Invisible_Hand.png",  # Invisible Hand
    "52": "https://static.wikia.nocookie.net/starwars/images/1/17/ATTEside.jpg",  # AT-TE
    "58": "https://static.wikia.nocookie.net/starwars/images/a/a8/Trade_Federation_cruiser.png",  # Trade Fed Cruiser
    "59": "https://static.wikia.nocookie.net/starwars/images/0/03/Theta-class_shuttle.png",  # Theta-class shuttle
    "61": "https://static.wikia.nocookie.net/starwars/images/4/47/RepublicAttackCruiser-TCW.png",  # Venator
    "63": "https://static.wikia.nocookie.net/starwars/images/7/74/RepublicAssaultShip-class.png",  # Acclamator
    "64": "https://static.wikia.nocookie.net/starwars/images/c/c6/Arc170-TFOWM.jpg",  # ARC-170
    "65": "https://static.wikia.nocookie.net/starwars/images/5/5d/BankingClanFrigate-DB.png",  # Banking Clan
    "66": "https://static.wikia.nocookie.net/starwars/images/2/21/Bellicose_Separatist_cruiser.png",  # Recusant
    "68": "https://static.wikia.nocookie.net/starwars/images/c/c3/Jedistarfighter_negvv.jpg",  # Jedi Starfighter Ep3
    "74": "https://static.wikia.nocookie.net/starwars/images/4/47/TriFighter.png",  # Tri-Fighter
    "75": "https://static.wikia.nocookie.net/starwars/images/5/53/SoullessOne-FF.png",  # Belbullab-22
}


def _load_character_images() -> dict:
    """Carrega mapeamento de imagens do Akabab Star Wars API."""
    global _character_images
    if _character_images is not None:
        return _character_images

    try:
        req = urllib.request.Request(
            "https://akabab.github.io/starwars-api/api/all.json",
            headers={"User-Agent": "StarWarsAPI/1.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json_lib.loads(response.read().decode("utf-8"))
            # Criar mapeamento por ID E por nome (normalizado)
            _character_images = {}
            for char in data:
                _character_images[str(char["id"])] = char.get("image", "")
                # Adicionar por nome normalizado
                name = char.get("name", "").lower().strip()
                if name:
                    _character_images[f"name:{name}"] = char.get("image", "")
            return _character_images
    except Exception:
        _character_images = {}
        return _character_images


def _get_character_image(swapi_id: str) -> str | None:
    """Obtém URL da imagem de personagem, usando mapeamento manual se necessário."""
    char_images = _load_character_images()

    # Primeiro tentar ID direto
    if swapi_id in char_images and char_images[swapi_id]:
        return char_images[swapi_id]

    # Se não encontrar, tentar mapeamento manual por nome
    if swapi_id in _MANUAL_CHARACTER_MAPPING:
        name = _MANUAL_CHARACTER_MAPPING[swapi_id].lower().strip()
        name_key = f"name:{name}"
        if name_key in char_images and char_images[name_key]:
            return char_images[name_key]

    return None


def handle_image_proxy(request: Request) -> tuple:
    """
    Proxy para imagens de Star Wars.

    Usa múltiplas fontes:
    - Characters: Akabab API (imagens do Wikia/Fandom)
    - Films: TMDB posters
    - Starships: Wookieepedia images

    Endpoints:
        GET /images/characters/{id} - Imagem de personagem
        GET /images/films/{id} - Poster de filme
        GET /images/starships/{id} - Imagem de nave
    """
    path_parts = request.path.strip("/").split("/")

    if len(path_parts) < 3:
        return make_error("Formato: /images/{type}/{id}", 400)

    img_type = path_parts[1]  # characters, films, etc
    img_id = path_parts[2]

    # Validar tipo
    valid_types = ["characters", "films", "starships", "planets", "species", "vehicles"]
    if img_type not in valid_types:
        return make_error(f"Tipo inválido. Use: {', '.join(valid_types)}", 400)

    cache_key = f"{img_type}/{img_id}"

    # Verificar cache de imagem
    if cache_key in _image_cache:
        img_data, content_type = _image_cache[cache_key]
        return Response(img_data, mimetype=content_type), 200

    # Determinar URL da imagem baseado no tipo
    img_url = None

    if img_type == "characters":
        # Usar Akabab API para personagens com fallback para mapeamento manual
        img_url = _get_character_image(img_id)
    elif img_type == "films":
        # Usar pôsteres do TMDB
        img_url = _FILM_POSTERS.get(img_id)
    elif img_type == "starships":
        # Usar imagens do Wookieepedia
        img_url = _STARSHIP_IMAGES.get(img_id)

    if not img_url:
        # Placeholder SVG estilizado para cada tipo
        icons = {
            "characters": "👤",
            "films": "🎬",
            "starships": "🚀",
            "planets": "🌍",
            "species": "👽",
            "vehicles": "🚗",
        }
        icon = icons.get(img_type, "★")
        placeholder_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400">
            <defs>
                <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#1a1a2e"/>
                    <stop offset="100%" style="stop-color:#0f0f1a"/>
                </linearGradient>
            </defs>
            <rect fill="url(#bg)" width="300" height="400"/>
            <circle cx="150" cy="150" r="60" fill="#FFE81F" opacity="0.1"/>
            <text x="150" y="170" text-anchor="middle" fill="#FFE81F" font-size="64" font-family="Arial">{icon}</text>
            <text x="150" y="280" text-anchor="middle" fill="#9CA3AF" font-size="16" font-family="Arial">{img_type.title()}</text>
            <text x="150" y="310" text-anchor="middle" fill="#FFE81F" font-size="24" font-family="Arial">#{img_id}</text>
        </svg>"""
        return Response(placeholder_svg, mimetype="image/svg+xml"), 200

    try:
        # Fazer requisição para a imagem do Wikia
        req = urllib.request.Request(
            img_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "image/webp,image/jpeg,image/png,image/*",
                "Referer": "https://starwars.fandom.com/",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            img_data = response.read()
            content_type = response.headers.get("Content-Type", "image/jpeg")

            # Cachear (limite de 50 imagens para não estourar memória)
            if len(_image_cache) < 50:
                _image_cache[cache_key] = (img_data, content_type)

            return Response(img_data, mimetype=content_type), 200

    except Exception:
        # Fallback para placeholder
        placeholder_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400">
            <rect fill="#1a1a2e" width="300" height="400"/>
            <text x="150" y="200" text-anchor="middle" fill="#FFE81F" font-size="48">★</text>
            <text x="150" y="280" text-anchor="middle" fill="#9CA3AF" font-size="14">{img_type}</text>
        </svg>"""
        return Response(placeholder_svg, mimetype="image/svg+xml"), 200


# ============================================================================
# HANDLERS POR RECURSO
# ============================================================================


async def handle_people(request: Request, swapi: SWAPIClient) -> tuple:
    """Handler para /people endpoints."""
    path_parts = request.path.strip("/").split("/")

    # GET /people/search?name=
    if len(path_parts) >= 2 and path_parts[1] == "search":
        name_query = request.args.get("name", "").lower().strip()
        if not name_query:
            return make_error("Parâmetro 'name' é obrigatório", 400)

        all_people = await swapi.get_all_people()

        # Filtrar por nome (case-insensitive, partial match)
        matched = [p for p in all_people if name_query in p.get("name", "").lower()]

        results = []
        for p in matched:
            results.append(
                {
                    "id": extract_id(p.get("url", "")),
                    "name": p.get("name"),
                    "height": p.get("height"),
                    "mass": p.get("mass"),
                    "gender": p.get("gender"),
                    "birth_year": p.get("birth_year"),
                    "films_count": len(p.get("films", [])),
                }
            )

        return make_response(
            {
                "items": results,
                "total": len(results),
                "query": name_query,
            }
        )

    # GET /people
    if len(path_parts) == 1 or (len(path_parts) == 2 and path_parts[1] == ""):
        all_people = await swapi.get_all_people()

        # Aplicar filtros
        gender = request.args.get("gender")
        if gender:
            all_people = [p for p in all_people if p.get("gender", "").lower() == gender.lower()]

        # Paginação
        page = parse_int(request.args.get("page"), 1) or 1
        page_size = parse_int(request.args.get("page_size"), 10) or 10

        # Converter para modelo simplificado
        results = []
        for p in all_people:
            results.append(
                {
                    "id": extract_id(p.get("url", "")),
                    "name": p.get("name"),
                    "height": p.get("height"),
                    "mass": p.get("mass"),
                    "gender": p.get("gender"),
                    "birth_year": p.get("birth_year"),
                    "films_count": len(p.get("films", [])),
                }
            )

        # Paginar
        start = (page - 1) * page_size
        end = start + page_size
        paginated = results[start:end]

        return make_response(
            {
                "items": paginated,
                "total": len(results),
                "page": page,
                "page_size": page_size,
                "total_pages": (len(results) + page_size - 1) // page_size,
            }
        )

    # GET /people/{id}
    if len(path_parts) == 2:
        try:
            person_id = int(path_parts[1])
            person = await swapi.get_person(person_id)

            # Adicionar campos extras
            person["id"] = person_id
            person["films_count"] = len(person.get("films", []))

            # Extrair IDs dos filmes
            film_ids = [extract_id(url) for url in person.get("films", [])]
            person["film_ids"] = film_ids

            return make_response(person)
        except ValueError:
            return make_error("ID inválido", 400)
        except Exception as e:
            return make_error(f"Personagem não encontrado: {e}", 404)

    return make_error("Endpoint não encontrado", 404)


async def handle_films(request: Request, swapi: SWAPIClient) -> tuple:
    """Handler para /films endpoints."""
    path_parts = request.path.strip("/").split("/")

    # GET /films
    if len(path_parts) == 1 or (len(path_parts) == 2 and path_parts[1] == ""):
        all_films = await swapi.get_all_films()

        results = []
        for f in all_films:
            results.append(
                {
                    "id": extract_id(f.get("url", "")),
                    "episode_id": f.get("episode_id"),
                    "title": f.get("title"),
                    "director": f.get("director"),
                    "release_date": f.get("release_date"),
                    "opening_crawl": f.get("opening_crawl", "")[:100] + "...",
                    "characters_count": len(f.get("characters", [])),
                }
            )

        return make_response({"items": results, "total": len(results)})

    # GET /films/{id}
    if len(path_parts) == 2:
        try:
            film_id = int(path_parts[1])
            film = await swapi.get_film(film_id)

            # Adicionar campos extras
            film["id"] = film_id
            film["characters_count"] = len(film.get("characters", []))
            film["character_ids"] = [extract_id(url) for url in film.get("characters", [])]

            return make_response(film)
        except ValueError:
            return make_error("ID inválido", 400)
        except Exception as e:
            return make_error(f"Filme não encontrado: {e}", 404)

    # GET /films/{id}/characters
    if len(path_parts) == 3 and path_parts[2] == "characters":
        try:
            film_id = int(path_parts[1])
            film = await swapi.get_film(film_id)
            character_urls = film.get("characters", [])

            characters = []
            for url in character_urls[:10]:  # Limitar a 10 para performance
                char_id = extract_id(url)
                char = await swapi.get_person(char_id)
                characters.append(
                    {
                        "id": char_id,
                        "name": char.get("name"),
                    }
                )

            return make_response(
                {
                    "film": film.get("title"),
                    "characters": characters,
                    "total": len(character_urls),
                }
            )
        except Exception as e:
            return make_error(f"Erro: {e}", 500)

    return make_error("Endpoint não encontrado", 404)


async def handle_starships(request: Request, swapi: SWAPIClient) -> tuple:
    """Handler para /starships endpoints."""
    path_parts = request.path.strip("/").split("/")

    # GET /starships
    if len(path_parts) == 1 or (len(path_parts) == 2 and path_parts[1] == ""):
        all_starships = await swapi.get_all_starships()

        # Filtros
        manufacturer = request.args.get("manufacturer")
        if manufacturer:
            all_starships = [
                s
                for s in all_starships
                if manufacturer.lower() in s.get("manufacturer", "").lower()
            ]

        results = []
        for s in all_starships:
            results.append(
                {
                    "id": extract_id(s.get("url", "")),
                    "name": s.get("name"),
                    "model": s.get("model"),
                    "manufacturer": s.get("manufacturer"),
                    "starship_class": s.get("starship_class"),
                    "max_atmosphering_speed": s.get("max_atmosphering_speed"),
                    "hyperdrive_rating": s.get("hyperdrive_rating"),
                    "MGLT": s.get("MGLT"),
                    "length": s.get("length"),
                    "crew": s.get("crew"),
                    "passengers": s.get("passengers"),
                }
            )

        # Paginação
        page = parse_int(request.args.get("page"), 1) or 1
        page_size = parse_int(request.args.get("page_size"), 10) or 10
        start = (page - 1) * page_size
        end = start + page_size

        return make_response(
            {
                "items": results[start:end],
                "total": len(results),
                "page": page,
                "page_size": page_size,
            }
        )

    # GET /starships/{id}
    if len(path_parts) == 2:
        try:
            starship_id = int(path_parts[1])
            starship = await swapi.get_starship(starship_id)
            return make_response(starship)
        except ValueError:
            return make_error("ID inválido", 400)
        except Exception as e:
            return make_error(f"Nave não encontrada: {e}", 404)

    return make_error("Endpoint não encontrado", 404)


async def handle_planets(request: Request, swapi: SWAPIClient) -> tuple:
    """Handler para /planets endpoints."""
    path_parts = request.path.strip("/").split("/")

    # GET /planets
    if len(path_parts) == 1 or (len(path_parts) == 2 and path_parts[1] == ""):
        all_planets = await swapi.get_all_planets()

        # Filtros
        climate = request.args.get("climate")
        if climate:
            all_planets = [
                p for p in all_planets if climate.lower() in p.get("climate", "").lower()
            ]

        results = []
        for p in all_planets:
            results.append(
                {
                    "id": extract_id(p.get("url", "")),
                    "name": p.get("name"),
                    "climate": p.get("climate"),
                    "terrain": p.get("terrain"),
                    "population": p.get("population"),
                }
            )

        return make_response({"items": results, "total": len(results)})

    # GET /planets/{id}
    if len(path_parts) == 2:
        try:
            planet_id = int(path_parts[1])
            planet = await swapi.get_planet(planet_id)
            return make_response(planet)
        except ValueError:
            return make_error("ID inválido", 400)
        except Exception as e:
            return make_error(f"Planeta não encontrado: {e}", 404)

    return make_error("Endpoint não encontrado", 404)


async def handle_rankings(request: Request, swapi: SWAPIClient) -> tuple:
    """Handler para /rankings endpoints."""
    path_parts = request.path.strip("/").split("/")

    limit = parse_int(request.args.get("limit"), 10)

    # GET /rankings/tallest-characters
    if len(path_parts) >= 2 and path_parts[1] == "tallest-characters":
        all_people = await swapi.get_all_people()

        with_height = []
        for p in all_people:
            try:
                height = int(p.get("height", "0").replace(",", ""))
                with_height.append(
                    {
                        "id": extract_id(p.get("url", "")),
                        "name": p.get("name"),
                        "height": height,
                        "gender": p.get("gender"),
                    }
                )
            except (ValueError, TypeError):
                continue

        sorted_list = sorted(with_height, key=lambda x: x["height"], reverse=True)
        return make_response(sorted_list[:limit])

    # GET /rankings/heaviest (mais pesados)
    if len(path_parts) >= 2 and path_parts[1] == "heaviest":
        all_people = await swapi.get_all_people()

        with_mass = []
        for p in all_people:
            try:
                mass_str = p.get("mass", "0").replace(",", "").replace("unknown", "0")
                mass = int(float(mass_str))
                if mass > 0:
                    with_mass.append(
                        {
                            "id": extract_id(p.get("url", "")),
                            "name": p.get("name"),
                            "mass": mass,
                            "height": p.get("height"),
                            "gender": p.get("gender"),
                        }
                    )
            except (ValueError, TypeError):
                continue

        sorted_list = sorted(with_mass, key=lambda x: x["mass"], reverse=True)
        return make_response(sorted_list[:limit])

    # GET /rankings/most-appeared (mais aparições em filmes)
    if len(path_parts) >= 2 and path_parts[1] == "most-appeared":
        all_people = await swapi.get_all_people()

        with_films = []
        for p in all_people:
            films_count = len(p.get("films", []))
            with_films.append(
                {
                    "id": extract_id(p.get("url", "")),
                    "name": p.get("name"),
                    "films_count": films_count,
                    "gender": p.get("gender"),
                }
            )

        sorted_list = sorted(with_films, key=lambda x: x["films_count"], reverse=True)
        return make_response(sorted_list[:limit])

    # GET /rankings/fastest-starships
    if len(path_parts) >= 2 and path_parts[1] == "fastest-starships":
        all_starships = await swapi.get_all_starships()

        with_speed = []
        for s in all_starships:
            try:
                mglt = int(s.get("MGLT", "0"))
                with_speed.append(
                    {
                        "id": extract_id(s.get("url", "")),
                        "name": s.get("name"),
                        "model": s.get("model"),
                        "mglt": mglt,
                    }
                )
            except (ValueError, TypeError):
                continue

        sorted_list = sorted(with_speed, key=lambda x: x["mglt"], reverse=True)
        return make_response(sorted_list[:limit])

    return make_error("Ranking não encontrado", 404)


async def handle_timeline(request: Request, swapi: SWAPIClient) -> tuple:
    """Handler para /timeline endpoints."""
    path_parts = request.path.strip("/").split("/")

    # GET /timeline/films/chronological
    if "chronological" in path_parts:
        all_films = await swapi.get_all_films()

        films = []
        for f in all_films:
            films.append(
                {
                    "id": extract_id(f.get("url", "")),
                    "episode_id": f.get("episode_id"),
                    "title": f.get("title"),
                    "release_date": f.get("release_date"),
                }
            )

        sorted_films = sorted(films, key=lambda x: x["episode_id"])
        return make_response(sorted_films)

    # GET /timeline/films/release-order
    if "release-order" in path_parts:
        all_films = await swapi.get_all_films()

        films = []
        for f in all_films:
            films.append(
                {
                    "id": extract_id(f.get("url", "")),
                    "episode_id": f.get("episode_id"),
                    "title": f.get("title"),
                    "release_date": f.get("release_date"),
                }
            )

        sorted_films = sorted(films, key=lambda x: x.get("release_date", ""))
        return make_response(sorted_films)

    return make_error("Timeline não encontrada", 404)


async def handle_health(request: Request) -> tuple:
    """Handler para health check."""
    return make_response(
        {
            "status": "healthy",
            "service": "Star Wars API Platform",
            "version": "1.0.0",
            "platform": "Google Cloud Functions",
        }
    )


# ============================================================================
# ENTRY POINT PRINCIPAL
# ============================================================================


@functions_framework.http
def starwars_api(request: Request):
    """
    Entry point principal da Cloud Function.

    Roteia requisições para os handlers apropriados baseado no path.

    Args:
        request: Flask Request object

    Returns:
        Response: JSON response
    """
    # CORS headers
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    # Headers padrão
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
    }

    path = request.path.strip("/")

    # Remove prefixo /api/v1/ se existir (para compatibilidade)
    if path.startswith("api/v1/"):
        path = path[7:]  # Remove "api/v1/"
    elif path.startswith("api/"):
        path = path[4:]  # Remove "api/"

    swapi = get_swapi_client()

    # Roteamento
    try:
        if path == "" or path == "health":
            result = run_async(handle_health(request))
        elif path.startswith("images"):
            # Proxy de imagens (síncrono) - retorno especial com headers de imagem
            response, status = handle_image_proxy(request)
            img_headers = {
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "public, max-age=86400",  # Cache 24h
            }
            return (response.get_data(), status, img_headers)
        elif path.startswith("people"):
            result = run_async(handle_people(request, swapi))
        elif path.startswith("films"):
            result = run_async(handle_films(request, swapi))
        elif path.startswith("starships"):
            result = run_async(handle_starships(request, swapi))
        elif path.startswith("planets"):
            result = run_async(handle_planets(request, swapi))
        elif path.startswith("rankings"):
            result = run_async(handle_rankings(request, swapi))
        elif path.startswith("timeline"):
            result = run_async(handle_timeline(request, swapi))
        else:
            result = make_error(f"Endpoint não encontrado: /{path}", 404)

        response, status = result
        return (response.get_data(), status, response_headers)

    except Exception as e:
        return (
            json.dumps({"error": "Internal Server Error", "message": str(e)}),
            500,
            response_headers,
        )
