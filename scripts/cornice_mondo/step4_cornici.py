#!/usr/bin/env python3
"""
Step 4 (cornice_mondo) — 24 cornici nelle 12 storie + tracking refrain.

Legge: scripts/cornice_mondo/_data/cornici_24.yaml (24 cornici, schema DOC_3 §3).

Scrive nel grafo:
  - stories.<sid>.cornice_dettagli: lista oggetti cornice per ogni storia
  - quote_tracker.refrain_animal_used_per_story: append tuple per ogni formula
  - quote_tracker.cantilene_coltivatori_stories: append entry per s08-c1, s09-c2

Idempotente: se already-applied per una storia, no-op (ricontrollo per id cornice).
Backup automatico prima di apply.

Uso:
  python3 scripts/cornice_mondo/step4_cornici.py            # dry-run
  python3 scripts/cornice_mondo/step4_cornici.py --apply    # apply
"""
import argparse
import json
import shutil
import sys
import time
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = REPO_ROOT / "pipeline_narrativa" / "story_graph.json"
DATA_PATH = REPO_ROOT / "scripts" / "cornice_mondo" / "_data" / "cornici_24.yaml"


def load_graph():
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_cornici():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_graph(graph):
    ts = int(time.time())
    backup_path = GRAPH_PATH.with_suffix(f".json.bak.{ts}")
    shutil.copy2(GRAPH_PATH, backup_path)
    print(f"[backup] {backup_path.relative_to(REPO_ROOT)}")
    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)


def add_cornici_to_stories(graph, cornici_data):
    """Aggiunge cornice_dettagli a ogni storia. Idempotente per id cornice."""
    actions = []
    cornici = cornici_data["cornici"]
    by_story = {}
    for c in cornici:
        by_story.setdefault(c["story"], []).append(c)

    for sid, story_cornici in sorted(by_story.items()):
        story = graph["stories"].get(sid)
        if not story:
            actions.append(("error", f"stories.{sid}", "story not found in graph"))
            continue
        existing = story.get("cornice_dettagli", [])
        existing_ids = {c.get("id") for c in existing}
        new_ids = [c["id"] for c in story_cornici if c["id"] not in existing_ids]
        already = [c["id"] for c in story_cornici if c["id"] in existing_ids]
        if new_ids:
            actions.append(("add", f"stories.{sid}.cornice_dettagli", f"adding {new_ids}"))
        if already:
            actions.append(("noop", f"stories.{sid}.cornice_dettagli", f"already present {already}"))
    return actions, by_story


def collect_refrain_tuples(cornici):
    """Estrae le tuple [story, group, animal, type] da quote_tracker_impact."""
    tuples = []
    for c in cornici:
        impact = c.get("quote_tracker_impact")
        if not impact:
            continue
        if "refrain_animal_used_per_story" in impact:
            tup = impact["refrain_animal_used_per_story"]
            tuples.append({"cornice_id": c["id"], "tuple": tup})
    return tuples


def collect_cantilene_entries(cornici):
    """Estrae entry per cantilene_coltivatori_stories."""
    entries = []
    for c in cornici:
        impact = c.get("quote_tracker_impact")
        if not impact:
            continue
        if "cantilene_coltivatori_stories" in impact:
            entries.append({"cornice_id": c["id"], "entry": impact["cantilene_coltivatori_stories"]})
    return entries


def update_quote_tracker(graph, cornici_data, dry_run=True):
    """Aggiorna quote_tracker. Idempotente."""
    actions = []
    cornici = cornici_data["cornici"]
    qt = graph.get("quote_tracker", {})

    refrain_tuples = collect_refrain_tuples(cornici)
    existing_refrain = qt.get("refrain_animal_used_per_story", [])
    existing_keys = {json.dumps(t, sort_keys=True) for t in existing_refrain}
    for item in refrain_tuples:
        tup = item["tuple"]
        key = json.dumps(tup, sort_keys=True)
        if key in existing_keys:
            actions.append(("noop", f"qt.refrain_animal_used_per_story[{item['cornice_id']}]",
                            "tuple already present"))
        else:
            actions.append(("add", f"qt.refrain_animal_used_per_story[{item['cornice_id']}]",
                            f"appending {tup}"))

    cantilene_entries = collect_cantilene_entries(cornici)
    existing_cantilene = qt.get("cantilene_coltivatori_stories", [])
    for item in cantilene_entries:
        entry = item["entry"]
        if entry in existing_cantilene:
            actions.append(("noop", f"qt.cantilene_coltivatori_stories[{item['cornice_id']}]",
                            f"'{entry}' already present"))
        else:
            actions.append(("add", f"qt.cantilene_coltivatori_stories[{item['cornice_id']}]",
                            f"appending '{entry}'"))

    return actions


def append_migration_log_entry(graph):
    log = graph.get("migration_log", [])
    if any(e.get("phase") == "cornice_mondo_step4" for e in log):
        return [("noop", "migration_log", "entry cornice_mondo_step4 already present")]
    return [("append", "migration_log", "entry cornice_mondo_step4")]


def apply_changes(graph, by_story, cornici_data):
    cornici_all = cornici_data["cornici"]

    # Add cornice_dettagli
    for sid, story_cornici in by_story.items():
        story = graph["stories"][sid]
        existing = story.setdefault("cornice_dettagli", [])
        existing_ids = {c.get("id") for c in existing}
        for c in story_cornici:
            if c["id"] not in existing_ids:
                existing.append(c)

    # Update quote_tracker
    qt = graph.setdefault("quote_tracker", {})
    refrain_list = qt.setdefault("refrain_animal_used_per_story", [])
    refrain_existing = {json.dumps(t, sort_keys=True) for t in refrain_list}
    for item in collect_refrain_tuples(cornici_all):
        tup = item["tuple"]
        if json.dumps(tup, sort_keys=True) not in refrain_existing:
            refrain_list.append(tup)

    cantilene_list = qt.setdefault("cantilene_coltivatori_stories", [])
    for item in collect_cantilene_entries(cornici_all):
        entry = item["entry"]
        if entry not in cantilene_list:
            cantilene_list.append(entry)

    graph["last_updated"] = time.strftime("%Y-%m-%d")
    log = graph.setdefault("migration_log", [])
    if not any(e.get("phase") == "cornice_mondo_step4" for e in log):
        log.append({
            "timestamp": time.strftime("%Y-%m-%d"),
            "phase": "cornice_mondo_step4",
            "action": "added 24 cornice_dettagli + extended quote_tracker (refrain + cantilene)",
            "doc_source": "DOC_3_cornici_processi.md",
            "stories_modified": sorted(by_story.keys()),
            "cornici_count": len(cornici_all),
            "additive_only": True,
        })


def print_actions(actions, header):
    print(f"\n=== {header} ===")
    for kind, target, detail in actions:
        marker = {"add": "[+]", "update": "[~]", "noop": "[ ]", "append": "[+]", "error": "[!]"}.get(kind, "[?]")
        print(f"  {marker} {target}: {detail}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply changes (default: dry-run)")
    args = parser.parse_args()
    dry_run = not args.apply

    if not GRAPH_PATH.exists():
        print(f"ERROR: graph not found at {GRAPH_PATH}", file=sys.stderr)
        sys.exit(1)
    if not DATA_PATH.exists():
        print(f"ERROR: data file not found at {DATA_PATH}", file=sys.stderr)
        sys.exit(1)

    graph = load_graph()
    cornici_data = load_cornici()
    cornici = cornici_data["cornici"]

    print(f"[load] graph: {GRAPH_PATH.relative_to(REPO_ROOT)} (schema {graph.get('schema_version')}, graph {graph.get('graph_version')})")
    print(f"[load] cornici: {DATA_PATH.relative_to(REPO_ROOT)} ({len(cornici)} cornici, {len(set(c['story'] for c in cornici))} stories)")

    cornici_actions, by_story = add_cornici_to_stories(graph, cornici_data)
    qt_actions = update_quote_tracker(graph, cornici_data, dry_run=dry_run)
    log_actions = append_migration_log_entry(graph)

    print_actions(cornici_actions, "Cornici per storia")
    print_actions(qt_actions, "Quote tracker (refrain + cantilene)")
    print_actions(log_actions, "Migration log")

    all_actions = cornici_actions + qt_actions + log_actions
    has_changes = any(a[0] not in ("noop", "error") for a in all_actions)
    has_errors = any(a[0] == "error" for a in all_actions)

    if has_errors:
        print("\n[ERROR] aborting due to errors above.", file=sys.stderr)
        sys.exit(2)

    if dry_run:
        print("\n[DRY-RUN] no changes written. Use --apply to write.")
        return
    if not has_changes:
        print("\n[noop] nothing to do.")
        return

    apply_changes(graph, by_story, cornici_data)
    save_graph(graph)
    print(f"\n[applied] cornice_dettagli written to {len(by_story)} stories.")


if __name__ == "__main__":
    main()
