#!/usr/bin/env python3
"""
search-uiux.py — Motor de busca local dos datasets UI/UX.

Uso principal:
    python search-uiux.py "<consulta>" --domain <dominio>
    python search-uiux.py --list-domains

Uso legado (retrocompatível):
    python search-uiux.py <dataset.csv> <termo>
"""
import argparse
import csv
import json
import os
import sys

BASE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

DOMAIN_MAP = {
    "style": "styles.csv",
    "color": "colors.csv",
    "product": "products.csv",
    "typography": "typography.csv",
    "ux": "ux-guidelines.csv",
    "reasoning": "ui-reasoning.csv",
}

MAX_FIELD_LEN = 120  # Truncamento padrão de campos longos


def safe_print(text):
    """Print com fallback para terminais que não suportam Unicode (ex: cp1252)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="replace"))


def _score_row(row, term):
    """Conta quantas colunas da row contêm o termo (case-insensitive)."""
    term_lower = term.lower()
    return sum(1 for v in row.values() if term_lower in str(v).lower())


def _truncate(value, full=False):
    """Trunca o valor se exceder MAX_FIELD_LEN, a não ser que --full."""
    s = str(value)
    if full or len(s) <= MAX_FIELD_LEN:
        return s
    return s[:MAX_FIELD_LEN] + "…"


def search_dataset(filepath, term, full=False):
    """Busca no CSV e retorna lista de (score, row) ordenada por relevância."""
    if not os.path.exists(filepath):
        return []

    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        scored = []
        for row in reader:
            score = _score_row(row, term)
            if score > 0:
                display_row = {k: _truncate(v, full) for k, v in row.items()}
                scored.append((score, display_row))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


def print_results(results, domain_name, term, as_json=False):
    """Imprime resultados formatados ou em JSON."""
    rows = [row for _, row in results]

    if as_json:
        safe_print(json.dumps({"domain": domain_name, "query": term, "count": len(rows), "results": rows}, ensure_ascii=False, indent=2))
        return

    if not rows:
        safe_print(f"  Nenhum resultado em {domain_name} para '{term}'.")
        return

    safe_print(f"\n--- {domain_name} | {len(rows)} resultado(s) para '{term}' ---")
    for row in rows:
        for k, v in row.items():
            safe_print(f"  {k}: {v}")
        safe_print("-" * 40)


def list_domains():
    """Lista todos os domínios disponíveis."""
    print("Domínios disponíveis:\n")
    for domain, csv_file in sorted(DOMAIN_MAP.items()):
        filepath = os.path.join(BASE_DATA_DIR, csv_file)
        exists = "[ok]" if os.path.exists(filepath) else "[--]"
        print(f"  {exists} {domain:12s} -> {csv_file}")
    print("\nUso: python search-uiux.py \"<consulta>\" --domain <dominio>")


def detect_legacy_args(args):
    """Detecta o padrão legado: search-uiux.py <csv> <termo>."""
    if len(args) == 2 and args[0].endswith(".csv"):
        return args[0], args[1]
    return None, None


def main():
    # Detecção de uso legado antes do argparse
    raw_args = sys.argv[1:]
    legacy_csv, legacy_term = detect_legacy_args(raw_args)
    if legacy_csv is not None:
        filepath = os.path.join(BASE_DATA_DIR, legacy_csv)
        results = search_dataset(filepath, legacy_term, full=False)
        print_results(results, legacy_csv, legacy_term)
        return

    parser = argparse.ArgumentParser(
        description="Motor de busca local dos datasets UI/UX.",
        epilog="Domínios: style, color, product, typography, ux, reasoning",
    )
    parser.add_argument("query", nargs="?", help="Termo de busca")
    parser.add_argument("--domain", "-d", choices=list(DOMAIN_MAP.keys()), help="Domínio para filtrar a busca")
    parser.add_argument("--list-domains", action="store_true", help="Lista todos os domínios disponíveis")
    parser.add_argument("--full", "-f", action="store_true", help="Exibe resultado completo sem truncamento")
    parser.add_argument("--json", "-j", action="store_true", dest="as_json", help="Saída em formato JSON")

    args = parser.parse_args()

    if args.list_domains:
        list_domains()
        return

    if not args.query:
        parser.error("É necessário fornecer um termo de busca ou --list-domains.")

    if args.domain:
        # Busca em domínio específico
        csv_file = DOMAIN_MAP[args.domain]
        filepath = os.path.join(BASE_DATA_DIR, csv_file)
        results = search_dataset(filepath, args.query, full=args.full)
        print_results(results, args.domain, args.query, as_json=args.as_json)
    else:
        # Busca em todos os domínios, retorna o de maior relevância
        best_domain = None
        best_results = []
        best_top_score = 0

        all_json_results = {}

        for domain, csv_file in DOMAIN_MAP.items():
            filepath = os.path.join(BASE_DATA_DIR, csv_file)
            results = search_dataset(filepath, args.query, full=args.full)
            if results:
                top_score = results[0][0]
                total_matches = len(results)
                # Prioriza: maior score individual, depois mais resultados
                relevance = (top_score, total_matches)
                if relevance > (best_top_score, len(best_results)):
                    best_top_score = top_score
                    best_results = results
                    best_domain = domain

                if args.as_json:
                    all_json_results[domain] = [row for _, row in results]

        if args.as_json:
            safe_print(json.dumps({
                "query": args.query,
                "best_domain": best_domain,
                "results_by_domain": all_json_results,
            }, ensure_ascii=False, indent=2))
        elif best_domain:
            safe_print(f"[Auto] Domínio mais relevante: {best_domain}")
            print_results(best_results, best_domain, args.query)
        else:
            safe_print(f"Nenhum resultado encontrado para '{args.query}' em nenhum domínio.")


if __name__ == "__main__":
    main()