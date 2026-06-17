"""
Test collocazione immagini del FRONT MATTER Vol.1.

Guard contro lo scambio (già successo una volta) di:
  - pagina 2 (occhiello copertina)  → copertina personaggi SENZA testo
  - "Ecco l'isola" / stato zero      → veduta NOTTURNA
  - "Questa è l'isola" / atlante      → mappa isola di GIORNO (pulita, no titolo)

Girano in `make check` PRIMA del build del PDF. La fonte di verità è
`FRONTMATTER_ISOLA` + `_occhiello_cover_path()` in build_volume.py: cambiando lì
le sorgenti, questi test segnalano subito se notte/giorno/copertina finiscono
nel posto sbagliato.
"""
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageStat

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_volume as bv  # noqa: E402


def _lum(path):
    return ImageStat.Stat(
        Image.open(path).convert("L").resize((128, 128))).mean[0] / 255.0


@pytest.fixture
def night():
    return bv.FRONTMATTER_ISOLA["stato_zero"]


@pytest.fixture
def day():
    return bv.FRONTMATTER_ISOLA["atlante_questa_isola"]


@pytest.fixture
def cover():
    return bv._occhiello_cover_path()


def test_sorgenti_esistono(night, day, cover):
    assert night.exists(), f"immagine notte mancante: {night}"
    assert day.exists(), f"immagine giorno mancante: {day}"
    assert cover is not None and cover.exists(), "copertina pagina-2 non risolta"


def test_eccoisola_e_notturna(night):
    """'Ecco l'isola' (stato zero) deve essere una veduta NOTTURNA (scura)."""
    assert _lum(night) < 0.30, (
        f"'Ecco l'isola' usa {night.name} (lum {_lum(night):.2f}): non è notturna")


def test_questaisola_e_diurna(day):
    """'Questa è l'isola' (atlante) deve essere la mappa di GIORNO (chiara)."""
    assert _lum(day) > 0.35, (
        f"'Questa è l'isola' usa {day.name} (lum {_lum(day):.2f}): non è diurna")


def test_notte_piu_scura_del_giorno(night, day):
    """Guard diretto allo SCAMBIO notte↔giorno tra i due spread."""
    ln, lg = _lum(night), _lum(day)
    assert ln < lg - 0.15, (
        f"notte/giorno forse scambiate: notte={night.name}({ln:.2f}) "
        f"giorno={day.name}({lg:.2f})")


def test_pag2_e_copertina_senza_testo(cover, night, day):
    """Pagina 2 = copertina personaggi SENZA testo, non una mappa-isola né una
    cover col titolo impresso."""
    name = cover.name.lower()
    assert ("notxt" in name or "clean" in name), (
        f"pagina-2 non usa una cover senza testo: {cover.name}")
    assert "candidate_v2" not in name, (
        f"pagina-2 usa la cover col titolo impresso: {cover.name}")
    assert cover != night and cover != day, (
        "pagina-2 usa una delle immagini-isola invece della copertina")


def test_atlante_non_usa_mappa_titolata(day):
    """La mappa-giorno dell'atlante deve essere la versione pulita: se fosse la
    candidate_v2 (titolo 'L'Isola dei Tre Venti' impresso) si avrebbe doppio
    titolo sopra il 'Questa è l'isola' dell'atlante."""
    assert "candidate_v2" not in day.name, (
        f"atlante usa la mappa col titolo impresso: {day.name}")


def test_tre_slot_distinti(cover, night, day):
    paths = {cover.resolve(), night.resolve(), day.resolve()}
    assert len(paths) == 3, "due slot del front matter puntano alla stessa immagine"


def test_wiring_pag2_render_non_e_notte():
    """Wiring: la pagina-2 renderizzata NON deve essere l'immagine notturna
    (catch se make_occhiello_copertina venisse ricablato sulla notte)."""
    page = bv.make_occhiello_copertina()
    lum = ImageStat.Stat(page.convert("L")).mean[0] / 255.0
    assert lum > 0.50, f"pagina-2 renderizzata troppo scura (lum {lum:.2f}): è la notte?"


def test_guard_prebuild_rileva_scambio(monkeypatch):
    """Il guard pre-build deve segnalare uno scambio notte↔giorno."""
    assert bv.validate_frontmatter_isola(log_warn=False) == []
    swapped = {
        "stato_zero": bv.FRONTMATTER_ISOLA["atlante_questa_isola"],
        "atlante_questa_isola": bv.FRONTMATTER_ISOLA["stato_zero"],
    }
    monkeypatch.setattr(bv, "FRONTMATTER_ISOLA", swapped)
    assert len(bv.validate_frontmatter_isola(log_warn=False)) >= 1
