---
description: Planeja e cria o scaffolding TypeScript de um projeto React, Next.js ou Expo.
---
# /criar-projeto

Roda **uma vez por projeto**. É aqui que a estrutura de pastas e os arquivos da aplicação nascem.

## Antes de perguntar

Leia o perfil salvo em `dashboard-config.json` (ou `GET /api/config`) e use `devLevel`, `projectsRoot`, `defaultPlatform` e `defaultGoal` como valores de partida. **Não repergunte o nível de calibração** — ele já foi definido no `/setup`.

Se o perfil não existir, aplique o fallback da referência `./skills/react-dev/references/dashboard-projetos.md`: avise que `/setup` não rodou, assuma `Junior` como nível provisório, colete só nome/pasta/plataforma e sugira `/setup` ao final. Não pergunte o nível.

Pergunte apenas o que é específico deste projeto:

- Nome e pasta de destino (padrão: dentro de `projectsRoot`).
- Plataforma, se diferente de `defaultPlatform`.
- Objetivo **deste projeto** e escopo do MVP (padrão: `defaultGoal`).

Para uma ideia vaga, use `./skills/react-dev/references/project-builder.md` em modo Discovery: defina público, objetivo, MVP, premissas e riscos antes de gerar qualquer código.

## Geração

Aplique `./skills/react-dev/references/react-core.md` e a referência da plataforma (`./skills/react-dev/references/nextjs.md` ou `./skills/react-dev/references/react-native.md`). Use a estrutura de pastas correspondente ao `devLevel` do perfil — não adote arquitetura acima do nível registrado sem apontar explicitamente por que este projeto exige a exceção.

TypeScript estrito, componentes funcionais e Hooks. Sem class components e sem dependências legadas. Prefira Context/Hooks; Zustand somente para estado global compartilhado e mutável; TanStack Query para estado remoto.

## Entrega

1. Estrutura de pastas criada.
2. Arquivos iniciais e configurações (`tsconfig`, lint, formatação).
3. Comandos de instalação e execução.
4. Justificativa curta de cada escolha, com alternativa e trade-off.
5. Registro do projeto no Project Hub via `POST /api/projects`, com **todos** os campos preenchidos e usando as chaves exatas:

   ```json
   {
     "name": "<nome da pasta do projeto>",
     "path": "<caminho absoluto real da pasta que você acabou de criar>",
     "platform": "React | Next.js | Expo",
     "status": "mvp",
     "reactVersion": "<versão instalada, ex. 19>",
     "stack": "<bibliotecas principais escolhidas>",
     "level": "<devLevel do perfil>",
     "notes": "",
     "repoUrl": ""
   }
   ```

   `name` e `path` são obrigatórios — sem `path` o painel não consegue detectar componentes depois. Nunca use placeholder no `path`: você criou a pasta, então já sabe o caminho absoluto. Confira o array `warnings` da resposta e complete o que ele apontar antes de seguir. O schema completo, incluindo componentes e reviews, está na referência `./skills/react-dev/references/dashboard-projetos.md`.

6. Próximos passos concretos.
