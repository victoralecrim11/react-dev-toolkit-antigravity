# React Dev Hub Plugin — Antigravity Edition — v1.0.0

> Plugin de desenvolvimento orientado a aprendizado para planejar, construir, revisar, publicar e acompanhar projetos **React, Next.js e React Native/Expo** no **Google Antigravity**.

Adaptacao do [plugin-react-dev-toolkit](https://github.com/victoralecrim11/plugin-react-dev-toolkit) (Claude Code / Codex) para o formato nativo do Antigravity: `plugin.json` + `mcp_config.json` + `skills/`.

## Instalacao

Copie a pasta do plugin para um dos locais que o Antigravity varre:

- **Global (todos os projetos):** `~/.gemini/antigravity-cli/plugins/plugin-react-dev-toolkit/`
- **Só no projeto atual:** `.agents/plugins/plugin-react-dev-toolkit/` na raiz do workspace aberto.

Ou use o comando de instalacao:

```shell
agy plugin install https://github.com/victoralecrim11/plugin-react-dev-toolkit-antigravity.git
```

As skills carregam sozinhas — nao precisa copiar nada manualmente.

### MCP

O `mcp_config.json` do plugin ja declara os servidores MCP:

- **Vercel** — `https://mcp.vercel.com/`
- **Higgsfield** — `https://mcp.higgsfield.ai/mcp` (requer API key; edite o `mcp_config.json` e coloque sua chave no placeholder `COLOQUE_SUA_CHAVE_AQUI`)

O Antigravity le o `mcp_config.json` do plugin automaticamente. Para gerenciar via interface: **Settings → Permissions → MCP Tools → Add**.

## Como usar (linguagem natural)

O Antigravity nao usa slash-commands (`/`). As skills sao acionadas por linguagem natural:

1. **"configurar o ambiente"** → aciona a skill `setup` (perfil do dev, pasta-base, Project Hub)
2. **"criar projeto React"** → aciona `criar-projeto` (scaffolding TypeScript)
3. **"criar componente"** → aciona `criar-componente`
4. **"definir arquitetura"** → aciona `arquitetura`
5. **"revisar meu codigo"** → aciona `review`
6. **"publicar projeto"** → aciona `deploy`
7. **"gerar imagem do projeto"** → aciona `gerar-midia` (via Higgsfield MCP)
8. **"abrir dashboard"** → aciona `dashboard` (Project Hub local)

## Estrutura do plugin

```text
plugin-react-dev-toolkit-antigravity/
├── plugin.json                 # Marcador do plugin (Antigravity)
├── mcp_config.json             # MCP servers (Vercel + Higgsfield)
├── skills/                     # Skills do Antigravity (linguagem natural)
│   ├── react-dev/              # Base de conhecimento (references/)
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── react-core.md
│   │       ├── nextjs.md
│   │       ├── react-native.md
│   │       ├── project-builder.md
│   │       ├── deploy-advisor.md
│   │       ├── dashboard-projetos.md
│   │       └── project-hub/
│   ├── setup/
│   ├── criar-projeto/
│   ├── criar-componente/
│   ├── arquitetura/
│   ├── review/
│   ├── deploy/
│   ├── gerar-midia/
│   └── dashboard/
├── commands/                   # Instrucoes completas (referencia)
├── examples/
├── scripts/
│   └── validate-plugin.py
├── manual.html
├── LICENSE
└── README.md
```

## Padroes tecnicos

- **TypeScript estrito** — obrigatorio, nao configuravel.
- **Componentes funcionais e Hooks** — sem class components.
- **Zustand** — somente para estado global compartilhado e mutavel.
- **TanStack Query** — para dados remotos (cache, loading, erro).
- **Next.js** — App Router, Server Components, Server Actions.
- **React Native/Expo** — Expo managed, Expo Router, Hermes, Reanimated.

## Arquitetura que evolui com o projeto

| Nivel | Quando usar | Estrutura recomendada |
| --- | --- | --- |
| Beginner |Projeto academico, portifolio ou MVP pequeno | `components`, `screens`, `repositories`, `theme`, `types` |
| Junior | Mais telas, formularios ou reaproveitamento de logica | Adiciona `hooks` e `utils` |
| Mid-Level |Multiplas funcionalidades, integracoes ou equipe | Adiciona `features`, `store` e `shared` |
| Senior |Dominio complexo e evolucao de longo prazo | Modularizacao avancada somente com justificativa |

## Project Hub local

O painel local (`http://127.0.0.1:8766`) acompanha projetos, componentes, reviews e checklist arquitetural.Implementado com Python padrao (sem `pip`, sem banco de dados).

**Para iniciar:** acione a skill `setup` ("configurar o ambiente"). Ela copia os arquivos, sobe o servidor e abre o painel.

## Relacao com o repo original

Este repo e uma adaptacao do [plugin-react-dev-toolkit](https://github.com/victoralecrim11/plugin-react-dev-toolkit) para o Antigravity. O repo original mantem compatibilidade com Claude Code e Codex. Este repo foca exclusivamente no Antigravity.

Diferencas principais:

| |Repo original (Claude/Codex) |Este repo (Antigravity) |
|---|---|---|
| Manifesto | `.claude-plugin/plugin.json` + `.codex-plugin/plugin.json` | `plugin.json` (raiz) |
| MCP | `.mcp.json` | `mcp_config.json` |
| Comandos | `commands/` (slash-commands) | `skills/` (linguagem natural) |
| Skills | 1 skill `react-dev` com `references/` | 9 skills (1 base + 8 entry points) |

## Licenca

MIT — veja [LICENSE](LICENSE).
