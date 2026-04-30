# Prompt Grok Imagine — `bandana_rovo`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica di riferimento della bandana di Rovo (firma visiva del tasso brontolone, vive ai margini della Foresta Intrecciata).

---

## Prompt principale (English, single shot)

```
A worn dark cloth bandana, color a muted earthy grey-brown (between umber and dark taupe), tied tightly across a forehead in a flat band — the kind of band a labourer or hunter would tie under the ears. The fabric is rough cotton or hemp, hand-woven, slightly faded at the folds, with a few subtle dust traces and a single small fray on one corner. The knot is tied at the back, simple and tight, never decorative. The bandana is shown isolated as a still-life on a piece of dark mossy wood (a tree stump fragment) against an out-of-focus background of dim forest interior — deep greens, root-browns, ochre, dappled low light filtering through leaves. The cloth is well-used, never new, never torn — carefully kept, like a working tool.

Lighting: low filtered woodland light, cool greens with warm ochre highlights, deep earthy shadows. The atmosphere is grounded, quiet, slightly somber — the western Quartiere di Terra palette.

Color palette: muted grey-brown bandana (think dark taupe / aged umber), forest dark greens, root browns, ochre highlights. NO bright red, NO black-pure, NO patterned fabric, NO tribal motif.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a 19th-century forest still-life — quiet, dignified, materially honest. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the bandana laid or hung on the dark mossy stump showing the knot and the texture. Frame includes a hint of forest floor and dappled light. Aspect ratio 4:5 (portrait).
```

---

## Variante "in uso" — Rovo che la indossa

**Aspect ratio:** 4:5
**Filename atteso:** `bandana_rovo_in_uso_v1.jpg` (opzionale, dopo la canonica)

```
Same style, same palette. Close-up portrait of Rovo, an adult badger (grey-dark fur with the canonical white stripe down head and nape), the dark grey-brown bandana tied tightly across his forehead in a flat band, knot at the back of the head, sitting just under the rounded badger ears. The bandana is the focal element, snug and worn-in. Three-quarter view of the head, soft forest light, subdued forest greens behind. Painterly oil-style, dignified.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale, classico per oggetto isolato).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. Colore grigio-marrone terra (mai rosso, mai nero puro)
  2. Tessuto grezzo, mai liscio sintetico
  3. Nessun pattern decorativo, nessuna stampa
  4. Nodo semplice, mai elaborato
  5. Stato d'uso: usata ma curata, mai stracciata né nuova

---

## Negative prompt

```
no bright red bandana, no pure black, no pirate skull pattern, no tribal pattern, no paisley, no polka dots, no stripes, no embroidery, no decorative trim, no fluorescent colors, no plastic synthetic look, no smooth silk, no clean new fabric, no torn rags, no costume, no theatrical, no cartoon, no anime, no 3D render, no flat vector, no logos, no text, no signatures.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`bandana_rovo_v1.jpg` in `visual/oggetti/bandana_rovo/immagini/`), verificare:

- [ ] Colore grigio-marrone terra (mai vivido, mai nero pieno)?
- [ ] Tessuto grezzo cotone/canapa (mai sintetico/lucido)?
- [ ] Nessun pattern decorativo (mai paisley, teschi, righe)?
- [ ] Nodo semplice e stretto?
- [ ] Stato usato ma curato (mai stracciato, mai nuovo)?
- [ ] Sfondo coerente con palette Quartiere di Terra (verde scuro, marrone radici, ocra)?
- [ ] Stile painterly, mai cartoon né photoreal-iper?
