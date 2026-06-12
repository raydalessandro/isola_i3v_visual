#!/usr/bin/env python3
"""
ingest_tavola.py — Ingest meccanico di una tavola-atlante nello spec.

La dichiarazione di Manus (manifest JSON) non diventa MAI verità diretta:
questo script la VERIFICA e, solo se tutti i controlli passano, scrive
variante + tavola nella voce corrispondente di ATLANTE_SPEC.json.
Lo script libro (build_volume.py) legge solo lo spec — fonte unica.

Controlli:
  1. Manifest      — schema, campi, slug esistente nello spec, variante valida
  2. Immagine      — esiste, JPEG/RGB, ≥ 1748×2480, verticale
  3. Quiete zone   — luminosità media e densità di bordi nelle zone testo
                     (stessa statistica del trattamento DODGE delle pagine
                     storia): la zona dichiarata quieta deve esserlo davvero
  4. Ritmo         — la variante non crea due uguali consecutive nel volume
                     (warning, non blocco: lo blinda il test suite)

Uso:
  python3 scripts/ingest_tavola.py visual/atlante/tavole/<slug>_tavola_v1.json
  python3 scripts/ingest_tavola.py <manifest> --dry-run   # solo report
  python3 scripts/ingest_tavola.py <manifest> --force     # ignora quiete zone

Exit code: 0 ok, 1 controlli falliti, 2 errore d'uso.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat

REPO = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO / "visual/atlante/ATLANTE_SPEC.json"

MANIFEST_SCHEMA = "tavola_atlante/1.0"
CAMPI_MANIFEST = {"schema", "slug", "variante", "file", "generatore", "data", "note"}

# Soglie di quiete (frazioni 0–1). Tarate sulle stesse statistiche del
# trattamento DODGE in build_volume.py (bright>0.60 & move<0.11 = calmo).
# Qui leggermente più permissive: la schiarita DODGE in render fa da rete.
SOGLIA_LUMINOSITA = 0.50   # media grigio minima della zona
SOGLIA_BORDI      = 0.13   # media FIND_EDGES massima della zona


def _zona_box(z: dict, w: int, h: int, default_w=0.55, default_h=0.10):
    x0 = z["x"] * w
    y0 = z["y"] * h
    x1 = x0 + (z["w"] or default_w) * w
    y1 = y0 + (z["h"] or default_h) * h
    return (int(x0), int(y0), int(min(x1, w)), int(min(y1, h)))


def misura_quiete(img: Image.Image, box) -> tuple[float, float]:
    """Ritorna (luminosità media 0–1, densità bordi 0–1) della zona."""
    crop = img.convert("L").crop(box)
    lum = ImageStat.Stat(crop).mean[0] / 255.0
    edges = ImageStat.Stat(crop.filter(ImageFilter.FIND_EDGES)).mean[0] / 255.0
    return lum, edges


def verifica_tavola(manifest_path: Path, force: bool = False
                    ) -> tuple[bool, dict, list[str]]:
    """Esegue tutti i controlli. Ritorna (ok, manifest, report_righe)."""
    rep: list[str] = []
    ok = True

    # 1 ── Manifest ─────────────────────────────────────────────────────────
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, {}, [f"✗ Manifest illeggibile: {exc}"]

    if set(manifest.keys()) != CAMPI_MANIFEST:
        ok = False
        rep.append(f"✗ Campi manifest non uniformi: {sorted(manifest.keys())} "
                   f"(attesi: {sorted(CAMPI_MANIFEST)})")
    if manifest.get("schema") != MANIFEST_SCHEMA:
        ok = False
        rep.append(f"✗ Schema manifest: {manifest.get('schema')!r} "
                   f"(atteso {MANIFEST_SCHEMA!r})")
    if not ok:
        return False, manifest, rep

    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    per_slug = {v["slug"]: v for v in spec["voci"]}
    slug, variante = manifest["slug"], manifest["variante"]

    if slug not in per_slug:
        return False, manifest, [f"✗ Slug sconosciuto nello spec: {slug!r}"]
    voce = per_slug[slug]
    if voce["tipo"] != "tavola":
        return False, manifest, [f"✗ La voce '{voce['titolo']}' è di tipo "
                                 f"'{voce['tipo']}', non accetta tavole"]
    if variante not in spec["varianti"]:
        return False, manifest, [f"✗ Variante sconosciuta: {variante!r}"]
    rep.append(f"✓ Manifest valido — {voce['titolo']} · variante {variante}")

    # 2 ── Immagine ─────────────────────────────────────────────────────────
    img_path = REPO / manifest["file"]
    if not img_path.exists():
        return False, manifest, rep + [f"✗ Immagine non trovata: {manifest['file']}"]
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    q = spec["qualita_tavole"]
    if w < q["min_w"] or h < q["min_h"] or h < w:
        ok = False
        rep.append(f"✗ Immagine {w}×{h}px — sotto spec "
                   f"(min {q['min_w']}×{q['min_h']} verticale)")
    else:
        rep.append(f"✓ Immagine {w}×{h}px")

    # 3 ── Quiete delle zone testo ──────────────────────────────────────────
    Z = spec["varianti"][variante]["zone"]
    head = _zona_box({"x": Z["eyebrow"]["x"] - 0.02, "y": Z["eyebrow"]["y"] - 0.01,
                      "w": 0.58, "h": 0.115}, w, h)
    corpo = _zona_box(Z["corpo"], w, h)
    quiete_ok = True
    for nome_z, box in (("testa", head), ("corpo", corpo)):
        lum, edges = misura_quiete(img, box)
        calma = lum >= SOGLIA_LUMINOSITA and edges <= SOGLIA_BORDI
        simbolo = "✓" if calma else ("!" if force else "✗")
        rep.append(f"{simbolo} Zona {nome_z}: luminosità {lum:.2f} "
                   f"(min {SOGLIA_LUMINOSITA}), bordi {edges:.2f} "
                   f"(max {SOGLIA_BORDI})")
        if not calma:
            quiete_ok = False
    if not quiete_ok:
        if force:
            rep.append("! Quiete zone NON rispettata — accettata per --force "
                       "(la schiarita DODGE in render farà da rete)")
        else:
            ok = False
            rep.append("✗ Zone testo non abbastanza quiete: rigenerare la "
                       "tavola o usare --force se la selezione umana approva")

    # 4 ── Ritmo (warning) ──────────────────────────────────────────────────
    seq = [(v["slug"], variante if v["slug"] == slug else v["variante"])
           for v in spec["voci"]
           if v["volume"] == voce["volume"] and v["tipo"] == "tavola"]
    for (sa, a), (sb, b) in zip(seq, seq[1:]):
        if a == b:
            rep.append(f"! RITMO: variante '{a}' consecutiva nel volume "
                       f"{voce['volume']} ({sa} → {sb}) — i test falliranno")

    return ok, manifest, rep


def aggiorna_spec(manifest: dict) -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    for v in spec["voci"]:
        if v["slug"] == manifest["slug"]:
            v["variante"] = manifest["variante"]
            v["tavola"]   = manifest["file"]
            if manifest.get("note"):
                v["note"] = manifest["note"]
    SPEC_PATH.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest tavola-atlante nello spec")
    ap.add_argument("manifest", type=str, help="Path del manifest JSON della tavola")
    ap.add_argument("--dry-run", action="store_true",
                    help="Solo report, non scrive lo spec")
    ap.add_argument("--force", action="store_true",
                    help="Accetta zone non quiete (selezione umana approvata)")
    args = ap.parse_args()

    mp = Path(args.manifest)
    if not mp.is_absolute():
        mp = REPO / mp
    if not mp.exists():
        print(f"✗ Manifest non trovato: {mp}")
        return 2

    ok, manifest, rep = verifica_tavola(mp, force=args.force)
    print(f"\n── Ingest tavola atlante: {mp.name} ──")
    for r in rep:
        print(" ", r)

    if not ok:
        print("\nESITO: RESPINTA — lo spec non è stato toccato.")
        return 1
    if args.dry_run:
        print("\nESITO: OK (dry-run) — lo spec non è stato toccato.")
        return 0

    aggiorna_spec(manifest)
    print(f"\nESITO: ACCETTATA — ATLANTE_SPEC.json aggiornato "
          f"({manifest['slug']} → variante {manifest['variante']}).")
    print("Ora: python3 -m pytest tests/test_atlante.py -q")
    return 0


if __name__ == "__main__":
    sys.exit(main())
