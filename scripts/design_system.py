#!/usr/bin/env python3
"""
design_system.py — Identità visiva "L'Isola dei Tre Venti"
============================================================
Collana per bambini di Spirale Editrice.

Definisce palette, font, e componenti grafici riutilizzabili per dare
ANIMA editoriale ai volumi: non un PDF impaginato, ma un libro.

Identità:
  - Calore avorio della carta (eredità Spirale)
  - I tre venti come sistema-colore (Taglio/Intreccio/Mulinello)
  - Tipografia: Fraunces (serif caldo, display+corpo) come voce principale,
    Nunito (sans tondo) per eyebrow/metadati, Fredoka per il marchio collana
  - Il logo Spirale (spirale-foglia) come filo conduttore

Usato da build_volume.py. Importabile come modulo.
"""

from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# ═══════════════════════════════════════════════════════════════════════════
# PERCORSI FONT
# ═══════════════════════════════════════════════════════════════════════════
_HERE = Path(__file__).resolve().parent
FONT_DIRS = [
    _HERE.parent / "assets/fonts",
    Path("/usr/share/fonts/truetype/google-fonts"),
    Path("/Library/Fonts"),
    Path("C:/Windows/Fonts"),
]

def _find(name: str) -> Path | None:
    for d in FONT_DIRS:
        fp = d / name
        if fp.exists():
            return fp
    return None

# Font della collana
F_DISPLAY = _find("Fraunces.ttf")          # titoli, corpo storia, display caldo
F_DISPLAY_I = _find("Fraunces-Italic.ttf") # corsivi eleganti
F_SANS    = _find("Nunito.ttf")            # eyebrow, metadati, didascalie
F_SANS_I  = _find("Nunito-Italic.ttf")
F_MARK    = _find("Fredoka.ttf")           # marchio collana, numeri grandi
# Fallback serif (corpo classico se Fraunces non c'è)
F_SERIF   = _find("Lora-Variable.ttf") or F_DISPLAY
F_SERIF_I = _find("Lora-Italic-Variable.ttf") or F_DISPLAY_I


def font(which: str, size: int) -> ImageFont.FreeTypeFont:
    """
    which: 'display' | 'display_i' | 'sans' | 'sans_i' | 'mark' | 'serif' | 'serif_i'
    """
    mapping = {
        "display":   F_DISPLAY,
        "display_i": F_DISPLAY_I,
        "sans":      F_SANS,
        "sans_i":    F_SANS_I,
        "mark":      F_MARK,
        "serif":     F_SERIF,
        "serif_i":   F_SERIF_I,
    }
    path = mapping.get(which, F_DISPLAY)
    if path and path.exists():
        f = ImageFont.truetype(str(path), size)
        # Imposta peso variabile dove serve
        try:
            if which in ("display", "serif"):
                f.set_variation_by_axes([400])
            elif which == "mark":
                f.set_variation_by_axes([600, 100])  # wght, wdth per Fredoka
        except Exception:
            pass
        return f
    return ImageFont.load_default()


def font_weighted(which: str, size: int, weight: int) -> ImageFont.FreeTypeFont:
    """Font con peso variabile specifico (per Fraunces/Nunito variable)."""
    f = font(which, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f

# ═══════════════════════════════════════════════════════════════════════════
# PALETTE — "I tre venti"
# ═══════════════════════════════════════════════════════════════════════════
# Carta e inchiostri base (eredità Spirale, calda)
PAPER       = (250, 247, 240)   # avorio caldo
PAPER_DEEP  = (244, 238, 227)   # avorio più saturo (fondi alternati)
INK         = (43,  35,  27)    # marrone-nero caldo (corpo testo)
INK_SOFT    = (92,  78,  62)    # testo secondario
INK_FAINT   = (150, 134, 112)   # didascalie, numeri pagina

# Verde Spirale (marchio, eredità collana adulti)
SPIRALE     = (21, 135, 90)     # #15875a

# I tre venti — sistema cromatico della saga
VENTO_TAGLIO    = (74, 110, 138)   # azzurro freddo, inverno, Gabriel (Δ distingue)
VENTO_INTRECCIO = (94, 138, 86)    # verde, primavera/estate, Elias (⇄ connette)
VENTO_MULINELLO = (190, 130, 58)   # ambra, autunno, Noah (⟳ cambia)

# Accento caldo principale (per titoli, accenti editoriali)
ACCENT      = (140, 90, 48)     # terracotta calda
RULE        = (200, 180, 152)   # linee decorative

# Mappa ciclo → colore vento
CICLO_COLOR = {
    "Δ":            VENTO_TAGLIO,
    "⇄":            VENTO_INTRECCIO,
    "⟳":            VENTO_MULINELLO,
    "Integrazione": ACCENT,
}

# I quartieri dell'isola — colore d'appartenenza (per la cornice dell'atlante).
# Toni naturali, coerenti con l'elemento di ciascun quartiere.
QUARTIERE_COLOR = {
    "fuoco":     (190, 130, 58),   # ambra calda (il Forno, Fiamma)
    "acqua":     (74, 130, 150),   # azzurro-verde acqua
    "aria":      (120, 140, 165),  # azzurro chiaro, cielo
    "terra":     (140, 110, 66),   # bruno terra
    "centro":    (150, 120, 70),   # ocra del Villaggio
    "perimetro": (110, 120, 95),   # verde-grigio della costa/bosco
}
DEFAULT_QUARTIERE_COLOR = ACCENT

# ═══════════════════════════════════════════════════════════════════════════
# LOGO SPIRALE (vettoriale, disegnato)
# ═══════════════════════════════════════════════════════════════════════════
def draw_spirale_logo(draw: ImageDraw.ImageDraw, cx: int, cy: int,
                      r: int, color: tuple = SPIRALE, width: int = 0) -> None:
    """
    Disegna il marchio Spirale: una spirale-foglia.
    Una spirale logaritmica che si chiude come una foglia/conchiglia.
    cx, cy: centro · r: raggio esterno
    """
    if width == 0:
        width = max(2, r // 12)

    # Spirale logaritmica
    points = []
    turns = 2.6
    steps = 120
    a = r / math.exp(0.30 * turns * 2 * math.pi)
    b = 0.30
    for i in range(steps + 1):
        theta = (i / steps) * turns * 2 * math.pi
        rad = a * math.exp(b * theta)
        x = cx + rad * math.cos(theta - math.pi / 2)
        y = cy + rad * math.sin(theta - math.pi / 2)
        points.append((x, y))

    if len(points) > 1:
        draw.line(points, fill=color, width=width, joint="curve")

    # Piccola foglia/goccia di chiusura in cima
    tip = points[-1]
    leaf_r = max(3, r // 8)
    draw.ellipse(
        [tip[0] - leaf_r, tip[1] - leaf_r, tip[0] + leaf_r, tip[1] + leaf_r],
        fill=color,
    )


def make_logo_image(size: int = 200, color: tuple = SPIRALE,
                    bg: tuple | None = None) -> Image.Image:
    """Crea un'immagine del logo Spirale, opzionalmente con sfondo."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0) if bg is None else (*bg, 255))
    d = ImageDraw.Draw(img)
    draw_spirale_logo(d, size // 2, size // 2, int(size * 0.38), color)
    return img

# ═══════════════════════════════════════════════════════════════════════════
# DECORI E ORNAMENTI
# ═══════════════════════════════════════════════════════════════════════════
def draw_wind_rule(draw: ImageDraw.ImageDraw, x0: int, x1: int, y: int,
                   color: tuple = RULE, width: int = 1) -> None:
    """
    Linea decorativa 'soffio di vento': una linea sottile che ondeggia
    leggermente al centro, come una folata. Più viva di una riga dritta.
    """
    mid = (x0 + x1) / 2
    span = x1 - x0
    points = []
    for i in range(61):
        t = i / 60
        x = x0 + t * span
        # piccola onda al centro che si smorza ai bordi
        env = math.sin(t * math.pi)        # 0 ai bordi, 1 al centro
        wave = math.sin(t * math.pi * 3) * 2.2 * env
        points.append((x, y + wave))
    draw.line(points, fill=color, width=width, joint="curve")


def draw_dot_ornament(draw: ImageDraw.ImageDraw, cx: int, cy: int,
                      color: tuple = RULE, spread: int = 22) -> None:
    """Tre puntini orizzontali — separatore minimale tra sezioni."""
    rdot = 2
    for dx in (-spread, 0, spread):
        draw.ellipse([cx + dx - rdot, cy - rdot, cx + dx + rdot, cy + rdot], fill=color)


def draw_corner_flourish(draw: ImageDraw.ImageDraw, x: int, y: int,
                         size: int, color: tuple = RULE, corner: str = "tl") -> None:
    """Piccolo svolazzo d'angolo per cornici delicate."""
    w = max(1, size // 20)
    if corner == "tl":
        draw.arc([x, y, x + size, y + size], 180, 270, fill=color, width=w)
    elif corner == "tr":
        draw.arc([x - size, y, x, y + size], 270, 360, fill=color, width=w)
    elif corner == "bl":
        draw.arc([x, y - size, x + size, y], 90, 180, fill=color, width=w)
    elif corner == "br":
        draw.arc([x - size, y - size, x, y], 0, 90, fill=color, width=w)


# ═══════════════════════════════════════════════════════════════════════════
# MOTIVI-AMBIENTE (tratto leggero, per i margini delle presentazioni)
# ═══════════════════════════════════════════════════════════════════════════
# Ogni motivo disegna un piccolo elemento del mondo del personaggio.
# Stile: tratto sottile, colore tenue. Pensati per stare nei margini.

def motif_wheat(draw, x, y, scale, color):
    """Spiga di grano (Fiamma, il Forno)."""
    w = max(1, int(scale * 0.05))
    draw.line([(x, y), (x, y - scale)], fill=color, width=w)
    for i in range(6):
        yy = y - scale * 0.16 * i - scale * 0.08
        l = scale * 0.26
        draw.line([(x, yy), (x - l * 0.7, yy - l * 0.55)], fill=color, width=w)
        draw.line([(x, yy), (x + l * 0.7, yy - l * 0.55)], fill=color, width=w)


def motif_bread(draw, cx, cy, scale, color):
    """Pagnotta tonda con taglio a croce (Fiamma)."""
    import math as _m
    w = max(1, int(scale * 0.05))
    # corpo della pagnotta (ovale schiacciato)
    draw.arc([cx - scale, cy - scale * 0.5, cx + scale, cy + scale * 0.85],
             185, 355, fill=color, width=w)
    draw.line([(cx - scale * 0.96, cy + scale * 0.16),
               (cx + scale * 0.96, cy + scale * 0.16)], fill=color, width=w)
    # taglio sopra
    draw.line([(cx - scale * 0.35, cy - scale * 0.18),
               (cx + scale * 0.05, cy - scale * 0.42)], fill=color, width=w)


def motif_star(draw, cx, cy, scale, color):
    """Stella alpina (Grunto, le Gemelle)."""
    import math as _m
    w = max(1, int(scale * 0.05))
    for a in range(10):
        ang = a * _m.pi / 5
        rr = scale if a % 2 == 0 else scale * 0.42
        draw.line([(cx, cy), (cx + _m.cos(ang) * rr, cy + _m.sin(ang) * rr)],
                  fill=color, width=w)


def motif_stone(draw, cx, cy, scale, color):
    """Sasso tondeggiante (Grunto, il Burrone)."""
    w = max(1, int(scale * 0.06))
    draw.ellipse([cx - scale, cy - scale * 0.62, cx + scale, cy + scale * 0.62],
                 outline=color, width=w)
    draw.arc([cx - scale * 0.5, cy - scale * 0.3, cx + scale * 0.2, cy + scale * 0.2],
             20, 160, fill=color, width=w)


def motif_curl(draw, cx, cy, scale, color):
    """Truciolo di legno (Mèmolo falegname)."""
    import math as _m
    pts = []
    for i in range(44):
        t = i / 44
        ang = t * _m.pi * 2.4
        rad = scale * (1 - t * 0.55)
        pts.append((cx + _m.cos(ang) * rad, cy + _m.sin(ang) * rad))
    if len(pts) > 1:
        draw.line(pts, fill=color, width=max(1, int(scale * 0.06)), joint="curve")


def motif_leaf(draw, cx, cy, scale, color):
    """Foglia (Rovo, la Foresta Intrecciata)."""
    import math as _m
    w = max(1, int(scale * 0.05))
    # nervatura centrale
    draw.line([(cx, cy + scale), (cx, cy - scale)], fill=color, width=w)
    # contorno foglia (due archi)
    pts_l, pts_r = [], []
    for i in range(21):
        t = i / 20
        yy = cy + scale - t * 2 * scale
        env = _m.sin(t * _m.pi) * scale * 0.5
        pts_l.append((cx - env, yy))
        pts_r.append((cx + env, yy))
    draw.line(pts_l, fill=color, width=w, joint="curve")
    draw.line(pts_r, fill=color, width=w, joint="curve")


def motif_feather(draw, cx, cy, scale, color):
    """Piuma (Stria airone, Nodo)."""
    import math as _m
    w = max(1, int(scale * 0.045))
    draw.line([(cx, cy + scale), (cx + scale * 0.15, cy - scale)], fill=color, width=w)
    for i in range(7):
        t = i / 7
        yy = cy + scale - t * 1.8 * scale
        xx = cx + scale * 0.15 * t
        bl = scale * 0.4 * (1 - t * 0.5)
        draw.line([(xx, yy), (xx - bl, yy - bl * 0.3)], fill=color, width=w)
        draw.line([(xx, yy), (xx + bl, yy - bl * 0.3)], fill=color, width=w)


def motif_drop(draw, cx, cy, scale, color):
    """Goccia d'acqua (Amo, il Quartiere d'Acqua)."""
    import math as _m
    w = max(1, int(scale * 0.06))
    pts = []
    for i in range(33):
        t = i / 32
        ang = t * 2 * _m.pi
        r = scale * (0.5 + 0.5 * _m.sin(ang / 2))
        pts.append((cx + _m.sin(ang) * scale * 0.6, cy - _m.cos(ang) * r))
    draw.line(pts + [pts[0]], fill=color, width=w, joint="curve")


# Repertorio motivi per personaggio/luogo (slug → lista di motivi)
MOTIF_MAP = {
    "fiamma":      [motif_wheat, motif_bread],
    "grunto":      [motif_star, motif_stone],
    "memolo_pun":  [motif_curl, motif_leaf],
    "memolo":      [motif_curl, motif_leaf],
    "rovo_bru":    [motif_leaf, motif_stone],
    "bru":         [motif_leaf],
    "stria":       [motif_feather, motif_leaf],
    "nodo":        [motif_feather],
    "salvia":      [motif_leaf, motif_drop],
    "zolla":       [motif_leaf, motif_stone],
    "bartolo_toba":[motif_drop, motif_feather],
    "bambini":     [motif_leaf, motif_star],
}

DEFAULT_MOTIFS = [motif_leaf, motif_stone]


def tint_color(color, amount=0.55):
    """Versione schiarita di un colore (per i motivi tenui)."""
    return tuple(int(c * (1 - amount) + 255 * amount) for c in color)


# ═══════════════════════════════════════════════════════════════════════════
# COMPOSIZIONE — helper condivisi
# ═══════════════════════════════════════════════════════════════════════════
def small_spiral(draw, cx, cy, r, color, width, mirror=False):
    """Spiralina-marchio (chiusura filetti, angoli). mirror inverte il verso."""
    pts = []
    turns, steps = 2.2, 80
    a = r / math.exp(0.30 * turns * 2 * math.pi)
    b = 0.30
    for i in range(steps + 1):
        th = (i / steps) * turns * 2 * math.pi
        rad = a * math.exp(b * th)
        ang = -th if mirror else th
        pts.append((cx + rad * math.cos(ang - math.pi / 2),
                    cy + rad * math.sin(ang - math.pi / 2)))
    if len(pts) > 1:
        draw.line(pts, fill=color, width=width, joint="curve")
    tip = pts[-1]
    lr = max(2, r // 8)
    draw.ellipse([tip[0] - lr, tip[1] - lr, tip[0] + lr, tip[1] + lr], fill=color)


def paste_soft(canvas, illus, box, feather, paper=PAPER):
    """
    Incolla un'immagine dentro `box` (x0,y0,x1,y1) con i bordi sfumati
    nella carta. L'immagine viene contenuta (contain) senza tagli.
    Ritorna il box effettivo (px0,py0,px1,py1) dell'immagine piazzata.
    """
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    iw, ih = illus.size
    scale = min(bw / iw, bh / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    illus = illus.resize((nw, nh), Image.LANCZOS)
    px = x0 + (bw - nw) // 2
    py = y0 + (bh - nh) // 2
    mask = Image.new("L", (nw, nh), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle([feather, feather, nw - feather, nh - feather], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather * 0.6))
    canvas.paste(illus, (px, py), mask)
    return (px, py, px + nw, py + nh)


def draw_wind_frame(draw, box, color, width, amp, spiral_r):
    """
    Cornice-vento: quattro lati con leggera ondulazione (folata) e
    spiraline-marchio ai quattro angoli. `box` = (x0,y0,x1,y1).
    """
    x0, y0, x1, y1 = box

    def wavy(p0, p1, horizontal, n=90):
        pts = []
        for i in range(n + 1):
            t = i / n
            if horizontal:
                x = p0[0] + (p1[0] - p0[0]) * t
                y = p0[1] + math.sin(t * math.pi * 4) * amp
            else:
                x = p0[0] + math.sin(t * math.pi * 4) * amp
                y = p0[1] + (p1[1] - p0[1]) * t
            pts.append((x, y))
        return pts

    draw.line(wavy((x0, y0), (x1, y0), True),  fill=color, width=width, joint="curve")
    draw.line(wavy((x0, y1), (x1, y1), True),  fill=color, width=width, joint="curve")
    draw.line(wavy((x0, y0), (x0, y1), False), fill=color, width=width, joint="curve")
    draw.line(wavy((x1, y0), (x1, y1), False), fill=color, width=width, joint="curve")
    for (cx, cy) in [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]:
        small_spiral(draw, cx, cy, spiral_r, color, width)


# ─── CORNICI DELLA COLLANA (asset) ──────────────────────────────────────────
# Quattro cornici per l'atlante dei personaggi. Tornano in tutti e 4 i volumi.
# Tutte parametriche: box=(x0,y0,x1,y1), colore del vento, spessore.

def cornice_doppio_filetto(draw, box, color, width, unit):
    """1 — doppio filetto + spirali agli angoli. Elegante, sobria."""
    x0, y0, x1, y1 = box
    off = max(3, int(unit * 0.5))
    for o in (0, off):
        draw.rectangle([x0-o, y0-o, x1+o, y1+o], outline=color, width=max(1, width//2))
    r = unit
    small_spiral(draw, x0, y0, r, color, width)
    small_spiral(draw, x1, y0, r, color, width, mirror=True)
    small_spiral(draw, x0, y1, r, color, width, mirror=True)
    small_spiral(draw, x1, y1, r, color, width)


def cornice_angoli_vento(draw, box, color, width, unit):
    """2 — solo angoli, lati aperti. Moderna, leggera."""
    x0, y0, x1, y1 = box
    L = int(unit * 2.6)
    for cx, cy, sx, sy in [(x0,y0,1,1), (x1,y0,-1,1), (x0,y1,1,-1), (x1,y1,-1,-1)]:
        draw.line([(cx, cy+sy*L), (cx, cy), (cx+sx*L, cy)],
                  fill=color, width=width, joint="curve")
        small_spiral(draw, cx, cy, int(unit*0.8), color, width, mirror=(sx*sy < 0))


def cornice_festone(draw, box, color, width, unit):
    """3 — festone ondulato continuo: il vento reso visibile. Giocosa."""
    x0, y0, x1, y1 = box
    amp = max(3, int(unit * 0.18))

    def side(p0, p1, horiz, n=120):
        pts = []
        for i in range(n + 1):
            t = i / n
            if horiz:
                x = p0[0] + (p1[0]-p0[0])*t; y = p0[1] + math.sin(t*math.pi*8)*amp
            else:
                x = p0[0] + math.sin(t*math.pi*8)*amp; y = p0[1] + (p1[1]-p0[1])*t
            pts.append((x, y))
        return pts

    draw.line(side((x0,y0),(x1,y0),True),  fill=color, width=width, joint="curve")
    draw.line(side((x0,y1),(x1,y1),True),  fill=color, width=width, joint="curve")
    draw.line(side((x0,y0),(x0,y1),False), fill=color, width=width, joint="curve")
    draw.line(side((x1,y0),(x1,y1),False), fill=color, width=width, joint="curve")
    for cx, cy, m in [(x0,y0,False),(x1,y0,True),(x0,y1,True),(x1,y1,False)]:
        small_spiral(draw, cx, cy, int(unit*0.75), color, width, mirror=m)


def cornice_grappolo(draw, box, color, width, unit):
    """4 — cantonali a grappolo: tre soffi-spirale per angolo (i tre venti).
    La piu' caratteristica: lega la cornice alla mitologia della saga."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=color, width=width)

    def cluster(cx, cy, sx, sy):
        m = (sx * sy < 0)
        small_spiral(draw, cx, cy, int(unit*0.85), color, width, mirror=m)
        small_spiral(draw, cx + sx*int(unit*1.1), cy + sy*int(unit*0.35),
                     int(unit*0.42), color, max(1, width-1), mirror=m)
        small_spiral(draw, cx + sx*int(unit*0.35), cy + sy*int(unit*1.1),
                     int(unit*0.42), color, max(1, width-1), mirror=m)

    cluster(x0, y0, 1, 1); cluster(x1, y0, -1, 1)
    cluster(x0, y1, 1, -1); cluster(x1, y1, -1, -1)


# Repertorio cornici (per scelta/iterazione)
CORNICI = {
    "doppio_filetto": cornice_doppio_filetto,
    "angoli_vento":   cornice_angoli_vento,
    "festone":        cornice_festone,
    "grappolo":       cornice_grappolo,
}


# ─── SEPARATORE CAMUNO ──────────────────────────────────────────────────────
# Sostituisce le linee dritte / filetti standard. Tratto "inciso a mano":
# una fila di piccole marche camune unite da un filo ondulato leggero.

def separatore_camuno(draw, x0, x1, y, color, width, motif=None):
    """
    Filo ondulato leggero con tre marche camune (al centro e ai capi).
    Da usare al posto di linee dritte e separatori standard.
    """
    span = x1 - x0
    mid = (x0 + x1) / 2
    # filo ondulato (folata), non retta
    pts = []
    for i in range(81):
        t = i / 80
        x = x0 + t * span
        env = math.sin(t * math.pi)
        wave = math.sin(t * math.pi * 5) * 2.4 * env
        pts.append((x, y + wave))
    draw.line(pts, fill=color, width=width, joint="curve")
    # marca centrale: rosa camuna piccola
    r = max(6, int(span * 0.025))
    if motif is None:
        motif = camuno_rosa
    motif(draw, int(mid), int(y), r, color, width)
    # due piccole spirali ai capi, rivolte verso il centro
    small_spiral(draw, x0, y, int(r*0.7), color, width)
    small_spiral(draw, x1, y, int(r*0.7), color, width, mirror=True)


# ═══════════════════════════════════════════════════════════════════════════
# DECORI D'ANIMA — incisioni camune, rosa dei venti, atlante, glifi
# ═══════════════════════════════════════════════════════════════════════════
# Asset vettoriali della collana. Tratto essenziale "inciso a mano",
# coerente con un libro per bambini e con l'immaginario arcaico dell'isola.
# Ispirati alle incisioni rupestri della Val Camonica.

# ─── Rosa dei tre venti ─────────────────────────────────────────────────────
def rosa_tre_venti(draw, cx, cy, r, width, colors=None, faint=False):
    """Tre spirali a 120° nei colori dei venti — simbolo-firma della collana."""
    if colors is None:
        colors = [VENTO_TAGLIO, VENTO_INTRECCIO, VENTO_MULINELLO]
    for k, col in enumerate(colors):
        if faint:
            col = tint_color(col, 0.55)
        base_ang = k * 2 * math.pi / 3 - math.pi / 2
        pts = []
        turns, steps = 0.85, 60
        a = r / math.exp(0.55 * turns * 2 * math.pi)
        b = 0.55
        for i in range(steps + 1):
            th = (i / steps) * turns * 2 * math.pi
            rad = a * math.exp(b * th)
            ang = base_ang + th
            pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
        if len(pts) > 1:
            draw.line(pts, fill=col, width=width, joint="curve")
        tip = pts[-1]
        lr = max(2, width)
        draw.ellipse([tip[0]-lr, tip[1]-lr, tip[0]+lr, tip[1]+lr], fill=col)
    draw.ellipse([cx-width, cy-width, cx+width, cy+width], fill=INK_SOFT)


# ─── Isola stilizzata (atlantino) ───────────────────────────────────────────
def isola_stilizzata(draw, cx, cy, r, color, vento_colors=None):
    """L'isola a tratto: contorno, fiume che gira, villaggio, quattro quartieri."""
    if vento_colors is None:
        vento_colors = [VENTO_MULINELLO, VENTO_TAGLIO, VENTO_INTRECCIO, ACCENT]
    w = max(2, r // 60)
    # contorno isola
    pts = []
    for i in range(73):
        t = i / 72; ang = t * 2 * math.pi
        wob = 1 + 0.04 * math.sin(ang * 5)
        pts.append((cx + math.cos(ang) * r * wob, cy + math.sin(ang) * r * wob))
    draw.line(pts, fill=color, width=w, joint="curve")
    # fiume che gira
    rin = r * 0.62
    pts = [(cx + math.cos(i/72*2*math.pi)*rin, cy + math.sin(i/72*2*math.pi)*rin)
           for i in range(73)]
    draw.line(pts, fill=VENTO_TAGLIO, width=max(1, w-1), joint="curve")
    # villaggio: alberello
    draw.line([(cx, cy+r*0.12), (cx, cy-r*0.08)], fill=color, width=w)
    draw.ellipse([cx-r*0.10, cy-r*0.22, cx+r*0.10, cy-r*0.02], outline=color, width=w)
    # quartieri ai punti cardinali
    ex, ey = cx+r*0.40, cy   # E fuoco — triangolo
    draw.polygon([(ex,ey-r*0.06),(ex-r*0.05,ey+r*0.04),(ex+r*0.05,ey+r*0.04)],
                 outline=vento_colors[0], width=w)
    sx, sy = cx, cy+r*0.40   # S acqua — goccia
    draw.ellipse([sx-r*0.045,sy-r*0.03,sx+r*0.045,sy+r*0.06], outline=VENTO_TAGLIO, width=w)
    ox, oy = cx-r*0.40, cy   # O terra — quadrato
    draw.rectangle([ox-r*0.045,oy-r*0.045,ox+r*0.045,oy+r*0.045],
                   outline=vento_colors[2], width=w)
    nx, ny = cx, cy-r*0.40   # N aria — tre linee
    for dy in (-r*0.03, 0, r*0.03):
        draw.line([(nx-r*0.05,ny+dy),(nx+r*0.05,ny+dy)], fill=vento_colors[1], width=w)


# ─── Glifi dei tre venti (disegnati, non da font) ───────────────────────────
def glifo_taglio(draw, cx, cy, r, color, width):
    """Δ — distingue: triangolo netto."""
    draw.line([(cx,cy-r),(cx-r*0.88,cy+r*0.6),(cx+r*0.88,cy+r*0.6),(cx,cy-r)],
              fill=color, width=width, joint="curve")

def glifo_intreccio(draw, cx, cy, r, color, width):
    """⇄ — connette: due archi che si abbracciano."""
    draw.arc([cx-r, cy-r*0.5, cx+r*0.2, cy+r*0.5], 270, 90, fill=color, width=width)
    draw.arc([cx-r*0.2, cy-r*0.5, cx+r, cy+r*0.5], 90, 270, fill=color, width=width)

def glifo_mulinello(draw, cx, cy, r, color, width):
    """⟳ — cambia: spirale-vortice con freccia."""
    pts = []
    turns, steps = 1.4, 90
    a = r / math.exp(0.18*turns*2*math.pi); b = 0.18
    for i in range(steps+1):
        th = (i/steps)*turns*2*math.pi
        rad = a*math.exp(b*th)
        pts.append((cx+rad*math.cos(th-math.pi/2), cy+rad*math.sin(th-math.pi/2)))
    draw.line(pts, fill=color, width=width, joint="curve")
    tip = pts[-1]
    draw.line([tip,(tip[0]-r*0.18,tip[1]-r*0.05)], fill=color, width=width)
    draw.line([tip,(tip[0]-r*0.05,tip[1]+r*0.16)], fill=color, width=width)

GLIFO_VENTO = {"Δ": glifo_taglio, "⇄": glifo_intreccio, "⟳": glifo_mulinello}


# ─── Repertorio camuno (incisioni Val Camonica) ─────────────────────────────
def camuno_rosa(draw, cx, cy, r, color, width):
    """Rosa camuna: quattro bracci a uncino che ruotano (girandola curvilinea),
    ognuno con occhiello terminale, + cuore centrale. Leggibile anche piccola."""
    w = width
    for k in range(4):
        ang = k * math.pi / 2
        ca, sa = math.cos(ang), math.sin(ang)
        def rot(x, y): return (cx + x*ca - y*sa, cy + x*sa + y*ca)
        pts = [rot(r*0.12, -r*0.10), rot(r*0.12, -r*0.72)]
        steps = 16
        for i in range(steps + 1):
            t = i / steps
            a = math.pi * 1.15 * t
            ox = r*0.12 + r*0.30 * math.sin(a)
            oy = -r*0.72 - r*0.30 * (1 - math.cos(a))
            pts.append(rot(ox, oy))
        draw.line(pts, fill=color, width=w, joint="curve")
        end = pts[-1]
        lr = max(2, int(r*0.07))
        draw.ellipse([end[0]-lr, end[1]-lr, end[0]+lr, end[1]+lr], fill=color)
    cr = max(2, int(r*0.11))
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=color)

def camuno_orante(draw, cx, cy, r, color, width):
    """Figura umana con braccia alzate."""
    w = width
    draw.ellipse([cx-r*0.16, cy-r, cx+r*0.16, cy-r*0.68], outline=color, width=w)
    draw.line([(cx,cy-r*0.68),(cx,cy+r*0.30)], fill=color, width=w)
    draw.line([(cx,cy-r*0.45),(cx-r*0.5,cy-r*0.75)], fill=color, width=w)
    draw.line([(cx,cy-r*0.45),(cx+r*0.5,cy-r*0.75)], fill=color, width=w)
    draw.line([(cx,cy+r*0.30),(cx-r*0.4,cy+r*0.9)], fill=color, width=w)
    draw.line([(cx,cy+r*0.30),(cx+r*0.4,cy+r*0.9)], fill=color, width=w)

def camuno_capanna(draw, cx, cy, r, color, width):
    """Casa/insediamento su palafitta."""
    w = width
    draw.line([(cx-r*0.7,cy),(cx,cy-r*0.8),(cx+r*0.7,cy)], fill=color, width=w, joint="curve")
    draw.line([(cx-r*0.55,cy),(cx-r*0.55,cy+r*0.7)], fill=color, width=w)
    draw.line([(cx+r*0.55,cy),(cx+r*0.55,cy+r*0.7)], fill=color, width=w)
    draw.line([(cx-r*0.55,cy+r*0.7),(cx+r*0.55,cy+r*0.7)], fill=color, width=w)
    draw.line([(cx-r*0.35,cy+r*0.7),(cx-r*0.35,cy+r*1.0)], fill=color, width=w)
    draw.line([(cx+r*0.35,cy+r*0.7),(cx+r*0.35,cy+r*1.0)], fill=color, width=w)

def camuno_cervo(draw, cx, cy, r, color, width):
    """Cervo camuno: corpo con dorso, quattro zampe slanciate, collo,
    testa allungata, grandi corna ramificate, coda."""
    w = width
    bx0, bx1 = cx - r*0.55, cx + r*0.5
    # dorso leggermente inarcato
    draw.line([(bx0, cy+r*0.05), (cx-r*0.1, cy-r*0.05), (bx1, cy)],
              fill=color, width=w, joint="curve")
    # ventre
    draw.line([(bx0+r*0.08, cy+r*0.5), (bx1-r*0.05, cy+r*0.45)], fill=color, width=w)
    # zampe
    for dx in (-0.42, -0.18, 0.18, 0.40):
        x = cx + r*dx
        draw.line([(x, cy+r*0.08), (x, cy+r*0.62)], fill=color, width=w)
    # collo + testa
    nx, ny = bx1, cy
    hx, hy = nx + r*0.30, ny - r*0.55
    draw.line([(nx, ny), (hx, hy)], fill=color, width=w)
    draw.line([(hx, hy), (hx+r*0.22, hy-r*0.05)], fill=color, width=w)  # muso
    # corna ramificate
    def palco(sx):
        base = (hx - r*0.02, hy - r*0.02)
        tip = (base[0] + sx*r*0.12, base[1] - r*0.55)
        draw.line([base, tip], fill=color, width=w)
        draw.line([(base[0]+sx*r*0.04, base[1]-r*0.18),
                   (base[0]+sx*r*0.26, base[1]-r*0.24)], fill=color, width=w)
        draw.line([(base[0]+sx*r*0.08, base[1]-r*0.36),
                   (base[0]+sx*r*0.30, base[1]-r*0.40)], fill=color, width=w)
    palco(-1); palco(1)
    # coda
    draw.line([(bx0, cy+r*0.05), (bx0-r*0.12, cy-r*0.08)], fill=color, width=w)

def camuno_sole(draw, cx, cy, r, color, width):
    """Disco raggiato."""
    w = width
    draw.ellipse([cx-r*0.4,cy-r*0.4,cx+r*0.4,cy+r*0.4], outline=color, width=w)
    for k in range(8):
        ang = k*math.pi/4
        draw.line([(cx+math.cos(ang)*r*0.4,cy+math.sin(ang)*r*0.4),
                   (cx+math.cos(ang)*r*0.8,cy+math.sin(ang)*r*0.8)], fill=color, width=w)

CAMUNI = [camuno_orante, camuno_capanna, camuno_sole, camuno_cervo, camuno_rosa]


def scatter_camuni(draw, page_w, page_h, color=None, seed=0, n=3):
    """
    Sparge petroglifi camuni tenui nei margini, in modo che ogni pagina sia
    una piccola scoperta: poche marche (3-4), tipi/posizioni/dimensioni che
    variano col seed, sempre lontane dalla colonna di testo.
    """
    import random as _r
    if color is None:
        color = tint_color(INK_FAINT, 0.32)
    rng = _r.Random(seed)

    # zone candidate nei margini (sinistro e destro), lontane dal testo.
    # x molto vicino ai bordi; y distribuito su fasce diverse.
    left_x  = (0.045, 0.085)
    right_x = (0.915, 0.955)
    y_bands = [(0.12, 0.26), (0.30, 0.46), (0.50, 0.66), (0.70, 0.86), (0.88, 0.95)]

    rng.shuffle(y_bands)
    chosen = y_bands[:max(1, min(n, len(y_bands)))]

    motifs = CAMUNI[:]
    rng.shuffle(motifs)

    for i, (y0, y1) in enumerate(chosen):
        side = right_x if (i % 2 == 0) else left_x   # alterna lato
        # leggera casualità su lato per non creare colonne perfette
        if rng.random() < 0.3:
            side = left_x if side is right_x else right_x
        px = rng.uniform(*side) * page_w
        py = rng.uniform(y0, y1) * page_h
        fn = motifs[i % len(motifs)]
        sc = rng.randint(int(page_w*0.013), int(page_w*0.022))
        try:
            fn(draw, int(px), int(py), sc, color, max(2, page_w//600))
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════
# "NASCE DALLA PAGINA" — l'immagine affiora dalla carta senza stacco
# ═══════════════════════════════════════════════════════════════════════════
# Usato per la pagina-soglia "Qui entri nell'isola". L'immagine schiarisce
# come un acquerello sbiadito (mantenendo il colore) e si dissolve ai bordi
# con una maschera organica, così sembra nascere dalla pagina.

def _radial_mask(w, h, edge_softness=0.5, seed=0):
    """Maschera piena al centro, dissolta verso i bordi in modo organico."""
    import random as _r
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    pad_x = int(w * edge_softness * 0.5)
    pad_y = int(h * edge_softness * 0.5)
    d.ellipse([pad_x, pad_y, w - pad_x, h - pad_y], fill=255)
    _r.seed(seed)
    for _ in range(40):
        bx = _r.randint(0, w); by = _r.randint(0, h)
        br = _r.randint(int(w*0.04), int(w*0.12))
        d.ellipse([bx-br, by-br, bx+br, by+br], fill=_r.choice([255, 255, 0]))
    return m.filter(ImageFilter.GaussianBlur(int(w * 0.06)))


def nasce_dalla_pagina(illus, page_w, page_h, box, paper=PAPER,
                       fade=0.42, edge_softness=0.52, seed=0):
    """
    Compone `illus` dentro `box` su una pagina `paper` in modo che l'immagine
    sembri affiorare dalla carta: schiarisce mantenendo il colore (velo
    d'acquerello + saturazione ravvivata) e si dissolve ai bordi.
    Ritorna la pagina intera (page_w × page_h).
    """
    from PIL import ImageEnhance
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    iw, ih = illus.size
    scale = max(bw / iw, bh / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    illus = illus.resize((nw, nh), Image.LANCZOS)
    cx0 = (nw - bw) // 2; cy0 = (nh - bh) // 2
    illus = illus.crop((cx0, cy0, cx0 + bw, cy0 + bh))

    paper_layer = Image.new("RGB", illus.size, paper)
    faded = Image.blend(illus, paper_layer, fade)
    faded = ImageEnhance.Color(faded).enhance(1.25)

    omask = _radial_mask(bw, bh, edge_softness=edge_softness, seed=seed)
    page = Image.new("RGB", (page_w, page_h), paper)
    page.paste(faded, (x0, y0), omask)
    return page


if __name__ == "__main__":
    # Test: genera una tavola con palette, logo, font, decori
    W, H = 1200, 1600
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Logo
    logo = make_logo_image(200, SPIRALE)
    img.paste(logo, (W // 2 - 100, 60), logo)

    # Titolo collana
    f_mark = font("mark", 64)
    title = "L'Isola dei Tre Venti"
    w = d.textlength(title, font=f_mark)
    d.text((W // 2 - w / 2, 290), title, font=f_mark, fill=INK)

    # Sottotitolo
    f_sub = font("sans", 26)
    sub = "SPIRALE EDITRICE · COLLANA BAMBINI"
    w = d.textlength(sub, font=f_sub)
    d.text((W // 2 - w / 2, 380), sub, font=f_sub, fill=SPIRALE)

    # Palette swatches
    y = 480
    swatches = [
        ("Paper", PAPER), ("Ink", INK), ("Spirale", SPIRALE),
        ("Taglio", VENTO_TAGLIO), ("Intreccio", VENTO_INTRECCIO),
        ("Mulinello", VENTO_MULINELLO), ("Accent", ACCENT),
    ]
    x = 100
    for name, col in swatches:
        d.rounded_rectangle([x, y, x + 130, y + 130], radius=16, fill=col,
                            outline=INK_FAINT, width=1)
        d.text((x, y + 140), name, font=font("sans", 20), fill=INK)
        x += 155

    # Wind rule
    draw_wind_rule(d, 100, W - 100, 720, RULE, 2)

    # Font samples
    y = 780
    samples = [
        ("display", 52, "Fraunces — La Nebbia delle Montagne"),
        ("display_i", 36, "Fraunces Italic — un mattino d'inverno"),
        ("serif", 28, "Lora — corpo del testo narrativo, caldo e leggibile"),
        ("sans", 24, "Nunito — eyebrow, metadati, didascalie tonde"),
        ("mark", 44, "Fredoka — il marchio della collana"),
    ]
    for which, sz, txt in samples:
        d.text((100, y), txt, font=font(which, sz), fill=INK)
        y += sz + 30

    draw_dot_ornament(d, W // 2, y + 20, RULE)

    img.save("/home/claude/design_test.png")
    print("Design system test → /home/claude/design_test.png")


# ═══════════════════════════════════════════════════════════════════════════
# DECORI MARINI — vettoriali, stile glifo "disegnato a mano da bambino"
# ═══════════════════════════════════════════════════════════════════════════
# Usati nella doppia "Questa è l'isola" per legare la pagina-isola alla
# pagina-testo: il mare prosegue e si dissolve, con ondine, gabbiani,
# barchette, pesci. Niente PNG — solo linee curve leggere, come i glifi.

def mare_gradiente(w, h, color, verso="verticale", riflesso=0.0):
    """
    Tela mare w×h con gradiente morbido: in alto schiarito (riflesso del
    cielo), in basso il colore pieno. 'riflesso' (0..1) alza la luce in alto.
    Ritorna un'immagine RGB. Vettoriale (NumPy) per velocità.
    """
    from PIL import Image
    import numpy as np
    top = np.array([c + (255 - c) * (0.45 + 0.4*riflesso) for c in color[:3]])
    bot = np.array([c * 0.82 for c in color[:3]])
    t = np.linspace(0.0, 1.0, h)
    t = t*t*(3 - 2*t)                        # easing dolce
    col = (top[None, :] + (bot - top)[None, :] * t[:, None])  # (h,3)
    arr = np.repeat(col[:, None, :], w, axis=1).astype("uint8")  # (h,w,3)
    return Image.fromarray(arr, "RGB")


def onde(draw, x0, x1, y, color, width, ampiezza=None, passo=None, fase=0.0):
    """Una fila di ondine (~~~) leggere, come tratteggio dell'acqua."""
    import math
    span = x1 - x0
    amp = ampiezza if ampiezza is not None else max(3, span * 0.012)
    step = passo if passo is not None else max(8, span * 0.06)
    pts = []
    x = x0
    while x <= x1:
        pts.append((x, y + amp * math.sin((x - x0) / step * math.pi + fase)))
        x += max(2, step / 10)
    if len(pts) > 1:
        draw.line(pts, fill=color, width=width, joint="curve")


def gabbiano(draw, cx, cy, r, color, width):
    """Un gabbiano stilizzato: due archi a 'm' morbida (le ali in volo)."""
    draw.arc([cx - r, cy - r*0.5, cx, cy + r*0.5], 200, 340, fill=color, width=width)
    draw.arc([cx, cy - r*0.5, cx + r, cy + r*0.5], 200, 340, fill=color, width=width)


def barchetta(draw, cx, cy, r, color, width):
    """Barchetta stilizzata: scafo a mezzaluna + alberetto + vela triangolo."""
    # scafo
    draw.arc([cx - r, cy - r*0.35, cx + r, cy + r*0.7], 20, 160, fill=color, width=width)
    # albero
    draw.line([(cx, cy - r*0.9), (cx, cy + r*0.15)], fill=color, width=width)
    # vela (triangolo verso destra)
    draw.line([(cx, cy - r*0.85), (cx + r*0.7, cy), (cx, cy)],
              fill=color, width=width, joint="curve")


def pesce(draw, cx, cy, r, color, width):
    """Pesciolino: corpo a goccia (due archi) + codina a V."""
    draw.arc([cx - r, cy - r*0.5, cx + r*0.6, cy + r*0.5], 30, 330, fill=color, width=width)
    # coda
    draw.line([(cx - r, cy), (cx - r*1.4, cy - r*0.35)], fill=color, width=width)
    draw.line([(cx - r, cy), (cx - r*1.4, cy + r*0.35)], fill=color, width=width)


def pesciolino_bolla(draw, cx, cy, r, color, width):
    """Pesce + una bollicina sopra (vezzo da disegno di bambino)."""
    pesce(draw, cx, cy, r, color, width)
    draw.ellipse([cx + r*0.5, cy - r*0.9, cx + r*0.5 + r*0.18, cy - r*0.9 + r*0.18],
                 outline=color, width=max(1, width - 1))
