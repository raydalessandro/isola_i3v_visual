# Prompt Grok Imagine — `cesto_salvia`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica di riferimento del cesto a tracolla di Salvia (lepre erbalist, vive agli Orti del Cerchio).

---

## Prompt principale (English, single shot)

```
A small woven basket made of fine, slender willow wicker — light sand-cream color, the kind of pale natural unstained willow. The basket has a single soft fabric or braided-wicker shoulder strap (crossbody). The basket is small (about the size of a hand-and-a-half), shallow-rounded, and CONTAINS visible fresh herbs: bunches of sage with silvery-green leaves, sprigs of thyme, small ochre-tinged dried bundles tied with thin twine, perhaps a few green stems peeking over the rim. The wickerwork is fine and tightly woven, never crude or rustic-heavy, slightly worn in places where the strap rubs. The basket is shown isolated as a still-life on a flat warm wooden surface or a sun-warmed garden stone, against a softly out-of-focus background of an herb-garden — neat rows of green plants, hint of ochre garden wall, gentle morning light.

Lighting: warm soft morning light from one side, gentle shadows, the kind of clean herbalist's light that brings out the green and silver tones of the herbs.

Color palette: pale sand-cream wicker, fresh sage-green and silvery-green herbs, ochre and warm earth highlights, hints of dark forest green behind. NO bright primary colors, NO synthetic green, NO basket painted or stained.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a Dutch still-life or a 19th-century herbalist illustration. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the basket showing the strap, the wickerwork, and the herbs inside. Frame includes hint of garden rows and warm morning light. Aspect ratio 4:5 (portrait).
```

---

## Variante "in uso" — Salvia che lo porta

**Aspect ratio:** 4:5
**Filename atteso:** `cesto_salvia_in_uso_v1.jpg` (opzionale)

```
Same style, same palette. Three-quarter view of Salvia, an adult hare with sand-colored fur and a soft white belly, walking with quick short steps along a row of herb plants. The fine wicker basket hangs crossbody at her side, herbs visible inside. She holds her body purposefully forward, ears alert. Painterly oil-style, dignified, warm garden light, the light of someone working with care.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. Vimini **sottile** color sabbia naturale (mai grosso/rustico, mai colorato)
  2. **Piccolo** (mai cesto da mercato, mai cestino picnic decorativo)
  3. A tracolla con cinghia singola
  4. Sempre con erbe dentro (sage, thyme, ochre-tinted bundles)
  5. Aspetto da lavoro (mai decorativo, mai cesto di Pasqua)

---

## Negative prompt

```
no large basket, no picnic basket, no Easter basket, no decorative bow, no painted wicker, no stained wicker, no synthetic green herbs, no plastic flowers, no fake leaves, no costume prop, no theatrical, no cartoon, no anime, no 3D render, no flat vector, no logos, no text, no signatures, no kitsch ribbon, no lace trim, no pastel colors.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`cesto_salvia_v1.jpg` in `visual/oggetti/cesto_salvia/immagini/`), verificare:

- [ ] Vimini **sottile**, color sabbia naturale (mai colorato/dipinto)?
- [ ] **Piccolo** (mano-e-mezza, mai grande)?
- [ ] Cinghia a tracolla?
- [ ] Erbe visibili dentro (sage/thyme/bundles ocra)?
- [ ] Aspetto da lavoro (mai decorativo/festivo)?
- [ ] Sfondo coerente con orto erbe + palette Quartiere di Terra?
- [ ] Stile painterly, mai cartoon né photoreal-iper?
