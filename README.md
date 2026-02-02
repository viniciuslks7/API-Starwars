# ⚔️ Star Wars API Platform

> **REST API Serverless na Google Cloud Platform**  
> PowerOfData Case Técnico | Vinícius Oliveira | Fevereiro 2026

---

## 🌐 Live Demo

| Ambiente | URL | Descrição |
|----------|-----|-----------|
| **Cloud Function** ⭐ | https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function | Backend principal |
| **Frontend** | `frontend/index.html` (local) | Interface visual |
| API Gateway | https://starwars-gateway-d9x6gbjl.uc.gateway.dev | Roteamento |
| Cloud Run | https://starwars-api-1040331397233.us-central1.run.app | Deploy alternativo |

### 🧪 Teste Agora!

```bash
# Health Check
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/

# Buscar Luke Skywalker
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/people/1

# Listar filmes
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/films

# Top 10 personagens mais altos
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/rankings/tallest-characters

# Linha do tempo dos filmes (ordem cronológica)
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/timeline/films/chronological

# Proxy de imagem (personagem)
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/images/characters/1
```

---

## 🚀 Features

### Core
- ✅ **REST API** completa com endpoints CRUD
- ✅ **Cache inteligente** com TTL por recurso
- ✅ **Rate Limiting** (100 req/min por IP)
- ✅ **CORS** configurado para frontend
- ✅ **OpenAPI/Swagger** documentação automática

### Endpoints Exclusivos
- 🏆 **Rankings** - Top 10 por aparições, altura, peso
- 📅 **Timeline** - Linha do tempo cronológica dos filmes
- 🔍 **Search** - Busca por nome de personagem

### Infraestrutura
- ☁️ **Cloud Functions Gen2** - Compute serverless
- 🌐 **API Gateway** - Roteamento e OpenAPI
- 🐳 **Cloud Run** - Deploy alternativo containerizado
- 💰 **$0.00/mês** - 100% Free Tier

---

## 🛠️ Tech Stack

| Categoria | Tecnologia |
|-----------|------------|
| **Linguagem** | Python 3.12 |
| **Framework** | Flask (Cloud Functions) / FastAPI (Cloud Run) |
| **Validação** | Pydantic v2 |
| **HTTP Client** | HTTPX (async) |
| **Cloud** | GCP (Functions, API Gateway, Cloud Run) |
| **Testes** | Pytest (48 testes) |
| **Linting** | Ruff |

---

## 📦 Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/starwars-api.git
cd starwars-api

# Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Copie as variáveis de ambiente
copy .env.example .env
# Edite .env com suas configurações
```

---

## 🏃 Executar Localmente

```bash
# Modo desenvolvimento com auto-reload
uvicorn src.main:app --reload --port 8000

# Abrir documentação Swagger
# http://localhost:8000/docs
```

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Teste específico
pytest tests/unit/test_models.py -v
```

**Resultado esperado:** 48 testes passando ✅

---

## 📡 API Endpoints

### Core
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/` | Health check |
| `GET` | `/health` | Health check detalhado |

### People (Personagens)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/people` | Lista paginada |
| `GET` | `/api/v1/people/{id}` | Detalhes |
| `GET` | `/api/v1/people/search?name=` | Busca por nome |

### Films (Filmes)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/films` | Lista todos |
| `GET` | `/api/v1/films/{id}` | Detalhes |

### Planets (Planetas)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/planets` | Lista paginada |
| `GET` | `/api/v1/planets/{id}` | Detalhes |

### Starships (Naves)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/starships` | Lista paginada |
| `GET` | `/api/v1/starships/{id}` | Detalhes |

### Rankings & Timeline ⭐
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/rankings/tallest-characters` | Top 10 mais altos |
| `GET` | `/rankings/fastest-starships` | Top 10 naves mais rápidas |
| `GET` | `/timeline/films/chronological` | Filmes em ordem cronológica |
| `GET` | `/timeline/films/release-order` | Filmes em ordem de lançamento |

### Imagens (Proxy)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/images/characters/{id}` | Imagem do personagem |
| `GET` | `/images/films/{id}` | Pôster do filme |

---

## 📁 Estrutura do Projeto

```
starwars-api/
├── cloud_functions/          # ⭐ Deploy Cloud Functions
│   ├── main.py               # Entry point Flask
│   ├── requirements.txt      # Dependências
│   ├── api_gateway_config.yaml
│   └── src/                  # Código aplicação
│
├── src/                      # FastAPI (Cloud Run)
│   ├── main.py
│   ├── api/                  # Routers
│   ├── services/             # Lógica de negócio
│   └── models/               # Modelos Pydantic
│
├── tests/                    # 48 testes unitários
├── docs/                     # Documentação
│   ├── architecture.md
│   ├── DEPLOY_GUIDE.md
│   └── PRESENTATION.md
│
├── Dockerfile                # Container Cloud Run
├── pyproject.toml            # Config Python/Ruff
└── README.md                 # Este arquivo
```

---

## 🚀 Deploy

Consulte [docs/DEPLOY_GUIDE.md](docs/DEPLOY_GUIDE.md) para instruções completas.

### Deploy Rápido

```bash
# Cloud Function
cd cloud_functions
gcloud functions deploy starwars-api-function --gen2 --runtime=python312 --trigger-http --allow-unauthenticated

# Cloud Run
gcloud builds submit --tag gcr.io/starwars-api-2026/starwars-api
gcloud run deploy starwars-api --image gcr.io/starwars-api-2026/starwars-api --allow-unauthenticated
```

---

## 📚 Documentação

| Arquivo | Descrição |
|---------|-----------|
| [docs/architecture.md](docs/architecture.md) | Arquitetura técnica |
| [docs/DEPLOY_GUIDE.md](docs/DEPLOY_GUIDE.md) | Guia de deploy |
| [docs/PRESENTATION.md](docs/PRESENTATION.md) | Slides apresentação |
| [CLAUDE.md](CLAUDE.md) | Constituição de desenvolvimento |

---

## 📝 License

MIT License

---

> **May the Force be with you!** ⚔️
