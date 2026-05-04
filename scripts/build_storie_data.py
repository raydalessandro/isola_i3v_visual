#!/usr/bin/env python3
"""
build_storie_data.py — genera catalogo_web/data/storie.json

Per ognuna delle 12 storie:
1. Legge il frontmatter da `pipeline_narrativa/storie_finali/sNN_*.md`
2. Estrae i 10 hook (marker @hook ... @page ... @subhooks ... @image ...)
3. Audit filesystem per stato prompt grok + immagini canoniche di personaggi,
   luoghi, oggetti
4. Se esiste `_inventory/sNN_inventory.md`, arricchisce con dati manuali
5. Output: catalogo_web/data/storie.json — struttura per dashboard web

Idempotente. Da rilanciare quando:
- Cambia un testo definitivo
- Si aggiungono img canoniche a personaggi/luoghi/oggetti
- Si crea/aggiorna un inventory manuale
"""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STORIE_DIR = REPO_ROOT / "pipeline_narrativa" / "storie_finali"
INVENTORY_DIR = STORIE_DIR / "_inventory"
VISUAL_DIR = REPO_ROOT / "visual"
OUT_PATH = REPO_ROOT / "catalogo_web" / "data" / "storie.json"


def parse_yaml_frontmatter(content: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", content, re.S)
    if not m:
        return {}
    fm = m.group(1)
    out = {}
    for line in fm.split("\n"):
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def parse_hooks(content: str) -> list:
    """Trova tutti i marker @hook nei file storia."""
    hooks = []
    pattern = re.compile(
        r"^## Pagina (\d+)\s*\n+<!-- @hook (\S+) \| @page (\d+) \| @subhooks (\[.*?\]) \| @image (\S+) -->\s*\n+(.*?)(?=^## Pagina|\Z)",
        re.M | re.S,
    )
    for m in pattern.finditer(content):
        page_num = int(m.group(1))
        hook_id = m.group(2)
        subhooks_raw = m.group(4)
        image = m.group(5)
        text = m.group(6).strip().rstrip("---").strip()
        # Trim text per dashboard preview
        text_preview = text[:300] + ("..." if len(text) > 300 else "")
        hooks.append({
            "hook_id": hook_id,
            "page": page_num,
            "subhooks": subhooks_raw,
            "image": image,
            "text_preview": text_preview,
            "text_full": text,
        })
    return hooks


def audit_visual_entity(entity_type: str, entity_id: str) -> dict:
    """Cerca nel filesystem: prompt grok + immagini canoniche per un'entità."""
    # entity_type: "personaggi" | "luoghi" | "oggetti"
    if entity_type == "personaggi":
        # Cerca in tutte le sotto-cartelle di personaggi/individuali/* + collettivi
        for base in (
            VISUAL_DIR / "personaggi" / "individuali" / "bambini",
            VISUAL_DIR / "personaggi" / "individuali" / "primari",
            VISUAL_DIR / "personaggi" / "individuali" / "secondari",
            VISUAL_DIR / "personaggi" / "individuali" / "cuccioli",
            VISUAL_DIR / "personaggi" / "collettivi",
        ):
            p = base / entity_id
            if p.is_dir():
                return _audit_dir(p, entity_id)
        return {"found": False}
    elif entity_type == "oggetti":
        p = VISUAL_DIR / "oggetti" / entity_id
        if p.is_dir():
            return _audit_dir(p, entity_id)
        return {"found": False}
    elif entity_type == "luoghi":
        # Cerca ricorsivamente sotto luoghi/
        for p in (VISUAL_DIR / "luoghi").rglob(entity_id):
            if p.is_dir():
                return _audit_dir(p, entity_id)
        return {"found": False}
    return {"found": False}


def _audit_dir(p: Path, entity_id: str) -> dict:
    has_scheda = (p / "scheda.md").exists()
    has_prompt = (p / "prompt_grok.md").exists()
    img_dir = p / "immagini"
    img_count = 0
    img_paths = []
    if img_dir.is_dir():
        imgs = sorted([f for f in img_dir.glob("*.jpg") if f.name != ".gitkeep"])
        img_count = len(imgs)
        img_paths = [str(f.relative_to(REPO_ROOT)) for f in imgs[:6]]
    rel = str(p.relative_to(REPO_ROOT))
    return {
        "found": True,
        "id": entity_id,
        "path": rel,
        "scheda": has_scheda,
        "prompt_grok": has_prompt,
        "n_images": img_count,
        "image_paths": img_paths,
    }


def parse_inventory_md(sid: str) -> dict:
    """Se esiste un _inventory/sNN_inventory.md, estrae le sezioni rilevanti."""
    p = INVENTORY_DIR / f"{sid}_inventory.md"
    if not p.exists():
        return {"exists": False}
    content = p.read_text(encoding="utf-8")
    rel_path = str(p.relative_to(REPO_ROOT))
    out = {
        "exists": True,
        "path": rel_path,
        "github_url": f"https://github.com/raydalessandro/isola_i3v_visual/blob/main/{rel_path}",
    }

    # Estrai sezione "Aggiunte dalla prosa al canone"
    m = re.search(r"## Aggiunte dalla prosa al canone[^#]*?\n(.*?)(?=^## )", content, re.M | re.S)
    if m:
        out["additions_summary"] = m.group(1).strip()[:1500]

    # Estrai sezione "Gap operativi"
    m = re.search(r"## Gap operativi[^#]*?\n(.*?)(?=^## )", content, re.M | re.S)
    if m:
        out["gaps_summary"] = m.group(1).strip()[:1500]

    # Estrai sezione "Cosa serve per concludere"
    m = re.search(r"## Cosa serve per concludere[^#]*?\n(.*?)(?=^## )", content, re.M | re.S)
    if m:
        out["todo_summary"] = m.group(1).strip()[:1500]

    return out


def extract_entities_from_text(text: str, all_entities: dict) -> dict:
    """Cerca menzioni di entità note (personaggi/luoghi/oggetti) nel testo
    della pagina. Heuristic: matching case-insensitive del name canonico."""
    found = {"personaggi": [], "luoghi": [], "oggetti": []}
    text_lc = text.lower()
    for kind, entities in all_entities.items():
        for ent in entities:
            name_lc = ent["name"].lower()
            # Skip nomi troppo brevi/comuni
            if len(name_lc) < 3:
                continue
            # Match come parola intera (con boundary semplificato)
            if name_lc in text_lc:
                found[kind].append(ent["id"])
    # Dedup
    for k in found:
        found[k] = sorted(set(found[k]))
    return found


def load_all_entities() -> dict:
    """Carica gli ID e nomi canonici da entities.json."""
    ent_json = REPO_ROOT / "catalogo_web" / "data" / "entities.json"
    if not ent_json.exists():
        return {"personaggi": [], "luoghi": [], "oggetti": []}
    data = json.loads(ent_json.read_text(encoding="utf-8"))
    out = {"personaggi": [], "luoghi": [], "oggetti": []}
    for e in data.get("entities", []):
        fam = e.get("famiglia")
        if fam == "personaggio":
            out["personaggi"].append({"id": e["id"], "name": e["name"]})
        elif fam == "luogo":
            out["luoghi"].append({"id": e["id"], "name": e["name"]})
        elif fam == "oggetto":
            out["oggetti"].append({"id": e["id"], "name": e["name"]})
    return out


def process_storia(path: Path, all_entities: dict) -> dict:
    content = path.read_text(encoding="utf-8")
    fm = parse_yaml_frontmatter(content)
    hooks_raw = parse_hooks(content)

    # Per ogni hook: estrai entità menzionate + audit
    audited_chars = {}
    audited_locs = {}
    audited_objs = {}
    enriched_hooks = []
    for h in hooks_raw:
        ents = extract_entities_from_text(h["text_full"], all_entities)
        # Audit (cache per non ripetere)
        for cid in ents["personaggi"]:
            if cid not in audited_chars:
                audited_chars[cid] = audit_visual_entity("personaggi", cid)
        for lid in ents["luoghi"]:
            if lid not in audited_locs:
                audited_locs[lid] = audit_visual_entity("luoghi", lid)
        for oid in ents["oggetti"]:
            if oid not in audited_objs:
                audited_objs[oid] = audit_visual_entity("oggetti", oid)
        enriched_hooks.append({
            "hook_id": h["hook_id"],
            "page": h["page"],
            "subhooks": h["subhooks"],
            "image": h["image"],
            "text_preview": h["text_preview"],
            "entities": {
                "personaggi": ents["personaggi"],
                "luoghi": ents["luoghi"],
                "oggetti": ents["oggetti"],
            },
        })

    # Stats aggregati
    chars_with_imgs = sum(1 for v in audited_chars.values() if v.get("n_images", 0) > 0)
    locs_with_imgs = sum(1 for v in audited_locs.values() if v.get("n_images", 0) > 0)
    locs_with_prompt = sum(1 for v in audited_locs.values() if v.get("prompt_grok"))
    objs_with_prompt = sum(1 for v in audited_objs.values() if v.get("prompt_grok"))
    hooks_image_ready = sum(1 for h in enriched_hooks if h["image"] != "TBD")

    sid = fm.get("sid", "")
    inventory = parse_inventory_md(sid) if sid else {"exists": False}

    return {
        "sid": sid,
        "title": fm.get("title", path.stem),
        "slug": fm.get("slug", ""),
        "cycle": fm.get("cycle", ""),
        "total_pages": int(fm.get("total_pages", 10)),
        "total_hooks": int(fm.get("total_hooks", 10)),
        "status": fm.get("status", "definitiva"),
        "ultima_modifica": fm.get("ultima_modifica", ""),
        "file_path": str(path.relative_to(REPO_ROOT)),
        "github_url": f"https://github.com/raydalessandro/isola_i3v_visual/blob/main/{path.relative_to(REPO_ROOT)}",
        "stats": {
            "chars_distinct": len(audited_chars),
            "chars_with_imgs": chars_with_imgs,
            "locs_distinct": len(audited_locs),
            "locs_with_imgs": locs_with_imgs,
            "locs_with_prompt": locs_with_prompt,
            "objs_distinct": len(audited_objs),
            "objs_with_prompt": objs_with_prompt,
            "hooks_image_ready": hooks_image_ready,
            "hooks_total": len(enriched_hooks),
        },
        "hooks": enriched_hooks,
        "audited_entities": {
            "personaggi": audited_chars,
            "luoghi": audited_locs,
            "oggetti": audited_objs,
        },
        "inventory": inventory,
    }


def main():
    if not STORIE_DIR.exists():
        raise SystemExit(f"ERROR: {STORIE_DIR} not found")
    all_entities = load_all_entities()
    print(f"[load] entities.json: {len(all_entities['personaggi'])} personaggi, "
          f"{len(all_entities['luoghi'])} luoghi, {len(all_entities['oggetti'])} oggetti")

    storie_files = sorted(STORIE_DIR.glob("s*_*.md"))
    storie = []
    for f in storie_files:
        if f.name.startswith("_"):
            continue
        print(f"  [+] {f.name}")
        storie.append(process_storia(f, all_entities))

    out = {
        "generated_from": "scripts/build_storie_data.py",
        "n_storie": len(storie),
        "storie": storie,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[done] {OUT_PATH.relative_to(REPO_ROOT)} ({OUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
