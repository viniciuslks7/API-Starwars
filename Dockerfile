# =============================================================================
# Star Wars API Platform - Dockerfile para Cloud Run
# =============================================================================
# Multi-stage build otimizado para produção
# Imagem final: ~150MB | Startup: <3s
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Build - Instalar dependências
# -----------------------------------------------------------------------------
FROM python:3.12-slim as builder

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para otimização
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências de build (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas requirements primeiro (cache de layer)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Runtime - Imagem final mínima
# -----------------------------------------------------------------------------
FROM python:3.12-slim as runtime

# Labels para metadados
LABEL maintainer="viniciuslks7" \
      version="1.0.0" \
      description="Star Wars API Platform - REST API consuming SWAPI"

# Criar usuário não-root para segurança
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente de produção
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    # Cloud Run define PORT automaticamente
    PORT=8080 \
    # Modo produção
    DEBUG=false \
    ENVIRONMENT=production

# Copiar dependências instaladas do builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código fonte
COPY src/ ./src/

# Alterar ownership para usuário não-root
RUN chown -R appuser:appgroup /app

# Mudar para usuário não-root
USER appuser

# Expor porta (Cloud Run usa 8080 por padrão)
EXPOSE 8080

# Healthcheck para monitoramento
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Comando de inicialização otimizado para Cloud Run
# - workers: 1 (Cloud Run escala via instâncias)
# - timeout: 0 (Cloud Run gerencia timeout)
# - host: 0.0.0.0 (aceitar conexões externas)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
