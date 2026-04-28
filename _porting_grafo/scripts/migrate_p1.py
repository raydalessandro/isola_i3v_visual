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
import re
import sys
from pathlib import Path

# REGOLA 0.5 — rinomine enum legacy v1.1 -> canonical v1.2
ENUM_RENAMES = {
    "attribute_dominant": {
        "delta": "distinguere",
        "connettere_sottile": "connettere",  # s06: nota va in structural_notes
    }
}

# REGOLA 0.10 — season deve essere in enum ['primavera','estate','autunno','inverno']
SEASON_ENUM = {"primavera", "estate", "autunno", "inverno"}
SEASON_NORMALIZE = {
    # Storia: storia inizia/cade in PRIMA stagione, passaggio narrativo verso seconda
    "passaggio_primavera_estate": ("primavera", "passaggio_primavera_estate"),
    "estate_piena": ("estate", None),
    "estate_piena_tarda": ("estate", None),
    "passaggio_estate_autunno": ("estate", "passaggio_estate_autunno"),
    "autunno_pieno": ("autunno", None),
}


def normalize_season(value: str, current_season_passage):
    """REGOLA 0.10 (post-s06): season legacy fuori enum -> canonical + season_passage.
    Ritorna (season_canonical, season_passage). Se old_node ha gia' season_passage
    valorizzato, viene preservato (override sul default derivato)."""
    if value in SEASON_ENUM:
        return value, current_season_passage
    if value in SEASON_NORMALIZE:
        canonical, default_passage = SEASON_NORMALIZE[value]
        # se old_node ha gia' season_passage valorizzato, preserva
        return canonical, current_season_passage if current_season_passage else default_passage
    raise ValueError(f"season '{value}' non normalizzabile: aggiungi a SEASON_NORMALIZE")


# REGOLA 0.9 — block_position deve matchare ^(apertura|centro|chiusura)_blocco_[abcd]$
BLOCK_POSITION_PATTERN = re.compile(r"^(apertura|centro|chiusura)_blocco_[abcd]$")
BLOCK_POSITION_MAP = {
    "apertura_saga": "apertura_blocco_a",  # s01
}
BLOCK_POSITION_TRUNCATE = re.compile(r"^((?:apertura|centro|chiusura)_blocco_[abcd])(_.+)?$")


def normalize_block_position(value: str) -> str:
    """REGOLA 0.9 (post-s03): block_position legacy -> canonical pattern v1.2.
    1) Mappa esplicita per nomi semantici (apertura_saga -> apertura_blocco_a).
    2) Tronca suffissi semantici (chiusura_blocco_a_passaggio_stagionale ->
       chiusura_blocco_a). Info estesa va conservata in structural_notes.
    3) Se gia' canonico: invariato."""
    if value in BLOCK_POSITION_MAP:
        return BLOCK_POSITION_MAP[value]
    if BLOCK_POSITION_PATTERN.match(value):
        return value
    m = BLOCK_POSITION_TRUNCATE.match(value)
    if m:
        return m.group(1)
    raise ValueError(f"block_position '{value}' non normalizzabile: aggiungi al mapping in migrate_p1.py")

def load_canonical_oggetti(repo: Path) -> set:
    """Lista degli ID oggetti canonici dal catalogo (famiglia=oggetto)."""
    cat = json.loads((repo / "catalogo_web/data/entities.json").read_text())
    return {x["id"] for x in cat["entities"] if x.get("famiglia") == "oggetto"}


DISTINCT_FROM_PATTERN = re.compile(r"^distinct_from_s\d+$")


def normalize_characters_in_scene(characters: list) -> list:
    """REGOLA 1bis (post-s05): characters_in_scene[*].distinct_from_s<NN> ->
    distinct_from_other_story (campo canonico schema v1.2). Il valore stringa
    contiene gia' l'info su quale storia distinguere; va preservato."""
    out = []
    for ch in characters:
        ch_new = {}
        for k, v in ch.items():
            if DISTINCT_FROM_PATTERN.match(k):
                # rinomina a campo canonico; se gia' presente per qualche
                # motivo, concatena (caso edge non osservato finora).
                if "distinct_from_other_story" in ch_new:
                    ch_new["distinct_from_other_story"] += " | " + v
                else:
                    ch_new["distinct_from_other_story"] = v
            else:
                ch_new[k] = v
        out.append(ch_new)
    return out


def normalize_callbacks(callbacks: list, story_id: str) -> list:
    """REGOLA 1bis (post-s02): callbacks_made richiede to_story (schema v1.2).
    Se manca: deriva to_story = story_id corrente (il callback e' fatto IN questa storia
    da un'altra storia di provenienza). Mantiene registered_in_story se presente."""
    out = []
    for cb in callbacks:
        cb_new = dict(cb)
        if "to_story" not in cb_new:
            cb_new["to_story"] = cb.get("registered_in_story") or story_id
        out.append(cb_new)
    return out


def filter_oggetti_simbolo(recurring: list, canonical_oggetti: set) -> tuple[list, list]:
    """Regola §8.2 esplicitata (post-s02): oggetti_simbolo_presenti accetta SOLO ID
    in catalogo come famiglia=oggetto (13 oggetti canonici saga). Tutto il resto
    (oggetti-firma personaggio, oggetti di scena non catalogati) viene scartato e
    riportato nei misalignments dell'output di P1.
    Ritorna (kept, dropped)."""
    kept = [x for x in recurring if x in canonical_oggetti]
    dropped = [x for x in recurring if x not in canonical_oggetti]
    return kept, dropped


def migrate(story_id: str):
    repo = Path(__file__).resolve().parents[2]
    in_path = repo / f"_porting_grafo/dossier_fase_e/dossier/INPUT_NODES/{story_id}_input.json"
    map_path = repo / f"_porting_grafo/output/{story_id}/_p1_mapping.json"
    out_path = repo / f"_porting_grafo/output/{story_id}/{story_id}_canonical.json"

    src = json.loads(in_path.read_text())
    on = src["old_node"]
    mapping = json.loads(map_path.read_text())

    # ----- TOP-LEVEL -----
    season_canonical, season_passage = normalize_season(on["season"], on.get("season_passage"))
    canonical = {
        "id": on["id"],
        "title_provvisorio": on["title_provvisorio"],
        "cycle": on["cycle"],
        "attribute_dominant": ENUM_RENAMES["attribute_dominant"].get(
            on["attribute_dominant"], on["attribute_dominant"]
        ),
        "block_position": normalize_block_position(on["block_position"]),
        "season": season_canonical,
        "season_passage": season_passage,
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
    canonical["characters_in_scene"] = normalize_characters_in_scene(on.get("characters_in_scene", []))
    canonical["characters_offscreen_or_background"] = on.get("characters_offscreen_or_background", [])

    # seeds: copia diretta
    canonical["seeds_planted"] = on.get("seeds_planted", [])
    canonical["seeds_picked_up"] = on.get("seeds_picked_up", [])
    canonical["seeds_maturing_here"] = on.get("seeds_maturing_here", [])
    canonical["seeds_bloomed_here"] = on.get("seeds_bloomed_here", [])

    canonical["callbacks_made"] = normalize_callbacks(on.get("callbacks_made", []), story_id)
    canonical["callback_summary"] = on.get("callback_summary", "")

    # debts: REGOLA 0ter — i seed_refs del precomputed_context vengono archiviati (non vanno nel canonical)
    canonical["debts_opened"] = mapping.get("debts_opened_keep", [])
    canonical["debts_closed"] = mapping.get("debts_closed_keep", [])

    canonical["key_phrase_indicative"] = on.get("key_phrase_indicative")
    canonical["key_phrase_notes"] = on.get("key_phrase_notes")
    # key_phrase_attributed_to (campo opzionale schema v1.2): popolato solo se P0 lo
    # dichiara nel _p1_mapping.json (es. s03 con frase di Rovo). Per le storie con
    # key_phrase del narratore o null, il campo va aggiunto da Ray in fase D quando
    # popola key_phrase_indicative. Cf. REGOLA 0.8 MIGRATION_PROMPT.
    if "key_phrase_attributed_to" in mapping:
        canonical["key_phrase_attributed_to"] = mapping["key_phrase_attributed_to"]
    # premise/problem/threshold/resolution: copia identica REGOLA 2
    for k in ("premise", "problem", "threshold_moment", "resolution_mode", "palette_emotiva"):
        canonical[k] = on.get(k, "")

    canonical["active_constraints_touched"] = on.get("active_constraints_touched", [])
    canonical["voice_notes_essential"] = on.get("voice_notes_essential", [])
    canonical["structural_notes"] = on.get("structural_notes", [])

    if on.get("fear_touched"):
        canonical["fear_touched"] = on["fear_touched"]

    # ----- visual_anchors -----
    # REGOLA 3: caso s06 string_legacy. Se hook e' una stringa, mapping deve
    # fornire 'hook_dict' completo (parsing manuale fatto in P0).
    hooks_new = []
    for i, h_old in enumerate(on.get("visual_anchors", {}).get("scene_hooks", [])):
        if isinstance(h_old, str):
            hid_default = f"{story_id}_h{i+1}"
            hmap = mapping["hooks"].get(hid_default) or mapping["hooks"].get(f"{story_id}_h{i+1}_signature")
            if hmap is None or "hook_dict" not in hmap:
                raise ValueError(f"string_legacy hook {hid_default}: mapping deve fornire 'hook_dict' completo (REGOLA 3 MIGRATION_PROMPT)")
            h_new = dict(hmap["hook_dict"])
            # preserva la stringa legacy come prima entry di elements per tracciabilita'.
            # notes resta null -> P2 puo' popolarla narrativamente.
            legacy_marker = f"FONTE_LEGACY: {h_old}"
            h_new["elements"] = [legacy_marker] + list(h_new.get("elements", []))
            h_new.setdefault("notes", None)
            hooks_new.append(h_new)
            continue
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

    # oggetti_simbolo_presenti: filtra recurring_visual_objects contro catalogo (solo famiglia=oggetto)
    canonical_oggetti = load_canonical_oggetti(repo)
    recurring = on.get("visual_anchors", {}).get("recurring_visual_objects") or []
    kept, dropped = filter_oggetti_simbolo(recurring, canonical_oggetti)
    canonical["oggetti_simbolo_presenti"] = kept
    # `dropped` viene riportato a stdout: l'operatore aggiorna manualmente
    # _canon_misalignments.json (object_missing_from_catalog o oggetto_firma_personaggio).

    # personaggi_vincoli_attivi: da mapping (manuale, riferito a character_constraints.json)
    canonical["personaggi_vincoli_attivi"] = mapping.get("personaggi_vincoli_attivi", [])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(canonical, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote: {out_path}")
    print(f"Top-level fields: {len(canonical)}")
    print(f"Hooks: {len(hooks_new)}")
    print(f"attribute_dominant: {canonical['attribute_dominant']}")
    print(f"callbacks_made: {len(canonical['callbacks_made'])} (to_story derivato dove mancante)")
    print(f"oggetti_simbolo_presenti (canonici): {kept}")
    if dropped:
        print(f"  WARN: dropped da recurring_visual_objects (non in catalogo come famiglia=oggetto): {dropped}")
        print(f"        -> aggiungere mis_<NNN> in _canon_misalignments.json (type: oggetto_firma_personaggio | object_missing_from_catalog)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: migrate_p1.py <story_id>", file=sys.stderr)
        sys.exit(1)
    migrate(sys.argv[1])
