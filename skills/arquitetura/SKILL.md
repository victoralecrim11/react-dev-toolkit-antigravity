---
name: arquitetura
description: Estrutura de pastas e arquitetura proporcional ao nivel do desenvolvedor.
user-invocable: false
---

Leia `devLevel` via `GET /api/config`. Siga `./skills/react-dev/references/dashboard-projetos.md` se o perfil nao existir.

Selecione a menor arquitetura que resolva o problema. Explique trade-offs e atualize o checklist arquitetural do Project Hub.
Em decisoes de interface e estado de telas, garanta desacoplamento dos tokens visuais. Se existir `.design/design-system.md` na raiz do projeto, use-o como fonte primária de tokens. Caso contrário, consulte via `python skills/ui-ux/scripts/search-uiux.py "<termo>" --domain color`/`--domain style` e as diretrizes de `./skills/ui-ux/references/responsive-design.md`.