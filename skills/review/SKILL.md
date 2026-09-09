---
name: review
description: Code review didatico com metricas de qualidade, passada de seguranca e registro no dashboard.
user-invocable: false
---

# Review

## Contrato de responsabilidade

`review` = code review técnico.
`qa-engineer` = QA / testes / regressão / investigação de bugs.
`quality-auditor` = gate final e consolidação.

Leia `devLevel` via `dashboard-config.json`. Revise preservando comportamento. Siga `./skills/react-dev/references/dashboard-projetos.md`. Registre via `POST /api/reviews`.

Avalie tipos, erros, loading e empty states, responsabilidades, performance (re-renderizacoes, cache, data-fetching e N+1, bundle), casos de borda, testes e divida tecnica. Valide acessibilidade (contrastes, focus, roles) e responsividade segundo `./skills/ui-ux/references/accessibility.md` e `./skills/ui-ux/references/responsive-design.md`. Se existir `.design/design-system.md` na raiz do projeto, valide a aderência dos tokens implementados (cores, tipografia, espaçamentos, variáveis CSS) contra o design system documentado — divergências são achados de categoria `[ui-ux]`. Para um problema pontual de UX já catalogado, use `python skills/ui-ux/scripts/search-uiux.py "<problema>" --domain ux` antes de descrever a correção do zero. Classifique por prioridade e explique o motivo.

Faca sempre uma passada de **seguranca**: segredo ou chave de API no codigo ou no bundle do cliente, `dangerouslySetInnerHTML` com conteudo do usuario, entrada nao validada em route handlers e Server Actions, token em `localStorage` ou `AsyncStorage`, autorizacao checada so no cliente e dados sensiveis expostos. Use o criterio de `./skills/react-dev/references/security-review.md` e trate achado critico como bloqueante. Para auditoria dedicada e mais profunda, aponte a skill `auditar-seguranca`.
