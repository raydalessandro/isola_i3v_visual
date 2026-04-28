#!/usr/bin/env python3
"""P1 carpentiere meccanico: porta old_node v1.1 -> canonical v1.2.

Uso:
  python3 migrate_p1.py s02

Legge:
  _porting_grafo/dossier_fase_e/dossier/INPUT_NODES/<sNN>_input.json
  _porting_grafo/output/<sNN>/_p1_mapping.json (decisioni manuali da P0: hook + quadrant + sottotipo personaggi_vincoli)

Scrive:
  _porting_grafo/output/<sNN>/<sNN>_canonical.json
"""
import json
import sys
from pathlib import Path

# REGOLA 0.5 — rinomine enum legacy v1.1 -> canonical v1.2
ENUM_RENAMES = {
    "attribute_dominant": {
        "delta": "distinguere",
        "connettere_sottile": "connettere",  # s06: nota va in structural_notes
    }
}

def migrate(story_id: str):
    repo = Path(__file__).resolve().parents[2]
    in_path = repo / f"_porting_grafo/dossier_fase_e/dossier/INPUT_NODES/{story_id}_input.json"
    map_path = repo / f"_porting_grafo/output/{story_id}/_p1_mapping.json"
    out_path = repo / f"_porting_grafo/output/{story_id}/{story_id}_canonical.json"

    src = json.loads(in_path.read_text())
    on = src["old_node"]
    mapping = json.loads(map_path.read_text())

    # ----- TOP-LEVEL -----
    canonical = {
        "id": on["id"],
        "title_provvisorio": on["title_provvisorio"],
        "cycle": on["cycle"],
        "attribute_dominant": ENUM_RENAMES["attribute_dominant"].get(
            on["attribute_dominant"], on["attribute_dominant"]
        ),
        "block_position": on.get("block_position"),
        "season": on["season"],
        "season_passage": on.get("season_passage"),
        "wind_active": on.get("wind_active"),
        "wind_notes": on.get("wind_notes"),
        "pattern_a_active": on.get("pattern_a_active", "none"),
        "pattern_a_notes": on.get("pattern_a_notes"),
        "night_scene": on.get("night_scene", False),
        "night_scene_notes": on.get("night_scene_notes"),
        "when_water_trembles": on.get("when_water_trembles", False),
    }

    # location_primary: {id, note, role}. Accorpa _note + specific_points info se presenti.
    lp_old = on["location_primary"]
    lp_note_parts = []
    if lp_old.get("_note"):
        lp_note_parts.append(lp_old["_note"])
    if lp_old.get("specific_points"):
        lp_note_parts.append(f"specific_points: {lp_old['specific_points']}")
    canonical["location_primary"] = {"id": lp_old["id"]}
    if lp_note_parts:
        canonical["location_primary"]["note"] = " | ".join(lp_note_parts)

    # locations_secondary: rinomina scene_role -> role; tiene id
    canonical["locations_secondary"] = [
        {"id": s["id"], "role": s.get("scene_role") or s.get("role", "")}
        for s in on.get("locations_secondary", [])
    ]

    # characters_in_scene: copia campi rilevanti (no rinomine)
    canonical["characters_in_scene"] = on.get("characters_in_scene", [])
    canonical["characters_offscreen_or_background"] = on.get("characters_offscreen_or_background", [])

    # seeds: copia diretta
    canonical["seeds_planted"] = on.get("seeds_planted", [])
    canonical["seeds_picked_up"] = on.get("seeds_picked_up", [])
    canonical["seeds_maturing_here"] = on.get("seeds_maturing_here", [])
    canonical["seeds_bloomed_here"] = on.get("seeds_bloomed_here", [])

    canonical["callbacks_made"] = on.get("callbacks_made", [])
    canonical["callback_summary"] = on.get("callback_summary", "")

    # debts: REGOLA 0ter — i seed_refs del precomputed_context vengono archiviati (non vanno nel canonical)
    canonical["debts_opened"] = mapping.get("debts_opened_keep", [])
    canonical["debts_closed"] = mapping.get("debts_closed_keep", [])

    canonical["key_phrase_indicative"] = on.get("key_phrase_indicative")
    canonical["key_phrase_notes"] = on.get("key_phrase_notes")
    # premise/problem/threshold/resolution: copia identica REGOLA 2
    for k in ("premise", "problem", "threshold_moment", "resolution_mode", "palette_emotiva"):
        canonical[k] = on.get(k, "")

    canonical["active_constraints_touched"] = on.get("active_constraints_touched", [])
    canonical["voice_notes_essential"] = on.get("voice_notes_essential", [])
    canonical["structural_notes"] = on.get("structural_notes", [])

    if on.get("fear_touched"):
        canonical["fear_touched"] = on["fear_touched"]

    # ----- visual_anchors -----
    hooks_new = []
    for h_old in on.get("visual_anchors", {}).get("scene_hooks", []):
        hid = h_old["hook_id"]
        hmap = mapping["hooks"][hid]
        h_new = {
            "hook_id": hid,
            "moment": h_old.get("time_of_day") or hmap.get("moment", ""),
            "location": {
                "id": hmap["location"]["id"],
                "qualifier": hmap["location"]["qualifier"],
                "legacy_string": hmap["location"]["legacy_string"],
            },
            "quadrant": hmap.get("quadrant", h_old.get("quadrant")),
            "characters_present": h_old.get("characters_present", []),
            "elements": h_old.get("elements", []),
            "palette": h_old.get("palette_local", h_old.get("palette", "")),
            "notes": h_old.get("notes"),
            "focal_action": h_old.get("focal_action"),
            "focal_object": h_old.get("focal_object"),
            "atmosphere": h_old.get("atmosphere"),
            "wind_visible": h_old.get("wind_visible"),
            "onomatopee": h_old.get("onomatopee", []),
        }
        hooks_new.append(h_new)
    canonical["visual_anchors"] = {"scene_hooks": hooks_new}

    # ----- 13 nuovi campi v1.2 -----
    # 5 no_inference_fields -> null
    canonical["entry_point_type"] = None
    canonical["closure_type"] = None
    canonical["register"] = None
    canonical["estimated_length"] = None
    canonical["descriptive_pauses_count"] = None

    # 4 flag da precomputed_context
    flags = src.get("precomputed_context", {}).get("flags_quote_tracker", {})
    canonical["grunto_memory_fragment"] = flags.get("grunto_memory_fragment", False)
    canonical["paronomastico_used"] = flags.get("paronomastico_used", False)
    canonical["narrator_address"] = flags.get("narrator_address", False)
    canonical["narrator_meta_voice"] = flags.get("narrator_meta_voice", False)
    canonical["onomatopee_firma"] = flags.get("onomatopee_firma", [])

    # quartieri_attraversati: derivato dai quadrant degli hook (distinct, ordine apparizione)
    quartieri = []
    for h in hooks_new:
        q = h["quadrant"]
        if q and q not in quartieri:
            quartieri.append(q)
    canonical["quartieri_attraversati"] = quartieri

    # oggetti_simbolo_presenti: da recurring_visual_objects
    canonical["oggetti_simbolo_presenti"] = on.get("visual_anchors", {}).get("recurring_visual_objects", [])

    # personaggi_vincoli_attivi: da mapping (manuale, riferito a character_constraints.json)
    canonical["personaggi_vincoli_attivi"] = mapping.get("personaggi_vincoli_attivi", [])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(canonical, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote: {out_path}")
    print(f"Top-level fields: {len(canonical)}")
    print(f"Hooks: {len(hooks_new)}")
    print(f"attribute_dominant: {canonical['attribute_dominant']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: migrate_p1.py <story_id>", file=sys.stderr)
        sys.exit(1)
    migrate(sys.argv[1])
