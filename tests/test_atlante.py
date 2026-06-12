#!/usr/bin/env python3
"""
Suite di test per l'Atlante degli Abitanti a tavole naturalistiche.
Blinda le invarianti di visual/atlante/ATLANTE_SPEC.json e del rendering
make_atlante_plate_page in scripts/build_volume.py.

Esecuzione:
    cd <repo> && python3 -m pytest tests/test_atlante.py -v

Livelli:
  1. Spec            — JSON valido, schema uniforme, zone sane
  2. Copertura       — ogni voce della presentazione parziale ha una voce spec
  3. Ritmo           — mai due varianti uguali consecutive nel volume
  4. Capienza        — ogni trafiletto reale entra nella zona della sua variante
  5. Rendering       — dimensioni pagina, determinismo, warning, fallback
"""
import json
import sys
import importlib.util
from pathlib import Path

import pytest
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
SPEC_PATH = REPO / "visual/atlante/ATLANTE_SPEC.json"
sys.path.insert(0, str(SCRIPTS))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def bv():
    return _load("build_volume", SCRIPTS / "build_volume.py")


@pytest.fixture(scope="session")
def spec():
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def tavola_finta(tmp_path_factory, bv):
    """Tavola sintetica a spec (carta avorio, dimensione pagina piena)."""
    p = tmp_path_factory.mktemp("tavole") / "finta_tavola.jpg"
    Image.new("RGB", (bv.ATL_MIN_W, bv.ATL_MIN_H), (236, 228, 210)).save(
        p, "JPEG", quality=95)
    return p


# ═══ 1. SPEC — schema e zone ════════════════════════════════════════════════

CAMPI_VOCE = {"titolo", "slug", "volume", "tipo", "variante", "tavola",
              "quartiere", "binomio", "note"}
ZONE_RICHIESTE = {"eyebrow", "nome", "corpo", "firma", "figura"}


def test_spec_esiste_ed_e_json_valido(spec):
    assert "varianti" in spec and "voci" in spec


def test_schema_voci_uniforme(spec):
    """Forma uniforme dei nodi: tutti i campi presenti (null ammesso)."""
    for voce in spec["voci"]:
        assert set(voce.keys()) == CAMPI_VOCE, f"Campi non uniformi: {voce['titolo']}"
        assert voce["tipo"] in ("tavola", "mappa")
        if voce["tipo"] == "tavola":
            assert voce["variante"] in spec["varianti"], voce["titolo"]
        else:
            assert voce["variante"] is None, voce["titolo"]
        assert voce["volume"] in (1, 2, 3, 4)


def test_slug_coerenti_con_titoli(spec, bv):
    """Lo slug nello spec deve coincidere con _title_to_slug(titolo)."""
    for voce in spec["voci"]:
        assert voce["slug"] == bv._title_to_slug(voce["titolo"]), voce["titolo"]


def test_varianti_zone_complete_e_in_range(spec):
    for vid, var in spec["varianti"].items():
        assert set(var["zone"].keys()) >= ZONE_RICHIESTE, vid
        assert isinstance(var["fs_corpo"], int) and 20 <= var["fs_corpo"] <= 60
        for zid, z in var["zone"].items():
            for k in ("x", "y", "w", "h"):
                v = z.get(k)
                if v is not None:
                    assert 0.0 <= v <= 1.0, f"{vid}/{zid}/{k}={v}"
            if z.get("w") is not None and z.get("h") is not None:
                assert z["x"] + z["w"] <= 1.0 + 1e-9, f"{vid}/{zid} esce a destra"
                assert z["y"] + z["h"] <= 1.0 + 1e-9, f"{vid}/{zid} esce in basso"


def test_zone_testo_non_sovrapposte_alla_figura(spec):
    """Il corpo del testo non deve invadere la zona figura (verticalmente)."""
    for vid, var in spec["varianti"].items():
        c, f = var["zone"]["corpo"], var["zone"]["figura"]
        c_box = (c["x"], c["y"], c["x"] + c["w"], c["y"] + c["h"])
        f_box = (f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"])
        overlap_x = min(c_box[2], f_box[2]) - max(c_box[0], f_box[0])
        overlap_y = min(c_box[3], f_box[3]) - max(c_box[1], f_box[1])
        assert overlap_x <= 0 or overlap_y <= 0, \
            f"Variante {vid}: corpo e figura si sovrappongono"


def test_tavole_dichiarate_esistono(spec):
    """Se una voce dichiara una tavola, il file deve esistere nella repo."""
    for voce in spec["voci"]:
        if voce["tavola"]:
            assert (REPO / voce["tavola"]).exists(), \
                f"Tavola dichiarata ma assente: {voce['tavola']}"


# ═══ 2. COPERTURA — spec ↔ presentazioni parziali ═══════════════════════════

def test_copertura_voci_presentazione(spec, bv):
    """Ogni titolo della presentazione parziale ha la sua voce nello spec,
    nel volume giusto. Se i trafiletti cambiano, questo test lo segnala."""
    per_slug = {v["slug"]: v for v in spec["voci"]}
    for vol in (1, 2, 3, 4):
        for titolo, _ in bv.get_presentazione_parziale(vol):
            slug = bv._title_to_slug(titolo)
            assert slug in per_slug, f"Voce mancante nello spec: {titolo} (vol {vol})"
            assert per_slug[slug]["volume"] == vol, \
                f"{titolo}: volume spec={per_slug[slug]['volume']}, reale={vol}"


# ═══ 3. RITMO — mai due varianti uguali consecutive ═════════════════════════

def test_ritmo_senza_ripetizioni_consecutive(spec, bv):
    for vol in (1, 2, 3, 4):
        seq = []
        per_slug = {v["slug"]: v for v in spec["voci"]}
        for titolo, _ in bv.get_presentazione_parziale(vol):
            voce = per_slug[bv._title_to_slug(titolo)]
            if voce["tipo"] == "tavola":
                seq.append(voce["variante"])
        for a, b in zip(seq, seq[1:]):
            assert a != b, f"Vol {vol}: variante '{a}' ripetuta consecutiva ({seq})"


# ═══ 4. CAPIENZA — i trafiletti reali entrano nelle zone ════════════════════

def test_capienza_trafiletti_reali(spec, bv, tavola_finta):
    """Render di TUTTE le voci tavola con il loro trafiletto reale: nessun
    overflow. Blinda sia le zone dello spec sia future modifiche ai testi."""
    per_slug = {v["slug"]: v for v in spec["voci"]}
    for vol in (1, 2, 3, 4):
        for titolo, body in bv.get_presentazione_parziale(vol):
            voce = per_slug[bv._title_to_slug(titolo)]
            if voce["tipo"] != "tavola":
                continue
            warns = []
            img = bv.make_atlante_plate_page(
                titolo, body, tavola_finta, volume=vol,
                variante_id=voce["variante"], layout_warnings=warns)
            overflow = [w for w in warns if w.get("testo_tagliato")]
            assert not overflow, (
                f"{titolo} (variante {voce['variante']}): trafiletto non entra — "
                f"{overflow[0]['suggerimento']}")
            assert img.size == (bv.TX_W, bv.TX_H)


# ═══ 5. RENDERING — invarianti della pagina ═════════════════════════════════

def test_pagina_dimensioni_trim(bv, tavola_finta, spec):
    for vid in spec["varianti"]:
        img = bv.make_atlante_plate_page("Fiamma", "Testo di prova breve.",
                                         tavola_finta, volume=1, variante_id=vid)
        assert img.size == (bv.TX_W, bv.TX_H), f"Variante {vid}"


def test_pagina_deterministica(bv, tavola_finta):
    a = bv.make_atlante_plate_page("Fiamma", "Testo di prova.", tavola_finta,
                                   volume=1, variante_id="D")
    b = bv.make_atlante_plate_page("Fiamma", "Testo di prova.", tavola_finta,
                                   volume=1, variante_id="D")
    assert a.tobytes() == b.tobytes()


def test_testo_lunghissimo_genera_warning(bv, tavola_finta):
    warns = []
    bv.make_atlante_plate_page("Fiamma", "parola " * 600, tavola_finta,
                               volume=1, variante_id="A", layout_warnings=warns)
    assert any(w.get("testo_tagliato") for w in warns)


def test_tavola_sotto_spec_genera_warning(bv, tmp_path):
    small = tmp_path / "piccola.jpg"
    Image.new("RGB", (800, 1100), (236, 228, 210)).save(small, "JPEG")
    warns = []
    img = bv.make_atlante_plate_page("Fiamma", "Testo di prova.", small,
                                     volume=1, variante_id="A",
                                     layout_warnings=warns)
    assert img.size == (bv.TX_W, bv.TX_H)
    assert any("TAVOLA SOTTO SPEC" in w["entry"] for w in warns)


def test_tavola_orizzontale_e_sotto_spec(bv, tmp_path):
    land = tmp_path / "orizzontale.jpg"
    Image.new("RGB", (2480, 1748), (236, 228, 210)).save(land, "JPEG")
    ok, _ = bv.check_tavola_quality(land)
    assert not ok


def test_fallback_quando_tavola_assente(bv, spec):
    """Stato attuale: nessuna tavola pronta → atlante_entry_for deve dare None
    e il volume si monta col layout classico (degradazione dolce)."""
    per_slug = {v["slug"]: v for v in spec["voci"]}
    for slug, voce in per_slug.items():
        if voce["tipo"] == "tavola" and not voce["tavola"]:
            assert bv.atlante_entry_for(voce["titolo"]) is None, voce["titolo"]


def test_voce_mappa_mai_tavola(bv):
    assert bv.atlante_entry_for("Questa è l'isola") is None


def test_binomio_renderizzato_senza_errori(bv, tavola_finta):
    img = bv.make_atlante_plate_page("Fiamma", "Testo di prova.", tavola_finta,
                                     volume=1, variante_id="A",
                                     binomio="Vulpes fornaria")
    assert img.size == (bv.TX_W, bv.TX_H)


# ═══ 6. INGEST — manifest verificato, mai creduto ═══════════════════════════

@pytest.fixture(scope="session")
def ingest():
    return _load("ingest_tavola", SCRIPTS / "ingest_tavola.py")


def _scrivi_manifest(tmp_path, slug="fiamma", variante="D",
                     file_rel="visual/atlante/tavole/x.jpg", **extra):
    m = {"schema": "tavola_atlante/1.0", "slug": slug, "variante": variante,
         "file": file_rel, "generatore": "manus", "data": "2026-06-12",
         "note": None}
    m.update(extra)
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps(m), encoding="utf-8")
    return p, m


def _tavola_quieta(path, bv, spec, variante):
    """Scena finta: zona figura scura/dettagliata, zone testo quiete."""
    import random
    img = Image.new("RGB", (bv.ATL_MIN_W, bv.ATL_MIN_H), (228, 222, 206))
    d = __import__("PIL.ImageDraw", fromlist=["ImageDraw"]).Draw(img)
    fz = spec["varianti"][variante]["zone"]["figura"]
    x0, y0 = fz["x"]*bv.TX_W, fz["y"]*bv.TX_H
    x1, y1 = x0 + fz["w"]*bv.TX_W, y0 + fz["h"]*bv.TX_H
    rng = random.Random(432)
    for _ in range(4000):   # "scena" rumorosa dentro la zona figura
        px = rng.uniform(x0, x1-6); py = rng.uniform(y0, y1-6)
        d.rectangle([px, py, px+6, py+6],
                    fill=(rng.randint(40, 160), rng.randint(40, 140),
                          rng.randint(30, 110)))
    img.save(path, "JPEG", quality=95)


def test_ingest_accetta_tavola_buona(ingest, bv, spec, tmp_path, monkeypatch):
    rel = "visual/atlante/tavole/_test_fiamma.jpg"
    img_path = REPO / rel
    _tavola_quieta(img_path, bv, spec, "D")
    try:
        mp, _ = _scrivi_manifest(tmp_path, file_rel=rel)
        ok, manifest, rep = ingest.verifica_tavola(mp)
        assert ok, "\n".join(rep)
    finally:
        img_path.unlink(missing_ok=True)


def test_ingest_respinge_zona_rumorosa(ingest, bv, spec, tmp_path):
    """Scena che invade la zona testo (dettaglio scuro sul corpo) → respinta."""
    rel = "visual/atlante/tavole/_test_rumorosa.jpg"
    img_path = REPO / rel
    img = Image.new("RGB", (bv.ATL_MIN_W, bv.ATL_MIN_H), (228, 222, 206))
    d = __import__("PIL.ImageDraw", fromlist=["ImageDraw"]).Draw(img)
    cz = spec["varianti"]["D"]["zone"]["corpo"]
    x0, y0 = cz["x"]*bv.TX_W, cz["y"]*bv.TX_H
    x1, y1 = x0 + cz["w"]*bv.TX_W, y0 + cz["h"]*bv.TX_H
    # "Scena" fitta e scura dentro la zona corpo: strisce alternate
    yy = y0
    while yy < y1:
        d.rectangle([x0, yy, x1, yy+8], fill=(52, 44, 30))
        yy += 16
    img.save(img_path, "JPEG", quality=95)
    try:
        mp, _ = _scrivi_manifest(tmp_path, file_rel=rel)
        ok, _, rep = ingest.verifica_tavola(mp)
        assert not ok
        assert any("quiete" in r.lower() or "Zona" in r for r in rep)
        # --force la accetta (selezione umana sovrana)
        ok_f, _, _ = ingest.verifica_tavola(mp, force=True)
        assert ok_f
    finally:
        img_path.unlink(missing_ok=True)


def test_ingest_respinge_manifest_rotto(ingest, tmp_path):
    p = tmp_path / "rotto.json"
    p.write_text('{"schema": "altro/9.9", "slug": "fiamma"}', encoding="utf-8")
    ok, _, rep = ingest.verifica_tavola(p)
    assert not ok


def test_ingest_respinge_slug_sconosciuto(ingest, bv, spec, tmp_path):
    rel = "visual/atlante/tavole/_test_slug.jpg"
    img_path = REPO / rel
    _tavola_quieta(img_path, bv, spec, "A")
    try:
        mp, _ = _scrivi_manifest(tmp_path, slug="drago_inventato", file_rel=rel)
        ok, _, rep = ingest.verifica_tavola(mp)
        assert not ok
        assert any("sconosciuto" in r for r in rep)
    finally:
        img_path.unlink(missing_ok=True)


def test_ingest_respinge_voce_mappa(ingest, bv, spec, tmp_path):
    rel = "visual/atlante/tavole/_test_mappa.jpg"
    img_path = REPO / rel
    _tavola_quieta(img_path, bv, spec, "A")
    try:
        mp, _ = _scrivi_manifest(tmp_path, slug="questa_l_isola",
                                 variante="A", file_rel=rel)
        ok, _, rep = ingest.verifica_tavola(mp)
        assert not ok
    finally:
        img_path.unlink(missing_ok=True)


def test_ingest_respinge_immagine_sotto_spec(ingest, bv, spec, tmp_path):
    rel = "visual/atlante/tavole/_test_piccola.jpg"
    img_path = REPO / rel
    Image.new("RGB", (800, 1100), (228, 222, 206)).save(img_path, "JPEG")
    try:
        mp, _ = _scrivi_manifest(tmp_path, file_rel=rel)
        ok, _, rep = ingest.verifica_tavola(mp)
        assert not ok
        assert any("sotto spec" in r for r in rep)
    finally:
        img_path.unlink(missing_ok=True)


def test_ingest_aggiorna_spec_e_ripristino(ingest, bv, spec, tmp_path):
    """aggiorna_spec scrive variante+tavola nella voce giusta (poi ripristina)."""
    backup = SPEC_PATH.read_text(encoding="utf-8")
    try:
        ingest.aggiorna_spec({"slug": "fiamma", "variante": "D",
                              "file": "visual/atlante/tavole/x.jpg",
                              "note": None})
        nuovo = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
        voce = next(v for v in nuovo["voci"] if v["slug"] == "fiamma")
        assert voce["tavola"] == "visual/atlante/tavole/x.jpg"
        assert voce["variante"] == "D"
    finally:
        SPEC_PATH.write_text(backup, encoding="utf-8")
