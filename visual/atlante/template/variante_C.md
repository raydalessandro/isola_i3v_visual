# Template tavola-atlante — VARIANTE C · "radura"

**Composizione:** scena piena, soggetto nella metà ALTA, spazio quieto nella fascia BASSA.
Il testo (eyebrow, nome, trafiletto) verrà sovrapposto dalla pipeline nella
fascia bassa; la firma in una sottile fascia in basso al centro.

Coordinate delle zone (frazioni della pagina, da `ATLANTE_SPEC.json`):
- testa (eyebrow+nome): x 0.085, y 0.555–0.660
- corpo testo:          x 0.085, y 0.672, w 0.83, h 0.205
- fascia firma:         y 0.88–0.96, centrata
- zona soggetto:        x 0.040, y 0.045, w 0.92, h 0.48

## Blocco composizione (incollare nel prompt, dopo lo SAGA STYLESHEET)

```
FULL-PAGE COMPOSITION — the subject lives in their real place on the
island (home, workshop, neighborhood), shown in a complete scene, not
floating on blank paper. The subject and all detailed elements occupy
the UPPER HALF of the page (from the top down to 52% of the height).

The LOWER HALF of the page (from 53% of the height to the bottom edge,
full width) must be QUIET DIEGETIC SPACE: the foreground fading into
soft mist, a calm stretch of meadow, sand, still water or bare earth — painted in
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
  "variante": "C",
  "file": "visual/atlante/tavole/<slug>_tavola_v1.jpg",
  "generatore": "manus",
  "data": "AAAA-MM-GG",
  "note": null
}
```

Poi: `python3 scripts/ingest_tavola.py visual/atlante/tavole/<slug>_tavola_v1.json`
(l'ingest verifica dimensioni e quiete reale delle zone testo, e solo se
passa aggiorna `ATLANTE_SPEC.json`).
