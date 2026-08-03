---
description: Faz code review didático e propõe refatorações seguras.
---
# /review

Leia `devLevel` em `dashboard-config.json` (`GET /api/config`) para calibrar o tom e a profundidade didática do review. Não pergunte o nível; se o perfil não existir, aplique o fallback da referência `./skills/react-dev/references/dashboard-projetos.md`.

Revise preservando comportamento. Avalie tipos, erros, loading/empty states, acessibilidade, segurança, responsabilidades, performance, testes e dívida técnica. Classifique achados por prioridade, explique o motivo e sugira correções graduais. Registre o resultado via `POST /api/reviews` com as chaves exatas `project`, `maintainability` (0–100), `summary` e `debts` (lista). Schema completo na referência `./skills/react-dev/references/dashboard-projetos.md`.
