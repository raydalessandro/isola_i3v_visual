# Prompt Grok Imagine — `cicatrice_grunto`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica di riferimento della cicatrice di Grunto (stambecco vecchio verde, Burrone tra le Montagne Gemelle).

> **Nota:** la cicatrice è una firma anatomica, NON un oggetto separabile dal personaggio. La canonica si genera come close-up del fianco sinistro. La cicatrice non viene mai spiegata né nominata nel testo (porta socchiusa per memoria-lunga). L'immagine deve renderla VISIBILE come fatto, mai come simbolo drammatico.

---

## Prompt principale (English, single shot)

```
Close-up detail study of the LEFT SIDE flank of Grunto, an old male ibex (stambecco) with characteristic dark moss-green fur (verde scuro come muschio bagnato — the saga's signature unique green coat). The detail focuses on a LONG, healed scar running diagonally along his left flank — a strip where no fur grows, the underlying skin visibly PALER (warm pale beige-cream) than the dark green moss-fur around it. The scar is OLD and well-healed: smooth, slightly raised, never raw, never red, never bleeding. The contrast between the dark green moss-fur and the pale skin strip is the focal element. Around the scar, the dark green fur is visibly textured, slightly damp-looking like wet moss. The scar shape is irregular but clean, suggesting an old wound that has long since closed. The viewpoint is a respectful three-quarter side view, framed close enough to show the scar clearly but not so close as to lose the surrounding flank context.

Setting: the close-up takes place against a softly out-of-focus background of a high mountain ravine — grey stone, hint of cold blue ice, dry wind atmosphere of the northern Quartiere d'Aria.

Lighting: cool diffuse mountain light, slightly overcast, the kind of bone-white-grey light that softens shadows and brings out fur and skin texture. Subtle warmth on the scar where the pale skin catches a little ambient warm light by contrast.

Color palette: dark moss-green fur (the unique saga green for Grunto), pale beige-cream scar tissue, cold grey stone, ice-blue distance, dry wind tones. NO red, NO blood, NO dramatic crimson, NO black-charred look, NO bright pink scar.

Style: realistic anatomical study painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a 19th-century natural history detail study — quiet, dignified, materially honest, NEVER theatrical, NEVER trauma-spectacular. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: the scar centered and clearly readable, the surrounding flank fur giving context, mountain background softly blurred. The subject is the QUIET TRACE — never the wound, never the violence. Aspect ratio 4:5 (portrait).
```

---

## Variante "intera figura" — Grunto a tre quarti, cicatrice visibile

**Aspect ratio:** 4:5
**Filename atteso:** `cicatrice_grunto_figura_intera_v1.jpg` (opzionale)

```
Same style, same palette. Three-quarter side view of Grunto, an old male ibex with dark moss-green fur, large curved ridged horns (now slightly weathered), QUADRUPED stance on the rocky shelf of his cave-shelter at the high ravine. He stands turned slightly to show his LEFT flank, where the long pale-beige scar is visible as a quiet trace along the dark green coat. He is calm, dignified, perhaps with head turned to look out over the ravine. Painterly oil-style, cool mountain light, bone-grey stone behind, hint of ice-blue distance.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. **Fianco sinistro** (NEVER right side — è la firma)
  2. **Cicatrice OLD/healed** — pelle pallida, MAI rossa, MAI ferita aperta
  3. Pelo verde scuro intorno (signature Grunto)
  4. Tono **quieto/dignitoso** (mai drammatico, mai trauma-spectacle)
  5. La cicatrice come fatto, mai come spiegazione

---

## Negative prompt

```
no blood, no red wound, no fresh injury, no raw flesh, no bandage, no theatrical violence, no scar drawn dramatic, no scar with stitches, no glowing scar, no magical scar, no tribal scarification pattern, no body art, no tattoo, no costume prop, no theatrical lighting, no horror style, no gritty grimdark, no cartoon, no anime, no 3D render, no flat vector, no logos, no text, no signatures.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`cicatrice_grunto_v1.jpg` in `visual/oggetti/cicatrice_grunto/immagini/`), verificare:

- [ ] **Fianco sinistro** (mai destro)?
- [ ] Cicatrice **OLD/healed** (mai rossa, mai sanguinante, mai aperta)?
- [ ] Pelle **pallida beige-cream** dove non c'è pelo?
- [ ] Pelo intorno **verde scuro muschio bagnato** (signature Grunto)?
- [ ] Tono **quieto/dignitoso** (mai drammatico/trauma)?
- [ ] Sfondo coerente con palette Quartiere d'Aria (grigio pietra, blu ghiaccio)?
- [ ] Stile painterly anatomical-study (mai horror, mai cartoon)?

---

## Note di canone (non per il prompt)

- La cicatrice **non viene mai spiegata né nominata** nel testo della saga (Bible §4.8). Il visual la mostra come fatto silenzioso.
- È testimone unico vincolato in s12 (frammento pre-Vento unico saga).
- "Porta socchiusa per memoria-lunga": l'immagine deve avere la stessa qualità — visibile ma non spiegata.
