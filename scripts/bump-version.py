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
"""
import argparse
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# arquivo -> quantas ocorrencias de "version" devem existir no Antigravity
TARGETS = {
    "plugin.json": 1,
}

VERSION_RE = re.compile(r'("version"\s*:\s*")(\d+\.\d+\.\d+)(")')

# No manual.html a versao e texto
MANUAL = "manual.html"
MANUAL_RE = re.compile(r'(v)(\d+\.\d+\.\d+)')

# No README.md, atualiza APENAS o cabecalho h1 principal do plugin
# O historico de changelog (## O que mudou na vX.Y.Z) NAO e alterado
README = "README.md"
README_RE = re.compile(r'^(# .*?Antigravity Edition.*? v)(\d+\.\d+\.\d+)\s*$', re.MULTILINE)
README_TOP_LINK_RE = re.compile(r'^(- \[.*? v)(\d+\.\d+\.\d+)(\]\(#.*?-v)(\d+)(\))\s*$', re.MULTILINE)
# Captura a identacao exata para o Indice (TOC)
README_LINK_ITEM_RE = re.compile(r'^(\s*)- \[O que mudou na v\d+\.\d+\.\d+\]\(#o-que-mudou-na-v\d+\)\s*$', re.MULTILINE)
# Tolera a presenca ou ausencia da ancora <a id>
README_SECTION_HEADING_RE = re.compile(r'^(?:<a id="o-que-mudou-na-v\d+"></a>\n)?## O que mudou na v\d+\.\d+\.\d+\s*$', re.MULTILINE)

TOTAIS = sum(TARGETS.values()) + 2


def read_current():
    p = ROOT / "plugin.json"
    v = json.loads(p.read_text(encoding="utf-8")).get("version")
    if not v:
        sys.exit("erro: plugin.json nao tem campo version")
    return v


def git_last_commit_subject():
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--pretty=%s"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def bump(v, part):
    major, minor, patch = (int(x) for x in v.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


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
            
            # Atualiza titulo principal
            newrt = README_RE.sub(lambda m: m.group(1) + new, rt)
            
            # Atualiza o link principal do indice
            newrt = README_TOP_LINK_RE.sub(
                lambda m: m.group(1) + new + m.group(3) + new.replace(".", "") + m.group(5),
                newrt,
            )
            
            # Atualiza os links aninhados do changelog no Indice
            if f"[O que mudou na v{new}]" not in newrt:
                first_link = README_LINK_ITEM_RE.search(newrt)
                if first_link:
                    indent = first_link.group(1) # Pega a identacao exata da linha
                    newrt = (newrt[:first_link.start()] +
                             f"{indent}- [O que mudou na v{new}](#o-que-mudou-na-v{new.replace('.', '')})\n" +
                             newrt[first_link.start():])
                else:
                    # Fallback caso nao haja links anteriores (coloca abaixo do link principal)
                    top_link = README_TOP_LINK_RE.search(newrt)
                    if top_link:
                        newrt = (newrt[:top_link.end()] + 
                                 f"\n    - [O que mudou na v{new}](#o-que-mudou-na-v{new.replace('.', '')})" + 
                                 newrt[top_link.end():])

            # Atualiza o corpo do Changelog
            if f"## O que mudou na v{new}" not in newrt:
                commit_subject = git_last_commit_subject()
                summary_line = (f"- **Commit:** {commit_subject}"
                                if commit_subject else
                                f"- **Bump:** versão atualizada para v{new}.")
                section_content = (
                    f"<a id=\"o-que-mudou-na-v{new.replace('.', '')}\"></a>\n"
                    f"## O que mudou na v{new}\n\n"
                    f"{summary_line}\n"
                    f"- **Automação de changelog.** `scripts/bump-version.py` agora cria esta seção automaticamente no `README.md` durante o bump de versão.\n\n"
                )
                
                first_section = README_SECTION_HEADING_RE.search(newrt)
                if first_section:
                    newrt = newrt[:first_section.start()] + section_content + newrt[first_section.start():]
                else:
                    license_anchor = re.search(r'^## Licen[cç]a', newrt, re.MULTILINE)
                    if license_anchor:
                        newrt = newrt[:license_anchor.start()] + section_content + newrt[license_anchor.start():]
                    else:
                        newrt += f"\n{section_content}"
                        
            rr.write_text(newrt, encoding="utf-8", newline=nl)
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
        # Nao valida versoes do historico de changelog — apenas o h1 e plugin.json
        if seen != {new}:
            sys.exit(f"erro: versoes divergentes apos o bump: {sorted(seen)}")
        print(f"\nversao sincronizada em {TOTAIS} lugares: {new}")
        print(f"::set-version::{new}")


if __name__ == "__main__":
    main()