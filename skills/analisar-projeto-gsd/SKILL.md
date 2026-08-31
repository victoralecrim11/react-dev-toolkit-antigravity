---
name: analisar-projeto-gsd
description: Analisa um projeto React, Next.js ou Expo construido com o framework GSD, cruzando os artefatos da pasta .planning (PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, phases) com o codigo real para achar deriva de spec, e corrige divergencias com aprovacao. Use quando o usuario falar de GSD, spec-driven, analisar projeto feito com GSD, .planning, roadmap versus codigo ou auditar aderencia a especificacao.
user-invocable: false
---

# Analisar projeto GSD

Siga o método completo de `./skills/react-dev/references/gsd-analyzer.md`.

1. Leia `devLevel` em `dashboard-config.json` (`GET /api/config`) para calibrar tom e profundidade. Não pergunte o nível; sem perfil, aplique o fallback de `./skills/react-dev/references/dashboard-projetos.md`.
2. Detecte a pasta `.planning/` na raiz do projeto. Se não existir, avise em uma linha, ofereça a skill `review` no lugar e pare.
3. Cruze a intenção documentada (`PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`, `phases/XX-YY-PLAN.md` versus `XX-YY-SUMMARY.md`) com o código real, usando:
   * `./skills/react-dev/references/react-core.md` e a referência da plataforma como critério técnico.
   * `./skills/ui-ux/references/accessibility.md` e `./skills/ui-ux/references/responsive-design.md` como critério de interface e usabilidade.
   * `./skills/ui-ux/data/colors.csv` e `styles.csv` para checar aderência a tokens do Design System.
4. Classifique cada achado como `[spec]`, `[qualidade]` ou `[ui-ux]`, por prioridade. Apresente o relatório antes de qualquer edição e pergunte o que corrigir. Não edite os artefatos `.planning/` por conta própria.
5. Registre via `POST /api/projects` (se ainda não existir) e `POST /api/reviews`, com o estado do ciclo GSD no `summary`. Schema em `./skills/react-dev/references/dashboard-projetos.md`.