"""
test_canon.py — Test del canone normativo machine-readable (Branch A).

Tre livelli:
  1. il loader carica saga_config.yaml reale e i valori sono quelli attesi
  2. il loader è FAIL-LOUD su config assente/rotto/incompleto
  3. i consumatori (audit, writer) derivano DAVVERO dal canone: le loro
     costanti coincidono con il config — se qualcuno re-hardcoda, qui salta.

Esecuzione: python3 -m pytest tests/test_canon.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "scripts" / "audit"))

import saga_canon  # noqa: E402


# ---------------------------------------------------------------------------
# 1. caricamento reale
# ---------------------------------------------------------------------------

def test_canone_carica_e_valori_attesi():
    C = saga_canon.load(REPO)
    assert C.saga_id == "isola_tre_venti"
    assert C.story_ids == tuple(f"s{i:02d}" for i in range(1, 13))
    assert C.hooks.per_story == 10
    assert C.hooks.focal_action_max_words == 30
    assert "panorama" in C.hooks.types and len(C.hooks.types) == 7
    assert C.cornici.who_kinds == frozenset(
        {"gruppo", "nominato", "nominati", "anonimo"})
    assert C.paths.details_total == 20 and len(C.paths.tier_a) == 5
    assert C.lexicon.piano_family_saga_max == 6
    assert any(q.pattern == "si ricordò di" and q.only_stories == ("s11", "s12")
               for q in C.lexicon.quotas)


def test_regex_marker_compilate_matchano_esempi_reali():
    C = saga_canon.load(REPO)
    hook = ('<!-- @hook s01_h01 | @page 1 | @subhooks [s01_h01a, s01_h01b] '
            '| @image visual/x.jpg -->')
    m = C.markers.hook_re.search(hook)
    assert m and m.group(1) == "s01_h01" and m.group(3) == "s01_h01a, s01_h01b"
    sub = '<!-- @subhook s01_h01a | @page_book [4, 5] | @layout double_spread | @image TBD -->'
    m = C.markers.subhook_re.search(sub)
    assert m and m.group(1) == "s01_h01a" and m.group(2) == "[4, 5]"
    assert m.group(3) == "double_spread"


# ---------------------------------------------------------------------------
# 2. fail-loud
# ---------------------------------------------------------------------------

def test_config_assente_solleva_canon_error(tmp_path):
    with pytest.raises(saga_canon.CanonError):
        saga_canon.load(tmp_path)


def test_yaml_rotto_solleva_canon_error(tmp_path):
    (tmp_path / saga_canon.CONFIG_NAME).write_text("hooks: [unclosed",
                                                   encoding="utf-8")
    with pytest.raises(saga_canon.CanonError):
        saga_canon.load(tmp_path)


def test_chiave_mancante_indicata_nel_messaggio(tmp_path):
    # config minimale senza hooks.per_story → errore che NOMINA la chiave
    src = (REPO / saga_canon.CONFIG_NAME).read_text(encoding="utf-8")
    src = src.replace("  per_story: 10\n", "", 1)  # rimuove hooks.per_story
    (tmp_path / saga_canon.CONFIG_NAME).write_text(src, encoding="utf-8")
    with pytest.raises(saga_canon.CanonError, match="per_story"):
        saga_canon.load(tmp_path)


# ---------------------------------------------------------------------------
# 3. i consumatori derivano dal canone
# ---------------------------------------------------------------------------

def test_audit_derivano_dal_canone():
    C = saga_canon.load(REPO)
    import audit_1_integrity as a1
    import audit_2_schema as a2
    import audit_3_navigability as a3
    import audit_4_drift as a4

    assert a1.EXPECTED_SCHEMA == C.graph.expected_schema
    assert a1.EXPECTED_GRAPH == C.graph.expected_graph
    assert a2.VALID_TYPES == C.hooks.types
    assert a2.FOCAL_ACTION_MAX_WORDS == C.hooks.focal_action_max_words
    assert a2.EXPECTED_TIER_A_PATHS == C.paths.tier_a
    assert a2.WHO_KINDS == C.cornici.who_kinds
    assert a3.VALID_QUADRANTS == C.quadrants
    assert a4.PIANO_FAMILY_SAGA_MAX == C.lexicon.piano_family_saga_max
    assert a4.HOOK_MARKER_RE.pattern == C.markers.hook_re.pattern
    assert [q.pattern for q in C.lexicon.quotas] == [p for p, _, _ in a4.LEXICAL_QUOTAS]


def test_writer_deriva_dal_canone():
    C = saga_canon.load(REPO)
    import write_hooks_to_graph as w
    assert w.VALID_TYPES == C.hooks.types
    assert w.VALID_COMPOSITION_ZONES == C.hooks.composition_zones
    assert w.REQUIRED_FIELDS == C.hooks.required_fields
    assert w.FOCAL_ACTION_MAX_WORDS == C.hooks.focal_action_max_words
