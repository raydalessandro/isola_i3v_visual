#!/usr/bin/env python3
"""
Suite di test per lo script di impaginazione de "L'Isola dei Tre Venti".
Blinda le invarianti che devono valere identiche su tutti e 4 i volumi.

Esecuzione:
    pip install pytest Pillow reportlab pymupdf --break-system-packages
    cd <repo> && python3 -m pytest tests/ -v

Livelli:
  1. Import e struttura       — moduli, costanti, firme
  2. Robustezza dei dati      — input difficili non fanno crashare il rendering
  3. Invarianti di stampa     — A5 esatto, 300 DPI, pagine pari, immagini valide
  4. Coerenza sui 4 volumi    — metadati, indice, colori-quartiere, decori
  5. Determinismo            — stesso input → stesso output
"""
import sys
import importlib.util
from pathlib import Path

import pytest
from PIL import Image

# ── Caricamento moduli sotto test ───────────────────────────────────────────
REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def ds():
    return _load("design_system", SCRIPTS / "design_system.py")


@pytest.fixture(scope="session")
def bv():
    return _load("build_volume", SCRIPTS / "build_volume.py")


# Pagina di test bianca su cui disegnare
@pytest.fixture
def canvas_draw():
    from PIL import ImageDraw
    img = Image.new("RGB", (1748, 2480), (250, 247, 240))
    return img, ImageDraw.Draw(img)


# ═══════════════════════════════════════════════════════════════════════════
# 1. IMPORT E STRUTTURA
# ═══════════════════════════════════════════════════════════════════════════
class TestStruttura:
    def test_design_system_importa(self, ds):
        assert ds is not None

    def test_build_volume_importa(self, bv):
        assert bv is not None

    def test_palette_presente(self, ds):
        for nome in ["PAPER", "INK", "SPIRALE", "VENTO_TAGLIO",
                     "VENTO_INTRECCIO", "VENTO_MULINELLO", "ACCENT", "RULE"]:
            col = getattr(ds, nome)
            assert isinstance(col, tuple) and len(col) == 3
            assert all(0 <= c <= 255 for c in col)

    def test_quartiere_color_completo(self, ds):
        attesi = {"fuoco", "acqua", "aria", "terra", "centro", "perimetro"}
        assert attesi <= set(ds.QUARTIERE_COLOR.keys())
        for col in ds.QUARTIERE_COLOR.values():
            assert isinstance(col, tuple) and len(col) == 3

    def test_glifi_vento_presenti(self, ds):
        assert set(ds.GLIFO_VENTO.keys()) == {"Δ", "⇄", "⟳"}
        for fn in ds.GLIFO_VENTO.values():
            assert callable(fn)

    def test_cornici_presenti(self, ds):
        for nome in ["doppio_filetto", "angoli_vento", "festone", "grappolo"]:
            assert nome in ds.CORNICI
            assert callable(ds.CORNICI[nome])

    def test_camuni_presenti(self, ds):
        assert len(ds.CAMUNI) >= 5
        for fn in ds.CAMUNI:
            assert callable(fn)

    def test_dimensioni_stampa(self, bv):
        # A5 a 300 DPI
        assert bv.TX_W == 1748
        assert bv.TX_H == 2480
        assert bv.DPI == 300
        assert bv.BLEED_PX > 0
        assert bv.IMG_W > bv.TX_W   # immagini includono il bleed
        assert bv.IMG_H > bv.TX_H

    def test_volume_config_quattro_volumi(self, bv):
        assert set(bv.VOLUME_CONFIG.keys()) == {1, 2, 3, 4}
        for v, cfg in bv.VOLUME_CONFIG.items():
            assert "ciclo" in cfg and "storie" in cfg and "vol_id" in cfg
            assert len(cfg["storie"]) == 3

    def test_dodici_storie_totali(self, bv):
        tutte = [s for cfg in bv.VOLUME_CONFIG.values() for s in cfg["storie"]]
        assert len(tutte) == 12
        assert len(set(tutte)) == 12   # nessun duplicato
        assert tutte == [f"s{i:02d}" for i in range(1, 13)]


# ═══════════════════════════════════════════════════════════════════════════
# 2. ROBUSTEZZA DEI DATI — input difficili non devono far crashare
# ═══════════════════════════════════════════════════════════════════════════
class TestRobustezza:
    def test_title_to_slug_casi(self, bv):
        assert bv._title_to_slug("Mèmolo e Pun") == "memolo_pun"
        assert bv._title_to_slug("Rovo e Bru") == "rovo_bru"
        assert bv._title_to_slug("Fiamma") == "fiamma"
        # non deve crashare su input strani
        assert isinstance(bv._title_to_slug(""), str)
        assert isinstance(bv._title_to_slug("123 !!! ò"), str)

    def test_clean_prose_rimuove_markup(self, bv):
        sporco = "# Titolo\n**grassetto** e *corsivo*\n<!-- commento -->\n> citazione\ntesto vero."
        pulito = bv.clean_prose(sporco)
        assert "**" not in pulito
        assert "<!--" not in pulito
        assert "# " not in pulito
        assert "testo vero." in pulito

    def test_clean_prose_vuoto(self, bv):
        assert bv.clean_prose("") == ""
        assert bv.clean_prose("\n\n\n") == ""

    def test_word_wrap_non_crasha(self, bv):
        from PIL import ImageDraw
        f = bv.fnt(bv.FS_BODY)
        d = ImageDraw.Draw(Image.new("RGB", (100, 100)))
        assert bv.word_wrap("", f, 500, d) == [] or bv.word_wrap("", f, 500, d) == [""]
        # parola più lunga della riga non deve loopare all'infinito
        lunga = "a" * 200
        out = bv.word_wrap(lunga, f, 500, d)
        assert isinstance(out, list)

    def test_presentazione_immagine_mancante(self, bv):
        # immagine None → pagina generata lo stesso, niente crash
        warns = []
        img = bv.make_presentazione_page(
            "Fiamma", "Testo breve di prova.", None,
            volume=1, kind="personaggio", layout_warnings=warns)
        assert img.size == (bv.TX_W, bv.TX_H)

    def test_presentazione_immagine_inesistente(self, bv):
        warns = []
        img = bv.make_presentazione_page(
            "Fiamma", "Testo.", Path("/non/esiste.jpg"),
            volume=1, kind="personaggio", layout_warnings=warns)
        assert img.size == (bv.TX_W, bv.TX_H)

    def test_presentazione_testo_lunghissimo(self, bv):
        # testo molto lungo → overflow gestito, warning emesso, niente crash
        warns = []
        testo = ("Frase di prova molto lunga. " * 80)
        img = bv.make_presentazione_page(
            "Grunto", testo, None, volume=1, kind="personaggio",
            layout_warnings=warns)
        assert img.size == (bv.TX_W, bv.TX_H)
        # deve aver segnalato il troncamento
        assert any(w.get("entry") == "Grunto" for w in warns)

    def test_presentazione_testo_minimo(self, bv):
        warns = []
        img = bv.make_presentazione_page(
            "Amo", "A.", None, volume=1, kind="personaggio",
            layout_warnings=warns)
        assert img.size == (bv.TX_W, bv.TX_H)

    def test_text_pages_vuoto(self, bv):
        pagine = bv.make_text_pages("", title="Prova")
        assert len(pagine) >= 1
        assert all(p.size == (bv.TX_W, bv.TX_H) for p in pagine)

    def test_text_pages_lungo_pagina(self, bv):
        # testo lungo deve impaginarsi su più pagine, tutte valide
        testo = "Una frase media che riempie spazio. " * 200
        pagine = bv.make_text_pages(testo, title="Lungo")
        assert len(pagine) >= 2
        assert all(p.size == (bv.TX_W, bv.TX_H) for p in pagine)


# ═══════════════════════════════════════════════════════════════════════════
# 3. DECORI E COLORI — disegno vettoriale non crasha, colori coerenti
# ═══════════════════════════════════════════════════════════════════════════
class TestDecori:
    def test_tutti_i_camuni_disegnano(self, ds, canvas_draw):
        img, d = canvas_draw
        for fn in ds.CAMUNI:
            fn(d, 800, 800, 60, ds.INK_SOFT, 4)   # non deve sollevare

    def test_tutte_le_cornici_disegnano(self, ds, canvas_draw):
        img, d = canvas_draw
        box = (200, 200, 1200, 1600)
        for nome, fn in ds.CORNICI.items():
            fn(d, box, ds.ACCENT, 5, 40)

    def test_glifi_disegnano(self, ds, canvas_draw):
        img, d = canvas_draw
        for fn in ds.GLIFO_VENTO.values():
            fn(d, 800, 800, 60, ds.VENTO_TAGLIO, 5)

    def test_decori_anima(self, ds, canvas_draw):
        img, d = canvas_draw
        ds.rosa_tre_venti(d, 800, 800, 120, 5)
        ds.isola_stilizzata(d, 800, 800, 200, ds.INK_SOFT)
        ds.separatore_camuno(d, 200, 1200, 800, ds.ACCENT, 4)
        ds.scatter_camuni(d, 1748, 2480, seed=1)

    def test_nasce_dalla_pagina(self, ds):
        # motore immagine-da-pagina: input sintetico
        illus = Image.new("RGB", (800, 1200), (120, 100, 80))
        out = ds.nasce_dalla_pagina(illus, 1748, 2480,
                                    (0, 200, 1748, 1700), ds.PAPER)
        assert out.size == (1748, 2480)

    def test_quartiere_color_per_personaggio(self, bv, ds):
        # Fiamma → fuoco (ambra) ; Rovo → terra
        assert bv._quartiere_color_for("Fiamma") == ds.QUARTIERE_COLOR["fuoco"]
        assert bv._quartiere_color_for("Rovo e Bru") == ds.QUARTIERE_COLOR["terra"]
        # voce sconosciuta → colore di default, niente crash
        assert bv._quartiere_color_for("Sconosciuto") == ds.DEFAULT_QUARTIERE_COLOR


# ═══════════════════════════════════════════════════════════════════════════
# 4. COERENZA SUI 4 VOLUMI — front matter, occhielli, indice per ogni volume
# ═══════════════════════════════════════════════════════════════════════════
class TestQuattroVolumi:
    @pytest.mark.parametrize("vol", [1, 2, 3, 4])
    def test_frontespizio(self, bv, vol):
        img = bv.make_frontespizio(vol)
        assert img.size == (bv.TX_W, bv.TX_H)

    @pytest.mark.parametrize("vol", [1, 2, 3, 4])
    def test_colophon(self, bv, vol):
        img = bv.make_colophon(vol)
        assert img.size == (bv.TX_W, bv.TX_H)

    @pytest.mark.parametrize("vol", [1, 2, 3, 4])
    def test_occhielli(self, bv, vol):
        assert bv.make_occhiello_prima_di_leggere().size == (bv.TX_W, bv.TX_H)
        assert bv.make_occhiello_abitanti().size == (bv.TX_W, bv.TX_H)
        assert bv.make_occhiello_porte(vol).size == (bv.TX_W, bv.TX_H)

    @pytest.mark.parametrize("vol", [1, 2, 3, 4])
    def test_occhiello_storia(self, bv, vol):
        storie = bv.VOLUME_CONFIG[vol]["storie"]
        img = bv.make_occhiello_storia(1, "Titolo Di Prova", vol)
        assert img.size == (bv.TX_W, bv.TX_H)

    @pytest.mark.parametrize("vol", [1, 2, 3, 4])
    def test_indice_si_costruisce(self, bv, vol):
        storie = bv.VOLUME_CONFIG[vol]["storie"]
        voci = bv.build_indice_voci(vol, storie, "dopo")
        assert len(voci) >= 5   # prima di leggere, isola dorme, storie, abitanti, porte, sigillo
        img = bv.make_indice(vol, voci)
        assert img.size == (bv.TX_W, bv.TX_H)

    @pytest.mark.parametrize("vol", [1, 2, 3, 4])
    def test_indice_numerato(self, bv, vol):
        storie = bv.VOLUME_CONFIG[vol]["storie"]
        marks = {"prima_di_leggere": 6, "isola_dorme": 12, "storia_1": 16,
                 "storia_2": 30, "storia_3": 44, "abitanti": 50,
                 "porte": 60, "sigillo": 66, "congedo": 66}
        voci = bv.build_indice_voci_numerate(vol, storie, "dopo", marks)
        # le voci con mark devono avere un numero di pagina
        nums = [n for _, _, n, _ in voci if n is not None]
        assert len(nums) >= 4

    def test_soglia_ingresso(self, bv):
        img = bv.make_soglia_ingresso("L'isola dorme")
        assert img.size == (bv.TX_W, bv.TX_H)


# ═══════════════════════════════════════════════════════════════════════════
# 5. DETERMINISMO — stesso input → stesso output (byte identici)
# ═══════════════════════════════════════════════════════════════════════════
class TestDeterminismo:
    def test_presentazione_deterministica(self, bv):
        a = bv.make_presentazione_page("Fiamma", "Testo di prova.", None,
                                       volume=1, kind="personaggio")
        b = bv.make_presentazione_page("Fiamma", "Testo di prova.", None,
                                       volume=1, kind="personaggio")
        assert a.tobytes() == b.tobytes()

    def test_scatter_camuni_deterministico(self, ds):
        from PIL import ImageDraw
        def render():
            img = Image.new("RGB", (1748, 2480), ds.PAPER)
            ds.scatter_camuni(ImageDraw.Draw(img), 1748, 2480, seed=42)
            return img.tobytes()
        assert render() == render()

    def test_frontespizio_deterministico(self, bv):
        assert bv.make_frontespizio(1).tobytes() == bv.make_frontespizio(1).tobytes()
