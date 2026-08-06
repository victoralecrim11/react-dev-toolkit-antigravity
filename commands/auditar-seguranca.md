---
description: Faz uma auditoria de segurança do projeto React/Next/Expo — segredos vazados, deps vulneráveis, XSS, injeção, auth frágil e exposição de dados — e propõe correções.
---
# /auditar-seguranca

Audita a segurança do projeto atual em busca de brechas que possam ser exploradas: segredos hardcoded ou vazados no bundle do cliente, dependências vulneráveis, XSS, injeção, autenticação/autorização frágil e dados sensíveis expostos. É o antídoto para o padrão de "vibe coding" — código que funciona na tela mas deixa a porta aberta.

Assuma o papel e o método da referência **Security Review** (`./skills/react-dev/references/security-review.md`).

1. Leia `devLevel` em `dashboard-config.json` (`GET /api/config`) para calibrar a profundidade da explicação. Não pergunte o nível; se o perfil não existir, aplique o fallback da `./skills/react-dev/references/dashboard-projetos.md`. A calibração muda a explicação, **não** o rigor: uma falha crítica é sempre sinalizada como crítica.
2. Detecte a stack (React, Next.js ou Expo) e percorra o checklist da referência nas categorias que se aplicam. Rode checagens **não destrutivas** como `npm audit` quando fizer sentido; nunca explore uma falha nem exfiltre dados.
3. Classifique cada achado por severidade (Crítico / Alto / Médio / Baixo) com onde, por que é explorável e como corrigir.
4. Apresente o relatório **antes** de qualquer edição e pergunte o que corrigir. Corrija preservando comportamento. Segredo já commitado: avise que é preciso **revogar e rotacionar** a credencial no provedor, não só apagar do arquivo — ela já está no histórico do Git. Nunca escreva um segredo real; use placeholder + `.env`.
5. Registre via `POST /api/reviews` usando `maintainability` como índice de postura de segurança e `debts` com cada achado prefixado pela severidade. Schema em `./skills/react-dev/references/dashboard-projetos.md`. Se o painel estiver fora do ar, entregue o relatório e avise que o registro ficou pendente.
