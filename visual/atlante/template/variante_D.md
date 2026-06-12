# Template tavola-atlante — VARIANTE D · "cielo alto"

**Composizione:** scena piena, soggetto nella metà BASSA, spazio quieto (cielo) in ALTO.
Il testo (eyebrow, nome, trafiletto) verrà sovrapposto dalla pipeline nella
fascia alta; la firma in una sottile fascia in basso al centro.

Coordinate delle zone (frazioni della pagina, da `ATLANTE_SPEC.json`):
- testa (eyebrow+nome): x 0.085, y 0.058–0.165 (invariata)
- corpo testo:          x 0.085, y 0.178, w 0.83, h 0.205
- fascia firma:         y 0.88–0.96, centrata
- zona soggetto:        x 0.040, y 0.430, w 0.92, h 0.44

## Blocco composizione (incollare nel prompt, dopo lo SAGA STYLESHEET)

```
FULL-PAGE COMPOSITION — the subject lives in their real place on the
island (home, workshop, neighborhood), shown in a complete scene, not
floating on blank paper. The subject and all detailed elements occupy
the LOWER HALF of the page (from 43% of the height down to 88%).

The UPPER 40% of the page (from the top edge down to 40% of the height,
full width) must be QUIET DIEGETIC SPACE: open sky with at most very
faint distant clouds, soft morning haze, or pale empty air — painted in
very soft, pale, low-contrast watercolor washes with no objects, no
characters, no strong lines, no detailed texture. A thin strip along the
bottom of the page (lowest 10%) must also stay calm and uncluttered.

ABSOLUTE RULE: no text anywhere on the page. No letters, numbers, signs,
labels, captions, handwriting or pseudo-handwriting.

Portrait orientation, aspect ratio 1748:2480, minimum 1748×2480 px.
```

## Manifest da consegnare insieme all'immagine

Salvare come `visual/atlante/tavole/<slug>_tavola_v1.json`:

```json
{
  "schema": "tavola_atlante/1.0",
  "slug": "<slug>",
  "variante": "D",
  "file": "visual/atlante/tavole/<slug>_tavola_v1.jpg",
  "generatore": "manus",
  "data": "AAAA-MM-GG",
  "note": null
}
```

Poi: `python3 scripts/ingest_tavola.py visual/atlante/tavole/<slug>_tavola_v1.json`
(l'ingest verifica dimensioni e quiete reale delle zone testo, e solo se
passa aggiorna `ATLANTE_SPEC.json`).
