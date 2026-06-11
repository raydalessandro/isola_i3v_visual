#!/usr/bin/env python3
"""
audit_5_timeline.py — Integrità temporale-causale: semi, callback, quote.

Gli audit 1-4 verificano che i riferimenti ESISTANO; questo verifica che
rispettino l'ORDINE DEL TEMPO narrativo (s01 → s12). Sola lettura.

MODELLO. Un seme ha due piani:
  - intento:   bloom_target_stories, maturing_planned_stories
  - effettivo: origin_story, maturing_in_stories / maturing_history /
               pickup_history (eventi con .story), bloomed_in_story + status
L'audit è severo sull'effettivo (ERRORE) e morbido sull'intento
(WARNING: la storia può legittimamente deviare dal piano).

ERRORI (bloccanti):
  semi
    - origin_story / sid evento / bloomed_in_story inesistenti
    - status == "bloomed" senza bloomed_in_story
    - fioritura PRIMA dell'origine (order(bloomed) < order(origin))
    - evento effettivo PRIMA dell'origine
    - related_seed inesistente
  incroci storia ↔ seme
    - sNN.seeds_planted contiene X ma X.origin_story != sNN
    - sNN.seeds_bloomed_here contiene X ma X.bloomed_in_story != sNN
    - sNN.seeds_maturing_here contiene X con order(sNN) < order(origine)
  callback
    - from_story / registered_in_story inesistenti
    - registrato NON DOPO l'origine (order(from) >= order(registered))
    - sNN.callbacks_made contiene C ma C.registered_in_story != sNN
  quote_tracker
    - qualunque sid citato (chiave o valore, a qualunque profondità)
      inesistente

WARNING (informativi, mai bloccanti):
  - bloomed_in_story fuori da bloom_target_stories (deviazione dal piano)
  - status != "bloomed" ma bloomed_in_story presente
  - evento effettivo DOPO la fioritura (eco post-bloom: legittima, tracciata)
  - sNN.seeds_maturing_here senza evento effettivo registrato per sNN
    (drift tra le due rappresentazioni della maturazione)

Baseline a cricchetto: scripts/audit/_data/known_issues.yaml (kind timeline_*),
stesso meccanismo di audit_3. Oggi la baseline timeline è vuota: il grafo
v1.2.0 passa pulito (verificato 2026-06-10).

Convenzione output: exit 0 = PASS, exit 1 = FAIL.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GRAPH = REPO / "pipeline_narrativa" / "story_graph.json"
KNOWN_ISSUES = Path(__file__).resolve().parent / "_data" / "known_issues.yaml"

# Canone normativo se presente (branch canone-machine-readable), altrimenti
# fallback locale: la branch resta mergiabile in entrambi gli ordini.
try:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import saga_canon  # type: ignore
    _STORY_IDS = saga_canon.load(REPO).story_ids
except Exception:
    _STORY_IDS = tuple(f"s{i:02d}" for i in range(1, 13))

SID_RE = re.compile(r"^s\d{2}$")
SEED_EVENT_FIELDS = ("maturing_in_stories", "maturing_history", "pickup_history")
SEED_FIELDS_IN_STORY = ("seeds_planted", "seeds_picked_up",
                        "seeds_maturing_here", "seeds_bloomed_here")

errors: list[tuple[str, str, str, str]] = []   # (kind, where, ref, msg)
warnings: list[str] = []


def err(kind: str, where: str, ref: str, msg: str) -> None:
    errors.append((kind, where, ref, str(msg)))


def warn(msg: str) -> None:
    warnings.append(msg)


def order(sid: str) -> int:
    return int(sid[1:])


def as_list(v) -> list:
    return v if isinstance(v, list) else ([v] if v else [])


def ids_of(v) -> list[str]:
    out = []
    for x in as_list(v):
        out.append(x if isinstance(x, str)
                   else (x.get("seed_id") or x.get("callback_id") or x.get("id")))
    return [i for i in out if i]


def seed_event_stories(sd: dict) -> list[tuple[str, str]]:
    """Eventi EFFETTIVI del seme: [(campo, sid), ...]."""
    out = []
    for f in SEED_EVENT_FIELDS:
        for e in as_list(sd.get(f)):
            st = e.get("story") if isinstance(e, dict) else e
            if st:
                out.append((f, st))
    return out


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------

def check_seeds(g: dict) -> None:
    stories = g.get("stories", {})
    seeds = g.get("seeds", {})
    for sid_seed, sd in seeds.items():
        o = sd.get("origin_story")
        b = sd.get("bloomed_in_story")
        status = sd.get("status")
        if o not in stories:
            err("timeline_seed_origin", sid_seed, str(o),
                f"seeds.{sid_seed}: origin_story {o!r} inesistente")
            continue
        if status == "bloomed" and not b:
            err("timeline_seed_bloom", sid_seed, "",
                f"seeds.{sid_seed}: status=bloomed senza bloomed_in_story")
        if b:
            if b not in stories:
                err("timeline_seed_bloom", sid_seed, str(b),
                    f"seeds.{sid_seed}: bloomed_in_story {b!r} inesistente")
            elif order(b) < order(o):
                err("timeline_seed_bloom", sid_seed, b,
                    f"seeds.{sid_seed}: fiorisce in {b} PRIMA dell'origine {o}")
            if status != "bloomed":
                warn(f"seeds.{sid_seed}: bloomed_in_story={b} ma status={status!r}")
        for f, es in seed_event_stories(sd):
            if es not in stories:
                err("timeline_seed_event", sid_seed, es,
                    f"seeds.{sid_seed}.{f}: story {es!r} inesistente")
            elif order(es) < order(o):
                err("timeline_seed_event", sid_seed, es,
                    f"seeds.{sid_seed}.{f}: evento in {es} PRIMA dell'origine {o}")
            elif b and b in stories and order(es) > order(b):
                warn(f"seeds.{sid_seed}.{f}: evento in {es} dopo la fioritura "
                     f"{b} (eco post-bloom)")
        bt = as_list(sd.get("bloom_target_stories"))
        if b and bt and b not in bt:
            warn(f"seeds.{sid_seed}: fiorito in {b}, target era {bt} "
                 f"(deviazione dal piano)")
        for rs in as_list(sd.get("related_seed")):
            if rs not in seeds:
                err("timeline_seed_related", sid_seed, rs,
                    f"seeds.{sid_seed}: related_seed {rs!r} inesistente")


def check_story_seed_cross(g: dict) -> None:
    stories = g.get("stories", {})
    seeds = g.get("seeds", {})
    for sid, s in stories.items():
        for x in ids_of(s.get("seeds_planted")):
            if x in seeds and seeds[x].get("origin_story") != sid:
                err("timeline_planted_mismatch", sid, x,
                    f"{sid}.seeds_planted: {x} ha origin_story="
                    f"{seeds[x].get('origin_story')!r} (atteso {sid})")
        for x in ids_of(s.get("seeds_bloomed_here")):
            if x in seeds and seeds[x].get("bloomed_in_story") != sid:
                err("timeline_bloomed_mismatch", sid, x,
                    f"{sid}.seeds_bloomed_here: {x} ha bloomed_in_story="
                    f"{seeds[x].get('bloomed_in_story')!r} (atteso {sid})")
        for x in ids_of(s.get("seeds_maturing_here")):
            if x not in seeds:
                continue  # esistenza → audit_3
            o = seeds[x].get("origin_story")
            if o and o in stories and order(sid) < order(o):
                err("timeline_maturing_order", sid, x,
                    f"{sid}.seeds_maturing_here: {x} matura PRIMA "
                    f"dell'origine {o}")
            else:
                acts = {es for _, es in seed_event_stories(seeds[x])}
                if acts and sid not in acts:
                    warn(f"{sid}.seeds_maturing_here: {x} senza evento "
                         f"effettivo registrato per {sid} (drift "
                         f"maturing_here ↔ maturing_in_stories)")


def check_callbacks(g: dict) -> None:
    stories = g.get("stories", {})
    cbs = g.get("callbacks", {})
    for cid, cb in cbs.items():
        f, r = cb.get("from_story"), cb.get("registered_in_story")
        if f not in stories or r not in stories:
            err("timeline_callback_sid", cid, f"{f}->{r}",
                f"callbacks.{cid}: from/registered {f!r}->{r!r} inesistenti")
        elif order(f) >= order(r):
            err("timeline_callback_order", cid, f"{f}->{r}",
                f"callbacks.{cid}: registrato in {r} NON DOPO l'origine {f}")
    for sid, s in stories.items():
        for xc in ids_of(s.get("callbacks_made")):
            if xc in cbs and cbs[xc].get("registered_in_story") != sid:
                err("timeline_callback_mismatch", sid, xc,
                    f"{sid}.callbacks_made: {xc} ha registered_in_story="
                    f"{cbs[xc].get('registered_in_story')!r} (atteso {sid})")


def check_quote_tracker(g: dict) -> None:
    stories = g.get("stories", {})
    bad: set[str] = set()

    def walk(o):
        if isinstance(o, str):
            if SID_RE.fullmatch(o) and o not in stories:
                bad.add(o)
        elif isinstance(o, dict):
            for k, v in o.items():
                walk(k)
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(g.get("quote_tracker", {}))
    for q in sorted(bad):
        err("timeline_quote_sid", "quote_tracker", q,
            f"quote_tracker: sid {q!r} citato ma inesistente")


# ---------------------------------------------------------------------------

def load_known_issues() -> list[dict]:
    if not KNOWN_ISSUES.exists():
        return []
    try:
        import yaml  # PyYAML
    except ImportError:
        warn("PyYAML assente: baseline known_issues ignorata")
        return []
    data = yaml.safe_load(KNOWN_ISSUES.read_text(encoding="utf-8")) or {}
    return [i for i in (data.get("issues") or [])
            if str(i.get("kind", "")).startswith("timeline_")]


def main() -> int:
    print(f"== audit_5_timeline — {GRAPH.relative_to(REPO)} ==")
    try:
        g = json.loads(GRAPH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL — grafo non leggibile/parseable: {e}")
        return 1

    check_seeds(g)
    check_story_seed_cross(g)
    check_callbacks(g)
    check_quote_tracker(g)

    baseline = load_known_issues()
    known_keys = {(i.get("kind"), i.get("where"), i.get("ref")) for i in baseline}
    real, known_hits = [], []
    for kind, where, ref, msg in errors:
        (known_hits if (kind, where, ref) in known_keys else real).append(msg)
    found = {(k, w, r) for k, w, r, _ in errors}
    for i in baseline:
        if (i.get("kind"), i.get("where"), i.get("ref")) not in found:
            warn(f"baseline timeline stantia (risolta? rimuovi da "
                 f"known_issues.yaml): {i.get('kind')}/{i.get('where')}/{i.get('ref')}")

    for m in known_hits:
        print(f"  [known] {m}")
    for w in warnings:
        print(f"  [warn] {w}")

    if real:
        print(f"\nFAIL — {len(real)} errori temporali NUOVI "
              f"({len(known_hits)} noti in baseline):")
        for m in real:
            print(f"  ✗ {m}")
        return 1
    n_seeds = len(g.get("seeds", {}))
    n_cbs = len(g.get("callbacks", {}))
    print(f"\nPASS — timeline coerente: {n_seeds} semi, {n_cbs} callback, "
          f"quote_tracker ok ({len(warnings)} warning informativi).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
