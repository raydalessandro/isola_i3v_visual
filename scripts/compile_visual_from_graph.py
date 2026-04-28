#!/usr/bin/env python3
"""Fase F.1: travaso meccanico grafo v1.0.0 -> schede visual.

Per ogni scheda con sezioni '_da popolare dal grafo_', popola SOLO con
dati esistenti nel grafo (no inferenza, no invenzione). Preserva il resto.

Sezioni mappate per famiglia:
- personaggio:
  - 'Identità visuale (sintesi)' <- role_saga + type + species + attribute_ear + age_band
  - 'Espressione / comportamento' <- voice_notes + narrative_function
  - 'Cliché da evitare' <- character_constraints.json[id]
  - 'Storie / scene di apparizione' <- scan 12 canonical (characters_in_scene)
- luogo:
  - 'Identità visuale (sintesi)' <- type + quadrant + role_saga
  - 'Contesto e ambientazioni ricorrenti' <- quadrant + position + inhabitant
  - 'Storie / scene di apparizione' <- scan 12 canonical
- oggetto:
  - 'Identità visuale (sintesi)' <- category + saga_role + owner
  - 'Aspetto / forma' (se vuoto) <- description
  - 'Storie / scene di apparizione' <- scan canonical
- vento:
  - 'Identità visuale (sintesi)' <- effect + origin_spirit + attribute_ear
  - 'Aspetto / forma' <- visual_profile
  - 'Espressione / comportamento' <- time_of_day + direction
  - 'Storie / scene di apparizione' <- scan canonical wind_active
- visual_signature:
  - 'Identità visuale (sintesi)' <- description + type + constraint

Sezioni che restano '_da popolare dal grafo_' (no dato grafo):
  Variabilità ammessa, Per stampa 3D, Per narrativa e social
  (lavoro fase D/F autoriale).
"""
import json
import re
from pathlib import Path

REPO = Path("/home/user/isola_i3v_visual")
STUB = "_da popolare dal grafo_"

# Carica fonti
GRAPH = json.loads((REPO / "pipeline_narrativa/story_graph.json").read_text())
CHAR_CONSTRAINTS = json.loads((REPO / "_porting_grafo/dossier_fase_e/dossier/character_constraints.json").read_text())

# Carica 12 canonical
CANONICAL = {}
for n in range(1, 13):
    sid = f"s{n:02d}"
    CANONICAL[sid] = json.loads((REPO / f"_porting_grafo/output/{sid}/{sid}_canonical.json").read_text())


# ------- helpers -------

def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not m: return None, text
    fm_text, body = m.groups()
    # parse YAML manualmente per evitare dipendenza
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"')
    return fm, body


def replace_section(body: str, section_title: str, new_content: str) -> str:
    """Trova `## <section_title>` e sostituisce contenuto fino al prossimo ## (o fine).
    Sostituisce SOLO se il contenuto attuale e' lo stub marker (case insensitive)."""
    pattern = re.compile(
        rf"(##\s+{re.escape(section_title)}\s*\n)(.*?)(?=\n## |\Z)",
        re.DOTALL,
    )
    m = pattern.search(body)
    if not m: return body
    current = m.group(2).strip()
    # Sostituisce solo se la sezione e' "vuota" (= solo stub marker o whitespace).
    if current == STUB:
        return body[:m.start(2)] + "\n" + new_content.strip() + "\n\n" + body[m.end(2):]
    return body


def find_in_canonical(entity_id: str, kind: str):
    """kind: 'character' | 'location' | 'object'.
    Ritorna lista di (story_id, info_dict) per ogni storia in cui entity_id appare."""
    out = []
    for sid, can in CANONICAL.items():
        appearances = []
        if kind == "character":
            for ch in can.get("characters_in_scene", []):
                if ch.get("id") == entity_id:
                    role = ch.get("role", "")
                    nw = ch.get("narrative_weight", "")
                    appearances.append(f"in scena (role: {role})" + (f" — peso: {nw}" if nw else ""))
            for ch in can.get("characters_offscreen_or_background", []):
                if isinstance(ch, dict) and ch.get("id") == entity_id:
                    appearances.append(f"off-screen (role: {ch.get('role','')})")
                elif isinstance(ch, str) and ch == entity_id:
                    appearances.append("off-screen")
        elif kind == "location":
            if can.get("location_primary", {}).get("id") == entity_id:
                appearances.append("location_primary")
            for ls in can.get("locations_secondary", []):
                if ls.get("id") == entity_id:
                    appearances.append(f"location_secondary (role: {ls.get('role','')[:80]})")
            for h in can.get("visual_anchors", {}).get("scene_hooks", []):
                if h.get("location", {}).get("id") == entity_id:
                    appearances.append(f"scene_hook {h['hook_id']} (qualifier: {h['location'].get('qualifier','')})")
        elif kind == "object":
            for h in can.get("visual_anchors", {}).get("scene_hooks", []):
                if h.get("focal_object") == entity_id:
                    appearances.append(f"focal_object hook {h['hook_id']}")
            if entity_id in can.get("oggetti_simbolo_presenti", []):
                appearances.append("oggetti_simbolo_presenti")
        elif kind == "wind":
            if can.get("wind_active") == entity_id:
                appearances.append(f"wind_active")
        elif kind == "visual_signature":
            if entity_id == "quando_acqua_trema" and can.get("when_water_trembles"):
                appearances.append("when_water_trembles=true")
        if appearances:
            out.append((sid, " | ".join(appearances)))
    return out


def fmt_appearances_block(items, total_storie=12):
    """Format Storie/scene di apparizione block. items: lista (sid, descr)."""
    if not items:
        return ""
    seen = {sid for sid, _ in items}
    lines = []
    for n in range(1, total_storie + 1):
        sid = f"s{n:02d}"
        match = next((d for s, d in items if s == sid), None)
        if match:
            lines.append(f"- **{sid}**: {match}.")
        else:
            lines.append(f"- **{sid}**: assente.")
    return "\n".join(lines)


# ------- compilazione per famiglia -------

def compile_personaggio(entity_id: str, body: str, fm: dict) -> str:
    char = GRAPH["entities"]["characters"].get(entity_id, {})
    if not char:
        return body

    # Identità visuale (sintesi)
    parts = []
    if char.get("role_saga"): parts.append(f"**Ruolo saga:** {char['role_saga']}.")
    if char.get("type"): parts.append(f"**Tipo:** {char['type']}.")
    if char.get("species"): parts.append(f"**Specie:** {char['species']}.")
    if char.get("attribute_ear"): parts.append(f"**Attribute EAR:** {char['attribute_ear']}.")
    if char.get("age_band"): parts.append(f"**Età:** {char['age_band']}.")
    if char.get("familial_role_episodic"): parts.append(f"**Ruolo familiare episodico:** {char['familial_role_episodic']}.")
    if char.get("home_location"): parts.append(f"**Dimora:** {char['home_location']} (quartiere: {char.get('quadrant','?')}).")
    if char.get("narrative_function"):
        parts.append(f"\n*Funzione narrativa (dal grafo):* {char['narrative_function']}")
    if parts:
        body = replace_section(body, "Identità visuale (sintesi)", "\n".join(parts))

    # Espressione / comportamento
    parts = []
    if char.get("voice_notes"):
        parts.append(f"**Voce:** {char['voice_notes']}")
    if char.get("narrative_function"):
        parts.append(f"\n**Comportamento (sintesi grafo):** {char['narrative_function']}")
    fa = char.get("fear_arc")
    if fa:
        parts.append(f"\n**Arco paura:** `{fa.get('fear_id','?')}` — semina pianificata in {fa.get('first_emergence_planned','?')}, "
                     f"bloom in {fa.get('bloomed_in_story','?')}, modo: `{fa.get('resolution_mode','?')}`.")
    if parts:
        body = replace_section(body, "Espressione / comportamento", "\n".join(parts))

    # Cliché da evitare (vincoli da character_constraints.json)
    cc = CHAR_CONSTRAINTS.get(entity_id, [])
    graph_constraints = char.get("constraints", [])
    all_constraints = list(dict.fromkeys(list(cc) + list(graph_constraints)))
    if all_constraints:
        new = "Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.\n\n**Vincoli individuali (da `character_constraints.json` + grafo):**\n"
        for v in all_constraints:
            new += f"- `{v}`\n"
        body = replace_section(body, "Cliché da evitare", new)

    # Storie / scene di apparizione (preserva contenuto esistente solo se stub)
    appearances = find_in_canonical(entity_id, "character")
    if appearances:
        block = fmt_appearances_block(appearances)
        body = replace_section(body, "Storie / scene di apparizione", block)
        # state_by_story aggiuntivo come "Note per storia (dal grafo)"
        sbs = char.get("state_by_story") or {}
        if sbs:
            extra = "\n\n**Note per storia (dal grafo `entities.characters.<id>.state_by_story`):**\n"
            for sid in sorted(sbs.keys()):
                extra += f"- **{sid}**: {sbs[sid]}\n"
            # Append solo se la sezione contiene ora il block (non vuota)
            body = body.replace(block, block + extra, 1)

    return body


def compile_luogo(entity_id: str, body: str, fm: dict) -> str:
    loc = GRAPH["entities"]["locations"].get(entity_id, {})
    if not loc:
        return body

    parts = []
    if loc.get("type"): parts.append(f"**Tipo:** {loc['type']}.")
    if loc.get("quadrant"): parts.append(f"**Quadrante:** {loc['quadrant']}.")
    if loc.get("position"): parts.append(f"**Posizione:** {loc['position']}.")
    if loc.get("inhabitant"): parts.append(f"**Abitante:** {loc['inhabitant']}.")
    if loc.get("role_saga"): parts.append(f"**Ruolo saga:** {loc['role_saga']}.")
    if loc.get("contains"): parts.append(f"**Contiene:** {', '.join(loc['contains'])}.")
    if parts:
        body = replace_section(body, "Identità visuale (sintesi)", "\n".join(parts))

    # Contesto e ambientazioni ricorrenti
    parts = []
    if loc.get("quadrant"): parts.append(f"Quartiere **{loc['quadrant']}**.")
    if loc.get("position"): parts.append(f"Posizione: {loc['position']}.")
    if loc.get("inhabitant"): parts.append(f"Abitante canonico: {loc['inhabitant']}.")
    if loc.get("features"):
        parts.append("\n**Caratteristiche (dal grafo `entities.locations.<id>.features`):**")
        for f in loc["features"]:
            parts.append(f"- {f}")
    if parts:
        body = replace_section(body, "Contesto e ambientazioni ricorrenti", "\n".join(parts))

    # Storie / scene di apparizione
    appearances = find_in_canonical(entity_id, "location")
    if appearances:
        block = fmt_appearances_block(appearances)
        body = replace_section(body, "Storie / scene di apparizione", block)

    return body


def compile_oggetto(entity_id: str, body: str, fm: dict) -> str:
    obj = GRAPH["entities"]["objects"].get(entity_id, {})

    parts = []
    if obj.get("category"): parts.append(f"**Categoria:** {obj['category']}.")
    if obj.get("owner"): parts.append(f"**Proprietario:** {obj['owner']}.")
    if obj.get("origin_location"): parts.append(f"**Origine:** {obj['origin_location']}.")
    if obj.get("saga_role"): parts.append(f"**Ruolo saga:** {obj['saga_role']}.")
    if parts:
        body = replace_section(body, "Identità visuale (sintesi)", "\n".join(parts))

    # Aspetto / forma da description
    if obj.get("description"):
        body = replace_section(body, "Aspetto / forma", obj["description"])

    # Storie
    appearances = find_in_canonical(entity_id, "object")
    if appearances:
        block = fmt_appearances_block(appearances)
        body = replace_section(body, "Storie / scene di apparizione", block)

    return body


def compile_vento(entity_id: str, body: str, fm: dict) -> str:
    w = GRAPH["entities"]["winds"].get(entity_id, {})
    if not w:
        return body

    parts = []
    if w.get("effect"): parts.append(f"**Effetto:** {w['effect']}.")
    if w.get("origin_spirit"): parts.append(f"**Spirito di origine:** {w['origin_spirit']}.")
    if w.get("attribute_ear"): parts.append(f"**Attribute EAR:** {w['attribute_ear']}.")
    if w.get("mirrors_brother"): parts.append(f"**Specchio fratello:** {w['mirrors_brother']}.")
    if parts:
        body = replace_section(body, "Identità visuale (sintesi)", "\n".join(parts))

    # Aspetto / forma da visual_profile (oggetto descrittivo)
    vp = w.get("visual_profile")
    if vp and isinstance(vp, dict):
        block = ""
        for k, v in vp.items():
            block += f"**{k.replace('_',' ')}:** {v}\n\n"
        body = replace_section(body, "Aspetto / forma", block.strip())

    # Espressione / comportamento
    parts = []
    if w.get("time_of_day"): parts.append(f"**Momento della giornata:** {w['time_of_day']}.")
    if w.get("direction"): parts.append(f"**Direzione:** {w['direction']}.")
    if parts:
        body = replace_section(body, "Espressione / comportamento", "\n".join(parts))

    # Storie
    appearances = find_in_canonical(entity_id, "wind")
    if appearances:
        block = fmt_appearances_block(appearances)
        body = replace_section(body, "Storie / scene di apparizione", block)

    return body


def compile_visual_signature(entity_id: str, body: str, fm: dict) -> str:
    vs = GRAPH["entities"]["visual_signatures"].get(entity_id, {})
    if not vs:
        return body

    parts = []
    if vs.get("description"): parts.append(f"**Descrizione (grafo):** {vs['description']}.")
    if vs.get("type"): parts.append(f"**Tipo:** {vs['type']}.")
    if vs.get("constraint"): parts.append(f"**Vincolo:** `{vs['constraint']}`.")
    if vs.get("pattern_a_linked"): parts.append("**Pattern A linked:** sì.")
    if parts:
        body = replace_section(body, "Identità visuale (sintesi)", "\n".join(parts))

    # Storie
    appearances = find_in_canonical(entity_id, "visual_signature")
    if appearances:
        block = fmt_appearances_block(appearances)
        body = replace_section(body, "Storie / scene di apparizione", block)

    return body


# ------- main loop -------

DISPATCHERS = {
    "personaggio": compile_personaggio,
    "luogo": compile_luogo,
    "oggetto": compile_oggetto,
    "vento": compile_vento,
    "visual_signature": compile_visual_signature,
}

stats = {"processed": 0, "filled_sections": 0, "by_famiglia": {}, "no_data_in_graph": []}

for scheda_path in (REPO / "visual").rglob("scheda.md"):
    text = scheda_path.read_text()
    fm, body = parse_frontmatter(text)
    if fm is None: continue
    eid = fm.get("id")
    fam = fm.get("famiglia")
    if not eid or fam not in DISPATCHERS:
        continue

    before_stub_count = body.count(STUB)
    new_body = DISPATCHERS[fam](eid, body, fm)
    after_stub_count = new_body.count(STUB)
    filled = before_stub_count - after_stub_count

    if filled > 0:
        scheda_path.write_text(text[:text.index("\n---\n") + 5] + "\n" + new_body)
    elif eid not in GRAPH.get("entities", {}).get(fam + "s", {}) and fam not in ("vento", "visual_signature"):
        # Per personaggi/luoghi/oggetti, segnalo se non c'è entry grafo
        stats["no_data_in_graph"].append(f"{fam}/{eid}")

    stats["processed"] += 1
    stats["filled_sections"] += filled
    stats["by_famiglia"].setdefault(fam, {"processed": 0, "filled": 0})
    stats["by_famiglia"][fam]["processed"] += 1
    stats["by_famiglia"][fam]["filled"] += filled

print(f"=== Compilazione visual da grafo v1.0.0 ===")
print(f"Schede processate: {stats['processed']}")
print(f"Sezioni stub compilate: {stats['filled_sections']}")
print(f"Per famiglia: {stats['by_famiglia']}")
if stats["no_data_in_graph"]:
    print(f"\nSchede senza entry grafo (segnalate, NON modificate): {len(stats['no_data_in_graph'])}")
    for x in stats["no_data_in_graph"][:10]:
        print(f"  - {x}")
