#!/usr/bin/env python3
"""
build_visual_skeleton.py

Genera la struttura `visual/` a partire da:
- `pipeline_narrativa/story_graph.json`  (read-only)
- `cartografia/geo/island.geojson`        (read-only)

Crea per ogni entita' della saga una cartella dedicata con:
- `scheda.md`     stub con frontmatter YAML compilato dal grafo + GeoJSON
- `immagini/`     directory con `.gitkeep` per riferimenti IA / 4 vedute 3D

Idempotente:
- Non sovrascrive `scheda.md` se esiste gia' (preserva lavoro umano/agenti).
- Crea solo cartelle/file mancanti.
- Rigenera sempre `visual/catalogo.md`.

Scrive in: visual/ (esclusivamente).
"""

import json
import math
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "pipeline_narrativa" / "story_graph.json"
GEO_PATH = ROOT / "cartografia" / "geo" / "island.geojson"
VISUAL = ROOT / "visual"

# ------------------------------------------------------------------ helpers

def load_json(p):
    with open(p) as f:
        return json.load(f)


def to_local_meters(lon, lat, orig_lon=17.956, orig_lat=34.4685):
    """Converti WGS84 in metri locali rispetto all'origin di island.geojson."""
    m_per_deg_lat = 111000.0
    m_per_deg_lon = 111000.0 * math.cos(math.radians(orig_lat))
    return ((lon - orig_lon) * m_per_deg_lon, (lat - orig_lat) * m_per_deg_lat)


def all_coords(geom):
    out = []
    def walk(c):
        if isinstance(c, (list, tuple)):
            if c and isinstance(c[0], (int, float)):
                out.append((c[0], c[1]))
            else:
                for x in c:
                    walk(x)
    walk(geom["coordinates"])
    return out


def geo_metadata(feat):
    """Estrai metadati cartografici utili al visual."""
    g = feat["geometry"]
    coords = all_coords(g)
    locals_m = [to_local_meters(*c) for c in coords]
    xs = [c[0] for c in locals_m]
    ys = [c[1] for c in locals_m]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    bbox_m = [round(min(xs)), round(min(ys)), round(max(xs)), round(max(ys))]
    size_m = [bbox_m[2] - bbox_m[0], bbox_m[3] - bbox_m[1]]
    p = feat["properties"]
    return {
        "feature_id": p.get("id"),
        "type_geo": p.get("type"),
        "status_geo": p.get("status"),
        "quarter": p.get("quarter"),
        "category": p.get("category"),
        "centroid_m_local": [round(cx), round(cy)],
        "bbox_m_local": bbox_m,
        "size_m_local": size_m,
        "altitudine_m": p.get("elevation_m"),
        "geometry_type": g["type"],
        "parent_geo": p.get("parent"),
        "children_geo": p.get("children", []),
        "aliases_geo": p.get("aliases", []),
    }


def path_metadata(feat):
    """Metadati specializzati per LineString (strade): lunghezza, endpoints, n_punti."""
    base = geo_metadata(feat)
    g = feat["geometry"]
    if g["type"] != "LineString":
        return base
    coords_local = [to_local_meters(*c[:2]) for c in g["coordinates"]]
    # Lunghezza: somma distanze euclidee fra punti consecutivi
    length = 0.0
    for i in range(len(coords_local) - 1):
        x0, y0 = coords_local[i]
        x1, y1 = coords_local[i + 1]
        length += math.hypot(x1 - x0, y1 - y0)
    a = coords_local[0]
    b = coords_local[-1]
    base.update({
        "lunghezza_m_local": round(length),
        "n_punti": len(coords_local),
        "endpoint_a_m": [round(a[0]), round(a[1])],
        "endpoint_b_m": [round(b[0]), round(b[1])],
        "endpoints_inferiti_dal_id": _parse_endpoints_from_id(feat["properties"].get("id", "")),
    })
    return base


def _parse_endpoints_from_id(fid):
    """Estrai token semantici dall'id strada (rimosso prefix sentiero_/viottolo_).

    Approccio greedy: split su '_' e ritorno la lista. Indicativo, non autoritativo —
    serve solo come hint per consultazione veloce. Il body della scheda chiarisce.
    """
    s = fid
    for prefix in ("sentiero_", "viottolo_", "via_"):
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    return s.split("_")


# ------------------------------------------------------------------ structures

# Mappatura sottotipi personaggi (da entities.characters.*.type)
CHAR_TYPE_TO_SUBTYPE = {
    "protagonista": "bambini",
    "abitante_maggiore": "primari",
    "testimone_unico_pre_vento": "primari",
    "cucciolo_scuola": "cuccioli",
    "abitante_minore_mestiere": "secondari",
    "gruppo_istituzione": "collettivo",
}

# Mappatura quarter (GeoJSON) -> nome cartella visual/luoghi/<x>/
QUARTER_TO_FOLDER = {
    "centro": "villaggio_centrale",
    "terra": "quartiere_terra",
    "fuoco": "quartiere_fuoco",
    "acqua": "quartiere_acqua",
    "aria": "quartiere_aria",
    "perimetro": "perimetro",
}

# Albero geografico frattale (chiave = parent path relativo a visual/luoghi/)
# Sotto ogni quartiere, lista di (id_luogo, [figli...]) per nesting.
LUOGHI_TREE = {
    "villaggio_centrale": [
        ("piazza_villaggio", [
            ("albero_vecchio", [
                ("panca_di_pietra", []),
                ("cespuglio_dietro_albero_vecchio", []),
            ]),
            ("pozzo_piazza", []),
        ]),
        ("scuola_stria", []),
        ("via_scuola", []),
        ("casa_memolo_cortile", []),
    ],
    "quartiere_terra": [
        ("orti_del_cerchio", []),
        ("via_degli_orti", []),
        ("casa_salvia", []),
        ("casa_zolla", []),
        ("foresta_intrecciata", [
            ("radura_dei_pini", []),
            ("tana_rovo", []),
            ("torrente_affluente_foresta", []),
            ("zona_di_lavoro_salvia", []),
        ]),
    ],
    "quartiere_fuoco": [
        ("forno", []),
        ("case_del_mattino", []),
        ("via_dell_alba", []),
    ],
    "quartiere_acqua": [
        ("pontile_bocca", []),
        ("bocca", []),
        ("spiaggia_conchiglie", []),
        ("casa_amo", []),
        ("case_basse_pescatori", []),
        ("via_del_pontile", []),
    ],
    "quartiere_aria": [
        ("pascoli_alti", []),
        ("roccia_alta", []),
        ("montagne_gemelle", []),
        ("burrone", [
            ("grotta_grunto", []),
        ]),
        ("via_che_sale", []),
    ],
    "perimetro": [
        ("fiume_che_gira", [
            ("fiume_capo", []),
            ("fiume_braccio_ovest_alto", []),
            ("fiume_stretta_due_massi", []),
            ("fiume_braccio_ovest_medio", []),
            ("fiume_braccio_ovest_basso", []),
            ("fiume_braccio_est", []),
            ("guado_di_pietre_piatte", []),
        ]),
        ("fascia_costiera", []),
    ],
}

# Locations da escludere come scheda autonoma (alias o meta)
LUOGHI_SKIP = {
    "tutta_isola_quattro_quartieri_attraversati",  # meta
    "villaggio_centrale",  # alias di piazza_villaggio
    "mercato_del_mezzogiorno_panca_di_pietra",  # alias di panca_di_pietra
}

# ------------------------------------------------------------------ scheda render

def yaml_dump_value(v, indent=0):
    pad = "  " * indent
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        if any(c in v for c in [":", "#", "[", "]", "{", "}", "&", "*", "!", "|", ">", "%", "@", "`"]) or v == "":
            return json.dumps(v, ensure_ascii=False)
        return v
    if isinstance(v, list):
        if not v:
            return "[]"
        if all(isinstance(x, (str, int, float, bool)) or x is None for x in v):
            inner = ", ".join(yaml_dump_value(x) for x in v)
            return f"[{inner}]"
        out = "\n"
        for x in v:
            out += f"{pad}- {yaml_dump_value(x, indent+1)}\n"
        return out.rstrip()
    if isinstance(v, dict):
        if not v:
            return "{}"
        out = "\n"
        for k, val in v.items():
            rendered = yaml_dump_value(val, indent+1)
            if isinstance(val, (dict, list)) and val and not (isinstance(val, list) and all(isinstance(x, (str, int, float, bool)) or x is None for x in val)):
                out += f"{pad}{k}:{rendered}\n"
            else:
                out += f"{pad}{k}: {rendered}\n"
        return out.rstrip()
    return json.dumps(v, ensure_ascii=False)


def render_scheda(meta):
    """Genera testo Markdown della scheda stub."""
    fm_lines = ["---"]
    for k, v in meta.items():
        rendered = yaml_dump_value(v, indent=1)
        if isinstance(v, (dict, list)) and v and not (isinstance(v, list) and all(isinstance(x, (str, int, float, bool)) or x is None for x in v)):
            fm_lines.append(f"{k}:{rendered}")
        else:
            fm_lines.append(f"{k}: {rendered}")
    fm_lines.append("---")
    fm = "\n".join(fm_lines)

    body = f"""
# {meta.get('name', meta['id'])}

## Identita' visuale (sintesi)

[stub — da compilare]

## Aspetto / forma

[stub]

## Abbigliamento / stato d'uso

[stub — applicare se personaggio o oggetto]

## Espressione / comportamento

[stub — applicare se personaggio o vento]

## Palette e atmosfera

[stub]

## Contesto e ambientazioni ricorrenti

[stub]

## Coerenza cross-scena (cose che NON cambiano)

[stub]

## Variabilita' ammessa

[stub]

## Cliche' da evitare

Riferimento: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

[stub]

## Per stampa 3D

Volumi, proporzioni, scala, orientamento canonico.

[stub]

## Per narrativa e social

Registri d'uso testuale, tono, parole-chiave da usare/evitare.

[stub]

## Storie / scene di apparizione

[stub — popolare con elenco s01..s12 e ruolo per scena]

## Disallineamenti / domande aperte

[vuoto se nulla]

## Riferimenti puntuali (citazioni dirette dalle fonti)

[stub — ogni dato visivo riportato sopra deve essere ancorato a una fonte citata qui]
"""
    return fm + "\n" + body


def write_scheda(folder: Path, meta: dict):
    """Crea folder + scheda.md (creato o frontmatter aggiornato) + immagini/.gitkeep.

    Comportamento idempotente:
    - Se scheda.md NON esiste: la crea per intero (frontmatter + body stub).
    - Se scheda.md esiste: rigenera SOLO il frontmatter (derivato da grafo+GeoJSON),
      preserva il body (lavoro umano/agenti).
    """
    folder.mkdir(parents=True, exist_ok=True)
    scheda = folder / "scheda.md"
    if not scheda.exists():
        scheda.write_text(render_scheda(meta), encoding="utf-8")
    else:
        # Update-mode: sostituisci frontmatter, preserva body
        existing = scheda.read_text(encoding="utf-8")
        # Trova il body dopo il secondo ---
        if existing.startswith("---\n"):
            end_idx = existing.find("\n---\n", 4)
            if end_idx != -1:
                body = existing[end_idx + len("\n---\n"):]
            else:
                # Frontmatter non chiuso, tratta tutto come body
                body = existing
        else:
            # Nessun frontmatter, tutto e' body
            body = existing
        # Costruisci nuovo frontmatter
        new = render_scheda(meta)
        new_end = new.find("\n---\n", 4)
        new_frontmatter = new[:new_end + len("\n---\n")]
        scheda.write_text(new_frontmatter + body, encoding="utf-8")

    immagini = folder / "immagini"
    immagini.mkdir(exist_ok=True)
    gitkeep = immagini / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("")


# ------------------------------------------------------------------ main

def main():
    graph = load_json(GRAPH_PATH)
    geo = load_json(GEO_PATH)

    geo_by_id = {f["properties"]["id"]: f for f in geo["features"]}

    today = str(date.today())
    created_count = 0
    fm_updated_count = 0
    catalog_rows = []

    def write(folder, meta):
        nonlocal created_count, fm_updated_count
        existed = (folder / "scheda.md").exists()
        write_scheda(folder, meta)
        if existed:
            fm_updated_count += 1
        else:
            created_count += 1
        rel = folder.relative_to(ROOT)
        catalog_rows.append({
            "id": meta["id"],
            "name": meta.get("name", meta["id"]),
            "famiglia": meta.get("famiglia"),
            "sottotipo": meta.get("sottotipo"),
            "status": meta.get("status"),
            "path": str(rel) + "/scheda.md",
        })

    # 1) PERSONAGGI
    chars = graph["entities"]["characters"]
    for cid, c in chars.items():
        ctype = c.get("type", "")
        sub = CHAR_TYPE_TO_SUBTYPE.get(ctype)
        if not sub:
            print(f"[warn] character {cid} has unknown type '{ctype}', defaulting to 'secondari'")
            sub = "secondari"
        if sub == "collettivo":
            base = VISUAL / "personaggi" / "collettivi"
        else:
            base = VISUAL / "personaggi" / "individuali" / sub
        folder = base / cid
        rel_to = c.get("related_to", [])
        meta = {
            "id": cid,
            "name": c.get("name", cid.replace("_", " ").title()),
            "famiglia": "personaggio",
            "sottotipo": sub,
            "specie": c.get("species"),
            "tipo_grafo": ctype,
            "ruolo_saga": c.get("role_saga") or c.get("narrative_function"),
            "status": "stub",
            "ultima_modifica": today,
            "fonti": [
                f"pipeline_narrativa/story_graph.json#entities.characters.{cid}",
            ],
            "appare_in_storie": [],
            "relazioni": {
                "dimora": c.get("home_location"),
                "quadrante_grafo": c.get("quadrant"),
                "related_to": rel_to,
                "cross_skill": {
                    "cartografia": None,
                },
            },
        }
        write(folder, meta)

    # 2) LUOGHI (frattale)
    seen_luoghi = set()

    def emit_luogo(folder, lid):
        seen_luoghi.add(lid)
        feat = geo_by_id.get(lid)
        gmeta = geo_metadata(feat) if feat else None
        graph_loc = graph["entities"]["locations"].get(lid)
        name = (graph_loc or {}).get("name") if isinstance(graph_loc, dict) else None
        if not name and feat:
            name = feat["properties"].get("name")
        if not name:
            name = lid.replace("_", " ").title()
        meta = {
            "id": lid,
            "name": name,
            "famiglia": "luogo",
            "sottotipo": (feat["properties"].get("type") if feat else None),
            "quartiere": (feat["properties"].get("quarter") if feat else None),
            "status": "stub",
            "ultima_modifica": today,
            "fonti": [
                f"pipeline_narrativa/story_graph.json#entities.locations.{lid}" if graph_loc else None,
                f"cartografia/geo/island.geojson#features.id={lid}" if feat else None,
            ],
            "appare_in_storie": [],
            "cartografia": gmeta,
        }
        # rimuovi None da fonti
        meta["fonti"] = [x for x in meta["fonti"] if x]
        write(folder, meta)

    def walk_tree(parent_path, tree):
        for lid, children in tree:
            folder = parent_path / lid
            emit_luogo(folder, lid)
            if children:
                walk_tree(folder, children)

    luoghi_root = VISUAL / "luoghi"
    for quartiere, tree in LUOGHI_TREE.items():
        walk_tree(luoghi_root / quartiere, tree)

    # Verifica: ogni location del grafo (escluse SKIP) sta in seen_luoghi?
    graph_locs = set(graph["entities"]["locations"].keys()) - LUOGHI_SKIP
    missing = graph_locs - seen_luoghi
    extra = seen_luoghi - graph_locs - {
        # location nel GeoJSON ma non nel grafo (cartografia ricca):
        "fiume_capo", "fiume_braccio_ovest_alto", "fiume_stretta_due_massi",
        "fiume_braccio_ovest_medio", "fiume_braccio_ovest_basso", "fiume_braccio_est",
        "radura_dei_pini",
        "panca_di_pietra",  # vero ID GeoJSON; il grafo lo cita via alias mercato_del_mezzogiorno_panca_di_pietra
        "zona_di_lavoro_salvia",  # cartografia v0.4 inferita da S4
    }
    if missing:
        print(f"[warn] location del grafo NON ancora nell'albero LUOGHI_TREE: {missing}")
    if extra:
        print(f"[warn] cartelle LUOGHI_TREE che non corrispondono a entities.locations e non sono carto-only: {extra}")

    # 3) OGGETTI (flat)
    objs = graph["entities"]["objects"]
    for oid, o in objs.items():
        folder = VISUAL / "oggetti" / oid
        meta = {
            "id": oid,
            "name": o.get("name", oid.replace("_", " ").title()),
            "famiglia": "oggetto",
            "sottotipo": o.get("type"),
            "status": "stub",
            "ultima_modifica": today,
            "fonti": [
                f"pipeline_narrativa/story_graph.json#entities.objects.{oid}",
            ],
            "appare_in_storie": [],
            "relazioni": {
                "associato_a_personaggio": o.get("associated_character") or o.get("owner"),
                "associato_a_luogo": o.get("associated_location"),
            },
        }
        write(folder, meta)

    # 4) VENTI (escluso _shared)
    winds = graph["entities"]["winds"]
    for wid, w in winds.items():
        if wid.startswith("_"):
            continue
        folder = VISUAL / "venti" / wid
        meta = {
            "id": wid,
            "name": w.get("name", wid.replace("_", " ").title()),
            "famiglia": "vento",
            "sottotipo": w.get("type"),
            "status": "stub",
            "ultima_modifica": today,
            "fonti": [
                f"pipeline_narrativa/story_graph.json#entities.winds.{wid}",
            ],
            "appare_in_storie": [],
        }
        write(folder, meta)

    # 5) VISUAL_SIGNATURES (escluso _note)
    vsigs = graph["entities"].get("visual_signatures", {})
    for sid, s in vsigs.items():
        if sid.startswith("_"):
            continue
        folder = VISUAL / "visual_signatures" / sid
        meta = {
            "id": sid,
            "name": (s.get("name") if isinstance(s, dict) else None) or sid.replace("_", " ").title(),
            "famiglia": "visual_signature",
            "status": "stub",
            "ultima_modifica": today,
            "fonti": [
                f"pipeline_narrativa/story_graph.json#entities.visual_signatures.{sid}",
            ],
            "appare_in_storie": [],
        }
        write(folder, meta)

    # 6) STRADE (sentieri/viottoli del GeoJSON, NON in entities.locations)
    strade_per_quartiere = {}  # per indice
    for f in geo["features"]:
        p = f["properties"]
        fid = p.get("id", "")
        if not any(fid.startswith(prefix) for prefix in ("sentiero_", "viottolo_")):
            continue
        if fid in graph["entities"]["locations"]:
            continue  # gia' gestito come location del grafo (vie principali)
        quarter = p.get("quarter")
        sub = QUARTER_TO_FOLDER.get(quarter)
        if not sub:
            print(f"[warn] strada {fid} ha quarter '{quarter}' non mappato — skip")
            continue
        folder = VISUAL / "luoghi" / sub / "strade" / fid
        gmeta = path_metadata(f)
        meta = {
            "id": fid,
            "name": p.get("name", fid.replace("_", " ").title()),
            "famiglia": "luogo",
            "sottotipo": "strada",
            "categoria_strada": p.get("category"),
            "quartiere": quarter,
            "status": "stub",
            "ultima_modifica": today,
            "fonti": [
                f"cartografia/geo/island.geojson#features.id={fid}",
            ],
            "appare_in_storie": [],
            "cartografia": gmeta,
        }
        write(folder, meta)
        strade_per_quartiere.setdefault(sub, []).append({
            "id": fid,
            "name": p.get("name", fid),
            "category": p.get("category"),
            "status": p.get("status"),
            "lunghezza_m": gmeta.get("lunghezza_m_local"),
            "endpoint_a_m": gmeta.get("endpoint_a_m"),
            "endpoint_b_m": gmeta.get("endpoint_b_m"),
            "path": str((folder / "scheda.md").relative_to(ROOT)),
        })

    # 6b) Indice strade
    idx_lines = [
        "# Indice strade",
        "",
        "Generato automaticamente da `scripts/build_visual_skeleton.py`. Non modificare a mano.",
        "",
        "Le **5 Vie principali** (canoniche, in `entities.locations`) sono catalogate paritetiche con gli altri luoghi del rispettivo quartiere — non in questo indice. Qui solo le **strade secondarie** (solo cartografiche).",
        "",
    ]
    quartiere_label = {
        "villaggio_centrale": "centro",
        "quartiere_terra": "terra",
        "quartiere_fuoco": "fuoco",
        "quartiere_acqua": "acqua",
        "quartiere_aria": "aria",
        "perimetro": "perimetro / inter-quartiere",
    }
    quartiere_order = ["villaggio_centrale", "quartiere_terra", "quartiere_fuoco",
                       "quartiere_acqua", "quartiere_aria", "perimetro"]
    total_strade = sum(len(v) for v in strade_per_quartiere.values())
    idx_lines.append(f"Totale strade: **{total_strade}**.\n")
    for q in quartiere_order:
        if q not in strade_per_quartiere:
            continue
        rows = sorted(strade_per_quartiere[q], key=lambda r: (r["status"] or "", r["id"]))
        label = quartiere_label.get(q, q)
        idx_lines.append(f"## Quartiere {label} ({len(rows)})")
        idx_lines.append("")
        idx_lines.append("| id | nome | category | status | len m | endpoint A → B | scheda |")
        idx_lines.append("|---|---|---|---|---|---|---|")
        for r in rows:
            ea = r["endpoint_a_m"] or [None, None]
            eb = r["endpoint_b_m"] or [None, None]
            ep = f"({ea[0]},{ea[1]}) → ({eb[0]},{eb[1]})"
            rel_link = r["path"].replace("visual/", "", 1)
            idx_lines.append(
                f"| `{r['id']}` | {r['name']} | {r['category'] or ''} | {r['status']} | {r['lunghezza_m']} | {ep} | [`{r['path']}`](./{rel_link}) |"
            )
        idx_lines.append("")
    (VISUAL / "luoghi" / "_strade_index.md").write_text("\n".join(idx_lines), encoding="utf-8")

    # 7) CATALOGO MD
    catalog_rows.sort(key=lambda r: (r["famiglia"] or "", r["sottotipo"] or "", r["id"]))
    lines = [
        "# Catalogo entita' visual",
        "",
        "Generato automaticamente da `scripts/build_visual_skeleton.py`. Non modificare a mano: rilanciare lo script.",
        "",
        f"Totale schede: **{len(catalog_rows)}**.",
        "",
        "| id | nome | famiglia | sottotipo | status | path |",
        "|---|---|---|---|---|---|",
    ]
    for r in catalog_rows:
        lines.append(
            f"| `{r['id']}` | {r['name']} | {r['famiglia'] or ''} | {r['sottotipo'] or ''} | {r['status']} | [`{r['path']}`](./{r['path'].replace('visual/', '', 1)}) |"
        )
    (VISUAL / "catalogo.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 7) Summary
    print()
    print(f"Bootstrap visual completato.")
    print(f"  Schede create ex novo:           {created_count}")
    print(f"  Frontmatter aggiornato (body preservato): {fm_updated_count}")
    print(f"  Totale nel catalogo:              {len(catalog_rows)}")
    if missing:
        print(f"  Location non emesse: {missing}")


if __name__ == "__main__":
    main()
