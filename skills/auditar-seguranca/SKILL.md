---
name: auditar-seguranca
description: Auditoria de seguranca de projetos React, Next.js e Expo em busca de brechas exploraveis - segredos hardcoded ou vazados no bundle do cliente, dependencias vulneraveis, XSS, injecao, SSRF, autenticacao e autorizacao fragil, Server Actions sem validacao e exposicao de dados. Use quando o usuario falar de seguranca, vulnerabilidade, hackear, invadir, brecha, exploit, npm audit, segredo vazado, chave de API exposta, XSS, injecao, CSRF ou proteger o projeto.
user-invocable: false
---

# Auditar seguranca

Siga o modelo de ameacas e o checklist de `./skills/react-dev/references/security-review.md`. E o antidoto para as brechas tipicas de codigo gerado rapido: funciona na tela, mas deixa a porta aberta.

1. Leia `devLevel` em `dashboard-config.json` (`GET /api/config`) para calibrar a explicacao. Sem perfil, aplique o fallback de `./skills/react-dev/references/dashboard-projetos.md`. A calibracao muda a explicacao, **nao** o rigor: uma falha critica e sempre sinalizada como critica.
2. Detecte a stack (React, Next.js ou Expo) e percorra as categorias aplicaveis: segredos e variaveis de ambiente, dependencias, XSS, injecao, autenticacao e autorizacao, Server Actions e route handlers, especificidades de Expo, exposicao de dados e transporte.
3. Rode apenas checagens **nao destrutivas** (`npm audit --omit=dev` ou equivalente). Nunca explore uma falha de verdade nem envie dados para fora.
4. Classifique por severidade (Critico, Alto, Medio, Baixo) com onde, por que e exploravel e como corrigir. Apresente o relatorio antes de qualquer edicao e pergunte o que aplicar.
5. Segredo ja commitado: avise que e preciso **revogar e rotacionar** a credencial no provedor, nao apenas apagar do arquivo — ela ja esta no historico do Git. Nunca escreva um segredo real; use placeholder e `.env`.
6. Registre via `POST /api/reviews` usando `maintainability` como indice de postura de seguranca e `debts` com cada achado prefixado pela severidade. Schema em `./skills/react-dev/references/dashboard-projetos.md`.
