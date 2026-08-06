---
description: Analisa um projeto React/Next/Expo já construído com o framework GSD, cruzando os artefatos .planning/ com o código real, e corrige divergências.
---
# /analisar-projeto-gsd

Analisa um projeto que **já foi construído usando o framework GSD** (a pasta `.planning/` na raiz). Cruza a intenção documentada (`PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `phases/`) com o código React/Next/Expo que realmente existe, aponta divergências, faz o review técnico calibrado por nível e — com sua aprovação — corrige o que fugiu da spec. Registra o resultado no Project Hub.

Assuma o papel e o método definidos na referência **GSD Analyzer** (`./skills/react-dev/references/gsd-analyzer.md`).

1. Leia `devLevel` em `dashboard-config.json` (`GET /api/config`) para calibrar tom, profundidade e teto de complexidade. Não pergunte o nível; se o perfil não existir, aplique o fallback da `./skills/react-dev/references/dashboard-projetos.md`.
2. Detecte a pasta `.planning/` na raiz do projeto. Se ela não existir, o projeto não é GSD: avise em uma linha, ofereça `/review` no lugar e pare.
3. Siga a metodologia da referência: ler a intenção → ler o que foi entregue (`XX-YY-PLAN.md` vs `XX-YY-SUMMARY.md`) → cruzar com o código real usando `./skills/react-dev/references/react-core.md` e a referência da plataforma → verificar qualidade. Classifique cada achado como `[spec]` (deriva do que o `.planning/` documenta) ou `[qualidade]` (React/TS/arquitetura), priorizados.
4. Apresente o relatório **antes** de qualquer edição e pergunte o que corrigir. Corrija preservando comportamento, sem subir a arquitetura acima do `devLevel` sem justificar, e sem editar os artefatos `.planning/` por conta própria.
5. Registre no Project Hub via `POST /api/projects` (se ainda não existir) e `POST /api/reviews`, com as chaves exatas e o estado do ciclo GSD no `summary`. Schema completo na `./skills/react-dev/references/dashboard-projetos.md`. Se o painel estiver fora do ar, entregue o relatório e avise que o registro ficou pendente.
