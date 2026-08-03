---
description: Reabre o Project Hub local para projetos, componentes, reviews e checklist.
---
# /dashboard

Use a referência `./skills/react-dev/references/dashboard-projetos.md`.

Caso normal — o `/setup` já rodou: leia `projectsRoot` em `dashboard-config.json`, va ate `ProjectHub/` dentro dessa pasta e rode `iniciar-dashboard.bat` no Windows ou `./iniciar-dashboard.command` no macOS/Linux. O painel abre em `http://127.0.0.1:8766`.

Caso o Project Hub ainda não exista na máquina: sugira `/setup`, que faz a instalação completa. Se o usuário preferir apenas o painel agora, copie `./skills/react-dev/references/project-hub/dashboard-server.py`, `dashboard-template.html` e o inicializador para uma pasta `ProjectHub/` dentro da pasta desejada e execute ali mesmo.

Os dados persistem em `projetos-data.json` e o perfil em `dashboard-config.json`, ambos dentro de `ProjectHub/` ao lado de `dashboard-server.py`.
