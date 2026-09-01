---
name: gerar-midia
description: Gera imagem ou video de marketing usando o MCP da Higgsfield.
user-invocable: false
---
# /gerar-midia

Cria prompts especializados e orquestra a geração de mídia e assets visuais integrados à identidade do projeto.

## Fluxo de Execução

### 1. Extração de Contexto do Design System
Antes de formular o prompt de geração, consulte a identidade visual do projeto. Se existir `.design/design-system.md` na raiz do projeto, **use-o como fonte primária** de paleta, estética e tipografia. Caso contrário, consulte diretamente:
* **Paleta Semântica:** Extrair códigos hexadecimais e contrastes de `skills/ui-ux/data/colors.csv`.
* **Estética & Atmosfera:** Mapear linguagem visual de `skills/ui-ux/data/styles.csv` (ex: minimalista, iluminação suave, glassmorphism, tecnologia limpa).
* **Composição:** Definir proporção e hierarquia visual de acordo com o asset de destino.

### 2. Definição do Tipo de Asset
* **Hero Image:** Foco em impacto visual, legibilidade de texto sobreposto e proporção 16:9.
* **Open Graph (OG Image):** Proporção 1200x630, foco em clareza da proposta de valor e marca.
* **App Icon / Splash Screen:** Minimalismo, contraste alto e foco no elemento central (1:1).
* **Vídeo Curto / Demonstração:** Teaser de interação de interface ou transição suave.

### 3. Orquestração MCP
* Formular o prompt detalhado em inglês (otimizado para motores de difusão de imagem/vídeo), incorporando cores e referências estilísticas.
* Invocar as ferramentas disponíveis no MCP do **Higgsfield** configurado em `mcp_config.json`.

### 4. Saída
* Apresentar o prompt técnico utilizado.
* Fornecer o link/resultado do asset gerado pelo MCP.
* Código TSX com exemplo de integração do asset no Next.js (`<Image>` / metadata) ou React Native.