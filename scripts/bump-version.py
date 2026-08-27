#!/usr/bin/env python3
"""Sincroniza a versao do plugin Antigravity nos arquivos que a declaram.

Arquivos atualizados:
  - plugin.json (campo "version")
  - README.md (cabecalho vX.Y.Z e seção de changelog)
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
README_RE = re.compile(r'^(# React Dev Hub Plugin .+?— v)(\d+\.\d+\.\d+)\s*$', re.MULTILINE)
README_INDEX_RE = re.compile(r'^(\s*-\s*\[React Dev Hub Plugin — Antigravity Edition — v)(\d+\.\d+\.\d+)(\]\(#react-dev-hub-plugin--antigravity-edition--v)(\d+)(\)\s*)$', re.MULTILINE)
README_CHANGELOG_RE = re.compile(r'^## O que mudou na v\d+\.\d+\.\d+\s*\n(?:.*\n)*?(?=^## |\Z)', re.MULTILINE)

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


def update_readme(readme_text, new_version):
    readme_text = README_RE.sub(lambda m: m.group(1) + new_version, readme_text)
    readme_text = README_INDEX_RE.sub(
        lambda m: m.group(1) + new_version + m.group(3) + new_version.replace(".", "") + m.group(5),
        readme_text,
    )

    section_title = f"## O que mudou na v{new_version}"
    section_body = (
        f"{section_title}\n\n"
        f"- Atualização da documentação para a versão v{new_version}.\n"
        "- Ajustes de sincronização do README e do script de atualização.\n"
    )

    existing_section = README_CHANGELOG_RE.search(readme_text)
    if existing_section and existing_section.group(0).startswith(section_title):
        readme_text = readme_text[:existing_section.start()] + section_body + readme_text[existing_section.end():]
    else:
        marker = "\n## Licenca"
        if marker in readme_text:
            readme_text = readme_text.replace(marker, f"\n{section_body.strip()}\n\n## Licenca", 1)
        else:
            readme_text = readme_text.rstrip() + "\n\n" + section_body

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
            updated = update_readme(rt, new)
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
