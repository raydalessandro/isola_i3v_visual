#!/usr/bin/env python3
"""
Test d'integrazione: costruisce un PDF vero e verifica le invarianti di
STAMPA che KDP richiede. Più lento dei test unit (fa un build completo),
quindi marcato 'slow' — eseguibile a parte.

    python3 -m pytest tests/test_integration.py -v
    python3 -m pytest tests/ -v -m "not slow"   # salta questo
"""
import sys
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

fitz = pytest.importorskip("fitz")  # pymupdf


@pytest.fixture(scope="module")
def built_pdf(tmp_path_factory):
    """Esegue un build reale del volume 1 (storia s01) e ritorna il PDF stampa."""
    out = tmp_path_factory.mktemp("build")
    cmd = [
        sys.executable, str(SCRIPTS / "build_volume.py"),
        "--volume", "1", "--storie", "s01", "--presentazione", "dopo",
        "--output", str(out),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    assert res.returncode == 0, f"Build fallito:\n{res.stderr}\n{res.stdout}"
    pdfs = list(out.glob("*_stampa.pdf"))
    assert pdfs, f"Nessun PDF stampa prodotto in {out}"
    return pdfs[0]


@pytest.mark.slow
class TestStampa:
    def test_pdf_esiste_e_apre(self, built_pdf):
        doc = fitz.open(built_pdf)
        assert len(doc) > 0

    def test_pagina_a5_esatta(self, built_pdf):
        doc = fitz.open(built_pdf)
        for page in doc:
            w_mm = page.rect.width / 72 * 25.4
            h_mm = page.rect.height / 72 * 25.4
            assert abs(w_mm - 148) < 0.6, f"larghezza {w_mm:.1f}mm ≠ 148"
            assert abs(h_mm - 210) < 0.6, f"altezza {h_mm:.1f}mm ≠ 210"

    def test_conteggio_pagine_pari(self, built_pdf):
        # KDP richiede un numero di pagine pari
        doc = fitz.open(built_pdf)
        assert len(doc) % 2 == 0, f"{len(doc)} pagine (dispari)"

    def test_immagini_storia_a_300dpi(self, built_pdf):
        # almeno un'immagine a piena pagina deve essere ~300 DPI
        doc = fitz.open(built_pdf)
        page_w_in = doc[0].rect.width / 72
        trovata_hires = False
        for page in doc:
            for img in page.get_images():
                pix = fitz.Pixmap(doc, img[0])
                dpi = pix.width / page_w_in
                if dpi >= 290:
                    trovata_hires = True
                    break
            if trovata_hires:
                break
        assert trovata_hires, "Nessuna immagine a ~300 DPI trovata"

    def test_nessuna_pagina_vuota_inattesa(self, built_pdf):
        # ogni pagina deve avere o testo o immagini (le bianche di parità
        # sono poche: tolleranza)
        doc = fitz.open(built_pdf)
        vuote = 0
        for page in doc:
            if not page.get_text().strip() and not page.get_images():
                vuote += 1
        assert vuote <= 3, f"{vuote} pagine vuote (troppe)"

    def test_due_pdf_prodotti(self, built_pdf):
        # accanto al PDF stampa deve esserci anche il PDF libro
        out_dir = built_pdf.parent
        assert list(out_dir.glob("*_libro.pdf")), "manca il PDF libro sfogliabile"
