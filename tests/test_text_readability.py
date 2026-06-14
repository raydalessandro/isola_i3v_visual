"""
Test leggibilità testo — scrim adattivo locale (_overlay_text).

Nasce dai "bug di produzione" segnalati sul Volume 1 (testo poco leggibile su
fondi scuri/movimentati). Verifica che lo scrim adattivo:
  - SCHIARISCA il fondo sotto i glifi sulle pagine scure segnalate;
  - lasci pressoché INVARIATE le pagine già chiare (niente slavature);
  - sia LOCALIZZATO sulla sagoma del testo (non una banda piena).

Le pagine segnalate (tutte testo in alto, ciclo Δ Volume 1):
  S1 8a · S2 1a · S2 9b · S3 1a · S3 2b · S3 6a
"""
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_volume as bv  # noqa: E402

KEY = bv.DS.CICLO_COLOR.get("Δ", bv.DS.DEFAULT_QUARTIERE_COLOR)

# pagine segnalate in produzione (richiedevano schiaritura/sfumatura)
REPORTED = ["s01_h08a", "s02_h01a", "s02_h09b", "s03_h01a", "s03_h02b", "s03_h06a"]
# pagina già buona, NON segnalata (controllo non-regressione)
CLEAN = "s01_h05b"


def _subhook(subhook_id):
    sid = subhook_id.split("_")[0]
    return next(s for s in bv.parse_story_md(sid) if s["subhook_id"] == subhook_id)


def _raw_page(sh):
    p = sh["image_path"]
    r = bv.resolve_scene_image(p) if (p and p.exists()) else None
    if r is None:
        return Image.new("RGB", (bv.IMG_W, bv.IMG_H), (245, 241, 233))
    return Image.open(r).convert("RGB").resize((bv.IMG_W, bv.IMG_H), Image.LANCZOS)


def _text_footprint_mask(text):
    """Ricostruisce la sagoma del testo (come fa _overlay_text) per sapere
    dove cadono i glifi: ritorna (mask L, bbox)."""
    FS, LH, PGS, MX2, MT = 50, int(50 * 1.62), int(50 * 0.62), 136, 100
    f = bv.fnt(FS)
    f_key = bv._font_oracolo(FS)
    tmp = Image.new("L", (bv.IMG_W, bv.IMG_H), 0)
    d = ImageDraw.Draw(tmp)
    rows = bv.rich_word_wrap(text, f, f_key, bv.IMG_W - 2 * MX2, d)
    y = MT  # tutte le pagine in esame hanno testo in alto
    for row in rows:
        if not row:
            y += PGS; continue
        bv.draw_rich_row(d, MX2, y, row, f, f_key, 255, 255)
        y += LH
    return tmp, tmp.getbbox()


def _bg_percentile(page, footprint_mask, bbox, pct=75):
    """Luminanza al percentile `pct` dei pixel di FONDO (non-glifo) entro la
    bounding box del testo: rappresenta il fondo che il lettore vede dietro
    le parole, indipendente dall'inchiostro scuro dei glifi."""
    lum = page.convert("L").crop(bbox)
    # fondo = pixel NON coperti dai glifi (maschera invertita), dilatata un po'
    glyph = footprint_mask.crop(bbox).filter(ImageFilter.MaxFilter(3))
    vals = [v for v, g in zip(lum.getdata(), glyph.getdata()) if g < 40]
    if not vals:
        vals = list(lum.getdata())
    vals.sort()
    return vals[int(len(vals) * pct / 100)] / 255.0


@pytest.mark.parametrize("subhook_id", REPORTED)
def test_scrim_schiarisce_fondo_pagine_segnalate(subhook_id):
    """Sulle pagine segnalate il fondo sotto il testo deve risultare più
    chiaro DOPO il trattamento (schiarita effettiva)."""
    sh = _subhook(subhook_id)
    raw = _raw_page(sh)
    mask, bbox = _text_footprint_mask(sh["text"])
    assert bbox is not None
    page = bv._overlay_text(raw.copy(), sh["text"], key_color=KEY)
    bg_raw = _bg_percentile(raw, mask, bbox)
    bg_new = _bg_percentile(page, mask, bbox)
    assert bg_new >= bg_raw, f"{subhook_id}: il trattamento ha scurito il fondo"
    # il fondo trattato deve avvicinarsi alla soglia di leggibilità
    assert bg_new >= 0.62, (
        f"{subhook_id}: fondo sotto il testo ancora troppo scuro "
        f"({bg_new:.2f} < 0.62)")


def test_pagina_chiara_non_slavata():
    """Una pagina già chiara non deve essere washata: il fondo cambia poco."""
    sh = _subhook(CLEAN)
    raw = _raw_page(sh)
    mask, bbox = _text_footprint_mask(sh["text"])
    page = bv._overlay_text(raw.copy(), sh["text"], key_color=KEY)
    bg_raw = _bg_percentile(raw, mask, bbox)
    bg_new = _bg_percentile(page, mask, bbox)
    assert abs(bg_new - bg_raw) < 0.06, (
        f"pagina chiara alterata troppo: {bg_raw:.2f} -> {bg_new:.2f}")


@pytest.mark.parametrize("subhook_id", ["s03_h06a", "s03_h01a"])
def test_scrim_localizzato_non_banda_piena(subhook_id):
    """Lo scrim deve seguire la sagoma del testo: un angolo lontano dal testo
    (in basso, fuori dalla zona testo) resta praticamente invariato."""
    sh = _subhook(subhook_id)
    raw = _raw_page(sh)
    page = bv._overlay_text(raw.copy(), sh["text"], key_color=KEY)
    # angolo in basso a destra, lontano dal testo in alto
    box = (bv.IMG_W - 300, bv.IMG_H - 300, bv.IMG_W, bv.IMG_H)
    a = raw.crop(box).convert("L")
    b = page.crop(box).convert("L")
    from PIL import ImageChops, ImageStat
    d = ImageStat.Stat(ImageChops.difference(a, b)).mean[0]
    assert d < 1.0, f"{subhook_id}: lo scrim sconfina lontano dal testo (Δ={d:.2f})"
