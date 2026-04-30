# Prompt Grok Imagine — `lanterna_velata_s10`

**Versione:** 1.0
**Data:** 2026-04-30
**Scopo:** generare l'immagine canonica della lanterna di Elias nella sua versione velata di s10 (cammino notturno al Pontile). Oggetto pratico di casa, gesto canonico una-tantum.

> **Vincoli forti:** Vetro tondo con riflesso giallo, panno di lana vecchia avvolto **tre-quarti** attorno al vetro, sportellino metallico parzialmente coperto. NESSUN paesaggio. Il nero riempie 80-90% della tavola. Solo il cerchio di luce.

---

## Prompt principale (English, single shot) — versione velata s10

```
A small household oil/wax lantern, carried in the hand. The lantern has a round glass globe (vetro tondo) with a small wick burning inside (riserva di grasso/cera, stoppino), a metal frame and a small metallic side-door (sportellino) partially covered. THREE-QUARTERS of the glass globe is wrapped/swathed in a piece of OLD ROUGH WOOL CLOTH (panno di lana vecchia ruvida — warm muted brown, slightly worn, hand-bound around the glass with a simple fold, no string), so that only ONE QUARTER of the glass remains uncovered, casting a small narrow circle of warm yellow light DOWNWARD onto the ground at the carrier's feet. The cloth muffles the light: dim, intimate, soft. Around the lantern: ABSOLUTE BLACK — pure deep darkness fills 80-90% of the frame, no landscape, no horizon line, no tree silhouettes, no house outlines, NOTHING but the small circle of yellow light on a path of dry ochre autumn leaves and warm brown earth. The lantern itself is in the lower-third of the frame, at hand-height, the small bright wick visible behind the wool veil as a faint warm glow.

Lighting: ONLY the lantern's veiled yellow flame as light source. Everything else is unlit. Pitch black surroundings, the small yellow circle on the feet path, ochre dry leaves caught in the warm light, hint of brown wool clothing inside the circle.

Color palette: warm muffled yellow (veiled flame), warm brown wool wrap, faint ochre of dry leaves, dark warm brown of the path, ABSOLUTE BLACK everywhere else. NO blue moonlight, NO stars (cielo coperto), NO landscape silhouette, NO bright orange flame, NO cool tones.

Style: realistic painterly chiaroscuro, oil-on-canvas feel, painterly brushwork, slight grain. Reminiscent of a Georges de La Tour candlelit scene or a Caravaggio nocturne — quiet, dignified, the dignity of one small light in absolute night. NOT cartoon, NOT 3D render, NOT photoreal hyper-detail, NOT flat illustration.

Composition: lantern in lower-third (hand-height), small circle of yellow light on the path leaves at bottom, vast pure black above filling 80-90% of the frame. Aspect ratio 4:5 (portrait).
```

---

## Variante "lanterna ferma in cucina" — stato base senza velatura

**Aspect ratio:** 4:5
**Filename atteso:** `lanterna_velata_s10_base_v1.jpg` (opzionale)

```
Same style, same palette but warmer. The same household lantern WITHOUT the wool wrap — round glass globe, small wick lit inside, metal frame, side-door, the bright warm yellow flame casting a normal circle of light. The lantern stands on a wooden kitchen shelf in the brothers' home, against an out-of-focus warm domestic background. Painterly oil-style, dignified household still-life. NO black-out: this is the lantern AT REST, ordinary household object before s10's veiling gesture.
```

---

## Variante "alba al Pontile" — lanterna quasi spenta

**Aspect ratio:** 4:5
**Filename atteso:** `lanterna_velata_s10_alba_v1.jpg` (opzionale)

```
Same style, same palette. The same lantern (still wrapped in the wool cloth) held low at the wooden Pontile at dawn. The flame is now nearly out — a faint warm-yellow ember behind the cloth, almost invisible against the slowly rising grigio-rosa-dorato dawn light over the sea. The lantern is no longer the light source: dawn is. The wool wrap is the same, slightly dampened. Painterly oil-style, soft transitional light.
```

---

## Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly chiaroscuro. Mai cartoon, mai 3D.
- **Aspect ratio:** 4:5 (verticale).
- **Iterazione:** generare 4-6 varianti, selezionare quella che meglio rispetta:
  1. **Vetro tondo** (mai lanterna a forma rettangolare/gabbia)
  2. **Tre-quarti coperto da lana vecchia** ruvida (signature s10)
  3. **Solo cerchio di luce sui piedi** — niente paesaggio, niente skyline
  4. **Nero pieno 80-90% della tavola**
  5. Foglie secche ocra nel cerchio + marrone sentiero (palette s10)

---

## Negative prompt

```
no landscape, no horizon line, no tree silhouettes, no house outlines, no stars, no moon, no streetlight, no electric lantern, no kerosene-gas lamp, no Halloween jack-o-lantern, no Chinese paper lantern, no decorative lantern, no firefly glow, no magic glow, no bright daylight, no blue night, no cool tones, no costume prop, no theatrical, no cartoon, no anime, no 3D render, no flat vector, no logos, no text, no signatures.
```

---

## Checklist post-generazione

Prima di salvare l'immagine come canonica (`lanterna_velata_s10_v1.jpg` in `visual/oggetti/lanterna_velata_s10/immagini/`), verificare:

- [ ] **Vetro tondo** con stoppino + riserva grasso/cera?
- [ ] **Panno di lana vecchia avvolto tre-quarti** attorno al vetro?
- [ ] Sportellino metallico parzialmente coperto?
- [ ] **Cerchio piccolo di luce sui piedi**?
- [ ] **Nero assoluto** 80-90% della tavola?
- [ ] **Nessun paesaggio** (no case, no alberi, no orizzonte)?
- [ ] Foglie secche ocra + sentiero marrone visibili dentro il cerchio?
- [ ] Stile chiaroscuro De La Tour / Caravaggio (mai cartoon, mai photoreal-iper)?

---

## Note di canone (non per il prompt)

- **Gesto di velatura non spiegato** (vincolo grafo `ELIAS_GESTO_VELATURA_LANTERNA_NON_SPIEGATO`). Solo mostrato.
- Pattern formale "oggetto narrativo una-tantum di forte presenza scenica" (deferred #17).
- Dopo s10 torna in cucina, non necessariamente riappare.
- "Resistere alla tentazione di illustrare il paesaggio: nessun contorno di case, nessuna sagoma di albero. Solo il cerchio di luce."
