# React Dev Hub Plugin — Antigravity Edition — v1.2.1
> Plugin de desenvolvimento orientado a aprendizado para planejar, construir, revisar, publicar e acompanhar projetos **React, Next.js e React Native/Expo** no **Google Antigravity**.

Adaptacao do [plugin-react-dev-toolkit](https://github.com/victoralecrim11/plugin-react-dev-toolkit) para o formato nativo do Antigravity: `plugin.json` + `mcp_config.json` + `skills/` + `rules/`.

Inclui a skill `analisar-projeto-gsd`, que audita projetos construidos com o **framework GSD** cruzando os artefatos da pasta `.planning/` com o codigo real, a skill `auditar-seguranca`, que caca as brechas tipicas de codigo gerado rapido, e os **guardrails sempre ativos** de `rules/`, que previnem essas brechas antes de existirem.

## Indice

- [React Dev Hub Plugin — Antigravity Edition — v1.2.1](#react-dev-hub-plugin--antigravity-edition--v121)
  - [Indice](#indice)
  - [Instalacao](#instalacao)
    - [Desinstalar](#desinstalar)
    - [MCP](#mcp)
  - [Como usar (linguagem natural)](#como-usar-linguagem-natural)
  - [Estrutura do plugin](#estrutura-do-plugin)
    - [O que cada pasta faz](#o-que-cada-pasta-faz)
  - [Guardrails sempre ativos (`rules/`)](#guardrails-sempre-ativos-rules)
  - [Seguranca](#seguranca)
  - [Projetos feitos com o framework GSD](#projetos-feitos-com-o-framework-gsd)
  - [Atualizar depois de um push](#atualizar-depois-de-um-push)
    - [Atualizar o plugin](#atualizar-o-plugin)
  - [Padroes tecnicos](#padroes-tecnicos)
  - [Arquitetura que evolui com o projeto](#arquitetura-que-evolui-com-o-projeto)
  - [Project Hub local](#project-hub-local)
    - [Onde ficam os dados](#onde-ficam-os-dados)
  - [Relacao com o repo original](#relacao-com-o-repo-original)
  - [O que mudou na v1.2.1](#o-que-mudou-na-v121)
  - [O que mudou na v1.1.1](#o-que-mudou-na-v111)
  - [Licenca](#licenca)

## Instalacao

Copie a pasta do plugin para um dos locais que o Antigravity varre:

- **Global (todos os projetos):** `~/.gemini/config/plugins/plugin-react-dev-toolkit/`
  - Windows: `C:\Users\SEU_USUARIO\.gemini\config\plugins\plugin-react-dev-toolkit\`
  - macOS/Linux: `~/.gemini/config/plugins/plugin-react-dev-toolkit/`
- **So no projeto atual:** `.agents/plugins/plugin-react-dev-toolkit/` na raiz do workspace aberto (o Antigravity tambem aceita `_agents/plugins/`).

Para instalacao inicial, use:

```shell
agy plugin install https://github.com/victoralecrim11/plugin-react-dev-toolkit-antigravity.git
```

> Se a pasta `~/.gemini/config/plugins/` nao existir ainda, crie ela.

As skills e as rules carregam sozinhas — nao precisa copiar nada manualmente.

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

| Diga algo como | Aciona a skill | O que faz |
| :-- | :-- | :-- |
| "configurar o ambiente" | `setup` | Perfil do dev, pasta-base e instalacao do Project Hub |
| "criar projeto React" | `criar-projeto` | Discovery do MVP e scaffolding TypeScript |
| "criar componente" | `criar-componente` | Componentes, hooks e testes tipados |
| "definir arquitetura" | `arquitetura` | Pastas, estado e responsabilidades proporcionais ao nivel |
| "revisar meu codigo" | `review` | Code review didatico, com passada de seguranca embutida |
| "auditar a seguranca do projeto" | `auditar-seguranca` | Auditoria de brechas por severidade |
| "analisar meu projeto GSD" | `analisar-projeto-gsd` | Cruza os artefatos `.planning/` com o codigo real |
| "publicar projeto" | `deploy` | Analisa a stack, valida o build e publica |
| "gerar imagem do projeto" | `gerar-midia` | Hero, OG image ou video curto via Higgsfield MCP |
| "abrir dashboard" | `dashboard` | Reabre o Project Hub local |

## Estrutura do plugin

Estrutura atual do repositorio — este bloco reflete os arquivos e pastas realmente presentes.

```text
plugin-react-dev-toolkit-antigravity/
├── plugin.json                      # manifesto do Antigravity (name, version, description)
├── mcp_config.json                  # servidores MCP: vercel + higgsfield
├── rules/                           # guardrails SEMPRE ativos
│   ├── seguranca.md
│   └── typescript-estrito.md
├── skills/                          # pontos de entrada (linguagem natural)
│   ├── setup/SKILL.md
│   ├── criar-projeto/SKILL.md
│   ├── criar-componente/SKILL.md
│   ├── arquitetura/SKILL.md
│   ├── review/SKILL.md
│   ├── auditar-seguranca/SKILL.md
│   ├── analisar-projeto-gsd/SKILL.md
│   ├── deploy/SKILL.md
│   ├── gerar-midia/SKILL.md
│   └── dashboard/SKILL.md
├── commands/                        # paridade com a versao original; o Antigravity NAO usa
│   ├── setup.md
│   ├── criar-projeto.md
│   ├── criar-componente.md
│   ├── arquitetura.md
│   ├── review.md
│   ├── auditar-seguranca.md
│   ├── analisar-projeto-gsd.md
│   ├── deploy.md
│   ├── gerar-midia.md
│   └── dashboard.md
├── scripts/
│   ├── bump-version.py              # sincroniza a versao em 3 lugares
│   ├── validate-plugin.py           # checagens de estrutura, roda no CI
│   ├── atualizar-plugin.ps1
│   └── atualizar-plugin.sh
├── .github/
│   └── workflows/
│       └── bump-version.yml
├── manual.html
├── .gitignore
├── LICENSE
└── README.md
```

### O que cada pasta faz

**`rules/`** — carregada em toda sessao pelo Antigravity, sem precisar de gatilho. Define o piso de comportamento (ver secao abaixo).

**`skills/`** — o que o Antigravity usa como ponto de entrada. Cada `SKILL.md` tem `name` e `description` no frontmatter; a `description` e o que faz o agente escolher a skill a partir do que voce escreve. As skills de entrada sao curtas de proposito e delegam o metodo detalhado para os arquivos de referencia do plugin, carregados sob demanda. Isso mantem o contexto enxuto.

**`commands/`** — nao e lido pelo Antigravity (que nao tem slash-commands). Existe para manter paridade textual com o repo original, servindo de referencia ao portar mudancas entre as duas versoes. O `validate-plugin.py` valida o frontmatter desses arquivos, mas eles nao afetam o comportamento do plugin no Antigravity.

## Guardrails sempre ativos (`rules/`)

Diferente das skills, que precisam ser acionadas, as **rules valem em toda sessao**. Sao restricoes, nao sugestoes: aplicam mesmo quando voce nao pediu revisao nenhuma.

- **`rules/seguranca.md`** — proibe hardcodar segredo, por chave em `NEXT_PUBLIC_`/`EXPO_PUBLIC_`, montar query por concatenacao, usar `dangerouslySetInnerHTML` com entrada do usuario e guardar token em `localStorage`/`AsyncStorage`. Exige validar e autorizar no servidor e checar propriedade em acesso por id. Se encontrar uma brecha, o agente avisa na hora, mesmo que a tarefa em curso seja outra.
- **`rules/typescript-estrito.md`** — TypeScript estrito obrigatorio, sem `any` para calar o compilador, componentes funcionais e Hooks, Zustand so para estado global mutavel, TanStack Query para dados remotos, e o `devLevel` como teto de complexidade arquitetural.

A ideia e simples: **prevenir a brecha vale mais do que audita-la depois**. As rules seguram o piso enquanto o codigo esta sendo escrito; a skill `auditar-seguranca` faz a varredura profunda quando voce pede.

## Seguranca

Tres camadas, em ordem de atuacao:

1. **`rules/seguranca.md`** — sempre ativa, previne durante a escrita do codigo.
2. **skill `review`** — todo code review inclui uma passada de seguranca de primeira linha.
3. **skill `auditar-seguranca`** — a auditoria dedicada. Percorre segredos e variaveis de ambiente, dependencias (`npm audit`), XSS, injecao e SSRF, autenticacao e autorizacao, Server Actions e route handlers do Next, especificidades de Expo, e exposicao de dados e transporte.

Os achados saem classificados por severidade (**Critico**, **Alto**, **Medio**, **Baixo**), cada um com onde, por que e exploravel e como corrigir. Nada e editado sem a sua aprovacao. Ao encontrar um segredo **ja commitado**, o plugin avisa que apagar do arquivo nao basta: a credencial esta no historico do Git e precisa ser **revogada e rotacionada** no provedor.

O resultado e registrado no Project Hub via `POST /api/reviews`, usando `maintainability` como indice de postura de seguranca.

## Projetos feitos com o framework GSD

O [GSD](https://github.com/open-gsd/gsd-core) e um framework de engenharia de contexto e desenvolvimento orientado a especificacoes: ele conduz o agente por um ciclo de cinco fases por marco (Discuss, Plan, Execute, Verify, Ship) e deixa todo o rastro em disco, na pasta `.planning/`.

A skill `analisar-projeto-gsd` usa esse rastro como regua. Ela le a intencao documentada (`PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md` e os `XX-YY-PLAN.md` / `XX-YY-SUMMARY.md` de cada fase) e cruza com o codigo React/Next/Expo que existe de fato. Os achados vem separados em dois eixos, porque tem donos diferentes:

- **`[spec]`** — deriva: o plano prometeu e nao entregou, o summary afirma e nao fez, a convencao registrada em `codebase/CONVENTIONS.md` nao foi seguida, um requisito de v1 esta faltando.
- **`[qualidade]`** — problemas de React/TypeScript/arquitetura, independentes da spec.

Se a pasta `.planning/` nao existir, a skill avisa e oferece o `review` comum no lugar, em vez de inventar artefatos. Ela tambem **nao edita os arquivos `.planning/`** por conta propria: eles sao a memoria do GSD, e atualiza-los e responsabilidade do fluxo do proprio framework.

## Atualizar depois de um push

O Antigravity compara o campo `version` do `plugin.json` para detectar atualizacao. O repositorio tem um workflow que **bumpa o patch e sincroniza a versao** a cada push na `main` — voce commita normal, a Action publica.

```
.github/workflows/bump-version.yml   # bump + validacao + tag, no push da main
scripts/bump-version.py              # sincroniza a versao em 3 lugares
scripts/validate-plugin.py           # checagens de estrutura, roda no CI
scripts/atualizar-plugin.ps1 / .sh   # atualiza sua maquina
```

Os 3 arquivos sincronizados sao `plugin.json`, `README.md` (cabecalho e changelog) e `manual.html`.

O workflow valida antes de taguear. Para pular o bump num commit so de documentacao, o workflow ja ignora mudancas em `**/*.md`, `manual.html`, `LICENSE`, `.github/**` e `scripts/**`. Para forcar um `minor` ou `major`, use **Actions → Bump da versao do plugin → Run workflow** e escolha a parte.

### Atualizar o plugin

```shell
# Atualizar este plugin
agy plugin update plugin-react-dev-toolkit

# Atualizar todos os plugins
agy plugin update --all
```

Ou use os scripts auxiliares na maquina:

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

Esses padroes nao sao apenas documentacao: estao codificados em `rules/typescript-estrito.md` e valem em toda sessao.

## Arquitetura que evolui com o projeto

| Nivel | Quando usar | Estrutura recomendada |
| --- | --- | --- |
| Beginner | Projeto academico, portifolio ou MVP pequeno | `components`, `screens`, `repositories`, `theme`, `types` |
| Junior | Mais telas, formularios ou reaproveitamento de logica | Adiciona `hooks` e `utils` |
| Mid-Level | Multiplas funcionalidades, integracoes ou equipe | Adiciona `features`, `store` e `shared` |
| Senior | Dominio complexo e evolucao de longo prazo | Modularizacao avancada somente com justificativa |

O nivel fica em `devLevel`, definido pela skill `setup`, e funciona como **teto** de complexidade: nenhuma skill sobe acima dele sem apontar o requisito do projeto que exige a excecao.

## Project Hub local

O painel local (`http://127.0.0.1:8766`) acompanha projetos, componentes, reviews e checklist arquitetural. Implementado com Python padrao (sem `pip`, sem banco de dados).

**Para iniciar:** acione a skill `setup` ("configurar o ambiente"). Ela copia os arquivos do Project Hub para `<projectsRoot>/ProjectHub/`, sobe o servidor e abre o painel.

### Onde ficam os dados

Dois arquivos ficam ao lado de `dashboard-server.py`:

- **`projetos-data.json`** — projetos, componentes, reviews e checklists.
- **`dashboard-config.json`** — seu perfil (`devLevel`, `projectsRoot`, etc.).

Ambos estao no `.gitignore`. Nunca sao enviados para servico externo.

## Relacao com o repo original

Este repo e uma adaptacao do [plugin-react-dev-toolkit](https://github.com/victoralecrim11/plugin-react-dev-toolkit) para o Antigravity. Ele foca exclusivamente no formato nativo do Antigravity.

| | Repo original | Este repo (Antigravity) |
|---|---|---|
| Manifesto | plugin manifest separado | `plugin.json` (raiz) |
| MCP | formato legacy de configuração | `mcp_config.json` (`serverUrl`) |
| Acionamento | `commands/` (slash-commands prefixados) | `skills/` (linguagem natural) |
| Skills | 1 skill `react-dev` com `references/` | 11 skills (1 base + 10 entry points) |
| Guardrails sempre ativos | nao tem equivalente | `rules/` (2 arquivos) |
| Referencias | 9 arquivos em `references/` | os mesmos arquivos-base, incluindo `security-review.md` |
| Caminho das referencias | plugin root legacy | `./skills/...` (relativo ao plugin) |
| Bump | manifestos adicionais + docs | `plugin.json` + README + manual |
| Caminho global | plugin cache antigo | `~/.gemini/config/plugins/` |

> O `manual.html` deste repo ainda e a copia herdada do repo original e mostra os comandos no formato slash legado. Como o Antigravity usa linguagem natural, use a tabela da secao [Como usar](#como-usar-linguagem-natural) como referencia canonica de acionamento.

## O que mudou na v1.2.1

- Portadas para Antigravity as referências completas da versão original: `react-core`, `project-builder`, `react-mentor`, `gsd-analyzer` e demais arquivos-base.
- Adicionada a referência `security-review.md`, que já era citada pelas skills de review e auditoria de segurança.
- Reforçado o validador para falhar quando comandos ou skills citarem referências internas inexistentes.

## O que mudou na v1.1.1

- Atualização da documentação do README para remover a seção dedicada à skill react-dev e alinhar a estrutura do plugin com a adaptação Antigravity.
- Ajuste do script de atualização para sincronizar a versão do README e inserir automaticamente a seção de changelog a cada bump.

## Licenca

MIT — veja [LICENSE](LICENSE).
