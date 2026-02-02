# 🚀 Guia de Deploy - Star Wars API Platform

> **PowerOfData Case Técnico** | Última atualização: 01/02/2026

---

## 📋 Índice

1. [Pré-requisitos](#-pré-requisitos)
2. [Deploy Cloud Functions + API Gateway](#-deploy-cloud-functions--api-gateway) ⭐
3. [Deploy Cloud Run (Alternativo)](#-deploy-cloud-run-alternativo)
4. [Verificação](#-verificação)
5. [Troubleshooting](#-troubleshooting)

---

## 🔧 Pré-requisitos

### Google Cloud CLI

```powershell
# Windows - Instalar via winget
winget install Google.CloudSDK

# Verificar instalação
gcloud --version

# Autenticar
gcloud auth login
gcloud auth application-default login

# Configurar projeto
gcloud config set project starwars-api-2026
```

### APIs Necessárias

```powershell
# Habilitar APIs (executar uma vez)
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

---

## ⭐ Deploy Cloud Functions + API Gateway

### Arquitetura Recomendada

Esta é a arquitetura solicitada no case técnico:

```
Cliente → API Gateway → Cloud Function → SWAPI
```

### Passo 1: Deploy da Cloud Function

```powershell
# Navegar para pasta cloud_functions
cd cloud_functions

# Deploy Gen2 function
gcloud functions deploy starwars-api-function `
    --gen2 `
    --runtime=python312 `
    --trigger-http `
    --allow-unauthenticated `
    --entry-point=starwars_api `
    --memory=256MB `
    --timeout=60s `
    --region=us-central1
```

**Saída esperada:**
```
Deploying function...
✓ Function starwars-api-function deployed
URL: https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function
```

### Passo 2: Testar Cloud Function Diretamente

```powershell
# Health check
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/

# Buscar personagem
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/api/v1/people/1
```

### Passo 3: Criar API Gateway

```powershell
# 3.1 Criar API
gcloud api-gateway apis create starwars-api `
    --display-name="Star Wars API"

# 3.2 Criar config com OpenAPI spec
gcloud api-gateway api-configs create starwars-config-v3 `
    --api=starwars-api `
    --openapi-spec=api_gateway_config.yaml `
    --display-name="Star Wars Config v3"

# 3.3 Criar gateway
gcloud api-gateway gateways create starwars-gateway `
    --api=starwars-api `
    --api-config=starwars-config-v3 `
    --location=us-central1 `
    --display-name="Star Wars Gateway"
```

### Passo 4: Obter URL do Gateway

```powershell
# Listar gateways
gcloud api-gateway gateways describe starwars-gateway `
    --location=us-central1 `
    --format="value(defaultHostname)"
```

**URL obtida:** `https://starwars-gateway-d9x6gbjl.uc.gateway.dev`

---

## 🐳 Deploy Cloud Run (Alternativo)

Deploy containerizado como alternativa:

### Build e Push

```powershell
# Voltar para raiz do projeto
cd ..

# Build da imagem
gcloud builds submit --tag gcr.io/starwars-api-2026/starwars-api

# Deploy no Cloud Run
gcloud run deploy starwars-api `
    --image gcr.io/starwars-api-2026/starwars-api `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --memory 256Mi `
    --timeout 60s `
    --min-instances 0 `
    --max-instances 10
```

**URL obtida:** `https://starwars-api-1040331397233.us-central1.run.app`

---

## ✅ Verificação

### Testar API Gateway (Principal)

```powershell
# Health check
curl https://starwars-gateway-d9x6gbjl.uc.gateway.dev/
# Esperado: {"status":"online","message":"Star Wars API Platform..."}

# Personagens
curl https://starwars-gateway-d9x6gbjl.uc.gateway.dev/api/v1/people/1
# Esperado: {"name":"Luke Skywalker",...}

# Filmes
curl https://starwars-gateway-d9x6gbjl.uc.gateway.dev/api/v1/films
# Esperado: Lista de 6 filmes

# Rankings
curl https://starwars-gateway-d9x6gbjl.uc.gateway.dev/api/v1/rankings/most-appeared
# Esperado: Top 10 personagens por aparições

# Timeline
curl https://starwars-gateway-d9x6gbjl.uc.gateway.dev/api/v1/timeline
# Esperado: Linha do tempo dos filmes
```

### Testar Cloud Run (Backup)

```powershell
curl https://starwars-api-1040331397233.us-central1.run.app/
curl https://starwars-api-1040331397233.us-central1.run.app/docs
```

---

## 🔄 Atualização

### Atualizar Cloud Function

```powershell
cd cloud_functions
gcloud functions deploy starwars-api-function `
    --gen2 `
    --runtime=python312 `
    --trigger-http `
    --allow-unauthenticated `
    --entry-point=starwars_api `
    --region=us-central1
```

### Atualizar API Gateway Config

```powershell
# Criar nova versão da config
gcloud api-gateway api-configs create starwars-config-v4 `
    --api=starwars-api `
    --openapi-spec=api_gateway_config.yaml

# Atualizar gateway para usar nova config
gcloud api-gateway gateways update starwars-gateway `
    --api=starwars-api `
    --api-config=starwars-config-v4 `
    --location=us-central1
```

### Atualizar Cloud Run

```powershell
gcloud builds submit --tag gcr.io/starwars-api-2026/starwars-api
gcloud run deploy starwars-api --image gcr.io/starwars-api-2026/starwars-api
```

---

## 🔧 Troubleshooting

### Erro: "Permission denied"

```powershell
# Verificar permissões
gcloud auth list
gcloud config list

# Re-autenticar se necessário
gcloud auth login
```

### Erro: "API not enabled"

```powershell
# Habilitar API específica
gcloud services enable <api-name>.googleapis.com
```

### Erro: "Function deployment failed"

```powershell
# Verificar logs
gcloud functions logs read starwars-api-function --gen2 --region=us-central1

# Verificar requirements.txt
cat cloud_functions/requirements.txt
```

### Erro: "Gateway returns 500"

```powershell
# Testar função diretamente
curl https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function/

# Verificar logs da função
gcloud functions logs read starwars-api-function --gen2 --limit=50
```

### Erro: "CORS blocked"

Os headers CORS são configurados automaticamente no `cloud_functions/main.py`:

```python
response.headers["Access-Control-Allow-Origin"] = "*"
response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
```

---

## 📊 Monitoramento

### Logs Cloud Functions

```powershell
# Logs em tempo real
gcloud functions logs read starwars-api-function --gen2 --limit=100

# Filtrar por erro
gcloud functions logs read starwars-api-function --gen2 --filter="severity>=ERROR"
```

### Logs Cloud Run

```powershell
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=starwars-api" --limit=50
```

### Console Web

- **Cloud Functions:** https://console.cloud.google.com/functions
- **API Gateway:** https://console.cloud.google.com/api-gateway
- **Cloud Run:** https://console.cloud.google.com/run

---

## 💰 Custos

| Serviço | Free Tier | Uso Atual |
|---------|-----------|-----------|
| Cloud Functions | 2M invocações/mês | ~10k |
| API Gateway | 2M chamadas/mês | ~10k |
| Cloud Run | 2M requests/mês | ~1k |
| Networking | 1GB egress/mês | ~100MB |
| Cloud Build | 120 min/dia | ~5 min |

**Custo estimado:** $0.00/mês ✅

---

## 📚 Referências

- [Cloud Functions Gen2 Docs](https://cloud.google.com/functions/docs)
- [API Gateway Docs](https://cloud.google.com/api-gateway/docs)
- [Cloud Run Docs](https://cloud.google.com/run/docs)
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)

---

> **Autor:** Vinícius Lopes | **Projeto:** PowerOfData Case Técnico
