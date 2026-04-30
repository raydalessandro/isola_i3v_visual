#!/usr/bin/env python3
"""
Step 5 (cornice_mondo) — append sentieri "fantasma" a locations_secondary.

Legge: scripts/cornice_mondo/_data/sentieri_fantasma.yaml
Scrive: stories.<sid>.locations_secondary (append idempotente per id).

Uso:
  python3 scripts/cornice_mondo/step5_sentieri_fantasma.py            # dry-run
  python3 scripts/cornice_mondo/step5_sentieri_fantasma.py --apply    # apply
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
    print("ERROR: PyYAML required.", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = REPO_ROOT / "pipeline_narrativa" / "story_graph.json"
DATA_PATH = REPO_ROOT / "scripts" / "cornice_mondo" / "_data" / "sentieri_fantasma.yaml"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply changes (default: dry-run)")
    args = parser.parse_args()
    dry_run = not args.apply

    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        graph = json.load(f)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    mapping = data["mapping"]
    role = data["role_default"]

    print(f"[load] graph: schema {graph.get('schema_version')}, graph {graph.get('graph_version')}")
    print(f"[load] mapping: {len(mapping)} stories, {sum(len(v) for v in mapping.values())} entry totali")

    actions = []
    for sid in sorted(mapping):
        story = graph["stories"].get(sid)
        if not story:
            actions.append(("error", sid, "story not found"))
            continue
        existing = story.get("locations_secondary", [])
        existing_ids = {e.get("id") for e in existing}
        for path_id in mapping[sid]:
            if path_id in existing_ids:
                actions.append(("noop", f"{sid}.locations_secondary", f"'{path_id}' already present"))
            else:
                actions.append(("add", f"{sid}.locations_secondary", f"appending '{path_id}'"))

    log_action = "noop"
    if not any(e.get("phase") == "cornice_mondo_step5" for e in graph.get("migration_log", [])):
        log_action = "append"

    print("\n=== Sentieri fantasma → locations_secondary ===")
    for kind, target, detail in actions:
        marker = {"add": "[+]", "noop": "[ ]", "error": "[!]"}.get(kind, "[?]")
        print(f"  {marker} {target}: {detail}")
    print(f"\n  [{'+' if log_action == 'append' else ' '}] migration_log: entry cornice_mondo_step5 ({log_action})")

    has_changes = any(a[0] == "add" for a in actions) or log_action == "append"
    has_errors = any(a[0] == "error" for a in actions)

    if has_errors:
        print("\n[ERROR] aborting.", file=sys.stderr)
        sys.exit(2)
    if dry_run:
        print("\n[DRY-RUN] no changes written.")
        return
    if not has_changes:
        print("\n[noop] nothing to do.")
        return

    # Apply
    for sid in sorted(mapping):
        story = graph["stories"][sid]
        existing = story.setdefault("locations_secondary", [])
        existing_ids = {e.get("id") for e in existing}
        for path_id in mapping[sid]:
            if path_id not in existing_ids:
                existing.append({"id": path_id, "role": role})

    graph["last_updated"] = time.strftime("%Y-%m-%d")
    log = graph.setdefault("migration_log", [])
    if log_action == "append":
        added_count = sum(1 for a in actions if a[0] == "add")
        log.append({
            "timestamp": time.strftime("%Y-%m-%d"),
            "phase": "cornice_mondo_step5",
            "action": f"appended {added_count} sentieri fantasma to locations_secondary",
            "doc_source": "DOC_4_audit_sentieri.md §4",
            "stories_modified": sorted(mapping.keys()),
            "additive_only": True,
        })

    ts = int(time.time())
    backup_path = GRAPH_PATH.with_suffix(f".json.bak.{ts}")
    shutil.copy2(GRAPH_PATH, backup_path)
    print(f"[backup] {backup_path.relative_to(REPO_ROOT)}")
    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"\n[applied] sentieri fantasma scritti.")


if __name__ == "__main__":
    main()
