---
description: Cria componentes, hooks e testes TypeScript reutilizáveis.
---
# /criar-componente

Leia `devLevel` em `dashboard-config.json` (`GET /api/config`) para calibrar a profundidade da explicação e o grau de abstração. Não pergunte o nível; se o perfil não existir, aplique o fallback da referência `./skills/react-dev/references/dashboard-projetos.md`.

Crie componentes funcionais tipados, acessíveis e pequenos. Antes de extrair abstrações, confirme reutilização real. Separe hook, apresentação e acesso a dados quando isso reduzir complexidade. Inclua exemplos de uso e explique a responsabilidade de cada arquivo. Registre componentes reutilizáveis no catálogo do dashboard via `POST /api/components`, usando as chaves exatas `name`, `project`, `category`, `path` e `description` — `name` e `project` são obrigatórios, e `path` deve ser o caminho real do arquivo. Schema completo na referência `./skills/react-dev/references/dashboard-projetos.md`.
