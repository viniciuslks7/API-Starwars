# 🎬 Star Wars API Platform - Apresentação

> **Tempo Total:** 20 minutos  
> **Candidato:** Vinicius (viniciuslks7)  
> **Vaga:** PowerOfData

---

## 📊 Estrutura da Apresentação

| Slide | Título | Tempo | Descrição |
|-------|--------|-------|-----------|
| 1 | Título & Intro | 1 min | Apresentação pessoal |
| 2 | Contexto do Desafio | 2 min | O que foi pedido |
| 3 | Arquitetura Técnica | 3 min | Diagrama e componentes |
| 4 | Stack Tecnológica | 2 min | Tecnologias escolhidas |
| 5 | Features Principais | 3 min | O que foi implementado |
| 6 | Demo ao Vivo | 5 min | Demonstração prática |
| 7 | Qualidade & Testes | 2 min | Testes e cobertura |
| 8 | Diferenciais | 1 min | O que vai além do pedido |
| 9 | Conclusão | 1 min | Próximos passos |

---

## 📝 SLIDE 1: Título e Apresentação

### Star Wars API Platform
**REST API para explorar o universo Star Wars**

- 👤 **Candidato:** Vinicius
- 📧 **GitHub:** viniciuslks7
- 🗓️ **Data:** Fevereiro 2026

---

## 📝 SLIDE 2: Contexto do Desafio

### O que foi pedido:
- ✅ Ambiente GCP (Cloud Run - Free Tier)
- ✅ Python como linguagem principal
- ✅ Consumir SWAPI (swapi.dev)
- ✅ Endpoints com filtros

### Interpretação:
> "Criar uma API robusta, production-ready, que demonstre conhecimento
> em arquitetura de software, boas práticas e cloud."

---

## 📝 SLIDE 3: Arquitetura Técnica

```
┌─────────────────────────────────────────────────────────────┐
│                        CLOUD RUN                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                     FastAPI App                        │  │
│  │  ┌─────────┐  ┌─────────────┐  ┌──────────────────┐   │  │
│  │  │ Routes  │→ │  Services   │→ │   SWAPI Client   │───│──│──→ swapi.dev
│  │  │ (API)   │  │  (Business) │  │  (HTTP + Cache)  │   │  │
│  │  └─────────┘  └─────────────┘  └──────────────────┘   │  │
│  │       ↓              ↓                 ↓              │  │
│  │  ┌─────────┐  ┌─────────────┐  ┌──────────────────┐   │  │
│  │  │ Pydantic│  │   Firebase  │  │  In-Memory Cache │   │  │
│  │  │ Models  │  │    Auth     │  │    (TTL-based)   │   │  │
│  │  └─────────┘  └─────────────┘  └──────────────────┘   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Componentes:**
- **Camada de API:** FastAPI com rotas versionadas (/api/v1/)
- **Camada de Serviços:** Lógica de negócio isolada
- **Camada de Dados:** Cliente SWAPI com cache inteligente
- **Autenticação:** Firebase Auth + API Keys

---

## 📝 SLIDE 4: Stack Tecnológica

| Categoria | Tecnologia | Motivo |
|-----------|------------|--------|
| **Framework** | FastAPI 0.128 | Performance, async, OpenAPI automático |
| **Validação** | Pydantic 2.x | Type safety, validação robusta |
| **HTTP** | httpx | Async, moderno, type hints |
| **Auth** | Firebase Admin | GRATUITO, escalável |
| **Testes** | pytest + coverage | Padrão de mercado |
| **Lint** | Ruff | Rápido, substitui black+isort+flake8 |
| **Deploy** | Cloud Run | GRATUITO (2M req/mês) |

**Python 3.12** - Versão mais recente com melhorias de performance

---

## 📝 SLIDE 5: Features Implementadas

### ✅ Requisitos Obrigatórios
- 6 recursos: People, Films, Starships, Planets, Vehicles, Species
- Filtros avançados por múltiplos campos
- Paginação configurável

### ⭐ Valor Agregado (Extras)
1. **Ordenação customizável** (sort_by, sort_order)
2. **Busca textual** (/search?q=luke)
3. **Consultas correlacionadas** (/people/1/films, /films/1/characters)
4. **Estatísticas** (/statistics/overview, /characters, /films, /planets)
5. **Comparação** (/compare/characters?ids=1&ids=4)
6. **Autenticação** (Firebase JWT + API Keys)
7. **Cache inteligente** (TTL variável por recurso)
8. **48 testes automatizados**

---

## 📝 SLIDE 6: Demo ao Vivo

### Roteiro da Demo (5 minutos)

**1. Health Check (30s)**
```
GET /health
GET /health/ready
```

**2. Listagem com Paginação (1min)**
```
GET /api/v1/people?page=1&page_size=5
GET /api/v1/people?page=2&page_size=5
```

**3. Filtros Avançados (1min)**
```
GET /api/v1/people?gender=female&min_height=150
GET /api/v1/starships?manufacturer=Corellian
```

**4. Ordenação (30s)**
```
GET /api/v1/planets?sort_by=population&sort_order=desc
```

**5. Consultas Correlacionadas (1min)**
```
GET /api/v1/people/1  → Luke Skywalker
GET /api/v1/people/1/films  → Filmes do Luke
GET /api/v1/films/1/characters  → Personagens do filme
```

**6. Estatísticas e Comparação (1min)**
```
GET /api/v1/statistics/overview
GET /api/v1/compare/characters?ids=1&ids=4  → Luke vs Vader
```

---

## 📝 SLIDE 7: Qualidade & Testes

### Cobertura de Testes

| Módulo | Coverage | Status |
|--------|----------|--------|
| Utilitários (pagination, sorting) | 96-100% | ✅ |
| Modelos (Pydantic) | 70-79% | ✅ |
| Cache Service | 98% | ✅ |
| Endpoints de Health | 100% | ✅ |
| **Total** | **50%** | ✅ |

### Tipos de Testes
- **Unit Tests:** Modelos, utilitários, cache
- **Integration Tests:** Endpoints API

### Qualidade de Código
- ✅ Type hints em 100% das funções
- ✅ Docstrings em funções públicas
- ✅ Ruff (lint + format)
- ✅ 48 testes passando

---

## 📝 SLIDE 8: Diferenciais

### O que foi além do pedido:

| Diferencial | Benefício |
|-------------|-----------|
| **Arquitetura em camadas** | Manutenibilidade, testabilidade |
| **OpenAPI automático** | Documentação sempre atualizada |
| **Cache com TTL** | Performance, menos chamadas à SWAPI |
| **Autenticação dupla** | Flexibilidade (JWT ou API Key) |
| **Consultas correlacionadas** | UX melhorada |
| **Endpoints de comparação** | Feature única e útil |
| **Estatísticas agregadas** | Insights do universo SW |
| **100% Free Tier** | Custo zero de operação |

---

## 📝 SLIDE 9: Conclusão

### ✅ Entregue
- API completa e funcional
- Documentação técnica
- Testes automatizados
- Deploy-ready para Cloud Run
- Postman collection

### 🚀 Próximos Passos (se houvesse mais tempo)
1. Cache persistente com Firestore
2. Rate limiting por usuário
3. Métricas e observabilidade
4. CI/CD com GitHub Actions

### 📞 Contato
- **GitHub:** github.com/viniciuslks7
- **Repositório:** github.com/viniciuslks7/API-Starwars

---

## 🎤 Perguntas?

> "May the Force be with you!"

---

# 📋 DICAS PARA APRESENTAÇÃO

## Antes da Apresentação
- [ ] Testar servidor local funcionando
- [ ] Ter Postman aberto com collection carregada
- [ ] Ter VS Code aberto no projeto
- [ ] Ter terminal pronto para comandos

## Durante a Apresentação
- Falar com calma e clareza
- Mostrar código quando relevante
- Na demo, explicar o que está fazendo
- Se algo falhar, ter backup (screenshots)

## Perguntas Frequentes (Prepare-se)

**1. Por que FastAPI e não Flask/Django?**
> FastAPI é async-first, tem melhor performance, gera OpenAPI automaticamente
> e tem validação built-in com Pydantic.

**2. Por que cache in-memory e não Redis?**
> Para manter 100% no free tier. Em produção real, usaria Redis/Memcached.

**3. Como escala?**
> Cloud Run escala automaticamente. Cada instância tem seu cache,
> mas isso é aceitável para dados read-only da SWAPI.

**4. E se a SWAPI cair?**
> O cache serve dados stale temporariamente. Poderia adicionar
> fallback para um banco de dados local.

**5. Por que Firebase Auth?**
> Gratuito, robusto, fácil integração, suporta múltiplos providers.
