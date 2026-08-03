---
description: Configura o ambiente de desenvolvimento e o perfil do dev; rode de novo a qualquer momento para alterar o perfil.
---
# /setup

Configura o ambiente de trabalho e entrega as ferramentas locais. É por máquina, não por projeto — a criação de projetos é responsabilidade do `/criar-projeto`.

O comando é **idempotente**: rodar de novo é seguro e é a forma correta de trocar de nível, de pasta-base ou de stack padrão. Não é um comando de uso único.

## Etapa 0 — Detectar o modo

Antes de perguntar qualquer coisa, procure um `dashboard-config.json` existente: na pasta-base conhecida ou, se o Project Hub já estiver no ar, por `GET /api/config`.

**Modo instalação** — não existe config, ou `setupCompletedAt` está vazio. Siga as Etapas 1 → 4 na ordem.

**Modo reconfiguração** — o perfil já existe. Então:

1. Mostre o perfil atual em uma lista curta (`devLevel`, `projectsRoot`, `defaultPlatform`, `defaultGoal`).
2. Pergunte **o que o usuário quer alterar**. Não repita o onboarding inteiro e não repergunte campos que ele não mencionou.
3. Grave apenas os campos alterados via `POST /api/config` (ver Etapa 3).
4. **Pule a Etapa 2 inteira.** Os arquivos já estão instalados. A única exceção é se o usuário mudou `projectsRoot`: nesse caso copie os arquivos para a nova pasta, mova `projetos-data.json` e `dashboard-config.json` junto, e reinicie o servidor lá.
5. Confirme o que mudou e encerre. Não rode scan nem reapresente o manual sem que o usuário peça.

Se o usuário alterar o `devLevel`, avise que isso muda o teto de complexidade arquitetural dos próximos comandos, mas **não** reescreve projetos já criados.

## Etapa 1 — Perfil e preferências

Pergunte somente o que ainda não estiver salvo:

- **Nível de calibração**: Beginner, Junior, Mid-Level ou Senior. Define a profundidade das explicações e o teto de complexidade arquitetural de todos os outros comandos.
- **Pasta-base dos projetos**: onde os projetos ficam e onde o Project Hub vai escanear.
- **Plataforma padrão**: React (Vite), Next.js ou React Native/Expo. É apenas um padrão; cada projeto pode divergir.
- **Objetivo predominante**: acadêmico, MVP ou produção.

Explique que TypeScript estrito é obrigatório e não é configurável.

## Etapa 2 — Instalação das ferramentas locais

Apenas no **modo instalação**. Vem antes da gravação do perfil: sem os arquivos copiados não existe `dashboard-config.json` nem servidor para receber o `POST`.

1. Copie `./skills/react-dev/references/project-hub/dashboard-server.py`, `dashboard-template.html` e o inicializador do sistema operacional para a pasta-base escolhida.

   > `./` e a raiz do plugin instalado. No Claude Code, quando o plugin e instalado por um marketplace, os arquivos ficam em um cache (`~/.claude/plugins/cache/...`); use sempre caminhos relativos ao diretorio do plugin, nunca ao projeto do usuario.
2. Escreva `dashboard-config.json` na pasta-base, ao lado de `dashboard-server.py`, com os campos do perfil (ver Etapa 3).

   > **Nunca sobrescreva um `dashboard-config.json` que já existe.** O arquivo também guarda `githubUsername` e `githubToken`, que não pertencem ao perfil e seriam perdidos. Se o arquivo existir, você está em modo reconfiguração: volte à Etapa 0 e use `POST /api/config`, que faz merge parcial.

3. Suba o Project Hub: `iniciar-dashboard.bat` no Windows, `./iniciar-dashboard.command` no macOS/Linux. O painel abre em `http://127.0.0.1:8766`.

## Etapa 3 — Persistência do perfil

Campos a gravar:

```json
{
  "devLevel": "Junior",
  "projectsRoot": "/caminho/dos/projetos",
  "defaultPlatform": "next",
  "defaultGoal": "mvp",
  "scanRoot": "/caminho/dos/projetos",
  "setupCompletedAt": "2026-01-01T00:00:00Z"
}
```

No modo instalação, escreva o arquivo diretamente (Etapa 2, passo 2). No modo reconfiguração, **sempre** use `POST /api/config`: ele faz merge parcial, então envie só os campos alterados e o resto é preservado. Se o Project Hub estiver fora do ar, suba-o antes em vez de reescrever o arquivo à mão.

Mantenha `scanRoot` alinhado com `projectsRoot` para que o scan do dashboard funcione sem reconfiguração. Se o usuário alterar `scanRoot` pelo modal de Configurações do painel, avise que `projectsRoot` não muda junto.

## Etapa 4 — Conferência

Apenas no modo instalação.

1. Informe o caminho de `manual.html` para consulta rápida dos comandos.
2. Rode o scan da pasta-base (`GET /api/scan`) para pré-popular projetos React já existentes, se houver.

## Encerramento

No modo instalação, confirme em uma lista curta: nível registrado, pasta-base, Project Hub no ar e manual disponível. Termine indicando o próximo passo real: `/criar-projeto` para um projeto novo, ou `/review` para um projeto que já existe.

No modo reconfiguração, liste apenas o que mudou, no formato `campo: antes → depois`.

Não gere scaffolding, não crie estrutura de pastas de aplicação e não instale dependências neste comando.
