---
name: ui-ux
description: "Motor especializado de UI/UX, Design System Architect, composição visual, tipografia e acessibilidade para ecossistemas React, Next.js e React Native."
---

# UI/UX Pro Max Engine

Esta skill atua como autoridade em design de interfaces, fornecendo direcionamento visual, paletas de cores, tipografia, guidelines de UX e acessibilidade antes da implementação técnica. Adaptação nativa do `ui-ux-pro-max-skill` para o Antigravity.

## Como consultar (Datasets)

Os datasets ficam em `data/*.csv`. Para qualquer consulta pontual (buscar um estilo, uma paleta, um par de fontes, uma regra de UX), rode o script de busca local em vez de ler o CSV inteiro — ele ranqueia por relevância e economiza contexto:

```bash
python skills/ui-ux/scripts/search-uiux.py "<consulta>" --domain <dominio>
python skills/ui-ux/scripts/search-uiux.py --list-domains
```

Domínios disponíveis: `style` (styles.csv), `color` (colors.csv), `product` (products.csv), `typography` (typography.csv), `ux` (ux-guidelines.csv), `reasoning` (ui-reasoning.csv).

Sem `--domain`, o script busca em todos e escolhe o de maior relevância automaticamente.

Use `--full` quando precisar do checklist/snippet sem truncamento.

Use `--json` para consumo programático.

Só leia um CSV inteiro via `data/` diretamente quando precisar varrer o dataset completo. Para o caso comum de "qual estilo/paleta/fonte serve aqui", prefira sempre o script.

## Fluxo de Operação Obrigatório (Reasoning & Handoff)

A responsabilidade da skill `ui-ux` é separar dois artefatos distintos:

- `DESIGN.md` na raiz do projeto = direção criativa, objetivo visual, persona, princípios, referências e decisões conceituais.
- `.design/design-system.md` = contrato técnico de tokens e implementação (cores, tipografia, spacing, radius, breakpoints, variáveis CSS, mapeamento Tailwind/React Native).

Se `DESIGN.md` não existir, o sistema pode seguir com o fluxo atual de reasoning e fallback. Se `.design/design-system.md` não existir, a skill continua usando os fallbacks atuais do plugin (CSV + referências) sem quebrar compatibilidade.

Para garantir que o time técnico (`react-dev` e `criar-projeto`) implemente a interface correta sem alucinações, siga o funil de design abaixo:

1. **Descoberta do Produto & Estilo:** Identifique o nicho e a linguagem visual.

   `search-uiux.py "<nicho>" --domain product`

   `search-uiux.py "<termo>" --domain style` (Minimalista, Brutalista, Clean SaaS, etc.)

2. **Harmonia Cromática e Tipográfica:** Extraia as paletas semânticas e pares de fonte.

   `search-uiux.py "<termo>" --domain color`

   `search-uiux.py "<termo>" --domain typography`

3. **Reasoning Engine (Motor de Raciocínio):**

   Consulte o domínio lógico: `search-uiux.py "<termo>" --domain reasoning` para encontrar o padrão de interface, os anti-padrões e os motivos.

   Consulte `references/reasoning-rules.md` para as regras de cruzamento de dados (ex: adequar o contraste WCAG AA/AAA ao estilo e aplicar as diretrizes de `ux`, `accessibility.md` e `responsive-design.md`).

4. **Handoff Técnico (Obrigatório quando houver implementação real):**

   Consulte `references/design-routing.md`.

   Primeiro, registre a direção criativa em `DESIGN.md`.
   Em seguida, quando a interface exigir implementação técnica real, grave fisicamente o contrato técnico em `.design/design-system.md`.

   O seu trabalho finaliza ao salvar estes documentos. Transmita o contexto para o `react-dev` apenas após a criação dos artefatos, para que ele saiba exatamente como estruturar o Tailwind CSS, shadcn/ui, styled-components ou StyleSheet sem duplicar a fonte de verdade.
