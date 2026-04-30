#!/usr/bin/env python3
"""
Step 6 (cornice_mondo) — popolare world_conventions.path_details.paths con Tier A.

Legge: scripts/cornice_mondo/_data/path_details_tierA.yaml (5 sentieri, 20 dettagli).
Scrive in: world_conventions.path_details.paths.<path_id> = { tier, anatomy, appears_in_stories, details: [...] }

Idempotente per path_id: se path già presente, ricontrollo per detail_id.
Backup automatico prima di apply.

Uso:
  python3 scripts/cornice_mondo/step6_path_details.py            # dry-run
  python3 scripts/cornice_mondo/step6_path_details.py --apply    # apply
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
DATA_PATH = REPO_ROOT / "scripts" / "cornice_mondo" / "_data" / "path_details_tierA.yaml"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply changes (default: dry-run)")
    args = parser.parse_args()
    dry_run = not args.apply

    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        graph = json.load(f)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    paths_data = data["paths"]
    total_details = sum(len(p["details"]) for p in paths_data.values())

    print(f"[load] graph: schema {graph.get('schema_version')}, graph {graph.get('graph_version')}")
    print(f"[load] paths YAML: {len(paths_data)} sentieri Tier A, {total_details} dettagli")

    wc = graph.get("world_conventions", {})
    if "path_details" not in wc:
        print("ERROR: world_conventions.path_details missing. Run Step 1 first.", file=sys.stderr)
        sys.exit(2)
    pd = wc.setdefault("path_details", {})
    paths_existing = pd.setdefault("paths", {})

    actions = []
    for path_id, path_def in paths_data.items():
        if path_id not in paths_existing:
            actions.append(("add", f"path_details.paths.{path_id}",
                            f"creating with {len(path_def['details'])} details"))
        else:
            existing = paths_existing[path_id]
            existing_detail_ids = {d.get("id") for d in existing.get("details", [])}
            for d in path_def["details"]:
                if d["id"] in existing_detail_ids:
                    actions.append(("noop", f"path_details.paths.{path_id}.details",
                                    f"'{d['id']}' already present"))
                else:
                    actions.append(("add", f"path_details.paths.{path_id}.details",
                                    f"appending '{d['id']}'"))

    log_action = "noop"
    if not any(e.get("phase") == "cornice_mondo_step6" for e in graph.get("migration_log", [])):
        log_action = "append"

    print("\n=== path_details Tier A ===")
    for kind, target, detail in actions:
        marker = {"add": "[+]", "noop": "[ ]", "error": "[!]"}.get(kind, "[?]")
        print(f"  {marker} {target}: {detail}")
    print(f"\n  [{'+' if log_action == 'append' else ' '}] migration_log: entry cornice_mondo_step6 ({log_action})")

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
    for path_id, path_def in paths_data.items():
        if path_id not in paths_existing:
            paths_existing[path_id] = {
                "tier": path_def["tier"],
                "anatomy": path_def["anatomy"],
                "appears_in_stories": path_def["appears_in_stories"],
                "details": list(path_def["details"]),
            }
        else:
            existing = paths_existing[path_id]
            existing_details = existing.setdefault("details", [])
            existing_detail_ids = {d.get("id") for d in existing_details}
            for d in path_def["details"]:
                if d["id"] not in existing_detail_ids:
                    existing_details.append(d)

    graph["last_updated"] = time.strftime("%Y-%m-%d")
    log = graph.setdefault("migration_log", [])
    if log_action == "append":
        log.append({
            "timestamp": time.strftime("%Y-%m-%d"),
            "phase": "cornice_mondo_step6",
            "action": f"populated path_details.paths with {len(paths_data)} Tier A sentieri / {total_details} dettagli",
            "doc_source": "DOC_5_index_sentieri.md + DOC_6_mercato_idee_tierA.md",
            "paths_added": sorted(paths_data.keys()),
            "additive_only": True,
        })

    ts = int(time.time())
    backup_path = GRAPH_PATH.with_suffix(f".json.bak.{ts}")
    shutil.copy2(GRAPH_PATH, backup_path)
    print(f"[backup] {backup_path.relative_to(REPO_ROOT)}")
    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"\n[applied] {len(paths_data)} paths Tier A scritti in path_details.paths.")


if __name__ == "__main__":
    main()
