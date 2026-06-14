"""
Test spread orizzontali (build_volume.py).

Copre il TODO docs/TODO_BUILD_VOLUME_SPREAD_HORIZONTAL.md:
  - il parser riconosce @page_book [N, N+1] CON spazio (regex);
  - i subhook @layout double_spread diventano un tuple ('spread', img);
  - il canvas spread è continuo (IMG_W*2 + gutter) × IMG_H;
  - lo split a metà produce 2 facciate A5 esatte (IMG_W × IMG_H ciascuna);
  - lo spread conta 2 facciate (parità recto/verso);
  - il testo è sovrapposto SOLO sulla metà sinistra.
"""
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageStat

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_volume as bv  # noqa: E402


SPREAD_SUBHOOKS = {"s01": "s01_h07a", "s02": "s02_h05a"}


@pytest.mark.parametrize("sid,expected", SPREAD_SUBHOOKS.items())
def test_parser_riconosce_spread_con_spazio(sid, expected):
    """La regex page_book deve gestire '[N, N+1]' con lo spazio."""
    shs = bv.parse_story_md(sid)
    spread = [s for s in shs if s["subhook_id"] == expected]
    assert spread, f"{expected} non parsato (regex page_book rotta?)"
    sh = spread[0]
    assert isinstance(sh["page_book"], list) and len(sh["page_book"]) == 2
    assert sh["layout"] == "double_spread"
    assert sh["image_path"] is not None, "immagine landscape non risolta"


@pytest.mark.parametrize("sid", SPREAD_SUBHOOKS)
def test_story_pages_ha_esattamente_uno_spread(sid):
    pages = bv.build_story_pages(sid)
    spreads = [p for p in pages if p[0] == "spread"]
    assert len(spreads) == 1, f"{sid}: atteso 1 spread, trovati {len(spreads)}"


@pytest.mark.parametrize("sid", SPREAD_SUBHOOKS)
def test_dimensioni_spread_e_split(sid):
    pages = bv.build_story_pages(sid)
    _, img = next(p for p in pages if p[0] == "spread")
    sw = bv.IMG_W * 2 + bv.SCALE * 4
    assert img.size == (sw, bv.IMG_H), "canvas spread di larghezza errata"
    # split a metà come fa build_stampa_pdf (cade a IMG_W + mezzo-gutter)
    half = img.width // 2
    assert half == bv.IMG_W + bv.SCALE * 2, "taglio centrale fuori dalla piega"
    left = img.crop((0, 0, half, img.height))
    right = img.crop((half, 0, img.width, img.height))
    assert left.size == (half, bv.IMG_H)
    assert right.size == (img.width - half, bv.IMG_H)


@pytest.mark.parametrize("sid", SPREAD_SUBHOOKS)
def test_facciate_spread_vale_due(sid):
    pages = bv.build_story_pages(sid)
    # 16 single + 1 spread => 18 facciate (parità => recto ok)
    assert bv._facciate(pages) == 18
    assert bv._facciate(pages) % 2 == 0


@pytest.mark.parametrize("sid", SPREAD_SUBHOOKS)
def test_testo_solo_a_sinistra(sid):
    """Confronta spread con testo vs senza: la differenza dei pixel deve
    concentrarsi nella metà sinistra (testo + schiarita DODGE), non a destra."""
    sh = next(s for s in bv.parse_story_md(sid)
              if s["subhook_id"] == SPREAD_SUBHOOKS[sid])
    _, img = bv.compose_spread_horizontal(sh["image_path"], sh["text"])
    _, plain = bv.compose_spread_horizontal(sh["image_path"], "")
    half = img.width // 2

    def mean_abs_diff(box):
        a = img.crop(box).convert("L")
        b = plain.crop(box).convert("L")
        from PIL import ImageChops
        return ImageStat.Stat(ImageChops.difference(a, b)).mean[0]

    d_left = mean_abs_diff((0, 0, half, img.height))
    d_right = mean_abs_diff((half, 0, img.width, img.height))
    assert d_left > 1.0, "nessun testo rilevato sulla pagina sinistra"
    assert d_right < 0.05, "la pagina destra è stata alterata (testo sconfinato)"
