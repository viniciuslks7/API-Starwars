# 🤖 CLAUDE.md - Constituição de Desenvolvimento Autônomo

> **Spec-Kit Development Constitution v2.0**  
> Star Wars API Platform | Claude Opus 4.5 Autonomous Agent

---

## 📋 Sumário Executivo

Este documento serve como **constituição de desenvolvimento** para o agente Claude Opus 4.5, estabelecendo diretrizes, padrões, contexto e autonomia para desenvolvimento eficiente do projeto Star Wars API Platform.

**Projeto:** Star Wars API Platform  
**Stack:** FastAPI + Python 3.12 + GCP (Cloud Functions)  
**Status:** ✅ Completo - Pronto para entrega  
**Idioma:** Português (Brasil)  
**Última Atualização:** 2026-02-03

---

# 🎮 SISTEMA DE COMANDOS

## Comandos Principais

| Comando | Descrição | Ação Executada |
|---------|-----------|----------------|
| `/constituicao` | Criar ou atualizar princípios de desenvolvimento | Atualiza este arquivo `CLAUDE.md` |
| `/especificar` | Definir requisitos e user stories | Cria/atualiza specs em `docs/planning/` |
| `/planejar` | Criar planos de implementação técnica | Atualiza `docs/planning/implementation_plan.md` |
| `/tarefas` | Gerar lista de tarefas acionáveis | Atualiza `docs/planning/task.md` com checklist |
| `/implementar` | Executar tarefas pendentes | Implementa código seguindo o plano |
| `/status` | Ver status atual do projeto | Lê e resume `docs/planning/walkthrough.md` |

## Comandos de Qualidade

| Comando | Descrição | Ação Executada |
|---------|-----------|----------------|
| `/clarificar` | Esclarecer áreas subespecificadas | Faz perguntas antes de implementar |
| `/analisar` | Análise de consistência entre artefatos | Verifica se código segue docs |
| `/validar` | Gerar checklist de qualidade | Valida completude e consistência |
| `/testar` | Executar testes e verificar coverage | Roda `pytest` e analisa resultados |
| `/revisar` | Code review do código atual | Analisa código com Ruff + boas práticas |
| `/documentar` | Atualizar documentação | Sincroniza docs com código atual |

## Comandos de Ambiente

| Comando | Descrição | Ação Executada |
|---------|-----------|----------------|
| `/setup` | Configurar ambiente de desenvolvimento | Cria venv, instala deps, copia .env |
| `/servidor` | Iniciar servidor de desenvolvimento | `uvicorn src.main:app --reload` |
| `/limpar` | Limpar caches e arquivos temporários | Remove `__pycache__`, `.pytest_cache` |
| `/formatar` | Formatar código com Ruff | `ruff format src/ tests/` |
| `/lint` | Verificar código com Ruff | `ruff check src/ tests/` |

## 🔄 Fluxo de Trabalho

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FLUXO DE DESENVOLVIMENTO                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1️⃣  /status          → Ver estado atual do projeto                    │
│      ↓                                                                  │
│  2️⃣  /especificar     → Definir o que construir (requisitos)           │
│      ↓                                                                  │
│  3️⃣  /clarificar      → Esclarecer dúvidas (opcional, recomendado)     │
│      ↓                                                                  │
│  4️⃣  /planejar        → Criar plano técnico de implementação           │
│      ↓                                                                  │
│  5️⃣  /tarefas         → Gerar lista de tarefas acionáveis              │
│      ↓                                                                  │
│  6️⃣  /analisar        → Verificar consistência (antes de implementar)  │
│      ↓                                                                  │
│  7️⃣  /implementar     → Executar as tarefas uma a uma                  │
│      ↓                                                                  │
│  8️⃣  /testar          → Rodar testes e verificar coverage              │
│      ↓                                                                  │
│  9️⃣  /revisar         → Code review e ajustes finais                   │
│      ↓                                                                  │
│  🔟  /documentar       → Atualizar docs com mudanças                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 📊 Variáveis de Contexto

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `FEATURE_ATUAL` | Feature sendo desenvolvida | Detectada automaticamente |
| `MODO_AUTONOMO` | Se pode agir sem confirmação | `true` para tarefas seguras |
| `NIVEL_DETALHE` | Quantidade de explicações | `medio` |
| `IDIOMA` | Idioma das respostas | `pt-BR` |
| `RODAR_TESTES` | Rodar testes após mudanças | `true` |
| `ATUALIZAR_DOCS` | Atualizar docs após mudanças | `true` |

---

## 🚨 DOCUMENTAÇÃO CRÍTICA - LEITURA OBRIGATÓRIA

### ⚠️ ANTES de qualquer alteração, SEMPRE consultar estes arquivos NA ORDEM:

| Prioridade | Arquivo | Conteúdo | Quando Consultar |
|------------|---------|----------|------------------|
| 🔴 **1** | `CLAUDE.md` | Esta constituição | **SEMPRE** - início de cada sessão |
| 🔴 **2** | `docs/architecture.md` | Arquitetura completa, diagramas Mermaid, fluxos | Alterações estruturais |
| 🔴 **3** | `docs/planning/task.md` | Checklist [x] feito / [ ] pendente | Ver o que já foi implementado |
| 🔴 **4** | `docs/planning/implementation_plan.md` | Especificações detalhadas de endpoints, modelos | Implementar features |
| 🟡 **5** | `docs/planning/walkthrough.md` | Status atual, servidor, testes | Contexto rápido |
| 🟡 **6** | `README.md` | Setup, instalação, uso | Referência geral |

### 📁 A Pasta `docs/` é a FONTE DA VERDADE

```
docs/                                    # 🔴 PASTA MAIS IMPORTANTE DO PROJETO
│
├── architecture.md                      # 🔴 CRÍTICO - Arquitetura Técnica
│   │
│   ├── 📊 Diagrama Mermaid completo da arquitetura
│   ├── 🔧 Detalhes de cada componente:
│   │   ├── API Gateway Layer (rate limiting, CORS)
│   │   ├── Authentication Layer (Firebase + API Keys)
│   │   ├── Compute Layer (Cloud Functions + FastAPI)
│   │   ├── Data Layer (Cache strategy, TTLs)
│   │   └── External Services (SWAPI)
│   ├── 📡 Todos os endpoints disponíveis
│   ├── 🔄 Fluxo de requisições (sequence diagram)
│   ├── 🛡️ Considerações de segurança
│   └── 📈 Estratégias de escalabilidade
│
└── planning/                            # 🔴 PLANEJAMENTO DETALHADO
    │
    ├── task.md                          # 🔴 CRÍTICO - Checklist Master
    │   ├── ✅ Planning Phase - O que foi planejado
    │   ├── ✅ Setup Phase - O que foi configurado
    │   ├── ✅ Development Phase - O que foi implementado
    │   ├── ⏳ Testing Phase - O que precisa testar
    │   ├── ⏳ Deployment Phase - O que falta para deploy
    │   └── ⏳ Documentation Phase - O que documentar
    │
    ├── implementation_plan.md           # 🔴 CRÍTICO - Especificações
    │   ├── 📁 Estrutura de pastas esperada
    │   ├── 📡 Especificação de TODOS os endpoints:
    │   │   ├── Query parameters suportados
    │   │   ├── Response models esperados
    │   │   └── Exemplos de request/response
    │   ├── 📦 Modelos Pydantic a implementar
    │   ├── 🔐 Estratégia de autenticação
    │   ├── 💾 Estratégia de cache
    │   └── 🧪 Plano de verificação e testes
    │
    └── walkthrough.md                   # 🟡 Status Atual
        ├── 🚀 Servidor rodando? URL?
        ├── ✅ Quantos testes passando?
        ├── 📋 Features implementadas (tabela)
        └── ➡️ Próximos passos sugeridos
```

---

## 🎯 Missão do Projeto

Construir uma API REST production-ready que consome dados da SWAPI (Star Wars API) e oferece funcionalidades avançadas:

- ✅ Autenticação (Firebase JWT + API Keys)
- ✅ Caching inteligente (in-memory + Firestore opcional)
- ✅ Filtragem, ordenação e paginação
- ✅ Queries correlacionadas
- ✅ Estatísticas e comparações
- ✅ Deploy serverless no GCP

---

## 🏗️ Arquitetura do Projeto

```
starwars-api/
├── 📄 CLAUDE.md                 # 🔴 Esta constituição
├── � Dockerfile                # 🚀 Deploy Cloud Run
├── 📄 deploy_cloud_functions.ps1 # 🚀 Script deploy Cloud Functions
├── 📁 docs/                     # 🔴 FONTE DA VERDADE - Ler SEMPRE
│   ├── architecture.md          # Arquitetura técnica completa
│   └── planning/
│       ├── task.md              # Checklist de tarefas
│       └── walkthrough.md       # Status atual
│
├── 📁 cloud_functions/          # Cloud Functions (produção)
│   ├── main.py                  # Handler HTTP para GCP
│   └── requirements.txt         # Deps mínimas para CF
│
├── 📁 frontend/                 # SPA Frontend
│   └── index.html               # Interface web completa
│
├── 📁 src/                      # Código fonte (FastAPI local)
│   ├── main.py                  # FastAPI entry point + StaticFiles
│   ├── config.py                # Pydantic Settings
│   ├── dependencies.py          # Injeção de dependências
│   ├── api/
│   │   ├── health.py            # Health checks
│   │   └── v1/                  # Endpoints v1
│   │       ├── router.py        # Agregador de rotas
│   │       ├── people.py        # Personagens
│   │       ├── films.py         # Filmes
│   │       ├── starships.py     # Naves
│   │       ├── planets.py       # Planetas
│   │       ├── vehicles.py      # Veículos
│   │       ├── species.py       # Espécies
│   │       ├── rankings.py      # Rankings/Top N
│   │       ├── timeline.py      # Timeline filmes
│   │       ├── statistics.py    # Analytics
│   │       └── comparison.py    # Comparações
│   ├── models/                  # Pydantic schemas
│   │   ├── base.py              # PaginatedResponse, ErrorResponse
│   │   ├── people.py            # Person, PersonSummary, PersonFilter
│   │   ├── films.py             # Film, FilmSummary
│   │   ├── starships.py         # Starship, StarshipSummary
│   │   ├── planets.py           # Planet, PlanetSummary
│   │   ├── vehicles.py          # Vehicle, VehicleSummary
│   │   ├── species.py           # Species, SpeciesSummary
│   │   └── statistics.py        # StatisticsResponse
│   ├── services/
│   │   ├── swapi_client.py      # Cliente HTTP async para SWAPI
│   │   └── cache_service.py     # Sistema de cache com TTL
│   └── utils/
│       ├── pagination.py        # Lógica de paginação
│       └── sorting.py           # Lógica de ordenação
│
├── 📁 tests/                    # Testes
│   ├── conftest.py              # Fixtures pytest
│   ├── unit/                    # Testes unitários
│   └── integration/             # Testes de integração
│
└── 📁 .github/
    └── copilot-instructions.md  # Instruções para Copilot/Claude
```

---

## 🔧 Padrões de Código

### Python Style Guide

```python
# ✅ CORRETO: Type hints obrigatórios
async def get_person(person_id: int) -> Person:
    """Busca um personagem por ID."""
    ...

# ✅ CORRETO: Docstrings em todas as funções públicas
class SWAPIClient:
    """Cliente HTTP assíncrono para a Star Wars API."""
    
    async def get_all_people(self) -> list[dict[str, Any]]:
        """Busca todos os personagens de todas as páginas."""
        ...

# ✅ CORRETO: Uso de Pydantic para validação
class PersonFilter(BaseModel):
    """Filtros para busca de personagens."""
    gender: str | None = None
    eye_color: str | None = None
    min_height: int | None = None
    max_height: int | None = None

# ❌ EVITAR: Código sem tipagem
def get_data(id):  # Sem type hints
    ...
```

### Convenções de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Variáveis/Funções | snake_case | `get_person_by_id` |
| Classes | PascalCase | `PersonSummary` |
| Constantes | UPPER_SNAKE_CASE | `TTL_MEDIUM` |
| Arquivos | snake_case.py | `swapi_client.py` |
| Endpoints | kebab-case | `/api/v1/people/{id}/films` |

### Estrutura de Endpoints

```python
@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Get character by ID",
    description="Get detailed information about a specific character.",
)
async def get_person(person_id: int) -> Person:
    """Implementação do endpoint."""
    ...
```

---

## 📦 Dependências e Ferramentas

### Core Dependencies

| Pacote | Versão | Uso |
|--------|--------|-----|
| fastapi | >=0.109.0 | Framework web |
| pydantic | >=2.5.0 | Validação de dados |
| pydantic-settings | >=2.1.0 | Configurações |
| httpx | >=0.26.0 | Cliente HTTP async |
| uvicorn | >=0.27.0 | Servidor ASGI |
| firebase-admin | >=6.3.0 | Autenticação |

### Dev Dependencies

| Pacote | Uso |
|--------|-----|
| pytest | Testes |
| pytest-asyncio | Testes async |
| pytest-cov | Coverage |
| ruff | Linting + Formatting |

### Ferramentas de Linting (pyproject.toml)

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
```

---

## 🔐 Autenticação

### Status Atual

A API é **pública** (sem autenticação obrigatória) para facilitar o consumo e avaliação do case técnico.

### Proteções Implementadas

- **Rate Limiting**: 100 requests/minuto por IP (middleware)
- **CORS**: Configurado para aceitar qualquer origem
- **Security Headers**: Headers de segurança padrão

### Futuro (Opcional)

Caso seja necessário adicionar autenticação:
- Firebase JWT via header `Authorization: Bearer <token>`
- API Keys via header `X-API-Key`

---

## 💾 Estratégia de Cache

### TTLs Configurados

```python
TTL_SHORT = 300      # 5 min  - Listas, resultados de busca
TTL_MEDIUM = 3600    # 1 hora - Recursos individuais
TTL_LONG = 86400     # 24h    - Dados estáticos (filmes)
```

### Chaves de Cache

```
swapi:https://swapi.dev/api/people/1/     # Pessoa individual
swapi:https://swapi.dev/api/films/        # Lista de filmes
```

---

## 🚀 Deploy

### URLs de Produção

| Ambiente | URL | Status |
|----------|-----|--------|
| **Cloud Function** ⭐ | https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function | ✅ Online |
| **API Gateway** | https://starwars-gateway-d9x6gbjl.uc.gateway.dev | ✅ Online |
| **Cloud Run** | https://starwars-api-1040331397233.us-central1.run.app | ✅ Online |

### Deploy Cloud Functions (Recomendado)

Usar o script automatizado:

```powershell
# Deploy completo com teste
.\deploy_cloud_functions.ps1

# Ou deploy manual
cd cloud_functions
gcloud functions deploy starwars-api `
    --gen2 `
    --runtime python312 `
    --region us-central1 `
    --source . `
    --entry-point starwars_api `
    --trigger-http `
    --allow-unauthenticated
```

### Deploy Cloud Run (Alternativo)

Usar Dockerfile para build:

```bash
# Build da imagem
docker build -t starwars-api .

# Push para GCR
docker tag starwars-api gcr.io/starwars-api-2026/starwars-api
docker push gcr.io/starwars-api-2026/starwars-api

# Deploy no Cloud Run
gcloud run deploy starwars-api \
    --image gcr.io/starwars-api-2026/starwars-api \
    --region us-central1 \
    --allow-unauthenticated
```

### Arquivos de Deploy

| Arquivo | Uso | Quando Usar |
|---------|-----|-------------|
| `deploy_cloud_functions.ps1` | Script PowerShell automatizado | Deploy rápido no Windows |
| `Dockerfile` | Container para Cloud Run | Deploy alternativo ou local |
| `cloud_functions/main.py` | Handler HTTP da Cloud Function | Produção principal |
| `cloud_functions/requirements.txt` | Deps mínimas | Cloud Functions |

---

## 🧪 Testes

### Estrutura de Testes

```
tests/
├── conftest.py       # Fixtures compartilhadas
├── unit/             # Testes unitários (sem I/O)
│   ├── test_cache_service.py
│   ├── test_models.py
│   ├── test_pagination.py
│   └── test_sorting.py
└── integration/      # Testes de integração (com API)
    └── test_api.py
```

### Comandos de Teste

```bash
# Rodar todos os testes
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/unit/test_models.py -v
```

---

## 🚀 Comandos de Desenvolvimento

### Setup Inicial

```bash
# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copiar variáveis de ambiente
copy .env.example .env
```

### Executar Localmente

```bash
# Servidor de desenvolvimento
uvicorn src.main:app --reload --port 8000

# Acessar documentação
# http://localhost:8000/docs
```

### Linting e Formatação

```bash
# Verificar código
ruff check src/

# Formatar código
ruff format src/
```

---

## 📊 Status do Projeto

### ✅ Implementado

- [x] Estrutura do projeto FastAPI
- [x] Cliente SWAPI com cache
- [x] Modelos Pydantic para todos os recursos
- [x] CRUD completo para People, Films, Starships, Planets, Vehicles, Species
- [x] Sistema de filtragem com query parameters
- [x] Sistema de ordenação (sort_by, sort_order)
- [x] Paginação (page, page_size)
- [x] Busca por nome (search)
- [x] Queries correlacionadas (characters in film, pilots of starship)
- [x] Endpoints de estatísticas/analytics
- [x] Endpoints de comparação
- [x] Endpoints de rankings (tallest, heaviest, most-appeared)
- [x] Endpoints de timeline (cronológica, lançamento)
- [x] Proxy de imagens (personagens, filmes, naves)
- [x] Cache in-memory com TTL
- [x] Testes unitários (48 passando)
- [x] Documentação de arquitetura
- [x] Deploy Cloud Functions ✅
- [x] Configurar API Gateway ✅
- [x] Frontend SPA completo ✅
- [x] Lint/Format com Ruff (0 erros) ✅

### ⏳ Pendente (Opcional)

- [ ] Testes de integração end-to-end
- [ ] Deploy frontend em Firebase Hosting
- [ ] Implementar Firestore persistent cache
- [ ] Setup monitoring/logging avançado

---

## 🤖 Diretrizes de Autonomia para Claude

### ⚡ WORKFLOW OBRIGATÓRIO - Antes de Qualquer Tarefa:

```
┌─────────────────────────────────────────────────────────────────┐
│  1. LER CLAUDE.md (este arquivo)                                │
│     ↓                                                           │
│  2. CONSULTAR docs/planning/task.md                             │
│     → Ver o que está pendente [ ] vs concluído [x]              │
│     ↓                                                           │
│  3. CONSULTAR docs/architecture.md                              │
│     → Entender componentes envolvidos                           │
│     ↓                                                           │
│  4. CONSULTAR docs/planning/implementation_plan.md              │
│     → Ver especificações detalhadas                             │
│     ↓                                                           │
│  5. IMPLEMENTAR seguindo padrões definidos                      │
│     ↓                                                           │
│  6. ATUALIZAR docs/planning/task.md                             │
│     → Marcar [x] o que foi concluído                            │
└─────────────────────────────────────────────────────────────────┘
```

### ✅ PODE fazer autonomamente:

| Ação | Descrição | Exemplo |
|------|-----------|---------|
| 🐛 **Correções de bugs** | Identificar e corrigir erros | Fix de exceção não tratada |
| 🔄 **Refatoração** | Melhorar código mantendo funcionalidade | Extrair função, renomear |
| 🧪 **Adicionar testes** | Aumentar coverage | Novo test case para edge case |
| 📝 **Atualizar docs** | Manter docs sincronizados | Atualizar task.md após implementar |
| 🔌 **Instalar extensões** | Melhorar DX | Extensões recomendadas |
| ✅ **Rodar testes/lint** | Verificar qualidade | pytest, ruff check |
| ⚙️ **Criar configs** | Arquivos de configuração | .env, settings |
| 🚀 **Implementar features** | Features do task.md | Seguindo implementation_plan.md |

### ⚠️ DEVE consultar usuário antes de:

| Ação | Motivo | Exemplo |
|------|--------|---------|
| 🏗️ **Alterar arquitetura** | Impacto estrutural | Mudar padrão de DI |
| 📦 **Novas dependências** | Aumenta bundle | Adicionar pacote não listado |
| 🔐 **Mudar auth** | Segurança crítica | Alterar fluxo de autenticação |
| 💥 **Breaking changes** | Afeta consumidores | Mudar schema de response |
| 🚢 **Deploy produção** | Risco operacional | Deploy no GCP |

### 🎯 Prioridades de Desenvolvimento:

| Prioridade | Tipo | Ação |
|------------|------|------|
| 🔴 **P0 - Crítico** | Bugs bloqueantes, falhas de segurança, testes falhando | Resolver IMEDIATAMENTE |
| 🟠 **P1 - Alto** | Features do task.md marcadas como pendentes | Próxima implementação |
| 🟡 **P2 - Médio** | Melhorias de performance, refatoração | Quando P0/P1 ok |
| 🟢 **P3 - Baixo** | Documentação extra, otimizações | Tempo livre |

---

## 📁 Arquivos de Referência - Hierarquia Completa

### 🔴 Nível 1 - SEMPRE Consultar

| Arquivo | Conteúdo | Frequência |
|---------|----------|------------|
| `CLAUDE.md` | Esta constituição | Início de cada sessão |
| `docs/architecture.md` | Diagramas, componentes, fluxos | Qualquer alteração estrutural |
| `docs/planning/task.md` | Checklist master | Antes e depois de cada task |
| `docs/planning/implementation_plan.md` | Especificações detalhadas | Ao implementar features |

### 🟡 Nível 2 - Consultar Frequentemente

| Arquivo | Conteúdo | Frequência |
|---------|----------|------------|
| `docs/planning/walkthrough.md` | Status atual, próximos passos | Contexto rápido |
| `README.md` | Setup, uso, endpoints | Referência |
| `pyproject.toml` | Config Ruff, pytest | Antes de rodar linters |
| `.github/copilot-instructions.md` | Padrões de código | Ao escrever código |

### 🟢 Nível 3 - Consultar Quando Necessário

| Arquivo | Conteúdo | Frequência |
|---------|----------|------------|
| `src/main.py` | Entry point FastAPI | Alterações globais |
| `src/config.py` | Settings | Adicionar configs |
| `src/dependencies.py` | DI container | Novos services |
| `tests/conftest.py` | Fixtures | Ao escrever testes |

---

## 🔌 MCP (Model Context Protocol) Tools

### Pylance MCP - Ferramentas Disponíveis

Estas ferramentas permitem automação avançada no desenvolvimento Python:

| Tool | Uso | Quando Usar |
|------|-----|-------------|
| `pylanceDocuments` | Busca documentação Pylance | Dúvidas sobre configuração |
| `pylanceFileSyntaxErrors` | Verifica erros de sintaxe em arquivo | Após edições |
| `pylanceImports` | Analisa imports do workspace | Verificar dependências |
| `pylanceInstalledTopLevelModules` | Lista módulos instalados | Verificar ambiente |
| `pylanceInvokeRefactoring` | Aplica refatorações automáticas | Melhorar código |
| `pylanceRunCodeSnippet` | Executa código Python | Testar snippets |
| `pylanceSyntaxErrors` | Valida código para erros | Antes de salvar |
| `pylanceWorkspaceUserFiles` | Lista arquivos Python | Navegar projeto |

### Comandos MCP Frequentes

```python
# Verificar erros de sintaxe em um arquivo
mcp_pylance_mcp_s_pylanceFileSyntaxErrors(
    workspaceRoot="file:///c%3A/Users/vinic/OneDrive/Desktop/Api%20Starwars",
    fileUri="file:///c%3A/Users/vinic/OneDrive/Desktop/Api%20Starwars/src/main.py"
)

# Executar código Python diretamente
mcp_pylance_mcp_s_pylanceRunCodeSnippet(
    workspaceRoot="file:///c%3A/Users/vinic/OneDrive/Desktop/Api%20Starwars",
    codeSnippet="print('Hello Star Wars!')"
)

# Remover imports não utilizados
mcp_pylance_mcp_s_pylanceInvokeRefactoring(
    fileUri="file:///path/to/file.py",
    name="source.unusedImports",
    mode="update"
)
```

---

## 🌐 Recursos Externos

| Recurso | URL | Uso |
|---------|-----|-----|
| **SWAPI Docs** | https://swapi.dev/documentation | API de origem |
| **FastAPI Docs** | https://fastapi.tiangolo.com/ | Framework principal |
| **Pydantic v2** | https://docs.pydantic.dev/latest/ | Validação de dados |
| **Firebase Admin** | https://firebase.google.com/docs/admin/setup | Autenticação |
| **GCP Functions** | https://cloud.google.com/functions/docs | Deploy |
| **httpx** | https://www.python-httpx.org/ | Cliente HTTP async |

---

## 📝 Changelog

### v2.1.0 (2026-02-03)
- 🚀 **NOVO**: Seção de Deploy com scripts e comandos
- 📁 **ATUALIZADO**: Estrutura do projeto com cloud_functions/ e frontend/
- 🔐 **ATUALIZADO**: Autenticação removida (API pública)
- ✅ **ATUALIZADO**: Status do projeto (100% completo)
- 📝 Adicionados arquivos de deploy (Dockerfile, deploy_cloud_functions.ps1)

### v2.0.0 (2026-02-01)
- 🎮 **NOVO**: Sistema de comandos completo (`/status`, `/implementar`, `/testar`, etc.)
- 📊 **NOVO**: Variáveis de contexto configuráveis
- 🔄 **NOVO**: Fluxo de trabalho visual com 10 etapas
- ✨ Sincronização completa com `.github/copilot-instructions.md`
- 📝 Exemplos de uso dos comandos

### v1.2.0 (2026-02-01)
- ✨ Documentação CRÍTICA enfatizada com prioridades visuais
- 📁 Seção detalhada sobre pasta `docs/` como FONTE DA VERDADE
- 🔄 Workflow obrigatório com diagrama de fluxo
- 📊 Tabelas de autonomia com exemplos concretos
- 🎯 Hierarquia de arquivos em 3 níveis de prioridade
- 📝 Instruções Copilot expandidas em `.github/copilot-instructions.md`

### v1.1.0 (2026-02-01)
- Adicionada seção MCP Tools
- Configurado Pylance MCP para automação
- Atualizado settings.json com instruções Copilot

### v1.0.0 (2026-02-01)
- Criação inicial da constituição CLAUDE.md
- Mapeamento completo do projeto
- Definição de padrões e diretrizes
- Setup de extensões VS Code (Python, Pylance, Ruff)

---

## 📝 Exemplos de Uso dos Comandos

### Exemplo: Verificar Status

```
Usuário: /status

Claude:  📊 STATUS DO PROJETO
         
         🚀 Servidor: Não iniciado
         🧪 Testes: 48 passando (última execução)
         📦 Deps: Não instaladas (venv não encontrado)
         
         ✅ Implementado: 18 itens
         ⏳ Pendente: 10 itens
         
         Próximas tarefas sugeridas:
         1. Configurar ambiente (/setup)
         2. Rodar testes (/testar)
         3. Iniciar servidor (/servidor)
```

### Exemplo: Implementar Tarefa

```
Usuário: /implementar

Claude:  🔍 Analisando docs/planning/task.md...
         
         Tarefas pendentes encontradas:
         1. [ ] Configurar ambiente local
         2. [ ] Rodar testes e verificar coverage
         
         Iniciando tarefa 1: Configurar ambiente local...
         
         ✅ Ambiente virtual criado
         ✅ Dependências instaladas
         ✅ .env copiado
         
         Atualizando task.md: [x] Configurar ambiente local
```

### Exemplo: Nova Feature

```
Usuário: /especificar
         Quero adicionar um endpoint de busca avançada para planetas

Claude:  📝 Especificação criada!
         
         Atualizei docs/planning/implementation_plan.md com:
         - Endpoint: GET /api/v1/planets/search
         - Query params: climate, terrain, min_population
         - Response model: list[PlanetSummary]
         
         Próximo passo: /planejar para criar o plano técnico
```

---

> **⚠️ LEMBRETE FINAL**: 
> - Use `/status` para ver o estado atual do projeto
> - Sempre atualizar `docs/planning/task.md` após concluir uma tarefa
> - A pasta `docs/` é a **FONTE DA VERDADE** do projeto
> - Quando em dúvida, use `/clarificar` antes de `/implementar`
