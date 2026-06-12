#!/usr/bin/env python3
"""
build_routing_table.py — rigenera la tabella di routing nel CLAUDE.md
dai frontmatter YAML delle skill (skills/*/SKILL.md).

Stile repo: idempotente, --dry-run di default, --apply per scrivere.

Frontmatter atteso in ogni skills/<ruolo>/SKILL.md:

    ---
    role: cartografo
    trigger: manutenzione/estensione della cartografia tecnica
    scope_write: "cartografia/, scripts/ (tool condivisi)"
    commands: "make audit"        # opzionale
    order: 10                      # opzionale, per l'ordinamento in tabella
    ---

La tabella viene scritta tra i marker nel CLAUDE.md:
    <!-- ROUTING:BEGIN ... -->
    ...
    <!-- ROUTING:END -->

Uso:
    python3 scripts/build_routing_table.py            # dry-run: mostra la tabella
    python3 scripts/build_routing_table.py --apply    # scrive nel CLAUDE.md
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = ROOT / "CLAUDE.md"
SKILLS_DIR = ROOT / "skills"

BEGIN_RE = re.compile(r"<!-- ROUTING:BEGIN[^>]*-->")
END_RE = re.compile(r"<!-- ROUTING:END -->")

BEGIN_LINE = (
    "<!-- ROUTING:BEGIN — generata da `make routing` "
    "(scripts/build_routing_table.py) dai frontmatter delle skill. "
    "Non editare a mano. -->"
)
END_LINE = "<!-- ROUTING:END -->"


def parse_frontmatter(path: Path):
    """Estrae il frontmatter YAML (--- ... ---) in testa al file. None se assente."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        print(f"  [WARN] frontmatter YAML non valido in {path}: {e}", file=sys.stderr)
        return None
    return data if isinstance(data, dict) else None


def collect_skills():
    rows = []
    problems = []
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        fm = parse_frontmatter(skill_md)
        rel = skill_md.relative_to(ROOT)
        if not fm:
            problems.append(f"{rel}: frontmatter mancante o non valido")
            continue
        missing = [k for k in ("role", "trigger", "scope_write") if k not in fm]
        if missing:
            problems.append(f"{rel}: campi mancanti {missing}")
            continue
        rows.append(
            {
                "order": fm.get("order", 100),
                "role": str(fm["role"]),
                "trigger": str(fm["trigger"]),
                "scope_write": str(fm["scope_write"]),
                "commands": str(fm.get("commands", "—")),
                "path": f"`{rel}`",
            }
        )
    rows.sort(key=lambda r: (r["order"], r["role"]))
    return rows, problems


def build_table(rows):
    lines = [
        "| Ruolo | Quando | Scrive in | Comandi | Skill |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| **{r['role']}** | {r['trigger']} | {r['scope_write']} "
            f"| {r['commands']} | {r['path']} |"
        )
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="scrive nel CLAUDE.md")
    args = ap.parse_args()

    rows, problems = collect_skills()
    for p in problems:
        print(f"[WARN] {p}", file=sys.stderr)
    if not rows:
        print("[ERRORE] nessuna skill con frontmatter valido trovata.", file=sys.stderr)
        return 1

    table = build_table(rows)

    text = CLAUDE_MD.read_text(encoding="utf-8")
    m_begin = BEGIN_RE.search(text)
    m_end = END_RE.search(text)
    if not m_begin or not m_end or m_end.start() < m_begin.end():
        print("[ERRORE] marker ROUTING:BEGIN/END non trovati (o invertiti) nel CLAUDE.md.",
              file=sys.stderr)
        return 1

    new_text = (
        text[: m_begin.start()]
        + BEGIN_LINE + "\n" + table + "\n" + END_LINE
        + text[m_end.end():]
    )

    if new_text == text:
        print(f"OK — tabella già allineata ({len(rows)} skill). Nessuna modifica.")
        return 0

    if args.apply:
        CLAUDE_MD.write_text(new_text, encoding="utf-8")
        print(f"SCRITTO — tabella di routing rigenerata nel CLAUDE.md ({len(rows)} skill).")
    else:
        print(f"DRY-RUN — la tabella verrebbe aggiornata a ({len(rows)} skill):\n")
        print(table)
        print("\nUsa --apply per scrivere.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
