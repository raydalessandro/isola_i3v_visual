# Prompt Grok Imagine — `scialle_stria`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica di riferimento dello scialle di Stria (airone cenerino, maestra-zia, scuola del villaggio).

---

## Prompt principale (English, single shot)

```
A LIGHT, fine, gauzy shawl in soft pale ash-grey color (cenere chiaro — the color of cooling embers, between dove-grey and pale silver, with a hint of warm undertone). The fabric is delicate and translucent — the kind of finely-woven cotton-silk blend that drapes elegantly and sways with the slightest motion. The shawl is rectangular, with a soft fringe or a finely hemmed edge (NOT heavy tassels). Surface plain, no patterns. The shawl is shown isolated as a still-life draped over a slim wooden coat-stand or laid in a soft pool on a smooth pale stone bench, partially folded so the drape and translucency are visible. Background is softly out-of-focus interior of a tall narrow village house with a steep sloping roof — pale plastered walls, a hint of a window with morning light, a tall narrow space.

Lighting: soft cool morning light, the kind of clean elegant light that brings out the silver-grey and the softness of the fabric. Slight warmth in the shadows.

Color palette: pale ash-grey shawl as the primary subject, against pale plaster walls, soft warm wood tones. NO bright colors, NO heavy dark grey, NO blue-cool grey, NO white-pure, NO patterned fabric.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of an Edwardian interior still-life — quiet, dignified, materially honest, with the quality of "owned by someone refined". NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the shawl draped showing the translucency and the drape. Frame includes a hint of the tall narrow interior. Aspect ratio 4:5 (portrait).
```

---

## Variante "in uso" — Stria atterra e lo rimette

**Aspect ratio:** 4:5
**Filename atteso:** `scialle_stria_in_uso_v1.jpg` (opzionale)

```
Same style, same palette. Three-quarter view of Stria, an adult grey heron, slim and tall with elegant grey-ash plumage and slightly darker wing-tips, JUST landed on the small grass meadow near the village school (between the old central tree and the garden rows). She is mid-gesture: drawing the pale ash-grey shawl back over her shoulders, the shawl draping along her folded wings. Her posture is composed, neck elegant, head slightly turned. Painterly oil-style, dignified, soft morning light filtering through. The shawl movement is the focal element.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. Color **cenere chiaro** (mai grigio scuro, mai blu-grigio, mai bianco puro)
  2. **Leggero/translucido** (mai pesante, mai lana spessa)
  3. Senza pattern (no fantasie, no decorazioni)
  4. Drapeggio elegante (signature: cade lungo le ali quando atterra)
  5. Stato curato, mai sporco, mai stracciato (Stria è elegante)

---

## Negative prompt

```
no dark grey, no charcoal, no blue-grey, no pure white, no heavy wool, no thick knit, no patterned fabric, no plaid, no checkered, no embroidery, no heavy fringe, no tassels with beads, no glitter, no sequins, no synthetic shiny fabric, no scarf-with-print, no bohemian style, no costume prop, no theatrical, no cartoon, no anime, no 3D render, no flat vector, no logos, no text.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`scialle_stria_v1.jpg` in `visual/oggetti/scialle_stria/immagini/`), verificare:

- [ ] Color **cenere chiaro** (mai grigio scuro/blu, mai bianco puro)?
- [ ] Tessuto **leggero/translucido** (mai lana pesante)?
- [ ] Plain, senza pattern decorativi?
- [ ] Drapeggio elegante visibile?
- [ ] Stato curato, mai sporco/stracciato?
- [ ] Sfondo coerente con casa stretta-alta o scuola (pareti chiare, palette pale)?
- [ ] Stile painterly, mai cartoon né photoreal-iper?
