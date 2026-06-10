#!/usr/bin/env python3
"""
audit_2_schema.py — Schema a riposo: hook, cornici, world_conventions.

Check indipendente sul grafo A RIPOSO (sola lettura). Replica i vincoli del
writer `scripts/write_hooks_to_graph.py` come verifica esterna, e li estende
alle strutture aggiunte dalla fase "cornice del mondo".

HOOK (per ognuna delle 12 storie):
  - esattamente 10 hook in visual_anchors.scene_hooks
  - hook_id pattern sNN_hMM, prefisso = storia, sequenza 01..10
  - campi obbligatori presenti e non vuoti: hook_id, type, is_signature,
    provenance, moment, location, characters_present, focal_action,
    atmosphere, palette, composition_zone
  - enum: type ∈ {panorama, azione, introspettivo, atmosferico, transizione,
    interno, dettaglio}; provenance ∈ {original_v1, extended_v2};
    composition_zone ∈ {sky_space, fog_space, ground_space, side_space,
    vignette, corner_lower_left, corner_lower_right}
  - is_signature booleano; max 3 signature per storia
  - focal_action ≤ 30 parole (regola operativa del writer; NB: alcune
    docstring storiche dicono 25 — il dato reale e il codice dicono 30)
  - almeno 4 type diversi per storia; mai più di 3 hook consecutivi
    dello stesso type
  - quadrant (se presente) coerente con entities.locations[location.id].quadrant

CORNICI (cornice_dettagli, fase Cornice del Mondo):
  - esattamente 2 per storia (24 totali)
  - id pattern sNN_cK coerente con la storia
  - campi obbligatori: id, story, type, who{kind, ref}, where{location_id},
    what
  - who.kind ∈ {gruppo, nominato, nominati, anonimo} (DOC_3 + estensione
    step8 2026-06-10: 'nominati' = coppie/triplette nominate insieme);
    who.ref obbligatorio per gruppo/nominato; who.refs lista (>=2)
    obbligatoria per nominati; null ammesso per anonimo

WORLD_CONVENTIONS:
  - refrain_animal_identification presente
  - path_details.paths: esattamente i 5 sentieri Tier A attesi,
    ognuno con tier == "A" e details non vuoti; totale dettagli == 20

QUOTE_TRACKER: presente, dict non vuoto.

Convenzione output: exit 0 = PASS, exit 1 = FAIL.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GRAPH = REPO / "pipeline_narrativa" / "story_graph.json"

VALID_TYPES = {
    "panorama", "azione", "introspettivo", "atmosferico",
    "transizione", "interno", "dettaglio",
}
VALID_COMPOSITION_ZONES = {
    "sky_space", "fog_space", "ground_space", "side_space",
    "vignette", "corner_lower_left", "corner_lower_right",
}
VALID_PROVENANCE = {"original_v1", "extended_v2"}
HOOK_ID_RE = re.compile(r"^s(\d{2})_h(\d{2})$")
CORNICE_ID_RE = re.compile(r"^s(\d{2})_c(\d+)$")
REQUIRED_HOOK_FIELDS = (
    "hook_id", "type", "is_signature", "provenance", "moment",
    "location", "characters_present", "focal_action", "atmosphere",
    "palette", "composition_zone",
)
REQUIRED_CORNICE_FIELDS = ("id", "story", "type", "who", "where", "what")
FOCAL_ACTION_MAX_WORDS = 30
EXPECTED_TIER_A_PATHS = {
    "via_dell_alba",
    "sentiero_orti_torrente_foresta",
    "via_che_sale",
    "sentiero_orti_casa_salvia",
    "viottolo_perimetrale_piazza",
}
EXPECTED_PATH_DETAILS_TOTAL = 20
STORY_IDS = tuple(f"s{i:02d}" for i in range(1, 13))

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def is_blank(v) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def check_hooks(sid: str, story: dict, graph: dict) -> None:
    va = story.get("visual_anchors") or {}
    hooks = va.get("scene_hooks")
    if not isinstance(hooks, list):
        err(f"{sid}: visual_anchors.scene_hooks assente o non-lista")
        return
    if len(hooks) != 10:
        err(f"{sid}: attesi 10 hook, trovati {len(hooks)}")

    locs = graph["entities"]["locations"]
    types_seen: list[str] = []
    sig_count = 0

    for i, h in enumerate(hooks, start=1):
        prefix = f"{sid} hook[{i}]"
        if not isinstance(h, dict):
            err(f"{prefix}: non è un oggetto")
            continue

        for f in REQUIRED_HOOK_FIELDS:
            if f not in h:
                err(f"{prefix}: campo obbligatorio mancante: {f}")
            elif is_blank(h[f]):
                err(f"{prefix}: campo obbligatorio vuoto/nullo: {f}")

        hid = h.get("hook_id", "")
        m = HOOK_ID_RE.match(str(hid))
        if not m:
            err(f"{prefix}: hook_id {hid!r} non rispetta pattern sNN_hMM")
        else:
            if m.group(1) != sid[1:]:
                err(f"{prefix}: hook_id {hid!r} non corrisponde a {sid}")
            if int(m.group(2)) != i:
                err(f"{prefix}: hook_id {hid!r} fuori sequenza (atteso h{i:02d})")

        t = h.get("type")
        if t not in VALID_TYPES:
            err(f"{prefix}: type {t!r} non in enum")
        types_seen.append(t)

        if h.get("provenance") not in VALID_PROVENANCE:
            err(f"{prefix}: provenance {h.get('provenance')!r} non valida")

        if h.get("composition_zone") not in VALID_COMPOSITION_ZONES:
            err(f"{prefix}: composition_zone {h.get('composition_zone')!r} non in enum")

        if not isinstance(h.get("is_signature"), bool):
            err(f"{prefix}: is_signature deve essere booleano")
        elif h["is_signature"]:
            sig_count += 1

        fa = h.get("focal_action") or ""
        n_words = len(str(fa).split())
        if n_words > FOCAL_ACTION_MAX_WORDS:
            err(f"{prefix}: focal_action {n_words} parole > {FOCAL_ACTION_MAX_WORDS}")

        loc = h.get("location")
        loc_id = loc.get("id") if isinstance(loc, dict) else None
        explicit_q = h.get("quadrant")
        if loc_id and loc_id in locs:
            derived_q = locs[loc_id].get("quadrant")
            if explicit_q and derived_q and explicit_q != derived_q:
                err(f"{prefix}: quadrant {explicit_q!r} ≠ quadrant location "
                    f"{loc_id!r} ({derived_q!r})")
        # (esistenza di loc_id in entities → audit_3)

    if types_seen and len(set(t for t in types_seen if t)) < 4:
        err(f"{sid}: tipologie diverse {len(set(types_seen))} < 4")

    streak = 1
    for j in range(1, len(types_seen)):
        if types_seen[j] is not None and types_seen[j] == types_seen[j - 1]:
            streak += 1
            if streak > 3:
                err(f"{sid}: più di 3 hook consecutivi stesso type "
                    f"({types_seen[j]!r}, intorno al hook {j + 1})")
                break
        else:
            streak = 1

    if sig_count > 3:
        err(f"{sid}: signature {sig_count} > 3")


def check_cornici(sid: str, story: dict) -> None:
    cornici = story.get("cornice_dettagli")
    if not isinstance(cornici, list):
        err(f"{sid}: cornice_dettagli assente o non-lista")
        return
    if len(cornici) != 2:
        err(f"{sid}: attese 2 cornici, trovate {len(cornici)}")
    for c in cornici:
        if not isinstance(c, dict):
            err(f"{sid}: cornice non-oggetto")
            continue
        cid = c.get("id", "?")
        prefix = f"{sid} cornice {cid}"
        for f in REQUIRED_CORNICE_FIELDS:
            if f not in c or is_blank(c[f]):
                err(f"{prefix}: campo obbligatorio mancante/vuoto: {f}")
        m = CORNICE_ID_RE.match(str(cid))
        if not m or m.group(1) != sid[1:]:
            err(f"{prefix}: id non rispetta pattern sNN_cK per {sid}")
        if c.get("story") != sid:
            err(f"{prefix}: campo story {c.get('story')!r} ≠ {sid}")
        who = c.get("who")
        if isinstance(who, dict):
            kind = who.get("kind")
            # Estensione step8 (2026-06-10): 'nominati' = coppia/tripletta
            # nominata insieme nella stessa cornice, usa who.refs lista.
            if kind not in {"gruppo", "nominato", "nominati", "anonimo"}:
                err(f"{prefix}: who.kind {kind!r} non in "
                    f"{{gruppo, nominato, nominati, anonimo}} (DOC_3)")
            if kind in {"gruppo", "nominato"} and is_blank(who.get("ref")):
                err(f"{prefix}: who.ref vuoto (obbligatorio per kind={kind})")
            if kind == "nominati":
                refs = who.get("refs")
                if not isinstance(refs, list) or len(refs) < 2:
                    err(f"{prefix}: who.refs lista non vuota (>=2) "
                        f"obbligatoria per kind=nominati")
            if kind == "anonimo" and not is_blank(who.get("ref")):
                err(f"{prefix}: who.ref {who.get('ref')!r} valorizzato "
                    f"con kind=anonimo")
        else:
            err(f"{prefix}: who non è un oggetto")
        where = c.get("where")
        if not isinstance(where, dict) or is_blank(where.get("location_id")):
            err(f"{prefix}: where.location_id assente/vuoto")


def check_world_conventions(g: dict) -> None:
    wc = g.get("world_conventions")
    if not isinstance(wc, dict):
        err("world_conventions assente o non-oggetto")
        return
    if "refrain_animal_identification" not in wc:
        err("world_conventions.refrain_animal_identification assente")
    pd = wc.get("path_details", {})
    paths = pd.get("paths") if isinstance(pd, dict) else None
    if not isinstance(paths, dict):
        err("world_conventions.path_details.paths assente o non-oggetto")
        return
    got = set(paths)
    if got != EXPECTED_TIER_A_PATHS:
        missing = EXPECTED_TIER_A_PATHS - got
        extra = got - EXPECTED_TIER_A_PATHS
        if missing:
            err(f"path_details: sentieri Tier A mancanti: {sorted(missing)}")
        if extra:
            err(f"path_details: sentieri inattesi: {sorted(extra)} "
                f"(se è un'estensione autorizzata, aggiorna EXPECTED_TIER_A_PATHS)")
    total_details = 0
    for pid, p in paths.items():
        if p.get("tier") != "A":
            err(f"path_details.{pid}: tier {p.get('tier')!r} ≠ 'A'")
        details = p.get("details") or []
        if not details:
            err(f"path_details.{pid}: details vuoti")
        total_details += len(details)
    if total_details != EXPECTED_PATH_DETAILS_TOTAL:
        err(f"path_details: dettagli totali {total_details} ≠ "
            f"{EXPECTED_PATH_DETAILS_TOTAL} attesi")


def main() -> int:
    print(f"== audit_2_schema — {GRAPH.relative_to(REPO)} ==")
    try:
        g = json.loads(GRAPH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL — grafo non leggibile/parseable: {e}")
        return 1

    stories = g.get("stories", {})
    for sid in STORY_IDS:
        s = stories.get(sid)
        if not isinstance(s, dict):
            err(f"{sid}: storia assente (vedi audit_1)")
            continue
        check_hooks(sid, s, g)
        check_cornici(sid, s)

    check_world_conventions(g)

    qt = g.get("quote_tracker")
    if not isinstance(qt, dict) or not qt:
        err("quote_tracker assente o vuoto")

    if errors:
        print(f"\nFAIL — {len(errors)} errori:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    n_hooks = sum(len(stories[s]["visual_anchors"]["scene_hooks"]) for s in STORY_IDS)
    print(f"PASS — {n_hooks} hook, 24 cornici, world_conventions conformi allo schema 1.4.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
