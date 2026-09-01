---
name: criar-projeto
description: Scaffolding TypeScript de projeto React, Next.js ou Expo com UI/UX Design System e registro no dashboard.
user-invocable: false
---

# Criar projeto

Roda uma vez por projeto.

1. **Discovery & Arquitetura:** Leia o perfil e aplique `./skills/react-dev/references/project-builder.md` via Discovery.
2. **Design System & UI/UX:** Invoque a skill `ui-ux` para executar o Fluxo de Operação completo (Reasoning & Handoff). Ela gerará o artefato `.design/design-system.md` na raiz do projeto com todos os tokens de paleta, tipografia, estilo visual, padrão de interface e acessibilidade. Leia esse arquivo para aplicar os tokens ao scaffolding. Se a skill `ui-ux` não estiver disponível, faça fallback para `python skills/ui-ux/scripts/search-uiux.py "<nicho/produto>" --domain product` e `--domain style`/`--domain color`/`--domain typography`. Aplique os padrões de `./skills/ui-ux/references/responsive-design.md`.
3. **Scaffolding:** Crie a estrutura de diretórios e arquivos TypeScript estritos adequados à stack (Next.js, Vite ou Expo).
4. **Registro:** Registre o projeto via `POST /api/projects`. Siga `./skills/react-dev/references/dashboard-projetos.md` para o schema exato.