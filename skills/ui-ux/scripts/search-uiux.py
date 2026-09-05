#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Engine Search - motor de busca por relevancia para os datasets locais
da skill `ui-ux` (adaptacao enxuta do ui-ux-pro-max-skill para este plugin).

Uso:
  python search-uiux.py "<consulta>"
  python search-uiux.py "<consulta>" --domain style
  python search-uiux.py "<consulta>" --domain color --max-results 5
  python search-uiux.py "<consulta>" --json
  python search-uiux.py "<consulta>" --full
  python search-uiux.py --list-domains

Dominios disponiveis (arquivo em skills/ui-ux/data/):
  style       -> styles.csv           (linguagem visual: minimalista, brutalista, glass...)
  color       -> colors.csv           (paletas semanticas por tipo de produto)
  product     -> products.csv         (recomendacao de estilo por tipo de produto)
  typography  -> typography.csv       (pares de fonte, heading/body, mood)
  ux          -> ux-guidelines.csv    (usabilidade, do/don't, severidade)
  reasoning   -> ui-reasoning.csv     (regras de decisao e anti-padroes)

Sem --domain, a consulta e' rodada em todos os datasets e o dominio com maior
pontuacao de relevancia e' escolhido automaticamente (auto-detected), com o
vice-lider informado quando houver empate proximo.

No dominio `reasoning`, alem da busca textual, cada resultado tem sua coluna
Decision_Rules (JSON de condicao -> acoes) interpretada contra a consulta —
condicoes como `if_checkout` ou `if_dashboard` sao disparadas se a consulta
contiver os sinais correspondentes (ex.: "checkout", "pagamento"), e
`must_have` sempre se aplica. Isso reproduz, de forma enxuta, o papel do
reasoning_contract.py do ui-ux-pro-max-skill original.

Uso legado (retrocompatível, mantido para quem ja tinha scripts/atalhos com
a sintaxe antiga de 2 argumentos posicionais):
  python search-uiux.py <dataset.csv> <termo>
"""

import argparse
import csv
import difflib
import io
import json as json_module
import sys
from pathlib import Path

# Forca UTF-8 no stdout/stderr (evita quebra de acentuacao no Windows/cp1252)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

BASE_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MAX_RESULTS_DEFAULT = 5
TRUNCATE_AT = 300

# Sinais de condicao (portado do reasoning_contract.py do ui-ux-pro-max-skill
# oficial): mapeia uma condicao ("if_checkout") para palavras-chave que, se
# presentes na consulta, a disparam. Usado só para leitura do Decision_Rules
# do dataset reasoning — nao e' um parser genérico, so o vocabulario de sinais.
CONDITION_SIGNALS = {
    "if_booking": ("booking", "appointment", "calendar", "agendamento", "reserva"),
    "if_boutique": ("boutique",),
    "if_casual": ("casual", "playful", "descontraido"),
    "if_checkout": ("checkout", "payment", "purchase", "pagamento", "compra"),
    "if_children": ("child", "children", "kids", "crianca", "infantil"),
    "if_collaboration": ("collaboration", "multiplayer", "co-edit", "colaboracao"),
    "if_competitive": ("competitive", "leaderboard", "ranking"),
    "if_content_focused": ("content", "article", "reading", "documentation", "conteudo", "artigo", "blog"),
    "if_conversion_focused": ("conversion", "sales", "signup", "purchase", "conversao", "venda", "cadastro"),
    "if_creative_field": ("creative", "artist", "portfolio", "criativo", "portfolio"),
    "if_crop_focused": ("crop", "farm", "agriculture", "agricultura"),
    "if_dashboard": ("dashboard", "operations", "monitoring", "painel"),
    "if_data_heavy": ("data heavy", "data-heavy", "analytics", "large dataset", "muitos dados"),
    "if_delivery": ("delivery", "courier", "shipping", "entrega"),
    "if_discovery_focused": ("discover", "discovery", "browse", "directory", "descoberta", "explorar"),
    "if_engagement_metric": ("engagement", "retention", "contribution", "engajamento", "retencao"),
    "if_experience_focused": ("experience", "immersive", "journey", "experiencia", "imersivo"),
    "if_gamification": ("gamification", "badges", "streak", "gamificacao"),
    "if_health": ("health", "medical", "patient", "saude", "medico", "paciente"),
    "if_hero_needed": ("hero", "showcase", "launch", "lancamento"),
    "if_large_dataset": ("large dataset", "thousands", "millions", "grande volume"),
    "if_light_mode_needed": ("light mode", "light theme", "modo claro"),
    "if_low_performance": ("low performance", "low-end", "slow device", "dispositivo fraco"),
    "if_luxury": ("luxury", "premium", "high-end", "luxo", "premium"),
    "if_medication": ("medication", "medicine", "prescription", "medicamento", "receita"),
    "if_meditation": ("meditation", "breathing", "mindfulness", "meditacao"),
    "if_minimal_portfolio": ("minimal portfolio", "simple portfolio", "portfolio simples"),
    "if_mobile": ("mobile", "phone", "tablet", "ios", "android", "celular"),
    "if_personalized": ("personalized", "personalised", "recommendation", "personalizado", "recomendacao"),
    "if_pre_launch": ("pre-launch", "prelaunch", "coming soon", "waitlist", "lista de espera"),
    "if_salary_focused": ("salary", "compensation", "pay range", "salario"),
    "if_team_collaboration": ("team collaboration", "team workspace", "colaboracao em equipe"),
    "if_trust_needed": ("trust", "secure", "verified", "authority", "confianca", "seguranca"),
    "if_ux_focused": ("ux", "usability", "accessibility", "accessible", "usabilidade", "acessibilidade"),
    "if_video_ready": ("video ready", "product video", "demo video", "video pronto"),
}

# Colunas que nunca devem ser truncadas (checklists, snippets, imports)
UNTRUNCATED_COLS = {
    "Implementation Checklist",
    "Design System Variables",
    "CSS Import",
    "Tailwind Config",
    "Code Example Good",
    "Code Example Bad",
    "Decision_Rules",
    "Anti_Patterns",
}

# Mapeamento dominio -> arquivo + colunas de busca (o que conta pra relevancia)
# + colunas priorizadas na saida quando o registro tem muitas colunas.
DOMAIN_CONFIG = {
    "style": {
        "file": "styles.csv",
        "search_cols": [
            "Style Category", "Type", "Keywords", "Best For", "Do Not Use For",
            "AI Prompt Keywords", "CSS/Technical Keywords", "Aliases", "Era/Origin",
        ],
        "priority_cols": [
            "Style Category", "Type", "Keywords", "Primary Colors", "Secondary Colors",
            "Effects & Animation", "Best For", "Do Not Use For", "Light Mode ✓",
            "Dark Mode ✓", "Performance", "Accessibility", "Mobile-Friendly",
            "Conversion-Focused", "Framework Compatibility", "Complexity",
            "Implementation Checklist", "Design System Variables",
        ],
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["Product Type", "Notes"],
        "priority_cols": [
            "Product Type", "Primary", "On Primary", "Secondary", "On Secondary",
            "Accent", "On Accent", "Background", "Foreground", "Card",
            "Card Foreground", "Muted", "Muted Foreground", "Border",
            "Destructive", "On Destructive", "Ring", "Notes",
        ],
    },
    "product": {
        "file": "products.csv",
        "search_cols": [
            "Product Type", "Keywords", "Primary Style Recommendation", "Key Considerations",
        ],
        "priority_cols": [
            "Product Type", "Keywords", "Primary Style Recommendation", "Secondary Styles",
            "Landing Page Pattern", "Dashboard Style (if applicable)", "Color Palette Focus",
            "Key Considerations",
        ],
    },
    "typography": {
        "file": "typography.csv",
        "search_cols": [
            "Font Pairing Name", "Category", "Mood/Style Keywords", "Best For",
            "Heading Font", "Body Font",
        ],
        "priority_cols": [
            "Font Pairing Name", "Category", "Heading Font", "Body Font",
            "Mood/Style Keywords", "Best For", "Google Fonts URL", "CSS Import",
            "Tailwind Config", "Notes",
        ],
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["Category", "Issue", "Description", "Platform"],
        "priority_cols": [
            "Category", "Issue", "Platform", "Description", "Do", "Don't",
            "Code Example Good", "Code Example Bad", "Severity",
        ],
    },
    "reasoning": {
        "file": "ui-reasoning.csv",
        "search_cols": [
            "UI_Category", "Recommended_Pattern", "Decision_Rules",
            "Anti_Patterns", "Reasoning",
        ],
        "priority_cols": [
            "UI_Category", "Recommended_Pattern", "Style_Priority", "Color_Mood",
            "Typography_Mood", "Key_Effects", "Decision_Rules", "Anti_Patterns",
            "Severity", "Reasoning", "Confidence",
        ],
    },
}

# Sinonimos/aliases em PT-BR e variacoes comuns -> chave canonica do dominio
DOMAIN_ALIASES = {
    "style": "style", "styles": "style", "estilo": "style", "estilos": "style",
    "color": "color", "colors": "color", "cor": "color", "cores": "color", "paleta": "color",
    "product": "product", "products": "product", "produto": "product", "produtos": "product",
    "typography": "typography", "tipografia": "typography", "font": "typography", "fonte": "typography",
    "ux": "ux", "usabilidade": "ux", "guidelines": "ux",
    "reasoning": "reasoning", "raciocinio": "reasoning", "decisao": "reasoning",
}


def resolve_domain(name):
    if not name:
        return None
    key = DOMAIN_ALIASES.get(name.strip().lower())
    if key is None:
        raise SystemExit(
            f"Dominio '{name}' desconhecido. Use --list-domains para ver as opcoes."
        )
    return key


def load_dataset(domain_key):
    """Carrega um dataset CSV como lista de dicts. Lanca erro claro se ausente."""
    config = DOMAIN_CONFIG[domain_key]
    filepath = BASE_DATA_DIR / config["file"]
    if not filepath.exists():
        available = ", ".join(sorted(BASE_DATA_DIR.glob("*.csv") and
                                      [p.name for p in BASE_DATA_DIR.glob("*.csv")]))
        raise SystemExit(
            f"Dataset '{config['file']}' nao encontrado em {BASE_DATA_DIR}.\n"
            f"Arquivos .csv disponiveis: {available or '(nenhum encontrado)'}"
        )
    # utf-8-sig lida com BOM; newline='' evita duplicar quebras de linha no Windows
    with open(filepath, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def score_row(row, terms, search_cols):
    """Pontua uma linha por numero de termos encontrados (case-insensitive),
    somando ocorrencias multiplas nas colunas relevantes para a busca."""
    haystacks = [str(row.get(col, "")).lower() for col in search_cols if col in row]
    if not haystacks:
        # fallback: se as colunas configuradas nao existem no CSV (schema mudou),
        # busca em todas as colunas para nao falhar silenciosamente.
        haystacks = [str(v).lower() for v in row.values()]
    joined = " \u241f ".join(haystacks)  # separador improvavel de colidir
    score = 0
    for term in terms:
        score += joined.count(term)
    return score


def search_domain(domain_key, terms, max_results):
    config = DOMAIN_CONFIG[domain_key]
    rows = load_dataset(domain_key)
    scored = []
    for row in rows:
        s = score_row(row, terms, config["search_cols"])
        if s > 0:
            scored.append((s, row))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    top = scored[:max_results]
    return {
        "domain": domain_key,
        "file": config["file"],
        "count": len(scored),
        "results": [row for _, row in top],
    }


def apply_decision_rules(row, query_text):
    """Le a coluna Decision_Rules (JSON de condicao -> acoes) de uma linha do
    dataset `reasoning` e retorna as regras cujo gatilho bate com a consulta.
    Ex.: {"if_checkout": ["constraint:emphasize-trust"]} dispara se a consulta
    contiver "checkout"/"pagamento"/"compra"."""
    raw = row.get("Decision_Rules", "")
    if not raw or not raw.strip():
        return []
    try:
        rules = json_module.loads(raw)
    except (json_module.JSONDecodeError, TypeError):
        return []
    if not isinstance(rules, dict):
        return []

    query_lower = query_text.lower()
    triggered = []
    for condition, actions in rules.items():
        if condition == "must_have":
            # regra incondicional do dataset oficial: sempre se aplica, sem gatilho de texto.
            triggered.append((condition, actions, True))
            continue
        signals = CONDITION_SIGNALS.get(condition)
        if signals is None:
            # condicao nao catalogada (dataset pode ter evoluido) - reporta mesmo assim,
            # sem gatilho verificavel, para nao esconder informacao.
            triggered.append((condition, actions, None))
            continue
        if any(signal in query_lower for signal in signals):
            triggered.append((condition, actions, True))
    return triggered


def suggest_terms(domain_key, terms):
    """Sugere termos proximos usando difflib contra o vocabulario das colunas
    de busca do dominio, para orientar uma nova tentativa."""
    config = DOMAIN_CONFIG[domain_key]
    rows = load_dataset(domain_key)
    vocab = set()
    for row in rows:
        for col in config["search_cols"]:
            val = row.get(col, "")
            for token in str(val).replace(",", " ").replace(";", " ").split():
                token = token.strip().strip(".:()[]\"'").lower()
                if len(token) > 2:
                    vocab.add(token)
    suggestions = []
    for term in terms:
        suggestions.extend(difflib.get_close_matches(term, vocab, n=3, cutoff=0.75))
    # remove duplicatas preservando ordem
    seen = set()
    out = []
    for s in suggestions:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out[:5]


def format_row(row, config, full):
    lines = []
    cols = [c for c in config["priority_cols"] if c in row] or list(row.keys())
    for col in cols:
        value = str(row.get(col, "")).strip()
        if not value:
            continue
        if not full and col not in UNTRUNCATED_COLS and len(value) > TRUNCATE_AT:
            value = value[:TRUNCATE_AT] + "..."
        lines.append(f"- **{col}:** {value}")
    return "\n".join(lines)


def format_output(result, query, full=False, auto_detected=False, runner_up=None):
    config = DOMAIN_CONFIG[result["domain"]]
    out = ["## UI/UX Engine — Resultado da busca"]
    domain_note = result["domain"]
    if auto_detected:
        domain_note += " (auto-detectado"
        if runner_up:
            domain_note += f", segundo colocado: {runner_up}"
        domain_note += ")"
    out.append(f"**Dominio:** {domain_note} | **Consulta:** {query}")
    out.append(f"**Fonte:** {config['file']} | **Encontrados:** {result['count']}\n")

    if result["count"] == 0:
        out.append(
            "Nenhum resultado. Isto NAO e' um valor vazio — a consulta nao bateu "
            "com nada no dataset. Tente termos mais amplos ou diferentes antes de "
            "recorrer a um padrao generico, e avise explicitamente que a base nao "
            "retornou nada caso caia no fallback."
        )
        suggestions = suggest_terms(result["domain"], query.lower().split())
        if suggestions:
            out.append(f"**Termos proximos na base:** {', '.join(suggestions)}")
        return "\n".join(out)

    for i, row in enumerate(result["results"], 1):
        out.append(f"### Resultado {i}")
        out.append(format_row(row, config, full))
        if result["domain"] == "reasoning":
            triggered = apply_decision_rules(row, query)
            if triggered:
                out.append("- **Regras condicionais acionadas por esta consulta:**")
                for condition, actions, verified in triggered:
                    actions_str = ", ".join(actions) if isinstance(actions, list) else str(actions)
                    if condition == "must_have":
                        tag = " (sempre aplicavel)"
                    elif verified:
                        tag = ""
                    else:
                        tag = " (condicao nao catalogada — revisar manualmente)"
                    out.append(f"  - `{condition}` → {actions_str}{tag}")
        out.append("")

    return "\n".join(out)


def run_all_domains(terms, max_results):
    """Roda a busca em todos os dominios e escolhe o melhor por pontuacao total."""
    per_domain = {}
    for key in DOMAIN_CONFIG:
        try:
            rows = load_dataset(key)
        except SystemExit:
            continue
        config = DOMAIN_CONFIG[key]
        total_score = sum(score_row(r, terms, config["search_cols"]) for r in rows)
        per_domain[key] = total_score

    ranked = sorted(per_domain.items(), key=lambda kv: kv[1], reverse=True)
    if not ranked or ranked[0][1] == 0:
        # nenhum dominio bateu; ainda assim devolve o primeiro pra mostrar "0 resultados"
        best = next(iter(DOMAIN_CONFIG))
        return search_domain(best, terms, max_results), False, None

    best_domain = ranked[0][0]
    runner_up = ranked[1][0] if len(ranked) > 1 and ranked[1][1] > 0 else None
    return search_domain(best_domain, terms, max_results), True, runner_up


def list_domains():
    print("Dominios disponiveis:\n")
    for key, cfg in DOMAIN_CONFIG.items():
        path = BASE_DATA_DIR / cfg["file"]
        status = "OK" if path.exists() else "AUSENTE"
        print(f"  {key:<11} -> data/{cfg['file']:<20} [{status}]")


def detect_legacy_args(raw_args):
    """Detecta o padrao legado de 2 argumentos posicionais: <dataset.csv> <termo>.
    Mantido por retrocompatibilidade com quem memorizou a sintaxe antiga."""
    if len(raw_args) == 2 and raw_args[0].endswith(".csv") and not raw_args[0].startswith("-"):
        return raw_args[0], raw_args[1]
    return None, None


def run_legacy(csv_filename, term):
    """Busca legada num arquivo CSV especifico por nome de arquivo (nao por
    dominio). Reaproveita o mesmo scoring/formatacao do modo atual quando o
    arquivo bate com um dominio conhecido; caso contrario, faz fallback para
    varredura simples do arquivo indicado."""
    matching_domain = next(
        (key for key, cfg in DOMAIN_CONFIG.items() if cfg["file"] == csv_filename),
        None,
    )
    terms = [t.lower() for t in term.split() if t.strip()]
    if matching_domain:
        result = search_domain(matching_domain, terms, MAX_RESULTS_DEFAULT)
        print(format_output(result, term, full=False, auto_detected=False, runner_up=None))
        return

    filepath = BASE_DATA_DIR / csv_filename
    if not filepath.exists():
        raise SystemExit(f"Dataset '{csv_filename}' nao encontrado em {BASE_DATA_DIR}.")
    with open(filepath, mode="r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    scored = [(score_row(r, terms, list(r.keys())), r) for r in rows]
    scored = [(s, r) for s, r in scored if s > 0]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    if not scored:
        print(f"Nenhum resultado em {csv_filename} para '{term}'.")
        return
    for i, (_, row) in enumerate(scored[:MAX_RESULTS_DEFAULT], 1):
        print(f"### Resultado {i}")
        for col, val in row.items():
            val = str(val).strip()
            if val:
                print(f"- **{col}:** {val}")
        print()


if __name__ == "__main__":
    _legacy_csv, _legacy_term = detect_legacy_args(sys.argv[1:])
    if _legacy_csv is not None:
        run_legacy(_legacy_csv, _legacy_term)
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description="Busca por relevancia nos datasets da skill ui-ux (local, sem dependencias externas)."
    )
    parser.add_argument("query", nargs="?", help="Termo(s) de busca")
    parser.add_argument("--domain", "-d", type=str, default=None,
                         help="Restringe a busca a um dominio: " + ", ".join(sorted(set(DOMAIN_CONFIG.keys()))))
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS_DEFAULT,
                         help=f"Numero maximo de resultados (padrao: {MAX_RESULTS_DEFAULT})")
    parser.add_argument("--json", action="store_true", help="Saida em JSON")
    parser.add_argument("--full", action="store_true", help="Nao truncar valores longos na saida em texto")
    parser.add_argument("--list-domains", action="store_true", help="Lista os dominios/datasets disponiveis e sai")

    args = parser.parse_args()

    if args.list_domains:
        list_domains()
        sys.exit(0)

    if not args.query:
        parser.error("informe uma consulta, ex.: python search-uiux.py \"dashboard saas dark mode\"")

    terms = [t.lower() for t in args.query.split() if t.strip()]
    if not terms:
        parser.error("consulta vazia apos normalizacao")

    domain_key = resolve_domain(args.domain)

    if domain_key:
        result = search_domain(domain_key, terms, args.max_results)
        auto_detected, runner_up = False, None
    else:
        result, auto_detected, runner_up = run_all_domains(terms, args.max_results)

    if args.json:
        payload = dict(result)
        payload["auto_detected"] = auto_detected
        payload["runner_up_domain"] = runner_up
        if result["domain"] == "reasoning":
            for row in payload["results"]:
                triggered = apply_decision_rules(row, args.query)
                row["_triggered_decision_rules"] = [
                    {"condition": c, "actions": a, "verified": v} for c, a, v in triggered
                ]
        print(json_module.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(format_output(result, args.query, full=args.full,
                             auto_detected=auto_detected, runner_up=runner_up))