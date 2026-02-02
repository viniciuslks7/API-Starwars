# 📋 Plano de Desenvolvimento - Próximo Dia

> **Data:** 02/02/2026  
> **Prazo Final:** 05/02/2026  
> **Autor:** Vinicius Oliveira  
> **Projeto:** Star Wars API Platform - Frontend & API

---

## 🎯 Objetivo

Corrigir todos os problemas identificados no frontend e garantir que **todos os dados da API** sejam consumidos corretamente, incluindo:
- Dados dos personagens (filmes, aparições)
- Pesquisa funcionando
- Filmes com pôsteres
- Rankings e Timeline corretos
- Navegação por Naves (Starships)

---

## 🐛 Problemas Identificados

### 1. Dados de Personagens Incompletos

**Sintoma:** 
- Luke Skywalker mostra "Filmes: 0 aparições"
- R2-D2 mostra "Filmes: 0 aparições"

**Causa Raiz:**
O frontend busca `char.film_ids?.length` mas a API retorna `films` como array de URLs, não IDs.

**Solução:**
- [ ] Backend: Adicionar campo `films_count` no endpoint `/people/{id}`
- [ ] Backend: Processar URLs de filmes para contar aparições
- [ ] Frontend: Usar `films?.length` ou `films_count`

---

### 2. Pesquisa "Explore a Galáxia" Não Funciona

**Sintoma:**
Ao clicar em "Buscar", nada acontece ou erro é retornado.

**Causa Raiz:**
O endpoint `/people/search?name=` não está implementado corretamente na Cloud Function - retorna 404.

**Solução:**
- [ ] Backend: Implementar handler para `/people/search` em `handle_people()`
- [ ] Backend: Filtrar personagens por nome (case-insensitive)
- [ ] Frontend: Verificar se a chamada está correta

---

### 3. Personagens Sem Imagens (~21 personagens)

**Lista:**
- Wedge Antilles, Lobot, Mon Mothma, Roos Tarpals, Rugor Nass
- Shmi Skywalker, Ratts Tyerel, Gasgano, Ben Quadinaros, Mace Windu
- Adi Gallia, Saesee Tiin, Yarael Poof, Cordé, Luminara Unduli
- Dormé, Dexter Jettster, San Hill, Grievous, Sly Moore, Tion Medon

**Causa Raiz:**
A API Akabab (fonte de imagens) não tem imagens para todos os personagens da SWAPI. Há IDs diferentes entre as duas APIs.

**Solução:**
- [ ] Backend: Melhorar mapeamento de nomes para imagens (fuzzy matching)
- [ ] Backend: Criar mapeamento manual para personagens populares sem imagem
- [ ] Frontend: Placeholder SVG mais bonito quando não há imagem

---

### 4. Filmes Sem Pôsteres e "0 Personagens"

**Sintoma:**
- Filmes mostram ícone "?" em vez de pôster
- "0 personagens" em todos os filmes

**Causa Raiz:**
- O proxy de imagens não tem mapeamento para filmes (só personagens via Akabab)
- O endpoint `/films` não retorna `character_ids`, retorna `characters` como URLs

**Solução:**
- [ ] Backend: Adicionar pôsteres de filmes (fonte alternativa ou base64 estático)
- [ ] Backend: Adicionar `characters_count` ou `character_ids` no endpoint `/films`
- [ ] Frontend: Usar `characters?.length` ou `characters_count`

---

### 5. Rankings Não Funcionam

**Sintoma:**
Rankings mostram skeleton loading infinito ou nada.

**Causa Raiz:**
O frontend espera `response.characters` mas a API retorna array direto.

**Endpoints da API:**
- `/rankings/tallest-characters` → retorna array `[{name, height, ...}]`
- `/rankings/fastest-starships` → retorna array `[{name, mglt, ...}]`
- NÃO EXISTE: `/rankings/most-appeared`, `/rankings/heaviest`

**Solução:**
- [ ] Backend: Implementar `/rankings/most-appeared` (contar filmes por personagem)
- [ ] Backend: Implementar `/rankings/heaviest` (ordenar por massa)
- [ ] Frontend: Ajustar para consumir array direto (sem `.characters`)

---

### 6. Timeline Não Funciona

**Sintoma:**
Timeline mostra "Erro ao carregar timeline"

**Causa Raiz:**
O frontend espera `response.timeline` mas a API retorna array direto.

**Endpoints da API:**
- `/timeline/films/chronological` → retorna array de filmes
- `/timeline/films/release-order` → retorna array de filmes

**Solução:**
- [ ] Frontend: Usar `/timeline/films/chronological`
- [ ] Frontend: Ajustar para consumir array direto (sem `.timeline`)

---

### 7. Falta Navegação por Naves (Starships)

**Sintoma:**
Não existe aba para ver naves espaciais.

**Recurso da API:**
- `GET /starships` → Lista de naves com paginação
- `GET /starships/{id}` → Detalhes da nave

**Solução:**
- [ ] Frontend: Adicionar aba "Naves" no menu
- [ ] Frontend: Criar grid de naves similar aos personagens
- [ ] Frontend: Modal de detalhes da nave
- [ ] Backend: Adicionar imagens de naves (se disponível)

---

### 8. Sabres de Luz

**Status:** ❌ Não disponível na SWAPI

A SWAPI (swapi.dev) **não possui endpoint de sabres de luz**. Os recursos disponíveis são:
- people, films, planets, species, starships, vehicles

**Alternativa:**
- Podemos criar um endpoint estático com dados de sabres conhecidos
- Ou indicar que "Sabres de Luz" não está disponível na API fonte

---

## 📊 Endpoints Atuais vs Necessários

### ✅ Funcionando
| Endpoint | Descrição | Frontend |
|----------|-----------|----------|
| `GET /people` | Lista personagens | ✅ |
| `GET /people/{id}` | Detalhes personagem | ⚠️ Falta contagem de filmes |
| `GET /films` | Lista filmes | ⚠️ Falta contagem de personagens |
| `GET /starships` | Lista naves | ❌ Não implementado no frontend |
| `GET /planets` | Lista planetas | ❌ Não implementado no frontend |
| `GET /images/characters/{id}` | Proxy de imagens | ✅ |

### ❌ Precisam Implementação

| Endpoint | Descrição | Prioridade |
|----------|-----------|------------|
| `GET /people/search?name=` | Busca por nome | 🔴 Alta |
| `GET /rankings/most-appeared` | Top personagens por filmes | 🔴 Alta |
| `GET /rankings/heaviest` | Top por peso | 🟡 Média |
| `GET /images/films/{id}` | Pôsteres de filmes | 🟡 Média |

---

## 🔧 Tarefas Técnicas Ordenadas por Prioridade

### 🔴 P0 - Crítico (Fazer Primeiro)

1. **Implementar busca de personagens**
   - Arquivo: `cloud_functions/main.py`
   - Handler: `handle_people()`
   - Adicionar rota `/people/search`

2. **Corrigir contagem de filmes nos personagens**
   - Arquivo: `cloud_functions/main.py`
   - Adicionar `films_count` no retorno de `/people/{id}`

3. **Implementar rankings faltantes**
   - Arquivo: `cloud_functions/main.py`
   - Handler: `handle_rankings()`
   - Adicionar `/rankings/most-appeared`
   - Adicionar `/rankings/heaviest`

4. **Corrigir frontend Rankings**
   - Arquivo: `frontend/index.html`
   - Ajustar chamadas para endpoints corretos
   - Remover `.characters` e consumir array direto

5. **Corrigir frontend Timeline**
   - Arquivo: `frontend/index.html`
   - Usar `/timeline/films/chronological`
   - Remover `.timeline` e consumir array direto

### 🟡 P1 - Importante (Fazer Depois)

6. **Adicionar aba de Naves no frontend**
   - Arquivo: `frontend/index.html`
   - Adicionar tab "Naves"
   - Criar `loadStarships()` e grid

7. **Implementar pôsteres de filmes**
   - Arquivo: `cloud_functions/main.py`
   - Adicionar mapeamento estático de pôsteres
   - Ou usar TMDB API (requer key)

8. **Melhorar mapeamento de imagens**
   - Arquivo: `cloud_functions/main.py`
   - Criar mapeamento por nome (fuzzy match)
   - Placeholder personalizado por personagem

### 🟢 P2 - Nice to Have

9. **Adicionar aba de Planetas**
   - Similar à aba de Naves

10. **Remover console.logs de debug**
    - Arquivo: `frontend/index.html`

11. **Adicionar favicon**
    - Arquivo: `frontend/favicon.ico`

---

## 📅 Cronograma Sugerido

### Dia 1 (02/02) - Fundação ✅
- [x] Identificar problemas
- [x] Criar plano de desenvolvimento
- [x] Atualizar documentação
- [x] Commit inicial

### Dia 2 (03/02) - Backend
- [ ] Implementar `/people/search`
- [ ] Implementar `/rankings/most-appeared`
- [ ] Implementar `/rankings/heaviest`
- [ ] Adicionar `films_count` em `/people/{id}`
- [ ] Deploy Cloud Function

### Dia 3 (04/02) - Frontend
- [ ] Corrigir Rankings (endpoint + parser)
- [ ] Corrigir Timeline (endpoint + parser)
- [ ] Adicionar aba Naves
- [ ] Testar busca

### Dia 4 (05/02) - Polish & Entrega
- [ ] Melhorar imagens (fallbacks)
- [ ] Adicionar pôsteres de filmes
- [ ] Remover debug logs
- [ ] Testes finais
- [ ] Documentação final
- [ ] **ENTREGA**

---

## 🧪 Testes de Aceite

Antes de considerar pronto, verificar:

```bash
# 1. Busca funciona
curl "https://...cloudfunctions.net/starwars-api-function/people/search?name=luke"

# 2. Rankings funcionam
curl "https://...cloudfunctions.net/starwars-api-function/rankings/most-appeared"
curl "https://...cloudfunctions.net/starwars-api-function/rankings/tallest-characters"
curl "https://...cloudfunctions.net/starwars-api-function/rankings/heaviest"

# 3. Timeline funciona
curl "https://...cloudfunctions.net/starwars-api-function/timeline/films/chronological"

# 4. Contagem de filmes
curl "https://...cloudfunctions.net/starwars-api-function/people/1" | jq '.films_count'
# Deve retornar 4 (A New Hope, Empire, Return, Revenge of the Sith)
```

---

## 📚 Arquivos a Modificar

| Arquivo | Alterações |
|---------|------------|
| `cloud_functions/main.py` | Busca, rankings, films_count |
| `frontend/index.html` | Rankings, Timeline, Naves, bugs |
| `docs/planning/task.md` | Atualizar checklist |
| `docs/architecture.md` | Documentar novos endpoints |
| `README.md` | Atualizar exemplos |

---

## ⚠️ Notas Importantes

1. **SWAPI Limitações:** A API fonte não tem sabres de luz, veículos de combate específicos, ou informações detalhadas de batalhas.

2. **Imagens:** O site starwars-visualguide.com foi hackeado. Estamos usando Akabab API (Wikia) como fonte.

3. **Deploy:** Lembrar de usar `--entry-point=starwars_api` (não `main`).

4. **Free Tier:** Manter dentro dos limites de 2M requisições/mês.

---

> **Última atualização:** 02/02/2026 01:00  
> **Próxima revisão:** 03/02/2026
