"""
Middleware para Rate Limiting, Request Tracking e Headers de Segurança.

Funcionalidades:
- Rate limiting por IP (100 requests/minuto)
- Request ID único para cada requisição
- Headers de segurança (CORS, X-Content-Type-Options)
- Tempo de resposta no header
"""

import time
import uuid
from collections import defaultdict
from collections.abc import Callable
from datetime import datetime, timedelta

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware para controle de rate limiting por IP.

    Limites padrão:
    - 100 requests por minuto por IP
    - Endpoints de health são isentos
    """

    def __init__(
        self,
        app,
        requests_per_minute: int = 100,
        exempt_paths: list[str] | None = None,
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.exempt_paths = exempt_paths or ["/health", "/health/ready", "/docs", "/openapi.json"]
        # Armazena requests por IP: {ip: [(timestamp, count), ...]}
        self._requests: dict[str, list[datetime]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Pular rate limiting para paths isentos
        if any(request.url.path.startswith(path) for path in self.exempt_paths):
            return await call_next(request)

        # Obter IP do cliente (considera proxies)
        client_ip = self._get_client_ip(request)

        # Limpar requests antigos (mais de 1 minuto)
        now = datetime.now()
        cutoff = now - timedelta(minutes=1)
        self._requests[client_ip] = [ts for ts in self._requests[client_ip] if ts > cutoff]

        # Verificar limite
        if len(self._requests[client_ip]) >= self.requests_per_minute:
            return Response(
                content='{"detail": "Rate limit exceeded. Try again in 1 minute."}',
                status_code=429,
                media_type="application/json",
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int((cutoff + timedelta(minutes=1)).timestamp())),
                },
            )

        # Registrar request
        self._requests[client_ip].append(now)

        # Processar request
        response = await call_next(request)

        # Adicionar headers de rate limit
        remaining = self.requests_per_minute - len(self._requests[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Obtém IP real do cliente considerando proxies."""
        # Cloud Run usa X-Forwarded-For
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para tracking de requests.

    Adiciona:
    - X-Request-ID: UUID único para cada request
    - X-Response-Time: Tempo de processamento em ms
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Gerar ou usar Request ID existente
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Registrar tempo de início
        start_time = time.perf_counter()

        # Processar request
        response = await call_next(request)

        # Calcular tempo de resposta
        process_time = (time.perf_counter() - start_time) * 1000  # em ms

        # Adicionar headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{process_time:.2f}ms"

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware para headers de segurança.

    Adiciona headers de segurança recomendados para APIs.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Headers de segurança
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Cache headers para respostas de API
        if request.url.path.startswith("/api/"):
            # Cache por 5 minutos para dados da SWAPI (raramente mudam)
            response.headers["Cache-Control"] = "public, max-age=300"

        return response
