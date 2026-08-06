---
description: Faz code review didático e propõe refatorações seguras.
---
# /review

Leia `devLevel` em `dashboard-config.json` (`GET /api/config`) para calibrar o tom e a profundidade didática do review. Não pergunte o nível; se o perfil não existir, aplique o fallback da referência `./skills/react-dev/references/dashboard-projetos.md`.

Revise preservando comportamento. Avalie tipos, erros, loading/empty states, acessibilidade, responsabilidades, performance (re-renderizações, cache, data-fetching/N+1, bundle), casos de borda, testes e dívida técnica. Classifique achados por prioridade, explique o motivo e sugira correções graduais.

Faça sempre uma passada de **segurança** — segredos ou chaves de API no código/bundle do cliente, `dangerouslySetInnerHTML` com conteúdo do usuário, entrada não validada em route handlers e Server Actions, token em `localStorage`/`AsyncStorage`, autorização checada só no cliente e dados sensíveis expostos. Aplique o critério da referência `./skills/react-dev/references/security-review.md` e trate qualquer achado crítico como bloqueante. Para uma auditoria de segurança dedicada e mais profunda, aponte o usuário para `/auditar-seguranca`.

Registre o resultado via `POST /api/reviews` com as chaves exatas `project`, `maintainability` (0–100), `summary` e `debts` (lista). Schema completo na referência `./skills/react-dev/references/dashboard-projetos.md`.
