---
name: react-dev
description: Base de conhecimento para projetos React, Next.js e React Native/Expo. Use quando o assunto envolver React, TypeScript, Hooks, Zustand, TanStack Query, App Router, Server Components, Server Actions, SSR, SSG, Expo, Expo Router, Hermes, Reanimated, discovery de MVP, scaffolding, code review, arquitetura de pastas, deploy, build de producao, publicar, hospedar, Vercel, Netlify, Cloudflare Pages, GitHub Pages, Expo EAS, GitHub Actions, CI/CD, variaveis de ambiente, analisar projeto feito com o framework GSD (pasta .planning, PROJECT.md, ROADMAP.md, STATE.md, phases), auditoria de seguranca (segredos vazados, dependencias vulneraveis, XSS, injecao, autenticacao, exposicao de dados), ou o Project Hub local (projetos, componentes, reviews, metricas, divida tecnica, checklist).
user-invocable: false
---

# React Dev Hub — base de conhecimento

Carregue o arquivo de referência que corresponde ao assunto. Cada um é
independente: leia só o que a tarefa exige, não todos.

| Assunto | Arquivo |
| :-- | :-- |
| React, TypeScript, Hooks, estado, dados remotos | `references/react-core.md` |
| Next.js: App Router, Server Components, Server Actions, SSR/SSG | `references/nextjs.md` |
| React Native e Expo: Expo Router, Hermes, Reanimated, mobile | `references/react-native.md` |
| Discovery, definição de MVP, implementação incremental, review | `references/project-builder.md` |
| Segurança: auditoria de brechas, segredos, XSS, injeção, auth | `references/security-review.md` |
| Deploy, CI/CD, provedores, build de produção, segredos | `references/deploy-advisor.md` |
| GSD: analisar projeto feito com o framework (`.planning/`, spec vs código) | `references/gsd-analyzer.md` |
| Project Hub: schema da API, perfil do dev, registros | `references/dashboard-projetos.md` |

Os caminhos são relativos a `./skills/react-dev/`. No Antigravity, o plugin
fica em `~/.gemini/antigravity-cli/plugins/plugin-react-dev-toolkit/`. No
Claude Code, o plugin é cacheado em `~/.claude/plugins/cache/...`. Em ambos,
resolva sempre por caminhos relativos ao diretorio do plugin, nunca por
caminhos do projeto do usuario.

## Regras que valem para tudo

- **`react-core.md` é a base.** Para Next.js ou Expo, leia `react-core.md`
  primeiro e depois a referência da plataforma.
- **TypeScript estrito é obrigatório** e não é configurável.
- **O nível do desenvolvedor é o teto de complexidade.** Ele vive em `devLevel`
  no `dashboard-config.json` e é definido pela skill `setup`. Nenhuma skill pergunta
  o nível; se o perfil não existir, aplique o fallback descrito em
  `references/dashboard-projetos.md`.
- **Cada recomendação vem com motivo, alternativas e quando não usar.**
- **Os guardrails de base já estão sempre ativos** em `rules/seguranca.md` e
  `rules/typescript-estrito.md`, carregados pelo Antigravity em toda sessão.
  Eles definem o piso (nunca hardcodar segredo, validar no servidor, TS estrito);
  as referências abaixo aprofundam. Não os contradiga.

## Arquivos de apoio do Project Hub

O servidor local e o template ficam em `references/project-hub/`:
`dashboard-server.py`, `dashboard-template.html`, `iniciar-dashboard.bat` e
`iniciar-dashboard.command`. Copie-os para `<projectsRoot>/ProjectHub/`; o servidor
usa so a biblioteca padrao do Python, sem `pip`.
