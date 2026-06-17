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
import json
import logging
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Literal

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.WARNING)
log = logging.getLogger("build_volume")

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat, ImageChops
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
except ImportError as exc:
    sys.exit(f"Dipendenza mancante: {exc}\nEsegui: pip install Pillow reportlab")

# Modulo identità visiva (palette, font, logo, ornamenti, componenti)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import design_system as DS

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
    """Font corpo del testo (Lora). Per display/sans usare DS.font()."""
    path = FONT_ITA if italic else FONT_REG
    if path and path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()

# ═══════════════════════════════════════════════════════════════════════════
# DIMENSIONI E SCALA — stampa Amazon KDP
# ═══════════════════════════════════════════════════════════════════════════
# Specifiche KDP (verificate maggio 2026):
#   - 300 DPI minimo (sotto = warning/rifiuto)
#   - dimensione pagina = trim size esatto
#   - bleed 0.125" (3.175mm) per lato sulle pagine al vivo
#   - font incorporati, colore sRGB
#
# Trim: A5 = 148×210mm. A 300 DPI:
DPI = 300
MM  = 1 / 25.4
TRIM_W_MM, TRIM_H_MM = 148, 210
BLEED_MM = 3.175                          # 0.125"

# Pagine testo: tutta la pagina al trim, a 300 DPI
TX_W = round(TRIM_W_MM * MM * DPI)        # 1748
TX_H = round(TRIM_H_MM * MM * DPI)        # 2480

# Bleed in px (per le pagine illustrate che vanno al vivo)
BLEED_PX = round(BLEED_MM * MM * DPI)     # 38

# Pagine illustrate (storia/presentazione): trim + bleed su ogni lato
IMG_W = TX_W + 2 * BLEED_PX               # 1824
IMG_H = TX_H + 2 * BLEED_PX               # 2556

# Compatibilità con codice esistente
IMG_W0, IMG_H0 = TX_W, TX_H
SCALE = 1

# PDF: il trim (le pagine al vivo includono il bleed nel PDF se richiesto)
PAGE_W_PT  = TRIM_W_MM * mm
PAGE_H_PT  = TRIM_H_MM * mm
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
# Autore UFFICIALE del libro (byline). DEVE combaciare con build_cover.AUTHOR:
# il test test_author_byline.py lo verifica per evitare divergenze cover↔interno.
AUTHOR_BYLINE = "Beatrice Mercuri"
# Luminanza minima desiderata del fondo SOTTO i glifi per una lettura comoda
# dell'inchiostro scuro (0..1). Guida la schiaritura adattiva locale del testo.
STORY_READ_FLOOR = 0.68
STORY_HALO  = (250, 246, 236)

# ═══════════════════════════════════════════════════════════════════════════
# TIPOGRAFIA (pagine testo) — scalata per 300 DPI
# ═══════════════════════════════════════════════════════════════════════════
# A 300 DPI la pagina è ~2× quella a 150, quindi tutta la scala raddoppia.
MX, MY_TOP, MY_BOT = 156, 176, 156
TW       = TX_W - 2 * MX
FS_TITLE = 68;  LH_TITLE = int(FS_TITLE * 1.45)
FS_BODY  = 50;  LH_BODY  = int(FS_BODY  * 1.62)
FS_SMALL = 40;  LH_SMALL = int(FS_SMALL * 1.55)
FS_NUM   = 32
PG       = int(FS_BODY * 0.62)   # gap paragrafo

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
    # Mappa per volume — allineata alla struttura di presentazioni_parziali.md
    # dove le voci sono distribuite sui 4 volumi (aggiornata 2026-05-19):
    #   Vol.1: isola, villaggio, quartieri fuoco/aria, Fiamma, Grunto, Rovo+Bru, Stria, Mèmolo+Pun, bambini
    #   Vol.2: quartieri terra/acqua, Nodo, Salvia, Zolla, Mercato
    #   Vol.3: Bartolo+Toba, altri
    #   Vol.4: I Pastori, altri

    if volume == 1:
        # Le reference personaggio (singole, coppie, collettivi) sono state
        # PROMOSSE dal volume al catalogo il 2026-06-10: vivono in
        # visual/<categoria>/<id>/immagini/. _volumi/ ora contiene solo
        # illustrazioni *prodotte per* il volume (es. intro narrative
        # non-reference). Stria HOLD: HD attuale in volo, Ray cerca versione
        # non-volante prima di promuoverla.
        return {
            # Luoghi vol.1
            "Questa è l'isola":
                M,
            "Il Villaggio":
                cat("visual/luoghi/villaggio_centrale/piazza_villaggio/immagini/piazza_villaggio_canonica_v1_panoramica.jpg"),
            "Il Quartiere di Fuoco":
                cat("visual/luoghi/quartiere_fuoco/forno/immagini/forno_canonica_v1_esterno_alba.jpg"),
            "Il Quartiere d'Aria":
                cat("visual/luoghi/quartiere_aria/via_che_sale/immagini/via_che_sale_canonica_v1_panoramica.jpg"),
            # Personaggi (lo script preferisce automaticamente la HD in _hd/
            # via resolve_scene_image — pattern condiviso col catalogo)
            "Fiamma":
                cat("visual/personaggi/individuali/primari/fiamma/immagini/fiamma_canonica_v1_ritratto.jpg"),
            "Grunto":
                cat("visual/personaggi/individuali/primari/grunto/immagini/grunto_canonica_v1_ritratto.jpg"),
            "Rovo e Bru":
                cat("visual/personaggi/individuali/primari/rovo/immagini/rovo_canonica_v1_con_bru.jpg"),
            "Stria":
                hd("stria"),  # HOLD: HD in volo, da sostituire con non-volante
            "Mèmolo e Pun":
                cat("visual/personaggi/individuali/primari/memolo/immagini/memolo_canonica_v1_con_pun.jpg"),
            "I bambini dell'isola":
                cat("visual/personaggi/individuali/bambini/gabriel/immagini/gabriel_canonica_v1_con_fratelli.jpg"),
        }

    if volume == 2:
        return {
            # Luoghi vol.2
            "Il Quartiere di Terra":       M,
            "Il Quartiere d'Acqua":        M,
            "Il Mercato del Mezzogiorno":   M,
            # Personaggi secondari (HD già in catalogo dopo promozione 2026-06-10)
            "Nodo":
                cat("visual/personaggi/individuali/secondari/nodo/immagini/nodo_canonica_v1_ritratto.jpg"),
            "Salvia":
                cat("visual/personaggi/individuali/secondari/salvia/immagini/salvia_canonica_v1_ritratto.jpg"),
            "Zolla":
                cat("visual/personaggi/individuali/secondari/zolla/immagini/zolla_canonica_v1_ritratto.jpg"),
        }

    if volume == 3:
        return {
            # Personaggi vol.3 — Bartolo+Toba promossi a catalogo 2026-06-10
            "Bartolo e Toba":
                cat("visual/personaggi/individuali/primari/bartolo/immagini/bartolo_canonica_v1_con_toba.jpg"),
        }

    if volume == 4:
        return {
            # Collettivi vol.4 — HD intro v04 (quando disponibili)
            "I Pastori": hd("pastori") or M,
        }

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
    block = _extract_volume_block(VOLUMI_DIR / "presentazioni_parziali.md", volume)
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

def make_text_pages(text: str, title: str = "", dark: bool = False,
                    camuni_seed: int | None = None) -> list[Image.Image]:
    """
    Genera 1+ pagine di testo con tipografia editoriale.
    Titolo in Fraunces, corpo in Lora, filetto-vento sotto il titolo.
    Pagine chiare: petroglifi camuni tenui nei margini (alleggerimento).
    """
    bg   = DS.INK if dark else DS.PAPER
    fg   = DS.PAPER if dark else DS.INK
    acc  = DS.tint_color(DS.ACCENT, 0.3) if dark else DS.ACCENT
    rule = DS.tint_color(DS.INK, 0.6) if dark else DS.RULE

    f_title = DS.font_weighted("display", FS_TITLE, 600)
    f_body  = fnt(FS_BODY)

    dummy = Image.new("RGB", (TX_W, TX_H), bg)
    d0    = ImageDraw.Draw(dummy)

    segs: list[tuple] = []
    if title:
        for tl in word_wrap(title, f_title, TW, d0):
            segs.append(("title", tl, f_title, DS.INK if not dark else fg, LH_TITLE))
        segs.append(("rule", "", None, rule, int(FS_TITLE*0.7)))

    for para in text.split("\n"):
        if not para.strip():
            segs.append(("gap", "", None, None, PG)); continue
        for ln in word_wrap(para, f_body, TW, d0):
            segs.append(("body", ln, f_body, fg, LH_BODY))
        segs.append(("gap", "", None, None, PG))

    pages: list[Image.Image] = []
    max_y = TX_H - MY_BOT
    page_idx = [0]

    def new_canvas():
        img = Image.new("RGB", (TX_W, TX_H), bg)
        dr = ImageDraw.Draw(img)
        # camuni nei margini solo su pagine chiare
        if not dark:
            seed = (camuni_seed if camuni_seed is not None else hash(title) & 0xffff) + page_idx[0]
            DS.scatter_camuni(dr, TX_W, TX_H, seed=seed)
        page_idx[0] += 1
        return img, dr, MY_TOP

    img, draw, y = new_canvas()

    for kind, text_s, font_s, color_s, height in segs:
        if kind in ("body", "title") and y + height > max_y:
            pages.append(img)
            img, draw, y = new_canvas()

        if kind == "title":
            draw.text((MX, y), text_s, font=font_s, fill=color_s)
            y += height
        elif kind == "rule":
            DS.draw_wind_rule(draw, MX, MX + int(TX_W*0.085), y + int(FS_TITLE*0.2),
                              acc, max(2, TX_W//560))
            y += height
        elif kind == "body":
            draw.text((MX, y), text_s, font=font_s, fill=color_s)
            y += height
        else:
            y += height

    pages.append(img)
    return pages

# ═══════════════════════════════════════════════════════════════════════════
# RENDERING — PAGINA PRESENTAZIONE (immagine + testo)
# ═══════════════════════════════════════════════════════════════════════════

# Quartiere d'appartenenza di ogni voce dell'atlante (slug → quartiere).
# Ricavato dai luoghi delle entità nel catalogo visual.
ENTITA_QUARTIERE = {
    # personaggi primari/secondari
    "fiamma": "fuoco",
    "grunto": "aria",
    "rovo_bru": "terra", "rovo": "terra", "bru": "terra",
    "salvia": "terra", "zolla": "terra",
    "amo": "acqua",
    "stria": "centro", "memolo_pun": "centro", "memolo": "centro",
    "nodo": "centro", "bartolo": "centro", "bartolo_toba": "centro",
    "bambini": "centro",
    # luoghi
    "questa_e_l_isola": "centro", "il_villaggio": "centro",
    "il_quartiere_di_fuoco": "fuoco", "il_quartiere_d_aria": "aria",
    "il_quartiere_di_terra": "terra", "il_quartiere_d_acqua": "acqua",
}


def _quartiere_color_for(title: str):
    """Colore della cornice in base al quartiere d'appartenenza della voce.
    Se il quartiere non è noto, usa l'accento neutro."""
    slug = _title_to_slug(title)
    q = ENTITA_QUARTIERE.get(slug)
    if q:
        return DS.QUARTIERE_COLOR.get(q, DS.DEFAULT_QUARTIERE_COLOR)
    return DS.DEFAULT_QUARTIERE_COLOR


def _vento_color_for(volume: int, title: str):
    """Colore-accento di una voce: il colore del suo quartiere."""
    return _quartiere_color_for(title)


def make_presentazione_page(
    title: str,
    text: str,
    img_path: Path | None,
    volume: int = 1,
    kind: str = "personaggio",
    layout_warnings: list | None = None,
) -> Image.Image:
    """
    Pagina-atlante (galleria abitanti) — comune a tutti i volumi.
    Layout mix A+C:
      - nome grande in alto a sinistra (ingresso dinamico) + glifo-vento
      - ritratto in cornice-grappolo a destra, fuso nella carta
      - testo in colonna a sinistra con capolettera nel colore-vento
      - firma in basso: oggetto del personaggio + glifo + separatore camuno
    Velo tenue del colore-vento su tutta la pagina (lega gli elementi).
    Niente linee dritte: separatori sempre in stile camuno.
    """
    vento = _vento_color_for(volume, title)
    slug  = _title_to_slug(title)
    motifs = DS.MOTIF_MAP.get(slug, DS.DEFAULT_MOTIFS)
    glifo_fn = DS.GLIFO_VENTO.get(VOLUME_CONFIG[volume]["ciclo"], DS.glifo_mulinello)

    # base con velo tenue del vento
    canvas = Image.blend(Image.new("RGB", (TX_W, TX_H), DS.PAPER),
                         Image.new("RGB", (TX_W, TX_H), vento), 0.03)
    draw = ImageDraw.Draw(canvas)
    MX2 = int(TX_W * 0.10)

    # ── Nome in alto a sinistra (da C) — peso 450, piu' caldo ─────────────
    y = int(TX_H * 0.075)
    f_eye = DS.font_weighted("sans", int(FS_SMALL*0.82), 700)
    eyebrow = "UN ABITANTE DELL'ISOLA" if kind == "personaggio" else "UN LUOGO DELL'ISOLA"
    ex = MX2
    for ch in eyebrow:
        draw.text((ex, y), ch, font=f_eye, fill=vento)
        ex += draw.textlength(ch, font=f_eye) + 4
    y += int(TX_H * 0.030)

    f_name = DS.font_weighted("display", int(TX_W*0.072), 450)
    draw.text((MX2, y), title, font=f_name, fill=DS.INK)
    name_w = draw.textlength(title, font=f_name)
    # glifo-vento accanto al nome
    glifo_fn(draw, int(MX2 + name_w + TX_W*0.045), int(y + TX_W*0.032),
             int(TX_W*0.020), vento, max(2, TX_W//500))
    name_top = y
    y += int(TX_H * 0.072)

    # ── Ritratto in cornice-grappolo a destra (da A) ──────────────────────
    bw = int(TX_W * 0.44)
    bh = int(TX_H * 0.36)
    img_box = (TX_W - MX2 - bw, y, TX_W - MX2, y + bh)
    placed = None
    resolved = Path(str(img_path)) if img_path else None
    if resolved and resolved.exists():
        try:
            illus = Image.open(resolved).convert("RGB")
            ok, quality_desc = check_image_quality(resolved)
            if not ok:
                illus = add_quality_banner(illus, resolved, quality_desc)
                log.warning("Immagine sotto spec per '%s': %s", title, quality_desc)
                if layout_warnings is not None:
                    layout_warnings.append({
                        "entry": f"[IMMAGINE SOTTO SPEC] {title}",
                        "troncato_dopo": "", "testo_tagliato": "",
                        "suggerimento": (
                            f'Sostituire immagine per "{title}" con versione HD '
                            f'(min {PRES_MIN_W}×{PRES_MIN_H}px). '
                            f'File attuale: {resolved.relative_to(REPO)} ({quality_desc})'
                        ),
                    })
            placed = DS.paste_soft(canvas, illus, img_box,
                                   feather=int(TX_W*0.016), paper=DS.PAPER)
        except (FileNotFoundError, OSError, IOError) as exc:
            log.warning("Immagine non caricata '%s': %s", resolved, exc)
    elif resolved:
        log.warning("Immagine non trovata: %s", resolved)

    draw = ImageDraw.Draw(canvas)
    if placed:
        pad = int(TX_W * 0.018)
        frame = (placed[0]-pad, placed[1]-pad, placed[2]+pad, placed[3]+pad)
        DS.cornice_grappolo(draw, frame, vento, max(3, TX_W//460), int(TX_W*0.020))

    # ── Testo: colonna stretta accanto all'immagine, poi piena sotto ──────
    f_body = fnt(FS_BODY)
    LH = LH_BODY
    f_drop = DS.font_weighted("display", int(TX_W*0.060), 500)
    ty = y
    full_w = TX_W - 2 * MX2                              # piena larghezza
    # bordo reale della cornice (placed puo' differire dal box teorico:
    # l'immagine verticale viene contenuta e centrata, quindi piu' stretta)
    if placed:
        pad = int(TX_W * 0.018)
        frame_left   = placed[0] - pad
        # le spiraline d'angolo della cornice grappolo sporgono oltre il
        # rettangolo: includiamo il loro ingombro (unit) nel bordo basso
        frame_bottom = placed[3] + pad + int(TX_W*0.020)
    else:
        frame_left   = TX_W - MX2 - bw
        frame_bottom = y + bh
    # la colonna stretta si ferma al bordo SINISTRO reale della cornice,
    # con un margine extra perche' le spiraline d'angolo sporgono all'interno
    col_w = frame_left - MX2 - int(TX_W*0.055)
    img_bottom = frame_bottom
    max_y = TX_H - int(TX_H * 0.14)   # spazio per la firma

    # capolettera nel colore-vento
    first, rest = text[0], text[1:]
    draw.text((MX2, ty - int(TX_W*0.004)), first, font=f_drop, fill=vento)
    dw = draw.textlength(first, font=f_drop)
    indent = int(dw + TX_W*0.010)

    dummy = ImageDraw.Draw(Image.new("RGB", (TX_W, TX_H)))

    # Costruisce le righe rispettando la larghezza CORRENTE (cambia quando
    # scendiamo sotto l'immagine): prima passata stima riga per riga.
    words = rest.strip().split()
    lines = []          # (testo, x_offset, larghezza_usata)
    cur = ""
    yy = ty
    line_no = 0
    i = 0
    def avail_width(y_pos, line_no, crossed):
        # accanto all'immagine: colonna stretta; sotto: piena larghezza
        if not crossed:
            xoff = indent if line_no < 2 else 0
            return col_w - xoff, (MX2 + xoff)
        else:
            return full_w, MX2

    crossed = False
    while i < len(words) and yy + LH <= max_y:
        # se la riga corrente cadrebbe a cavallo del bordo immagine, salta
        # sotto la cornice con un piccolo respiro (una sola volta)
        if not crossed and yy + LH > img_bottom:
            yy = img_bottom + int(TX_H*0.030)
            crossed = True
        w_av, x_at = avail_width(yy, line_no, crossed)
        cur = ""
        while i < len(words):
            t = (cur + " " + words[i]).strip()
            if dummy.textlength(t, font=f_body) <= w_av:
                cur = t; i += 1
            else:
                break
        if not cur:
            cur = words[i]; i += 1
        lines.append((cur, x_at, yy)); yy += LH; line_no += 1

    # overflow → warning
    if i < len(words) and layout_warnings is not None:
        remainder = " ".join(words[i:]).strip()
        if remainder:
            layout_warnings.append({
                "entry": title,
                "troncato_dopo": (lines[-1][0][-60:] if lines else ""),
                "testo_tagliato": remainder,
                "suggerimento": (
                    f'Accorciare "{title}" di ~{len(remainder.split())} parole '
                    f"in presentazioni_parziali.md"
                ),
            })

    for ln, x_at, ly in lines:
        draw.text((x_at, ly), ln, font=f_body, fill=DS.INK)

    # ── Firma in basso (da A): oggetto + glifo + separatore camuno ────────
    fy = int(TX_H * 0.90)
    obj_motif = motifs[-1] if motifs else None
    if obj_motif:
        obj_motif(draw, int(TX_W*0.42), fy, int(TX_W*0.026), vento)
    glifo_fn(draw, int(TX_W*0.58), fy, int(TX_W*0.020), vento, max(2, TX_W//500))
    # separatore camuno al posto del filetto dritto
    DS.separatore_camuno(draw, TX_W//2 - int(TX_W*0.14), TX_W//2 + int(TX_W*0.14),
                         fy + int(TX_H*0.030), DS.tint_color(vento, 0.35),
                         max(2, TX_W//560))

    return canvas

# ═══════════════════════════════════════════════════════════════════════════
# RENDERING — DOPPIA "QUESTA È L'ISOLA" (mappa-veduta a sinistra, testo a destra)
# ═══════════════════════════════════════════════════════════════════════════
# La voce mappa apre l'atlante con una doppia pagina: pagina sinistra =
# veduta dell'isola a piena pagina; pagina destra = trafiletto su carta.
# Così il testo lungo non si sovrappone mai all'immagine.

ISOLA_PANORAMICA = REPO / "visual/atlante/isola/_hd/isola_notturna_hd.jpg"
ISOLA_CHE_DORME  = REPO / "visual/atlante/isola/isola_che_dorme_v1.jpg"
# Mappa aerea dell'isola DI GIORNO (vista dall'alto), versione HD SENZA testo
# (la candidate_v2 ha il titolo impresso → doppione col titolo dell'atlante).
ISOLA_AEREA_GIORNO = REPO / "pipeline_narrativa/storie_finali/_volumi/v01/_hd/v01_copertina_candidate_v1_hd.jpg"

# ── Sorgenti immagine del FRONT MATTER Vol.1 — UNICA FONTE DI VERITÀ ──────────
# Tre slot facili da scambiare per sbaglio. Cambiare SOLO qui. I test in
# tests/test_frontmatter_images.py verificano PRIMA del build che notte / giorno
# / copertina non finiscano nel posto sbagliato (luminanza + filename).
OCCHIELLO_COVER = REPO / "pipeline_narrativa/storie_finali/_volumi/v01/_hd/v01_copertina_notxt_hd.jpg"
OCCHIELLO_COVER_FALLBACKS = [
    REPO / "visual/atlante/emblema/copertina_clean_v2.png",
    REPO / "visual/atlante/emblema/copertina_v1.jpg",
]
FRONTMATTER_ISOLA = {
    "stato_zero":           ISOLA_PANORAMICA,    # "Ecco l'isola" — veduta NOTTURNA
    "atlante_questa_isola": ISOLA_AEREA_GIORNO,  # "Questa è l'isola" — mappa GIORNO
}


def _occhiello_cover_path() -> "Path | None":
    """Sorgente della pagina-2 (occhiello copertina): la cover SENZA testo, con
    fallback. Centralizzata e testabile (vedi test_frontmatter_images)."""
    for p in (OCCHIELLO_COVER, *OCCHIELLO_COVER_FALLBACKS):
        if p.exists():
            return p
    return None


def make_isola_doppia(
    title: str,
    text: str,
    img_path: Path | None = None,
    volume: int = 1,
    layout_warnings: list | None = None,
    eyebrow: str = "UN LUOGO DELL'ISOLA",
    src_default: Path | None = None,
    remainder_out: list | None = None,
) -> Image.Image:
    """
    Spread "Questa è l'isola" / "L'isola che dorme": ritorna un'immagine larga
    IMG_W*2 (sinistra + destra già affiancate), compatibile con
    build_spread_pdf / build_stampa_pdf.
    Sinistra: veduta isola full-bleed (scala per altezza, sfumata sul bordo
    esterno). Destra: trafiletto su carta con eyebrow, titolo+glifo,
    capolettera, decori marini e firma — stesso linguaggio dell'atlante.
    """
    src = img_path or src_default or ISOLA_PANORAMICA
    import numpy as np
    vento    = _quartiere_color_for(title)
    slug     = _title_to_slug(title)
    motifs   = DS.MOTIF_MAP.get(slug, DS.DEFAULT_MOTIFS)
    glifo_fn = DS.GLIFO_VENTO.get(VOLUME_CONFIG[volume]["ciclo"], DS.glifo_mulinello)

    # ── PAGINA SINISTRA — la veduta dell'isola, satura, protagonista ──────
    # L'isola riempie tutta la larghezza. Sul bordo ESTERNO (sinistro = taglio
    # del libro) l'immagine si sfuma dolcemente, così non c'è stacco netto col
    # La pagina sinistra ospita la veduta dell'isola. NON usiamo un gradiente
    # azzurro artificiale come sfondo (creava una "striscia" che litigava coi
    # colori dell'immagine): la SOLA sorgente di colore è l'immagine stessa.
    mare = DS.CICLO_COLOR.get(VOLUME_CONFIG[volume]["ciclo"], DS.VENTO_TAGLIO)
    left = Image.new("RGB", (IMG_W, IMG_H), DS.PAPER)
    isola_fit = None
    if src and Path(src).exists():
        isola = Image.open(src).convert("RGB")
        ok, quality_desc = (check_tavola_quality(Path(src)) if src == ISOLA_PANORAMICA
                            else check_image_quality(Path(src)))
        # Scala per ALTEZZA piena: immagine intera in verticale, ancorata al
        # bordo ESTERNO (sinistro = taglio del libro), dove resta netta.
        sw, sh = isola.size
        scale = IMG_H / sh
        nw, nh = int(round(sw * scale)), IMG_H
        isola_fit = isola.resize((nw, nh), Image.LANCZOS).convert("RGB")
        oy = 0
        # ── Coda di colore: estende i COLORI REALI dell'immagine verso destra ──
        # Lo spazio tra il bordo destro dell'immagine (nw) e il bordo pagina
        # (IMG_W) viene riempito stirando l'ultima colonna dell'immagine, così
        # i colori dell'isola (mare/cielo/tramonto di quella riga) proseguono
        # nella pagina-testo e vi si dissolvono. È l'immagine che cola di là,
        # non una banda artificiale che fa da ponte.
        gap = IMG_W - nw
        if gap > 0:
            edge = isola_fit.crop((nw - 1, 0, nw, nh))          # ultima colonna
            tail = edge.resize((gap, nh), Image.LANCZOS)        # stirata a destra
            # leggera sfocatura orizzontale per togliere ogni rigatura netta
            tail = tail.filter(ImageFilter.GaussianBlur(max(1, gap // 8)))
            left.paste(tail, (nw, 0))
        left.paste(isola_fit, (0, oy))
        # Dissolvenza finale verso la carta SOLO nell'ultimo tratto a destra,
        # così la coda di colore non arriva dura al bordo pagina ma sfuma nel
        # foglio dove inizia la pagina-testo.
        fade_start = nw + int(gap * 0.35)
        fade_w = IMG_W - fade_start
        if fade_w > 0:
            band = left.crop((fade_start, 0, IMG_W, IMG_H)).convert("RGB")
            paper = Image.new("RGB", (fade_w, IMG_H), DS.PAPER)
            m = np.tile(
                (np.linspace(0.0, 1.0, fade_w) ** 1.5 * 255).astype("uint8"),
                (IMG_H, 1))
            blended = Image.composite(paper, band, Image.fromarray(m, "L"))
            left.paste(blended, (fade_start, 0))
        if not ok:
            left = add_quality_banner(left, Path(src), quality_desc)
            log.warning("Veduta isola sotto spec: %s", quality_desc)
            if layout_warnings is not None:
                layout_warnings.append({
                    "entry": f"[IMMAGINE SOTTO SPEC] {title}",
                    "troncato_dopo": "", "testo_tagliato": "",
                    "suggerimento": (
                        f'Sostituire veduta isola con versione HD '
                        f'(min {TX_W}×{TX_H}px). File: {Path(src).name} ({quality_desc})'
                    ),
                })
    else:
        log.warning("Veduta isola non trovata: %s", src)
        d0 = ImageDraw.Draw(left)
        d0.text((BLEED_PX + 60, IMG_H - 120), "[veduta isola in lavorazione]",
                font=fnt(36), fill=(180, 162, 138))

    # ── PAGINA DESTRA — trafiletto su carta, col mare che entra da sinistra ─
    right = Image.blend(Image.new("RGB", (IMG_W, IMG_H), DS.PAPER),
                        Image.new("RGB", (IMG_W, IMG_H), vento), 0.03)
    # Fascia di mare sul bordo SINISTRO (confine con l'isola) che si dissolve
    # nella carta. Sorgente colore: l'ULTIMA colonna dell'immagine isola (gli
    # stessi colori in cui finisce la pagina sinistra), così attraverso la
    # piega il colore è CONTINUO — l'immagine cola davvero nel testo, niente
    # banda azzurra artificiale. Fallback al mare-gradiente se manca l'immagine.
    band_w = int(IMG_W * 0.30)
    if isola_fit is not None:
        edge_r = isola_fit.crop((isola_fit.width - 1, 0, isola_fit.width, isola_fit.height))
        sea = edge_r.resize((band_w, IMG_H), Image.LANCZOS).filter(
            ImageFilter.GaussianBlur(max(1, band_w // 6)))
    else:
        sea = DS.mare_gradiente(band_w, IMG_H, mare, riflesso=0.5)
    # maschera orizzontale: piena a sinistra (x=0), 0 verso destra (dissolve).
    # Coda lunga e morbida (cubica) così il passaggio è impercettibile.
    xs = 1.0 - np.linspace(0.0, 1.0, band_w)
    col = (255 * xs**3).astype("uint8")             # (band_w,)
    mask_arr = np.repeat(col[None, :], IMG_H, axis=0)  # (IMG_H, band_w)
    mask = Image.fromarray(mask_arr, "L")
    right.paste(sea, (0, 0), mask)
    # decori marini ancorati alla fascia (dove c'è acqua, non nel bianco)
    dR = ImageDraw.Draw(right)
    deco_r = DS.tint_color(mare, 0.32)
    sea_mid = int(band_w * 0.34)     # centro visivo della parte ancora "mare"
    DS.onde(dR, int(band_w*0.06), int(band_w*0.58), int(IMG_H*0.20), deco_r, max(2,IMG_W//1000))
    DS.gabbiano(dR, sea_mid, int(IMG_H*0.115), int(band_w*0.13), deco_r, max(2,IMG_W//1000))
    DS.gabbiano(dR, int(sea_mid*1.4), int(IMG_H*0.14), int(band_w*0.09), deco_r, max(2,IMG_W//1100))
    DS.barchetta(dR, sea_mid, int(IMG_H*0.48), int(band_w*0.15), deco_r, max(2,IMG_W//950))
    DS.pesce(dR, int(band_w*0.30), int(IMG_H*0.64), int(band_w*0.11), deco_r, max(2,IMG_W//1050))
    DS.onde(dR, int(band_w*0.06), int(band_w*0.52), int(IMG_H*0.82), deco_r, max(2,IMG_W//1000), fase=0.9)
    draw = ImageDraw.Draw(right)
    MX = int(band_w * 0.66) + int(TX_W * 0.04)   # testo oltre la fascia mare
    RW = (IMG_W - BLEED_PX - int(TX_W * 0.10)) - MX   # larghezza utile testo
    y  = BLEED_PX + int(TX_H * 0.075)

    f_eye = DS.font_weighted("sans", int(FS_SMALL*0.82), 700)
    ex = MX
    for ch in eyebrow:
        draw.text((ex, y), ch, font=f_eye, fill=vento)
        ex += draw.textlength(ch, font=f_eye) + 4
    y += int(TX_H * 0.030)

    f_name = DS.font_weighted("display", int(TX_W*0.072), 450)
    draw.text((MX, y), title, font=f_name, fill=DS.INK)
    name_w = draw.textlength(title, font=f_name)
    glifo_fn(draw, int(MX + name_w + TX_W*0.045), int(y + TX_W*0.032),
             int(TX_W*0.020), vento, max(2, TX_W//500))
    y += int(TX_H * 0.082)

    # corpo con capolettera nel colore-vento
    fs = FS_BODY
    LH = LH_BODY
    f_body = fnt(fs)
    f_drop = DS.font_weighted("display", int(fs*2.05), 500)
    first, rest = text[0], text[1:]
    d_box = draw.textbbox((0, 0), first, font=f_drop)
    drop_h = d_box[3] - d_box[1]
    draw.text((MX, y - d_box[1]), first, font=f_drop, fill=vento)
    indent = int((d_box[2] - d_box[0]) + TX_W*0.012)
    drop_lines = max(2, -(-drop_h // LH))

    words = rest.strip().split()
    yy, line_no, i = y, 0, 0
    max_y = BLEED_PX + int(TX_H * 0.88)
    lines: list[tuple[str, int, int]] = []
    while i < len(words) and yy + LH <= max_y:
        xoff = indent if line_no < drop_lines else 0
        w_av = RW - xoff
        cur = ""
        while i < len(words):
            t = (cur + " " + words[i]).strip()
            if draw.textlength(t, font=f_body) <= w_av:
                cur = t; i += 1
            else:
                break
        if not cur:
            cur = words[i]; i += 1
        lines.append((cur, MX + xoff, yy)); yy += LH; line_no += 1

    if i < len(words):
        remainder = " ".join(words[i:]).strip()
        if remainder and remainder_out is not None:
            remainder_out.append(remainder)
        elif remainder and layout_warnings is not None:
            layout_warnings.append({
                "entry": title,
                "troncato_dopo": (lines[-1][0][-60:] if lines else ""),
                "testo_tagliato": remainder,
                "suggerimento": (
                    f'Accorciare "{title}" di ~{len(remainder.split())} parole '
                    f"in presentazioni_parziali.md"
                ),
            })
    for ln, x_at, ly in lines:
        draw.text((x_at, ly), ln, font=f_body, fill=DS.INK)

    # firma in basso (pagina destra)
    fy = BLEED_PX + int(TX_H * 0.90)
    obj_motif = motifs[-1] if motifs else None
    if obj_motif:
        obj_motif(draw, MX + int(TX_W*0.32), fy, int(TX_W*0.026), vento)
    glifo_fn(draw, MX + int(TX_W*0.48), fy, int(TX_W*0.020), vento, max(2, TX_W//500))
    cx = MX + RW // 2
    DS.separatore_camuno(draw, cx - int(TX_W*0.14), cx + int(TX_W*0.14),
                         fy + int(TX_H*0.030), DS.tint_color(vento, 0.35),
                         max(2, TX_W//560))

    # ── Affianca: spread larga IMG_W*2 ───────────────────────────────────
    spread = Image.new("RGB", (IMG_W * 2 + SCALE * 4, IMG_H), (165, 155, 142))
    spread.paste(left, (0, 0))
    spread.paste(right, (IMG_W + SCALE * 4, 0))
    return spread


# ═══════════════════════════════════════════════════════════════════════════
# RENDERING — PAGINA ATLANTE A TAVOLA (taccuino del naturalista)
# ═══════════════════════════════════════════════════════════════════════════
# Le tavole sono immagini full-page SENZA TESTO (visual/atlante/tavole/),
# generate con Manus lasciando quiete le zone definite in ATLANTE_SPEC.json.
# Il testo viene sovrapposto qui, in modo puramente meccanico, leggendo
# la variante di layout assegnata alla voce. Design-back from the answer:
# la verità sta nello spec, non nel prompt.

ATLANTE_DIR  = REPO / "visual/atlante"
ATLANTE_SPEC = ATLANTE_DIR / "ATLANTE_SPEC.json"
ATL_MIN_W, ATL_MIN_H = TX_W, TX_H        # la tavola È la pagina: min full-bleed trim

_atlante_spec_cache: dict | None = None


def load_atlante_spec(force: bool = False) -> dict | None:
    """Carica e cache-a ATLANTE_SPEC.json. None se il file non esiste."""
    global _atlante_spec_cache
    if _atlante_spec_cache is not None and not force:
        return _atlante_spec_cache
    if not ATLANTE_SPEC.exists():
        return None
    _atlante_spec_cache = json.loads(ATLANTE_SPEC.read_text(encoding="utf-8"))
    return _atlante_spec_cache


def atlante_entry_for(title: str) -> tuple[dict, Path] | None:
    """
    Se la voce ha una tavola pronta nello spec, ritorna (voce, path_tavola).
    Altrimenti None → il chiamante cade sul layout classico (degradazione
    dolce: il volume si monta sempre, con o senza tavole).
    """
    spec = load_atlante_spec()
    if spec is None:
        return None
    slug = _title_to_slug(title)
    for voce in spec.get("voci", []):
        if voce.get("slug") != slug:
            continue
        if voce.get("tipo") != "tavola" or not voce.get("tavola"):
            return None
        p = REPO / voce["tavola"]
        if not p.exists():
            log.warning("Tavola atlante dichiarata ma assente: %s", p)
            return None
        return voce, p
    return None


def check_tavola_quality(path: Path) -> tuple[bool, str]:
    """Qualità minima tavola atlante: pagina intera verticale (TX_W×TX_H)."""
    if not path.exists():
        return False, "FILE NON TROVATO"
    try:
        img = Image.open(path)
        w, h = img.size
        if w >= ATL_MIN_W and h >= ATL_MIN_H and h >= w:
            return True, f"{w}×{h}px ✓"
        return False, f"{w}×{h}px — sotto spec ({ATL_MIN_W}×{ATL_MIN_H} richiesti, verticale)"
    except (OSError, IOError) as exc:
        return False, f"ERRORE LETTURA: {exc}"


def _cover_fit(img: Image.Image, w: int, h: int) -> Image.Image:
    """Riempie w×h preservando le proporzioni (crop centrale dell'eccesso)."""
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    nw, nh = max(w, int(round(sw * scale))), max(h, int(round(sh * scale)))
    img = img.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - w) // 2
    y0 = (nh - h) // 2
    return img.crop((x0, y0, x0 + w, y0 + h))


def _contain_fit(img: Image.Image, w: int, h: int) -> Image.Image:
    """
    Mostra l'immagine INTERA dentro w×h (niente crop), centrata. Le bande
    di riempimento prendono il colore medio del bordo corrispondente
    dell'immagine (per la veduta isola = il mare), così la cornice non
    stacca e sembra continuità.
    """
    sw, sh = img.size
    scale = min(w / sw, h / sh)
    nw, nh = max(1, int(round(sw * scale))), max(1, int(round(sh * scale)))
    resized = img.resize((nw, nh), Image.LANCZOS)
    # colore di fondo: media dei bordi laterali (o sup/inf) dell'immagine
    if nw < w:   # bande verticali ai lati → campiona colonne di bordo
        left_col  = resized.crop((0, 0, 2, nh))
        right_col = resized.crop((nw - 2, 0, nw, nh))
        bg = tuple(int((a + b) / 2) for a, b in zip(
            ImageStat.Stat(left_col).mean, ImageStat.Stat(right_col).mean))
    else:        # bande orizzontali sopra/sotto → campiona righe di bordo
        top_row = resized.crop((0, 0, nw, 2))
        bot_row = resized.crop((0, nh - 2, nw, nh))
        bg = tuple(int((a + b) / 2) for a, b in zip(
            ImageStat.Stat(top_row).mean, ImageStat.Stat(bot_row).mean))
    bg = tuple(max(0, min(255, c)) for c in bg[:3])
    canvas = Image.new("RGB", (w, h), bg)
    canvas.paste(resized, ((w - nw) // 2, (h - nh) // 2))
    return canvas


def _quiet_zone(canvas: Image.Image, box: tuple[int, int, int, int],
                strength: float = 0.42) -> Image.Image:
    """
    Schiarita dolce e sfumata della zona testo (stessa tecnica DODGE delle
    pagine storia): garantisce leggibilità anche se la tavola ha macchie,
    senza box né bordi netti.
    """
    mask = Image.new("L", canvas.size, 0)
    md = ImageDraw.Draw(mask)
    md.rectangle(list(box), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(int(canvas.width * 0.025)))
    paper = Image.new("RGB", canvas.size, DS.PAPER)
    lightened = Image.blend(canvas, paper, strength)
    return Image.composite(lightened, canvas, mask)


def make_atlante_plate_page(
    title: str,
    text: str,
    plate_path: Path,
    volume: int = 1,
    variante_id: str = "A",
    kind: str = "personaggio",
    binomio: str | None = None,
    layout_warnings: list | None = None,
) -> Image.Image:
    """
    Pagina-atlante a tavola naturalistica full-page.
    La tavola (senza testo) fa da fondo; eyebrow, nome+glifo, trafiletto con
    capolettera e firma vengono disegnati nelle zone della variante assegnata
    (ATLANTE_SPEC.json). Stesso linguaggio tipografico della pagina classica.
    """
    spec = load_atlante_spec()
    var  = spec["varianti"][variante_id]
    Z    = var["zone"]
    vento    = _quartiere_color_for(title)
    slug     = _title_to_slug(title)
    motifs   = DS.MOTIF_MAP.get(slug, DS.DEFAULT_MOTIFS)
    glifo_fn = DS.GLIFO_VENTO.get(VOLUME_CONFIG[volume]["ciclo"], DS.glifo_mulinello)

    def zx(z): return int(Z[z]["x"] * TX_W)
    def zy(z): return int(Z[z]["y"] * TX_H)
    def zw(z): return int((Z[z]["w"] or 0) * TX_W)
    def zh(z): return int((Z[z]["h"] or 0) * TX_H)

    # ── Tavola di fondo: cover-fit + controllo qualità + velo del vento ───
    illus = Image.open(plate_path).convert("RGB")
    ok, quality_desc = check_tavola_quality(plate_path)
    canvas = _cover_fit(illus, TX_W, TX_H)
    if not ok:
        canvas = add_quality_banner(canvas, plate_path, quality_desc)
        log.warning("Tavola sotto spec per '%s': %s", title, quality_desc)
        if layout_warnings is not None:
            layout_warnings.append({
                "entry": f"[TAVOLA SOTTO SPEC] {title}",
                "troncato_dopo": "", "testo_tagliato": "",
                "suggerimento": (
                    f'Sostituire tavola per "{title}" con versione HD '
                    f"(min {ATL_MIN_W}×{ATL_MIN_H}px verticale). "
                    f"File attuale: {plate_path.name} ({quality_desc})"
                ),
            })
    canvas = Image.blend(canvas, Image.new("RGB", (TX_W, TX_H), vento), 0.03)

    # ── Zone quiete sotto i blocchi di testo ──────────────────────────────
    fs     = int(var["fs_corpo"])
    LH     = int(fs * 1.55)
    head_box = (zx("eyebrow") - int(TX_W*0.02), zy("eyebrow") - int(TX_H*0.012),
                zx("nome") + zw("nome") + int(TX_W*0.10),
                zy("nome") + int(TX_W*0.066) + int(TX_H*0.022))
    corpo_box = (zx("corpo") - int(TX_W*0.02), zy("corpo") - int(TX_H*0.012),
                 zx("corpo") + zw("corpo") + int(TX_W*0.02),
                 zy("corpo") + zh("corpo") + int(TX_H*0.012))
    canvas = _quiet_zone(canvas, head_box)
    canvas = _quiet_zone(canvas, corpo_box)
    draw = ImageDraw.Draw(canvas)

    # ── Eyebrow ───────────────────────────────────────────────────────────
    f_eye = DS.font_weighted("sans", int(FS_SMALL*0.82), 700)
    eyebrow = "UN ABITANTE DELL'ISOLA" if kind == "personaggio" else "UN LUOGO DELL'ISOLA"
    ex, ey = zx("eyebrow"), zy("eyebrow")
    for ch in eyebrow:
        draw.text((ex, ey), ch, font=f_eye, fill=vento)
        ex += draw.textlength(ch, font=f_eye) + 4

    # ── Nome + glifo-vento (+ binomio se canonizzato) ─────────────────────
    nx, ny = zx("nome"), zy("nome")
    f_name = DS.font_weighted("display", int(TX_W*0.066), 450)
    draw.text((nx, ny), title, font=f_name, fill=DS.INK)
    name_w = draw.textlength(title, font=f_name)
    glifo_fn(draw, int(nx + name_w + TX_W*0.040), int(ny + TX_W*0.030),
             int(TX_W*0.018), vento, max(2, TX_W//500))
    if binomio:
        f_bin = fnt(int(fs*0.82), italic=True)
        draw.text((nx + int(TX_W*0.004), ny + int(TX_W*0.074)),
                  binomio, font=f_bin, fill=DS.tint_color(DS.INK, 0.25))

    # ── Corpo con capolettera nel colore-vento ────────────────────────────
    cx, cy, cw, chh = zx("corpo"), zy("corpo"), zw("corpo"), zh("corpo")
    f_body = fnt(fs)
    f_drop = DS.font_weighted("display", int(fs*2.05), 500)
    first, rest = text[0], text[1:]
    # Allinea la cima della lettera alla cima della prima riga (bbox-aware:
    # i font display hanno spesso un offset interno verso il basso).
    d_box = draw.textbbox((0, 0), first, font=f_drop)
    drop_h = d_box[3] - d_box[1]
    draw.text((cx, cy - d_box[1]), first, font=f_drop, fill=vento)
    indent = int((d_box[2] - d_box[0]) + TX_W*0.012)
    # Quante righe di corpo "abbraccia" il capolettera: solo quelle rientrano.
    drop_lines = max(2, -(-drop_h // LH))   # ceil

    words = rest.strip().split()
    lines: list[tuple[str, int, int]] = []
    yy, line_no, i = cy, 0, 0
    max_y = cy + chh
    while i < len(words) and yy + LH <= max_y:
        xoff = indent if line_no < drop_lines else 0
        w_av = cw - xoff
        cur = ""
        while i < len(words):
            t = (cur + " " + words[i]).strip()
            if draw.textlength(t, font=f_body) <= w_av:
                cur = t; i += 1
            else:
                break
        if not cur:
            cur = words[i]; i += 1
        lines.append((cur, cx + xoff, yy)); yy += LH; line_no += 1

    if i < len(words) and layout_warnings is not None:
        remainder = " ".join(words[i:]).strip()
        if remainder:
            layout_warnings.append({
                "entry": title,
                "troncato_dopo": (lines[-1][0][-60:] if lines else ""),
                "testo_tagliato": remainder,
                "suggerimento": (
                    f'Variante {variante_id} stretta per "{title}": accorciare il '
                    f"trafiletto di ~{len(remainder.split())} parole in "
                    f"presentazioni_parziali.md o cambiare variante in ATLANTE_SPEC.json"
                ),
            })

    for ln, x_at, ly in lines:
        draw.text((x_at, ly), ln, font=f_body, fill=DS.INK)

    # ── Firma: oggetto + glifo + separatore camuno ────────────────────────
    fy = zy("firma")
    obj_motif = motifs[-1] if motifs else None
    if obj_motif:
        obj_motif(draw, int(TX_W*0.42), fy, int(TX_W*0.026), vento)
    glifo_fn(draw, int(TX_W*0.58), fy, int(TX_W*0.020), vento, max(2, TX_W//500))
    DS.separatore_camuno(draw, TX_W//2 - int(TX_W*0.14), TX_W//2 + int(TX_W*0.14),
                         fy + int(TX_H*0.030), DS.tint_color(vento, 0.35),
                         max(2, TX_W//560))

    return canvas

# ═══════════════════════════════════════════════════════════════════════════
# RENDERING — PAGINA STORIA (illustrata)
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# FRASI-ORACOLO — evidenziazione parole-chiave inline (stile "isola")
# ═══════════════════════════════════════════════════════════════════════════
# Le parole-chiave delle frasi-oracolo si marcano nel testo con *asterischi*:
#   «Le cose della *Foresta* hanno il loro *orario*.»
# Restano INLINE (nessuna riga aggiunta, nessuno spazio rubato all'immagine):
# il testo normale è in Lora, le parole-chiave in Fredoka leggermente più
# grande e nel colore-vento del ciclo. Il marker non appare mai nel libro.

_ORACOLO_RE = re.compile(r"\*([^*\n]+)\*")


def _font_oracolo(base_fs: int) -> ImageFont.FreeTypeFont:
    """Fredoka per le parole-chiave (tondo, giocoso), un filo più grande."""
    if DS.F_MARK and DS.F_MARK.exists():
        return ImageFont.truetype(str(DS.F_MARK), int(base_fs * 1.10))
    return fnt(int(base_fs * 1.10))


def _parse_rich(text: str) -> list[tuple[str, bool]]:
    """Spezza una stringa in segmenti (testo, is_keyword) sui marker *...*."""
    segs: list[tuple[str, bool]] = []
    pos = 0
    for m in _ORACOLO_RE.finditer(text):
        if m.start() > pos:
            segs.append((text[pos:m.start()], False))
        segs.append((m.group(1), True))
        pos = m.end()
    if pos < len(text):
        segs.append((text[pos:], False))
    return segs


def has_oracolo(text: str) -> bool:
    return bool(_ORACOLO_RE.search(text))


def strip_oracolo(text: str) -> str:
    """Rimuove i marker *...* lasciando le parole (per misure di lunghezza)."""
    return _ORACOLO_RE.sub(r"\1", text)


def rich_word_wrap(text: str, f_body: ImageFont.FreeTypeFont,
                   f_key: ImageFont.FreeTypeFont, max_w: int,
                   draw: ImageDraw.ImageDraw) -> list[list[tuple[str, bool, bool]]]:
    """
    Word-wrap che conosce le parole-chiave: ritorna righe, ogni riga è una
    lista di token (parola, is_keyword, attaccato_al_precedente). La larghezza
    di ogni token usa il font giusto; 'attaccato' evita lo spazio spurio tra
    una keyword e la punteggiatura che la segue (es. «...orario.»).
    """
    def tok_w(word: str, key: bool) -> float:
        return draw.textlength(word, font=(f_key if key else f_body))
    space_w = draw.textlength(" ", font=f_body)

    rows: list[list[tuple[str, bool, bool]]] = []
    for para in text.split("\n"):
        if not para.strip():
            rows.append([])
            continue
        # Costruisco token (parola, key, glued): glued=True → niente spazio prima.
        toks: list[tuple[str, bool, bool]] = []
        segs = _parse_rich(para)
        for si, (seg, key) in enumerate(segs):
            parts = seg.split(" ")
            for pi, w in enumerate(parts):
                if w == "":
                    continue
                # glued se: è il primo pezzo di un segmento che NON inizia con
                # spazio e segue un altro segmento senza spazio intermedio.
                glued = False
                if pi == 0 and toks:
                    # il segmento precedente finiva senza spazio e questo non
                    # inizia con spazio → attaccato (es. keyword + ".")
                    prev_seg = segs[si-1][0] if si > 0 else ""
                    if not prev_seg.endswith(" ") and not seg.startswith(" "):
                        glued = True
                toks.append((w, key, glued))

        cur: list[tuple[str, bool, bool]] = []
        cur_w = 0.0
        for word, key, glued in toks:
            ww = tok_w(word, key)
            add = ww if (not cur or glued) else space_w + ww
            if cur and not glued and cur_w + add > max_w:
                rows.append(cur)
                cur = [(word, key, False)]; cur_w = ww
            else:
                cur.append((word, key, glued)); cur_w += add
        if cur:
            rows.append(cur)
    return rows


def draw_rich_row(draw: ImageDraw.ImageDraw, x: int, y: int,
                  row: list[tuple[str, bool, bool]],
                  f_body: ImageFont.FreeTypeFont,
                  f_key: ImageFont.FreeTypeFont,
                  ink, key_color) -> None:
    """Disegna una riga di token, parole-chiave in Fredoka+colore-vento.
    Le keyword sono allineate per baseline col corpo (Fredoka è più alto).
    Il flag 'glued' sopprime lo spazio prima del token (punteggiatura)."""
    space_w = draw.textlength(" ", font=f_body)
    body_asc = f_body.getmetrics()[0]
    key_asc  = f_key.getmetrics()[0]
    dy = body_asc - key_asc
    cx = x
    first = True
    for word, key, glued in row:
        if not first and not glued:
            cx += space_w
        first = False
        if key:
            draw.text((cx, y + dy), word, font=f_key, fill=key_color)
            cx += draw.textlength(word, font=f_key)
        else:
            draw.text((cx, y), word, font=f_body, fill=ink)
            cx += draw.textlength(word, font=f_body)


def _scegli_fascia_v2(img: "Image.Image", block_h: int):
    """
    Scelta fascia testo migliorata (alto/basso, mai blocchi flottanti).
    Rispetto alla v1 (solo media di luminosità/movimento), questa:
      - divide ciascuna fascia candidata in strisce sottili e misura il
        dettaglio per striscia, così una piccola zona molto dettagliata
        (es. i volti dei personaggi) non viene "diluita" dalla media;
      - penalizza la fascia il cui PICCO di dettaglio è alto (probabile
        soggetto/volto sotto il testo), non solo la media;
      - sceglie la fascia col soggetto meno invaso; a parità, preferisce
        l'alto (posizione di default, prevedibile in lettura).
    Ritorna (zone, y0z, bright, move) compatibile con la v1.
    """
    H = img.height
    def metriche(y0, y1):
        y0 = max(0, y0); y1 = min(H, y1)
        z = img.crop((0, y0, img.width, y1)).convert("L")
        bright = ImageStat.Stat(z).mean[0] / 255.0
        edges  = z.filter(ImageFilter.FIND_EDGES)
        move_mean = ImageStat.Stat(edges).mean[0] / 255.0
        # picco di dettaglio: striscia orizzontale più "movimentata"
        n = 8
        sh = max(1, (y1 - y0) // n)
        peak = 0.0
        for k in range(n):
            s = edges.crop((0, k*sh, img.width, min((k+1)*sh, y1-y0)))
            if s.height <= 0: continue
            peak = max(peak, ImageStat.Stat(s).mean[0] / 255.0)
        return bright, move_mean, peak

    bt, mt, pt = metriche(0, block_h)
    bb, mb, pb = metriche(H - block_h, H)
    # costo della fascia: il PICCO conta doppio (è lì che stanno i volti),
    # più una penalità se è scura (testo meno leggibile anche dopo dodge).
    def costo(bright, move, peak):
        return peak * 2.0 + move + max(0.0, 0.45 - bright) * 0.5
    c_top, c_bot = costo(bt, mt, pt), costo(bb, mb, pb)
    # preferenza all'alto: il basso vince solo se è chiaramente migliore
    if c_bot < c_top - 0.05:
        return "bottom", H - block_h, bb, mb
    return "top", 0, bt, mt


def _overlay_text(img: Image.Image, text: str, key_color=None,
                  force_zone=None) -> Image.Image:
    """
    Sovrappone il testo storia su una pagina già pronta IMG_W×IMG_H.
    Stessa logica adattiva (fascia alto/basso + schiarita DODGE) usata dalle
    pagine singole: estratta qui per essere riusata dagli spread orizzontali
    (testo solo sulla pagina sinistra). Non tocca mai il file sorgente.
    Ritorna RGB.
    """
    FS  = 50
    LH  = int(FS * 1.62)
    PGS = int(FS * 0.62)
    MX2 = 136
    MT  = 100

    img = img.convert("RGB")
    if not text.strip():
        return img

    f      = fnt(FS)
    f_key  = _font_oracolo(FS)
    kc     = key_color or DS.DEFAULT_QUARTIERE_COLOR
    d0     = ImageDraw.Draw(img)
    rows   = rich_word_wrap(text, f, f_key, IMG_W - 2*MX2, d0)
    n_lines = len([r for r in rows if r])
    block_h = n_lines * LH + MT + int(FS * 0.8)

    def zone_metrics(y0, y1):
        z = img.crop((0, max(0,y0), IMG_W, min(IMG_H,y1))).convert("L")
        brightness = ImageStat.Stat(z).mean[0] / 255.0
        movement = ImageStat.Stat(z.filter(ImageFilter.FIND_EDGES)).mean[0] / 255.0
        return brightness, movement

    top_zone    = (0, block_h)
    bottom_zone = (IMG_H - block_h, IMG_H)
    b_top, m_top = zone_metrics(*top_zone)
    b_bot, m_bot = zone_metrics(*bottom_zone)

    if force_zone == "bottom":
        zone = "bottom"; y0z = IMG_H - block_h; bright, move = b_bot, m_bot
    elif force_zone == "top":
        zone = "top"; y0z = 0; bright, move = b_top, m_top
    elif os.environ.get("TESTO_V2") == "1":
        zone, y0z, bright, move = _scegli_fascia_v2(img, block_h)
    else:
        if m_top > 0.16 and m_bot < m_top - 0.04:
            zone = "bottom"; y0z = IMG_H - block_h
            bright, move = b_bot, m_bot
        else:
            zone = "top"; y0z = 0
            bright, move = b_top, m_top

    # ── SCRIM ADATTIVO LOCALE ────────────────────────────────────────────
    # Sostituisce il vecchio on/off INSIDE/DODGE (forza fissa su banda
    # rettangolare). Misura il fondo SOLO dove cadono i glifi e schiarisce
    # con una sagoma morbida che segue il testo:
    #   - fondo già chiaro e calmo  → scrim ~0 (pagina invariata);
    #   - fondo scuro/movimentato   → schiarita progressiva, ben sfumata;
    #   - macchie scure residue sotto il testo → recupero locale mirato.
    paper  = Image.new("RGB", (IMG_W, IMG_H), DS.PAPER)
    y_text = MT if zone == "top" else (y0z + MT)

    # 1) maschera-sagoma: i glifi in bianco su L (corpo + parole-chiave)
    tmask = Image.new("L", (IMG_W, IMG_H), 0)
    td    = ImageDraw.Draw(tmask)
    yy    = y_text
    for row in rows:
        if not row:
            yy += PGS; continue
        draw_rich_row(td, MX2, yy, row, f, f_key, 255, 255)
        yy += LH

    bbox = tmask.getbbox()
    if bbox is not None:
        bx0, by0, bx1, by1 = bbox
        pad = int(FS * 0.6)
        crop = (max(0, bx0 - pad), max(0, by0 - pad),
                min(IMG_W, bx1 + pad), min(IMG_H, by1 + pad))
        foot = img.crop(crop).convert("L")

        # 2) metriche LOCALI sotto i glifi (non la media dell'intera banda)
        bg   = ImageStat.Stat(foot).mean[0] / 255.0
        busy = ImageStat.Stat(foot.filter(ImageFilter.FIND_EDGES)).mean[0] / 255.0
        floor255  = int(STORY_READ_FLOOR * 255)
        hist = foot.histogram()
        tot  = sum(hist) or 1
        dark_frac = sum(hist[:floor255]) / tot

        # 3) forza base continua (0 dove è già leggibile, su dove serve)
        base = 0.0
        if bg < 0.72:
            base += (0.72 - bg) * 1.15
        base += busy * 0.85
        base += dark_frac * 0.40
        base = max(0.0, min(0.82, base))

        # 4) scrim dalla sagoma: fonde le righe + alone morbido ("sfumare")
        scrim = tmask.filter(ImageFilter.GaussianBlur(int(LH * 0.95)))
        scrim = scrim.point(lambda v: 255 if v > 38 else int(v * 255 / 38))
        scrim = scrim.filter(ImageFilter.GaussianBlur(int(IMG_W * 0.022)))

        # 5) schiarita base verso la carta, modulata da base e mascherata sul testo
        if base > 0.02:
            base_mask = scrim.point(lambda v, b=base: int(v * b))
            img = Image.composite(paper, img, base_mask)

        # 6) recupero locale: dove resta sotto la soglia, schiarisci di più
        #    ("schiarire sfondo sotto testo") — solo entro la sagoma del testo
        lum     = img.convert("L")
        deficit = lum.point(lambda v: max(0, min(255, int((floor255 - v) * 1.7))))
        deficit = ImageChops.multiply(deficit, scrim)
        deficit = deficit.filter(ImageFilter.GaussianBlur(int(IMG_W * 0.015)))
        img = Image.composite(paper, img, deficit)

    # 7) disegna il testo
    draw = ImageDraw.Draw(img)
    y = y_text
    for row in rows:
        if not row:
            y += PGS; continue
        draw_rich_row(draw, MX2, y, row, f, f_key, STORY_INK, kc)
        y += LH
    return img


def compose_story_page(img_path: Path | None, text: str,
                       key_color=None, force_zone=None) -> Image.Image:
    """
    Compone una pagina storia:
    - Se esiste la HD (_hd/), la carica direttamente (già ≥1664×2496)
    - Se esiste solo il low-res, fa upscale 2× con Lanczos
    - Se manca, crea un placeholder avorio con il nome file
    Sovrappone il testo con halo leggero per leggibilità.
    """
    FS  = 50            # font size sul canvas a 300 DPI
    LH  = int(FS * 1.62)
    PGS = int(FS * 0.62)
    MX2 = 136
    MT  = 100

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
            f      = fnt(FS)
            f_key  = _font_oracolo(FS)
            kc     = key_color or DS.DEFAULT_QUARTIERE_COLOR
            rows   = rich_word_wrap(text, f, f_key, IMG_W - 2*MX2, draw)
            y      = MT
            for row in rows:
                if not row: y += PGS; continue
                draw_rich_row(draw, MX2, y, row, f, f_key, STORY_INK, kc)
                y += LH
        return img

    # Carica e controlla qualità
    try:
        img = Image.open(resolved).convert("RGBA")
    except (FileNotFoundError, OSError, IOError) as exc:
        log.error("Impossibile aprire '%s': %s", resolved, exc)
        img = Image.new("RGBA", (IMG_W, IMG_H), (245, 241, 233))

    # Controllo qualità: le scene devono essere HD (≥ trim+bleed)
    ok, quality_desc = check_image_quality(resolved)

    # Normalizza a IMG_W×IMG_H (trim + bleed, 300 DPI)
    if img.size != (IMG_W, IMG_H):
        img = img.resize((IMG_W, IMG_H), Image.LANCZOS)
    img = img.convert("RGB")

    # ── Testo ADATTIVO: dentro l'illustrazione, con schiarita dolce ───────
    # Ancora: alto (default). Se la fascia alta è occupata da un soggetto
    # importante o troppo scura, l'helper sposta in basso e/o schiarisce.
    img = _overlay_text(img, text, key_color=key_color, force_zone=force_zone)

    # Applica banner qualità sulle storie sotto spec
    if not ok:
        img_rgb = add_quality_banner(img.convert("RGB"), resolved, quality_desc)
        log.warning("Immagine storia sotto spec: %s (%s)", resolved.name, quality_desc)
        return img_rgb

    return img.convert("RGB")


def _split_text_balanced(text: str) -> tuple[str, str]:
    """Divide il testo in due parti ~uguali per uno spread con testo su
    entrambe le pagine, scegliendo il confine MIGLIORE: preferisce un confine
    di PARAGRAFO (riga vuota), altrimenti di FRASE, più vicino al punto di metà.
    Ritorna (sinistra, destra). Se non c'è un confine sensato → (testo, "")."""
    text = (text or "").strip()
    if not text:
        return "", ""
    target = len(text) / 2.0
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(paras) >= 2:
        blocks, joiner = paras, "\n\n"
    else:
        blocks = [b.strip() for b in
                  re.findall(r'.*?[.!?…]+[»"”\')\]]?(?:\s+|$)', text, flags=re.S)
                  if b.strip()]
        joiner = " "
    if len(blocks) < 2:
        return text, ""
    best_k, best_d, cum = 1, None, 0
    for k in range(1, len(blocks)):
        cum += len(blocks[k - 1]) + len(joiner)
        d = abs(cum - target)
        if best_d is None or d < best_d:
            best_d, best_k = d, k
    return joiner.join(blocks[:best_k]).strip(), joiner.join(blocks[best_k:]).strip()


def compose_spread_horizontal(landscape_path: Path | None, text: str,
                              key_color=None, spread_text: str = "left"
                              ) -> tuple[str, Image.Image]:
    """
    Compone uno spread orizzontale doppia-pagina da UNA sola immagine
    landscape che attraversa le due facciate.

      - cover-fit dell'immagine su un canvas CONTINUO (IMG_W*2 + gutter)×IMG_H:
        nessuna banda inserita al centro, la continuità è reale e lo split
        a metà (fatto da build_stampa_pdf) cade naturalmente sulla piega,
        come in ogni spread fisico;
      - il testo è sovrapposto SOLO sulla pagina sinistra (zona quieta del
        paesaggio), riusando _overlay_text (stessa logica delle pagine singole);
      - se l'immagine non basta a servire 2 facciate full-bleed HD, applica
        il banner arancione "sotto spec" per la verifica visiva (non blocca).

    Ritorna ('spread', canvas). A valle:
      - build_spread_pdf  → la rende come doppia pagina continua (digitale)
      - build_stampa_pdf  → la taglia a metà in 2 pagine A5 indipendenti (KDP)
    """
    SW = IMG_W * 2 + SCALE * 4   # stessa larghezza usata altrove per gli spread

    resolved = None
    if landscape_path and landscape_path.exists():
        resolved = resolve_scene_image(landscape_path)

    # ── Placeholder se manca l'immagine ──────────────────────────────────
    if resolved is None or not resolved.exists():
        if resolved:
            log.warning("Spread landscape non trovato: %s", resolved)
        canvas = Image.new("RGB", (SW, IMG_H), (245, 241, 233))
        d = ImageDraw.Draw(canvas)
        label = landscape_path.name if landscape_path else "spread in lavorazione"
        d.text((136, IMG_H - 100), f"[{label}]", font=fnt(36), fill=(180, 162, 138))
        left = _overlay_text(canvas.crop((0, 0, IMG_W, IMG_H)), text, key_color)
        canvas.paste(left, (0, 0))
        return ("spread", canvas)

    # ── Carica + cover-fit sul canvas continuo ───────────────────────────
    try:
        src = Image.open(resolved).convert("RGB")
    except (OSError, IOError) as exc:
        log.error("Spread non apribile '%s': %s", resolved, exc)
        src = Image.new("RGB", (SW, IMG_H), (245, 241, 233))
    canvas = _cover_fit(src, SW, IMG_H)

    # ── Testo: solo a sinistra (default) oppure SPLIT sulle due pagine ────
    if spread_text == "split":
        left_txt, right_txt = _split_text_balanced(text)
        left = _overlay_text(canvas.crop((0, 0, IMG_W, IMG_H)),
                             left_txt, key_color=key_color)
        canvas.paste(left, (0, 0))
        if right_txt:
            rx0 = SW - IMG_W   # pagina destra (oltre la piega)
            right = _overlay_text(canvas.crop((rx0, 0, SW, IMG_H)),
                                  right_txt, key_color=key_color)
            canvas.paste(right, (rx0, 0))
    else:
        left = _overlay_text(canvas.crop((0, 0, IMG_W, IMG_H)),
                             text, key_color=key_color)
        canvas.paste(left, (0, 0))

    # ── Banner qualità: lo spread serve 2 facciate full-bleed ────────────
    sw, sh = src.size
    if sw < 2 * PRES_MIN_W or sh < PRES_MIN_H:
        desc = (f"{sw}×{sh}px — spread sotto spec "
                f"(≥{2*PRES_MIN_W}×{PRES_MIN_H} per 2 facciate HD)")
        canvas = add_quality_banner(canvas, resolved, desc)
        log.warning("Spread sotto spec: %s (%s)", resolved.name, desc)

    return ("spread", canvas)

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
        r"\s*@page_book\s+(\[[^\]]*\]|\S+)\s*"
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
    """Dedica: corsivo Fraunces centrato, ornamento a puntini."""
    img  = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    draw = ImageDraw.Draw(img)
    f    = DS.font("display_i", int(TX_W * 0.031))
    lh   = int(TX_W * 0.05)
    y    = int(TX_H * 0.40)
    for line in text.split("\n"):
        w = draw.textlength(line, font=f)
        draw.text((TX_W/2 - w/2, y), line, font=f, fill=DS.INK_SOFT)
        y += lh
    DS.draw_dot_ornament(draw, TX_W//2, y + int(TX_W*0.03), DS.RULE,
                         spread=int(TX_W*0.025))
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


def _facciate(pages: list) -> int:
    """Conta le facciate reali: uno spread occupa 2 facciate, un single 1."""
    return sum(2 if k == "spread" else 1 for k, _ in pages)


def ensure_recto(pages: list) -> list:
    """Aggiunge una bianca se necessario perché la prossima pagina cada su recto.
    Conta gli spread come 2 facciate (altrimenti la parità si sfasa)."""
    if _facciate(pages) % 2 == 1:
        return pages + [("single", make_blank())]
    return pages


# ═══════════════════════════════════════════════════════════════════════════
# FRONT MATTER EDITORIALE — frontespizio, colophon, indice
# ═══════════════════════════════════════════════════════════════════════════
VOLUME_NOMI = {1: "VOLUME PRIMO", 2: "VOLUME SECONDO",
               3: "VOLUME TERZO", 4: "VOLUME QUARTO"}
CICLO_SOTTOTITOLO = {
    "Δ": "Il vento che taglia",
    "⇄": "Il vento che intreccia",
    "⟳": "Il vento che fa girare",
    "Integrazione": "I tre venti insieme",
}


def _center(draw, text, font, y, color, w=TX_W):
    tw = draw.textlength(text, font=font)
    draw.text((w/2 - tw/2, y), text, font=font, fill=color)


def _tracked_center(draw, text, font, y, color, tracking, w=TX_W):
    total = sum(draw.textlength(c, font=font) + tracking for c in text) - tracking
    x = w/2 - total/2
    for c in text:
        draw.text((x, y), c, font=font, fill=color)
        x += draw.textlength(c, font=font) + tracking


def make_occhiello_copertina() -> Image.Image:
    """Occhiello illustrato: la copertina riproposta come pagina interna a
    piena pagina (half-title illustrato), prima del frontespizio. Riempie la
    larghezza; il minimo eccesso verticale è centrato (scena piena, nessuna
    perdita significativa). Se manca l'immagine, ritorna carta vuota."""
    img = Image.new("RGB", (IMG_W, IMG_H), DS.PAPER)
    # La copertina VERA (illustrazione personaggi) SENZA testo, in HD: pagina
    # interna che "replica la copertina" come soglia. Niente scritte (il testo
    # della cover lo disegna build_cover.py, non sta nell'immagine pulita).
    cov_p = _occhiello_cover_path()
    if cov_p is not None:
        cov = Image.open(cov_p).convert("RGB")
        sw, sh = cov.size
        scale = IMG_W / sw
        nw, nh = IMG_W, int(round(sh * scale))
        cov_fit = cov.resize((nw, nh), Image.LANCZOS)
        oy = (IMG_H - nh) // 2          # centra l'eccesso verticale
        # Velo verso la carta: la copertina-occhiello non parte a colori pieni
        # ma più chiara/attenuata, così legge come "intro" / soglia interna.
        paper = Image.new("RGB", cov_fit.size, DS.PAPER)
        cov_fit = Image.blend(cov_fit, paper, 0.25)
        img.paste(cov_fit, (0, oy))
        # Vignettatura morbida: i bordi sfumano nella carta (cornice-soglia).
        import numpy as np
        paper_full = Image.new("RGB", (IMG_W, IMG_H), DS.PAPER)
        yy, xx = np.mgrid[0:IMG_H, 0:IMG_W]
        dx = np.abs(xx - IMG_W/2) / (IMG_W/2)
        dy = np.abs(yy - IMG_H/2) / (IMG_H/2)
        edge = np.maximum(dx, dy)                 # 0 centro, 1 bordi
        vmask = (np.clip((edge - 0.74) / 0.26, 0, 1) ** 1.6 * 160).astype("uint8")
        img = Image.composite(paper_full, img, Image.fromarray(vmask, "L"))
    return img


def make_frontespizio(volume: int) -> Image.Image:
    """Frontespizio: titolo + rosone dei tre venti (emblema) + volume + editore.
    L'emblema (foglia/onda/piuma nel cerchio) dà peso visivo senza ripetere la
    copertina; è il linguaggio dei tre venti in forma decorativa, non esplicita.
    """
    cfg = VOLUME_CONFIG[volume]
    img = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    d = ImageDraw.Draw(img)
    vento = DS.CICLO_COLOR.get(cfg["ciclo"], DS.ACCENT)

    # Titolo in alto
    f_title = DS.font("mark", int(TX_W*0.066))
    _center(d, "L'Isola", f_title, int(TX_H*0.085), DS.INK)
    _center(d, "dei Tre Venti", f_title, int(TX_H*0.142), DS.INK)

    # Emblema centrale: il rosone dei tre venti (terra/acqua/aria + spirale)
    rosone_p = REPO / "visual/atlante/emblema/rosone_tre_venti.png"
    if rosone_p.exists():
        ros = Image.open(rosone_p).convert("RGBA")
        target = int(TX_W * 0.52)
        rr = ros.resize((target, int(target * ros.height / ros.width)), Image.LANCZOS)
        rx = TX_W//2 - rr.width//2
        ry = int(TX_H*0.30)
        img.paste(rr, (rx, ry), rr)
    else:
        logo = DS.make_logo_image(int(TX_W*0.13), DS.SPIRALE)
        img.paste(logo, (TX_W//2 - logo.width//2, int(TX_H*0.32)), logo)

    # Volume + sottotitolo-ciclo sotto l'emblema
    DS.draw_wind_rule(d, TX_W//2 - int(TX_W*0.14), TX_W//2 + int(TX_W*0.14),
                      int(TX_H*0.70), DS.RULE, max(2, TX_W//560))
    f_vol = DS.font_weighted("sans", int(TX_W*0.025), 700)
    _tracked_center(d, VOLUME_NOMI[volume], f_vol, int(TX_H*0.725), DS.SPIRALE, 5)
    f_sub = DS.font("display_i", int(TX_W*0.032))
    _center(d, CICLO_SOTTOTITOLO.get(cfg["ciclo"], ""), f_sub, int(TX_H*0.765), DS.INK_SOFT)

    # Autore + editore in basso
    f_auth = DS.font("sans", int(TX_W*0.024))
    _center(d, AUTHOR_BYLINE, f_auth, int(TX_H*0.88), DS.INK)
    f_ed = DS.font_weighted("sans", int(TX_W*0.019), 600)
    _tracked_center(d, "SPIRALE EDITRICE", f_ed, int(TX_H*0.91), DS.INK_FAINT, 4)
    return img


def make_colophon(volume: int) -> Image.Image:
    """Colophon: copyright, dati edizione, disclaimer AI, lockup."""
    cfg = VOLUME_CONFIG[volume]
    img = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    d = ImageDraw.Draw(img)
    MXc = int(TX_W * 0.10)
    y = int(TX_H * 0.12)

    d.text((MXc, y), f"© 2026 {AUTHOR_BYLINE.upper()}",
           font=DS.font_weighted("sans", int(TX_W*0.023), 800), fill=DS.INK)
    y += int(TX_H * 0.045)

    f  = DS.font("serif", int(TX_W*0.021))
    fi = DS.font("serif_i", int(TX_W*0.021))
    LH = int(TX_W * 0.036)

    def wrap_c(text, font, maxw):
        out=[]; cur=""
        for word in text.split():
            t=(cur+" "+word).strip()
            if d.textlength(t, font=font) <= maxw: cur=t
            else: out.append(cur); cur=word
        if cur: out.append(cur)
        return out

    sub = f"L'Isola dei Tre Venti — {VOLUME_NOMI[volume].title()}: {CICLO_SOTTOTITOLO.get(cfg['ciclo'],'')}"
    d.text((MXc, y), sub, font=fi, fill=DS.INK_SOFT); y += int(LH*1.5)

    blocks = [
        "Prima edizione, 2026. Pubblicato da Spirale Editrice.",
        "",
        "ISBN paperback: [da inserire dopo registrazione su KDP]",
        "ISBN eBook: [da inserire dopo registrazione su KDP]",
        "",
    ]
    for b in blocks:
        if b: d.text((MXc, y), b, font=f, fill=DS.INK_SOFT)
        y += LH

    paras = [
        ("Tutti i diritti riservati. Nessuna parte di questo libro può essere "
         "riprodotta o trasmessa in qualsiasi forma senza il permesso scritto "
         "dell'autore, eccetto per brevi citazioni in recensioni critiche."),
        ("Questo libro è stato prodotto con l'assistenza di sistemi di intelligenza "
         "artificiale, sotto la direzione e responsabilità editoriale dell'autore. "
         "Ogni scelta narrativa è frutto di pensiero umano."),
        ("I marchi e i nomi citati appartengono ai rispettivi proprietari e sono "
         "usati a scopo descrittivo."),
    ]
    for p in paras:
        y += int(LH*0.4)
        for ln in wrap_c(p, f, TX_W - 2*MXc):
            d.text((MXc, y), ln, font=f, fill=DS.INK_SOFT); y += LH

    logo = DS.make_logo_image(int(TX_W*0.06), DS.INK_FAINT)
    ly = TX_H - int(TX_H*0.12)
    img.paste(logo, (MXc, ly), logo)
    d.text((MXc + logo.width + 14, ly + logo.height//3),
           "SPIRALE EDITRICE",
           font=DS.font_weighted("sans", int(TX_W*0.018), 700), fill=DS.INK_FAINT)
    return img


def make_indice(volume: int, voci: list[tuple]) -> Image.Image:
    """
    Indice completo: storie E sezioni comuni, nell'ordine reale del libro.
    voci: lista di (numero|None, titolo, sottotitolo|None, tipo) dove
    tipo ∈ {'storia','sezione'}.
    """
    cfg = VOLUME_CONFIG[volume]
    vento = DS.CICLO_COLOR.get(cfg["ciclo"], DS.ACCENT)
    img = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    d = ImageDraw.Draw(img)
    MXi = int(TX_W * 0.10)
    y = int(TX_H * 0.12)

    d.text((MXi, y), "Indice", font=DS.font_weighted("mark", int(TX_W*0.058), 600),
           fill=DS.INK)
    y += int(TX_H * 0.058)
    f_eye = DS.font_weighted("sans", int(TX_W*0.019), 700)
    ex = MXi
    label = f"L'ISOLA DEI TRE VENTI · {VOLUME_NOMI[volume]}"
    for c in label:
        d.text((ex, y), c, font=f_eye, fill=DS.SPIRALE)
        ex += d.textlength(c, font=f_eye) + 2
    y += int(TX_H * 0.055)

    f_num = DS.font_weighted("mark", int(TX_W*0.042), 600)
    f_tit = DS.font_weighted("display", int(TX_W*0.027), 600)
    f_sec = DS.font("display_i", int(TX_W*0.026))
    f_pg  = DS.font("sans", int(TX_W*0.021))

    def leader_and_page(tx, tit_w, y_text, pagenum, baseline_off):
        """Disegna i puntini-guida e il numero di pagina a destra."""
        if pagenum is None:
            return
        pg_s = str(pagenum)
        pg_w = d.textlength(pg_s, font=f_pg)
        dot_start = tx + tit_w + int(TX_W*0.014)
        dot_end   = TX_W - MXi - pg_w - int(TX_W*0.014)
        dx = dot_start
        dy = y_text + baseline_off
        while dx < dot_end:
            d.ellipse([dx, dy, dx+3, dy+3], fill=DS.INK_FAINT)
            dx += int(TX_W*0.011)
        d.text((TX_W - MXi - pg_w, y_text), pg_s, font=f_pg, fill=DS.INK_SOFT)

    for num, titolo, pagenum, tipo in voci:
        if tipo == "storia":
            d.text((MXi, y), str(num), font=f_num, fill=vento)
            tx = MXi + int(TX_W*0.075)
            ty = y + int(TX_W*0.006)
            d.text((tx, ty), titolo, font=f_tit, fill=DS.INK)
            tit_w = d.textlength(titolo, font=f_tit)
            leader_and_page(tx, tit_w, ty, pagenum, int(TX_W*0.016))
            row_h = int(TX_W * 0.060)
        else:
            tx = MXi
            d.text((tx, y), titolo, font=f_sec, fill=DS.INK_SOFT)
            tit_w = d.textlength(titolo, font=f_sec)
            leader_and_page(tx, tit_w, y, pagenum, int(TX_W*0.013))
            row_h = int(TX_W * 0.050)
        y += row_h

    # filetto-vento di chiusura
    DS.draw_wind_rule(d, MXi, TX_W - MXi, TX_H - int(TX_H*0.10), DS.RULE,
                      max(2, TX_W//560))
    return img


def build_indice_voci(volume: int, storie: list[str],
                      posizione_pres: str) -> list[tuple]:
    """Costruisce l'elenco voci dell'indice nell'ordine reale del libro."""
    voci = []
    voci.append((None, "Prima di leggere", None, "sezione"))
    voci.append((None, "L'isola dorme", None, "sezione"))
    if posizione_pres == "prima":
        voci.append((None, "Gli abitanti dell'isola", None, "sezione"))
    for i, sid in enumerate(storie, 1):
        t = get_story_title(sid)
        voci.append((i, t, None, "storia"))
    if posizione_pres == "dopo":
        voci.append((None, "Gli abitanti dell'isola", None, "sezione"))
    voci.append((None, "Le porte", None, "sezione"))
    voci.append((None, "Il sigillo" if volume != 4 else "A te che torni",
                 None, "sezione"))
    return voci


def build_indice_voci_numerate(volume: int, storie: list[str],
                               posizione_pres: str, marks: dict) -> list[tuple]:
    """Come build_indice_voci ma con i numeri di pagina reali dai marks.
    Il numero mostrato è 1-based (pagina fisica del libro)."""
    def pg(key):
        idx = marks.get(key)
        return (idx + 1) if idx is not None else None

    voci = []
    voci.append((None, "Prima di leggere", pg("prima_di_leggere"), "sezione"))
    voci.append((None, "L'isola dorme", pg("isola_dorme"), "sezione"))
    if posizione_pres == "prima":
        voci.append((None, "Gli abitanti dell'isola", pg("abitanti"), "sezione"))
    for i, sid in enumerate(storie, 1):
        voci.append((i, get_story_title(sid), pg(f"storia_{i}"), "storia"))
    if posizione_pres == "dopo":
        voci.append((None, "Gli abitanti dell'isola", pg("abitanti"), "sezione"))
    voci.append((None, "Le porte", pg("porte"), "sezione"))
    if volume == 4:
        voci.append((None, "A te che torni", pg("congedo"), "sezione"))
    else:
        voci.append((None, "Il sigillo", pg("sigillo"), "sezione"))
    return voci


# ═══════════════════════════════════════════════════════════════════════════
# PAGINE-OCCHIELLO — aperture di sezione illustrate
# ═══════════════════════════════════════════════════════════════════════════

def _occhiello_base(eyebrow: str, titolo: str, sottotitolo: str,
                    disegno_fn, vento) -> Image.Image:
    """Schema comune: eyebrow + disegno + titolo + filetto + frasetta-guida."""
    img = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    d = ImageDraw.Draw(img)

    # eyebrow tracciato
    f_eye = DS.font_weighted("sans", int(TX_W*0.020), 700)
    tot = sum(d.textlength(c, font=f_eye) + 5 for c in eyebrow) - 5
    ex = TX_W/2 - tot/2
    for c in eyebrow:
        d.text((ex, int(TX_H*0.14)), c, font=f_eye, fill=DS.SPIRALE)
        ex += d.textlength(c, font=f_eye) + 5

    # disegno centrale
    if disegno_fn:
        disegno_fn(d, TX_W//2, int(TX_H*0.37))

    # titolo (può andare su più righe, centrato)
    f_t = DS.font_weighted("display", int(TX_W*0.058), 600)
    lines = []
    cur = ""
    for w in titolo.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f_t) <= TX_W*0.78: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    y = int(TX_H*0.55)
    for ln in lines:
        tw = d.textlength(ln, font=f_t)
        d.text((TX_W/2 - tw/2, y), ln, font=f_t, fill=DS.INK)
        y += int(TX_W*0.062)

    # filetto-vento
    DS.draw_wind_rule(d, TX_W//2 - int(TX_W*0.13), TX_W//2 + int(TX_W*0.13),
                      y + int(TX_H*0.01), DS.RULE, max(2, TX_W//560))
    y += int(TX_H*0.035)

    # frasetta-guida in corsivo
    if sottotitolo:
        f_s = DS.font("display_i", int(TX_W*0.030))
        for ln in sottotitolo.split("\n"):
            tw = d.textlength(ln, font=f_s)
            d.text((TX_W/2 - tw/2, y), ln, font=f_s, fill=DS.INK_SOFT)
            y += int(TX_W*0.040)
    return img


def make_occhiello_prima_di_leggere() -> Image.Image:
    return _occhiello_base(
        "L'ATLANTE DELL'ISOLA", "Prima di leggere",
        "Tutto quello che serve sapere\nprima di salpare per l'isola.",
        lambda d, cx, cy: DS.isola_stilizzata(d, cx, cy, int(TX_W*0.22), DS.INK_SOFT),
        DS.ACCENT)


def make_occhiello_abitanti() -> Image.Image:
    return _occhiello_base(
        "LA GALLERIA", "Gli abitanti dell'isola",
        "Chi incontrerai, e dove vive.",
        lambda d, cx, cy: DS.rosa_tre_venti(d, cx, cy, int(TX_W*0.13), max(3, TX_W//280)),
        DS.SPIRALE)


def make_occhiello_porte(volume: int) -> Image.Image:
    vento = DS.CICLO_COLOR.get(VOLUME_CONFIG[volume]["ciclo"], DS.ACCENT)
    return _occhiello_base(
        "DOPO LE STORIE", "Le porte",
        "Domande e giochi\nper restare ancora un po' sull'isola.",
        lambda d, cx, cy: DS.camuno_rosa(d, cx, cy, int(TX_W*0.10), vento, max(3, TX_W//300)),
        vento)


def make_occhiello_storia(num: int, titolo: str, volume: int) -> Image.Image:
    """Apertura storia: glifo-vento del ciclo + numero + titolo."""
    cfg = VOLUME_CONFIG[volume]
    vento = DS.CICLO_COLOR.get(cfg["ciclo"], DS.ACCENT)
    glifo_fn = DS.GLIFO_VENTO.get(cfg["ciclo"])
    img = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    d = ImageDraw.Draw(img)

    # glifo-vento del ciclo
    if glifo_fn:
        glifo_fn(d, TX_W//2, int(TX_H*0.34), int(TX_W*0.085), vento, max(4, TX_W//360))

    # eyebrow "STORIA N"
    f_eye = DS.font_weighted("sans", int(TX_W*0.020), 700)
    eb = f"STORIA {num}"
    tot = sum(d.textlength(c, font=f_eye) + 6 for c in eb) - 6
    ex = TX_W/2 - tot/2
    for c in eb:
        d.text((ex, int(TX_H*0.46)), c, font=f_eye, fill=vento)
        ex += d.textlength(c, font=f_eye) + 6

    # titolo
    f_t = DS.font_weighted("display", int(TX_W*0.050), 600)
    lines = []; cur = ""
    for w in titolo.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f_t) <= TX_W*0.80: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    y = int(TX_H*0.50)
    for ln in lines:
        tw = d.textlength(ln, font=f_t)
        d.text((TX_W/2 - tw/2, y), ln, font=f_t, fill=DS.INK)
        y += int(TX_W*0.058)
    DS.draw_wind_rule(d, TX_W//2 - int(TX_W*0.10), TX_W//2 + int(TX_W*0.10),
                      y + int(TX_H*0.008), vento, max(2, TX_W//560))
    return img


# Immagine d'ingresso per la soglia (establishing shot dei tre fratelli)
SOGLIA_IMG = REPO / "pipeline_narrativa/storie_finali/_scene/s01/_hd/s01_h01a_hd.jpg"


def make_soglia_ingresso(titolo_sezione: str = "L'isola dorme") -> Image.Image:
    """
    Pagina-soglia 'Qui entri nell'isola': l'immagine d'ingresso affiora dalla
    carta (nessuno stacco) e introduce la sezione che segue.
    Stacco editoriale tra 'Prima di leggere' e 'L'isola dorme'.
    """
    if SOGLIA_IMG.exists():
        illus = Image.open(SOGLIA_IMG).convert("RGB")
        box = (0, int(TX_H*0.10), TX_W, int(TX_H*0.72))
        img = DS.nasce_dalla_pagina(illus, TX_W, TX_H, box, DS.PAPER,
                                    fade=0.42, edge_softness=0.52, seed=3)
    else:
        img = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    d = ImageDraw.Draw(img)

    f_eye = DS.font_weighted("sans", int(TX_W*0.020), 700)
    eb = "QUI ENTRI NELL'ISOLA"
    tot = sum(d.textlength(c, font=f_eye) + 5 for c in eb) - 5
    ex = TX_W/2 - tot/2
    for c in eb:
        d.text((ex, int(TX_H*0.76)), c, font=f_eye, fill=DS.SPIRALE)
        ex += d.textlength(c, font=f_eye) + 5

    f_t = DS.font_weighted("display", int(TX_W*0.052), 600)
    tw = d.textlength(titolo_sezione, font=f_t)
    d.text((TX_W/2 - tw/2, int(TX_H*0.80)), titolo_sezione, font=f_t, fill=DS.INK)
    DS.draw_wind_rule(d, TX_W//2 - int(TX_W*0.10), TX_W//2 + int(TX_W*0.10),
                      int(TX_H*0.87), DS.RULE, max(2, TX_W//560))
    return img

# ═══════════════════════════════════════════════════════════════════════════
# COSTRUZIONE PAGINE STORIA
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# IL MITO DEI TRE VENTI — bonus illustrato (tempo arcaico, deroga palette)
# ═══════════════════════════════════════════════════════════════════════════

MITO_DIR = REPO / "visual/atlante/mito"
MITO_SCENE = MITO_DIR / "scene"
# Colore "antico" desaturato per il mito (oro spento, non legato a un ciclo)
MITO_INK = (92, 74, 52)


def make_occhiello_mito() -> Image.Image:
    """Frontespizio del mito: eyebrow 'IL MITO DELLE ORIGINI', titolo, riga
    vento. Tono arcaico, sobrio. Apre il bonus."""
    img = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    d = ImageDraw.Draw(img)
    oro = DS.ACCENT

    # rosone dei tre venti, piccolo, in alto (richiamo all'emblema)
    rosone_p = REPO / "visual/atlante/emblema/rosone_tre_venti.png"
    if rosone_p.exists():
        ros = Image.open(rosone_p).convert("RGBA")
        target = int(TX_W * 0.30)
        rr = ros.resize((target, int(target * ros.height / ros.width)), Image.LANCZOS)
        img.paste(rr, (TX_W//2 - rr.width//2, int(TX_H*0.20)), rr)

    f_eye = DS.font_weighted("sans", int(TX_W*0.021), 700)
    eb = "IL MITO DELLE ORIGINI"
    tot = sum(d.textlength(c, font=f_eye) + 5 for c in eb) - 5
    ex = TX_W/2 - tot/2
    for c in eb:
        d.text((ex, int(TX_H*0.48)), c, font=f_eye, fill=oro)
        ex += d.textlength(c, font=f_eye) + 5

    f_t = DS.font("mark", int(TX_W*0.058))
    _center(d, "Il Mito", f_t, int(TX_H*0.52), DS.INK)
    _center(d, "dei Tre Venti", f_t, int(TX_H*0.575), DS.INK)

    DS.draw_wind_rule(d, TX_W//2 - int(TX_W*0.12), TX_W//2 + int(TX_W*0.12),
                      int(TX_H*0.65), DS.RULE, max(2, TX_W//560))

    f_sub = DS.font("display_i", int(TX_W*0.028))
    _center(d, "come lo raccontava Grunto", f_sub, int(TX_H*0.67), DS.INK_SOFT)
    return img


def _parse_mito() -> list[dict]:
    """Legge mito_tre_venti.md, ritorna lista di scene (testo + immagine)."""
    md_p = MITO_DIR / "mito_tre_venti.md"
    if not md_p.exists():
        return []
    md = md_p.read_text(encoding="utf-8")
    pat = re.compile(
        r"<!--\s*@scene\s+(\S+)\s*\|\s*@page\s+(\d+)\s*\|\s*@image\s+([^\s>]+)\s*-->",
        re.IGNORECASE)
    parts = pat.split(md)
    scenes = []
    i = 1
    while i + 3 < len(parts) + 1 and i < len(parts):
        if i + 2 >= len(parts):
            break
        scene_id = parts[i].strip()
        img_name = parts[i+2].strip()
        text = parts[i+3].strip() if i+3 < len(parts) else ""
        scenes.append({
            "scene": scene_id,
            "image_path": MITO_SCENE / img_name,
            "text": text,
        })
        i += 4
    return scenes


def build_mito_pages() -> list[tuple[str, Image.Image]]:
    """Monta il mito completo: occhiello + pagine illustrate. Le immagini hanno
    già la deroga palette (antica/desaturata). Testo con oracoli (parole-chiave
    evidenziate) nel colore oro del mito."""
    pages: list[tuple[str, Image.Image]] = []
    pages.append(("single", make_occhiello_mito()))
    for sc in _parse_mito():
        # La scena tempesta ha il gufo in alto: il testo sta meglio in basso.
        fz = "bottom" if sc["scene"] == "s4_tempesta" else None
        img = compose_story_page(sc["image_path"], sc["text"],
                                 key_color=DS.ACCENT, force_zone=fz)
        pages.append(("single", img))
    return pages


def build_story_pages(sid: str, key_color=None) -> list[tuple[str, Image.Image]]:
    pages: list[tuple[str, Image.Image]] = []
    for sh in parse_story_md(sid):
        layout = sh["layout"]
        is_spread = layout.startswith("double_spread") or isinstance(sh["page_book"], list)
        if is_spread:
            # Spread orizzontale: 1 immagine landscape su 2 facciate.
            # double_spread       → testo solo a sinistra
            # double_spread_split → testo diviso sulle due pagine (punto migliore)
            # build_stampa_pdf taglia poi lo spread in 2 A5.
            spread_text = "split" if layout == "double_spread_split" else "left"
            pages.append(compose_spread_horizontal(
                sh["image_path"], sh["text"], key_color=key_color,
                spread_text=spread_text))
        else:
            img = compose_story_page(sh["image_path"], sh["text"], key_color=key_color)
            pages.append(("single", img))
    return pages

# ═══════════════════════════════════════════════════════════════════════════
# COSTRUZIONE SEQUENZA VOLUME
# ═══════════════════════════════════════════════════════════════════════════

def _mean_lum(path: "Path", sample: int = 128) -> float:
    """Luminanza media (0..1) su un campione ridotto — veloce, per i guard."""
    return ImageStat.Stat(
        Image.open(path).convert("L").resize((sample, sample))).mean[0] / 255.0


def validate_frontmatter_isola(log_warn=True) -> list[str]:
    """Guard PRE-BUILD: verifica che notte/giorno/copertina del front matter non
    siano scambiati. Ritorna la lista dei problemi (vuota = ok). Non blocca il
    build, ma logga un avviso netto. Gli stessi invarianti sono coperti dai test
    (tests/test_frontmatter_images.py) che girano in `make check`."""
    problems: list[str] = []
    notte = FRONTMATTER_ISOLA["stato_zero"]
    giorno = FRONTMATTER_ISOLA["atlante_questa_isola"]
    cover = _occhiello_cover_path()
    if notte.exists() and giorno.exists():
        ln, lg = _mean_lum(notte), _mean_lum(giorno)
        if not (ln < lg - 0.15):
            problems.append(
                f"isola notte/giorno forse SCAMBIATE: 'Ecco l'isola'={notte.name} "
                f"(lum {ln:.2f}) non è più scura di 'Questa è l'isola'="
                f"{giorno.name} (lum {lg:.2f})")
    if cover is not None and ("candidate_v2" in cover.name):
        problems.append(
            f"pagina-2 usa una cover col TITOLO impresso ({cover.name}): serve "
            f"la versione senza testo (notxt/clean)")
    if log_warn:
        for p in problems:
            log.warning("FRONT MATTER: %s", p)
    return problems


def build_volume_pages(
    volume:            int,
    storie_override:   list[str] | None = None,
    solo_storie:       bool = False,
    con_front_matter:  bool = True,
    posizione_pres:    Literal["prima", "dopo"] = "dopo",
    dedica:            str = DEDICA_DEFAULT,
    map_path:          Path | None = None,
    usa_atlante:       bool = True,
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
    if con_front_matter and not solo_storie:
        validate_frontmatter_isola()   # guard: notte/giorno/copertina al posto giusto
    pages: list[tuple[str, Image.Image]] = []
    layout_warnings: list[dict] = []

    image_map = build_presentazione_image_map(volume)

    # Tracking posizioni per l'indice a due passate.
    # Registriamo (chiave → indice di pagina 0-based) quando una sezione inizia.
    toc_marks: dict[str, int] = {}
    indice_page_idx = [None]   # dove sta la pagina indice (da rigenerare)

    def mark(key: str) -> None:
        toc_marks[key] = len(pages)

    def add(imgs: list[Image.Image]) -> None:
        for p in imgs: pages.append(("single", p))

    def txt(text: str, title: str = "", dark: bool = False) -> None:
        add(make_text_pages(text, title=title, dark=dark))

    def build_pres_pages() -> None:
        pages_recto()
        mark("abitanti")
        pages.append(("single", make_occhiello_abitanti()))
        entries = get_presentazione_parziale(volume)
        print(f"  → Presentazione: {len(entries)} voci")
        luoghi = {"questa è l'isola", "il villaggio", "il quartiere di fuoco",
                  "il quartiere d'aria", "il quartiere di terra",
                  "il quartiere d'acqua", "il mercato del mezzogiorno"}
        for t, body in entries:
            kind = "luogo" if t.lower() in luoghi else "personaggio"
            # "Questa è l'isola": doppia pagina (mappa isola GIORNO sx + testo dx).
            if _title_to_slug(t) == "questa_l_isola":
                print(f"    · {t}: doppia isola giorno (spread)")
                pages.append(("spread", make_isola_doppia(
                    t, body, volume=volume, layout_warnings=layout_warnings,
                    src_default=FRONTMATTER_ISOLA["atlante_questa_isola"])))
                continue
            # Tavola naturalistica (visual/atlante/) se pronta nello spec;
            # altrimenti layout classico — degradazione dolce.
            atl = atlante_entry_for(t) if usa_atlante else None
            if atl is not None:
                voce, tavola = atl
                print(f"    · {t}: tavola atlante ({voce['variante']})")
                pages.append(("single", make_atlante_plate_page(
                    t, body, tavola, volume=volume,
                    variante_id=voce["variante"], kind=kind,
                    binomio=voce.get("binomio"),
                    layout_warnings=layout_warnings)))
                continue
            img = find_presentazione_image(t, image_map)
            # Promozione HD: se è un path low-res nel catalogo, prendi la HD
            # da _hd/<stem>_hd.jpg quando disponibile. Stesso pattern degli
            # hook scena (vedi resolve_scene_image). Preserva il filename
            # nei warning di qualità (basta la low-res come riferimento).
            if img is not None:
                img = resolve_scene_image(img)
            pages.append(("single", make_presentazione_page(
                t, body, img, volume=volume, kind=kind,
                layout_warnings=layout_warnings)))

    def pages_recto():
        nonlocal pages
        if con_front_matter and not solo_storie:
            pages = ensure_recto(pages)

    # ── Front matter editoriale ───────────────────────────────────────────
    if con_front_matter and not solo_storie:
        print("  → Front matter (frontespizio, colophon, dedica, indice)")
        voci_indice = build_indice_voci(volume, storie, posizione_pres)
        cover_p = REPO / "pipeline_narrativa/storie_finali/_volumi/v01/_hd/v01_copertina_candidate_v2_hd.jpg"
        if not cover_p.exists():
            cover_p = REPO / "visual/atlante/emblema/copertina_v1.jpg"
        pages.append(("single", make_blank()))   # foglio di guardia iniziale
        if cover_p.exists():
            pages.append(("single", make_occhiello_copertina()))
        pages.extend([
            ("single", make_frontespizio(volume)),
            ("single", make_colophon(volume)),
            ("single", make_dedica(dedica)),
            ("single", make_blank()),
        ])
        indice_page_idx[0] = len(pages)
        pages.append(("single", make_indice(volume, voci_indice)))  # placeholder
        pages = ensure_recto(pages)

    if not solo_storie:
        print("  → Soglia")
        pages_recto()
        mark("prima_di_leggere")
        pages.append(("single", make_occhiello_prima_di_leggere()))
        txt(get_soglia())
        print(f"  → Introduzione ciclo {volume}")
        txt(get_introduzione_ciclo(volume))
        print(f"  → Stato Zero vol.{volume}")
        _isola_notte = FRONTMATTER_ISOLA["stato_zero"]
        if _isola_notte.exists() and usa_atlante:
            # La doppia "L'isola che dorme" sostituisce la pagina-soglia:
            # è già l'ingresso forte, inutile ripetere il titolo prima.
            # Veduta NOTTURNA HD dell'isola (coerente con "l'isola che dorme").
            print("    · L'isola che dorme: doppia (spread) + continuazione")
            pages = ensure_recto(pages)
            mark("isola_dorme")
            _rem = []
            pages.append(("spread", make_isola_doppia(
                "L'isola che dorme", get_stato_zero(volume),
                volume=volume, layout_warnings=layout_warnings,
                eyebrow="ECCO L'ISOLA", src_default=_isola_notte,
                remainder_out=_rem)))
            if _rem and _rem[0].strip():
                # il testo che non entra nella doppia prosegue su pagina/e carta
                txt(_rem[0])
        else:
            # Fallback senza immagine: pagina-soglia + testo su carta.
            pages_recto()
            mark("isola_dorme")
            pages.append(("single", make_soglia_ingresso("L'isola dorme")))
            txt(get_stato_zero(volume))

        if posizione_pres == "prima":
            build_pres_pages()

    # ── Storie ────────────────────────────────────────────────────────────
    for i, sid in enumerate(storie, 1):
        title = get_story_title(sid)
        print(f"  → Storia {sid}: {title}")
        if con_front_matter and not solo_storie:
            pages_recto()
            mark(f"storia_{i}")
            pages.append(("single", make_occhiello_storia(i, title, volume)))
            pages = ensure_recto(pages)
        else:
            add(make_text_pages("", title=title))
        ciclo = VOLUME_CONFIG[volume]["ciclo"]
        pages.extend(build_story_pages(
            sid, key_color=DS.CICLO_COLOR.get(ciclo, DS.DEFAULT_QUARTIERE_COLOR)))

    # ── Sezioni finali ────────────────────────────────────────────────────
    if not solo_storie:
        if posizione_pres == "dopo":
            build_pres_pages()

        print(f"  → Le Porte vol.{volume}")
        pages_recto()
        mark("porte")
        pages.append(("single", make_occhiello_porte(volume)))
        txt(get_porte(volume))

        if volume == 4:
            print("  → Congedo")
            mark("congedo")
            txt(get_congedo(), title="A te che torni")
        else:
            sig = get_sigillo(volume)
            if sig:
                print(f"  → Sigillo vol.{volume}")
                mark("sigillo")
                txt(sig, dark=True)

    # ── Seconda passata: rigenera l'indice con i numeri di pagina reali ───
    if indice_page_idx[0] is not None:
        voci_num = build_indice_voci_numerate(volume, storie, posizione_pres, toc_marks)
        pages[indice_page_idx[0]] = ("single", make_indice(volume, voci_num))

    # ── Garanzia KDP: numero di facciate pari (spread = 2 facciate) ───────
    if _facciate(pages) % 2 == 1:
        pages.append(("single", make_blank()))

    print(f"  Totale facciate: {_facciate(pages)} "
          f"({len(pages)} elementi, {sum(1 for k,_ in pages if k=='spread')} spread)")
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
    ap.add_argument("--atlante",        choices=["auto", "off"], default="auto",
                    help="Tavole naturalistiche atlante: auto (usa quelle pronte, "
                         "fallback classico) o off (sempre layout classico)")
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
        usa_atlante      = (args.atlante == "auto"),
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
