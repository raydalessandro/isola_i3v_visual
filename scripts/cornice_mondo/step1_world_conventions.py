#!/usr/bin/env python3
"""
Step 1+2 (cornice_mondo) — world_conventions root + quote_tracker extension.

Aggiunge nodo radice 'world_conventions' al grafo:
  - refrain_animal_identification (DOC_1): formula sg+pl, vincoli, pool, attivazione
  - path_details (placeholder): { paths: {} } popolato da Step 6

Estende quote_tracker:
  - refrain_animal_used_per_story: [] (popolato da Step 4)

Bumpa graph_version: 1.1.0 -> 1.2.0 (additivo).
Bumpa schema_version: 1.3 -> 1.4 (additivo: nuovo nodo root).

Idempotente: se already-applied, no-op + log.
Backup automatico: story_graph.json.bak.<ts> prima di modificare.

Uso:
  python3 scripts/cornice_mondo/step1_world_conventions.py            # dry-run di default
  python3 scripts/cornice_mondo/step1_world_conventions.py --apply    # scrive davvero
"""
import argparse
import json
import shutil
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = REPO_ROOT / "pipeline_narrativa" / "story_graph.json"
DATA_DIR = REPO_ROOT / "scripts" / "cornice_mondo" / "_data"


def load_graph():
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_graph(graph, dry_run):
    if dry_run:
        return
    ts = int(time.time())
    backup_path = GRAPH_PATH.with_suffix(f".json.bak.{ts}")
    shutil.copy2(GRAPH_PATH, backup_path)
    print(f"[backup] {backup_path.relative_to(REPO_ROOT)}")
    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)


def build_world_conventions():
    """Costruisce il blocco world_conventions da DOC_1 (decisioni autoriali)."""
    return {
        "refrain_animal_identification": {
            "doc_source": "DOC_1_formula_ritornello.md",
            "approved_date": "2026-04-30",
            "formula": {
                "singular": "Era un/una <ruolo del gruppo> — quale, oggi? Una/Un <animale>.",
                "plural": "Erano i/le <gruppo> — chi, oggi? Una/Un <animale>, una/un <animale>, una/un <animale>.",
            },
            "groups_eligible": [
                "camminanti",
                "mantenitori",
                "coltivatori_del_cerchio",
                "mercato_del_mezzogiorno",
                "pastori",
                "pescatori_case_basse",
            ],
            "excluded_targets": {
                "named_characters": "Mai ai personaggi nominati. La specie loro è canone.",
                "vecchie_del_mercato": "Mai. Restano coralità silenziosa.",
                "cuccioli_protagonisti": "Mai (Pun, Toba, Bru, Cardo, Liù).",
            },
            "activation_rules": {
                "primo_incontro_only": True,
                "max_formule_per_story": 2,
                "max_plurale_per_story": 1,
                "tre_nomi_in_plurale": True,
                "almeno_uno_insolito_in_plurale": True,
                "paesaggio_omittibile": True,
            },
            "quotes_saga": {
                "max_per_story": 2,
                "unique_animal_saga": True,
                "stagionalita_rispettata": True,
            },
            "typography": {
                "position": "inline_paragrafo",
                "pause": "trattino_lungo",
                "variations_allowed_after_first": "4-5 incontri",
                "max_variants_in_late_stories": 2,
            },
            "pool_excluded_priori": [
                "volpe_rossa", "airone_cenerino", "riccio_adulto", "tartaruga_di_mare_anziana",
                "tasso", "tassino", "stambecco_verde_vecchio", "lepre", "picchio",
                "cormorano", "scoiattolo_grigio_anziano", "riccino", "tartarughina",
                "lupacchiotto", "libellulina",
            ],
            "pool_available": {
                "mammiferi_piccoli": ["talpa", "donnola", "faina", "ermellino", "arvicola", "ghiro", "marmotta"],
                "mammiferi_medi": ["volpe_argentata", "volpe_della_sabbia", "cinghialino", "capriolo", "daino"],
                "domestici_lavoro": ["capra", "pecora", "asino", "mulo", "cane_da_pastore"],
                "uccelli": ["allodola", "pettirosso", "fringuello", "capinera", "rondine", "rondine_di_mare",
                            "gazza", "cornacchia", "tortora", "poiana", "gheppio"],
                "anfibi_rettili_max_1_2": ["rospo", "rana_di_palude", "ramarro", "lucertola"],
            },
        },
        "path_details": {
            "doc_source": "DOC_5_index_sentieri.md + DOC_6_mercato_idee_tierA.md",
            "schema_note": "campo `tipo` rimosso dallo slot dettaglio — un dettaglio è un dettaglio, libero",
            "paths": {},  # popolato da Step 6
        },
    }


def step1_add_world_conventions(graph):
    """Aggiunge nodo world_conventions. Idempotente."""
    actions = []
    if "world_conventions" in graph:
        existing_keys = sorted(graph["world_conventions"].keys())
        actions.append(("noop", "world_conventions", f"already present (keys: {existing_keys})"))
    else:
        actions.append(("add", "world_conventions", "creating root node with refrain_animal_identification + path_details"))
    return actions


def step2_extend_quote_tracker(graph):
    """Aggiunge refrain_animal_used_per_story al quote_tracker. Idempotente."""
    actions = []
    qt = graph.get("quote_tracker", {})
    if "refrain_animal_used_per_story" in qt:
        actions.append(("noop", "quote_tracker.refrain_animal_used_per_story", "already present"))
    else:
        actions.append(("add", "quote_tracker.refrain_animal_used_per_story", "initializing as []"))
    return actions


def bump_versions(graph):
    """Bump graph_version 1.1.0 -> 1.2.0, schema_version 1.3 -> 1.4."""
    actions = []
    cur_graph = graph.get("graph_version")
    cur_schema = graph.get("schema_version")
    if cur_graph != "1.2.0":
        actions.append(("update", "graph_version", f"{cur_graph} -> 1.2.0"))
    else:
        actions.append(("noop", "graph_version", "already 1.2.0"))
    if cur_schema != 1.4:
        actions.append(("update", "schema_version", f"{cur_schema} -> 1.4"))
    else:
        actions.append(("noop", "schema_version", "already 1.4"))
    return actions


def append_migration_log(graph):
    """Aggiunge entry al migration_log."""
    log = graph.get("migration_log", [])
    entry = {
        "timestamp": time.strftime("%Y-%m-%d"),
        "phase": "cornice_mondo_step1_2",
        "action": "added world_conventions root + extended quote_tracker.refrain_animal_used_per_story",
        "doc_sources": ["DOC_1_formula_ritornello.md", "DOC_5_index_sentieri.md"],
        "graph_version_bump": "1.1.0 -> 1.2.0",
        "schema_version_bump": "1.3 -> 1.4",
        "additive_only": True,
    }
    if any(e.get("phase") == "cornice_mondo_step1_2" for e in log):
        return [("noop", "migration_log", "entry cornice_mondo_step1_2 already present")]
    return [("append", "migration_log", "entry cornice_mondo_step1_2")]


def apply_changes(graph):
    """Applica le modifiche in-place. Idempotente."""
    if "world_conventions" not in graph:
        graph["world_conventions"] = build_world_conventions()
    qt = graph.setdefault("quote_tracker", {})
    if "refrain_animal_used_per_story" not in qt:
        qt["refrain_animal_used_per_story"] = []
    graph["graph_version"] = "1.2.0"
    graph["schema_version"] = 1.4
    graph["last_updated"] = time.strftime("%Y-%m-%d")
    log = graph.setdefault("migration_log", [])
    if not any(e.get("phase") == "cornice_mondo_step1_2" for e in log):
        log.append({
            "timestamp": time.strftime("%Y-%m-%d"),
            "phase": "cornice_mondo_step1_2",
            "action": "added world_conventions root + extended quote_tracker.refrain_animal_used_per_story",
            "doc_sources": ["DOC_1_formula_ritornello.md", "DOC_5_index_sentieri.md"],
            "graph_version_bump": "1.1.0 -> 1.2.0",
            "schema_version_bump": "1.3 -> 1.4",
            "additive_only": True,
        })


def print_actions(actions, header):
    print(f"\n=== {header} ===")
    for kind, target, detail in actions:
        marker = {"add": "[+]", "update": "[~]", "noop": "[ ]", "append": "[+]"}.get(kind, "[?]")
        print(f"  {marker} {target}: {detail}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply changes (default: dry-run)")
    args = parser.parse_args()
    dry_run = not args.apply

    if not GRAPH_PATH.exists():
        print(f"ERROR: graph not found at {GRAPH_PATH}", file=sys.stderr)
        sys.exit(1)

    graph = load_graph()
    print(f"[load] {GRAPH_PATH.relative_to(REPO_ROOT)}")
    print(f"  schema_version: {graph.get('schema_version')}")
    print(f"  graph_version:  {graph.get('graph_version')}")
    print(f"  stories:        {len(graph.get('stories', {}))}")

    all_actions = []
    all_actions.extend(step1_add_world_conventions(graph))
    all_actions.extend(step2_extend_quote_tracker(graph))
    all_actions.extend(bump_versions(graph))
    all_actions.extend(append_migration_log(graph))

    print_actions(step1_add_world_conventions(graph), "Step 1 — world_conventions")
    print_actions(step2_extend_quote_tracker(graph), "Step 2 — quote_tracker extension")
    print_actions(bump_versions(graph), "Version bump")
    print_actions(append_migration_log(graph), "Migration log")

    has_changes = any(a[0] != "noop" for a in all_actions)

    if dry_run:
        print("\n[DRY-RUN] no changes written. Use --apply to write.")
        return

    if not has_changes:
        print("\n[noop] nothing to do, graph already up to date — skip save.")
        return

    apply_changes(graph)
    save_graph(graph, dry_run=False)
    print(f"\n[applied] graph_version: {graph['graph_version']}, schema_version: {graph['schema_version']}")


if __name__ == "__main__":
    main()
