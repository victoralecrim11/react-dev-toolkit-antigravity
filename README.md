# React Dev Hub Plugin — Antigravity Edition — v1.0.2
> Plugin de desenvolvimento orientado a aprendizado para planejar, construir, revisar, publicar e acompanhar projetos **React, Next.js e React Native/Expo** no **Google Antigravity**.

Adaptacao do [plugin-react-dev-toolkit](https://github.com/victoralecrim11/plugin-react-dev-toolkit) (Claude Code / Codex) para o formato nativo do Antigravity: `plugin.json` + `mcp_config.json` + `skills/`.

## Instalacao

Copie a pasta do plugin para um dos locais que o Antigravity varre:

- **Global (todos os projetos):** `~/.gemini/config/plugins/plugin-react-dev-toolkit/`
  - Windows: `C:\Users\SEU_USUARIO\.gemini\config\plugins\plugin-react-dev-toolkit\`
  - macOS/Linux: `~/.gemini/config/plugins/plugin-react-dev-toolkit/`
- **So no projeto atual:** `.agents/plugins/plugin-react-dev-toolkit/` na raiz do workspace aberto.

Ou use o comando de instalacao:

```shell
agy plugin install https://github.com/victoralecrim11/plugin-react-dev-toolkit-antigravity.git
```

> Se a pasta `~/.gemini/config/plugins/` nao existir ainda, crie ela.

As skills carregam sozinhas — nao precisa copiar nada manualmente.

### Desinstalar

```shell
agy plugin uninstall plugin-react-dev-toolkit
```

Se o cache nao limpar direito, remova manualmente:

```shell
# Windows
rmdir /s /q "%USERPROFILE%\.gemini\config\plugins\plugin-react-dev-toolkit"
rmdir /s /q "%USERPROFILE%\.gemini\antigravity-cli\plugins\plugin-react-dev-toolkit"

# macOS / Linux
rm -rf ~/.gemini/config/plugins/plugin-react-dev-toolkit
rm -rf ~/.gemini/antigravity-cli/plugins/plugin-react-dev-toolkit
```

Depois reinstale com `agy plugin install`.

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
├── scripts/
│   ├── bump-version.py         # Sincroniza a versao no plugin.json, README e manual
│   ├── validate-plugin.py      # Checagens de estrutura (roda no CI)
│   ├── atualizar-plugin.ps1    # Atualiza o Antigravity (Windows)
│   └── atualizar-plugin.sh     # Atualiza o Antigravity (macOS/Linux)
├── .github/workflows/
│   └── bump-version.yml        # Bump, validacao e tag no push da main
├── manual.html
├── LICENSE
└── README.md
```

## Atualizar depois de um push

O Antigravity compara o campo `version` do `plugin.json` para detectar atualizacao. O repositorio tem um workflow que **bumpa o patch e sincroniza a versao** a cada push na `main` — voce commita normal, a Action publica.

```
.github/workflows/bump-version.yml   # bump + validacao + tag, no push da main
scripts/bump-version.py              # sincroniza a versao em 3 lugares
scripts/validate-plugin.py           # checagens de estrutura, roda no CI
scripts/atualizar-plugin.ps1 / .sh   # atualiza sua maquina
```

O workflow valida antes de taguear. Para pular o bump num commit so de documentacao, o workflow ja ignora mudancas em `**/*.md`, `manual.html`, `LICENSE`, `.github/**` e `scripts/**`. Para forcar um `minor` ou `major`, use **Actions → Bump da versao do plugin → Run workflow** e escolha a parte.

### Na sua maquina

```shell
# Windows
powershell scripts/atualizar-plugin.ps1

# macOS / Linux
./scripts/atualizar-plugin.sh
```

Se algo ficar preso numa versao antiga, `--limpar-cache` remove o plugin instalado antes de reinstalar.

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
| Beginner | Projeto academico, portifolio ou MVP pequeno | `components`, `screens`, `repositories`, `theme`, `types` |
| Junior | Mais telas, formularios ou reaproveitamento de logica | Adiciona `hooks` e `utils` |
| Mid-Level | Multiplas funcionalidades, integracoes ou equipe | Adiciona `features`, `store` e `shared` |
| Senior | Dominio complexo e evolucao de longo prazo | Modularizacao avancada somente com justificativa |

## Project Hub local

O painel local (`http://127.0.0.1:8766`) acompanha projetos, componentes, reviews e checklist arquitetural. Implementado com Python padrao (sem `pip`, sem banco de dados).

**Para iniciar:** acione a skill `setup` ("configurar o ambiente"). Ela copia os arquivos, sobe o servidor e abre o painel.

### Onde ficam os dados

Dois arquivos ficam ao lado de `dashboard-server.py`:

- **`projetos-data.json`** — projetos, componentes, reviews e checklists.
- **`dashboard-config.json`** — seu perfil (`devLevel`, `projectsRoot`, etc.).

Ambos estao no `.gitignore`.

## Relacao com o repo original

Este repo e uma adaptacao do [plugin-react-dev-toolkit](https://github.com/victoralecrim11/plugin-react-dev-toolkit) para o Antigravity. O repo original mantem compatibilidade com Claude Code e Codex. Este repo foca exclusivamente no Antigravity.

| | Repo original (Claude/Codex) | Este repo (Antigravity) |
|---|---|---|
| Manifesto | `.claude-plugin/plugin.json` + `.codex-plugin/plugin.json` | `plugin.json` (raiz) |
| MCP | `.mcp.json` | `mcp_config.json` |
| Comandos | `commands/` (slash-commands) | `skills/` (linguagem natural) |
| Skills | 1 skill `react-dev` com `references/` | 9 skills (1 base + 8 entry points) |
| Bump | 4 manifestos + README + manual | `plugin.json` + README + manual |
| Caminho global | `~/.claude/plugins/cache/` | `~/.gemini/config/plugins/` |

## Licenca

MIT — veja [LICENSE](LICENSE).
