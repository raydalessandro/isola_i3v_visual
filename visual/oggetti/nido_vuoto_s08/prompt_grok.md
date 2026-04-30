# Prompt Grok Imagine — `nido_vuoto_s08`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica del nido vuoto trovato da Noah in s08 (oggetto-ponte verso s10, "i posti vuoti non sono vuoti"). Pattern A: mai nominato nel testo, sopravvive solo per immagini.

> **Vincoli forti:** Nido di maggio abbandonato dopo covata, fragile e secco. Raccolto a due mani a coppa, posato dietro il Pozzo coperto con una foglia. La fisica della fragilità giustifica la sopravvivenza — leggibile come cura-del-mondo, non come miracolo.

---

## Prompt principale (English, single shot) — nido posato dietro il Pozzo

```
A small old bird's nest, woven of dry twigs, fine grass stems, a few pale feathers and bits of moss-fluff — the kind of compact cup-nest a small bird builds in May. The nest is EMPTY: no eggs, no chicks, no fragments. The weave is slightly disheveled at the rim but the cup-shape holds — clearly survived a fall but not in active use. The texture is DRY, friable, late-summer brittle (estate piena = friabile): you can read in the painted strokes that touching it would risk crumbling it. The nest is placed on the warm white-stone ground BEHIND the village well (Pozzo) — partially sheltered by the curve of the well's stone base — and it is COVERED by a single fresh GREEN LEAF laid carefully over it like a shallow lid (foglia di copertura). The leaf is just large enough to shadow the nest from rain or sun.

Setting: low-angle three-quarter view from near ground level, the nest centered and tender in scale, with hints of the well's weathered white stone wrapping behind, dry late-summer earth and a few fallen walnut leaves around. Background softly out-of-focus.

Lighting: late-afternoon to crepuscolo light (the s08 storm's aftermath), cielo color piombo (lead-grey sky overhead suggested by cool diffuse light), the white stone of the well picking up the cool light, deep greens of fallen walnut foliage, a hint of warm ochre on the protective leaf where the last warm light catches it.

Color palette: dry warm tan/beige nest, soft brown twigs, pale feather hints, fresh green leaf cover (slightly muted, not vivid), white-stone of the Pozzo (bianco pietra del pozzo), cool grey-piombo of the sky, dark greens of the fallen walnut canopy, hint of nero lucido of fresh-split wood at the edge. NO vivid colors, NO bright eggs, NO chicks, NO theatrical pity-light, NO dramatic spotlight.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of an early-Northern still-life or a quiet John Constable nature study — the dignity of one small thing carefully tended. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: nest centered low in frame, partially shadowed by the green leaf cover and the well's stone curve, dry summer ground around, soft cool late-afternoon light. The image carries the principle "i posti vuoti non sono vuoti" — the nest is empty but ATTENDED, not abandoned. Aspect ratio 4:5 (portrait).
```

---

## Variante "trovamento" — Noah lo raccoglie a coppa

**Aspect ratio:** 4:5
**Filename atteso:** `nido_vuoto_s08_trovamento_v1.jpg` (opzionale)

```
Same style, same palette but slightly more crepuscular. Three-quarter view of Noah, the youngest brother child, kneeling near the broken/fallen walnut branches at the edge of the Pozzo. He has just discovered the nest wedged in a small secondary fork of branch that remained suspended after the main branch was levered away. He is lifting it with BOTH hands held cup-style (a due mani a coppa), the nest cradled gently. His face is focused, careful, slightly furrowed with the awareness that "si sente che è secco" — the dry fragility readable in his hands' careful grip. Painterly oil-style, dignified. The nest must read as fragile but not theatrical-pity. Crepuscolo light, cool grey sky above, fallen branches around.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. **Vuoto** (no uova, no pulcini, no piume sparse)
  2. **Fragile e secco** (estate piena, friabile leggibile)
  3. **Coperto con UNA foglia verde** (mai foglie multiple, mai costruzione)
  4. **Posato dietro il Pozzo** (white stone visibile)
  5. La cura **leggibile**, mai dichiarata (Pattern A: solo immagini)

---

## Negative prompt

```
no eggs, no chicks, no baby birds, no parent bird returning, no decorated nest, no fairy nest, no Easter nest, no painted twigs, no glitter, no sparkles, no theatrical spotlight on the nest, no pity-lit close-up, no shrine arrangement, no candles, no flower wreath, no costume prop, no theatrical, no cartoon, no anime, no 3D render, no flat vector, no logos, no text, no signatures.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`nido_vuoto_s08_v1.jpg` in `visual/oggetti/nido_vuoto_s08/immagini/`), verificare:

- [ ] **Nido vuoto** (no uova, no pulcini)?
- [ ] **Fragile/secco** leggibile (estate piena friabile)?
- [ ] **Una sola foglia verde** sopra come copertura?
- [ ] **Posato dietro il Pozzo** (white stone wrap visibile)?
- [ ] Crepuscolo cielo piombo (mai sole pieno, mai luce drammatica)?
- [ ] La cura leggibile dalla composizione, mai dichiarata?
- [ ] Sfondo coerente con palette emotiva s08 (piombo, verdi scuri noce, bianco pietra, accent ocra)?
- [ ] Stile painterly Constable / Northern still-life (mai cartoon, mai theatrical)?

---

## Note di canone (non per il prompt)

- **Pattern A**: mai nominato nel testo della saga, sopravvive solo per immagini.
- Oggetto-ponte verso s10 (debt `debt_s08_to_s10_nido_vuoto_bloom_notte`): "Il buio era pieno", "i posti che sembrano vuoti non lo sono".
- La fisica della fragilità giustifica la sopravvivenza: NON miracolo, ma caso fisico leggibile come cura del mondo.
- Gesto di Noah a coppa = fisica nei verbi, non negli aggettivi.
