#!/usr/bin/env python3
"""
Step 8 (cornice_mondo) — Allinea i riferimenti canonici nel grafo agli id
ufficiali del catalogo. Risolve le 7 incoerenze note nella baseline
`scripts/audit/_data/known_issues.yaml`.

Autorizzazione Ray (2026-06-10): "uniformiamoli, va bene? Non c'è problema."
Scelta operativa: id canonici del catalogo (meno lavoro, meno rotture).

Modifiche al grafo (additive/rinomi puntuali, schema invariato per il 99%):

  1. Cornici foresta (s02_c2, s03_c2, s04_c2, s07_c2):
     where.location_id: "margine_foresta_intrecciata" -> "foresta_intrecciata"
     (qualifier originale invariato — già descrive il margine)

  2. Cornice pontile (s06_c2):
     where.location_id: "pontile" -> "pontile_bocca"

  3. Storia s06:
     location_primary.id: "centro_villaggio" -> "villaggio_centrale"

  4. Cornice s05_c2 (Pun + Mèmolo insieme):
     who: { kind: "nominato", ref: "pun_e_memolo", ... }
     ->  who: { kind: "nominati", ref: null, refs: ["pun","memolo"], ... }
     (estensione additiva schema: `refs` lista, kind plurale)

Idempotente: rieseguendo, se le modifiche sono già applicate, esce no-op.
Backup automatico: pipeline_narrativa/story_graph.json.pre_step8_canonical_refs.backup.json
Migration log: aggiunge entry "cornice_mondo_step8".

Dopo l'applicazione:
  - svuotare scripts/audit/_data/known_issues.yaml (issues: [])
  - aggiornare manifest backup: python3 scripts/audit/audit_1_integrity.py --update-manifest

Uso:
  python3 scripts/cornice_mondo/step8_fix_canonical_refs.py            # dry-run
  python3 scripts/cornice_mondo/step8_fix_canonical_refs.py --apply    # apply
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPH_PATH = REPO_ROOT / "pipeline_narrativa" / "story_graph.json"
BACKUP_PATH = REPO_ROOT / "pipeline_narrativa" / "story_graph.json.pre_step8_canonical_refs.backup.json"

# Le 4 cornici foresta (location_id da rinominare)
FORESTA_CORNICI = [("s02", "s02_c2"), ("s03", "s03_c2"), ("s04", "s04_c2"), ("s07", "s07_c2")]


def find_cornice(story: dict, cid: str) -> dict | None:
    for c in story.get("cornice_dettagli", []) or []:
        if c.get("id") == cid:
            return c
    return None


def apply_fixes(g: dict) -> tuple[int, list[str]]:
    """Ritorna (n_modifiche, log_umano)."""
    n = 0
    log: list[str] = []

    # 1) Foreste — location_id
    for sid, cid in FORESTA_CORNICI:
        c = find_cornice(g["stories"].get(sid, {}), cid)
        if c and c.get("where", {}).get("location_id") == "margine_foresta_intrecciata":
            c["where"]["location_id"] = "foresta_intrecciata"
            n += 1
            log.append(f"  {cid}: where.location_id -> foresta_intrecciata")

    # 2) Pontile s06_c2
    c = find_cornice(g["stories"].get("s06", {}), "s06_c2")
    if c and c.get("where", {}).get("location_id") == "pontile":
        c["where"]["location_id"] = "pontile_bocca"
        n += 1
        log.append("  s06_c2: where.location_id -> pontile_bocca")

    # 3) location_primary s06
    s06 = g["stories"].get("s06", {})
    lp = s06.get("location_primary")
    if isinstance(lp, dict) and lp.get("id") == "centro_villaggio":
        lp["id"] = "villaggio_centrale"
        n += 1
        log.append("  s06.location_primary.id -> villaggio_centrale")

    # 4) s05_c2.who: ref composito -> refs lista
    c = find_cornice(g["stories"].get("s05", {}), "s05_c2")
    if c:
        who = c.get("who") or {}
        if who.get("ref") == "pun_e_memolo":
            who["kind"] = "nominati"
            who["ref"] = None
            who["refs"] = ["pun", "memolo"]
            n += 1
            log.append("  s05_c2.who: ref 'pun_e_memolo' -> kind 'nominati' + refs ['pun','memolo']")

    return n, log


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="scrivi le modifiche (default: dry-run)")
    args = ap.parse_args()

    if not GRAPH_PATH.exists():
        print(f"ERRORE: grafo non trovato in {GRAPH_PATH}", file=sys.stderr)
        return 1

    g = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    n, log = apply_fixes(g)

    print(f"== step8_fix_canonical_refs ({'APPLY' if args.apply else 'DRY-RUN'}) ==")
    if n == 0:
        print("  Nessuna modifica necessaria — grafo gia' allineato (idempotente).")
        return 0

    print(f"  {n} modifiche da applicare:")
    for line in log:
        print(line)

    if not args.apply:
        print("\n  (dry-run) — usa --apply per scrivere.")
        return 0

    # Backup (solo se non esiste: i backup sono immutabili)
    if not BACKUP_PATH.exists():
        shutil.copy2(GRAPH_PATH, BACKUP_PATH)
        print(f"\n  Backup creato: {BACKUP_PATH.name}")
    else:
        print(f"\n  Backup gia' presente: {BACKUP_PATH.name} (non sovrascritto)")

    # Migration log
    g.setdefault("migration_log", []).append({
        "date": date.today().isoformat(),
        "script": "scripts/cornice_mondo/step8_fix_canonical_refs.py",
        "phase": "cornice_mondo_step8",
        "summary": (
            f"{n} riferimenti canonici uniformati: foresta_intrecciata x4, "
            "pontile_bocca, villaggio_centrale, who.refs plurale per s05_c2 "
            "(autorizzazione Ray 2026-06-10, risolve known_issues baseline)."
        ),
    })
    g["last_updated"] = date.today().isoformat()

    # Scrittura atomica (pattern blindatura 2026-06)
    payload = json.dumps(g, ensure_ascii=False, indent=2) + "\n"
    tmp = GRAPH_PATH.with_name(GRAPH_PATH.name + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    os.replace(tmp, GRAPH_PATH)
    print(f"  Grafo aggiornato: {GRAPH_PATH.name}")
    print(f"\n  Prossimo passo: svuotare scripts/audit/_data/known_issues.yaml")
    print(f"  Poi: python3 scripts/audit/audit_1_integrity.py --update-manifest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
