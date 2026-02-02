# Script de Deploy - Cloud Functions + API Gateway
# Star Wars API Platform
# 
# Uso: .\deploy_cloud_functions.ps1
#
# Pré-requisitos:
# - gcloud CLI instalado e autenticado
# - Projeto GCP configurado

param(
    [string]$ProjectId = "starwars-api-2026",
    [string]$Region = "us-central1",
    [string]$FunctionName = "starwars-api"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Star Wars API - Cloud Functions Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configurar projeto
Write-Host "1. Configurando projeto GCP..." -ForegroundColor Yellow
gcloud config set project $ProjectId

# Habilitar APIs necessárias
Write-Host ""
Write-Host "2. Habilitando APIs necessárias..." -ForegroundColor Yellow
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com

# Deploy da Cloud Function
Write-Host ""
Write-Host "3. Fazendo deploy da Cloud Function..." -ForegroundColor Yellow
Write-Host "   Isso pode levar alguns minutos..." -ForegroundColor Gray

Push-Location cloud_functions

gcloud functions deploy $FunctionName `
    --gen2 `
    --runtime python312 `
    --region $Region `
    --source . `
    --entry-point starwars_api `
    --trigger-http `
    --allow-unauthenticated `
    --memory 256MB `
    --timeout 60s `
    --min-instances 0 `
    --max-instances 10

Pop-Location

# Obter URL da função
Write-Host ""
Write-Host "4. Obtendo URL da função..." -ForegroundColor Yellow
$functionUrl = gcloud functions describe $FunctionName --region $Region --format="value(serviceConfig.uri)" 2>$null

if ($functionUrl) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host " DEPLOY CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Cloud Function URL:" -ForegroundColor Cyan
    Write-Host "  $functionUrl" -ForegroundColor White
    Write-Host ""
    Write-Host "Endpoints disponíveis:" -ForegroundColor Cyan
    Write-Host "  GET $functionUrl/health" -ForegroundColor White
    Write-Host "  GET $functionUrl/people" -ForegroundColor White
    Write-Host "  GET $functionUrl/films" -ForegroundColor White
    Write-Host "  GET $functionUrl/starships" -ForegroundColor White
    Write-Host "  GET $functionUrl/planets" -ForegroundColor White
    Write-Host "  GET $functionUrl/rankings/tallest-characters" -ForegroundColor White
    Write-Host "  GET $functionUrl/timeline/films/chronological" -ForegroundColor White
    Write-Host ""
    
    # Testar health endpoint
    Write-Host "5. Testando endpoint /health..." -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "$functionUrl/health" -Method GET
        Write-Host "   Status: $($response.status)" -ForegroundColor Green
        Write-Host "   Service: $($response.service)" -ForegroundColor Green
    } catch {
        Write-Host "   Erro ao testar: $_" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "Erro ao obter URL da função." -ForegroundColor Red
    Write-Host "Verifique o console do GCP para detalhes." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Próximo passo: Configurar API Gateway" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para configurar o API Gateway, execute:" -ForegroundColor Yellow
Write-Host '  gcloud api-gateway apis create starwars-api --project=$ProjectId' -ForegroundColor White
Write-Host '  gcloud api-gateway api-configs create starwars-config \' -ForegroundColor White
Write-Host '    --api=starwars-api \' -ForegroundColor White
Write-Host '    --openapi-spec=cloud_functions/api_gateway_config.yaml \' -ForegroundColor White
Write-Host '    --project=$ProjectId' -ForegroundColor White
Write-Host ""
