---
description: Analisa a stack do projeto, valida o build e publica no provedor ideal (Vercel, Netlify, Cloudflare Pages, GitHub Pages, Expo EAS) ou configura CI/CD com GitHub Actions.
disable-model-invocation: true
---
# Deploy da Aplicação

Inicia o assistente de infraestrutura para preparar e publicar o projeto atual.

## Instruções de Execução para o Assistente

1. Assuma imediatamente o papel e as regras definidas na referência **Deploy Advisor** (`./skills/react-dev/references/deploy-advisor.md`).
2. Não peça informações iniciais ao usuário. Inicie o fluxo obrigatoriamente pelo **Passo 1 (ANALISAR)**, inspecionando os arquivos do projeto em modo silencioso.
3. Siga o fluxo contínuo até o **Passo 4 (CONFIRMAR)**.
4. Pare e apresente ao usuário o relatório da análise, recomendando o melhor provedor com base na stack detectada.
5. Aguarde a resposta do usuário (1 a 6) para então prosseguir com os passos de **DEPLOY** e **INFORMAR RESULTADO**.
