#!/usr/bin/env python3
"""Project Hub local: Python standard library + JSON persistence."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit, parse_qs
import json, os, re, sys, webbrowser
import urllib.request, urllib.error

APP_VERSION = "2026-07-28-v7"

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "projetos-data.json"
CONFIG_FILE = ROOT / "dashboard-config.json"
HTML_FILE = ROOT / "dashboard-template.html"

DEFAULT = {"projects": [], "components": [], "reviews": [], "checklists": {}}
DEFAULT_CONFIG = {
    "scanRoot": str(Path.home() / "Downloads"),
    "githubUsername": "",
    "githubToken": "",
    # Perfil do desenvolvedor. Escrito somente pelo comando /setup; os demais
    # comandos apenas leem. Vazio significa que /setup ainda nao rodou.
    "devLevel": "",          # Beginner | Junior | Mid-Level | Senior
    "projectsRoot": "",      # pasta-base dos projetos
    "defaultPlatform": "",   # react | next | expo
    "defaultGoal": "",       # academico | mvp | producao
    "setupCompletedAt": "",  # ISO-8601
}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".expo", "coverage", ".turbo", ".cache"}
REACT_DEP_MARKERS = ("react", "react-native", "next", "expo")

def load_data():
    if not DATA_FILE.exists(): return json.loads(json.dumps(DEFAULT))
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        for key, value in DEFAULT.items(): data.setdefault(key, json.loads(json.dumps(value)))
        # Registros gravados antes da normalizacao podem ter as chaves em
        # portugues (nome, caminho, nivel...) e por isso apareciam com os campos
        # em branco no painel. Normalizar na leitura recupera esses valores sem
        # exigir que o usuario reescreva nada.
        for collection in CANONICAL:
            data[collection] = [normalize_item(collection, item)[0] for item in data.get(collection, [])]
        return data
    except (OSError, json.JSONDecodeError): return json.loads(json.dumps(DEFAULT))

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def load_config():
    if not CONFIG_FILE.exists(): return DEFAULT_CONFIG.copy()
    try:
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        for key, value in DEFAULT_CONFIG.items(): cfg.setdefault(key, value)
        return cfg
    except (OSError, json.JSONDecodeError): return DEFAULT_CONFIG.copy()

def save_config(cfg):
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

def stamp(item):
    item["updatedAt"] = datetime.now(timezone.utc).isoformat()
    if not item.get("id"):
        item["id"] = str(int(datetime.now(timezone.utc).timestamp() * 1000000))
    return item

# ---------------------------------------------------------------------------
# Normalizacao de payload
#
# O POST antes gravava o payload cru. Quem registrava um projeto via API tinha
# que acertar o nome exato de cada chave; qualquer variacao (em portugues, em
# snake_case) era gravada como campo extra e o campo real ficava vazio -- o que
# fazia o card aparecer sem nome e sem caminho local. Agora toda chave passa
# por um mapa de sinonimos e o item sai com o conjunto canonico completo.
# ---------------------------------------------------------------------------

CANONICAL = {
    "projects": ["name", "path", "platform", "status", "reactVersion", "stack", "level", "notes", "repoUrl"],
    "components": ["name", "project", "category", "path", "description"],
    "reviews": ["project", "maintainability", "summary", "debts"],
}

# Campos sem os quais o painel perde funcionalidade (detectar componentes, etc.).
REQUIRED = {"projects": ["name", "path"], "components": ["name", "project"], "reviews": ["project"]}

ALIASES = {
    "projects": {
        "nome": "name", "projectname": "name", "projeto": "name", "title": "name",
        "caminho": "path", "caminholocal": "path", "localpath": "path", "projectpath": "path",
        "folder": "path", "pasta": "path", "dir": "path", "directory": "path", "root": "path",
        "plataforma": "platform", "stackplatform": "platform", "framework": "platform",
        "situacao": "status", "estado": "status",
        "versaoreact": "reactVersion", "reactversion": "reactVersion", "versao": "reactVersion",
        "react": "reactVersion",
        "tecnologias": "stack", "techstack": "stack", "technologies": "stack",
        "nivel": "level", "senioridade": "level", "devlevel": "level", "seniority": "level",
        "notas": "notes", "observacoes": "notes", "obs": "notes",
        "repo": "repoUrl", "repositorio": "repoUrl", "github": "repoUrl", "repourl": "repoUrl",
    },
    "components": {
        "nome": "name", "componente": "name",
        "projectname": "project", "projeto": "project",
        "categoria": "category", "tipo": "category",
        "caminho": "path", "filepath": "path", "arquivo": "path",
        "descricao": "description", "desc": "description", "reuso": "description",
    },
    "reviews": {
        "projeto": "project", "projectname": "project",
        "manutenibilidade": "maintainability", "score": "maintainability", "nota": "maintainability",
        "resumo": "summary", "sumario": "summary",
        "debitos": "debts", "dividas": "debts", "technicaldebt": "debts", "debitostecnicos": "debts",
    },
}

LEVELS = {"beginner": "Beginner", "junior": "Junior", "midlevel": "Mid-Level",
          "mid": "Mid-Level", "pleno": "Mid-Level", "senior": "Senior"}

def _slug(key):
    return re.sub(r"[^a-z0-9]", "", str(key).lower())

def normalize_item(collection, payload):
    """Mapeia sinonimos para as chaves canonicas e completa o conjunto de campos.

    Retorna (item, warnings). Campos preservados: id, updatedAt e quaisquer
    chaves desconhecidas, para nunca descartar dado que o usuario enviou.
    """
    canonical = CANONICAL.get(collection, [])
    if not canonical:
        return payload, []
    by_slug = {_slug(k): k for k in canonical}
    aliases = ALIASES.get(collection, {})

    item, extras = {}, {}
    for raw_key, value in payload.items():
        if raw_key in ("id", "updatedAt"):
            item[raw_key] = value
            continue
        slug = _slug(raw_key)
        target = by_slug.get(slug) or aliases.get(slug)
        if target:
            # Nao deixa um alias vazio sobrescrever um valor ja preenchido.
            if target not in item or (item.get(target) in ("", None) and value not in ("", None)):
                item[target] = value
        else:
            extras[raw_key] = value

    for key in canonical:
        item.setdefault(key, [] if key == "debts" else "")

    # debts aceita string separada por virgula ou lista.
    if collection == "reviews" and isinstance(item.get("debts"), str):
        item["debts"] = [d.strip() for d in item["debts"].split(",") if d.strip()]

    if collection == "projects":
        lvl = _slug(item.get("level", ""))
        if lvl in LEVELS:
            item["level"] = LEVELS[lvl]
        if isinstance(item.get("path"), str):
            item["path"] = item["path"].strip().strip('"').strip("'")

    item.update(extras)
    return item, field_warnings(collection, item)

def field_warnings(collection, item):
    """Avisos sobre campos vazios. Deve ser calculado sobre o registro FINAL.

    Calcular sobre o payload de entrada daria falso positivo em atualizacao
    parcial: um POST so com 'notes' acusaria 'name' e 'path' vazios mesmo que
    o registro salvo tenha os dois preenchidos.
    """
    canonical = CANONICAL.get(collection, [])
    faltando = [k for k in REQUIRED.get(collection, []) if not str(item.get(k, "")).strip()]
    vazios = [k for k in canonical if not str(item.get(k, "")).strip() and k not in faltando]
    warnings = []
    if faltando:
        warnings.append("Campos obrigatorios vazios: " + ", ".join(faltando))
    if vazios:
        warnings.append("Campos opcionais vazios: " + ", ".join(vazios))
    return warnings

def resolve_project_path(item):
    """Tenta descobrir o caminho local quando ele nao foi enviado.

    Procura <projectsRoot>/<name> e <scanRoot>/<name>. So aceita se a pasta
    existir de fato -- nunca inventa um caminho.
    """
    if str(item.get("path", "")).strip() or not str(item.get("name", "")).strip():
        return False
    cfg = load_config()
    for base in (cfg.get("projectsRoot", ""), cfg.get("scanRoot", "")):
        if not base:
            continue
        try:
            candidate = Path(base).expanduser() / item["name"]
        except (OSError, RuntimeError):
            continue
        if candidate.is_dir():
            item["path"] = str(candidate)
            return True
    return False

# Campos de projeto que podem ser herdados do perfil quando vierem vazios.
# Espelha o pre-preenchimento que o formulario do painel faz via suggest():
# um projeto registrado pela API passa a ficar tao completo quanto um
# cadastrado na tela.
PROFILE_DEFAULTS = {"status": "defaultGoal", "platform": "defaultPlatform", "level": "devLevel"}

def apply_profile_defaults(item):
    """Completa campos vazios com o perfil salvo. Retorna os campos herdados."""
    cfg = load_config()
    herdados = []
    for field, cfg_key in PROFILE_DEFAULTS.items():
        if str(item.get(field, "")).strip():
            continue
        value = str(cfg.get(cfg_key, "")).strip()
        if not value:
            continue
        if field == "level":
            value = LEVELS.get(_slug(value), value)
        item[field] = value
        herdados.append(field)
    return herdados

def scan_projects(root, max_depth=6):
    results = []
    try:
        root_path = Path(root).expanduser().resolve()
    except (OSError, RuntimeError):
        return results
    if not root_path.exists() or not root_path.is_dir():
        return results
    root_depth = len(root_path.parts)
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        depth = len(Path(dirpath).parts) - root_depth
        if depth > max_depth:
            dirnames[:] = []
            continue
        if "package.json" not in filenames:
            continue
        try:
            pkg = json.loads((Path(dirpath) / "package.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        if not any(marker in deps for marker in REACT_DEP_MARKERS):
            continue
        platform = ("Expo" if "expo" in deps else "Next.js" if "next" in deps
                    else "React Native" if "react-native" in deps else "React")
        stack = [k for k in ("react", "react-native", "next", "expo", "typescript", "zustand", "redux", "tailwindcss") if k in deps]
        results.append({
            "name": pkg.get("name") or Path(dirpath).name,
            "path": str(dirpath),
            "reactVersion": deps.get("react", deps.get("react-native", "")),
            "platform": platform,
            "stack": ", ".join(stack),
        })
        dirnames[:] = []  # nao desce dentro de um projeto ja identificado
    return results

CATEGORY_HINTS = ["atoms", "molecules", "organisms", "templates", "pages", "screens", "hooks", "layout", "layouts", "components"]
IGNORED_SUFFIXES = (".test.tsx", ".test.jsx", ".spec.tsx", ".spec.jsx", ".stories.tsx", ".stories.jsx", ".d.ts")

def scan_components(root, max_depth=8):
    results = []
    try:
        root_path = Path(root).expanduser().resolve()
    except (OSError, RuntimeError):
        return results
    if not root_path.exists() or not root_path.is_dir():
        return results
    root_depth = len(root_path.parts)
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        depth = len(Path(dirpath).parts) - root_depth
        if depth > max_depth:
            dirnames[:] = []
            continue
        for filename in filenames:
            if not filename.endswith((".tsx", ".jsx")): continue
            if filename.endswith(IGNORED_SUFFIXES): continue
            stem = filename.rsplit(".", 1)[0]
            if not stem[:1].isupper(): continue  # convencao de componente React: PascalCase
            file_path = Path(dirpath) / filename
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            looks_like_component = (
                re.search(r"export\s+default\s+function\s+" + re.escape(stem), content)
                or re.search(r"export\s+(default\s+)?(const|function|class)\s+" + re.escape(stem), content)
                or "export default" in content
            )
            if not looks_like_component: continue
            parent_names = [p.lower() for p in Path(dirpath).parts[root_depth:]]
            category = next((h for h in CATEGORY_HINTS if h in parent_names), "component")
            results.append({
                "name": stem,
                "path": str(file_path.relative_to(root_path)),
                "category": category,
            })
    return results

def github_api(path, token=""):
    url = "https://api.github.com" + path
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "react-dev-hub-dashboard"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        msg = "Usuario/token invalido ou limite de requisicoes atingido" if e.code in (401, 403) else "GitHub retornou %s" % e.code
        return None, msg
    except urllib.error.URLError:
        return None, "Sem conexao com a internet"

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, status, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        parsed = urlsplit(self.path)
        qs = parse_qs(parsed.query)

        if parsed.path == "/api/version":
            return self.send_json(200, {"version": APP_VERSION, "root": str(ROOT), "html": str(HTML_FILE), "data": str(DATA_FILE)})
        if parsed.path == "/api/data": return self.send_json(200, load_data())
        if parsed.path == "/api/config": return self.send_json(200, load_config())

        if parsed.path == "/api/scan":
            cfg = load_config()
            scan_root = qs.get("path", [cfg.get("scanRoot", "")])[0]
            found = scan_projects(scan_root)
            registered = {p.get("path") for p in load_data()["projects"]}
            for item in found: item["alreadyRegistered"] = item["path"] in registered
            return self.send_json(200, {"root": scan_root, "found": found})

        if parsed.path == "/api/scan-components":
            project_id = qs.get("projectId", [""])[0]
            data = load_data()
            project = next((p for p in data["projects"] if str(p.get("id")) == str(project_id)), None)
            if not project:
                return self.send_json(404, {"error": "Projeto nao encontrado (id %s)" % project_id})
            if not project.get("path"):
                return self.send_json(400, {"error": "Este projeto nao tem um caminho local salvo. Edite o projeto e preencha o campo 'Caminho local'."})
            if not Path(project["path"]).expanduser().is_dir():
                return self.send_json(400, {"error": "A pasta '%s' nao existe ou nao e acessivel." % project["path"]})
            found = scan_components(project["path"])
            registered = {(c.get("project"), c.get("path")) for c in data["components"]}
            for c in found: c["alreadyRegistered"] = (project.get("name"), c["path"]) in registered
            return self.send_json(200, {"projectId": project_id, "projectName": project.get("name", ""),
                                        "projectPath": project.get("path", ""), "found": found})

        if parsed.path == "/api/github/repos":
            cfg = load_config()
            username = cfg.get("githubUsername", "")
            if not username: return self.send_json(400, {"error": "Configure seu usuario do GitHub em Configuracoes."})
            result, err = github_api("/users/%s/repos?per_page=100&sort=updated" % username, cfg.get("githubToken", ""))
            if err: return self.send_json(502, {"error": err})
            registered = {p.get("repoUrl") for p in load_data()["projects"]}
            repos = [{
                "name": r["name"], "fullName": r["full_name"], "description": r.get("description") or "",
                "language": r.get("language") or "", "stars": r.get("stargazers_count", 0),
                "private": r.get("private", False), "url": r.get("html_url"), "pushedAt": r.get("pushed_at"),
                "alreadyRegistered": r["full_name"] in registered,
            } for r in result]
            return self.send_json(200, repos)

        if parsed.path == "/api/github/repo-info":
            repo = qs.get("repo", [""])[0]
            if not repo: return self.send_json(400, {"error": "Parametro repo e obrigatorio (owner/nome)."})
            cfg = load_config()
            info, err = github_api("/repos/" + repo, cfg.get("githubToken", ""))
            if err: return self.send_json(502, {"error": err})
            commits, cerr = github_api("/repos/%s/commits?per_page=1" % repo, cfg.get("githubToken", ""))
            last_msg = commits[0]["commit"]["message"].split("\n")[0] if not cerr and commits else ""
            last_date = commits[0]["commit"]["author"]["date"] if not cerr and commits else ""
            return self.send_json(200, {
                "stars": info.get("stargazers_count", 0), "defaultBranch": info.get("default_branch", ""),
                "lastCommitMessage": last_msg, "lastCommitDate": last_date,
            })

        if parsed.path in ("/", "/index.html", "/dashboard-template.html"):
            return self.serve_html()
        return super().do_GET()

    def serve_html(self):
        # Le o HTML do disco a cada requisicao e envia com no-store, sem passar pelo cache
        # condicional (If-Modified-Since / ETag) do SimpleHTTPRequestHandler. Era esse cache
        # que gerava "304 Not Modified" e fazia o navegador continuar usando a versao antiga
        # do arquivo mesmo depois de ele ter sido substituido no disco.
        try:
            raw = HTML_FILE.read_bytes()
        except OSError:
            return self.send_json(404, {"error": "dashboard-template.html nao encontrado em " + str(HTML_FILE)})
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        try: payload = self.read_json()
        except json.JSONDecodeError: return self.send_json(400, {"error": "JSON invalido"})

        if self.path == "/api/config":
            cfg = load_config()
            cfg.update(payload)
            # projectsRoot e a fonte da verdade da pasta-base; scanRoot acompanha
            # para o scan nao apontar para outro lugar sem o usuario perceber.
            if str(payload.get("projectsRoot", "")).strip() and "scanRoot" not in payload:
                cfg["scanRoot"] = cfg["projectsRoot"]
            save_config(cfg)
            return self.send_json(200, cfg)

        data = load_data()
        collection = {"/api/projects": "projects", "/api/components": "components", "/api/reviews": "reviews"}.get(self.path)
        if collection:
            # O formulario do painel manda _replace: campo apagado na tela deve
            # ficar apagado. Chamadas de API (agentes) omitem a flag e recebem
            # merge, para um payload parcial nao zerar campos ja preenchidos.
            replace = bool(payload.pop("_replace", False))
            item, warnings = normalize_item(collection, payload)
            items = data[collection]
            existe = any(str(v.get("id")) == str(item.get("id", "")) for v in items) if item.get("id") else False
            if collection == "projects":
                if resolve_project_path(item):
                    warnings = [w for w in warnings if "path" not in w]
                    warnings.append("Caminho local deduzido da pasta-base: " + item["path"])
                # Herdar do perfil so ao CRIAR. Em atualizacao nao: com _replace o
                # usuario esta apagando o campo de proposito, e reencher seria
                # desfazer a acao dele.
                if not existe and not replace:
                    herdados = apply_profile_defaults(item)
                    if herdados:
                        warnings.append("Herdado do perfil: " + ", ".join(herdados))
            item = stamp(item)
            old = next((i for i, value in enumerate(items) if str(value.get("id")) == str(item["id"])), None)
            if old is None:
                items.append(item)
            elif replace:
                items[old] = item
            else:
                merged = dict(items[old])
                for key, value in item.items():
                    if value not in ("", None, []) or key not in merged:
                        merged[key] = value
                item = merged
                items[old] = item
            save_data(data)
            # Recalcula sobre o registro final; ver field_warnings(). Os avisos
            # informativos (deducao de caminho, heranca de perfil) sao mantidos.
            final = field_warnings(collection, item)
            final += [w for w in warnings if w.startswith(("Caminho local deduzido", "Herdado do perfil"))]
            return self.send_json(200, dict(item, warnings=final))
        if self.path == "/api/checklists":
            project_id = str(payload.get("projectId", "")); data["checklists"][project_id] = payload.get("items", {})
            save_data(data); return self.send_json(200, data["checklists"][project_id])
        return self.send_json(404, {"error": "Endpoint nao encontrado"})

    def do_DELETE(self):
        parts = self.path.strip("/").split("/")
        if len(parts) != 3 or parts[0] != "api": return self.send_json(404, {"error": "Rota invalida"})
        collection = {"projects": "projects", "components": "components", "reviews": "reviews"}.get(parts[1])
        if not collection: return self.send_json(404, {"error": "Colecao invalida"})
        data = load_data(); data[collection] = [x for x in data[collection] if x.get("id") != parts[2]]; save_data(data)
        return self.send_json(200, {"ok": True})

if __name__ == "__main__":
    print("=" * 70)
    print(" Project Hub", APP_VERSION)
    print(" Pasta lida por este servidor :", ROOT)
    print(" HTML  :", HTML_FILE, "(existe)" if HTML_FILE.exists() else "(NAO ENCONTRADO!)")
    print(" Dados :", DATA_FILE, "(existe)" if DATA_FILE.exists() else "(sera criado no primeiro registro)")
    print("=" * 70)
    if not HTML_FILE.exists():
        print("\nERRO: o dashboard-template.html precisa estar NA MESMA PASTA deste .py.")
        print("Coloque os dois arquivos juntos em", ROOT, "e rode de novo.\n")
        sys.exit(1)
    server = ThreadingHTTPServer(("127.0.0.1", 8766), Handler)
    print("Abra http://127.0.0.1:8766")
    webbrowser.open("http://127.0.0.1:8766")
    try: server.serve_forever()
    except KeyboardInterrupt: print("\nServidor encerrado.")