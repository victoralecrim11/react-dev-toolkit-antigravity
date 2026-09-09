#!/usr/bin/env python3
"""Valida a estrutura do plugin Antigravity antes de publicar.

Checa: plugin.json, mcp_config.json, skills/*/SKILL.md, commands/*.md,
frontmatter YAML, referencias internas, ausencia de segredos hardcoded,
ausencia de '-extension' e residuos.

Uso:
    python scripts/validate-plugin.py

Sai com codigo 1 se houver erro. Warnings nao falham.
"""
import glob
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

errs, warns, oks = [], [], []
E, W, O = errs.append, warns.append, oks.append


def load(rel):
    try:
        return json.loads(Path(rel).read_text(encoding="utf-8"))
    except FileNotFoundError:
        E(f"{rel}: nao encontrado")
    except json.JSONDecodeError as exc:
        E(f"{rel}: JSON invalido - {exc}")
    return None


def frontmatter(path):
    text = Path(path).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "sem frontmatter YAML"
    end = text.find("\n---", 4)
    if end == -1:
        return None, "frontmatter nao fechado"
    data = {}
    current_key = None
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(" ") and not line.startswith("  "):
            # YAML de lista ou bloco indentado simples
            pass
        if line.startswith(" ") and current_key is not None:
            if not line.lstrip().startswith("-"):
                return None, f"linha sem ':' no frontmatter: {line!r}"
            item = line.strip()
            if item.startswith("-"):
                item = item[1:].strip()
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(item)
            continue
        if ":" not in line:
            return None, f"linha sem ':' no frontmatter: {line!r}"
        k, v = line.split(":", 1)
        current_key = k.strip()
        v = v.strip()
        if not v:
            data[current_key] = []
            continue
        if v.lower() in ("true", "yes", "on", "1"):
            v = True
        elif v.lower() in ("false", "no", "off", "0"):
            v = False
        data[current_key] = v
    return data, None


# ---------- manifestos Antigravity ----------
pj = load("plugin.json")
if pj is None:
    print("\n".join("  ERRO  " + e for e in errs))
    sys.exit(1)

if not pj.get("name"):
    E("plugin.json: sem campo 'name'")
elif not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", pj["name"]):
    E(f"plugin name nao e kebab-case: {pj['name']}")
else:
    O(f"plugin.json: name ok ({pj['name']})")

if not pj.get("description"):
    W("plugin.json: sem description")
else:
    O("plugin.json: description ok")

mcp = load("mcp_config.json")
if mcp is not None:
    servers = mcp.get("mcpServers", {})
    if not servers:
        W("mcp_config.json: sem nenhum servidor MCP")
    else:
        O(f"mcp_config.json: {len(servers)} servidor(es) MCP ({', '.join(servers.keys())})")

# ---------- skills ----------
skill_files = sorted(glob.glob("skills/*/SKILL.md"))
if not skill_files:
    E("nenhuma skill encontrada em skills/*/SKILL.md")
else:
    O(f"{len(skill_files)} skills encontradas")

for f in skill_files:
    data, err = frontmatter(f)
    if err:
        E(f"{f}: {err}")
        continue
    if not data.get("name"):
        E(f"{f}: frontmatter sem name")
    if not data.get("description"):
        E(f"{f}: frontmatter sem description")

# ---------- agents ----------
agent_files = sorted(glob.glob("agents/*/agent.md"))
if agent_files:
    O(f"{len(agent_files)} agents encontrados")
    seen_names = {}
    for f in agent_files:
        data, err = frontmatter(f)
        if err:
            E(f"{f}: {err}")
            continue
        name = data.get("name")
        if not name:
            E(f"{f}: frontmatter sem name")
        if not data.get("description"):
            E(f"{f}: frontmatter sem description")
        if not data.get("tools"):
            E(f"{f}: frontmatter sem tools")
        if name:
            if name in seen_names:
                E(f"agent duplicado: {name} em {seen_names[name]} e {f}")
            else:
                seen_names[name] = f
else:
    O("nenhum agent encontrado em agents/*/agent.md (opcional)")

# ---------- commands ----------
cmd_files = sorted(glob.glob("commands/*.md"))
for f in cmd_files:
    data, err = frontmatter(f)
    if err:
        E(f"{f}: {err}")
        continue
    if not data.get("description"):
        E(f"{f}: frontmatter sem description")

# ---------- seguranca: deteccao de segredos ----------
SECRET_PATTERNS = {
    "GitHub Token": re.compile(r"gh[pous]_[A-Za-z0-9_]{36,255}"),
    "OpenAI / Provider Key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "Vercel Token": re.compile(r"\bvercel_[A-Za-z0-9_]{24,}\b"),
    "Chave Privada": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "Chave/Token em Hardcode": re.compile(
        r"""(?i)(?:api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]"""
    ),
}

found_secrets = []
scan_files = (
    glob.glob("commands/*.md")
    + glob.glob("skills/**/*.md", recursive=True)
    + glob.glob("agents/**/*.md", recursive=True)
    + glob.glob("rules/*.md")
    + glob.glob("scripts/*.py")
    + glob.glob("scripts/*.sh")
    + glob.glob("scripts/*.ps1")
)

for f in scan_files:
    content = Path(f).read_text(encoding="utf-8", errors="ignore")
    for line_num, line in enumerate(content.splitlines(), start=1):
        if any(token in line.lower() for token in ("placeholder", "exemplo", "example", "<chave")):
            continue
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                found_secrets.append(f"{f}:{line_num} ({name})")

if found_secrets:
    for item in found_secrets:
        E(f"possivel segredo hardcoded detectado: {item}")
else:
    O("nenhum segredo ou chave de API hardcoded detectado")

# ---------- higiene ----------
leaked = [
    os.path.basename(os.path.dirname(f))
    for f in skill_files
    if "extension" in os.path.basename(os.path.dirname(f))
]
if leaked:
    E(f"skills com 'extension' no nome: {leaked}")

ext_hits = [
    f
    for f in glob.glob("commands/*.md") + glob.glob("skills/**/*.md", recursive=True)
    if re.search(r"-extension", Path(f).read_text(encoding="utf-8"))
]
if ext_hits:
    E(f"ainda ha referencia a '-extension' em: {ext_hits}")
else:
    O("nenhuma referencia a '-extension' nos arquivos do plugin")

junk = 0
# Concatenando a string para o filtro do chat não cortar o código
cite_pattern = re.compile(r"\[c" + r"ite:\s*\d+\]")

for f in glob.glob("**/*.md", recursive=True):
    content = Path(f).read_text(encoding="utf-8")
    matches = cite_pattern.findall(content)
    if matches:
        E(f"{f}: {len(matches)} marcador(es) residuais")
        junk += len(matches)
if not junk:
    O("nenhum marcador residual")

bytecode = glob.glob("**/__pycache__", recursive=True) + glob.glob("**/*.pyc", recursive=True)
if bytecode:
    E(f"bytecode versionado: {bytecode}")
else:
    O("sem __pycache__/*.pyc")

missing_refs = []
ref_pattern = re.compile(
    r"`((?:\./)?skills/(?:react-dev|ui-ux)/(?:references|data)/[^`\s]+|references/[^`\s]+)`"
)
for f in glob.glob("commands/*.md") + glob.glob("skills/**/*.md", recursive=True):
    if f.endswith("SKILL.md"):
        base = Path(f).parent
    elif Path(f).as_posix().startswith("skills/react-dev/references/"):
        base = Path("skills/react-dev")
    elif Path(f).as_posix().startswith("skills/ui-ux/references/"):
        base = Path("skills/ui-ux")
    else:
        base = Path(".")
    text = Path(f).read_text(encoding="utf-8")
    for m in ref_pattern.finditer(text):
        ref = m.group(1)
        if ref.startswith("references/"):
            target = base / ref
        else:
            target = Path(ref[2:] if ref.startswith("./") else ref)
        if not target.exists():
            missing_refs.append(f"{f}: {ref}")

if missing_refs:
    E(f"referencias internas inexistentes: {missing_refs}")
else:
    O("referencias internas citadas existem")

# ---------- saida ----------
for o in oks:
    print(f"  OK    {o}")
if warns:
    print()
    for w in warns:
        print(f"  WARN  {w}")
if errs:
    print()
    for e in errs:
        print(f"  ERRO  {e}")
print(f"\n{len(errs)} erro(s), {len(warns)} warning(s)")
sys.exit(1 if errs else 0)