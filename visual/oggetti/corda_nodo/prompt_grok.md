# Prompt Grok Imagine — `corda_nodo`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica di riferimento della corda di Nodo (picchio rosso maggiore, bottega villaggio centrale, maestro di nodi).

---

## Prompt principale (English, single shot)

```
A coil of natural rope, hand-laid hemp or sisal in a warm pale beige color (corda chiara — light natural fibre, slightly variegated with paler and darker strands woven together), of medium thickness (the size you'd use for boat rigging or carpentry — about a finger's diameter). The rope is COILED neatly, as if just slipped off an arm — a tidy circular roll about hand-span wide, with the loose end tucked through. A FEW SAMPLE KNOTS are visible in the scene as small examples around the main coil: a figure-eight knot (Otto), a slip knot (Scorsoio), a bowline / sailor's knot (Marinaro), and a small drying-tie (Lega-asciuga) — each tied in a short tail of similar rope, laid out as if for a lesson. The rope fibres are visibly twisted, with subtle natural variation, no synthetic uniformity. The coil is shown as a still-life on a warm wooden workbench surface, against a softly out-of-focus background of an open carpentry workshop — tools hanging on pegs, a hint of a wooden facade dotted with tiny pecking holes (the picchio's signature on the wall).

Lighting: warm afternoon light from one side, the light of a craftsman's open workshop, with deep wood-tone shadows.

Color palette: pale natural-beige rope, warm wood tones of bench and tools, terracotta of the village, hint of the central tree's green. NO bright white rope, NO synthetic plastic shine, NO neon, NO black rope.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a Chardin or Vermeer interior — quiet, dignified, materially honest, the dignity of a craftsman's tool. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the rope coil with the four sample knots arranged informally around it. Frame includes the workbench surface and a hint of the workshop. Aspect ratio 4:5 (portrait).
```

---

## Variante "in uso" — Nodo con corda sul braccio

**Aspect ratio:** 4:5
**Filename atteso:** `corda_nodo_in_uso_v1.jpg` (opzionale)

```
Same style, same palette. Three-quarter view of Nodo, an adult great spotted woodpecker (picchio rosso maggiore — black and white plumage with the signature RED nape patch, sharp pointed beak), standing in his open carpentry workshop. A coil of pale natural rope is wrapped around his upper arm/wing, ready to be pulled and worked. He is mid-task, focused, beak slightly forward as if just delivered a TOK against the wood. Painterly oil-style, dignified, warm workshop light, the wooden facade behind dotted with tiny pecking holes.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. Corda **chiara naturale** (mai bianca, mai sintetica)
  2. **Coil arrotolato pulito** (signature: arrotolata sul braccio)
  3. **Quattro nodi-esempio visibili** (Otto, Scorsoio, Marinaro, Lega-asciuga)
  4. Fibre naturali visibili (twisted hemp/sisal, mai liscia)
  5. Aspetto da lavoro, mai decorativo

---

## Negative prompt

```
no synthetic rope, no plastic rope, no nylon, no climbing rope colorful, no white-bleach rope, no black rope, no neon, no satin cord, no jewellery cord, no decorative tassels, no rope ladder, no cowboy lasso, no costume prop, no theatrical, no cartoon, no anime, no 3D render, no flat vector, no logos, no text, no signatures.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`corda_nodo_v1.jpg` in `visual/oggetti/corda_nodo/immagini/`), verificare:

- [ ] **Corda chiara naturale** (hemp/sisal beige, mai bianca, mai sintetica)?
- [ ] **Arrotolata pulita** (coil signature)?
- [ ] **Quattro nodi-esempio** visibili intorno (Otto, Scorsoio, Marinaro, Lega-asciuga)?
- [ ] Fibre twisted visibili (mai liscia)?
- [ ] Aspetto da lavoro (mai decorativa, mai costume)?
- [ ] Sfondo coerente con bottega villaggio centrale (terracotta, legno caldo, eventuali buchi nella facciata)?
- [ ] Stile painterly, mai cartoon né photoreal-iper?
