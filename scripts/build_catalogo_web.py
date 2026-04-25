#!/usr/bin/env python3
"""
build_catalogo_web.py

Scansiona `visual/` ricorsivamente e genera `catalogo_web/data/entities.json`,
file unico letto dal frontend HTML+JS in `catalogo_web/`.

Per ogni cartella entita' con `scheda.md`:
- estrae frontmatter YAML (PyYAML);
- preserva il body markdown;
- raccoglie i path delle immagini in `<entita>/immagini/` (escludendo `.gitkeep`).

Costruisce inoltre un albero gerarchico che riflette la struttura di `visual/`
(famiglia -> sottotipo -> entita', con nesting frattale per i luoghi).

Idempotente. Da rilanciare quando le schede o le immagini cambiano.

Scrive in: `catalogo_web/data/`.
"""

import json
from datetime import datetime, date
from pathlib import Path

import yaml  # PyYAML

ROOT = Path(__file__).resolve().parent.parent
VISUAL = ROOT / "visual"
OUT_DIR = ROOT / "catalogo_web" / "data"
OUT_FILE = OUT_DIR / "entities.json"
STRADE_INDEX = VISUAL / "luoghi" / "_strade_index.md"
CATALOGO = VISUAL / "catalogo.md"
IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def parse_scheda(scheda_path: Path):
    """Ritorna (frontmatter_dict, body_str)."""
    text = scheda_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    body = text[end + len("\n---\n"):]
    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as e:
        print(f"[warn] YAML parse error in {scheda_path}: {e}")
        fm = {}
    return fm, body.strip()


def collect_images(folder: Path):
    img_dir = folder / "immagini"
    if not img_dir.is_dir():
        return []
    out = []
    for p in sorted(img_dir.iterdir()):
        if p.is_file() and p.suffix.lower() in IMG_EXTS:
            out.append({
                "filename": p.name,
                "path": str(p.relative_to(ROOT)),
                "size_kb": p.stat().st_size // 1024,
            })
    return out


def scan_visual():
    entities = []
    for scheda in sorted(VISUAL.rglob("scheda.md")):
        folder = scheda.parent
        rel_folder = str(folder.relative_to(ROOT))
        rel_scheda = str(scheda.relative_to(ROOT))
        fm, body = parse_scheda(scheda)
        images = collect_images(folder)
        breadcrumb = list(folder.relative_to(VISUAL).parts)
        entities.append({
            "id": fm.get("id"),
            "name": fm.get("name") or fm.get("id"),
            "famiglia": fm.get("famiglia"),
            "sottotipo": fm.get("sottotipo"),
            "status": fm.get("status"),
            "quartiere": fm.get("quartiere"),
            "categoria_strada": fm.get("categoria_strada"),
            "frontmatter": fm,
            "body_md": body,
            "body_size_chars": len(body),
            "folder_path": rel_folder,
            "scheda_path": rel_scheda,
            "breadcrumb": breadcrumb,
            "images": images,
            "n_images": len(images),
        })
    return entities


def build_tree(entities):
    """Costruisci un albero gerarchico riflettendo la struttura visual/.

    Ogni nodo ha:
      - "_label": label leggibile (di default = chiave segmento)
      - "_children": dict di sotto-nodi
      - se foglia (entita'): "_entity_id" punta all'id e "_entity_meta" basic info
    """
    root = {"_children": {}}
    for e in entities:
        node = root
        path = e["breadcrumb"]
        for i, segment in enumerate(path):
            children = node["_children"]
            if segment not in children:
                children[segment] = {"_children": {}}
            node = children[segment]
            if i == len(path) - 1:
                # foglia: marca come entita'
                node["_entity_id"] = e["id"]
                node["_entity_meta"] = {
                    "name": e["name"],
                    "famiglia": e["famiglia"],
                    "sottotipo": e["sottotipo"],
                    "status": e["status"],
                    "n_images": e["n_images"],
                    "folder_path": e["folder_path"],
                }
    return root["_children"]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    entities = scan_visual()
    totals = {"totale": len(entities)}
    by_famiglia = {}
    by_status = {}
    for e in entities:
        f = e.get("famiglia") or "?"
        totals[f] = totals.get(f, 0) + 1
        by_famiglia.setdefault(f, []).append(e["id"])
        s = e.get("status") or "?"
        by_status[s] = by_status.get(s, 0) + 1

    # Read auxiliary indexes (raw markdown) for special pages
    aux = {}
    if STRADE_INDEX.is_file():
        aux["strade_index_md"] = STRADE_INDEX.read_text(encoding="utf-8")
    if CATALOGO.is_file():
        aux["catalogo_md"] = CATALOGO.read_text(encoding="utf-8")

    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "totals": totals,
        "by_status": by_status,
        "tree": build_tree(entities),
        "entities": entities,
        "aux": aux,
    }

    def _default(o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        raise TypeError(f"Object of type {o.__class__.__name__} not serializable")

    OUT_FILE.write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=_default),
        encoding="utf-8",
    )
    size_kb = OUT_FILE.stat().st_size // 1024

    print(f"Catalogo web generato: {OUT_FILE} ({size_kb} KB)")
    print(f"  Entita' totali: {len(entities)}")
    for k, v in sorted(totals.items()):
        print(f"  {k}: {v}")
    print(f"  Status: {by_status}")
    n_imgs = sum(e["n_images"] for e in entities)
    print(f"  Immagini totali catalogate: {n_imgs}")


if __name__ == "__main__":
    main()
