#!/bin/bash
# ========================================
# Git Pre-Commit Hook (Opcional)
# Star Wars API Platform
# ========================================
#
# Este hook roda automaticamente antes de cada commit
# para verificar vazamento de informações sensíveis
#
# Instalação:
#   cp scripts/pre-commit.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Para pular o hook (use com cautela!):
#   git commit --no-verify
#

echo "🔒 Running security checks before commit..."
echo ""

# Run the security check script
if ! ./scripts/security_check.sh; then
    echo ""
    echo "❌ Commit abortado devido a problemas de segurança!"
    echo ""
    echo "Corrija os problemas listados acima antes de fazer commit."
    echo "Para pular este check (NÃO RECOMENDADO), use: git commit --no-verify"
    exit 1
fi

echo ""
echo "✅ Security checks passed! Proceeding with commit..."
exit 0
