#!/usr/bin/env python3
"""Sincroniza a versao do plugin Antigravity nos arquivos que a declaram.

Arquivos atualizados:
  - plugin.json (campo "version")
  - README.md (cabecalho vX.Y.Z, Indice aninhado e secao de changelog)
  - manual.html (texto vX.Y.Z)

Uso:
    python scripts/bump-version.py            # bump do patch
    python scripts/bump-version.py --minor
    python scripts/bump-version.py --major
    python scripts/bump-version.py --set 2.0.0
    python scripts/bump-version.py --check    # so imprime, nao escreve

Edita apenas a string da versao, preservando a formatacao dos JSONs
(nao reserializa: isso evitaria diffs de formatacao desnecessarios).
"""
import argparse
import json
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Arquivo JSON com campo "version"
TARGETS = {
    "plugin.json": 1,
}

VERSION_RE = re.compile(r'("version"\s*:\s*")(\d+\.\d+\.\d+)(")')

# No manual.html e README.md a versao e texto, nao campo JSON.
MANUAL = "manual.html"
MANUAL_RE = re.compile(r'(v)(\d+\.\d+\.\d+)')

README = "README.md"
# Flexivel para aceitar tanto " - v" quanto " — v" no cabecalho
README_RE = re.compile(r'^(# .*?v)(\d+\.\d+\.\d+)\s*$', re.MULTILINE)

TOTAIS = sum(TARGETS.values()) + 2  # plugin.json + manual + readme


def read_current():
    p = ROOT / "plugin.json"
    v = json.loads(p.read_text(encoding="utf-8")).get("version")
    if not v:
        sys.exit("erro: plugin.json nao tem campo version")
    return v


def bump(v, part):
    major, minor, patch = (int(x) for x in v.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def get_last_commit():
    """Captura a ultima mensagem de commit via git log."""
    try:
        return subprocess.check_output("git log -1 --pretty=%B", shell=True).decode('utf-8').strip().split('\n')[0]
    except Exception:
        return "Atualizacao de versao"


def update_readme(readme_text, new_version, last_commit):
    # 1. Atualizar o titulo principal com a nova versao
    readme_text = README_RE.sub(lambda m: m.group(1) + new_version, readme_text)

    anchor_id = f"o-que-mudou-na-v{new_version.replace('.', '')}"
    toc_entry = f"- [O que mudou na v{new_version}](#{anchor_id})"

    # 2. Atualizar o Indice (TOC) para aninhar a versao anterior
    if re.search(r"^- \[O que mudou na v", readme_text, flags=re.MULTILINE):
        readme_text = re.sub(
            r"(^- \[O que mudou na v\d+\.\d+\.\d+\].*)",
            f"{toc_entry}\n  \\1",
            readme_text,
            count=1,
            flags=re.MULTILINE
        )
    # Se ainda nao existe changelog no Indice, coloca acima de Licenca
    elif "- [Licenca]" in readme_text:
        readme_text = readme_text.replace("- [Licenca]", f"{toc_entry}\n- [Licenca]", 1)
    elif "- [Licença]" in readme_text:
        readme_text = readme_text.replace("- [Licença]", f"{toc_entry}\n- [Licença]", 1)

    # 3. Atualizar o Corpo do Changelog
    body_entry = (
        f"<a id=\"{anchor_id}\"></a>\n"
        f"## O que mudou na v{new_version}\n\n"
        f"- **Commit:** {last_commit}\n"
        f"- **Automacao de changelog.** `scripts/bump-version.py` inseriu esta secao automaticamente no `README.md` durante o bump de versao.\n\n"
    )

    # Empurra versoes anteriores para baixo caso ja exista historico
    if re.search(r"^## O que mudou na v", readme_text, flags=re.MULTILINE):
        readme_text = re.sub(
            r"((?:<a id=\"o-que-mudou-na-v\d+\"></a>\n)?^## O que mudou na v\d+\.\d+\.\d+)",
            f"{body_entry}\\1",
            readme_text,
            count=1,
            flags=re.MULTILINE
        )
    # Se e o primeiro changelog automatizado, poe embaixo do marcador principal
    elif "## 📝 Changelog" in readme_text:
        readme_text = readme_text.replace(
            "## 📝 Changelog\n",
            f"## 📝 Changelog\n\n{body_entry}"
        )
    elif "## Licenca" in readme_text:
        readme_text = readme_text.replace("## Licenca", f"{body_entry}## Licenca", 1)

    return readme_text


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--major", action="store_true")
    g.add_argument("--minor", action="store_true")
    g.add_argument("--patch", action="store_true")
    g.add_argument("--set", dest="explicit", metavar="X.Y.Z")
    ap.add_argument("--check", action="store_true", help="nao escreve, so valida")
    args = ap.parse_args()

    current = read_current()
    if args.explicit:
        if not re.fullmatch(r"\d+\.\d+\.\d+", args.explicit):
            sys.exit(f"erro: '{args.explicit}' nao e semver X.Y.Z")
        new = args.explicit
    else:
        part = "major" if args.major else "minor" if args.minor else "patch"
        new = bump(current, part)

    if args.check:
        print(f"atual={current}")
        print(f"proxima={new}")

    problems, written = [], []
    
    # Valida plugin.json
    for rel, expected in TARGETS.items():
        path = ROOT / rel
        if not path.exists():
            problems.append(f"{rel}: arquivo nao encontrado")
            continue
        text = path.read_text(encoding="utf-8")
        found = len(VERSION_RE.findall(text))
        if found != expected:
            problems.append(f"{rel}: esperava {expected} campo(s) version, achei {found}")
            continue
        if args.check:
            written.append(f"  {rel}: {found} ocorrencia(s) ok")
            continue
        new_text = VERSION_RE.sub(lambda m: m.group(1) + new + m.group(3), text)
        try:
            json.loads(new_text)
        except json.JSONDecodeError as exc:
            problems.append(f"{rel}: substituicao geraria JSON invalido ({exc})")
            continue
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
        written.append(f"  {rel}: {current} -> {new}")

    # Valida manual.html
    mp = ROOT / MANUAL
    if not mp.exists():
        problems.append(f"{MANUAL}: nao encontrado")
    else:
        mt = mp.read_text(encoding="utf-8")
        found = len(MANUAL_RE.findall(mt))
        if found == 0:
            problems.append(f"{MANUAL}: nenhuma versao vX.Y.Z encontrada")
        elif args.check:
            written.append(f"  {MANUAL}: {found} ocorrencia(s) ok")
        else:
            nl = "\r\n" if "\r\n" in mt else "\n"
            mp.write_text(MANUAL_RE.sub(lambda m: m.group(1) + new, mt),
                          encoding="utf-8", newline=nl)
            written.append(f"  {MANUAL}: {found} ocorrencia(s) -> {new}")

    # Valida README.md e aplica o Changelog inteligente
    rr = ROOT / README
    if not rr.exists():
        problems.append(f"{README}: nao encontrado")
    else:
        rt = rr.read_text(encoding="utf-8")
        found = len(README_RE.findall(rt))
        if found == 0:
            problems.append(f"{README}: nenhuma cabecalho de versao encontrada")
        elif args.check:
            written.append(f"  {README}: {found} ocorrencia(s) ok")
        else:
            nl = "\r\n" if "\r\n" in rt else "\n"
            last_commit = get_last_commit()
            updated = update_readme(rt, new, last_commit)
            rr.write_text(updated, encoding="utf-8", newline=nl)
            written.append(f"  {README}: {found} ocorrencia(s) -> {new}")

    if problems:
        print("FALHOU:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        sys.exit(1)

    print("\n".join(written))
    if not args.check:
        seen = set()
        for rel in TARGETS:
            for m in VERSION_RE.finditer((ROOT / rel).read_text(encoding="utf-8")):
                seen.add(m.group(2))
        for m in MANUAL_RE.finditer((ROOT / MANUAL).read_text(encoding="utf-8")):
            seen.add(m.group(2))
        for m in README_RE.finditer((ROOT / README).read_text(encoding="utf-8")):
            seen.add(m.group(2))
        if seen != {new}:
            sys.exit(f"erro: versoes divergentes apos o bump: {sorted(seen)}")
        print(f"\nversao sincronizada em {TOTAIS} lugares: {new}")
        print(f"::set-version::{new}")


if __name__ == "__main__":
    main()