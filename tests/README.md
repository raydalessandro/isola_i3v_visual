# Test dello script di impaginazione

Blindano lo script che monta il libro, così funziona identico su tutti e 4 i volumi.

## Come si eseguono

```bash
pip install pytest Pillow reportlab pymupdf --break-system-packages

# tutti i test (unit + integrazione)
python3 -m pytest tests/ -v

# solo i veloci (saltano il build PDF completo)
python3 -m pytest tests/ -v -m "not slow"

# solo l'integrazione (build PDF reale + invarianti di stampa)
python3 -m pytest tests/test_integration.py -v
```

## Cosa coprono

**test_build_volume.py** (veloci, ~4s)
- Struttura: moduli, palette, colori-quartiere, glifi, cornici, camuni,
  dimensioni 300 DPI, i 4 volumi configurati, le 12 storie.
- Robustezza: slug, pulizia prosa, word-wrap, e soprattutto che le pagine
  si generino senza crash con immagine mancante / inesistente, testo
  lunghissimo (overflow + warning), testo minimo, testo vuoto.
- Decori: tutti i camuni, le 4 cornici, i glifi, i decori d'anima,
  `nasce_dalla_pagina`, e i colori-quartiere per personaggio.
- Coerenza sui 4 volumi: frontespizio, colophon, occhielli, occhiello
  storia, indice (semplice e numerato), soglia — per ogni volume.
- Determinismo: stesso input → output byte-identico.

**test_integration.py** (lento, ~60s, marcato `slow`)
- Build PDF reale del volume 1.
- Pagina A5 esatta (148×210 mm).
- Conteggio pagine pari (requisito KDP).
- Immagini a ~300 DPI.
- Nessuna pagina vuota inattesa.
- Produzione dei due PDF (stampa + libro).

## Quando rieseguirli

- Prima di pubblicare ogni volume.
- Dopo ogni modifica a `build_volume.py` o `design_system.py`.
- Quando si aggiungono le storie/immagini dei volumi 2–4.
