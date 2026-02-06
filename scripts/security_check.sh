#!/bin/bash
# ========================================
# Security Audit Script
# Star Wars API Platform
# ========================================
#
# Este script verifica se há vazamento de informações sensíveis
# no repositório antes de fazer commit ou push
#
# Uso: ./scripts/security_check.sh
#

set -e

echo "🔒 Security Audit - Star Wars API Platform"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
WARNINGS=0
ERRORS=0

# Check 1: Verify .env is not tracked
echo "📋 Check 1: Verificando arquivos .env..."
if git ls-files | grep -q "^\.env$"; then
    echo -e "${RED}❌ ERRO: Arquivo .env está sendo rastreado pelo Git!${NC}"
    echo "   Execute: git rm --cached .env"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ OK: Arquivo .env não está rastreado${NC}"
fi
echo ""

# Check 2: Look for service account keys
echo "📋 Check 2: Verificando service account keys..."
if git ls-files | grep -E "serviceAccountKey\.json|firebase-adminsdk.*\.json"; then
    echo -e "${RED}❌ ERRO: Service account key encontrado no Git!${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ OK: Nenhum service account key rastreado${NC}"
fi
echo ""

# Check 3: Search for hardcoded secrets
echo "📋 Check 3: Procurando por secrets hardcoded..."
PATTERNS=(
    "sk-[a-zA-Z0-9]{32,}"  # OpenAI keys
    "AIza[0-9A-Za-z\\-_]{35}"  # Google API keys
    "AKIA[0-9A-Z]{16}"  # AWS Access Key
    "ghp_[a-zA-Z0-9]{36}"  # GitHub Personal Access Token
    "gho_[a-zA-Z0-9]{36}"  # GitHub OAuth Token
)

for pattern in "${PATTERNS[@]}"; do
    if git grep -E "$pattern" -- '*.py' '*.js' '*.ts' '*.json' 2>/dev/null; then
        echo -e "${RED}⚠️  AVISO: Possível API key encontrada!${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
done

if [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ OK: Nenhuma API key hardcoded encontrada${NC}"
fi
echo ""

# Check 4: Verify .gitignore is protecting sensitive files
echo "📋 Check 4: Verificando .gitignore..."
REQUIRED_PATTERNS=(
    "\.env"
    "serviceAccountKey\.json"
    "firebase-adminsdk"
)

MISSING=0
for pattern in "${REQUIRED_PATTERNS[@]}"; do
    if ! grep -q "$pattern" .gitignore; then
        echo -e "${YELLOW}⚠️  AVISO: Pattern '$pattern' não encontrado no .gitignore${NC}"
        MISSING=$((MISSING + 1))
    fi
done

if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}✅ OK: .gitignore está protegendo arquivos sensíveis${NC}"
fi
echo ""

# Check 5: Look for TODO comments with sensitive info
echo "📋 Check 5: Verificando TODOs com informações sensíveis..."
if git grep -i "TODO.*password\|TODO.*secret\|TODO.*key" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  AVISO: TODO com possível referência a senha/secret${NC}"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✅ OK: Nenhum TODO suspeito encontrado${NC}"
fi
echo ""

# Check 6: Verify if .env.example exists
echo "📋 Check 6: Verificando .env.example..."
if [ ! -f ".env.example" ]; then
    echo -e "${YELLOW}⚠️  AVISO: .env.example não encontrado${NC}"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}✅ OK: .env.example existe${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo "📊 RESUMO DA AUDITORIA"
echo "=========================================="
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ APROVADO: Repositório seguro!${NC}"
    echo ""
    echo "Nenhum problema de segurança detectado."
    exit 0
elif [ $ERRORS -gt 0 ]; then
    echo -e "${RED}❌ REPROVADO: $ERRORS erro(s) crítico(s) encontrado(s)${NC}"
    echo -e "${YELLOW}⚠️  $WARNINGS aviso(s)${NC}"
    echo ""
    echo "CORRIJA OS ERROS antes de fazer commit!"
    exit 1
else
    echo -e "${YELLOW}⚠️  ATENÇÃO: $WARNINGS aviso(s) encontrado(s)${NC}"
    echo ""
    echo "Revise os avisos, mas o repositório pode ser commitado."
    exit 0
fi
