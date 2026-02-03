# ⚔️ Star Wars API Platform

> **REST API Serverless na Google Cloud Platform**  
> PowerOfData Case Técnico | Vinícius Oliveira | Fevereiro 2026

---

## 🌐 Live Demo

| Ambiente | URL | Descrição |
|----------|-----|-----------|
| **Cloud Function** ⭐ | https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function | Backend principal |
| **Frontend Local** | http://127.0.0.1:8000/frontend/index.html | Interface visual |
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

# Abrir frontend (após iniciar o servidor)
# http://127.0.0.1:8000/frontend/index.html
```

O frontend detecta automaticamente se está rodando localmente e ajusta a URL da API.

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

## 📖 Como Consumir a API

### Base URL

```
# Produção (Cloud Function) - Recomendado
https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function

# Local (desenvolvimento)
http://localhost:8000/api/v1
```

> **Nota:** Na Cloud Function, os endpoints não usam o prefixo `/api/v1`.

### Exemplos de Uso

#### 1. Listar Personagens
```bash
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/people
```

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Luke Skywalker",
      "gender": "male",
      "birth_year": "19BBY",
      "homeworld_id": 1,
      "films_count": 5
    }
  ],
  "total": 82,
  "page": 1,
  "page_size": 10
}
```

#### 2. Buscar Personagem por ID
```bash
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/people/1
```

**Response:**
```json
{
  "id": 1,
  "name": "Luke Skywalker",
  "height": 172,
  "mass": 77,
  "hair_color": "blond",
  "skin_color": "fair",
  "eye_color": "blue",
  "birth_year": "19BBY",
  "gender": "male",
  "homeworld_id": 1,
  "film_ids": [1, 2, 3, 6, 7],
  "starship_ids": [12, 22]
}
```

#### 3. Buscar por Nome
```bash
curl "https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/people/search?name=luke"
```

#### 4. Top 10 Personagens Mais Altos
```bash
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/rankings/tallest-characters
```

**Response:**
```json
[
  {"rank": 1, "id": 20, "name": "Yarael Poof", "value": 264, "unit": "cm"},
  {"rank": 2, "id": 32, "name": "Chewbacca", "value": 228, "unit": "cm"}
]
```

#### 5. Timeline dos Filmes
```bash
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/timeline/films/chronological
```

### Usando com JavaScript (Fetch)

```javascript
const API_URL = 'https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function';

// Listar personagens
const response = await fetch(`${API_URL}/people`);
const data = await response.json();
console.log(data.items);

// Buscar por nome
const searchResponse = await fetch(`${API_URL}/people/search?name=vader`);
const characters = await searchResponse.json();
```

### Usando com Python (requests)

```python
import requests

API_URL = "https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function"

# Listar personagens
response = requests.get(f"{API_URL}/people")
data = response.json()
print(data["items"])

# Buscar personagem específico
response = requests.get(f"{API_URL}/people/1")
luke = response.json()
print(f"Nome: {luke['name']}, Altura: {luke['height']}cm")
```

### Códigos de Resposta

| Código | Descrição |
|--------|-----------|
| `200` | Sucesso |
| `404` | Recurso não encontrado |
| `429` | Rate limit excedido (100 req/min) |
| `500` | Erro interno do servidor |

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
│   └── DEPLOY_GUIDE.md
│
├── frontend/                 # Interface visual (HTML + Tailwind)
│   └── index.html
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
| [CLAUDE.md](CLAUDE.md) | Constituição de desenvolvimento |
| `/docs` no Swagger | Documentação interativa (local) |

---

## 🔗 Links Úteis

- **Swagger UI (local):** http://localhost:8000/docs
- **Frontend (local):** http://localhost:8000/frontend/index.html
- **API Produção:** https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function

---

## 📝 License

MIT License

---

> **May the Force be with you!** ⚔️
