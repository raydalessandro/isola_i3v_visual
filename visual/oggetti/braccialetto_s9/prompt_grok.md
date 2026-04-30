# Prompt Grok Imagine — `braccialetto_s9`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica del braccialetto fatto da Noah per il compleanno di Gabriel (s09 introduzione, s12 bloom). Oggetto piccolo e tenero — mai descritto come importante, solo visibile.

> **Vincoli forti:** Brutto-tenero, mai disastrato. Lo sforzo di Noah è visibile. Funzionale ma non perfetto. Mai bello "da pubblicare".

---

## Prompt principale (English, single shot) — stato s09 (nuovo)

```
A small handmade child's bracelet, sized for a child's wrist, made by a young child for a brother's birthday. Materials: thin natural hemp twine (sottile cordino di canapa, warm pale-beige) tied around two short DRY twigs of young willow or hazel (each twig about a finger's length, slightly curved, bark visible, dry but not brittle), with a single raw chestnut (castagna cruda — glossy chestnut-brown, slightly waxy surface) drilled through the center as a single bead. The knot closing the bracelet is a SIMPLE variant of a sailor's knot, slightly clumsy, the loose ends still trimmed unevenly with visible cut-marks. The whole piece reads as obviously made by a small child — functional, never elegant: the twigs are not perfectly aligned, the hemp is slightly twisted, the knot is just-barely-secure. But it's clearly made WITH CARE, not thrown together — the chestnut sits roughly centered, the assembly holds. The bracelet is shown as a still-life on a warm wooden tabletop (the kitchen table of the three brothers' home), surrounded by faint hints of a celebratory evening — a corner of a chestnut cake glazed with honey (rosa bordeaux), a few autumn leaves (giallo-arancio), the warm terracotta glow of the Forno wall behind in soft blur.

Lighting: warm late-afternoon / early-evening light, the kind of golden October light filtering through a window. Slight cool grey accent (ottobre air) in the background.

Color palette: warm hemp-beige cord, warm chestnut-brown bead, dry willow-pale twigs, terracotta wall behind, marrone caldo of chestnuts, rosa bordeaux of the cake, giallo-arancio of the leaves, accent grigio chiaro of October air. NO bright primary colors, NO bright orange, NO synthetic look.

Style: realistic still-life painting, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a Vermeer domestic still-life — quiet, dignified, materially honest, the dignity of a child's careful effort. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: centered subject, three-quarter view of the bracelet laid flat showing the cord, the two twigs, the chestnut bead, and the simple knot. Frame includes the wooden tabletop and softly-blurred celebration context. Aspect ratio 4:5 (portrait).
```

---

## Variante "stato s12" — castagna-perlina rugata, al polso di Gabriel

**Aspect ratio:** 4:5
**Filename atteso:** `braccialetto_s9_stato_s12_v1.jpg` (opzionale)

```
Same style, same palette but with subtle aging. Close-up of the same bracelet, now AGED — the chestnut bead is visibly RUGATA (wrinkled, slightly shrunken with seasonal age, surface no longer waxy but matte and faintly furrowed — a quiet memento mori), the hemp twine slightly darker and softer with use, the willow twigs a touch greyer-dryer. The bracelet is now AT THE WRIST of Gabriel (the eldest brother child) — visible but never centered as the focus. Gabriel's wrist is in three-quarter, the bracelet sits naturally — not displayed, just present. Painterly oil-style, dignified, soft warm light of the saga's closing scene. NEVER described as important — just visible.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. **Brutto-tenero** (mai elegante, mai disastrato — la zona è esattamente "fatto da un bambino con cura")
  2. **Tre materiali specifici** (canapa + 2 ramoscelli + 1 castagna cruda)
  3. **Nodo Marinaro semplice** (mai elaborato, mai sciatto)
  4. Stato **nuovo** in s09 / **rugato** in s12 (castagna invecchiata)
  5. Mai messo in scena drammatica, mai presentato come "speciale"

---

## Negative prompt

```
no elegant jewellery, no perfect symmetric beads, no metal charm bracelet, no string-and-plastic-bead bracelet, no friendship bracelet woven pattern, no rainbow colors, no glitter, no sequins, no professional craft look, no kit-instructions perfection, no synthetic cord, no nylon string, no plastic chestnut, no painted twigs, no decorative ribbon, no gift wrap with bracelet, no costume prop, no theatrical lighting, no jewellery shop styling, no cartoon, no anime, no 3D render, no flat vector, no logos, no text.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`braccialetto_s9_v1.jpg` in `visual/oggetti/braccialetto_s9/immagini/`), verificare:

- [ ] **Brutto-tenero** (sforzo bambino visibile, mai elegante, mai disastrato)?
- [ ] **Cordino canapa sottile**?
- [ ] **Due ramoscelli salice/nocciolo** (secchi ma non fragili)?
- [ ] **Una castagna cruda forata** (perlina centrale)?
- [ ] **Nodo Marinaro semplice** (variante a maglia di un bambino)?
- [ ] Stato adeguato (nuovo in s09 / castagna rugata in s12)?
- [ ] Sfondo coerente con palette emotiva s09 (terracotta+marrone+rosa bordeaux+giallo-arancio+grigio chiaro)?
- [ ] Stile painterly Vermeer-domestico (mai cartoon, mai jewellery shop)?

---

## Note di canone (non per il prompt)

- Vincolo grafo: `description_constraint: mai_descritto_dopo_s09`. In s12 visibile ma mai chiamato per nome né descritto.
- In s09 sul tavolo per tutto il dolce → poi Gabriel lo prende in mano a fine sera (hook `vh_s09_fine_sera_braccialetto_in_mano_gabriel_noah_ride`).
- In s12 al polso di Gabriel = bloom (debt `debt_s09_to_s12_braccialetto_al_polso_gabriel`).
- Memento mori stagionale involontario (Fase E): la castagna-perlina si ruga / si ristringe.
