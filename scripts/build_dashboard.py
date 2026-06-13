#!/usr/bin/env python3
"""build_dashboard.py — Estrae i dati di sistema della repo e li scrive in
dashboard/data/dashboard.js (window.DASHBOARD_DATA = {...}).

Idempotente, zero LLM, zero dipendenze esterne (solo stdlib).
Le pagine HTML in dashboard/ sono statiche e leggono questo file via <script>.

Uso:
    python3 scripts/build_dashboard.py            # scrive dashboard/data/dashboard.js
    python3 scripts/build_dashboard.py --dry-run  # stampa il riepilogo senza scrivere

Coerente col pattern repo: LLM judgment upstream, estrazione meccanica downstream.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dashboard" / "data" / "dashboard.js"
GITHUB_BLOB = "https://github.com/raydalessandro/isola_i3v_visual/blob/main/"

# ───────────────────────────────────────────────────────────────────────────
# Helper

def git_mtime(path: Path) -> str:
    """Ultima modifica del file secondo git (ISO). Fallback: mtime filesystem."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def git_head() -> dict:
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             cwd=ROOT, capture_output=True, text=True).stdout.strip()
        date = subprocess.run(["git", "log", "-1", "--format=%cI"],
                              cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return {"sha": sha, "date": date}
    except Exception:
        return {"sha": "?", "date": "?"}


def file_stats(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "lines": text.count("\n") + 1,
        "tokens_est": round(path.stat().st_size / 4),  # stima grezza ~4 byte/token
        "mtime": git_mtime(path),
        "url": GITHUB_BLOB + str(path.relative_to(ROOT)),
    }


def first_paragraph(path: Path, max_len: int = 240) -> str:
    """Primo paragrafo di contenuto: salta frontmatter YAML, titoli, righe vuote."""
    text = path.read_text(encoding="utf-8", errors="replace")
    # rimuovi frontmatter
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            text = text[end + 4:]
    para: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            if para:
                break
            continue
        if s.startswith("#") or s.startswith("```") or s.startswith("|"):
            if para:
                break
            continue
        para.append(s.lstrip("> "))
    p = " ".join(para)
    return (p[: max_len - 1] + "…") if len(p) > max_len else p


def parse_frontmatter(path: Path) -> dict:
    """Parser minimale del frontmatter delle skill (chiave: valore, una riga)."""
    fm: dict = {}
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end == -1:
        return fm
    for line in text[3:end].splitlines():
        m = re.match(r"^(\w+):\s*(.*)$", line.strip())
        if m:
            val = m.group(2).strip().strip('"')
            fm[m.group(1)] = val
    return fm


# ───────────────────────────────────────────────────────────────────────────
# 1. Classificazione documenti (pagina 6)

# Esclusi (contenuto, non meta): prosa, brief, annotazioni, schede entità,
# narrazione fattuale, web app, starter kit interno, asset.
EXCLUDE_PATTERNS = [
    "pipeline_narrativa/storie_finali/",
    "pipeline_narrativa/writing_briefs/",
    "pipeline_narrativa/narrazione_fattuale/",
    "pipeline_narrativa/hooks_proposals/",
    "pipeline_narrativa/prompts/",
    "visual/",
    "web/",
    "catalogo_web/",
    "node_modules/",
    "contributi/",
    "_porting_grafo/",
    ".github/",
    "_visual_pipeline/_esempi/",     # esempi validati = contenuto, non meta
    "_visual_pipeline/_templates/",  # template di compilazione, non doc di sistema
]

# Esclusi SOLO dalla scansione TODO (sono doc di sistema legittimi, ma le loro
# checkbox/⚠️ sono operativi o storici, non debito):
TODO_SCAN_EXCLUDE = [
    "SYNC_LOG.md",                       # log storico: i ⚠️ sono cronaca
    "_visual_pipeline/_skill/CHECKLIST.md",  # checklist operativa by design
]

CORE_EXACT = {
    "CLAUDE.md", "PROJECT_STATE.md", "saga_config.yaml",
    "Makefile", "SYNC_LOG.md",
}


def classify(rel: str) -> str | None:
    """Ritorna la categoria oppure None se il file è escluso."""
    for pat in EXCLUDE_PATTERNS:
        if rel.startswith(pat):
            return None
    if rel in CORE_EXACT:
        return "core"
    if re.match(r"^skills/[^/]+/SKILL\.md$", rel):
        return "core"
    if rel.startswith("docs/fasi/") or rel.startswith("_pacchetti_consegnati/"):
        return "archivio"
    if rel.startswith("pipeline_narrativa/documenti_progetto/"):
        return "progetto"
    # tutto il resto dei .md di sistema: README sparsi, docs/, _visual_pipeline,
    # _starter_kit, cartografia, scripts/README ecc.
    return "operativo"


def collect_documents() -> list[dict]:
    docs = []
    candidates = list(ROOT.rglob("*.md"))
    # file core non-md
    for name in ("saga_config.yaml", "Makefile"):
        p = ROOT / name
        if p.exists():
            candidates.append(p)
    for p in sorted(set(candidates)):
        if ".git" in p.parts:
            continue
        rel = str(p.relative_to(ROOT))
        cat = classify(rel)
        if cat is None:
            continue
        d = file_stats(p)
        d["category"] = cat
        d["preview"] = first_paragraph(p) if p.suffix == ".md" else ""
        docs.append(d)
    return docs


# ───────────────────────────────────────────────────────────────────────────
# 2. Agent entry (pagina 2)

AGENT_ENTRY_SEQUENCE = [
    ("CLAUDE.md", "Router. Regole stabili + tabella di routing. Letto sempre per primo."),
    ("PROJECT_STATE.md", "Snapshot operativo: stato corrente + ultima sessione."),
    ("saga_config.yaml", "Canone macchina: id, marker, lessico, vincoli (single source of truth)."),
    ("docs/MAPPA_REPO.md", "Mappa annotata delle directory (consultata se serve navigare)."),
    ("Makefile", "Comandi disponibili (make help)."),
]


def build_agent_entry(skills: list[dict]) -> dict:
    seq = []
    cumulative = 0
    for rel, role in AGENT_ENTRY_SEQUENCE:
        p = ROOT / rel
        if not p.exists():
            continue
        st = file_stats(p)
        st["role"] = role
        cumulative += st["tokens_est"]
        st["tokens_cumulative"] = cumulative
        seq.append(st)
    return {
        "sequence": seq,
        "base_tokens_est": cumulative,
        "note": ("Dopo il router l'agente legge UNA skill pertinente "
                 "(tabella di routing). Costo aggiuntivo per skill qui sotto."),
        "skills_cost": [
            {"role": s["role"], "path": s["path"], "bytes": s["bytes"],
             "lines": s["lines"], "tokens_est": s["tokens_est"],
             "tokens_total_entry": cumulative + s["tokens_est"], "url": s["url"]}
            for s in skills
        ],
    }


# ───────────────────────────────────────────────────────────────────────────
# 3. Skills (pagina 3)

def collect_skills() -> list[dict]:
    skills = []
    for sk in sorted((ROOT / "skills").glob("*/SKILL.md")):
        fm = parse_frontmatter(sk)
        st = file_stats(sk)
        skills.append({
            "role": fm.get("role", sk.parent.name),
            "trigger": fm.get("trigger", ""),
            "scope_write": fm.get("scope_write", ""),
            "commands": fm.get("commands", ""),
            "order": int(fm.get("order", 999)),
            "preview": first_paragraph(sk),
            **st,
        })
    skills.sort(key=lambda s: s["order"])
    return skills


# ───────────────────────────────────────────────────────────────────────────
# 4. Pipeline (pagina 4)

def collect_pipeline() -> list[dict]:
    """Estrae le tappe dai box ASCII di docs/PIPELINE.md."""
    p = ROOT / "docs" / "PIPELINE.md"
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8", errors="replace")
    tappe = []
    pattern = re.compile(
        r"│\s+TAPPA (\d+)\s+—\s+(.+?)\s+│(.*?)(?=└)", re.S)
    for m in pattern.finditer(text):
        num, title, body = m.group(1), m.group(2).strip(), m.group(3)
        fields = {}
        for key in ("Input", "Output", "Auto", "Prompt", "Doc"):
            fm = re.search(rf"│\s+{key}:\s+(.+?)\s+│", body)
            if fm:
                fields[key.lower()] = re.sub(r"\s+", " ", fm.group(1)).strip()
        # righe di continuazione di Input (indentate sotto)
        tappe.append({"n": int(num), "title": title, **fields})
    return tappe


# ───────────────────────────────────────────────────────────────────────────
# 5. Repo map (pagina 5)

def collect_repo_map() -> dict:
    p = ROOT / "docs" / "MAPPA_REPO.md"
    if not p.exists():
        return {"tree": "", "url": ""}
    text = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"```\n(.*?)```", text, re.S)
    return {
        "tree": m.group(1) if m else text,
        "url": GITHUB_BLOB + "docs/MAPPA_REPO.md",
        "mtime": git_mtime(p),
    }


# ───────────────────────────────────────────────────────────────────────────
# 6. TODO + debito (pagina 7)

TODO_LINE = re.compile(
    r"(TODO|FIXME|⚠️|XXX\b)", re.I)
UNCHECKED = re.compile(r"^\s*[-*]\s+\[ \]\s+(.+)$")
TODO_HEADER = re.compile(
    r"^#{1,6}\s+.*\b(TODO|Aperti|Da fare|Aperto|Debito|Pending)\b", re.I)
HEADER = re.compile(r"^#{1,6}\s+")


def extract_todos(docs: list[dict]) -> list[dict]:
    """Scansiona i .md di sistema (categorie core/operativo/progetto, non archivio)."""
    groups = []
    for d in docs:
        if d["category"] == "archivio" or not d["path"].endswith(".md"):
            continue
        if d["path"] in TODO_SCAN_EXCLUDE:
            continue
        p = ROOT / d["path"]
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        items = []
        in_todo_section = False
        in_code = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            if HEADER.match(line):
                in_todo_section = bool(TODO_HEADER.match(line))
                if in_todo_section:
                    items.append({"line": i, "kind": "sezione",
                                  "text": line.strip("# ").strip()})
                continue
            mu = UNCHECKED.match(line)
            if mu:
                items.append({"line": i, "kind": "checklist",
                              "text": mu.group(1).strip()[:200]})
                continue
            if re.search(r"\b(TODO|FIXME|XXX)\b", line):
                items.append({"line": i, "kind": "todo",
                              "text": line.strip()[:200]})
                continue
            if "⚠️" in line:
                items.append({"line": i, "kind": "warning",
                              "text": line.strip()[:200]})
                continue
            if in_todo_section and line.strip().startswith(("-", "*")):
                items.append({"line": i, "kind": "voce",
                              "text": line.strip("-* ").strip()[:200]})
        if items:
            groups.append({"path": d["path"], "url": d["url"],
                           "category": d["category"], "items": items})
    groups.sort(key=lambda g: -len(g["items"]))
    return groups


def collect_known_issues() -> dict:
    p = ROOT / "scripts" / "audit" / "_data" / "known_issues.yaml"
    if not p.exists():
        return {"raw": "", "count": 0, "url": ""}
    text = p.read_text(encoding="utf-8", errors="replace")
    # conteggio voci senza dipendere da PyYAML: righe "- " sotto issues:
    body = text.split("issues:", 1)[-1]
    count = len(re.findall(r"^\s*-\s", body, re.M))
    return {"raw": text, "count": count,
            "url": GITHUB_BLOB + "scripts/audit/_data/known_issues.yaml",
            "mtime": git_mtime(p)}


# ───────────────────────────────────────────────────────────────────────────
# 7. Make (pagina 8)

def collect_make() -> list[dict]:
    p = ROOT / "Makefile"
    targets = []
    if not p.exists():
        return targets
    text = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'@echo "  make (\S+)\s*—\s*(.+?)"', text):
        targets.append({"target": m.group(1), "desc": m.group(2)})
    return targets


# ───────────────────────────────────────────────────────────────────────────
# Main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    skills = collect_skills()
    docs = collect_documents()
    todos = extract_todos(docs)
    known = collect_known_issues()

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "head": git_head(),
        "agent_entry": build_agent_entry(skills),
        "skills": skills,
        "pipeline": collect_pipeline(),
        "repo_map": collect_repo_map(),
        "documents": docs,
        "todos": {
            "groups": todos,
            "total": sum(len(g["items"]) for g in todos),
            "known_issues": known,
        },
        "make": collect_make(),
        "counts": {
            "skills": len(skills),
            "documents": len(docs),
            "docs_by_category": {
                c: sum(1 for d in docs if d["category"] == c)
                for c in ("core", "operativo", "progetto", "archivio")
            },
        },
    }

    summary = (f"skills={len(skills)} docs={len(docs)} "
               f"todo_items={data['todos']['total']} "
               f"tappe={len(data['pipeline'])} "
               f"make_targets={len(data['make'])} "
               f"entry_tokens≈{data['agent_entry']['base_tokens_est']}")

    if args.dry_run:
        print("[dry-run]", summary)
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=1)
    OUT.write_text("window.DASHBOARD_DATA = " + payload + ";\n",
                   encoding="utf-8")
    print(f"Scritto {OUT.relative_to(ROOT)} — {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
