---
description: Define arquitetura proporcional ao nível e à complexidade do projeto.
---
# /arquitetura

Leia `devLevel` em `dashboard-config.json` (`GET /api/config`) e use-o como teto de complexidade. Não pergunte o nível: ele foi definido no `/setup`. Se o perfil não existir, aplique o fallback da referência `./skills/react-dev/references/dashboard-projetos.md`.

Selecione a menor arquitetura que resolva o problema: estrutura simples para Beginner; hooks/utils para Junior; features/store/shared para Mid-Level; modularização avançada apenas quando a complexidade e a equipe justificarem. Para propor algo acima do `devLevel` registrado, aponte explicitamente qual requisito do projeto exige a exceção.

Explique trade-offs e atualize o checklist arquitetural do Project Hub.
