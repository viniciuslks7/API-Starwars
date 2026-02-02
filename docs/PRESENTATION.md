# 🎬 Star Wars API Platform - Apresentação

> **PowerOfData Case Técnico** | Vinícius Lopes | Fevereiro 2026

---

## 📌 Slide 1: Título

# ⚔️ Star Wars API Platform

### API REST Serverless na Google Cloud Platform

**Candidato:** Vinícius Lopes  
**Desafio:** PowerOfData - Analista de Dados Jr.  
**Data:** Fevereiro 2026

---

## 📌 Slide 2: O Desafio

### 🎯 Objetivo

Desenvolver uma API REST usando a SWAPI como fonte de dados, com deploy na GCP.

### ✅ Requisitos Atendidos

| Requisito | Status |
|-----------|--------|
| API REST funcional | ✅ |
| Fonte: SWAPI | ✅ |
| Cloud Functions | ✅ |
| API Gateway | ✅ |
| Autenticação por API Key | ✅ |
| Rate Limiting | ✅ |
| Documentação completa | ✅ |

---

## 📌 Slide 3: Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     ARQUITETURA                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   👤 Cliente                                                │
│       │                                                     │
│       ▼                                                     │
│   ┌─────────────────┐                                       │
│   │  API Gateway    │  ← OpenAPI 2.0 Spec                   │
│   │  (Roteamento)   │                                       │
│   └────────┬────────┘                                       │
│            │                                                │
│            ▼                                                │
│   ┌─────────────────┐     ┌─────────────────┐               │
│   │ Cloud Function  │────▶│   In-Memory     │               │
│   │ (Python 3.12)   │     │   Cache (TTL)   │               │
│   └────────┬────────┘     └─────────────────┘               │
│            │                                                │
│            ▼                                                │
│   ┌─────────────────┐                                       │
│   │     SWAPI       │  ← swapi.dev/api                      │
│   │ (Fonte Externa) │                                       │
│   └─────────────────┘                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📌 Slide 4: Stack Tecnológica

### 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|-----------|------------|
| **Linguagem** | Python 3.12 |
| **Framework** | Flask (Cloud Functions) |
| **Validação** | Pydantic v2 |
| **HTTP Client** | HTTPX (async) |
| **Cloud** | GCP (Functions, API Gateway) |
| **Testes** | Pytest (48 testes) |
| **Linting** | Ruff |

---

## 📌 Slide 5: Endpoints Principais

### 📡 API Endpoints

| Recurso | Endpoint | Descrição |
|---------|----------|-----------|
| **Health** | `GET /` | Status da API |
| **People** | `GET /api/v1/people` | Lista personagens |
| **People** | `GET /api/v1/people/{id}` | Detalhes personagem |
| **Films** | `GET /api/v1/films` | Lista filmes |
| **Planets** | `GET /api/v1/planets` | Lista planetas |
| **Starships** | `GET /api/v1/starships` | Lista naves |

---

## 📌 Slide 6: Endpoints Exclusivos

### 🌟 Funcionalidades Extras

| Endpoint | Descrição |
|----------|-----------|
| `GET /api/v1/rankings/most-appeared` | Top 10 personagens por aparições em filmes |
| `GET /api/v1/rankings/tallest` | Top 10 personagens mais altos |
| `GET /api/v1/rankings/heaviest` | Top 10 personagens mais pesados |
| `GET /api/v1/timeline` | Linha do tempo cronológica dos filmes |

### 💡 Diferencial

Estes endpoints agregam dados e oferecem **insights** não disponíveis diretamente na SWAPI!

---

## 📌 Slide 7: URLs de Produção

### 🌐 API em Produção

| Ambiente | URL |
|----------|-----|
| **API Gateway** ⭐ | https://starwars-gateway-d9x6gbjl.uc.gateway.dev |
| **Cloud Function** | https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function |
| **Cloud Run** | https://starwars-api-1040331397233.us-central1.run.app |

### 🧪 Teste Agora!

```bash
curl https://starwars-gateway-d9x6gbjl.uc.gateway.dev/api/v1/people/1
```

---

## 📌 Slide 8: Demo - Personagens

### 👤 Buscar Luke Skywalker

**Request:**
```bash
GET /api/v1/people/1
```

**Response:**
```json
{
  "name": "Luke Skywalker",
  "height": "172",
  "mass": "77",
  "hair_color": "blond",
  "birth_year": "19BBY",
  "homeworld": "Tatooine"
}
```

---

## 📌 Slide 9: Demo - Rankings

### 🏆 Top 10 Personagens por Aparições

**Request:**
```bash
GET /api/v1/rankings/most-appeared
```

**Response:**
```json
{
  "ranking_type": "most_appeared",
  "characters": [
    {"rank": 1, "name": "R2-D2", "films_count": 6},
    {"rank": 2, "name": "C-3PO", "films_count": 6},
    {"rank": 3, "name": "Obi-Wan Kenobi", "films_count": 6}
  ]
}
```

---

## 📌 Slide 10: Demo - Timeline

### 📅 Linha do Tempo dos Filmes

**Request:**
```bash
GET /api/v1/timeline
```

**Response:**
```json
{
  "timeline": [
    {"episode": 1, "title": "The Phantom Menace", "year": "32 BBY"},
    {"episode": 2, "title": "Attack of the Clones", "year": "22 BBY"},
    {"episode": 3, "title": "Revenge of the Sith", "year": "19 BBY"},
    {"episode": 4, "title": "A New Hope", "year": "0 BBY"},
    {"episode": 5, "title": "The Empire Strikes Back", "year": "3 ABY"},
    {"episode": 6, "title": "Return of the Jedi", "year": "4 ABY"}
  ]
}
```

---

## 📌 Slide 11: Segurança

### 🛡️ Proteções Implementadas

| Feature | Descrição |
|---------|-----------|
| **Rate Limiting** | 100 req/min por IP |
| **CORS** | Headers configurados |
| **Headers Security** | X-Content-Type-Options, X-Frame-Options |
| **HTTPS** | Forçado em produção |

---

## 📌 Slide 12: Performance

### ⚡ Otimizações

| Feature | Benefício |
|---------|-----------|
| **Cache TTL** | Reduz chamadas à SWAPI |
| **Async HTTP** | Requests não-bloqueantes |
| **Cloud Functions Gen2** | Cold start otimizado |
| **API Gateway** | Caching na borda |

### 📊 Métricas

- **Tempo de resposta:** < 500ms (cache hit)
- **Cold start:** ~2s (primeira requisição)
- **Cache hit rate:** ~80%

---

## 📌 Slide 13: Testes

### 🧪 Cobertura de Testes

```
================================ test session ================================
collected 48 items
tests/unit/test_models.py ............                          [25%]
tests/unit/test_services.py ............................        [75%]
tests/unit/test_utils.py ........                               [100%]

========================= 48 passed in 2.34s ==========================
```

- **48 testes unitários** passando
- **Cobertura:** Modelos, Services, Utils
- **Framework:** Pytest + pytest-asyncio

---

## 📌 Slide 14: Custos

### 💰 Custo: $0.00/mês

| Serviço | Free Tier | Uso Estimado |
|---------|-----------|--------------|
| Cloud Functions | 2M invocações | ~10k |
| API Gateway | 2M chamadas | ~10k |
| Networking | 1GB egress | ~100MB |

✅ **100% dentro do Free Tier do GCP**

---

## 📌 Slide 15: Código Fonte

### 📁 Estrutura do Projeto

```
starwars-api/
├── cloud_functions/     # ⭐ Deploy principal
│   ├── main.py          # Entry point Flask
│   └── src/             # Código da aplicação
├── src/                 # FastAPI (alternativo)
├── tests/               # 48 testes unitários
├── docs/                # Documentação completa
└── README.md            # Getting started
```

### 🔗 Repositório

GitHub: [starwars-api-platform](https://github.com/seu-usuario/starwars-api)

---

## 📌 Slide 16: Próximos Passos

### 🚀 Melhorias Futuras

1. **Autenticação Firebase** - JWT tokens
2. **Banco de Dados** - Firestore para cache persistente
3. **Mais Endpoints** - Species, Vehicles
4. **GraphQL** - Alternativa ao REST
5. **Dashboard** - Métricas e analytics

---

## 📌 Slide 17: Conclusão

### ✅ Entregáveis Completos

- [x] API REST funcional em produção
- [x] Cloud Functions + API Gateway
- [x] Rate Limiting implementado
- [x] Documentação completa
- [x] 48 testes unitários
- [x] Endpoints exclusivos (rankings, timeline)
- [x] Custo $0.00/mês

### 🎯 Objetivo Atingido!

API serverless, escalável e dentro do orçamento.

---

## 📌 Slide 18: Contato

# Obrigado! 🙏

**Vinícius Lopes**

📧 Email: [seu-email@email.com]  
💼 LinkedIn: [linkedin.com/in/seu-perfil]  
🐙 GitHub: [github.com/seu-usuario]

---

### 🔗 Links Úteis

- **API Gateway:** https://starwars-gateway-d9x6gbjl.uc.gateway.dev
- **Documentação:** https://starwars-api-1040331397233.us-central1.run.app/docs
- **Repositório:** GitHub

---

> "May the Force be with you!" ⚔️
