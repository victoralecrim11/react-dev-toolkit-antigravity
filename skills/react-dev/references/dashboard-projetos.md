# Dashboard de Projetos

Use quando o usuário disser dashboard, projetos, componentes reutilizáveis, reviews, métricas, dívida técnica ou checklist arquitetural. O painel é local, sem banco externo, e usa dois arquivos: `projetos-data.json` para os registros e `dashboard-config.json` para o perfil e as preferências do desenvolvedor.

## Inicialização

Copie `references/dashboard-server.py`, `dashboard-template.html` e o inicializador adequado para a pasta desejada. Execute o inicializador; o servidor Python padrão abre `http://127.0.0.1:8766`. Não requer pip.

## Perfil do desenvolvedor — fonte única da verdade

O perfil fica em `dashboard-config.json`, lido por `GET /api/config` e gravado por `POST /api/config`. **Só o `/setup` escreve**; todos os outros comandos apenas **leem**. O `/setup` pode rodar quantas vezes o usuário quiser — é assim que o perfil se altera.

- `devLevel`: Beginner, Junior, Mid-Level ou Senior. Define o teto de complexidade arquitetural e a profundidade das explicações.
- `projectsRoot`: pasta-base dos projetos.
- `defaultPlatform`: `react`, `next` ou `expo`.
- `defaultGoal`: `academico`, `mvp` ou `producao`.
- `scanRoot`: raiz usada por `GET /api/scan`; manter igual a `projectsRoot`.
- `setupCompletedAt`: marca que o onboarding já rodou.

Regra: nenhum comando deve perguntar o nível de calibração se `devLevel` já estiver preenchido.

### Fallback quando o perfil não existe

Comportamento único, válido para todos os comandos e skills. Se `setupCompletedAt` ou `devLevel` estiverem vazios:

1. Avise em uma linha que `/setup` ainda não rodou.
2. Assuma `Junior` como nível provisório e siga com o trabalho pedido.
3. Sugira `/setup` ao final. Não conduza o onboarding por conta própria e não grave `dashboard-config.json` — isso é exclusivo do `/setup`.

Exceção: o `/criar-projeto` precisa de nome, pasta e plataforma para funcionar, então pode coletar apenas esses dados do projeto. O nível continua vindo do fallback acima, nunca de uma pergunta.

## Dados que comandos devem registrar

Use **exatamente** estas chaves. O painel lê os campos por nome; descrever o campo em português na chave (`nome`, `caminho`, `nivel`) faz o registro aparecer incompleto na tela.

### `POST /api/projects`

```json
{
  "name": "gerenciador-biblioteca",
  "path": "C:/Users/voce/Projetos/gerenciador-biblioteca",
  "platform": "React",
  "status": "mvp",
  "reactVersion": "19",
  "stack": "React 19 + TypeScript + Vite + TanStack Query",
  "level": "Junior",
  "notes": "",
  "repoUrl": "usuario/repo"
}
```

`name` e `path` são **obrigatórios**. Sem `path` o botão "Detectar componentes" não funciona. Use o caminho absoluto real da pasta, não um placeholder. `level` aceita Beginner, Junior, Mid-Level ou Senior. `repoUrl` é `usuario/repo`, sem `https://github.com/`.

### `POST /api/components`

```json
{ "name": "Button", "project": "gerenciador-biblioteca", "category": "ui", "path": "src/components/Button.tsx", "description": "botão base com variantes" }
```

### `POST /api/reviews`

```json
{ "project": "gerenciador-biblioteca", "maintainability": 82, "summary": "resumo curto", "debts": ["sem testes no formulário", "fetch direto no componente"] }
```

`debts` aceita lista ou string separada por vírgula.

### `POST /api/checklists`

```json
{ "projectId": "<id do projeto>", "items": { "0": true, "3": true } }
```

## Regras de escrita

- Para **atualizar** um registro, envie o `id` e apenas os campos que mudaram: o servidor faz merge e não zera o resto.
- Para **substituir** um registro por inteiro (campo vazio deve ficar vazio), inclua `"_replace": true`. O formulário do painel usa isso; comandos normalmente não devem.
- A resposta traz `warnings` listando campos vazios. **Leia esse array** e complete o registro em vez de deixar lacunas.
- O servidor aceita sinônimos (`nome`, `caminho`, `nivel`, `versaoReact`...) como rede de segurança, mas isso é tolerância a erro, não a interface. Use as chaves canônicas.
- Se `path` faltar, o servidor tenta deduzir `<projectsRoot>/<name>` e só aceita se a pasta existir. Não confie nisso: envie o caminho.
- Ao **criar** um projeto, `status`, `platform` e `level` vazios são herdados do perfil (`defaultGoal`, `defaultPlatform`, `devLevel`) e o aviso `Herdado do perfil: ...` aparece em `warnings`. Isso é rede de segurança: continue enviando os campos, porque só você sabe a plataforma real deste projeto. Em **atualização** não há herança — campo vazio permanece vazio.

Leitura por `GET /api/data` e `GET /api/config`. O dashboard também permite editar e excluir visualmente. Nunca envie os dados para serviços externos.
