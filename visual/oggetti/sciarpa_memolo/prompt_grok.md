# Prompt Grok Imagine — `sciarpa_memolo`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica di riferimento della sciarpa di Mèmolo (riccio "zio confuso", piazza Albero Vecchio).

---

## Prompt principale (English, single shot)

```
A small soft scarf, hand-knit or finely woven, in a warm muted color — primary tone is WARM SOFT BROWN with a subtle ochre undertone (the kind of dusty caramel-ochre that reads as "colorful but quiet"). The scarf is short (more a neckerchief than a long scarf), tied in a SLIGHTLY CROOKED knot at the neck — the knot is the signature: NEVER straight, NEVER perfectly centered, slightly off-axis, one end longer than the other, fabric naturally bunched on one side. The fabric is soft cotton or fine wool, slightly fuzzy at the edges, well-worn but cared for, never new, never tattered. The scarf is shown isolated as a still-life laid on a warm wooden tabletop or hung loosely over the back of a small round wooden chair, against a softly out-of-focus background of the central village — soft warm browns, hint of an old tree's bark, dappled afternoon light filtering down.

Lighting: warm afternoon side light, the kind of soft glow of the village square near the old central tree (Albero Vecchio).

Color palette: warm soft brown / dusty caramel-ochre as base, with subtle variation in the weave (a faint deeper umber thread, a faint lighter cream thread giving softness). Background warm browns, ochre, gentle greens of the village. NO bright primary colors, NO neon, NO grey-cool tones, NO synthetic dye look.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a Chardin domestic still-life — quiet, dignified, materially honest. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the scarf showing the crooked knot clearly and the two uneven ends. Frame includes hint of the village wood and warm afternoon light. Aspect ratio 4:5 (portrait).
```

---

## Variante "in uso s08" — sciarpa di sbieco al Pozzo

**Aspect ratio:** 4:5
**Filename atteso:** `sciarpa_memolo_in_uso_s08_v1.jpg` (opzionale)

```
Same style, same palette but with a slightly more pronounced ochre cast (the s08 visual anchor: "ocra sciarpa di memolo unico"). Three-quarter view of Mèmolo, an adult hedgehog with short soft spines (warm brown), seated on the stone edge of the village well in late afternoon-twilight. The scarf is at his neck, knot CLEARLY CROOKED, falling slightly to one side ("di sbieco") — even more visibly off-kilter than usual, as if he just absent-mindedly tugged it. He is in quiet confusion, looking down or to the side. Painterly oil-style, dignified, twilight palette around him cooled but the OCHRE of the scarf is the unique warm accent in the scene.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. **Nodo storto/crooked** (signature primaria — mai dritto)
  2. Marrone caldo morbido / dusty caramel-ochre (mai vivido)
  3. **Piccola** (neckerchief, non sciarpa lunga invernale)
  4. Tessuto morbido (cotone/lana fine), mai sintetico
  5. Stato vissuto, mai nuovo

---

## Negative prompt

```
no straight knot, no perfectly centered tie, no symmetric drape, no long winter scarf, no fluffy oversized scarf, no tartan pattern, no checkered, no stripes, no polka dots, no embroidery, no fringe tassels, no glitter, no sequins, no synthetic shiny fabric, no neon colors, no cool grey, no costume prop, no theatrical, no cartoon, no anime, no 3D render, no flat vector, no logos, no text.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`sciarpa_memolo_v1.jpg` in `visual/oggetti/sciarpa_memolo/immagini/`), verificare:

- [ ] **Nodo storto** (mai dritto/centrato) — la firma!
- [ ] Colore marrone caldo / dusty caramel-ochre (mai vivido)?
- [ ] **Piccola** (neckerchief, mai sciarpa lunga)?
- [ ] Tessuto morbido naturale (mai sintetico/lucido)?
- [ ] Estremità asimmetriche (una più lunga dell'altra)?
- [ ] Stato vissuto (mai nuova, mai stracciata)?
- [ ] Sfondo coerente con palette villaggio centrale (marroni caldi, ocra)?
- [ ] Stile painterly, mai cartoon né photoreal-iper?
