# Regra: TypeScript estrito e React moderno

Restricoes sempre ativas ao gerar ou alterar codigo React, Next.js e Expo neste plugin.

## TypeScript

- **TypeScript estrito e obrigatorio e nao e configuravel.** Tipar props, retornos publicos, DTOs e estados.
- **Nao use `any` para silenciar o compilador.** Se o tipo for realmente desconhecido, use `unknown` e estreite com checagem. Nao adicione `@ts-ignore` sem um comentario explicando por que e inevitavel.
- Nao desative regra de lint para fazer o codigo passar; corrija a causa.

## React

- **Componentes funcionais e Hooks.** Nunca introduza class components nem APIs legadas.
- Estado local fica no componente. Context serve para dependencias globais estaveis. **Zustand** somente para estado global compartilhado e mutavel. **TanStack Query** para estado remoto (cache, loading, erro, sincronizacao).
- Nao use Zustand para dados remotos, nem Redux sem justificativa concreta.
- Telas coordenam a UI, hooks encapsulam logica reutilizavel, componentes nao carregam regra de negocio. Acesso a API por clients ou repositories.

## Proporcionalidade

- **O `devLevel` do perfil e o teto de complexidade arquitetural.** Ele vive em `dashboard-config.json` e e definido pela skill `setup`. Leia em vez de perguntar; sem perfil, aplique o fallback de `./skills/react-dev/references/dashboard-projetos.md`.
- Para propor arquitetura acima do nivel registrado, aponte explicitamente qual requisito do projeto exige a excecao.
- Entregue um MVP funcional antes de propor abstracao avancada. Nao antecipe complexidade que o projeto ainda nao precisa.

## Sempre explique

Toda recomendacao de biblioteca, padrao ou estrutura vem com motivo, alternativa, trade-off e quando nao usar. O plugin e didatico: a decisao precisa ficar compreensivel, nao apenas aplicada.
