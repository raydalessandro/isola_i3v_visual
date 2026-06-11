"""
test_timeline_worldstate.py — Test della Branch B (audit_5 + stato del mondo).

Livelli:
  1. SMOKE — audit_5 passa sul grafo reale; il runner include 5 audit.
  2. CORRUZIONE SINTETICA — le regole temporali rilevano davvero le
     violazioni che dichiarano (fioritura prima dell'origine, callback non
     dopo, incroci storia↔seme incoerenti, sid fantasma nel quote_tracker).
  3. STATO DEL MONDO — la proiezione del brieffer è corretta su fatti noti
     del grafo reale (s01 vergine; bastoncino target in s02 e chiuso in s07;
     debutti s07) e su un mini-grafo sintetico.

Esecuzione: python3 -m pytest tests/test_timeline_worldstate.py -q
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts" / "audit"))

import audit_5_timeline as a5  # noqa: E402
import build_writing_brief as bwb  # noqa: E402


@pytest.fixture(autouse=True)
def _clear():
    a5.errors.clear()
    a5.warnings.clear()
    yield


def mini_graph() -> dict:
    return {
        "stories": {
            "s01": {"seeds_planted": ["seed_x"], "callbacks_made": []},
            "s02": {"seeds_bloomed_here": ["seed_x"],
                    "callbacks_made": ["cb_1"]},
        },
        "seeds": {
            "seed_x": {"origin_story": "s01", "status": "bloomed",
                       "bloomed_in_story": "s02",
                       "bloom_target_stories": ["s02"]},
        },
        "callbacks": {
            "cb_1": {"from_story": "s01", "registered_in_story": "s02"},
        },
        "quote_tracker": {"refrain": ["s01", "s02"]},
    }


# ---------------------------------------------------------------------------
# 1. smoke
# ---------------------------------------------------------------------------

def test_smoke_audit5_passa_su_repo():
    res = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "audit" / "audit_5_timeline.py")],
        capture_output=True, text=True, timeout=120)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "PASS" in res.stdout


def test_runner_include_cinque_audit():
    res = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "audit" / "run_all_audits.py"),
         "--fast"],
        capture_output=True, text=True, timeout=180)
    assert res.returncode == 0
    assert "audit_5_timeline.py" in res.stdout
    assert "audit_4_drift.py" not in res.stdout  # --fast salta solo la prosa


# ---------------------------------------------------------------------------
# 2. corruzioni sintetiche
# ---------------------------------------------------------------------------

def test_mini_grafo_valido_passa():
    g = mini_graph()
    a5.check_seeds(g)
    a5.check_story_seed_cross(g)
    a5.check_callbacks(g)
    a5.check_quote_tracker(g)
    assert a5.errors == []


def test_fioritura_prima_origine():
    g = mini_graph()
    g["seeds"]["seed_x"]["origin_story"] = "s02"
    g["seeds"]["seed_x"]["bloomed_in_story"] = "s01"
    a5.check_seeds(g)
    assert any("PRIMA dell'origine" in m for _, _, _, m in a5.errors)


def test_bloomed_senza_story():
    g = mini_graph()
    del g["seeds"]["seed_x"]["bloomed_in_story"]
    a5.check_seeds(g)
    assert any("senza bloomed_in_story" in m for _, _, _, m in a5.errors)


def test_evento_effettivo_prima_origine():
    g = mini_graph()
    g["seeds"]["seed_x"]["origin_story"] = "s02"
    g["seeds"]["seed_x"]["bloomed_in_story"] = "s02"
    g["seeds"]["seed_x"]["pickup_history"] = [{"story": "s01"}]
    a5.check_seeds(g)
    assert any("pickup_history" in m and "PRIMA" in m
               for _, _, _, m in a5.errors)


def test_callback_non_dopo_origine():
    g = mini_graph()
    g["callbacks"]["cb_1"]["from_story"] = "s02"
    a5.check_callbacks(g)
    assert any("NON DOPO" in m for _, _, _, m in a5.errors)


def test_planted_mismatch():
    g = mini_graph()
    g["seeds"]["seed_x"]["origin_story"] = "s02"
    a5.check_story_seed_cross(g)
    assert any("seeds_planted" in m for _, _, _, m in a5.errors)


def test_quote_tracker_sid_fantasma():
    g = mini_graph()
    g["quote_tracker"]["refrain"].append("s99")
    a5.check_quote_tracker(g)
    assert any("s99" in m for _, _, _, m in a5.errors)


def test_bloom_fuori_target_e_solo_warning():
    g = mini_graph()
    g["seeds"]["seed_x"]["bloom_target_stories"] = ["s03"]
    g["stories"]["s03"] = {}
    a5.check_seeds(g)
    assert a5.errors == []
    assert any("deviazione dal piano" in w for w in a5.warnings)


# ---------------------------------------------------------------------------
# 3. stato del mondo
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def real_graph():
    return bwb.load_graph(REPO)


def test_s01_mondo_vergine(real_graph):
    out = bwb.build_stato_mondo(real_graph, "s01")
    assert "Mondo vergine" in out
    assert "DEBUTTI" not in out


def test_s02_bastoncino_target_qui(real_graph):
    out = bwb.build_stato_mondo(real_graph, "s02")
    # il bastoncino di Noah: piantato s01, target e fioritura s02
    assert "seed_s01_bastoncino_noah" in out
    assert "TARGET FIORITURA: QUI" in out


def test_s07_bastoncino_chiuso_e_debutti(real_graph):
    out = bwb.build_stato_mondo(real_graph, "s07")
    assert "GIÀ FIORITI" in out and "seed_s01_bastoncino_noah" in out
    assert "DEBUTTI" in out and "bartolo" in out
    # i fratelli non sono debutti in s07
    sezione_debutti = out.split("DEBUTTI")[1].split("\n")[0]
    assert "gabriel" not in sezione_debutti


def test_sezione_inserita_nel_brief(real_graph):
    brief = bwb.build_brief(REPO, "s03")
    assert "STATO DEL MONDO ALL'INIZIO DI S03" in brief
    # posizionata dopo il core e prima della narrazione fattuale
    assert brief.index("CORE NARRATIVO") < brief.index("STATO DEL MONDO") \
        < brief.index("NARRAZIONE FATTUALE")
