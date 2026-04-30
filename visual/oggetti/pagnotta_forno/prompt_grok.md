# Prompt Grok Imagine — `pagnotta_forno`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica della pagnotta del Forno di Fiamma — oggetto-cornice della saga (s1↔s12), il pane dell'isola.

---

## Prompt principale (English, single shot)

```
A single rustic round country loaf, hand-shaped, just out of a wood-fired oven. The crust is deep golden-brown with darker scorch marks where the dome has caressed the embers, dusted lightly with flour, scored across the top in a single rough cross or line (the simple bakers'-mark of the island). The crumb hint is visible at a small open break on one side, showing pale honey-colored interior with irregular open holes — a country sourdough crumb. The loaf is medium-large (the size of two cupped hands), perfectly round, slightly domed. The surface texture shows visible kneading folds on the underside, a few small ember-burn dots from the oven floor, no symmetry, no machine-made perfection. The loaf is shown isolated as a still-life on a warm wooden bread-board, against a softly out-of-focus background of the bakery interior — terracotta walls, hint of the low oven mouth glowing warm, copper-orange ember light, dawn light filtering through.

Lighting: warm side light from the oven mouth and the rising dawn, deep warm shadows, golden glow on the crust. The kind of light that says "first warm place on the island in the morning".

Color palette: deep golden-brown crust, terracotta walls, ember-orange highlights, soft flour-cream dust, deep umber shadows. NO pale-white bread, NO factory bread, NO fluorescent yellow, NO sliced sandwich shape.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a Chardin bread still-life or a Velázquez bodegón — quiet, dignified, materially honest, bread-as-sacred. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the loaf showing the scoring on top, the deep-golden crust, and the small open break revealing the crumb. Frame includes the wooden board and a hint of the oven glow behind. Aspect ratio 4:5 (portrait).
```

---

## Variante "consegna" — pagnotta avvolta in panno per dono

**Aspect ratio:** 4:5
**Filename atteso:** `pagnotta_forno_consegna_v1.jpg` (opzionale)

```
Same style, same palette. The same round country loaf, partially wrapped in a piece of natural undyed linen cloth (cream-beige, a few subtle blue stripes), tied with a length of natural twine — ready to be carried as a gift to someone (e.g. "Portate una pagnotta a Grunto da parte mia"). The loaf is on the same wooden board or held in a small flat reed basket. The wrap reveals just enough of the crust to identify it. Painterly oil-style, dignified, warm bakery light.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. **Forma rotonda artigianale** (mai pane in cassetta, mai baguette, mai pan di lusso)
  2. **Crosta dorato-bruciato** con ember marks (mai pallida, mai bruciata)
  3. **Scoring semplice** sul dorso (croce/linea, mai pattern decorativo)
  4. Un piccolo break con mollica visibile (signature di freschezza/artigianalità)
  5. Aspetto da pane di campagna, mai industriale

---

## Negative prompt

```
no white bread, no sandwich loaf, no sliced bread, no baguette, no croissant, no pizza, no decorative bread shape, no machine-perfect symmetry, no glossy lacquer crust, no pre-packaged bread, no plastic wrap, no chain bakery look, no bright yellow, no cake, no pastry, no garnish, no parsley, no theatrical food styling, no cartoon, no anime, no 3D render, no flat vector, no logos, no text.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`pagnotta_forno_v1.jpg` in `visual/oggetti/pagnotta_forno/immagini/`), verificare:

- [ ] **Forma rotonda artigianale** (mai cassetta, mai baguette)?
- [ ] **Crosta dorato-bruciato** con ember marks?
- [ ] **Scoring semplice** sul dorso?
- [ ] Mollica visibile in un piccolo break?
- [ ] **Farina leggera** sul dorso?
- [ ] Aspetto pane di campagna (mai industriale, mai decorativo)?
- [ ] Sfondo coerente con palette Quartiere di Fuoco (terracotta, rosso brace, oro)?
- [ ] Stile painterly bodegón (mai cartoon né photoreal-iper)?
