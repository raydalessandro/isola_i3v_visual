#!/usr/bin/env python3
"""
build_volume.py — Compositore volumi L'Isola dei Tre Venti
============================================================
Legge la repo e produce PDF pronti per stampa (Amazon KDP o casalinga).

Struttura output di ogni volume:
  [front matter]  bianca · dedica · bianca
  [soglia]        "Prima di leggere" (identica in tutti i volumi)
  [introduzione]  testo del ciclo (specifico per volume)
  [stato zero]    trafiletto "L'isola dorme" (specifico per volume)
  [presentazione] pagine personaggi/luoghi con illustrazioni HD
                  → posizione configurabile: PRIMA o DOPO la storia
  [storia]        pagine illustrate con testo sovrapposto
  [porte]         "Le porte" (specifico per volume)
  [sigillo/congedo]

Output in _output/:
  vol{N}_libro.pdf           — spread affiancati (sfogliabile)
  vol{N}_stampa.pdf          — pagine singole A5 (da stampare)
  vol{N}_LAYOUT_WARNINGS.md  — testi troncati da correggere nel sorgente

Uso:
  python3 scripts/build_volume.py --volume 1
  python3 scripts/build_volume.py --volume 1 --storie s01
  python3 scripts/build_volume.py --volume 1 --presentazione dopo
  python3 scripts/build_volume.py --volume 1 --solo-storie

Dipendenze:
  pip install Pillow reportlab

Font:
  I file Lora .ttf devono essere in assets/fonts/ (già inclusi nella repo).
  Fallback al sistema se mancano (con warning).
"""

from __future__ import annotations

import argparse
import io
import logging
import re
import sys
import unicodedata
from pathlib import Path
from typing import Literal

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)
log = logging.getLogger("build_volume")

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
except ImportError as exc:
    sys.exit(f"Dipendenza mancante: {exc}\nEsegui: pip install Pillow reportlab")

# ═══════════════════════════════════════════════════════════════════════════
# PERCORSI REPO
# ═══════════════════════════════════════════════════════════════════════════
REPO          = Path(__file__).resolve().parent.parent
SCENE_DIR     = REPO / "pipeline_narrativa/storie_finali/_scene"
STORIE_DIR    = REPO / "pipeline_narrativa/storie_finali"
VOLUMI_DIR    = REPO / "pipeline_narrativa/storie_finali/_volumi"
OUTPUT_DIR    = REPO / "_output"
CARTO_DIR     = REPO / "cartografia/assets_mappa/_base"
MAP_ISOLA     = CARTO_DIR / "isola_base_v1.jpg"

# ─── Font (prima in repo, poi sistema, poi default con warning) ─────────────
_FONT_DIRS = [
    REPO / "assets/fonts",
    Path("/usr/share/fonts/truetype/google-fonts"),  # Linux
    Path("/Library/Fonts"),                           # macOS
    Path("C:/Windows/Fonts"),                         # Windows
]

def _find_font(name: str) -> Path | None:
    for d in _FONT_DIRS:
        fp = d / name
        if fp.exists():
            if d != REPO / "assets/fonts":
                log.warning(
                    "Font '%s' non trovato in assets/fonts/ — uso '%s'. "
                    "Per build riproducibili, aggiungi i .ttf alla repo.",
                    name, d,
                )
            return fp
    log.error("Font '%s' non trovato. Metriche tipografiche non garantite.", name)
    return None

FONT_REG = _find_font("Lora-Variable.ttf")
FONT_ITA = _find_font("Lora-Italic-Variable.ttf")

def fnt(size: int, italic: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_ITA if italic else FONT_REG
    if path and path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()

# ═══════════════════════════════════════════════════════════════════════════
# DIMENSIONI E SCALA
# ═══════════════════════════════════════════════════════════════════════════
# Pagine testo: A5 @ 150 DPI
TX_W, TX_H    = 874, 1240
# Immagini storia: il low-res è 832×1248; lo upscaliamo 2× per stampa HQ
# Le HD in _hd/ sono già ≥1664×2496 e si usano direttamente (no upscale)
IMG_W0, IMG_H0 = 832, 1248   # dimensione canonica per il layout
SCALE          = 2            # fattore upscale del low-res
IMG_W, IMG_H   = IMG_W0 * SCALE, IMG_H0 * SCALE   # 1664×2496
# PDF
PAGE_W_PT  = 148 * mm
PAGE_H_PT  = 210 * mm
SPREAD_W_PT = PAGE_W_PT * 2

# ═══════════════════════════════════════════════════════════════════════════
# PALETTE
# ═══════════════════════════════════════════════════════════════════════════
BG_WARM     = (250, 247, 240)
BG_DARK     = (36,  28,  16)
TEXT_DARK   = (40,  28,  16)
TEXT_MID    = (100, 75,  48)
TEXT_ACCENT = (115, 78,  38)
TEXT_RULE   = (190, 168, 138)
TEXT_LIGHT  = (245, 240, 228)
STORY_INK   = (45,  28,  14)
STORY_HALO  = (250, 246, 236)

# ═══════════════════════════════════════════════════════════════════════════
# TIPOGRAFIA (pagine testo)
# ═══════════════════════════════════════════════════════════════════════════
MX, MY_TOP, MY_BOT = 78, 88, 78
TW       = TX_W - 2 * MX
FS_TITLE = 34;  LH_TITLE = int(FS_TITLE * 1.45)
FS_BODY  = 27;  LH_BODY  = int(FS_BODY  * 1.78)
FS_SMALL = 21;  LH_SMALL = int(FS_SMALL * 1.65)
FS_NUM   = 16
PG       = int(FS_BODY * 0.72)   # gap paragrafo

# ═══════════════════════════════════════════════════════════════════════════
# MAPPATURA VOLUMI
# ═══════════════════════════════════════════════════════════════════════════
VOLUME_CONFIG = {
    1: dict(ciclo="Δ",            storie=["s01","s02","s03"],
            stagione="Inverno → Primavera", vento="Vento Taglio",   vol_id="v01"),
    2: dict(ciclo="⇄",            storie=["s04","s05","s06"],
            stagione="Primavera → Estate",  vento="Vento Intreccio", vol_id="v02"),
    3: dict(ciclo="⟳",            storie=["s07","s08","s09"],
            stagione="Estate → Autunno",    vento="Vento Mulinello", vol_id="v03"),
    4: dict(ciclo="Integrazione", storie=["s10","s11","s12"],
            stagione="Autunno → Inverno",   vento="Tutti e tre",     vol_id="v04"),
}

# ═══════════════════════════════════════════════════════════════════════════
# RISOLUZIONE IMMAGINI — HD-first
# ═══════════════════════════════════════════════════════════════════════════

def resolve_scene_image(low_res_path: Path) -> Path:
    """
    Dato il path low-res `_scene/sNN/sNN_hMMx.jpg`, ritorna il path HD
    `_scene/sNN/_hd/sNN_hMMx_hd.jpg` se esiste, altrimenti il low-res.
    Non modifica mai i .md sorgente — la scelta è trasparente al chiamante.
    """
    hd = low_res_path.parent / "_hd" / (low_res_path.stem + "_hd.jpg")
    if hd.exists():
        return hd
    return low_res_path


def resolve_intro_image(volume: int, slug: str) -> Path | None:
    """
    Cerca l'immagine HD intro volume per un dato slug personaggio.
    Path: _volumi/v0N/_hd/v0N_intro_<slug>_hd.jpg
    slug: snake_case del nome (es. 'fiamma', 'bartolo_toba', 'memolo_pun')
    """
    vol_id = VOLUME_CONFIG[volume]["vol_id"]
    hd_dir = VOLUMI_DIR / vol_id / "_hd"
    candidate = hd_dir / f"{vol_id}_intro_{slug}_hd.jpg"
    if candidate.exists():
        return candidate
    # Fuzzy: cerca qualsiasi file che contiene lo slug
    if hd_dir.exists():
        for f in hd_dir.glob(f"*{slug}*_hd.jpg"):
            return f
    return None


def _title_to_slug(title: str) -> str:
    """'Mèmolo e Pun' → 'memolo_pun', 'Rovo e Bru' → 'rovo_bru'"""
    s = unicodedata.normalize("NFD", title.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"\be\b", "", s)          # rimuovi " e " come congiunzione
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    return s


# ── Specifica qualità minima per le immagini di presentazione ─────────────
# Standard dalla skill illustratore: JPEG q95, RGB sRGB, min 1664×2496 px verticale
PRES_MIN_W   = 1664
PRES_MIN_H   = 2496
PRES_MIN_AREA = PRES_MIN_W * PRES_MIN_H   # usato per orientamento non-verticale


def check_image_quality(path: Path) -> tuple[bool, str]:
    """
    Controlla se un'immagine rispetta gli standard di qualità per la stampa.
    Ritorna (ok: bool, descrizione: str).
    Standard: JPEG, RGB, min 1664×2496 px (verticale).
    Per immagini landscape accetta area equivalente (es. mappa isola).
    """
    if not path.exists():
        return False, f"FILE NON TROVATO"
    try:
        img = Image.open(path)
        w, h = img.size
        area = w * h
        is_vertical = h >= w
        if is_vertical:
            ok = w >= PRES_MIN_W and h >= PRES_MIN_H
        else:
            # Landscape/quadrata: accetta se area >= standard (es. mappa)
            ok = area >= PRES_MIN_AREA
        if ok:
            return True, f"{w}×{h}px ✓"
        else:
            return False, f"{w}×{h}px — sotto spec ({PRES_MIN_W}×{PRES_MIN_H} richiesti)"
    except (OSError, IOError) as exc:
        return False, f"ERRORE LETTURA: {exc}"


def add_quality_banner(img: Image.Image, path: Path, desc: str) -> Image.Image:
    """
    Aggiunge un banner arancione semi-trasparente in fondo all'immagine
    per segnalare che la qualità è sotto spec. Non modifica il file originale.
    Il banner include il path del file da aggiornare.
    """
    img = img.copy()
    # Scala il banner all'altezza dell'immagine passata
    w, h = img.size
    banner_h = max(50, int(h * 0.055))

    # Crea overlay
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw    = ImageDraw.Draw(overlay)

    # Banda arancione in fondo
    banner_color = (220, 100, 20, 200)  # arancione, 78% opacità
    draw.rectangle([(0, h - banner_h), (w, h)], fill=banner_color)

    # Testo
    font_size = max(14, int(banner_h * 0.38))
    f = fnt(font_size)
    msg1 = f"⚠ IMMAGINE SOTTO SPEC — {desc}"
    msg2 = f"Sostituire: {path.name}"

    draw.text((12, h - banner_h + 4),      msg1, font=f, fill=(255, 255, 220, 255))
    draw.text((12, h - banner_h + 4 + font_size + 3), msg2, font=fnt(max(12, font_size - 2)), fill=(255, 240, 180, 220))

    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")


def build_presentazione_image_map(volume: int) -> dict[str, Path | None]:
    """
    Lookup esplicito e curato: titolo presentazione → path immagine migliore.

    Priorità per ogni voce:
      1. HD intro volume (_volumi/v0N/_hd/v0N_intro_<slug>_hd.jpg)
      2. Catalogo HD personaggio/luogo (_hd/ nella cartella immagini)
      3. Catalogo low-res
      4. Mappa isola come placeholder
      5. None → pagina senza illustrazione

    Il controllo qualità (banner) viene applicato al render, non qui.
    Aggiornare questo mapping quando arrivano nuove HD nella repo.
    """
    R  = REPO
    V  = VOLUME_CONFIG[volume]["vol_id"]
    HD = VOLUMI_DIR / V / "_hd"

    def hd(slug: str) -> Path | None:
        """Cerca HD intro volume per slug (es. 'fiamma', 'rovo_bru')."""
        p = HD / f"{V}_intro_{slug}_hd.jpg"
        return p if p.exists() else None

    def cat(rel: str) -> Path | None:
        """Path relativo alla repo."""
        p = R / rel
        return p if p.exists() else None

    M = MAP_ISOLA if MAP_ISOLA.exists() else None

    # Mapping esplicito per Volume 1.
    # Struttura (vol 2-4): aggiungere i casi volume > 1 quando le HD arrivano.
    if volume == 1:
        return {
            # ── Luoghi ────────────────────────────────────────────────────
            "Questa è l'isola":
                M,
            "Il Villaggio":
                cat("visual/luoghi/villaggio_centrale/piazza_villaggio/immagini/piazza_villaggio_canonica_v1_panoramica.jpg"),
            "Il Quartiere di Fuoco":
                cat("visual/luoghi/quartiere_fuoco/forno/immagini/forno_canonica_v1_esterno_alba.jpg"),
            "Il Quartiere d'Aria":
                cat("visual/luoghi/quartiere_aria/via_che_sale/immagini/via_che_sale_canonica_v1_panoramica.jpg"),
            "Il Quartiere di Terra":
                M,
            "Il Quartiere d'Acqua":
                M,
            "Il Mercato del Mezzogiorno":
                M,
            # ── Personaggi primari — HD intro v01 ─────────────────────────
            "Fiamma":
                hd("fiamma"),
            "Grunto":
                hd("grunto"),
            "Rovo e Bru":
                hd("rovo_bru"),
            "Stria":
                hd("stria"),
            "Mèmolo e Pun":
                hd("memolo_pun"),
            "Bartolo e Toba":
                hd("bartolo_toba"),
            # ── Personaggi secondari — HD intro v01 ───────────────────────
            "Nodo":
                hd("nodo"),
            "Salvia":
                hd("salvia"),
            "Zolla":
                hd("zolla"),
            # ── Collettivi / bambini ───────────────────────────────────────
            # "I bambini dell'isola": i tre fratelli insieme.
            # Non esiste ancora un'immagine HD dedicata → usiamo gabriel fronte
            # (low-res) come placeholder; quando arriva l'HD aggiungi hd("bambini").
            "I bambini dell'isola":
                hd("bambini") or
                cat("visual/personaggi/individuali/bambini/gabriel/immagini/gabriel_canonica_v1_fronte.jpg"),
            # "I Pastori": la voce descrive i pastori dell'isola (non i cuccioli
            # camminanti usati prima per errore). Non esiste immagine specifica
            # → mappa come placeholder finché non arriva l'HD.
            "I Pastori":
                hd("pastori") or M,
        }

    # Per volumi futuri: stesso schema, diversi slug
    # (costruire il mapping quando arrivano le HD)
    return {}


def find_presentazione_image(title: str, image_map: dict) -> Path | None:
    """Ricerca con fallback fuzzy + normalizzazione accenti."""
    if title in image_map:
        return image_map[title]

    def norm(s: str) -> str:
        return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                       if unicodedata.category(c) != "Mn")

    t_norm = norm(title)
    for k, v in image_map.items():
        if norm(k) == t_norm:
            return v
    words = [w for w in t_norm.split() if len(w) > 3]
    for k, v in image_map.items():
        if any(w in norm(k) for w in words):
            return v
    return None

# ═══════════════════════════════════════════════════════════════════════════
# PULIZIA TESTO
# ═══════════════════════════════════════════════════════════════════════════

def clean_prose(text: str) -> str:
    """Rimuove marker MD/HTML che non devono apparire in pagina."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"^>.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*-{2,}\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^#{1,4}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\*[^*\n]+\*\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\*\*[^*\n]+\*\*\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\([^)\n]{5,}\)\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*\n]+)\*", r"\1", text)
    text = re.sub(r"[❦❧☘✿❀❁]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def word_wrap(text: str, font: ImageFont.FreeTypeFont,
              max_w: int, draw: ImageDraw.ImageDraw) -> list[str]:
    lines: list[str] = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        cur = ""
        for word in para.split():
            test = (cur + " " + word).strip()
            if draw.textlength(test, font=font) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines

# ═══════════════════════════════════════════════════════════════════════════
# ESTRAZIONE TESTI DAI FILE SORGENTE
# ═══════════════════════════════════════════════════════════════════════════

def _extract_volume_block(filepath: Path, volume: int) -> str:
    text = filepath.read_text(encoding="utf-8")
    pat  = re.compile(r"^#{1,3}\s+VOLUME\s+" + str(volume) + r"\b.*$", re.MULTILINE)
    nxt  = re.compile(r"^#{1,3}\s+VOLUME\s+\d+\b", re.MULTILINE)
    m    = pat.search(text)
    if not m:
        return text
    start  = m.end()
    m_next = nxt.search(text, start)
    return text[start: m_next.start() if m_next else len(text)]


def get_soglia() -> str:
    raw  = (VOLUMI_DIR / "soglia.md").read_text(encoding="utf-8")
    m    = re.search(r"^# Soglia\s*\n(.*)", raw, re.DOTALL | re.MULTILINE)
    body = m.group(1) if m else raw
    return clean_prose(re.sub(r"^## [^\n]+\n", "", body, flags=re.MULTILINE))


def get_introduzione_ciclo(volume: int) -> str:
    return clean_prose(_extract_volume_block(VOLUMI_DIR / "introduzioni_cicli.md", volume))


def get_stato_zero(volume: int) -> str:
    block = _extract_volume_block(VOLUMI_DIR / "stato_zero_e_sigilli.md", volume)
    m = re.search(r"PAGINA DESTRA.*?TRAFILETTO\s*\n(.*)", block, re.DOTALL | re.IGNORECASE)
    if m:
        body  = m.group(1)
        end_m = re.search(r"^---", body, flags=re.MULTILINE)
        return clean_prose(body[: end_m.start()] if end_m else body)
    return clean_prose(block)


def get_sigillo(volume: int) -> str:
    raw     = (VOLUMI_DIR / "stato_zero_e_sigilli.md").read_text(encoding="utf-8")
    m_block = re.search(r"^# 3 SIGILLI.*?\n(.*)", raw, re.DOTALL | re.MULTILINE)
    if not m_block:
        return ""
    pat = re.compile(
        r"^## SIGILLO Vol " + str(volume) + r".*?\n(.*?)(?=^## SIGILLO|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    m = pat.search(m_block.group(1))
    if m:
        return clean_prose(re.sub(r"^\*[^\n]+\*\s*$", "", m.group(1), flags=re.MULTILINE))
    return ""


def get_presentazione_parziale(volume: int) -> list[tuple[str, str]]:
    """Ritorna lista di (titolo, testo) — senza immagini (risolte separatamente)."""
    raw   = (VOLUMI_DIR / "presentazioni_parziali.md").read_text(encoding="utf-8")
    block = _extract_volume_block(VOLUMI_DIR / "presentazioni_parziali.md", volume) \
            if volume > 1 else raw
    block = re.sub(r"^#[^\n]+\n", "", block, count=3, flags=re.MULTILINE)
    block = re.sub(r"^## NOTE TECNICHE.*?(?=^##|\Z)", "", block, flags=re.DOTALL | re.MULTILINE)
    entries = re.findall(
        r"#### \*([^*\n]+)\*\s*\n(.*?)(?=^---\s*$|\Z)", block, re.DOTALL | re.MULTILINE
    )
    return [(t.strip(), clean_prose(body)) for t, body in entries if clean_prose(body)]


def get_porte(volume: int) -> str:
    block = _extract_volume_block(VOLUMI_DIR / "porte.md", volume)
    return clean_prose(re.sub(r"^## NOTE TECNICHE.*?(?=## |\Z)", "", block,
                              flags=re.DOTALL | re.MULTILINE))


def get_congedo() -> str:
    raw  = (VOLUMI_DIR / "congedo.md").read_text(encoding="utf-8")
    m    = re.search(r"^# Congedo\s*\n(.*)", raw, re.DOTALL | re.MULTILINE)
    body = m.group(1) if m else raw
    return clean_prose(re.sub(r"^## [^\n]+\n", "", body, flags=re.MULTILINE))

# ═══════════════════════════════════════════════════════════════════════════
# RENDERING — PAGINE TESTO
# ═══════════════════════════════════════════════════════════════════════════

def make_text_pages(text: str, title: str = "", dark: bool = False) -> list[Image.Image]:
    """Genera 1+ pagine avorio con tipografia gerarchica. Paginazione automatica."""
    bg   = BG_DARK  if dark else BG_WARM
    fg   = TEXT_LIGHT if dark else TEXT_DARK
    mid  = (160, 130, 90) if dark else TEXT_MID
    acc  = (200, 165, 110) if dark else TEXT_ACCENT
    rule = (90, 70, 42)   if dark else TEXT_RULE

    f_title = fnt(FS_TITLE, italic=True)
    f_body  = fnt(FS_BODY)
    f_small = fnt(FS_SMALL, italic=True)

    dummy = Image.new("RGB", (TX_W, TX_H), bg)
    d0    = ImageDraw.Draw(dummy)

    segs: list[tuple] = []
    if title:
        for tl in word_wrap(title, f_title, TW, d0):
            segs.append(("title", tl, f_title, acc, LH_TITLE))
        segs.append(("rule", "", None, rule, 30))

    for para in text.split("\n"):
        if not para.strip():
            segs.append(("gap", "", None, None, PG))
            continue
        is_attr = para.strip().startswith("—") or bool(re.match(r"^\*[^*]+\*$", para.strip()))
        f  = f_small if is_attr else f_body
        lh = LH_SMALL if is_attr else LH_BODY
        tw = TW - 40  if is_attr else TW
        c  = mid      if is_attr else fg
        for ln in word_wrap(para, f, tw, d0):
            segs.append(("body", ln, f, c, lh))
        segs.append(("gap", "", None, None, PG))

    pages: list[Image.Image] = []
    max_y = TX_H - MY_BOT

    def new_canvas():
        img = Image.new("RGB", (TX_W, TX_H), bg)
        return img, ImageDraw.Draw(img), MY_TOP

    img, draw, y = new_canvas()

    for kind, text_s, font_s, color_s, height in segs:
        if kind in ("body", "title") and y + height > max_y:
            draw.line([(MX, TX_H - MY_BOT + 12), (TX_W - MX, TX_H - MY_BOT + 12)],
                      fill=rule, width=1)
            pages.append(img)
            img, draw, y = new_canvas()

        if kind == "title":
            draw.text((MX, y), text_s, font=font_s, fill=color_s)
            y += height
        elif kind == "rule":
            y += 8
            draw.line([(MX, y), (TX_W - MX, y)], fill=color_s, width=1)
            y += 22
        elif kind == "body":
            draw.text((MX, y), text_s, font=font_s, fill=color_s)
            y += height
        else:  # gap
            y += height

    draw.line([(MX, TX_H - MY_BOT + 12), (TX_W - MX, TX_H - MY_BOT + 12)],
              fill=rule, width=1)
    pages.append(img)
    return pages

# ═══════════════════════════════════════════════════════════════════════════
# RENDERING — PAGINA PRESENTAZIONE (immagine + testo)
# ═══════════════════════════════════════════════════════════════════════════

def make_presentazione_page(
    title: str,
    text: str,
    img_path: Path | None,
    layout_warnings: list | None = None,
) -> Image.Image:
    """
    Layout A5: illustrazione in alto (42% pagina) + separatore + titolo + testo.
    Le immagini HD del catalogo v01/_hd/ vengono usate in piena qualità.
    Tronca all'ultima frase completa se il testo eccede; registra avviso.
    Non modifica mai i .md sorgente.
    """
    canvas = Image.new("RGB", (TX_W, TX_H), BG_WARM)
    draw   = ImageDraw.Draw(canvas)

    ILLUS_H = int(TX_H * 0.42)
    SEP_Y   = ILLUS_H + 12
    TEXT_Y  = SEP_Y + 22

    f_title = fnt(FS_TITLE, italic=True)
    f_body  = fnt(FS_BODY)
    f_small = fnt(FS_SMALL, italic=True)

    # Illustrazione — con controllo qualità e banner se sotto spec
    resolved = Path(str(img_path)) if img_path else None
    if resolved and resolved.exists():
        try:
            illus = Image.open(resolved).convert("RGB")
            # Controllo qualità
            ok, quality_desc = check_image_quality(resolved)
            if not ok:
                illus = add_quality_banner(illus, resolved, quality_desc)
                log.warning("Immagine sotto spec per '%s': %s", title, quality_desc)
                if layout_warnings is not None:
                    layout_warnings.append({
                        "entry":         f"[IMMAGINE SOTTO SPEC] {title}",
                        "troncato_dopo": "",
                        "testo_tagliato": "",
                        "suggerimento":  (
                            f'Sostituire immagine per "{title}" con versione HD '
                            f'(min {PRES_MIN_W}×{PRES_MIN_H}px). '
                            f'File attuale: {resolved.relative_to(REPO)} ({quality_desc})'
                        ),
                    })
            iw, ih = illus.size
            ratio  = min(TX_W / iw, ILLUS_H / ih)
            nw, nh = int(iw * ratio), int(ih * ratio)
            illus  = illus.resize((nw, nh), Image.LANCZOS)
            canvas.paste(illus, ((TX_W - nw) // 2, max(0, ILLUS_H - nh)))
        except (FileNotFoundError, OSError, IOError) as exc:
            log.warning("Immagine non caricata '%s': %s", resolved, exc)
    elif resolved:
        log.warning("Immagine non trovata: %s", resolved)

    draw.line([(MX, SEP_Y), (TX_W - MX, SEP_Y)], fill=TEXT_RULE, width=1)

    y = TEXT_Y
    draw.text((MX, y), title, font=f_title, fill=TEXT_ACCENT)
    y += LH_TITLE + 12

    # Overflow detection + truncation a frase completa
    dummy     = ImageDraw.Draw(Image.new("RGB", (TX_W, TX_H)))
    all_lines = word_wrap(text, f_body, TW, dummy)
    max_y     = TX_H - MY_BOT
    y_sim     = y

    for idx, line in enumerate(all_lines):
        inc = PG if line == "" else LH_BODY
        if line != "" and y_sim + inc > max_y:
            rendered  = " ".join(l for l in all_lines[:idx] if l).strip()
            m         = re.search(r"(.*[.!?»])", rendered, re.DOTALL)
            truncated = m.group(1).strip() if m else rendered
            remainder = " ".join(l for l in all_lines[idx:] if l).strip()
            if remainder and layout_warnings is not None:
                layout_warnings.append({
                    "entry":          title,
                    "troncato_dopo":  truncated[-80:],
                    "testo_tagliato": remainder,
                    "suggerimento":   (
                        f'Accorciare "{title}" di ~{len(remainder.split())} parole '
                        f"in presentazioni_parziali.md"
                    ),
                })
            all_lines = word_wrap(truncated, f_body, TW, dummy)
            break
        y_sim += inc

    for line in all_lines:
        if line == "": y += PG; continue
        if y + LH_BODY > max_y: break
        is_attr = line.startswith("—")
        draw.text((MX, y), line,
                  font=f_small if is_attr else f_body,
                  fill=TEXT_MID if is_attr else TEXT_DARK)
        y += LH_SMALL if is_attr else LH_BODY

    draw.line([(MX, TX_H - MY_BOT + 12), (TX_W - MX, TX_H - MY_BOT + 12)],
              fill=TEXT_RULE, width=1)
    return canvas

# ═══════════════════════════════════════════════════════════════════════════
# RENDERING — PAGINA STORIA (illustrata)
# ═══════════════════════════════════════════════════════════════════════════

def compose_story_page(img_path: Path | None, text: str) -> Image.Image:
    """
    Compone una pagina storia:
    - Se esiste la HD (_hd/), la carica direttamente (già ≥1664×2496)
    - Se esiste solo il low-res, fa upscale 2× con Lanczos
    - Se manca, crea un placeholder avorio con il nome file
    Sovrappone il testo con halo leggero per leggibilità.
    """
    FS  = 26 * SCALE    # font size sul canvas 1664×2496
    LH  = int(FS * 1.80)
    PGS = int(FS * 0.65)
    MX2 = 68 * SCALE
    MT  = 44 * SCALE
    HS  = 2 * SCALE
    HB  = 2.5 * SCALE

    # Risolve: se il path punta a low-res, cerca la HD
    if img_path and img_path.exists():
        resolved = resolve_scene_image(img_path)
    elif img_path:
        resolved = img_path  # non esiste — placeholder gestito sotto
    else:
        resolved = None

    # Placeholder se immagine mancante
    if resolved is None or not resolved.exists():
        if resolved:
            log.warning("Immagine storia non trovata: %s", resolved)
        img  = Image.new("RGB", (IMG_W, IMG_H), (245, 241, 233))
        draw = ImageDraw.Draw(img)
        label = resolved.name if resolved else "in lavorazione"
        draw.text((MX2, IMG_H - 100), f"[{label}]", font=fnt(36), fill=(180, 162, 138))
        if text.strip():
            f     = fnt(FS)
            lines = word_wrap(text, f, IMG_W - 2*MX2, draw)
            y     = MT
            for ln in lines:
                if ln == "": y += PGS; continue
                draw.text((MX2, y), ln, font=f, fill=STORY_INK); y += LH
        return img

    # Carica e controlla qualità
    try:
        img = Image.open(resolved).convert("RGBA")
    except (FileNotFoundError, OSError, IOError) as exc:
        log.error("Impossibile aprire '%s': %s", resolved, exc)
        img = Image.new("RGBA", (IMG_W, IMG_H), (245, 241, 233))

    # Controllo qualità: le scene devono essere HD (≥1664×2496)
    # Le immagini low-res vengono upscalate ma ricevono il banner
    ok, quality_desc = check_image_quality(resolved)

    # Normalizza a IMG_W×IMG_H (1664×2496)
    if img.size != (IMG_W, IMG_H):
        img = img.resize((IMG_W, IMG_H), Image.LANCZOS)

    # Testo + halo
    d0    = ImageDraw.Draw(img)
    f     = fnt(FS)
    lines = word_wrap(text, f, IMG_W - 2*MX2, d0)

    halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    hd   = ImageDraw.Draw(halo)
    y    = MT
    for ln in lines:
        if ln == "": y += PGS; continue
        for dx in range(-HS, HS+1):
            for dy in range(-HS, HS+1):
                hd.text((MX2+dx, y+dy), ln, font=f, fill=(*STORY_HALO, 55))
        y += LH
    halo = halo.filter(ImageFilter.GaussianBlur(radius=HB))
    img  = Image.alpha_composite(img, halo)

    draw = ImageDraw.Draw(img)
    y    = MT
    for ln in lines:
        if ln == "": y += PGS; continue
        draw.text((MX2, y), ln, font=f, fill=STORY_INK); y += LH

    # Applica banner qualità sulle storie sotto spec
    if not ok:
        img_rgb = img.convert("RGB")
        img_rgb = add_quality_banner(img_rgb, resolved, quality_desc)
        log.warning("Immagine storia sotto spec: %s (%s)", resolved.name, quality_desc)
        return img_rgb

    return img.convert("RGB")

# ═══════════════════════════════════════════════════════════════════════════
# PARSER STORIA MD
# ═══════════════════════════════════════════════════════════════════════════

def parse_story_md(sid: str) -> list[dict]:
    """Legge i marker @subhook di una storia, ritorna lista di dict."""
    matches = list(STORIE_DIR.glob(f"{sid}_*.md"))
    if not matches:
        log.warning("File storia non trovato: %s", sid)
        return []
    md  = matches[0].read_text(encoding="utf-8")
    pat = re.compile(
        r"<!--\s*@subhook\s+(\S+)\s*\|"
        r"\s*@page_book\s+(\S+)\s*"
        r"(?:\|\s*@layout\s+(\S+)\s*)?"
        r"(?:\|\s*@image\s+([^\s>][^\|>]*?))?\s*-->",
        re.IGNORECASE,
    )
    parts  = pat.split(md)
    result = []
    i      = 1
    while i < len(parts) and i + 4 < len(parts):
        sh_id = parts[i].strip()
        if not re.match(r"s\d+_h\d+[a-z]?$", sh_id):
            i += 5; continue
        page_raw = parts[i+1].strip()
        layout   = (parts[i+2] or "normal").strip()
        img_raw  = (parts[i+3] or "").strip()
        text_raw = parts[i+4] if i+4 < len(parts) else ""

        page_book = (
            [int(n) for n in re.findall(r"\d+", page_raw)] if page_raw.startswith("[")
            else int(page_raw) if page_raw.isdigit() else 0
        )
        text_clean = re.sub(r"<!--.*?-->", "", text_raw, flags=re.DOTALL)
        text_clean = re.sub(
            r"^---\s*$|^##\s+Pagina\s+\d+\s*$", "", text_clean, flags=re.MULTILINE
        ).strip()

        # Risolve path immagine: @image punta al low-res, resolve_scene_image trova l'HD
        if img_raw and img_raw != "TBD":
            low_res = REPO / img_raw.strip()
            img_path = low_res if low_res.exists() else None
        else:
            candidate = SCENE_DIR / sid / f"{sh_id}.jpg"
            img_path  = candidate if candidate.exists() else None

        result.append({
            "subhook_id": sh_id,
            "page_book":  page_book,
            "layout":     layout,
            "text":       text_clean,
            "image_path": img_path,   # low-res; compose_story_page risolverà l'HD
        })
        i += 5
    return result


def get_story_title(sid: str) -> str:
    m_list = list(STORIE_DIR.glob(f"{sid}_*.md"))
    if m_list:
        m = re.search(r"^# S\d+ — (.+)", m_list[0].read_text(), re.MULTILINE)
        if m: return m.group(1)
    return sid

# ═══════════════════════════════════════════════════════════════════════════
# FRONT MATTER
# ═══════════════════════════════════════════════════════════════════════════

DEDICA_DEFAULT = (
    "a Gabriel, Elias e Noah\n"
    "perché i venti della vita\n"
    "possano colorare le vostre vie"
)
MAP_TITLE_PAGE = REPO / "pipeline_narrativa/storie_finali/_scene/mappa_isola.jpg"


def make_blank() -> Image.Image:
    return Image.new("RGB", (TX_W, TX_H), BG_WARM)


def make_dedica(text: str) -> Image.Image:
    """Dedica: corsivo, allineato a destra, posizione centro-basso."""
    img  = Image.new("RGB", (TX_W, TX_H), BG_WARM)
    draw = ImageDraw.Draw(img)
    f    = fnt(FS_SMALL + 3, italic=True)
    lh   = int((FS_SMALL + 3) * 1.70)
    y    = int(TX_H * 0.42)
    for line in text.split("\n"):
        w = draw.textlength(line, font=f)
        draw.text((TX_W - MX - 20 - w, y), line, font=f, fill=TEXT_MID)
        y += lh
    draw.line([(MX, TX_H - MY_TOP + 12), (TX_W - MX, TX_H - MY_TOP + 12)],
              fill=TEXT_RULE, width=1)
    return img


def make_title_map_page(title: str, sid: str, map_path: Path | None = None) -> Image.Image:
    """Pagina titolo storia: mappa isola (55%) + separatore + sigla + titolo."""
    resolved = map_path or (MAP_TITLE_PAGE if MAP_TITLE_PAGE.exists() else None) \
               or (MAP_ISOLA if MAP_ISOLA.exists() else None)
    img  = Image.new("RGB", (TX_W, TX_H), BG_WARM)
    draw = ImageDraw.Draw(img)
    MAP_H = int(TX_H * 0.55)
    MAP_W = TX_W - 2 * MX

    if resolved:
        try:
            mappa = Image.open(str(resolved)).convert("RGB")
            mw, mh = mappa.size
            ratio  = min(MAP_W / mw, MAP_H / mh)
            nw, nh = int(mw * ratio), int(mh * ratio)
            mappa  = mappa.resize((nw, nh), Image.LANCZOS)
            img.paste(mappa, (MX + (MAP_W - nw) // 2, int(TX_H * 0.04)))
        except (FileNotFoundError, OSError, IOError) as exc:
            log.warning("Mappa isola non caricata: %s", exc)

    sep_y = MAP_H + int(TX_H * 0.03)
    draw.line([(MX, sep_y), (TX_W - MX, sep_y)], fill=TEXT_RULE, width=1)

    f_num   = fnt(FS_NUM + 2)
    f_title = fnt(FS_TITLE + 2, italic=True)
    y       = sep_y + 18
    draw.text((MX, y), sid.upper(), font=f_num, fill=TEXT_MID)
    y      += int((FS_NUM + 2) * 1.8) + 8
    dummy   = ImageDraw.Draw(Image.new("RGB", (TX_W, TX_H)))
    for tl in word_wrap(title, f_title, TW, dummy):
        draw.text((MX, y), tl, font=f_title, fill=TEXT_ACCENT)
        y += int((FS_TITLE + 2) * 1.40)

    draw.line([(MX, TX_H - MY_TOP + 12), (TX_W - MX, TX_H - MY_TOP + 12)],
              fill=TEXT_RULE, width=1)
    return img


def ensure_recto(pages: list) -> list:
    """Aggiunge una bianca se necessario perché la prossima pagina cada su recto."""
    if len(pages) % 2 == 1:
        return pages + [("single", make_blank())]
    return pages

# ═══════════════════════════════════════════════════════════════════════════
# COSTRUZIONE PAGINE STORIA
# ═══════════════════════════════════════════════════════════════════════════

def build_story_pages(sid: str) -> list[tuple[str, Image.Image]]:
    pages: list[tuple[str, Image.Image]] = []
    for sh in parse_story_md(sid):
        img = compose_story_page(sh["image_path"], sh["text"])
        if sh["layout"] == "double_spread" or isinstance(sh["page_book"], list):
            sp = Image.new("RGB", (IMG_W * 2 + SCALE * 4, IMG_H), (165, 155, 142))
            sp.paste(img, (0, 0))
            sp.paste(Image.new("RGB", (IMG_W, IMG_H), (245, 241, 233)),
                     (IMG_W + SCALE * 4, 0))
            pages.append(("spread", sp))
        else:
            pages.append(("single", img))
    return pages

# ═══════════════════════════════════════════════════════════════════════════
# COSTRUZIONE SEQUENZA VOLUME
# ═══════════════════════════════════════════════════════════════════════════

def build_volume_pages(
    volume:            int,
    storie_override:   list[str] | None = None,
    solo_storie:       bool = False,
    con_front_matter:  bool = True,
    posizione_pres:    Literal["prima", "dopo"] = "dopo",
    dedica:            str = DEDICA_DEFAULT,
    map_path:          Path | None = None,
) -> tuple[list[tuple[str, Image.Image]], list[dict]]:
    """
    Costruisce la sequenza completa di pagine del volume.

    posizione_pres:
      "prima" — presentazione personaggi/luoghi PRIMA delle storie
      "dopo"  — presentazione DOPO (comportamento precedente)

    Ritorna (pages, layout_warnings).
    """
    cfg    = VOLUME_CONFIG[volume]
    storie = storie_override or cfg["storie"]
    pages: list[tuple[str, Image.Image]] = []
    layout_warnings: list[dict] = []

    image_map = build_presentazione_image_map(volume)

    def add(imgs: list[Image.Image]) -> None:
        for p in imgs: pages.append(("single", p))

    def txt(text: str, title: str = "", dark: bool = False) -> None:
        add(make_text_pages(text, title=title, dark=dark))

    def build_pres_pages() -> None:
        entries = get_presentazione_parziale(volume)
        print(f"  → Presentazione: {len(entries)} voci")
        for t, body in entries:
            img = find_presentazione_image(t, image_map)
            pages.append(("single", make_presentazione_page(
                t, body, img, layout_warnings=layout_warnings)))

    # ── Front matter ──────────────────────────────────────────────────────
    if con_front_matter and not solo_storie:
        pages.extend([
            ("single", make_blank()),
            ("single", make_dedica(dedica)),
            ("single", make_blank()),
        ])

    if not solo_storie:
        print("  → Soglia")
        txt(get_soglia(), title="Prima di leggere")
        print(f"  → Introduzione ciclo {volume}")
        txt(get_introduzione_ciclo(volume))
        print(f"  → Stato Zero vol.{volume}")
        txt(get_stato_zero(volume), title="L'isola dorme")

        if posizione_pres == "prima":
            build_pres_pages()

    # ── Storie ────────────────────────────────────────────────────────────
    for sid in storie:
        title = get_story_title(sid)
        print(f"  → Storia {sid}: {title}")
        if con_front_matter and not solo_storie:
            pages = ensure_recto(pages)
            pages.append(("single", make_title_map_page(title, sid, map_path)))
            pages = ensure_recto(pages)
        else:
            add(make_text_pages("", title=title))
        pages.extend(build_story_pages(sid))

    # ── Sezioni finali ────────────────────────────────────────────────────
    if not solo_storie:
        if posizione_pres == "dopo":
            build_pres_pages()

        print(f"  → Le Porte vol.{volume}")
        txt(get_porte(volume), title="Le porte")

        if volume == 4:
            print("  → Congedo")
            txt(get_congedo(), title="A te che torni")
        else:
            sig = get_sigillo(volume)
            if sig:
                print(f"  → Sigillo vol.{volume}")
                txt(sig, dark=True)

    print(f"  Totale pagine: {len(pages)}")
    return pages, layout_warnings

# ═══════════════════════════════════════════════════════════════════════════
# NORMALIZZAZIONE SPREAD E PDF
# ═══════════════════════════════════════════════════════════════════════════

def _normalize(img: Image.Image) -> Image.Image:
    """Porta a TX_W×TX_H per spread uniformi. Evita distorsioni."""
    return img if img.size == (TX_W, TX_H) else img.resize((TX_W, TX_H), Image.LANCZOS)


def _to_reader(img: Image.Image) -> ImageReader:
    """PIL → ImageReader ReportLab completamente in memoria (zero file temp)."""
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    buf.seek(0)
    return ImageReader(buf)


def _add_page(c: rl_canvas.Canvas, img: Image.Image, w: float, h: float) -> None:
    c.setPageSize((w, h))
    c.drawImage(_to_reader(img), 0, 0, w, h)
    c.showPage()


def build_spread_pdf(pages: list[tuple[str, Image.Image]], out_path: Path) -> None:
    """PDF sfogliabile: spread doppi, tutte le pagine normalizzate a TX_W×TX_H."""
    c = rl_canvas.Canvas(str(out_path))
    i = 0
    while i < len(pages):
        kind, img = pages[i]
        if kind == "spread":
            _add_page(c, img, SPREAD_W_PT, PAGE_H_PT)
            i += 1
        elif i + 1 < len(pages) and pages[i+1][0] == "single":
            left  = _normalize(img)
            right = _normalize(pages[i+1][1])
            sp = Image.new("RGB", (TX_W * 2 + 4, TX_H), BG_WARM)
            sp.paste(left, (0, 0)); sp.paste(right, (TX_W + 4, 0))
            _add_page(c, sp, SPREAD_W_PT, PAGE_H_PT)
            i += 2
        else:  # ultima pagina dispari
            pg = _normalize(img)
            sp = Image.new("RGB", (TX_W * 2 + 4, TX_H), BG_WARM)
            sp.paste(pg, (TX_W + 4, 0))
            _add_page(c, sp, SPREAD_W_PT, PAGE_H_PT)
            i += 1
    c.save()


def build_stampa_pdf(pages: list[tuple[str, Image.Image]], out_path: Path) -> None:
    """PDF stampa: pagine singole A5 in sequenza."""
    c = rl_canvas.Canvas(str(out_path))
    for kind, img in pages:
        if kind == "spread":
            half = img.width // 2
            for side in [img.crop((0,0,half,img.height)),
                         img.crop((half,0,img.width,img.height))]:
                _add_page(c, side, PAGE_W_PT, PAGE_H_PT)
        else:
            _add_page(c, img, PAGE_W_PT, PAGE_H_PT)
    c.save()

# ═══════════════════════════════════════════════════════════════════════════
# REPORT WARNINGS
# ═══════════════════════════════════════════════════════════════════════════

def write_layout_warnings(warnings: list[dict], out_path: Path, pfx: str) -> None:
    # Separa i due tipi di avviso
    img_warnings  = [w for w in warnings if w["entry"].startswith("[IMMAGINE")]
    text_warnings = [w for w in warnings if not w["entry"].startswith("[IMMAGINE")]

    with open(out_path, "w", encoding="utf-8") as wf:
        wf.write(f"# Layout Warnings — {pfx}\n")
        wf.write("_Generato da `build_volume.py`. Non modificare._\n\n")
        wf.write(
            f"**{len(img_warnings)} immagini sotto spec** · "
            f"**{len(text_warnings)} testi troncati**\n\n---\n\n"
        )

        if img_warnings:
            wf.write("## ⚠ Immagini sotto spec\n\n")
            wf.write(
                "Le seguenti immagini non rispettano lo standard di qualità per la stampa "
                f"(min {PRES_MIN_W}×{PRES_MIN_H}px, JPEG q95, RGB sRGB).\n"
                "Nel PDF sono marcate con un banner arancione.\n"
                "Caricare la versione HD nella cartella `_hd/` corrispondente.\n\n"
            )
            for w in img_warnings:
                wf.write(f"- {w['suggerimento']}\n")
            wf.write("\n---\n\n")

        if text_warnings:
            wf.write("## ✂ Testi troncati\n\n")
            wf.write(
                f"I seguenti {len(text_warnings)} testi vengono troncati nella pagina "
                "di presentazione per mancanza di spazio.\n"
                "Correggere in `pipeline_narrativa/storie_finali/_volumi/presentazioni_parziali.md`.\n"
                "Lo script non modifica mai i `.md` sorgente.\n\n"
            )
            for w in text_warnings:
                wf.write(f"### {w['entry']}\n\n")
                if w['troncato_dopo']:
                    wf.write(f"**Tronca dopo:** …{w['troncato_dopo']}\n\n")
                wf.write(f"**Testo tagliato ({len(w['testo_tagliato'].split())} parole):**\n")
                wf.write(f"> {w['testo_tagliato']}\n\n")
                wf.write(f"**Azione:** {w['suggerimento']}\n\n---\n\n")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Compositore volumi — L'Isola dei Tre Venti",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Esempi:\n"
            "  python3 scripts/build_volume.py --volume 1\n"
            "  python3 scripts/build_volume.py --volume 1 --storie s01\n"
            "  python3 scripts/build_volume.py --volume 1 --presentazione prima\n"
            "  python3 scripts/build_volume.py --volume 1 --solo-storie\n"
        ),
    )
    ap.add_argument("--volume",         "-v", type=int, default=1, choices=[1,2,3,4])
    ap.add_argument("--storie",         "-s", nargs="+", metavar="SID")
    ap.add_argument("--presentazione",  "-p", choices=["prima","dopo"], default="dopo",
                    help="Posizione presentazione personaggi: prima o dopo la storia (default: dopo)")
    ap.add_argument("--solo-storie",    action="store_true",
                    help="Solo storie, senza front matter e appendici")
    ap.add_argument("--output",         "-o", type=str, default=None)
    ap.add_argument("--no-stampa",      action="store_true")
    ap.add_argument("--no-libro",       action="store_true")
    ap.add_argument("--dedica",         type=str, default=None,
                    help="Testo dedica (usa \\n per a capo)")
    ap.add_argument("--no-front-matter", action="store_true")
    ap.add_argument("--map",            type=str, default=None,
                    help="Path mappa isola alternativa")
    ap.add_argument("--verbose",        action="store_true")
    args = ap.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    vol = args.volume
    cfg = VOLUME_CONFIG[vol]
    out = Path(args.output) if args.output else OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)

    font_ok   = FONT_REG and FONT_REG.parent == REPO / "assets/fonts"
    map_path  = Path(args.map) if getattr(args, "map", None) else None
    dedica    = getattr(args, "dedica", None) or DEDICA_DEFAULT

    print(f"\n{'='*60}")
    print(f"  L'Isola dei Tre Venti — Volume {vol}  ({cfg['ciclo']})")
    print(f"  {cfg['stagione']}  ·  {cfg['vento']}")
    print(f"  Storie: {', '.join(args.storie or cfg['storie'])}")
    print(f"  Presentazione: {args.presentazione} la storia")
    print(f"  Font: {'repo ✓' if font_ok else 'sistema ⚠'}")
    print(f"  Output: {out}")
    print(f"{'='*60}\n")

    pages, warnings = build_volume_pages(
        volume           = vol,
        storie_override  = args.storie or None,
        solo_storie      = args.solo_storie,
        con_front_matter = not getattr(args, "no_front_matter", False),
        posizione_pres   = args.presentazione,
        dedica           = dedica,
        map_path         = map_path,
    )

    pfx = f"vol{vol}_pres-{args.presentazione}"
    if args.storie:
        pfx += "_" + "-".join(args.storie)

    if not args.no_libro:
        p = out / f"{pfx}_libro.pdf"
        print(f"\nPDF libro → {p.name}")
        build_spread_pdf(pages, p)
        print(f"  ✓ {p.stat().st_size / 1024 / 1024:.1f} MB")

    if not args.no_stampa:
        p = out / f"{pfx}_stampa.pdf"
        print(f"\nPDF stampa → {p.name}")
        build_stampa_pdf(pages, p)
        print(f"  ✓ {p.stat().st_size / 1024 / 1024:.1f} MB")

    if warnings:
        wp = out / f"{pfx}_LAYOUT_WARNINGS.md"
        write_layout_warnings(warnings, wp, pfx)
        print(f"\n⚠  {len(warnings)} avvisi di layout → {wp.name}")
    else:
        print("\n✓  Nessun testo troncato.")

    print(f"\n{'='*60}  Build completato.\n")


if __name__ == "__main__":
    main()
