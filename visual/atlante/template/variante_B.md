# Template tavola-atlante — VARIANTE B · "controriva"

**Composizione:** scena piena, soggetto a SINISTRA, spazio quieto a DESTRA.
Il testo (eyebrow, nome, trafiletto) verrà sovrapposto dalla pipeline nella
colonna destra; la firma in una sottile fascia in basso al centro.

Coordinate delle zone (frazioni della pagina, da `ATLANTE_SPEC.json`):
- testa (eyebrow+nome): x 0.455, y 0.058–0.165
- corpo testo:          x 0.455, y 0.210, w 0.46, h 0.62
- fascia firma:         y 0.88–0.96, centrata
- zona soggetto:        x 0.040, y 0.055, w 0.405, h 0.80

## Blocco composizione (incollare nel prompt, dopo lo SAGA STYLESHEET)

```
FULL-PAGE COMPOSITION — the subject lives in their real place on the
island (home, workshop, neighborhood), shown in a complete scene, not
floating on blank paper. The subject and all detailed elements occupy
the LEFT 40% of the page.

The RIGHT half of the page (from 45% of the width to the right edge, full
height) must be QUIET DIEGETIC SPACE: open sky, soft mist, a plain
plastered wall, calm water, or an empty stretch of meadow — painted in
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
  "variante": "B",
  "file": "visual/atlante/tavole/<slug>_tavola_v1.jpg",
  "generatore": "manus",
  "data": "AAAA-MM-GG",
  "note": null
}
```

Poi: `python3 scripts/ingest_tavola.py visual/atlante/tavole/<slug>_tavola_v1.json`
(l'ingest verifica dimensioni e quiete reale delle zone testo, e solo se
passa aggiorna `ATLANTE_SPEC.json`).
