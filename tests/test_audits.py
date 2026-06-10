"""
test_audits.py — Test degli audit di scripts/audit/ (blindatura 2026-06).

Due livelli:
  1. SMOKE — gli audit passano sulla repo corrente (subprocess, exit 0).
     Se la repo regredisce (grafo corrotto, prosa fuori quota, backup
     manomesso), questi test falliscono insieme alla CI.
  2. CORRUZIONE SINTETICA — le funzioni di check rilevano davvero gli
     errori che dichiarano di rilevare (dati minimi corrotti ad hoc).
     Proteggono i protettori: un refactor che spegne un controllo
     viene intercettato qui.

Esecuzione: python3 -m pytest tests/test_audits.py -q   (suite veloce)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
AUDIT_DIR = REPO / "scripts" / "audit"
sys.path.insert(0, str(AUDIT_DIR))

import audit_1_integrity as a1  # noqa: E402
import audit_2_schema as a2  # noqa: E402
import audit_3_navigability as a3  # noqa: E402
import audit_4_drift as a4  # noqa: E402


# ---------------------------------------------------------------------------
# helper
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _clear_module_errors():
    """Gli audit accumulano in liste a livello modulo: pulizia tra i test."""
    for mod in (a1, a2, a3, a4):
        if hasattr(mod, "errors"):
            mod.errors.clear()
        if hasattr(mod, "warnings"):
            mod.warnings.clear()
        if hasattr(mod, "infos"):
            mod.infos.clear()
    yield


def make_valid_hook(sid: str, i: int) -> dict:
    return {
        "hook_id": f"{sid}_h{i:02d}",
        "type": ["interno", "panorama", "azione", "dettaglio"][i % 4],
        "is_signature": False,
        "provenance": "extended_v2",
        "moment": "mattino",
        "location": {"id": "forno", "qualifier": None},
        "quadrant": "centro",
        "characters_present": ["gabriel"],
        "focal_action": "Gabriel entra nel forno",
        "focal_object": None,
        "atmosphere": "caldo di pane",
        "palette": "ocra e oro",
        "wind_visible": None,
        "composition_zone": "vignette",
    }


def make_valid_graph(sid: str = "s01") -> dict:
    return {
        "entities": {
            "locations": {"forno": {"quadrant": "centro"}},
            "characters": {"gabriel": {}},
            "objects": {"pagnotta_forno": {}},
            "winds": {"vento_taglio": {}},
        },
        "stories": {
            sid: {
                "visual_anchors": {
                    "scene_hooks": [make_valid_hook(sid, i) for i in range(1, 11)]
                }
            }
        },
    }


# ---------------------------------------------------------------------------
# 1. SMOKE — repo corrente
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("script", [
    "audit_1_integrity.py",
    "audit_2_schema.py",
    "audit_3_navigability.py",
    "audit_4_drift.py",
])
def test_smoke_audit_passa_su_repo(script):
    res = subprocess.run(
        [sys.executable, str(AUDIT_DIR / script)],
        capture_output=True, text=True, timeout=120,
    )
    assert res.returncode == 0, f"{script} FAIL:\n{res.stdout}\n{res.stderr}"


def test_smoke_runner_aggrega():
    res = subprocess.run(
        [sys.executable, str(AUDIT_DIR / "run_all_audits.py"), "--fast"],
        capture_output=True, text=True, timeout=180,
    )
    assert res.returncode == 0
    assert "ESITO: PASS" in res.stdout


# ---------------------------------------------------------------------------
# 2. audit_1 — chiavi duplicate + manifest
# ---------------------------------------------------------------------------

def test_a1_intercetta_chiavi_duplicate():
    tracker = a1._DupKeyTracker()
    json.loads('{"a": 1, "b": 2, "a": 3}', object_pairs_hook=tracker)
    assert tracker.duplicates == ["a"]


def test_a1_manifest_parse(tmp_path, monkeypatch):
    mf = tmp_path / "backup_manifest.sha256"
    mf.write_text("# commento\nabc123  story_graph.x.backup.json\n")
    monkeypatch.setattr(a1, "MANIFEST", mf)
    assert a1.load_manifest() == {"story_graph.x.backup.json": "abc123"}


# ---------------------------------------------------------------------------
# 2. audit_2 — corruzioni sintetiche sugli hook
# ---------------------------------------------------------------------------

def _run_a2_hooks(graph) -> list[str]:
    a2.errors.clear()
    a2.check_hooks("s01", graph["stories"]["s01"], graph)
    return list(a2.errors)


def test_a2_passa_su_storia_valida():
    assert _run_a2_hooks(make_valid_graph()) == []


def test_a2_fallisce_su_9_hook():
    g = make_valid_graph()
    g["stories"]["s01"]["visual_anchors"]["scene_hooks"].pop()
    errs = _run_a2_hooks(g)
    assert any("attesi 10 hook" in e for e in errs)


def test_a2_fallisce_su_type_fuori_enum():
    g = make_valid_graph()
    g["stories"]["s01"]["visual_anchors"]["scene_hooks"][0]["type"] = "epico"
    errs = _run_a2_hooks(g)
    assert any("non in enum" in e for e in errs)


def test_a2_fallisce_su_hook_fuori_sequenza():
    g = make_valid_graph()
    g["stories"]["s01"]["visual_anchors"]["scene_hooks"][4]["hook_id"] = "s01_h09"
    errs = _run_a2_hooks(g)
    assert any("fuori sequenza" in e for e in errs)


def test_a2_fallisce_su_focal_action_31_parole():
    g = make_valid_graph()
    g["stories"]["s01"]["visual_anchors"]["scene_hooks"][0]["focal_action"] = \
        "parola " * 31
    errs = _run_a2_hooks(g)
    assert any("> 30" in e for e in errs)


def test_a2_fallisce_su_4_signature():
    g = make_valid_graph()
    for h in g["stories"]["s01"]["visual_anchors"]["scene_hooks"][:4]:
        h["is_signature"] = True
    errs = _run_a2_hooks(g)
    assert any("signature 4 > 3" in e for e in errs)


def test_a2_fallisce_su_quadrant_incoerente():
    g = make_valid_graph()
    g["stories"]["s01"]["visual_anchors"]["scene_hooks"][0]["quadrant"] = "aria_nord"
    errs = _run_a2_hooks(g)
    assert any("quadrant" in e for e in errs)


# ---------------------------------------------------------------------------
# 3. audit_3 — estrazione id da forme miste
# ---------------------------------------------------------------------------

def test_a3_ids_of_forme_miste():
    assert a3.ids_of("forno") == ["forno"]
    assert a3.ids_of({"id": "forno", "role": "x"}) == ["forno"]
    assert a3.ids_of([{"id": "a"}, "b", {"ref": "c"}]) == ["a", "b", "c"]
    assert a3.ids_of(None) == []


# ---------------------------------------------------------------------------
# 4. audit_4 — lessico bandito + marker
# ---------------------------------------------------------------------------

STORY_HEADER = """---
sid: s99
title: Storia di Test
slug: storia_di_test
cycle: A
total_pages: 10
total_hooks: 10
status: test
---

# S99 — Storia di Test

"""


def _hook_block(sid: str, i: int, text: str = "Prosa neutra di prova.") -> str:
    return (f"## Pagina {i}\n\n"
            f"<!-- @hook {sid}_h{i:02d} | @page {i} | "
            f"@subhooks [] | @image TBD -->\n\n{text}\n\n---\n\n")


def _write_story(tmp_path: Path, sid: str, body: str) -> Path:
    f = tmp_path / f"{sid}_storia_di_test.md"
    f.write_text(STORY_HEADER.replace("s99", sid) + body, encoding="utf-8")
    return f


def _run_a4(tmp_path: Path, sid: str, body: str,
            graph_hooks: list[str] | None = None) -> list[str]:
    a4.errors.clear()
    a4.infos.clear()
    f = _write_story(tmp_path, sid, body)
    hooks = graph_hooks if graph_hooks is not None \
        else [f"{sid}_h{i:02d}" for i in range(1, 11)]
    a4.check_story(sid, f, hooks, saga_counts={})
    return list(a4.errors)


def test_a4_passa_su_storia_pulita(tmp_path):
    body = "".join(_hook_block("s99", i) for i in range(1, 11))
    assert _run_a4(tmp_path, "s99", body) == []


def test_a4_fallisce_su_piano_piano_x2(tmp_path):
    body = "".join(_hook_block("s99", i) for i in range(1, 11))
    body += "\nCamminava piano piano. Poi ancora piano piano.\n"
    errs = _run_a4(tmp_path, "s99", body)
    assert any("piano piano" in e and "max 1" in e for e in errs)


def test_a4_fallisce_su_pattern_a_quota_zero(tmp_path):
    body = "".join(_hook_block("s99", i) for i in range(1, 11))
    body += "\nGuardò il cielo e parlò.\n"
    errs = _run_a4(tmp_path, "s99", body)
    assert any("guardò il cielo" in e for e in errs)


def test_a4_si_ricordo_di_solo_s11_s12(tmp_path):
    body = "".join(_hook_block("s99", i) for i in range(1, 11))
    body += "\nSi ricordò di quel giorno.\n"
    errs = _run_a4(tmp_path, "s99", body)
    assert any("si ricordò di" in e for e in errs)
    # in s11 invece è ammesso (1 occorrenza)
    body11 = body.replace("s99", "s11")
    errs11 = _run_a4(tmp_path, "s11", body11)
    assert not any("si ricordò di" in e for e in errs11)


def test_a4_fallisce_su_9_marker_hook(tmp_path):
    body = "".join(_hook_block("s99", i) for i in range(1, 10))  # solo 9
    errs = _run_a4(tmp_path, "s99", body)
    assert any("@hook" in e for e in errs)


def test_a4_fallisce_su_hook_prosa_diverso_da_grafo(tmp_path):
    body = "".join(_hook_block("s99", i) for i in range(1, 11))
    graph_hooks = [f"s99_h{i:02d}" for i in range(1, 11)]
    graph_hooks[-1] = "s99_h99"  # il grafo dichiara un id diverso
    errs = _run_a4(tmp_path, "s99", body, graph_hooks=graph_hooks)
    assert any("hook prosa ≠ hook grafo" in e for e in errs)


def test_a4_ignora_marker_di_esempio_nel_frontmatter(tmp_path):
    """Il frontmatter schema_marker contiene esempi <!-- @hook ... -->:
    non devono essere contati come marker reali."""
    header = STORY_HEADER.replace(
        "---\n\n# S99",
        'schema_marker: |\n  <!-- @hook sNN_hMM | @page MM | '
        '@subhooks [x] | @image TBD -->\n---\n\n# S99'
    )
    body = "".join(_hook_block("s99", i) for i in range(1, 11))
    f = tmp_path / "s99_storia_di_test.md"
    f.write_text(header + body, encoding="utf-8")
    a4.errors.clear()
    a4.check_story("s99", f, [f"s99_h{i:02d}" for i in range(1, 11)], {})
    assert a4.errors == []


def test_a4_page_book_values():
    assert a4.page_book_values("7") == [7]
    assert a4.page_book_values("[4, 5]") == [4, 5]


def test_a4_apparato_subhook_incompleto_fallisce(tmp_path):
    """Se l'apparato subhook è iniziato, deve essere coerente:
    book_pages_total dichiarato ma copertura pagine incompleta → errore."""
    header = STORY_HEADER.replace("status: test",
                                  "status: test\nbook_pages_total: 3")
    body = "".join(_hook_block("s99", i) for i in range(1, 11))
    body += ('<!-- @subhook s99_h01a | @page_book 1 | @image TBD -->\n'
             'Prosa pagina uno.\n')
    # dichiaro il subhook nel marker @hook 1
    body = body.replace("@subhooks [] | @image TBD -->\n\nProsa neutra",
                        "@subhooks [s99_h01a] | @image TBD -->\n\nProsa neutra", 1)
    f = tmp_path / "s99_storia_di_test.md"
    f.write_text(header + body, encoding="utf-8")
    a4.errors.clear()
    a4.check_story("s99", f, [f"s99_h{i:02d}" for i in range(1, 11)], {})
    assert any("@page_book non copre 1..3" in e for e in a4.errors)
