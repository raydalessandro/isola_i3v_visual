"""
Test byline autore.

Il nome autore del libro (frontespizio + copyright) deve combaciare con quello
della copertina. Una divergenza era già successa (interno "Ray D'Alessandro" vs
copertina "Beatrice Mercuri"): questo test la blocca in `make check`.
"""
import importlib.util
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
import build_volume as bv  # noqa: E402


def _load_build_cover():
    spec = importlib.util.spec_from_file_location(
        "build_cover", SCRIPTS / "build_cover.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_byline_combacia_con_copertina():
    cover = _load_build_cover()
    assert bv.AUTHOR_BYLINE == cover.AUTHOR, (
        f"byline interno '{bv.AUTHOR_BYLINE}' != copertina '{cover.AUTHOR}'")


def test_nessun_vecchio_autore_nel_build():
    """Nessun residuo del vecchio byline nel codice di build del libro."""
    src = (SCRIPTS / "build_volume.py").read_text(encoding="utf-8")
    assert "D'Alessandro" not in src, "residuo 'D'Alessandro' in build_volume.py"


def test_frontespizio_usa_la_costante():
    """make_frontespizio deve disegnare AUTHOR_BYLINE (non un literal)."""
    src = (SCRIPTS / "build_volume.py").read_text(encoding="utf-8")
    assert "AUTHOR_BYLINE" in src
    assert bv.AUTHOR_BYLINE == "Beatrice Mercuri"
