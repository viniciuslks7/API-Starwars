"""
Cloud Function entry point para Star Wars API Platform.

Esta Cloud Function serve como wrapper HTTP para a API FastAPI,
permitindo deploy no Google Cloud Functions com API Gateway.

Abordagem: Usar FastAPI diretamente via starlette com adaptação ASGI-to-WSGI.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

import functions_framework
from flask import Request, jsonify

# Adicionar o diretório raiz ao path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Imports do projeto (necessários para runtime)
from src.services.swapi_client import SWAPIClient  # noqa: E402
from src.services.cache_service import CacheService  # noqa: E402


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

import urllib.request
import json as json_lib
from flask import Response

# Cache de imagens em memória (para evitar requisições repetidas)
_image_cache: dict = {}

# Cache do mapeamento de personagens Akabab (ID -> URL da imagem)
_character_images: dict | None = None


def _load_character_images() -> dict:
    """Carrega mapeamento de imagens do Akabab Star Wars API."""
    global _character_images
    if _character_images is not None:
        return _character_images

    try:
        req = urllib.request.Request(
            "https://akabab.github.io/starwars-api/api/all.json",
            headers={"User-Agent": "StarWarsAPI/1.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json_lib.loads(response.read().decode("utf-8"))
            # Criar mapeamento por ID
            _character_images = {str(char["id"]): char.get("image", "") for char in data}
            return _character_images
    except Exception:
        _character_images = {}
        return _character_images


def handle_image_proxy(request: Request) -> tuple:
    """
    Proxy para imagens de Star Wars.

    Usa Akabab API (imagens do Wikia/Fandom) que são funcionais.

    Endpoints:
        GET /images/characters/{id} - Imagem de personagem
        GET /images/films/{id} - Poster de filme
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
        # Usar Akabab API para personagens
        char_images = _load_character_images()
        img_url = char_images.get(img_id)
    else:
        # Para outros tipos, usar placeholder estilizado
        pass

    if not img_url:
        # Placeholder SVG estilizado
        placeholder_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400">
            <defs>
                <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#1a1a2e"/>
                    <stop offset="100%" style="stop-color:#0f0f1a"/>
                </linearGradient>
            </defs>
            <rect fill="url(#bg)" width="300" height="400"/>
            <circle cx="150" cy="150" r="60" fill="#FFE81F" opacity="0.1"/>
            <text x="150" y="160" text-anchor="middle" fill="#FFE81F" font-size="48" font-family="Arial">★</text>
            <text x="150" y="280" text-anchor="middle" fill="#9CA3AF" font-size="16" font-family="Arial">{img_type.title()}</text>
            <text x="150" y="310" text-anchor="middle" fill="#FFE81F" font-size="24" font-family="Arial">#{img_id}</text>
        </svg>'''
        return Response(placeholder_svg, mimetype="image/svg+xml"), 200

    try:
        # Fazer requisição para a imagem do Wikia
        req = urllib.request.Request(
            img_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "image/webp,image/jpeg,image/png,image/*",
                "Referer": "https://starwars.fandom.com/"
            }
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
        placeholder_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 400">
            <rect fill="#1a1a2e" width="300" height="400"/>
            <text x="150" y="200" text-anchor="middle" fill="#FFE81F" font-size="48">★</text>
            <text x="150" y="280" text-anchor="middle" fill="#9CA3AF" font-size="14">{img_type}</text>
        </svg>'''
        return Response(placeholder_svg, mimetype="image/svg+xml"), 200


# ============================================================================
# HANDLERS POR RECURSO
# ============================================================================


async def handle_people(request: Request, swapi: SWAPIClient) -> tuple:
    """Handler para /people endpoints."""
    path_parts = request.path.strip("/").split("/")

    # GET /people
    if len(path_parts) == 1 or (len(path_parts) == 2 and path_parts[1] == ""):
        all_people = await swapi.get_all_people()

        # Aplicar filtros
        gender = request.args.get("gender")
        if gender:
            all_people = [p for p in all_people if p.get("gender", "").lower() == gender.lower()]

        # Paginação
        page = parse_int(request.args.get("page"), 1)
        page_size = parse_int(request.args.get("page_size"), 10)

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
                }
            )

        return make_response({"items": results, "total": len(results)})

    # GET /films/{id}
    if len(path_parts) == 2:
        try:
            film_id = int(path_parts[1])
            film = await swapi.get_film(film_id)
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
                }
            )

        # Paginação
        page = parse_int(request.args.get("page"), 1)
        page_size = parse_int(request.args.get("page_size"), 10)
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
