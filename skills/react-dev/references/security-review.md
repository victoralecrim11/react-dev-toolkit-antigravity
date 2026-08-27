# Security Review

Use esta referência para auditorias de segurança em projetos React, Next.js e React Native/Expo. Ela aprofunda os guardrails sempre ativos de `rules/seguranca.md` e deve ser usada pela skill `auditar-seguranca` e pela passada de segurança do `review`.

Calibre a explicação pelo `devLevel` lido em `dashboard-config.json` (`GET /api/config`). A calibração muda a didática, não o rigor: uma falha crítica continua crítica para qualquer nível.

## Modelo mental

O objetivo é encontrar brechas exploráveis antes que o projeto seja publicado: segredo exposto, entrada sem validação, autorização só no cliente, XSS, injeção, dependência vulnerável, dado sensível retornando demais e token guardado em local inseguro.

Nunca execute exploit real, nunca envie dados do projeto para fora e nunca escreva segredo real em código, comentário, exemplo ou documentação. Use placeholders e oriente a rotação quando uma credencial já foi commitada.

## Checklist

### Segredos e variáveis de ambiente

- Procure chaves de API, tokens, senhas, URLs com credencial, service role keys e secrets de webhook em código, testes, docs, `.env*`, configs, logs e bundles.
- Trate `NEXT_PUBLIC_` e `EXPO_PUBLIC_` como públicos: qualquer valor ali pode ser lido pelo usuário final.
- Confirme que `.env` e arquivos locais sensíveis estão no `.gitignore`.
- Se um segredo já entrou no Git, remover o arquivo não basta. Oriente revogar e rotacionar no provedor.

### Dependências

- Rode checagens não destrutivas como `npm audit --omit=dev`, `pnpm audit --prod`, `yarn npm audit --environment production` ou equivalente ao gerenciador usado.
- Priorize vulnerabilidades exploráveis no runtime, build pipeline, autenticação, parsing, upload, SSRF, template rendering e bibliotecas que processam entrada externa.
- Não atualize major version automaticamente sem avaliar breaking changes.

### XSS e execução de código

- Bloqueie `dangerouslySetInnerHTML`, `innerHTML`, `eval`, `new Function` e sanitização improvisada quando a origem for usuário, URL, CMS ou API.
- Em conteúdo HTML legítimo, exija sanitização explícita com biblioteca confiável e política clara de tags/atributos.
- Verifique renderização de Markdown, previews, rich text, uploads e campos de perfil.

### Injeção, SSRF e entrada não validada

- Nunca monte SQL, filtros, comandos, URLs internas ou queries por concatenação com entrada do usuário.
- Use schema de validação no servidor para `params`, `searchParams`, body JSON, forms, headers e webhooks.
- Em chamadas para URLs fornecidas pelo usuário, valide allowlist de domínio/protocolo e bloqueie redes internas quando houver risco de SSRF.

### Autenticação e autorização

- Toda rota, route handler, Server Action, função server-side e endpoint precisa validar sessão e permissão no servidor.
- UI que esconde botão não protege recurso. A mesma regra deve existir no backend.
- Em acesso por id, cheque propriedade/tenant antes de ler, alterar ou excluir para evitar IDOR.
- Diferencie autenticação ("quem é") de autorização ("pode fazer isso neste recurso").

### Next.js

- Trate Route Handlers e Server Actions como endpoints públicos.
- Em Server Actions, valide entrada, confira sessão e autorização dentro da action.
- Não retorne objetos completos quando a tela usa poucos campos; remova PII, hashes, tokens e flags internas.
- Confira cache e revalidação para não vazar dados privados entre usuários.

### React Native / Expo

- Não guarde token em `AsyncStorage`. Use `expo-secure-store` ou mecanismo seguro equivalente.
- Revise permissões no `app.json`/`app.config.*`: peça só o necessário e explique o motivo ao usuário.
- Não exponha segredo em `EXPO_PUBLIC_`; valores públicos entram no bundle.
- Verifique deep links, WebView, uploads, storage local e logs de erro.

### Transporte, logs e exposição de dados

- Produção deve usar HTTPS e cookies `httpOnly`, `Secure` e `SameSite` quando aplicável.
- Erros enviados ao cliente não devem conter stack trace, SQL, segredo, token, PII ou caminhos internos sensíveis.
- Logs devem mascarar credenciais e dados pessoais.
- APIs devem devolver somente os campos necessários.

## Classificação

- **Crítico:** segredo real exposto, auth bypass, acesso indevido a dados de outro usuário/tenant, execução remota, SQL injection explorável, XSS armazenado explorável, token sensível em storage inseguro.
- **Alto:** validação/autorizações frágeis em endpoint sensível, dependência vulnerável no runtime com caminho plausível, exposição de PII, webhook sem verificação.
- **Médio:** falha defensiva que exige pré-condições, logs excessivos, cache arriscado, permissões amplas, sanitização incompleta em área menos sensível.
- **Baixo:** hardening, documentação, mensagens de erro, headers, pequenas melhorias preventivas.

Para cada achado, informe: severidade, local, por que é explorável, impacto provável e correção recomendada.

## Correção

Apresente o relatório antes de editar e peça aprovação para aplicar correções. Ao corrigir, preserve comportamento, adicione validação/checagem no servidor, use placeholders para segredos e ajuste testes quando houver cobertura existente.
