# 🚀 Guia de Deploy - Cloud Run (GRATUITO)

> **Star Wars API Platform**  
> Deploy completo no Google Cloud Run usando apenas recursos gratuitos

---

## 📋 Pré-requisitos

1. **Conta Google Cloud** (gratuita)
   - Acesse: https://console.cloud.google.com
   - Crie uma conta (não precisa de cartão de crédito para free tier)

2. **Google Cloud CLI** instalado
   - Download: https://cloud.google.com/sdk/docs/install
   - Ou via PowerShell:
   ```powershell
   (New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:TEMP\GoogleCloudSDKInstaller.exe")
   & "$env:TEMP\GoogleCloudSDKInstaller.exe"
   ```

---

## 💰 Limites do Free Tier (Cloud Run)

| Recurso | Limite Gratuito/Mês |
|---------|---------------------|
| Requests | 2 milhões |
| CPU | 180,000 vCPU-segundos |
| Memória | 360,000 GiB-segundos |
| Networking | 1 GB egress (América do Norte) |

**Para este projeto:** Totalmente dentro do free tier! ✅

---

## 🔧 Passo a Passo do Deploy

### 1️⃣ Autenticar no Google Cloud

```powershell
# Login na conta Google
gcloud auth login

# Definir projeto (crie um novo se necessário)
gcloud projects create starwars-api-platform --name="Star Wars API"
gcloud config set project starwars-api-platform

# Habilitar APIs necessárias (GRATUITO)
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 2️⃣ Configurar Região

```powershell
# Usar região com melhor free tier
gcloud config set run/region us-central1
```

### 3️⃣ Deploy Direto (sem Docker local)

```powershell
# Navegar até a pasta do projeto
cd "c:\Users\vinic\OneDrive\Desktop\Api Starwars"

# Deploy com build automático no Cloud
gcloud run deploy starwars-api `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --memory 256Mi `
    --cpu 1 `
    --min-instances 0 `
    --max-instances 2 `
    --timeout 60 `
    --set-env-vars "DEBUG=false,ENVIRONMENT=production"
```

### 4️⃣ Verificar Deploy

```powershell
# Ver URL do serviço
gcloud run services describe starwars-api --region us-central1 --format="value(status.url)"

# Testar endpoint de saúde
$url = gcloud run services describe starwars-api --region us-central1 --format="value(status.url)"
Invoke-RestMethod "$url/health"
```

---

## 🔐 Configurar Variáveis de Ambiente

### Opção A: Via CLI

```powershell
gcloud run services update starwars-api `
    --region us-central1 `
    --set-env-vars "SWAPI_BASE_URL=https://swapi.dev/api,CACHE_ENABLED=true,CACHE_DEFAULT_TTL=3600"
```

### Opção B: Via Console

1. Acesse https://console.cloud.google.com/run
2. Clique no serviço `starwars-api`
3. Clique em "Edit & Deploy New Revision"
4. Na aba "Variables & Secrets", adicione:
   - `SWAPI_BASE_URL`: `https://swapi.dev/api`
   - `CACHE_ENABLED`: `true`
   - `DEBUG`: `false`

---

## 🔥 Configurar Firebase Auth (Opcional)

Se quiser usar autenticação Firebase:

### 1. Criar projeto Firebase (GRATUITO)

1. Acesse https://console.firebase.google.com
2. Crie novo projeto (pode usar o mesmo GCP project)
3. Ative Authentication > Sign-in methods > Email/Password

### 2. Gerar credenciais

1. Project Settings > Service Accounts
2. Clique "Generate New Private Key"
3. Salve o JSON

### 3. Adicionar ao Cloud Run

```powershell
# Criar secret com credenciais
gcloud secrets create firebase-credentials --data-file=path/to/firebase-key.json

# Montar secret no serviço
gcloud run services update starwars-api `
    --region us-central1 `
    --set-secrets "/app/firebase-credentials.json=firebase-credentials:latest"
```

---

## 📊 Monitoramento (GRATUITO)

### Ver Logs

```powershell
# Logs em tempo real
gcloud run services logs read starwars-api --region us-central1 --limit 100

# Logs contínuos
gcloud run services logs tail starwars-api --region us-central1
```

### Métricas no Console

1. Acesse https://console.cloud.google.com/run
2. Clique no serviço
3. Aba "Metrics" mostra:
   - Request count
   - Latency
   - Container instances
   - Memory/CPU usage

---

## 🔄 Atualizar Deploy

Quando fizer alterações no código:

```powershell
# Novo deploy (mesmo comando)
gcloud run deploy starwars-api `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated
```

---

## 🧪 Testar em Produção

Após o deploy, teste os endpoints:

```powershell
# Definir URL base
$API_URL = "https://starwars-api-xxxxx-uc.a.run.app"  # Substitua pela sua URL

# Testar health
Invoke-RestMethod "$API_URL/health"

# Testar listagem de personagens
Invoke-RestMethod "$API_URL/api/v1/people"

# Testar personagem específico
Invoke-RestMethod "$API_URL/api/v1/people/1"

# Testar com filtros
Invoke-RestMethod "$API_URL/api/v1/people?gender=male&sort_by=name"

# Testar estatísticas
Invoke-RestMethod "$API_URL/api/v1/statistics/films"
```

---

## ⚠️ Troubleshooting

### Erro: "Permission denied"

```powershell
gcloud auth login
gcloud config set project starwars-api-platform
```

### Erro: "Quota exceeded"

- Verifique se está dentro do free tier
- Aguarde reset do mês

### Erro: "Container failed to start"

```powershell
# Ver logs de erro
gcloud run services logs read starwars-api --region us-central1
```

### Erro de dependências

```powershell
# Verificar se requirements.txt está correto
gcloud builds log [BUILD_ID]
```

---

## ✅ Checklist de Deploy

- [ ] Google Cloud CLI instalado
- [ ] Projeto GCP criado
- [ ] APIs habilitadas (Run, Build)
- [ ] Deploy executado com sucesso
- [ ] URL do serviço obtida
- [ ] Endpoint /health respondendo
- [ ] Endpoints da API funcionando
- [ ] Variáveis de ambiente configuradas

---

## 🎉 Pronto!

Após o deploy, você terá:
- **URL pública**: `https://starwars-api-xxxxx-uc.a.run.app`
- **Swagger UI**: `https://starwars-api-xxxxx-uc.a.run.app/docs`
- **OpenAPI JSON**: `https://starwars-api-xxxxx-uc.a.run.app/openapi.json`

Tudo **100% GRATUITO** dentro dos limites do free tier! 🚀
