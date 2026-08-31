---
name: criar-componente
description: Cria componentes, hooks e testes TypeScript reutilizaveis com registro no dashboard.
user-invocable: false
---


# /criar-componente

Cria componentes React, Next.js ou React Native com TypeScript estrito, arquitetura limpa, documentação de props e integração direta com o Design System.

## Fluxo de Execução

### 1. Consulta ao Design System & UX (`skills/ui-ux/`)
Antes de escrever o código, consulte as diretrizes de interface:
* **Estilo & Tokens:** Consultar `skills/ui-ux/data/styles.csv` e `colors.csv` para paleta, bordas, sombras e espaçamentos.
* **Tipografia:** Alinhar hierarquia visual com `skills/ui-ux/data/typography.csv`.
* **Acessibilidade & Usabilidade:** Seguir regras de `skills/ui-ux/references/accessibility.md` (labels, roles, estados e contraste mínimo WCAG AA) e `skills/ui-ux/data/ux-guidelines.csv`.

### 2. Definição Técnica & Props
* Determinar se o componente pertence a **React Web / Next.js** ou **React Native**.
* Definir props tipadas explicitamente via `interface` TypeScript (sem `any`).
* Prever estados visuais: *Default*, *Hover/Active*, *Focus-Visible*, *Loading*, *Disabled* e *Error*.
* Definir se o componente deve ser atômico (`src/components/ui`) ou ligado a domínio (`src/features/.../components`).

### 3. Implementação
* Código limpo e modular.
* Uso de Tailwind CSS / CSS Modules (Web) ou StyleSheet / Styled-Components (Mobile).
* Tratamento acessível de eventos e navegação por teclado / leitor de tela.

### 4. Saída Esperada
Entregar a resposta no seguinte formato:
1. **Objetivo:** Papel do componente na aplicação.
2. **Tokens de UI/UX Adotados:** Paleta, estilo e regras de acessibilidade aplicadas.
3. **Código TSX:** Arquivo completo e tipado.
4. **Exemplo de Uso:** Demonstração de consumo com props preenchidas.