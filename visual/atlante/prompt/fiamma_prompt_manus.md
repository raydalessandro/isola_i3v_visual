# Prompt Manus — Tavola atlante: FIAMMA (prototipo)

**Voce:** Fiamma — variante D (cielo alto) — vedi `template/variante_D.md`
**Reference da allegare a Manus:**
- `visual/personaggi/individuali/primari/fiamma/immagini/fiamma_canonica_v1_ritratto.jpg`
  (preferire la `_hd/` se presente)
- `visual/luoghi/quartiere_fuoco/forno/immagini/forno_canonica_v1_esterno_alba.jpg`

**Composizione del prompt (3 blocchi, in quest'ordine):**

---

## BLOCCO 1 — SAGA STYLESHEET v1

Incollare identico da `_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md`
(blocco ART STYLE + negative prompt globale). Mai omesso, mai modificato.

---

## BLOCCO 2 — Soggetto e ambiente (dalle schede canoniche)

```
SUBJECT — Fiamma, anthropomorphic red fox baker, stable bipedal posture.
Ember-colored fur: brick-red back with coppery highlights, cream-ivory
chest and belly. Long bushy tail carried low, with a sharp white tip.
Erect triangular ears with cream inner fur and thin black edges. Pointed
muzzle, small black nose, amber-yellow narrow eyes with a lively, patient
gaze. Hands with black pads, dusted with flour. Visual signature: a
rough-weave terracotta apron, always floury, with bib, large front
pocket and back laces; underneath, a cream linen blouse with sleeves
rolled to the elbow and a straw-ivory skirt to mid-calf. Bare fox feet.

SCENE — Fiamma stands at the entrance of her bakery in the Fire Quarter
at early morning: a common village oven of rough plastered stone with a
pitched roof of dark terracotta tiles, warm light from the wood oven's
mouth glowing inside, wooden shelves with round loaves. She holds a
basket of fresh bread. The building feels communal and lived-in, like a
village oven of a Mediterranean hamlet — airy, not domestic.
```

---

## BLOCCO 3 — Composizione (da `template/variante_D.md`)

Incollare il blocco "FULL-PAGE COMPOSITION" del template D: soggetto e
Forno nella metà bassa della pagina (dal 43% all'88% dell'altezza), il
40% superiore cielo quieto del mattino — lavature pallide, al più nuvole
lontanissime, nessun oggetto né linea forte — e fascia bassa calma.
Divieto assoluto di testo. Verticale, min 1748×2480.

---

## Dopo la generazione

1. Selezione umana con la checklist di `skills/atlantista/SKILL.md` §3.
2. Salvare la scelta come `visual/atlante/tavole/fiamma_tavola_v1.jpg`.
3. Manifest `visual/atlante/tavole/fiamma_tavola_v1.json`:

```json
{
  "schema": "tavola_atlante/1.0",
  "slug": "fiamma",
  "variante": "D",
  "file": "visual/atlante/tavole/fiamma_tavola_v1.jpg",
  "generatore": "manus",
  "data": "AAAA-MM-GG",
  "note": null
}
```

4. `python3 scripts/ingest_tavola.py visual/atlante/tavole/fiamma_tavola_v1.json`
5. `python3 -m pytest tests/test_atlante.py -q`
