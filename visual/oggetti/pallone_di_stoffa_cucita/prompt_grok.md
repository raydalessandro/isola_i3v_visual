# Prompt Grok Imagine — `pallone_di_stoffa_cucita`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica del pallone di stoffa cucita dei tre fratelli (oggetto-perno s03, bloom s11). Oggetto di scena ricorrente, NON tra i 13 oggetti-simbolo saga.

> **Vincoli forti:** Stoffa cucita a mano, sferico imperfetto, non rimbalza come un pallone moderno, pesa di più. Oggetto di gioco. Appartiene al gruppo cuccioli, non a un singolo.

---

## Prompt principale (English, single shot)

```
A handmade child's ball, sewn together from PIECES OF CLOTH (panels of fabric stitched by hand with visible thread). The ball is roughly spherical but IMPERFECT — clearly hand-shaped, slightly lumpy where the stuffing settles unevenly, the seams visibly hand-sewn with simple running stitches in slightly variegated thread. The fabric panels are of mixed materials and tones: warm undyed linen-cream, faded ochre, soft red-rust, dusty brown, perhaps a single panel in muted blue — all in muted natural-dye tones, warm and quiet, never primary-bright. The size is roughly that of a child's two cupped hands. The surface shows visible wear: small smudges of grass-green at the bottom, dusty earth on one side, a small darker patch where it has been patched once. NO logos, NO printed designs, NO panels of synthetic geometry — just hand-cut hand-sewn cloth. The stuffing inside is suggested by the slight density and the way the ball reads as HEAVIER than an inflated ball would be (it does NOT bounce like a modern ball — it ROLLS).

Setting: shown isolated as a still-life on warm summer earth at the edge of a forest path (the margin of the Foresta Intrecciata) OR on the warm cobbles/packed earth of the village square (piazza con Albero Vecchio). A few fallen leaves or small grasses around suggest the outdoor play scene. Background softly out-of-focus.

Lighting: warm late-afternoon natural light, soft golden tone with gentle shadows on the uneven seamed surface — the kind of light that brings out the hand-stitched texture and the worn-in quality.

Color palette: muted natural earth tones — undyed linen-cream, faded ochre, dusty rust, soft brown, occasional muted blue. Background warm earth tones, hint of forest green or village terracotta. NO bright primary colors, NO neon, NO black-and-white pattern, NO commercial sports-ball look.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of an early-20th-century rural-childhood still-life — quiet, dignified, materially honest, the dignity of a hand-made play object. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the ball showing the hand-stitched panels and the imperfect spherical shape. Frame includes warm earth ground around it. Aspect ratio 4:5 (portrait).
```

---

## Variante "in gioco s03" — pallone fermo a un passo dal margine della Foresta

**Aspect ratio:** 4:5
**Filename atteso:** `pallone_di_stoffa_cucita_s03_v1.jpg` (opzionale)

```
Same style, same palette. The same handmade cloth ball at REST on the warm dry earth, just a single step from the dark, dense edge of the Foresta Intrecciata (deep green-brown forest interior softly out of focus). The ball is precisely placed, almost reverently — as if just gently set down rather than thrown back. NO figures visible, only the ball and the threshold of forest behind it (suggesting Rovo's quiet act of returning it). Painterly oil-style, dignified, late-afternoon warm light at the forest margin.
```

---

## Variante "festa raccolto s11" — pallone in mezzo ai giochi cuccioli

**Aspect ratio:** 4:5
**Filename atteso:** `pallone_di_stoffa_cucita_s11_v1.jpg` (opzionale)

```
Same style, same palette. The same handmade cloth ball mid-roll on the warm cobbles of the village square during the harvest festival — slightly more dust on it than s03, hint of a freshly-tied small repair on one seam (it's been played with for stories). Around it: softly-blurred legs and paws of indistinct cuccioli (NOT identifiable specific children, just a hint of the group), warm festive bunting in the periphery, the green of the Albero Vecchio's canopy above out of focus. Painterly oil-style, dignified, warm late-afternoon festival light.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. **Stoffa cucita a mano** (mai gomma, mai cuoio, mai sintetico)
  2. **Sferico imperfetto** (mai geometrico-perfetto)
  3. **Cuciture visibili a mano** (running stitch, mai industriale)
  4. **Toni naturali muti** (mai colori primari, mai pallone-sport moderno)
  5. **Pesa di più di un pallone gonfio** — leggibile dal modo in cui poggia/rotola

---

## Negative prompt

```
no rubber ball, no leather ball, no soccer ball pattern, no basketball, no football, no volleyball, no inflatable ball, no synthetic shine, no plastic, no commercial sports logo, no hexagonal panel pattern, no black-and-white panels, no bright neon, no rainbow colors, no glitter, no clown ball, no juggling ball decorative pattern, no gift bow, no costume prop, no theatrical, no cartoon, no anime, no 3D render, no flat vector, no logos, no text, no signatures.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`pallone_di_stoffa_cucita_v1.jpg` in `visual/oggetti/pallone_di_stoffa_cucita/immagini/`), verificare:

- [ ] **Stoffa cucita a mano** (panels, mai pelle/gomma)?
- [ ] **Sferico imperfetto** (mai geometrico)?
- [ ] **Running stitch visibile**?
- [ ] **Toni naturali muti** (lino crema, ocra, ruggine, marrone, eventuale blu muto)?
- [ ] **Aspetto vissuto** (smudge erba/terra, patch di riparazione)?
- [ ] **Mai logo / mai pattern commerciale**?
- [ ] Sfondo coerente (forest margin in s03 / piazza in s11)?
- [ ] Stile painterly rural-childhood still-life (mai cartoon né photoreal-iper)?

---

## Note di canone (non per il prompt)

- `oggetto_di_scena_ricorrente`, **non** uno dei 13 `oggetto_simbolo_saga` (REGOLA 0.6 fase E mis_004).
- Appartiene al **gruppo cuccioli/fratelli**, mai a un singolo personaggio.
- s03: oggetto-perno (calcio mal misurato Noah → oltre margine Foresta → Rovo lo restituisce a un passo).
- s11: ricomparsa nei giochi cuccioli durante festa raccolto = bloom collettivo seed s03.
- Coerenza cross-scena: stessa fattura, stesso aspetto vissuto (più rovinato in s11 rispetto a s03).
