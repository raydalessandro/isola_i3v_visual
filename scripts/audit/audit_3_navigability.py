#!/usr/bin/env python3
"""
audit_3_navigability.py — Integrità referenziale grafo ↔ catalogo ↔ cartografia.

Verifica che ogni riferimento per id nel grafo punti a qualcosa che esiste
(sola lettura, grafo a riposo).

UNIVERSI DI RISOLUZIONE:
  LOCS   = entities.locations
  CHARS  = entities.characters
  OBJS   = entities.objects
  WINDS  = entities.winds
  PATHS  = world_conventions.path_details.paths
  VIS    = directory con scheda.md sotto visual/luoghi/ (sentieri,
           sotto-luoghi) + i contenitori quartiere di primo livello
           (quartiere_acqua, perimetro, ... — canonici anche senza scheda)
  GRUPPI = directory sotto visual/personaggi/collettivi/
  EXT    = LOCS ∪ locations_secondary(12 storie) ∪ PATHS ∪ VIS
           (universo esteso per riferimenti "soft": cornici, sentieri)

CHECK (errore):
  - hook: location.id ∈ LOCS; characters_present ⊆ CHARS;
    focal_object ∈ OBJS; wind_visible ∈ WINDS; quadrant ∈ enum quadranti
  - storia: location_primary ∈ LOCS; locations_secondary ⊆ EXT;
    characters_in_scene/offscreen ⊆ CHARS; oggetti_simbolo_presenti ⊆ OBJS;
    wind_active ∈ WINDS (se valorizzato);
    seeds_planted/picked_up/maturing_here/bloomed_here ⊆ seeds;
    callbacks_made ⊆ callbacks
  - cornice: who.ref ∈ GRUPPI (kind=gruppo) o CHARS (kind=nominato);
    kind=anonimo → nessun ref da risolvere; where.location_id ∈ EXT
  - path_details: chiavi ⊆ locations_secondary ∪ VIS
  - seeds.origin_story / callbacks.from_story ∈ stories

CHECK (warning, non bloccante):
  - locations.*.contains: id non risolti (campo descrittivo legacy, alias)
  - entity del grafo senza scheda visual corrispondente (copertura catalogo)

BASELINE INCOERENZE NOTE — scripts/audit/_data/known_issues.yaml:
  le incoerenze già note e in attesa di decisione autoriale vengono
  declassate da errore a "[known]"; le voci della baseline non più
  riscontrate vengono segnalate come stantie (da rimuovere). Qualunque
  incoerenza NUOVA resta un errore → meccanismo a cricchetto: lo stato
  può solo migliorare.

Convenzione output: exit 0 = PASS, exit 1 = FAIL.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GRAPH = REPO / "pipeline_narrativa" / "story_graph.json"
VISUAL_LUOGHI = REPO / "visual" / "luoghi"
VISUAL_COLLETTIVI = REPO / "visual" / "personaggi" / "collettivi"
KNOWN_ISSUES = Path(__file__).resolve().parent / "_data" / "known_issues.yaml"

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # scripts/
import saga_canon  # noqa: E402  (canone normativo: saga_config.yaml)
_C = saga_canon.load(Path(__file__).resolve().parents[2])

VALID_QUADRANTS = _C.quadrants
STORY_IDS = _C.story_ids
SEED_FIELDS = ("seeds_planted", "seeds_picked_up",
               "seeds_maturing_here", "seeds_bloomed_here")

errors: list[tuple[str, str, str, str]] = []   # (kind, where, ref, msg)
warnings: list[str] = []


def err(kind: str, where: str, ref: str, msg: str) -> None:
    errors.append((kind, where, ref, msg))


def warn(msg: str) -> None:
    warnings.append(msg)


def ids_of(v) -> list[str]:
    """Estrae gli id da campi a forma mista: str | {id|ref|seed_id} | lista."""
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    if isinstance(v, dict):
        i = v.get("id") or v.get("ref") or v.get("seed_id")
        return [i] if i else []
    out: list[str] = []
    for x in v:
        out.extend(ids_of(x))
    return out


def load_known_issues() -> list[dict]:
    if not KNOWN_ISSUES.exists():
        return []
    try:
        import yaml  # PyYAML
    except ImportError:
        warn("PyYAML assente: baseline known_issues ignorata "
             "(pip install pyyaml)")
        return []
    data = yaml.safe_load(KNOWN_ISSUES.read_text(encoding="utf-8")) or {}
    return data.get("issues", []) or []


def main() -> int:
    print(f"== audit_3_navigability — {GRAPH.relative_to(REPO)} ==")
    try:
        g = json.loads(GRAPH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL — grafo non leggibile/parseable: {e}")
        return 1

    ents = g.get("entities", {})
    LOCS = set(ents.get("locations", {}))
    CHARS = set(ents.get("characters", {}))
    OBJS = set(ents.get("objects", {}))
    WINDS = set(ents.get("winds", {}))
    SEEDS = set(g.get("seeds", {}))
    CALLBACKS = set(g.get("callbacks", {}))
    PATHS = set(g.get("world_conventions", {})
                 .get("path_details", {}).get("paths", {}))
    VIS = set()
    if VISUAL_LUOGHI.exists():
        VIS = {p.name for p in VISUAL_LUOGHI.rglob("*")
               if p.is_dir() and (p / "scheda.md").exists()}
        # contenitori quartiere di primo livello: canonici anche senza scheda
        VIS |= {p.name for p in VISUAL_LUOGHI.iterdir() if p.is_dir()}
    GRUPPI = {p.name for p in VISUAL_COLLETTIVI.iterdir()
              if p.is_dir()} if VISUAL_COLLETTIVI.exists() else set()

    SEC: set[str] = set()
    stories = g.get("stories", {})
    for s in stories.values():
        SEC.update(ids_of(s.get("locations_secondary")))
    EXT = LOCS | SEC | PATHS | VIS

    # -- quadranti delle location -------------------------------------------
    for lid, l in ents.get("locations", {}).items():
        q = l.get("quadrant")
        if q and q not in VALID_QUADRANTS:
            err("location_quadrant", lid, str(q),
                f"locations.{lid}: quadrant {q!r} non in enum {sorted(VALID_QUADRANTS)}")

    # -- hook ----------------------------------------------------------------
    for sid in STORY_IDS:
        s = stories.get(sid) or {}
        hooks = (s.get("visual_anchors") or {}).get("scene_hooks") or []
        for h in hooks:
            hid = h.get("hook_id", f"{sid}_h??")
            loc = h.get("location") or {}
            lid = loc.get("id") if isinstance(loc, dict) else None
            if lid and lid not in LOCS:
                err("hook_location", hid, lid,
                    f"{hid}: location.id {lid!r} assente da entities.locations")
            for c in h.get("characters_present") or []:
                if c not in CHARS:
                    err("hook_character", hid, c,
                        f"{hid}: character {c!r} assente da entities.characters")
            fo = h.get("focal_object")
            if fo and fo not in OBJS:
                err("hook_object", hid, fo,
                    f"{hid}: focal_object {fo!r} assente da entities.objects")
            wv = h.get("wind_visible")
            if wv and wv not in WINDS:
                err("hook_wind", hid, wv,
                    f"{hid}: wind_visible {wv!r} assente da entities.winds")
            q = h.get("quadrant")
            if q and q not in VALID_QUADRANTS:
                err("hook_quadrant", hid, str(q),
                    f"{hid}: quadrant {q!r} non in enum")

    # -- campi storia ----------------------------------------------------------
    for sid in STORY_IDS:
        s = stories.get(sid) or {}
        for lp in ids_of(s.get("location_primary")):
            if lp not in LOCS:
                err("story_location_primary", sid, lp,
                    f"{sid}: location_primary {lp!r} assente da entities.locations")
        for ls in ids_of(s.get("locations_secondary")):
            if ls not in EXT:
                err("story_location_secondary", sid, ls,
                    f"{sid}: locations_secondary {ls!r} non risolvibile (LOCS∪PATHS∪VIS)")
        for c in ids_of(s.get("characters_in_scene")):
            if c not in CHARS:
                err("story_character", sid, c,
                    f"{sid}: characters_in_scene {c!r} assente")
        for c in ids_of(s.get("characters_offscreen_or_background")):
            if c not in CHARS:
                err("story_character_bg", sid, c,
                    f"{sid}: characters_offscreen {c!r} assente")
        for o in ids_of(s.get("oggetti_simbolo_presenti")):
            if o not in OBJS:
                err("story_object", sid, o,
                    f"{sid}: oggetto_simbolo {o!r} assente da entities.objects")
        wa = s.get("wind_active")
        if wa and wa not in WINDS:
            err("story_wind", sid, str(wa),
                f"{sid}: wind_active {wa!r} assente da entities.winds")
        for f in SEED_FIELDS:
            for r in ids_of(s.get(f)):
                if r not in SEEDS:
                    err("story_seed", sid, r,
                        f"{sid}: {f} {r!r} assente da seeds")
        for r in ids_of(s.get("callbacks_made")):
            if r not in CALLBACKS:
                err("story_callback", sid, r,
                    f"{sid}: callbacks_made {r!r} assente da callbacks")

        # -- cornici -----------------------------------------------------------
        for c in s.get("cornice_dettagli") or []:
            cid = c.get("id", f"{sid}_c?")
            who = c.get("who") or {}
            kind = who.get("kind")
            # Schema esteso (blindatura step8): `refs` lista plurale per kind
            # "nominati"/"gruppo plurimo"; `ref` singolo per kind classici.
            refs = who.get("refs") or ([who["ref"]] if who.get("ref") else [])
            if kind == "gruppo":
                for r in refs:
                    if r and r not in GRUPPI:
                        err("cornice_gruppo", cid, r,
                            f"{cid}: who ref {r!r} assente da visual/personaggi/collettivi/")
            elif kind in ("nominato", "nominati"):
                for r in refs:
                    if r and r not in CHARS:
                        err("cornice_nominato", cid, r,
                            f"{cid}: who ref {r!r} assente da entities.characters")
            wid = (c.get("where") or {}).get("location_id")
            if wid and wid not in EXT:
                err("cornice_location", cid, wid,
                    f"{cid}: where.location_id {wid!r} non risolvibile "
                    f"(LOCS∪locations_secondary∪PATHS∪VIS)")

    # -- path_details ↔ catalogo ----------------------------------------------
    for pid in PATHS:
        if pid not in SEC | VIS:
            err("path_details", pid, pid,
                f"path_details.{pid}: id non presente né in locations_secondary "
                f"né come scheda visual/luoghi")

    # -- seeds / callbacks interni --------------------------------------------
    for seed_id, sd in g.get("seeds", {}).items():
        os_ = sd.get("origin_story")
        if os_ and os_ not in stories:
            err("seed_origin", seed_id, str(os_),
                f"seeds.{seed_id}: origin_story {os_!r} inesistente")
    for cb_id, cb in g.get("callbacks", {}).items():
        fs = cb.get("from_story")
        if fs and fs not in stories:
            err("callback_from", cb_id, str(fs),
                f"callbacks.{cb_id}: from_story {fs!r} inesistente")

    # -- warning: contains + copertura catalogo --------------------------------
    for lid, l in ents.get("locations", {}).items():
        for c in l.get("contains", []) or []:
            if c not in LOCS | VIS:
                warn(f"locations.{lid}.contains: {c!r} non risolto "
                     f"(alias legacy? campo descrittivo)")
    vis_pers = set()
    base = REPO / "visual" / "personaggi"
    if base.exists():
        vis_pers = {p.name for p in base.rglob("*")
                    if p.is_dir() and (p / "scheda.md").exists()}
    for c in sorted(CHARS - vis_pers):
        warn(f"entities.characters.{c}: nessuna scheda visual corrispondente")
    vis_obj = set()
    base = REPO / "visual" / "oggetti"
    if base.exists():
        vis_obj = {p.name for p in base.iterdir() if p.is_dir()}
    for o in sorted(OBJS - vis_obj):
        warn(f"entities.objects.{o}: nessuna scheda visual corrispondente")

    # -- baseline incoerenze note ----------------------------------------------
    baseline = load_known_issues()
    known_keys = {(i.get("kind"), i.get("where"), i.get("ref")) for i in baseline}
    real_errors, known_hits = [], []
    for kind, where, ref, msg in errors:
        if (kind, where, ref) in known_keys:
            known_hits.append((kind, where, ref, msg))
        else:
            real_errors.append(msg)
    found_keys = {(k, w, r) for k, w, r, _ in errors}
    stale = [i for i in baseline
             if (i.get("kind"), i.get("where"), i.get("ref")) not in found_keys]

    for _, _, _, msg in known_hits:
        print(f"  [known] {msg}")
    for s_ in stale:
        warn(f"baseline stantia (incoerenza risolta? rimuovi da known_issues.yaml): "
             f"{s_.get('kind')}/{s_.get('where')}/{s_.get('ref')}")
    for w in warnings:
        print(f"  [warn] {w}")

    if real_errors:
        print(f"\nFAIL — {len(real_errors)} errori referenziali NUOVI"
              f" ({len(known_hits)} noti in baseline):")
        for m in real_errors:
            print(f"  ✗ {m}")
        return 1
    print(f"\nPASS — riferimenti risolti. "
          f"{len(known_hits)} incoerenze note in baseline, "
          f"{len(warnings)} warning informativi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
