# Prompt Grok Imagine — `grembiule_fiamma`

**Versione:** 1.0
**Data:** 2026-04-29
**Scopo:** generare l'immagine canonica di riferimento dell'oggetto-firma "grembiule di Fiamma". L'immagine fissa l'aspetto canonico per tutte le illustrazioni successive.

---

## Prompt principale (English, single shot)

⚠️ **NOTA 2026-04-29**: questo prompt era stato scritto con stile "Vermeer/Chardin oil painting" prima della validazione della stylesheet saga. **Va rigenerato** usando la stylesheet canonica saga di `_canone/01_SAGA_STYLESHEET_v1.md` (picture book painterly, watercolor + ink, no oil painting heaviness).

Per generazione futura del grembiule, usa la stylesheet saga + il blocco descrittivo dell'oggetto sotto.

```
[USARE STYLESHEET CANONICA SAGA da _canone/01_SAGA_STYLESHEET_v1.md]

OBJECT — Fiamma's apron:
A workman's apron in heavy rough-woven linen, terracotta brick-red color, hung on a wooden peg against a warm stone wall lit by morning light from an east-facing window. The apron has a bib-style chest panel held by a strap that goes around the neck, a wide single front pocket at belly level, and long ties at the waist hanging loose. The fabric texture is coarse and visibly woven, not smooth. The whole apron is dusted with pale flour, more heavily concentrated on the right-hand side and on the belly area where hands have wiped repeatedly, leaving uneven cloudy patches and a faint thumb-print along the pocket edge. Small dark scorch marks at the lower hem and along the ties, from contact with hot embers. The apron is well-used, never new, but carefully kept — patched but not torn. No embroidery, no decorations, no patterns, no lace, no contrasting trim. Pure work garment.

Lighting: warm side light from a low window, soft amber glow of a bakery interior at sunrise. Background: rough-plastered earthen wall, slightly out of focus, in warm ochre and brick tones. A faint dusting of flour particles in the air catching the light.

Color palette: terracotta brick-red as base, ivory-white flour dust, ember-orange highlights, deep umber shadows, warm ochre wall.

Composition: centered subject, three-quarter view of the apron hung on the peg, slightly angled to show the front pocket and the texture. Frame includes the wall behind, the wooden peg, and a hint of the floor/shelf below. Aspect ratio 4:5 (portrait).
```

⚠️ Versione vecchia (con oil painting style — DEPRECATA, NON USARE):

```
A workman's apron in heavy rough-woven linen, terracotta brick-red color, hung on a wooden peg against a warm stone wall lit by morning light from an east-facing window. The apron has a bib-style chest panel held by a strap that goes around the neck, a wide single front pocket at belly level, and long ties at the waist hanging loose. The fabric texture is coarse and visibly woven, not smooth. The whole apron is dusted with pale flour, more heavily concentrated on the right-hand side and on the belly area where hands have wiped repeatedly, leaving uneven cloudy patches and a faint thumb-print along the pocket edge. Small dark scorch marks at the lower hem and along the ties, from contact with hot embers. The apron is well-used, never new, but carefully kept — patched but not torn. No embroidery, no decorations, no patterns, no lace, no contrasting trim. Pure work garment.

Lighting: warm side light from a low window, deep shadow on the opposite side, the kind of soft amber glow of a bakery interior at sunrise. Background: rough-plastered earthen wall, slightly out of focus, in warm ochre and brick tones. A faint dusting of flour particles in the air catching the light.

Color palette: terracotta brick-red (RAL 8004 / Pantone 18-1248) as base, ivory-white flour dust, ember-orange highlights, deep umber shadows, warm ochre wall. NO pure white, NO bright orange, NO pastel pink.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a Vermeer or Chardin domestic interior — quiet, dignified, materially honest. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the apron hung on the peg, slightly angled to show the front pocket and the texture. Frame includes the wall behind, the wooden peg, and a hint of the floor/shelf below. Aspect ratio 4:5 (portrait).
```

---

## Note tecniche per Grok Imagine

- **Modalità consigliata**: realistico/painterly. Evitare modalità "anime", "stylized cartoon", "hyper-detailed photo".
- **Aspect ratio**: 4:5 (verticale, classico per oggetto isolato).
- **Seed**: salvare il seed dopo la prima generazione canonica per riuso futuro in varianti.
- **Iterazione**: generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. Colore terracotta (no rosso vivo, no rosa)
  2. Texture tela ruvida visibile
  3. Pattern di farina non simmetrico
  4. Bruciature piccole solo su bordi/lacci
  5. Nessuna decorazione

## Negative prompt (se Grok lo accetta)

```
white, pure white, pristine, clean, new, embroidery, lace, frills, hearts, flowers, decorative trim, contrasting borders, cartoon, anime, kawaii, 3D render, plastic, glossy, smooth fabric, silk, polyester, polka dots, stripes, checkered pattern, blood stains, red sauce, dramatic tear, worn-out rags, costume, theatrical, bright orange, fluorescent, pink, pastel, festive
```

## Variazioni opzionali (per generazioni successive)

Una volta fissato il canone con la prima immagine, queste varianti restano dentro la "Variabilità ammessa" della scheda:

1. **Variante "in uso"**: stesso grembiule indossato (su manichino o figura neutra di volpe stilizzata), con mani che impastano, farina più densa.
2. **Variante "fine giornata"**: leggermente più scuro per impasto secco accumulato, lacci leggermente più sgualciti.
3. **Variante "S12 cornice ferma"**: appeso al chiodo, Forno spento sullo sfondo, luce più fredda di sera tardi (ma il colore base resta lo stesso).

## Cosa NON fare nelle varianti

- Non cambiare mai colore base (sempre terracotta).
- Non aggiungere mai decorazioni nuove anche per "rendere più interessante" un cammeo.
- Non far svolazzare il grembiule al vento in modo drammatico.
- Non mostrare mai il grembiule pulito, nuovo, o stracciato.
- Non sostituirlo con un altro grembiule. È sempre lo stesso, in tutte le 12 storie.

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`grembiule_fiamma_v1.png` in `visual/oggetti/grembiule_fiamma/immagini/`), verificare:

- [ ] Colore base terracotta (non rosso vivo, non arancione fuoco, non rosa)
- [ ] Texture tela grezza visibile
- [ ] Pettorale + gonna + tasca frontale + lacci posteriori
- [ ] Farina presente, non simmetrica, più densa a destra/pancia
- [ ] Bruciature piccole solo su bordi bassi e lacci (no macchie drammatiche)
- [ ] Nessuna decorazione (niente cuori, fiori, pizzi, trim)
- [ ] Luce calda da est (alba), ombra calda
- [ ] Sfondo coerente con palette Quartiere di Fuoco (terracotta/ocra/brace)
- [ ] Stile painterly, non cartoon né hyper-photoreal
