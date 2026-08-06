---
name: analisar-projeto-gsd
description: Analisa um projeto React, Next.js ou Expo construido com o framework GSD, cruzando os artefatos da pasta .planning (PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, phases) com o codigo real para achar deriva de spec, e corrige divergencias com aprovacao. Use quando o usuario falar de GSD, spec-driven, analisar projeto feito com GSD, .planning, roadmap versus codigo ou auditar aderencia a especificacao.
user-invocable: false
---

# Analisar projeto GSD

Siga o metodo completo de `./skills/react-dev/references/gsd-analyzer.md`.

1. Leia `devLevel` em `dashboard-config.json` (`GET /api/config`) para calibrar tom e profundidade. Nao pergunte o nivel; sem perfil, aplique o fallback de `./skills/react-dev/references/dashboard-projetos.md`.
2. Detecte a pasta `.planning/` na raiz do projeto. Se nao existir, avise em uma linha, ofereca a skill `review` no lugar e pare.
3. Cruze a intencao documentada (`PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`, `phases/XX-YY-PLAN.md` versus `XX-YY-SUMMARY.md`) com o codigo real, usando `./skills/react-dev/references/react-core.md` e a referencia da plataforma como criterio tecnico.
4. Classifique cada achado como `[spec]` ou `[qualidade]`, por prioridade. Apresente o relatorio antes de qualquer edicao e pergunte o que corrigir. Nao edite os artefatos `.planning/` por conta propria.
5. Registre via `POST /api/projects` (se ainda nao existir) e `POST /api/reviews`, com o estado do ciclo GSD no `summary`. Schema em `./skills/react-dev/references/dashboard-projetos.md`.
