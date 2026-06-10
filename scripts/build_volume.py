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
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat
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

    # Controllo qualità: le scene devono essere HD (≥ trim+bleed)
    ok, quality_desc = check_image_quality(resolved)

    # Normalizza a IMG_W×IMG_H (trim + bleed, 300 DPI)
    if img.size != (IMG_W, IMG_H):
        img = img.resize((IMG_W, IMG_H), Image.LANCZOS)
    img = img.convert("RGB")

    # ── Testo ADATTIVO: dentro l'illustrazione, con schiarita dolce ───────
    # Ancora: alto (default). Se la fascia alta è occupata da un soggetto
    # importante o troppo scura, lo script sposta in basso e/o schiarisce.
    f     = fnt(FS)
    d0    = ImageDraw.Draw(img)
    lines = word_wrap(text, f, IMG_W - 2*MX2, d0)
    n_lines = len([l for l in lines if l])
    block_h = n_lines * LH + MT + int(FS * 0.8)

    def zone_metrics(y0, y1):
        z = img.crop((0, max(0,y0), IMG_W, min(IMG_H,y1))).convert("L")
        brightness = ImageStat.Stat(z).mean[0] / 255.0
        movement = ImageStat.Stat(z.filter(ImageFilter.FIND_EDGES)).mean[0] / 255.0
        return brightness, movement

    # valuta zona alta e bassa
    top_zone    = (0, block_h)
    bottom_zone = (IMG_H - block_h, IMG_H)
    b_top, m_top = zone_metrics(*top_zone)
    b_bot, m_bot = zone_metrics(*bottom_zone)

    # scegli ancora: preferisci alto; se alto molto movimentato e basso più
    # calmo, vai in basso (il soggetto comanda)
    if m_top > 0.16 and m_bot < m_top - 0.04:
        zone = "bottom"; y0z = IMG_H - block_h
        bright, move = b_bot, m_bot
    else:
        zone = "top"; y0z = 0
        bright, move = b_top, m_top

    # decidi trattamento: INSIDE se calmo+chiaro, altrimenti DODGE
    treatment = "INSIDE" if (bright > 0.60 and move < 0.11) else "DODGE"

    if treatment == "DODGE":
        # schiarita dolce, sfumata, niente box
        mask = Image.new("L", (IMG_W, IMG_H), 0)
        md = ImageDraw.Draw(mask)
        md.rectangle([0, y0z, IMG_W, y0z + block_h], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(int(IMG_W*0.04)))
        paper = Image.new("RGB", (IMG_W, IMG_H), DS.PAPER)
        lightened = Image.blend(img, paper, 0.72)
        img = Image.composite(lightened, img, mask)

    draw = ImageDraw.Draw(img)
    y = MT if zone == "top" else (y0z + MT)
    for ln in lines:
        if ln == "":
            y += PGS; continue
        draw.text((MX2, y), ln, font=f, fill=STORY_INK)
        y += LH

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


def ensure_recto(pages: list) -> list:
    """Aggiunge una bianca se necessario perché la prossima pagina cada su recto."""
    if len(pages) % 2 == 1:
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


def make_frontespizio(volume: int) -> Image.Image:
    """Frontespizio: logo spirale + titolo collana + volume + ciclo + editore."""
    cfg = VOLUME_CONFIG[volume]
    img = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    d = ImageDraw.Draw(img)
    vento = DS.CICLO_COLOR.get(cfg["ciclo"], DS.ACCENT)

    logo = DS.make_logo_image(int(TX_W*0.13), DS.SPIRALE)
    img.paste(logo, (TX_W//2 - logo.width//2, int(TX_H*0.14)), logo)

    f_title = DS.font("mark", int(TX_W*0.066))
    _center(d, "L'Isola", f_title, int(TX_H*0.265), DS.INK)
    _center(d, "dei Tre Venti", f_title, int(TX_H*0.322), DS.INK)

    DS.draw_wind_rule(d, TX_W//2 - int(TX_W*0.14), TX_W//2 + int(TX_W*0.14),
                      int(TX_H*0.40), DS.RULE, max(2, TX_W//560))

    f_vol = DS.font_weighted("sans", int(TX_W*0.025), 700)
    _tracked_center(d, VOLUME_NOMI[volume], f_vol, int(TX_H*0.425), DS.SPIRALE, 5)

    f_sub = DS.font("display_i", int(TX_W*0.032))
    _center(d, CICLO_SOTTOTITOLO.get(cfg["ciclo"], ""), f_sub, int(TX_H*0.465), DS.INK_SOFT)

    f_auth = DS.font("sans", int(TX_W*0.024))
    _center(d, "Ray D'Alessandro", f_auth, int(TX_H*0.85), DS.INK)
    f_ed = DS.font_weighted("sans", int(TX_W*0.019), 600)
    _tracked_center(d, "SPIRALE EDITRICE", f_ed, int(TX_H*0.88), DS.INK_FAINT, 4)
    return img


def make_colophon(volume: int) -> Image.Image:
    """Colophon: copyright, dati edizione, disclaimer AI, lockup."""
    cfg = VOLUME_CONFIG[volume]
    img = Image.new("RGB", (TX_W, TX_H), DS.PAPER)
    d = ImageDraw.Draw(img)
    MXc = int(TX_W * 0.10)
    y = int(TX_H * 0.12)

    d.text((MXc, y), "© 2026 RAY D'ALESSANDRO",
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
           "EAR LAB · SPIRALE EDITRICE",
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
            img = find_presentazione_image(t, image_map)
            # Promozione HD: se è un path low-res nel catalogo, prendi la HD
            # da _hd/<stem>_hd.jpg quando disponibile. Stesso pattern degli
            # hook scena (vedi resolve_scene_image). Preserva il filename
            # nei warning di qualità (basta la low-res come riferimento).
            if img is not None:
                img = resolve_scene_image(img)
            kind = "luogo" if t.lower() in luoghi else "personaggio"
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
        print(f"  → Qui entri nell'isola (soglia)")
        pages_recto()
        mark("isola_dorme")
        pages.append(("single", make_soglia_ingresso("L'isola dorme")))
        print(f"  → Stato Zero vol.{volume}")
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
        pages.extend(build_story_pages(sid))

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

    # ── Garanzia KDP: numero di pagine pari ───────────────────────────────
    if len(pages) % 2 == 1:
        pages.append(("single", make_blank()))

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
