# ✅ Star Wars API Platform - Task Checklist

> **📅 PRAZO: 5 de Fevereiro de 2026**  
> **⚠️ STATUS: EM ANDAMENTO - Correções Frontend/API**  
> **💰 CUSTO: $0.00/mês (GCP Free Tier)**

---

## 🌐 URLs de Produção

| Ambiente | URL | Status |
|----------|-----|--------|
| **Cloud Function** ⭐ | https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function | ✅ Online |
| **Frontend Local** | http://localhost:3000 | 🔧 Dev |
| **API Gateway** | https://starwars-gateway-d9x6gbjl.uc.gateway.dev | ✅ Online |
| **Cloud Run** | https://starwars-api-1040331397233.us-central1.run.app | ✅ Online |

---

## ✅ FASE 1: INFRAESTRUTURA (Concluída)

### 🚀 Deploy - Cloud Functions + API Gateway
- [x] Criar Cloud Function wrapper para API
- [x] Configurar API Gateway com OpenAPI spec
- [x] Deploy no Cloud Functions Gen2
- [x] Testar endpoints via API Gateway

### 🐳 Deploy - Cloud Run (Backup)
- [x] Criar `Dockerfile` otimizado para FastAPI
- [x] Criar `.dockerignore` para build limpo
- [x] Criar guia de deploy (`docs/DEPLOY_GUIDE.md`)
- [x] Fazer deploy no Cloud Run
- [x] Testar endpoints em produção

---

## ⚠️ FASE 2: API BACKEND (Em Correção)

### 📡 Endpoints Core
- [x] `GET /people` - Lista personagens
- [x] `GET /people/{id}` - Detalhes personagem
- [ ] `GET /people/search?name=` - ⚠️ **PRECISA IMPLEMENTAR**
- [x] `GET /films` - Lista filmes
- [x] `GET /films/{id}` - Detalhes filme
- [x] `GET /planets` - Lista planetas
- [x] `GET /planets/{id}` - Detalhes planeta
- [x] `GET /starships` - Lista naves
- [x] `GET /starships/{id}` - Detalhes nave

### ⭐ Endpoints Exclusivos (Rankings/Timeline)
- [x] `GET /rankings/tallest-characters` - Top 10 mais altos
- [x] `GET /rankings/fastest-starships` - Top 10 naves mais rápidas
- [ ] `GET /rankings/most-appeared` - ⚠️ **PRECISA IMPLEMENTAR**
- [ ] `GET /rankings/heaviest` - ⚠️ **PRECISA IMPLEMENTAR**
- [x] `GET /timeline/films/chronological` - Ordem cronológica
- [x] `GET /timeline/films/release-order` - Ordem de lançamento

### 🖼️ Proxy de Imagens
- [x] `GET /images/characters/{id}` - Imagens de personagens (via Akabab/Wikia)
- [ ] `GET /images/films/{id}` - ⚠️ **PRECISA IMPLEMENTAR** (pôsteres)

### 🐛 Correções Necessárias
- [ ] Adicionar `films_count` no retorno de `/people/{id}`
- [ ] Adicionar `characters_count` no retorno de `/films`
- [ ] Melhorar mapeamento de imagens para personagens faltantes

---

## ⚠️ FASE 3: FRONTEND (Em Correção)

### 🎨 Estrutura Base
- [x] HTML com Tailwind + DaisyUI
- [x] Tema Star Wars (cores, fontes)
- [x] Layout responsivo
- [x] Grid de personagens com paginação

### 🐛 Problemas a Corrigir

| # | Problema | Status | Prioridade |
|---|----------|--------|------------|
| 1 | Pesquisa "Explore a Galáxia" não funciona | ❌ Pendente | 🔴 Alta |
| 2 | Personagens mostram "0 aparições" | ❌ Pendente | 🔴 Alta |
| 3 | Rankings não carregam (endpoints errados) | ❌ Pendente | 🔴 Alta |
| 4 | Timeline não carrega (formato errado) | ❌ Pendente | 🔴 Alta |
| 5 | Filmes sem pôsteres | ❌ Pendente | 🟡 Média |
| 6 | Filmes mostram "0 personagens" | ❌ Pendente | 🟡 Média |
| 7 | ~21 personagens sem imagem | ❌ Pendente | 🟡 Média |
| 8 | Falta aba de Naves | ❌ Pendente | 🟡 Média |
| 9 | Console.logs de debug ativos | ❌ Pendente | 🟢 Baixa |
| 10 | Falta favicon | ❌ Pendente | 🟢 Baixa |

### 📋 Personagens Sem Imagem (~21)
```
Wedge Antilles, Lobot, Mon Mothma, Roos Tarpals, Rugor Nass,
Shmi Skywalker, Ratts Tyerel, Gasgano, Ben Quadinaros, Mace Windu,
Adi Gallia, Saesee Tiin, Yarael Poof, Cordé, Luminara Unduli,
Dormé, Dexter Jettster, San Hill, Grievous, Sly Moore, Tion Medon
```

---

## ✅ FASE 4: QUALIDADE (Concluída)

### 🧪 Testes
- [x] 48 testes unitários passando
- [x] Coverage de lógica crítica >90%

### 📚 Documentação
- [x] `docs/architecture.md` - Arquitetura técnica
- [x] `docs/DEPLOY_GUIDE.md` - Guia de deploy
- [x] `docs/PRESENTATION.md` - Slides apresentação
- [x] `docs/planning/task.md` - Checklist (este arquivo)
- [x] `docs/planning/walkthrough.md` - Status do projeto
- [x] `docs/planning/NEXT_DAY_PLAN.md` - **NOVO** Plano próximo dia
- [x] `README.md` - Documentação principal
- [x] `CLAUDE.md` - Constituição de desenvolvimento

---

## 📊 PROGRESSO GERAL

| Fase | Status | % |
|------|--------|---|
| Infraestrutura | ✅ Concluído | 100% |
| API Backend | ⚠️ Correções | 80% |
| Frontend | ⚠️ Correções | 60% |
| Testes | ✅ Concluído | 100% |
| Documentação | ✅ Concluído | 100% |

**📈 Progresso Total: ~85%**

---

## 📅 CRONOGRAMA

| Data | Tarefa | Status |
|------|--------|--------|
| 01/02 | Deploy Cloud Functions + API Gateway | ✅ |
| 02/02 | Frontend base + identificar problemas | ✅ |
| **03/02** | **Corrigir backend (busca, rankings)** | ⏳ Próximo |
| **04/02** | **Corrigir frontend (tabs, naves)** | ⏳ Próximo |
| **05/02** | **Testes finais + ENTREGA** | ⏳ Final |

---

## ⏭️ PRÓXIMOS PASSOS (Ver NEXT_DAY_PLAN.md)

### 🔴 Prioridade Alta
1. [ ] Implementar `/people/search?name=`
2. [ ] Implementar `/rankings/most-appeared`
3. [ ] Implementar `/rankings/heaviest`
4. [ ] Corrigir frontend Rankings
5. [ ] Corrigir frontend Timeline

### 🟡 Prioridade Média
6. [ ] Adicionar aba de Naves
7. [ ] Adicionar `films_count` nos personagens
8. [ ] Adicionar pôsteres de filmes

📖 **Plano Detalhado:** [`NEXT_DAY_PLAN.md`](NEXT_DAY_PLAN.md)

