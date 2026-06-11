#!/usr/bin/env python3
"""
audit_1_integrity.py — Integrità strutturale del grafo + catena backup.

Verifica (sul grafo A RIPOSO, sola lettura):
  1.  JSON parseable senza errori.
  2.  Nessuna chiave duplicata in nessun oggetto (il parser standard le
      silenzia tenendo l'ultima: qui vengono intercettate e segnalate).
  3.  Chiavi radice obbligatorie presenti (schema_version, graph_version,
      last_updated, entities, stories, quote_tracker, world_conventions,
      migration_log).
  4.  schema_version e graph_version coerenti con i valori attesi
      (EXPECTED_SCHEMA / EXPECTED_GRAPH — aggiornare qui ad ogni bump
      autorizzato).
  5.  Tutte e 12 le storie s01..s12 presenti, con id interno coerente.
  6.  last_updated in formato ISO (YYYY-MM-DD).
  7.  migration_log non vuoto e in ordine cronologico non decrescente.
  8.  Catena backup CONGELATA: ogni backup in pipeline_narrativa/ deve
      esistere, essere JSON valido e avere SHA-256 identico al manifest
      scripts/audit/_data/backup_manifest.sha256. I backup sono immutabili
      per definizione: qualunque variazione è un errore (corruzione o
      manomissione). Un nuovo backup legittimo va AGGIUNTO al manifest
      con --update-manifest (mai sostituire hash esistenti).

Convenzione output (vedi scripts/audit/README.md):
  exit 0 = PASS, exit 1 = FAIL, messaggi umano-leggibili.

Uso:
    python3 scripts/audit/audit_1_integrity.py
    python3 scripts/audit/audit_1_integrity.py --update-manifest   # solo per
        registrare NUOVI backup (gli hash esistenti non vengono mai toccati)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GRAPH = REPO / "pipeline_narrativa" / "story_graph.json"
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # scripts/
import saga_canon  # noqa: E402  (canone normativo: saga_config.yaml)
_C = saga_canon.load(Path(__file__).resolve().parents[2])

BACKUP_GLOBS = _C.graph.backup_globs
MANIFEST = Path(__file__).resolve().parent / "_data" / "backup_manifest.sha256"

# Versioni attese: dal canone (saga_config.yaml → graph.expected_*).
# Bump autorizzato = aggiornare il config, non questo file.
EXPECTED_SCHEMA = _C.graph.expected_schema
EXPECTED_GRAPH = _C.graph.expected_graph
REQUIRED_ROOT_KEYS = (
    "schema_version", "graph_version", "last_updated", "entities",
    "stories", "quote_tracker", "world_conventions", "migration_log",
)
STORY_IDS = _C.story_ids
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# ---------------------------------------------------------------------------
# 1+2. Parse con intercettazione chiavi duplicate
# ---------------------------------------------------------------------------

class _DupKeyTracker:
    """object_pairs_hook che registra chiavi duplicate invece di silenziarle."""

    def __init__(self) -> None:
        self.duplicates: list[str] = []

    def __call__(self, pairs):
        seen = {}
        for k, v in pairs:
            if k in seen:
                self.duplicates.append(k)
            seen[k] = v
        return seen


def load_graph_strict(path: Path) -> dict | None:
    tracker = _DupKeyTracker()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        err(f"grafo non leggibile: {e}")
        return None
    try:
        g = json.loads(text, object_pairs_hook=tracker)
    except json.JSONDecodeError as e:
        err(f"grafo NON parseable: {e}")
        return None
    if tracker.duplicates:
        uniq = sorted(set(tracker.duplicates))
        err(
            f"chiavi duplicate nel grafo ({len(tracker.duplicates)} occorrenze, "
            f"{len(uniq)} distinte): {', '.join(uniq[:10])}"
            + (" ..." if len(uniq) > 10 else "")
        )
    return g


# ---------------------------------------------------------------------------
# 3..7. Struttura radice
# ---------------------------------------------------------------------------

def check_root(g: dict) -> None:
    for k in REQUIRED_ROOT_KEYS:
        if k not in g:
            err(f"chiave radice mancante: {k!r}")

    # NB: nel grafo schema_version è un numero JSON (1.4), graph_version una
    # stringa ("1.2.0") — si confronta sempre la forma stringa.
    sv = g.get("schema_version")
    gv = g.get("graph_version")
    if str(sv) != EXPECTED_SCHEMA:
        err(f"schema_version {sv!r} != atteso {EXPECTED_SCHEMA!r} "
            f"(se il bump è autorizzato, aggiorna graph.expected_schema in saga_config.yaml)")
    if str(gv) != EXPECTED_GRAPH:
        err(f"graph_version {gv!r} != atteso {EXPECTED_GRAPH!r} "
            f"(se il bump è autorizzato, aggiorna graph.expected_graph in saga_config.yaml)")

    lu = g.get("last_updated", "")
    if not isinstance(lu, str) or not ISO_DATE_RE.match(lu):
        err(f"last_updated {lu!r} non in formato ISO YYYY-MM-DD")

    stories = g.get("stories", {})
    missing = [s for s in STORY_IDS if s not in stories]
    extra = [s for s in stories if s not in STORY_IDS]
    if missing:
        err(f"storie mancanti: {', '.join(missing)}")
    if extra:
        err(f"storie inattese: {', '.join(extra)}")
    for sid in STORY_IDS:
        s = stories.get(sid)
        if isinstance(s, dict) and s.get("id") not in (None, sid):
            err(f"{sid}: campo id interno {s.get('id')!r} non coerente")

    mlog = g.get("migration_log", [])
    if not isinstance(mlog, list) or not mlog:
        err("migration_log assente o vuoto")
    else:
        dates = []
        for i, entry in enumerate(mlog):
            # entry storiche usano "date", gli step cornice_mondo "timestamp"
            d = (entry.get("date") or entry.get("timestamp")) \
                if isinstance(entry, dict) else None
            if not d or not ISO_DATE_RE.match(str(d)):
                warn(f"migration_log[{i}]: data assente o non-ISO ({d!r})")
            else:
                dates.append(str(d)[:10])
        if dates != sorted(dates):
            err("migration_log non in ordine cronologico non-decrescente")


# ---------------------------------------------------------------------------
# 8. Catena backup congelata
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_backups() -> list[Path]:
    out: set[Path] = set()
    for pat in BACKUP_GLOBS:
        out.update((REPO / "pipeline_narrativa").glob(pat))
    return sorted(out)


def load_manifest() -> dict[str, str]:
    if not MANIFEST.exists():
        return {}
    entries: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, _, name = line.partition("  ")
        if digest and name:
            entries[name.strip()] = digest.strip()
    return entries


def check_backups(update_manifest: bool) -> None:
    backups = find_backups()
    manifest = load_manifest()

    if not backups:
        err("nessun backup trovato in pipeline_narrativa/ (catena attesa non vuota)")
        return

    new_entries: dict[str, str] = {}
    for b in backups:
        name = b.name
        # JSON valido
        try:
            json.loads(b.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            err(f"backup {name}: NON è JSON valido ({e})")
            continue
        digest = sha256_of(b)
        if name in manifest:
            if manifest[name] != digest:
                err(
                    f"backup {name}: SHA-256 DIVERSO dal manifest — i backup sono "
                    f"immutabili, questo indica corruzione o manomissione.\n"
                    f"        manifest: {manifest[name]}\n"
                    f"        attuale : {digest}"
                )
        else:
            if update_manifest:
                new_entries[name] = digest
            else:
                err(
                    f"backup {name}: non presente nel manifest "
                    f"{MANIFEST.relative_to(REPO)}. Se è un backup nuovo e "
                    f"legittimo, registralo con --update-manifest."
                )

    # file nel manifest spariti dal disco
    for name in manifest:
        if not (REPO / "pipeline_narrativa" / name).exists():
            err(f"backup {name}: presente nel manifest ma ASSENTE dal disco")

    if update_manifest and new_entries:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        if MANIFEST.exists():
            lines = MANIFEST.read_text(encoding="utf-8").rstrip("\n").splitlines()
        else:
            lines = [
                "# backup_manifest.sha256 — hash congelati dei backup del grafo.",
                "# I backup sono immutabili: MAI sostituire un hash esistente.",
                "# Nuovi backup: python3 scripts/audit/audit_1_integrity.py --update-manifest",
            ]
        for name in sorted(new_entries):
            lines.append(f"{new_entries[name]}  {name}")
        MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"[manifest] aggiunti {len(new_entries)} nuovi backup a {MANIFEST.relative_to(REPO)}")


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--update-manifest", action="store_true",
                    help="registra nel manifest i backup nuovi (mai sostituire hash esistenti)")
    args = ap.parse_args()

    print(f"== audit_1_integrity — {GRAPH.relative_to(REPO)} ==")

    g = load_graph_strict(GRAPH)
    if g is not None:
        check_root(g)
    check_backups(update_manifest=args.update_manifest)

    for w in warnings:
        print(f"[warn] {w}")
    if errors:
        print(f"\nFAIL — {len(errors)} errori:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print(f"PASS — grafo integro, {len(find_backups())} backup verificati contro manifest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
