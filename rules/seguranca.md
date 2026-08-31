# Regra: seguranca por padrao

Restricoes sempre ativas ao escrever ou alterar codigo de projetos React, Next.js e Expo. Sao limites, nao sugestoes: valem mesmo quando o usuario nao pediu uma auditoria. Para a auditoria completa e a classificacao por severidade, use a skill `auditar-seguranca`.

## Nunca faca

- **Nunca hardcode segredo.** Chave de API, token, senha, string de conexao ou credencial nao entram no codigo. Use variavel de ambiente e `.env`, e garanta que o `.env` esta no `.gitignore`.
- **Nunca coloque segredo em variavel publica.** Tudo com prefixo `NEXT_PUBLIC_` ou `EXPO_PUBLIC_` vai para o bundle e e legivel por qualquer usuario. Somente valores realmente publicos podem usar esses prefixos. Service role keys e secrets de webhook ficam sempre no servidor.
- **Nunca escreva um segredo real** em codigo, exemplo, comentario ou documentacao. Use placeholder.
- **Nunca monte query por concatenacao de string** com entrada do usuario. Use query parametrizada ou o ORM com bind.
- **Nunca use `dangerouslySetInnerHTML`, `innerHTML` ou `eval`** com conteudo que vem do usuario, da URL ou de uma API sem sanitizar antes.
- **Nunca guarde token de sessao em `localStorage` ou `AsyncStorage`.** Na web, cookie `httpOnly` + `Secure` + `SameSite`. No Expo, `expo-secure-store`.
- **Nunca deixe stack trace, PII ou credencial em log** ou em mensagem de erro que chega ao cliente em producao.

## Sempre faca

- **Valide e autorize no servidor.** Validacao no cliente e UX, nao seguranca. Toda Server Action (`'use server'`), route handler e endpoint e publico: valide a entrada com schema e confira a sessao e a permissao ali dentro.
- **Checagem de propriedade em acesso por id.** Antes de devolver ou alterar um recurso, confirme que ele pertence ao usuario logado (evita IDOR).
- **Devolva somente os campos necessarios.** Nao retorne o objeto inteiro quando a tela usa dois campos; hash de senha e campos internos nunca saem da API.
- **Esconder o botao nao protege o endpoint.** Se a UI oculta uma acao por permissao, a mesma regra tem que existir no servidor.

## Ao encontrar uma brecha

Avise o usuario na hora, com severidade e o motivo, mesmo que a tarefa em curso seja outra. Nao corrija em silencio e nao siga adiante fingindo que nao viu.

Se o segredo exposto **ja foi commitado**, remover do arquivo nao resolve: a credencial esta no historico do Git. Oriente a **revogar e rotacionar** a chave no provedor.

Nunca execute um exploit de verdade para "provar" a falha, e nunca envie dados do projeto para fora.