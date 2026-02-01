# 🤖 Instruções de Desenvolvimento - GitHub Copilot & Claude Opus

> **Spec-Kit Personalizado v1.0** - Star Wars API Platform  
> Sistema de comandos e diretrizes para desenvolvimento autônomo

---

## 📋 Contexto do Projeto

| Campo | Valor |
|-------|-------|
| **Projeto** | Star Wars API Platform |
| **Stack** | FastAPI + Python 3.11+ + Firebase Auth + GCP |
| **Estilo** | REST API production-ready |
| **Status** | Desenvolvimento ativo |
| **Idioma** | Português (Brasil) |

---

# 🎮 SISTEMA DE COMANDOS

## Comandos Principais

Use estes comandos para interagir com o agente de desenvolvimento:

| Comando | Descrição | Ação Executada |
|---------|-----------|----------------|
| `/constituicao` | Criar ou atualizar princípios de desenvolvimento | Atualiza `CLAUDE.md` com novas diretrizes |
| `/especificar` | Definir requisitos e user stories | Cria/atualiza specs em `docs/planning/` |
| `/planejar` | Criar planos de implementação técnica | Atualiza `docs/planning/implementation_plan.md` |
| `/tarefas` | Gerar lista de tarefas acionáveis | Atualiza `docs/planning/task.md` com checklist |
| `/implementar` | Executar tarefas pendentes | Implementa código seguindo o plano |
| `/status` | Ver status atual do projeto | Lê e resume `docs/planning/walkthrough.md` |

## Comandos de Qualidade

Comandos adicionais para validação e qualidade:

| Comando | Descrição | Ação Executada |
|---------|-----------|----------------|
| `/clarificar` | Esclarecer áreas subespecificadas | Faz perguntas antes de implementar |
| `/analisar` | Análise de consistência entre artefatos | Verifica se código segue docs |
| `/validar` | Gerar checklist de qualidade | Valida completude e consistência |
| `/testar` | Executar testes e verificar coverage | Roda `pytest` e analisa resultados |
| `/revisar` | Code review do código atual | Analisa código com Ruff + boas práticas |
| `/documentar` | Atualizar documentação | Sincroniza docs com código atual |

## Comandos de Ambiente

Comandos para setup e configuração:

| Comando | Descrição | Ação Executada |
|---------|-----------|----------------|
| `/setup` | Configurar ambiente de desenvolvimento | Cria venv, instala deps, copia .env |
| `/servidor` | Iniciar servidor de desenvolvimento | `uvicorn src.main:app --reload` |
| `/limpar` | Limpar caches e arquivos temporários | Remove `__pycache__`, `.pytest_cache` |
| `/formatar` | Formatar código com Ruff | `ruff format src/ tests/` |
| `/lint` | Verificar código com Ruff | `ruff check src/ tests/` |

---

## 🔄 Fluxo de Trabalho Completo

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

---

## 📊 Variáveis de Contexto

Variáveis que definem o comportamento do agente:

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `FEATURE_ATUAL` | Feature sendo desenvolvida | Detectada automaticamente |
| `MODO_AUTONOMO` | Se pode agir sem confirmação | `true` para tarefas seguras |
| `NIVEL_DETALHE` | Quantidade de explicações | `medio` (baixo/medio/alto) |
| `IDIOMA` | Idioma das respostas | `pt-BR` |
| `RODAR_TESTES` | Se deve rodar testes após mudanças | `true` |
| `ATUALIZAR_DOCS` | Se deve atualizar docs após mudanças | `true` |

### Configuração por Sessão

Para alterar comportamento, diga:
- "Modo verboso" → `NIVEL_DETALHE=alto`
- "Modo silencioso" → `NIVEL_DETALHE=baixo`
- "Confirmar antes de agir" → `MODO_AUTONOMO=false`
- "Pular testes" → `RODAR_TESTES=false`

---

# 🚨 DOCUMENTAÇÃO CRÍTICA

## ⚠️ ANTES de qualquer alteração, SEMPRE consultar:

| Prioridade | Arquivo | Conteúdo | Quando |
|------------|---------|----------|--------|
| 🔴 **1** | `CLAUDE.md` | Constituição de desenvolvimento | **SEMPRE** |
| 🔴 **2** | `docs/architecture.md` | Arquitetura, diagramas, fluxos | Alterações estruturais |
| 🔴 **3** | `docs/planning/task.md` | Checklist [x] feito / [ ] pendente | Ver o que fazer |
| 🔴 **4** | `docs/planning/implementation_plan.md` | Especificações detalhadas | Como implementar |
| 🟡 **5** | `docs/planning/walkthrough.md` | Status atual | Contexto rápido |
| 🟡 **6** | `README.md` | Setup e uso | Referência |

---

## 📁 Estrutura `docs/` - FONTE DA VERDADE

```
docs/                                    # 🔴 PASTA MAIS IMPORTANTE
│
├── architecture.md                      # 🔴 Arquitetura Técnica
│   ├── 📊 Diagrama Mermaid completo
│   ├── 🔧 Componentes e responsabilidades
│   ├── 📡 Todos os endpoints
│   ├── 🔄 Fluxo de requisições
│   ├── 💾 Estratégia de cache (TTLs)
│   └── 🛡️ Considerações de segurança
│
└── planning/                            # 🔴 Planejamento
    │
    ├── task.md                          # 🔴 Checklist Master
    │   ├── ✅ [x] Tarefas concluídas
    │   └── ⏳ [ ] Tarefas pendentes
    │
    ├── implementation_plan.md           # 🔴 Especificações
    │   ├── 📁 Estrutura de pastas
    │   ├── 📡 Endpoints com query params
    │   ├── 📦 Modelos Pydantic
    │   └── 🧪 Plano de testes
    │
    └── walkthrough.md                   # 🟡 Status Atual
        ├── 🚀 Servidor rodando?
        ├── ✅ Testes passando?
        └── ➡️ Próximos passos
```

---

# 🎯 PADRÕES DE CÓDIGO

## Python - Regras Obrigatórias

### ✅ Type Hints + Docstrings (OBRIGATÓRIO)

```python
async def get_person_by_id(
    person_id: int,
    include_films: bool = False,
) -> Person:
    """
    Busca um personagem por ID.

    Args:
        person_id: ID único do personagem na SWAPI.
        include_films: Se True, inclui dados dos filmes.

    Returns:
        Person com todos os dados do personagem.

    Raises:
        HTTPException: Se personagem não encontrado (404).
    """
    ...
```

### ✅ Union Types Modernos (Python 3.11+)

```python
# ✅ CORRETO
def parse_height(value: str | None) -> int | None:
    ...

# ❌ PROIBIDO
from typing import Optional
def parse_height(value: Optional[str]) -> Optional[int]:
    ...
```

### ✅ Pydantic v2 com Field

```python
class PersonFilter(BaseModel):
    """Filtros para busca de personagens."""
    
    gender: str | None = Field(None, description="Filtrar por gênero")
    min_height: int | None = Field(None, ge=0, description="Altura mínima")
    
    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str | None) -> str | None:
        return v.lower() if v else v
```

### ✅ Endpoints FastAPI

```python
@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Buscar personagem por ID",
    description="Retorna informações detalhadas de um personagem.",
    responses={
        200: {"description": "Personagem encontrado"},
        404: {"description": "Personagem não encontrado"},
    },
)
async def get_person(
    person_id: int = Path(..., ge=1, description="ID do personagem"),
    swapi: SWAPIClient = Depends(get_swapi_client),
) -> Person:
    """Busca personagem com dependency injection."""
    ...
```

### ✅ Testes Pytest

```python
class TestPersonService:
    """Testes para o serviço de personagens."""

    async def test_get_person_valid_id_returns_person(
        self,
        mock_swapi_client: MagicMock,
    ) -> None:
        """Deve retornar Person quando ID é válido."""
        # Arrange
        mock_swapi_client.get_person.return_value = MOCK_LUKE_DATA
        
        # Act
        result = await get_person(1)
        
        # Assert
        assert result.name == "Luke Skywalker"
```

---

## 🔧 Convenções de Nomenclatura

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Variáveis/Funções | `snake_case` | `get_person_by_id` |
| Classes | `PascalCase` | `PersonSummary` |
| Constantes | `UPPER_SNAKE_CASE` | `TTL_MEDIUM` |
| Arquivos | `snake_case.py` | `swapi_client.py` |
| Endpoints | `kebab-case` | `/api/v1/people/{id}` |
| Env Vars | `UPPER_SNAKE_CASE` | `SWAPI_BASE_URL` |

---

# 📁 HIERARQUIA DE ARQUIVOS

## Nível 🔴 Crítico - SEMPRE Consultar

| Arquivo | Conteúdo |
|---------|----------|
| `CLAUDE.md` | Constituição de desenvolvimento |
| `docs/architecture.md` | Arquitetura técnica completa |
| `docs/planning/task.md` | Checklist master de tarefas |
| `docs/planning/implementation_plan.md` | Especificações detalhadas |

## Nível 🟡 Alto - Consultar Frequentemente

| Arquivo | Conteúdo |
|---------|----------|
| `docs/planning/walkthrough.md` | Status atual |
| `README.md` | Setup e uso |
| `pyproject.toml` | Config Ruff, pytest |
| `.github/copilot-instructions.md` | Este arquivo |

## Nível 🟢 Médio - Quando Necessário

| Arquivo | Conteúdo |
|---------|----------|
| `src/main.py` | Entry point FastAPI |
| `src/config.py` | Configurações |
| `src/dependencies.py` | Injeção de dependências |
| `tests/conftest.py` | Fixtures de teste |

---

# 🚀 COMANDOS DE TERMINAL

## Desenvolvimento

```bash
# Servidor de desenvolvimento
uvicorn src.main:app --reload --port 8000

# Abrir documentação
# http://localhost:8000/docs
```

## Testes

```bash
# Rodar todos os testes
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Teste específico
pytest tests/unit/test_models.py -v
```

## Qualidade

```bash
# Verificar código
ruff check src/ tests/

# Formatar código
ruff format src/ tests/
```

---

# ⚡ CHECKLIST PRÉ-ALTERAÇÃO

Antes de qualquer mudança:

- [ ] Li `CLAUDE.md`?
- [ ] Consultei `docs/architecture.md`?
- [ ] Verifiquei `docs/planning/task.md`?
- [ ] Minha alteração segue os padrões?
- [ ] Adicionei/atualizei testes?
- [ ] Type hints em todas as funções?
- [ ] Docstrings em funções públicas?

---

# 🔐 AUTENTICAÇÃO

| Método | Header | Exemplo |
|--------|--------|---------|
| Firebase JWT | `Authorization` | `Bearer <token>` |
| API Key | `X-API-Key` | `dev-api-key-12345` |
| Dev Mode | N/A | `DEBUG=true` relaxa auth |

---

# 💾 CACHE TTLs

```python
TTL_SHORT = 300      # 5 min  - Listas, buscas
TTL_MEDIUM = 3600    # 1 hora - Recursos individuais  
TTL_LONG = 86400     # 24h    - Dados estáticos (filmes)
```

---

# 🌐 API EXTERNA

| Campo | Valor |
|-------|-------|
| **URL Base** | https://swapi.dev/api |
| **Rate Limit** | 10,000 requests/dia |
| **Recursos** | people, films, starships, planets, vehicles, species |

---

# 🤖 COMPORTAMENTO DO AGENTE

## Pode Fazer Autonomamente ✅

| Ação | Exemplo |
|------|---------|
| Correções de bugs | Fix de exceção não tratada |
| Refatoração | Extrair função, renomear |
| Adicionar testes | Novo test case |
| Atualizar docs | Atualizar task.md |
| Rodar testes/lint | pytest, ruff |
| Implementar features | Do task.md pendente |

## Deve Consultar Primeiro ⚠️

| Ação | Motivo |
|------|--------|
| Alterar arquitetura | Impacto estrutural |
| Novas dependências | Aumenta bundle |
| Mudar auth | Segurança crítica |
| Breaking changes | Afeta consumidores |
| Deploy produção | Risco operacional |

## Prioridades

| Prioridade | Tipo | Ação |
|------------|------|------|
| 🔴 P0 | Bugs, segurança, testes falhando | IMEDIATO |
| 🟠 P1 | Features pendentes | Próximo |
| 🟡 P2 | Performance, refatoração | Depois |
| 🟢 P3 | Docs extras, otimizações | Quando possível |

---

# 📝 EXEMPLOS DE USO DOS COMANDOS

## Exemplo: Nova Feature

```
Usuário: /especificar
         Quero adicionar um endpoint de busca avançada para planetas
         que permita filtrar por clima e terreno.

Claude:  📝 Especificação criada!
         
         Atualizei docs/planning/implementation_plan.md com:
         - Endpoint: GET /api/v1/planets/search
         - Query params: climate, terrain, min_population
         - Response model: list[PlanetSummary]
         
         Próximo passo: /planejar para criar o plano técnico
```

## Exemplo: Implementar

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

## Exemplo: Status

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

---

> **💡 Dica**: Sempre que tiver dúvida, use `/status` para ver o estado atual
> e `/clarificar` antes de `/implementar` para evitar retrabalho.
