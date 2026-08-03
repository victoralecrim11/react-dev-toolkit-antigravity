---
description: Gera imagem hero, preview social (OG image) ou vídeo curto de demonstração para o projeto atual usando o MCP da Higgsfield.
disable-model-invocation: true
---
# /gerar-midia

Usa as tools do servidor MCP `plugin:plugin-react-dev-toolkit:higgsfield` para gerar material visual de marketing para o projeto React/Next/Expo atual — hero image, preview de compartilhamento social (OG image) ou um vídeo curto de demonstração. Não é uma ferramenta de geração genérica: sempre amarre o resultado ao contexto real do projeto (nome, paleta, público) em vez de gerar algo solto.

## Antes de gerar

Confirme com o usuário, numa única pergunta objetiva se algo estiver faltando:

1. **O que gerar**: imagem hero, OG image (1200x630) ou vídeo curto (até 15s).
2. **Contexto**: nome do projeto, uma frase do que ele faz, paleta/cor de destaque (se houver `dashboard-config.json` ou `PROJECT.md` no projeto, leia de lá em vez de perguntar).
3. **Estilo**: fotorrealista, ilustração, abstrato/gradiente — sem estilo definido, use algo neutro e profissional coerente com o produto.

Vídeo consome bem mais créditos Higgsfield que imagem. Antes de chamar `generate_video`, confirme explicitamente que o usuário quer gastar créditos nisso — não assuma.

## Geração

1. Monte o prompt em inglês (os modelos da Higgsfield respondem melhor em inglês, mesmo com o resto da conversa em português), descrevendo cena, paleta e composição — nunca só o nome do produto.
2. Para imagem: chame `generate_image` com `prompt`, `model` (deixe o padrão do servidor escolher salvo se o usuário pedir um modelo específico) e o `aspect_ratio` adequado (`1:1` hero quadrado, `1.91:1` para OG image, `9:16` para stories).
3. Para vídeo: chame `generate_video`. A geração é assíncrona — depois da chamada, use `get_generation_status` para acompanhar até `completed` ou `failed`. Não fique repetindo a chamada em loop apertado; espere um intervalo razoável entre checagens.
4. Se o resultado vier com `nsfw` ou falhar, reformule o prompt uma vez com termos mais neutros antes de perguntar ao usuário o que fazer.

## Entrega

- Mostre a URL do asset gerado para o usuário revisar antes de qualquer coisa.
- Só baixe o arquivo para dentro do projeto (`public/`, `src/assets/` ou equivalente pela stack detectada) se o usuário aprovar o resultado. Não grave nada no repositório sem essa aprovação — é um asset gerado, gasta crédito, e o usuário pode preferir gerar de novo.
- Depois de salvo, informe o caminho relativo do arquivo e sugira onde usá-lo (ex: `og:image` no `<head>`, hero do README, banner da landing) sem editar esses arquivos automaticamente — isso é decisão do usuário.

## Limites

- Não é acionado automaticamente por outras skills do plugin (`/criar-projeto`, `/deploy` etc.) — só roda quando o usuário chama `/gerar-midia` diretamente.
- Se o MCP não estiver conectado ou a autenticação OAuth expirou, informe isso claramente e pare; não tente contornar via scraping ou chamada HTTP direta ao domínio da Higgsfield.
- Personagens recorrentes (`create_character`) e histórico (`list_characters`) só entram em jogo se o usuário pedir consistência visual entre múltiplas gerações — não use por padrão.
