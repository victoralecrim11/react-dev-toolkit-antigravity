# GSD Analyzer

Use quando o usuário quiser analisar um projeto React/Next/Expo que **já foi construído usando o framework GSD** (Get Stuff Done) — o comando `/analisar-projeto-gsd`. O objetivo é cruzar a intenção documentada nos artefatos do GSD com o código que realmente existe, apontar divergências e, quando o usuário aprovar, corrigir o que fugiu da spec. Não é uma ferramenta genérica de review: o diferencial é ler o "porquê" registrado pelo GSD e comparar com o "como" que virou código.

Calibre tudo pelo `devLevel` lido em `dashboard-config.json` (`GET /api/config`). O nível é definido só pelo `/setup`; **não pergunte**. Se o perfil não existir, aplique o fallback da `./skills/react-dev/references/dashboard-projetos.md` (avise em uma linha, assuma `Junior` provisório, siga o trabalho e sugira `/setup` ao final).

## O que é o GSD (contexto rápido)

GSD é um framework de engenharia de contexto e desenvolvimento orientado a especificações. Ele conduz o agente por um ciclo de cinco fases por marco (milestone): **Discuss** (decisões antes de planejar), **Plan** (pesquisa, decomposição e verificação de que o plano cabe numa janela limpa), **Execute** (execução em ondas paralelas, cada executor com contexto limpo de ~200k tokens), **Verify** (percorrer o que foi construído, diagnosticar e corrigir) e **Ship** (PR, arquivar a fase, repetir). Todo esse trabalho deixa rastros em disco — é isso que este comando lê.

## Detecção — como saber que é um projeto GSD

O marcador canônico é a pasta **`.planning/`** na raiz do projeto. Se ela não existir, o projeto não foi construído com GSD: avise o usuário em uma linha, ofereça rodar o `/review` comum no lugar e pare — não invente artefatos.

Confirme com pelo menos um destes presentes dentro de `.planning/`: `PROJECT.md`, `ROADMAP.md`, `STATE.md` ou a pasta `phases/`.

## Mapa dos artefatos do GSD

Todos ficam sob `.planning/` na raiz do projeto. Leia sob demanda — não precisa abrir todos; priorize os que existem e que respondem à pergunta em mãos.

Arquivos de topo (a espinha dorsal):

- `PROJECT.md` — visão, restrições, decisões e regras de evolução do produto. **É o "porquê".**
- `REQUIREMENTS.md` — requisitos escopados em v1 / v2 / fora de escopo. Fonte para checar o que devia estar pronto agora.
- `ROADMAP.md` — quebra em fases com status de cada uma. Diz onde o projeto deveria estar.
- `STATE.md` — memória viva: posição atual, decisões, bloqueios e métricas.
- `MILESTONES.md` — arquivo dos marcos já concluídos.
- `config.json` — configuração do workflow GSD.
- `continue-here.md` — handoff de contexto para retomar a sessão.

Subpastas:

- `research/` — pesquisa de domínio: `SUMMARY.md`, `STACK.md`, `FEATURES.md`, `ARCHITECTURE.md`, `PITFALLS.md`.
- `codebase/` — mapa do código existente (brownfield): `STACK.md`, `ARCHITECTURE.md`, `CONVENTIONS.md`, `CONCERNS.md`, `STRUCTURE.md`, `TESTING.md`, `INTEGRATIONS.md`. **`CONVENTIONS.md` e `CONCERNS.md` são ouro para o review** — dizem o padrão que o próprio projeto adotou e os pontos que ele já sabe frágeis.
- `phases/XX-nome-da-fase/` — uma pasta por fase, com prefixo numérico (`XX`) para ordenar. Planos usam numeração decimal (`XX-YY`). Conteúdo típico:
  - `XX-CONTEXT.md` — preferências capturadas na fase Discuss.
  - `XX-RESEARCH.md` — pesquisa da fase.
  - `XX-YY-PLAN.md` — os planos de execução (o que a fase Execute deveria produzir).
  - `XX-YY-SUMMARY.md` — o que a execução de fato entregou.
  - `XX-VERIFICATION.md` — verificação pós-execução.
  - `XX-VALIDATION.md` — mapeamento de cobertura de testes.
  - `XX-UI-SPEC.md` / `XX-UI-REVIEW.md` — contrato de UI e auditoria visual.
  - `XX-UAT.md` — testes de aceitação.
- `quick/`, `threads/`, `seeds/`, `debug/`, `todos/`, `ui-reviews/` — tarefas rápidas, threads de contexto, ideias futuras, sessões de debug, TODOs e screenshots. Leia só se forem relevantes à pergunta.

> Formatos evoluem. Se um arquivo esperado não existir, siga com os que existirem em vez de travar — a presença de `.planning/` já basta para tratar como projeto GSD.

## Metodologia de análise (o ciclo espelhando o GSD)

A ideia é seguir a mesma lógica das cinco fases do GSD, mas de trás para frente: em vez de construir, você audita o que foi construído contra o que foi especificado.

1. **Ler a intenção (Discuss + Plan).** Abra `PROJECT.md`, `REQUIREMENTS.md` e `ROADMAP.md`. Extraia: qual é o produto, o que é v1, qual fase o roadmap diz estar concluída, quais decisões de arquitetura foram registradas. Se houver `codebase/CONVENTIONS.md`, esse é o padrão oficial do projeto.
2. **Ler o que foi entregue (Execute).** Para cada fase marcada como concluída no `ROADMAP.md`/`STATE.md`, leia o `XX-YY-PLAN.md` e o `XX-YY-SUMMARY.md` correspondentes. O plano é o contrato; o summary é o que o executor afirma ter feito.
3. **Cruzar com o código real.** Abra os arquivos React/Next/Expo que os planos dizem ter criado. Aplique `./skills/react-dev/references/react-core.md` e a referência da plataforma (`nextjs.md` ou `react-native.md`) como critério técnico. Pergunte-se, arquivo por arquivo:
   - O que o `PLAN.md` prometeu existe mesmo? O `SUMMARY.md` diz "feito" para algo que não está no código? (deriva spec ↔ código)
   - O código respeita as `CONVENTIONS.md` e as decisões do `PROJECT.md`, ou divergiu sem registro?
   - Requisitos de v1 do `REQUIREMENTS.md` estão implementados? Algo de "fora de escopo" vazou para dentro?
   - Os `CONCERNS.md` conhecidos foram tratados ou continuam abertos?
4. **Verificar qualidade (Verify).** Sobre o código que existe, faça o review técnico normal do plugin: tipagem estrita, tratamento de erro, loading/empty states, acessibilidade, segurança, responsabilidades, re-renderizações, cache, bundle, testes e dívida técnica. Se houver `XX-VALIDATION.md`/`XX-UAT.md`, confira se a cobertura declarada bate com os testes que existem.
5. **Fechar (Ship).** Consolide num relatório e registre no Project Hub. Se o usuário aprovar correções, aplique-as (ver política abaixo) antes de encerrar.

## Classificação dos achados

Separe sempre em dois eixos, porque eles têm donos diferentes:

- **Deriva de spec** — o código não corresponde ao que o GSD documentou (plano promete e não entregou; summary afirma e não fez; convenção registrada e não seguida; requisito v1 faltando). Aqui a régua é o próprio `.planning/`.
- **Qualidade técnica** — problemas de React/TS/arquitetura independentemente da spec. Aqui a régua é o `react-core.md` e as referências de plataforma.

Ordene por prioridade (bloqueia v1 > risco de segurança/dados > dívida que trava evolução > polimento). Para cada achado: **o que**, **onde** (arquivo:linha ou artefato), **por que importa** e **como corrigir**. Calibre a profundidade da explicação ao `devLevel` — Beginner recebe o passo a passo do porquê; Senior recebe o diagnóstico direto e o trade-off.

## Política de correção

O escopo inclui corrigir o que divergir, mas com disciplina:

- **Nunca corrija sem mostrar antes.** Apresente o relatório, marque o que você recomenda corrigir e pergunte o que o usuário quer aplicar. Não saia editando em lote.
- **Preserve comportamento.** Correções seguras e graduais, como manda o `/review`. Não refatore por preferência pessoal nem suba a arquitetura acima do `devLevel` sem apontar o requisito que exige a exceção.
- **Priorize a deriva de spec.** Se o código diverge do `PROJECT.md`/`CONVENTIONS.md`, o padrão é alinhar o código à spec — a menos que a spec esteja obviamente errada, caso em que você aponta isso e deixa a decisão com o usuário (o GSD trata a spec como fonte da verdade).
- **Não edite os artefatos `.planning/` por conta própria.** Eles são a memória do GSD. Se o código mudou e a spec ficou desatualizada, aponte a divergência e sugira que o usuário rode o próprio fluxo do GSD para atualizar; só toque nesses arquivos se ele pedir explicitamente.
- Depois de aplicar qualquer correção, releia o trecho alterado e confirme que o build/tsc não quebrou antes de declarar concluído.

## Registro no Project Hub

Feche registrando no dashboard, com as chaves exatas da `./skills/react-dev/references/dashboard-projetos.md`. Confira o array `warnings` da resposta e complete o que faltar.

1. **Projeto** — se o projeto ainda não estiver no Hub, registre via `POST /api/projects` com `name`, `path` (caminho absoluto real da pasta), `platform`, `status`, `stack`, `level` (o `devLevel` do perfil) e, no `notes`, deixe claro que é um projeto GSD e qual fase o roadmap indica (ex.: `"GSD · fase 03 de 05 concluída"`). Se já existir, atualize enviando só `id` + campos mudados.
2. **Review** — registre a análise via `POST /api/reviews`:
   - `project`: nome do projeto.
   - `maintainability`: nota 0–100 ponderando qualidade técnica **e** aderência à spec GSD.
   - `summary`: resumo curto incluindo o estado do ciclo GSD (ex.: `"Fases 1-3 entregues; login (req. v1) ausente apesar do SUMMARY marcar feito."`).
   - `debts`: lista dos achados priorizados; prefixe cada item com `[spec]` ou `[qualidade]` para o usuário saber a régua.

Se o Project Hub estiver fora do ar, entregue o relatório mesmo assim e diga ao usuário que o registro no dashboard ficou pendente até subir o painel (`/dashboard`).

## Formato de saída

1. **Cabeçalho** — nome do produto (do `PROJECT.md`), plataforma detectada e onde o ciclo GSD está (fases concluídas / total, do `ROADMAP.md`/`STATE.md`).
2. **Deriva de spec** — o que o `.planning/` promete e o código não cumpre (ou o contrário), priorizado.
3. **Qualidade técnica** — achados de React/TS/arquitetura, priorizados.
4. **Nota de manutenibilidade** e o que mais pesou nela.
5. **Correções recomendadas** — lista objetiva do que dá para corrigir com segurança agora; pergunte o que aplicar.
6. **Próximos passos** — incluindo qual seria a próxima fase do GSD e um lembrete de que atualizar os artefatos `.planning/` é responsabilidade do fluxo GSD, não deste comando.

