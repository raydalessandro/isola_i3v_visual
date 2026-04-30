# Prompt Grok Imagine — `bisaccia_zolla`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica di riferimento della bisaccia di Zolla (scoiattolo anziano raccoglitore-conta-stagioni, vive ai margini degli Orti del Cerchio).

---

## Prompt principale (English, single shot)

```
A small soft leather satchel, hand-stitched, of warm light-brown to caramel-tan tone (well-aged worked leather), with a single crossbody strap and TWO simple drawstrings tied closed at the top. The bag is small (the size of two fists), pouchy and full — clearly bulging gently with foraged things inside (chestnuts, acorns, walnuts, dried roots) suggested by the irregular soft swelling of the leather, but the contents are not directly visible. The leather surface is slightly creased, soft from use, with subtle darker patina at the corners and around the strap attachment points. A small loose grain of acorn or a curled chestnut leaf may peek from the edge of the drawstring. The satchel is shown isolated as a still-life on a wooden plank or a flat mossy stone, against a softly out-of-focus background of garden-edge and forest interior — deep greens, root browns, ochre tones, dappled woodland light.

Lighting: warm side light filtering through leaves, soft amber-golden tone with cool green shadows. Quiet, grounded atmosphere of late-afternoon foraging — the western Quartiere di Terra palette.

Color palette: caramel-tan leather, warm umber stitching, ochre highlights, cool forest greens behind. NO pure white, NO bright red, NO black-pure leather, NO synthetic-looking dye.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a 19th-century rural still-life. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the satchel showing the strap, the two drawstrings, and the soft pouchy fullness. Frame includes hint of garden-edge foliage and dappled light. Aspect ratio 4:5 (portrait).
```

---

## Variante "in uso" — Zolla che la indossa

**Aspect ratio:** 4:5
**Filename atteso:** `bisaccia_zolla_in_uso_v1.jpg` (opzionale)

```
Same style, same palette. Three-quarter portrait of Zolla, an elderly grey squirrel, slightly wiry with grey fur darkening to dark grey at extremities, wearing a simple ochre-tinted vest. The soft-leather satchel is slung crossbody from his shoulder to opposite hip, the two drawstrings tied closed, bag visibly full. He is mid-step on a forest path or at the edge of a garden, head turned slightly as if listening or counting. Painterly oil-style, dignified, woodland late-afternoon light.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale, classico per oggetto isolato).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. Pelle morbida color cuoio caldo (mai nero, mai sintetico)
  2. **Due cordoncini visibili** (non uno, non zip)
  3. Borsa **piccola** (mai zaino, mai sacca grande)
  4. Sempre **piena/morbidamente bombata**
  5. Stato vissuto, mai nuovo, mai stracciato

---

## Negative prompt

```
no large bag, no backpack, no zipper, no buckle, no metal hardware, no synthetic leather look, no shiny lacquered surface, no bright red, no pure black, no pure white, no embroidered patterns, no decorative tooling, no studs, no rivets, no costume bag, no theatrical, no cartoon, no anime, no 3D render, no flat vector, no logos, no brand stamps, no text.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`bisaccia_zolla_v1.jpg` in `visual/oggetti/bisaccia_zolla/immagini/`), verificare:

- [ ] Pelle morbida, color cuoio caldo (mai nero, mai sintetico)?
- [ ] **Due cordoncini chiusi** visibili (non uno, mai zip)?
- [ ] Tracolla singola di traverso?
- [ ] **Piccola** (size of two fists, mai zaino)?
- [ ] **Sempre piena** — visibile bombatura morbida?
- [ ] Stato vissuto (mai nuova, mai stracciata)?
- [ ] Sfondo coerente con palette Quartiere di Terra (verde scuro, marrone radici, ocra)?
- [ ] Stile painterly, mai cartoon né photoreal-iper?
