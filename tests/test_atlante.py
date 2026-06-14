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


# ═══ 5bis. DOPPIA ISOLA — spread mappa+testo ════════════════════════════════

def test_isola_doppia_e_uno_spread(bv):
    """make_isola_doppia ritorna un'immagine larga ~IMG_W*2 (left+right)."""
    img = bv.make_isola_doppia("Questa è l'isola", "Questa è l'isola dei venti.",
                               volume=1)
    assert img.height == bv.IMG_H
    assert img.width >= bv.IMG_W * 2          # due facciate affiancate
    assert img.width <= bv.IMG_W * 2 + 100    # solo la gutter di mezzo


def test_isola_doppia_fallback_senza_immagine(bv, tmp_path):
    """Immagine assente → niente crash, placeholder, spread valido."""
    fantasma = tmp_path / "non_esiste.jpg"
    img = bv.make_isola_doppia("Questa è l'isola", "Testo.", img_path=fantasma,
                               volume=1)
    assert img.height == bv.IMG_H and img.width >= bv.IMG_W * 2


def test_isola_doppia_warning_sotto_spec(bv, tmp_path):
    small = tmp_path / "isola_piccola.jpg"
    Image.new("RGB", (800, 1100), (160, 180, 170)).save(small, "JPEG")
    warns = []
    bv.make_isola_doppia("Questa è l'isola", "Testo.", img_path=small,
                         volume=1, layout_warnings=warns)
    assert any("SOTTO SPEC" in w["entry"] for w in warns)


def test_isola_doppia_deterministica(bv):
    a = bv.make_isola_doppia("Questa è l'isola", "Testo di prova.", volume=1)
    b = bv.make_isola_doppia("Questa è l'isola", "Testo di prova.", volume=1)
    assert a.tobytes() == b.tobytes()


def test_isola_doppia_testo_lungo_non_crasha(bv):
    img = bv.make_isola_doppia("Questa è l'isola", "parola " * 400, volume=1)
    assert img.height == bv.IMG_H


def test_capolettera_non_invade_terza_riga(bv, tavola_finta, spec):
    """Il capolettera deve far rientrare le prime righe e liberare le
    successive: confronto il margine sinistro del testo riga per riga.
    Render reale di una tavola e analisi delle colonne d'inchiostro."""
    import numpy as np
    txt = ("Questa è una prova lunga abbastanza da generare diverse righe di "
           "testo nel corpo della scheda, così da poter osservare il rientro "
           "del capolettera nelle prime due righe e il ritorno a piena "
           "larghezza dalla terza riga in avanti, come deve essere.")
    img = bv.make_atlante_plate_page("Fiamma", txt, tavola_finta,
                                     volume=1, variante_id="A")
    Z = spec["varianti"]["A"]["zone"]["corpo"]
    x0 = int(Z["x"] * bv.TX_W); y0 = int(Z["y"] * bv.TX_H)
    w  = int(Z["w"] * bv.TX_W); h = int(Z["h"] * bv.TX_H)
    arr = np.asarray(img.convert("L").crop((x0, y0, x0 + w, y0 + h)))
    # Per ogni riga di pixel, prima colonna "scura" (inchiostro)
    dark = arr < 110
    left_edges = []
    for row in dark:
        nz = np.nonzero(row)[0]
        if nz.size:
            left_edges.append(int(nz[0]))
    assert left_edges, "nessun testo rilevato nella zona corpo"
    # Il bordo sinistro minimo (righe a piena larghezza, sotto il capolettera)
    # deve trovarsi più a sinistra del bordo delle righe rientrate.
    min_left = min(left_edges)
    max_left = max(left_edges)
    assert max_left - min_left > int(bv.TX_W * 0.02), \
        "il rientro del capolettera non è visibile (testo non rientrato)"


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


# ═══ 7. PARITÀ FACCIATE CON SPREAD — KDP richiede pagine pari ═══════════════

def test_facciate_conta_spread_come_due(bv):
    pagine = [("single", None), ("spread", None), ("single", None)]
    assert bv._facciate(pagine) == 4


def test_ensure_recto_con_spread(bv):
    """ensure_recto deve pareggiare contando lo spread come 2 facciate."""
    # 1 spread (2) + 1 single (1) = 3 facciate → dispari → aggiunge bianca
    pagine = [("spread", bv.make_blank()), ("single", bv.make_blank())]
    out = bv.ensure_recto(pagine)
    assert bv._facciate(out) % 2 == 0


def test_volume_intero_facciate_pari(bv):
    """Il volume 1 completo (con la doppia isola) deve avere facciate pari."""
    pages, _ = bv.build_volume_pages(1)
    assert bv._facciate(pages) % 2 == 0, \
        f"{bv._facciate(pages)} facciate (dispari) — KDP richiede pari"


# ═══ 8. FRASI-ORACOLO — evidenziazione inline parole-chiave ═════════════════

def test_oracolo_parse_segmenti(bv):
    segs = bv._parse_rich("Le cose della *Foresta* hanno il loro *orario*.")
    assert ("Foresta", True) in segs and ("orario", True) in segs
    assert any(not k for _, k in segs)  # c'è anche testo normale


def test_oracolo_has_e_strip(bv):
    s = "Le cose della *Foresta* hanno il loro *orario*."
    assert bv.has_oracolo(s)
    assert bv.strip_oracolo(s) == "Le cose della Foresta hanno il loro orario."
    assert not bv.has_oracolo("frase normale senza marker")


def test_oracolo_punteggiatura_attaccata(bv):
    """La keyword seguita da punteggiatura non deve avere spazio spurio."""
    from PIL import Image, ImageDraw
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = bv.fnt(50); fk = bv._font_oracolo(50)
    rows = bv.rich_word_wrap("«Le cose della *Foresta* hanno il loro *orario*.»",
                             f, fk, 1500, d)
    flat = [t for r in rows for t in r]
    # il token di chiusura ".»" deve essere glued (attaccato a orario)
    chius = [t for t in flat if t[0] == ".»"]
    assert chius and chius[0][2] is True, "punteggiatura finale non attaccata"


def test_oracolo_wrap_non_sfora(bv):
    """Le keyword in Fredoka (più larghe) non devono sforare il margine."""
    from PIL import Image, ImageDraw
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    f = bv.fnt(50); fk = bv._font_oracolo(50)
    maxw = 900
    rows = bv.rich_word_wrap("Una frase con *parolemoltolunghe* e *altrekeyword* "
                             "che messe in fila *potrebbero* sforare il margine.",
                             f, fk, maxw, d)
    for row in rows:
        w = 0.0
        space = d.textlength(" ", font=f)
        for i, (word, key, glued) in enumerate(row):
            ww = d.textlength(word, font=(fk if key else f))
            w += ww if (i == 0 or glued) else space + ww
        assert w <= maxw + 1, f"riga sfora: {w} > {maxw}"


def test_oracolo_rendering_pagina_non_crasha(bv):
    import design_system as DS
    shs = bv.parse_story_md("s03")
    target = [s for s in shs if "orario" in s["text"]]
    assert target, "frase-oracolo di s03 non trovata (marker rimosso?)"
    img = bv.compose_story_page(target[0]["image_path"], target[0]["text"],
                                key_color=DS.CICLO_COLOR["Δ"])
    assert img.size == (bv.IMG_W, bv.IMG_H)


# ═══ 9. DOPPIA ISOLA — mare di collegamento e decori vettoriali ═════════════

def test_primitive_marine_esistono(bv):
    import design_system as DS
    for fn in ("mare_gradiente", "onde", "gabbiano", "barchetta", "pesce"):
        assert hasattr(DS, fn), f"manca primitiva marina {fn}"


def test_mare_gradiente_dimensioni_e_tipo(bv):
    import design_system as DS
    img = DS.mare_gradiente(200, 400, DS.VENTO_TAGLIO, riflesso=0.5)
    assert img.size == (200, 400) and img.mode == "RGB"
    # la riga in alto deve essere più chiara di quella in basso (riflesso cielo)
    top = img.getpixel((100, 2)); bot = img.getpixel((100, 398))
    assert sum(top) > sum(bot), "il gradiente non schiarisce verso l'alto"


def test_isola_doppia_con_mare_non_crasha(bv):
    img = bv.make_isola_doppia("Questa è l'isola",
                               "Questa è l'isola dei tre venti. " * 8, volume=1)
    assert img.height == bv.IMG_H and img.width >= bv.IMG_W * 2


def test_isola_doppia_mare_per_ogni_ciclo(bv):
    """Il colore del mare segue il ciclo del volume: nessun volume crasha."""
    for vol in (1, 2, 3, 4):
        img = bv.make_isola_doppia("Questa è l'isola", "Testo di prova.", volume=vol)
        assert img.height == bv.IMG_H


# ═══ 9. DOPPIA "L'ISOLA CHE DORME" — spread + continuazione ═════════════════

def test_isola_dorme_doppia_e_spread(bv):
    img = bv.make_isola_doppia("L'isola che dorme", "Ecco l'isola. Vedi che c'è.",
                               volume=1, eyebrow="ECCO L'ISOLA",
                               src_default=bv.ISOLA_CHE_DORME)
    assert img.height == bv.IMG_H
    assert img.width >= bv.IMG_W * 2


def test_isola_dorme_remainder_split(bv):
    """Testo lungo: parte entra nella doppia, il resto va in remainder_out."""
    testo = "parola " * 400
    rem = []
    bv.make_isola_doppia("L'isola che dorme", testo, volume=1,
                         eyebrow="ECCO L'ISOLA", src_default=bv.ISOLA_CHE_DORME,
                         remainder_out=rem)
    assert rem and rem[0].strip(), "il testo eccedente deve finire in remainder_out"
    # il remainder è più corto del totale (qualcosa è entrato nella doppia)
    assert len(rem[0].split()) < 400


def test_isola_dorme_testo_corto_niente_remainder(bv):
    rem = []
    bv.make_isola_doppia("L'isola che dorme", "Testo breve.", volume=1,
                         eyebrow="ECCO L'ISOLA", src_default=bv.ISOLA_CHE_DORME,
                         remainder_out=rem)
    assert not rem or not rem[0].strip()


def test_eyebrow_personalizzato(bv):
    """L'eyebrow passato come parametro non deve crashare il render."""
    img = bv.make_isola_doppia("L'isola che dorme", "Testo.", volume=1,
                               eyebrow="ECCO L'ISOLA",
                               src_default=bv.ISOLA_CHE_DORME)
    assert img.height == bv.IMG_H
