#!/usr/bin/env python3
"""
audit_4_drift.py — Drift prosa: lessico AI bandito + coerenza prosa ↔ grafo.

Implementa la parte MECCANICA dell'audit di drift (sola lettura):

A. LESSICO BANDITO — applica le "RICERCHE LITERAL" di
   pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md §6
   alla prosa di pipeline_narrativa/storie_finali/sNN_*.md
   (frontmatter e marker HTML esclusi, case-insensitive):

     "piano piano"                  → max 1 per storia
     "qualcosa di"                  → max 1
     "in qualche modo"              → max 1
     "a poco a poco"                → 0
     "lentamente"                   → max 1
     "piccolo piccolo"              → max 1
     "guardò il cielo"              → 0
     "guardò fuori dalla finestra"  → 0
     "stringeva forte"              → 0
     "abbracciò forte"              → 0
     "si ricordò di"                → max 1, solo in s11-s12

   Quota saga (§1.4): famiglia "piano piano" (piano piano / pian piano /
   a poco a poco / un po' alla volta) → max 6 in tutta la saga.

B. COERENZA PROSA ↔ GRAFO (marker machine-readable, contratto di
   scripts/build_volume.py):
     - frontmatter: sid coerente col filename, total_hooks == 10,
       status presente
     - esattamente 10 marker @hook, id sNN_h01..h10, ordinati,
       identici agli hook_id della storia nel grafo
     - APPARATO SUBHOOK (pagine libro fisiche) — obbligatorio solo se
       la storia lo ha iniziato (book_pages_total in frontmatter o
       almeno un marker @subhook; oggi: pilota s01). Dove presente:
         * book_pages_total intero in frontmatter
         * la lista @subhooks di ogni @hook coincide con i marker
           @subhook effettivi sotto quell'hook
         * i @page_book coprono 1..book_pages_total senza buchi né
           duplicati (spread doppie [N, N+1] ammesse)
         * ogni @image ≠ TBD punta a un file esistente
       Dove assente: [info] di migrazione, non errore.

C. FUORI SCOPE (richiede lettura/LLM, vedi scripts/audit/README.md):
   ancorabilità di ogni focal_action alla narrazione fattuale;
   domande qualitative §6 (triadi, pugni emotivi, sguardo adulto-tenero).
   Da eseguire come review agente/Ray, non come grep.

Convenzione output: exit 0 = PASS, exit 1 = FAIL.
Uso:
    python3 scripts/audit/audit_4_drift.py            # tutte le storie
    python3 scripts/audit/audit_4_drift.py --story s01
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GRAPH = REPO / "pipeline_narrativa" / "story_graph.json"
STORIE = REPO / "pipeline_narrativa" / "storie_finali"

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # scripts/
import saga_canon  # noqa: E402  (canone normativo: saga_config.yaml)
_C = saga_canon.load(Path(__file__).resolve().parents[2])

STORY_IDS = _C.story_ids

# Quote lessicali e grammatica marker: dal canone (saga_config.yaml).
# (pattern, max per storia, solo_storie | None) — formato interno invariato.
LEXICAL_QUOTAS: list[tuple[str, int, tuple[str, ...] | None]] = [
    (q.pattern, q.max_per_story, q.only_stories) for q in _C.lexicon.quotas
]
PIANO_FAMILY = _C.lexicon.piano_family_patterns
PIANO_FAMILY_SAGA_MAX = _C.lexicon.piano_family_saga_max

HOOK_MARKER_RE = _C.markers.hook_re
SUBHOOK_MARKER_RE = _C.markers.subhook_re
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

errors: list[str] = []
infos: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def split_frontmatter(text: str) -> tuple[str, str]:
    m = FM_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def prose_only(body: str) -> str:
    """Prosa pura: via i commenti HTML (marker) e le righe heading."""
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("#"))
    return body


def fm_value(fm: str, key: str) -> str | None:
    m = re.search(rf"^{key}:\s*(.+?)\s*$", fm, re.MULTILINE)
    return m.group(1).strip() if m else None


def page_book_values(raw: str) -> list[int]:
    raw = raw.strip()
    if raw.startswith("["):
        return [int(x) for x in re.findall(r"\d+", raw)]
    return [int(raw)]


def check_story(sid: str, path: Path, graph_hook_ids: list[str],
                saga_counts: dict[str, int]) -> None:
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    if not fm:
        err(f"{sid}: frontmatter YAML assente in {path.name}")
        return
    prose = prose_only(body)
    low = prose.lower()

    # -- A. lessico bandito ---------------------------------------------------
    for pat, maxn, only in LEXICAL_QUOTAS:
        n = len(re.findall(pat, low))
        if only and sid not in only and n > 0:
            err(f"{sid}: {pat!r} ×{n} — ammesso solo in {'/'.join(only)} "
                f"(PATTERN_AI_DA_BANDIRE §6)")
        elif n > maxn:
            err(f"{sid}: {pat!r} ×{n} > max {maxn} (PATTERN_AI_DA_BANDIRE §6)")
    for pat in PIANO_FAMILY:
        saga_counts[pat] = saga_counts.get(pat, 0) + len(re.findall(pat, low))

    # -- B. frontmatter ---------------------------------------------------------
    if fm_value(fm, "sid") != sid:
        err(f"{sid}: frontmatter sid {fm_value(fm, 'sid')!r} ≠ filename")
    if fm_value(fm, "total_hooks") != "10":
        err(f"{sid}: frontmatter total_hooks {fm_value(fm, 'total_hooks')!r} ≠ 10")
    if not fm_value(fm, "status"):
        err(f"{sid}: frontmatter status assente")
    # apparato subhook: attivo se dichiarato in frontmatter o se esistono
    # marker @subhook nel corpo (pilota: s01; le altre storie migrano dopo)
    bpt_raw = fm_value(fm, "book_pages_total")
    has_subhook_markers = bool(SUBHOOK_MARKER_RE.search(body))
    subhook_apparatus = bpt_raw is not None or has_subhook_markers
    bpt = None
    if subhook_apparatus:
        try:
            bpt = int(bpt_raw)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            err(f"{sid}: frontmatter book_pages_total {bpt_raw!r} non intero "
                f"(obbligatorio: apparato subhook iniziato)")

    # -- B. marker @hook ----------------------------------------------------------
    hooks = HOOK_MARKER_RE.findall(body)
    hook_ids = [h[0] for h in hooks]
    expected = [f"{sid}_h{i:02d}" for i in range(1, 11)]
    if hook_ids != expected:
        err(f"{sid}: marker @hook {len(hook_ids)}/10 o fuori sequenza "
            f"(trovati: {hook_ids[:12]})")
    if graph_hook_ids and sorted(hook_ids) != sorted(graph_hook_ids):
        only_prose = sorted(set(hook_ids) - set(graph_hook_ids))
        only_graph = sorted(set(graph_hook_ids) - set(hook_ids))
        if only_prose or only_graph:
            err(f"{sid}: hook prosa ≠ hook grafo "
                f"(solo prosa: {only_prose}, solo grafo: {only_graph})")

    # -- B. marker @subhook + @page_book + @image -----------------------------------
    if not subhook_apparatus:
        infos.append(f"{sid}: apparato subhook non ancora migrato "
                     f"(solo marker @hook) — ok, pilota: s01")
        return
    declared: dict[str, list[str]] = {
        h[0]: [x.strip() for x in h[2].split(",") if x.strip()] for h in hooks
    }
    subhooks = SUBHOOK_MARKER_RE.findall(body)
    actual_by_hook: dict[str, list[str]] = {}
    pages: list[int] = []
    for sh_id, pb_raw, _layout, image in subhooks:
        parent = sh_id[:-1]
        actual_by_hook.setdefault(parent, []).append(sh_id)
        try:
            pages.extend(page_book_values(pb_raw))
        except ValueError:
            err(f"{sid}: @subhook {sh_id}: @page_book {pb_raw!r} non parseable")
        img = image.strip()
        if img and img.upper() != "TBD":
            if not (REPO / img).exists():
                err(f"{sid}: @subhook {sh_id}: @image {img!r} non esiste su disco")

    for hid, decl in declared.items():
        act = actual_by_hook.get(hid, [])
        if sorted(decl) != sorted(act):
            err(f"{sid}: {hid}: @subhooks dichiarati {decl} ≠ marker presenti {act}")

    if bpt is not None and pages:
        got = sorted(set(pages))
        want = list(range(1, bpt + 1))
        if got != want:
            missing = sorted(set(want) - set(got))
            extra = sorted(set(got) - set(want))
            dup = sorted({p for p in pages if pages.count(p) > 1})
            detail = []
            if missing:
                detail.append(f"mancanti {missing}")
            if extra:
                detail.append(f"fuori range {extra}")
            if dup:
                detail.append(f"duplicate {dup}")
            err(f"{sid}: @page_book non copre 1..{bpt}: {', '.join(detail)}")


def main() -> int:
    ap = argparse.ArgumentParser(description="audit drift prosa (parte meccanica)")
    ap.add_argument("--story", help="audita una sola storia (es. s01)")
    args = ap.parse_args()

    targets = (args.story,) if args.story else STORY_IDS
    print(f"== audit_4_drift — storie_finali/ ({len(targets)} storie) ==")

    graph_hooks: dict[str, list[str]] = {}
    try:
        g = json.loads(GRAPH.read_text(encoding="utf-8"))
        for sid, s in g.get("stories", {}).items():
            graph_hooks[sid] = [
                h.get("hook_id") for h in
                (s.get("visual_anchors") or {}).get("scene_hooks") or []
            ]
    except (OSError, json.JSONDecodeError) as e:
        err(f"grafo non leggibile per cross-check hook: {e}")

    saga_counts: dict[str, int] = {}
    for sid in targets:
        files = sorted(STORIE.glob(f"{sid}_*.md"))
        if not files:
            err(f"{sid}: file storia non trovato in storie_finali/")
            continue
        if len(files) > 1:
            err(f"{sid}: più file storia trovati: {[f.name for f in files]}")
        check_story(sid, files[0], graph_hooks.get(sid, []), saga_counts)

    if not args.story:  # quota saga solo su run completo
        fam_total = sum(saga_counts.values())
        if fam_total > PIANO_FAMILY_SAGA_MAX:
            err(f"saga: famiglia 'piano piano' ×{fam_total} > max "
                f"{PIANO_FAMILY_SAGA_MAX} (PATTERN_AI_DA_BANDIRE §1.4) — "
                f"dettaglio: { {k: v for k, v in saga_counts.items() if v} }")

    for i in infos:
        print(f"  [info] {i}")

    if errors:
        print(f"\nFAIL — {len(errors)} errori:")
        for e in errors:
            print(f"  ✗ {e}")
        print("\nNB: la parte qualitativa (triadi, pugno emotivo, ancoraggio "
              "focal_action↔narrazione) resta review umana/LLM — vedi §6 del "
              "documento PATTERN_AI_DA_BANDIRE e scripts/audit/README.md.")
        return 1
    print("PASS — lessico entro quota, marker prosa↔grafo coerenti, "
          "immagini referenziate esistenti.")
    print("(la parte qualitativa §6 resta review umana/LLM — fuori scope grep)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
