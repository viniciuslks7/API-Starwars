# 🔒 Política de Segurança

## Informações Sensíveis

Este projeto foi desenvolvido como um case técnico e **NÃO CONTÉM credenciais reais** ou informações sensíveis de produção.

### ✅ O que está seguro

- Não há chaves de API reais commitadas
- Não há credenciais Firebase/GCP no repositório
- Arquivos `.env` estão protegidos pelo `.gitignore`
- Service account keys estão bloqueados (`.gitignore`)

### ⚠️ Informações Públicas no Repositório

As seguintes informações estão intencionalmente expostas no repositório pois são **URLs públicas de demonstração**:

- **GCP Project ID**: `starwars-api-2026` - Projeto de demonstração temporário
- **Cloud Function URL**: `https://us-central1-starwars-api-2026.cloudfunctions.net/starwars-api-function`
- **API Gateway URL**: `https://starwars-gateway-d9x6gbjl.uc.gateway.dev`
- **Cloud Run URL**: `https://starwars-api-1040331397233.us-central1.run.app`

Estas URLs são:
- ✅ Públicas e sem autenticação (por design do projeto)
- ✅ Sem dados sensíveis ou pessoais
- ✅ Limitadas por rate limiting (100 req/min)
- ✅ Apenas consomem dados públicos da SWAPI
- ✅ Podem ser desativadas a qualquer momento

### 🔐 Boas Práticas Implementadas

1. **Arquivo `.env.example`**: Template sem valores reais
2. **`.gitignore` robusto**: Protege arquivos sensíveis
3. **Sem hardcoded secrets**: Todas as credenciais via variáveis de ambiente
4. **Rate Limiting**: 100 requisições/minuto por IP
5. **CORS controlado**: Configuração explícita
6. **Validação de entrada**: Pydantic models
7. **Logs sanitizados**: Sem exposição de dados sensíveis

### 📝 Para Deploy em Produção Real

Se você for usar este código em produção, **NUNCA commite**:

- ❌ Arquivos `.env` com valores reais
- ❌ Service account keys (`.json` do Firebase/GCP)
- ❌ Tokens de autenticação
- ❌ Chaves de API privadas
- ❌ Senhas ou secrets
- ❌ Informações pessoais (emails, telefones, etc)

### 🛡️ Checklist de Segurança para Produção

- [ ] Usar secrets manager (Google Secret Manager, AWS Secrets Manager)
- [ ] Habilitar autenticação Firebase/OAuth
- [ ] Configurar API Keys com rate limiting
- [ ] Implementar logging e monitoring
- [ ] Configurar WAF (Web Application Firewall)
- [ ] Revisar CORS para domínios específicos
- [ ] Habilitar HTTPS obrigatório
- [ ] Implementar input sanitization adicional
- [ ] Configurar backups e disaster recovery
- [ ] Realizar pentest e auditoria de segurança

### 📧 Reportar Vulnerabilidades

Se você encontrar uma vulnerabilidade de segurança neste projeto, por favor:

1. **NÃO abra uma issue pública**
2. Entre em contato diretamente via GitHub Issues (marque como privado)
3. Descreva a vulnerabilidade detalhadamente
4. Aguarde resposta antes de divulgar publicamente

### 📚 Referências

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google Cloud Security Best Practices](https://cloud.google.com/security/best-practices)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Pydantic Data Validation](https://docs.pydantic.dev/latest/)

---

**Última Atualização**: 2026-02-06
**Versão**: 1.0.0
