# Bru — Prompt per generazione immagini canoniche con Grok Imagine

> **Versione:** v1 (prima generazione canonica)
> **Data:** 2026-04-30
> **Scopo:** ottenere 4 immagini canoniche per Bru (`fronte`, `silenzio_ascolto`, `vicino_a_rovo`, `turnaround`) coerenti con stylesheet saga + canone personaggio.
> **Statura saga:** cucciolo tassino, nipote di Rovo (storia affidamento mai raccontata — porta socchiusa). Robusto come tutti i tassi ma piccolo. Bru ≈ **0.40 GU** (compatto, robusto). Presenza silenziosa che custodisce.

---

## STYLESHEET CANONICA SAGA (incolla in ogni prompt)

```
STYLE: classic European children's picture book illustration, watercolor and ink linework, hand-painted texture, warm natural light, gentle painterly atmosphere, in the tradition of Beatrix Potter, Brian Wildsmith, Ernest H. Shepard. Soft edges, visible brushstrokes, mild paper grain. Storybook composition, dignified and tender, never cartoonish. Anthropomorphic animal characters with realistic anatomy slightly stylized, expressive but never exaggerated. No outlines hard like vector art. No flat digital colors. No manga, no anime, no 3D render, no Pixar style.
```

---

## CANONE PERSONAGGIO BRU (incolla in ogni prompt)

```
CHARACTER CANON — BRU:
- Species: small young badger (tassino), nephew of Rovo the gruff adult badger (his backstory is NEVER told — door always half-closed).
- Anatomy: small but ROBUST as all badgers — compact, sturdy little body, never thin or elongated. Fur soft grey-dark (still cucciolo-soft, not yet adult-coarse). The signature white badger stripe on his head is ALREADY VISIBLE but THINNER/more delicate than Rovo's full adult stripe. Small dark paws, rounded ears.
- Eyes: black, alert, ATTENTI — and "un po' tristi anche quando è contento" (a slight sadness even when happy). Walks silently. Always carries a quiet, custodied quality underneath.
- Palette: fur grey-dark (warm dark grey, slightly brownish) — cucciolo rule §6 makes him a softer/lighter version of Rovo (grigio-marrone terra), but Bru's coat is specifically "grigio-scuro ancora morbido". White stripe head — thin/delicate. Underside paler beige-grey.
- Modalità "silenzio attento" (default): listening posture — head slightly tilted, ears forward, eyes locked but not staring, mouth closed. He LISTENS more than he speaks. Postura imitativa di Rovo (scoperta in piedi, leggermente piantata).
- Modalità "vicino a Rovo a distanza giusta": Bru positioned NEAR Rovo but with deliberate measured space — never clinging, never far. The distance itself is the gesture. When he sees Rovo arriving from far, he takes "due passi piccoli" toward him — small soft step of relief.
- NEVER:
  * Never as the center of a group scene — Bru is always at the edge, in the back, at the margin.
  * Never visibly crying — sadness stays in his eyes, never on his face as tears.
  * Never as a hero — no heroic poses, no bravura, no dramatic gestures.
  * Never narrating his own backstory through expression — the "porta socchiusa" must remain. No theatrical orphan-look.
  * Never bouncy, hyperactive, playful-loud — he plays "con misura".
  * Never adult-shaped or rendered as a small adult — clearly cucciolo, but ROBUST not delicate.
  * Never modern human clothing.
- ALWAYS:
  * Always the thin white head stripe (signature, but THINNER than Rovo's).
  * Always slightly sad-attentive black eyes (the trademark melancholy-under-calm).
  * Always silent posture — quiet body language, measured.
  * Always with the "watching/listening" quality more than the "doing" quality.
  * Always the imitative-of-Rovo body shape (compact, planted).
```

---

## IMMAGINE 1 — Bru canonica fronte (default mode)

**Aspect ratio:** 3:4 (verticale ritratto)
**Filename atteso al salvataggio:** `bru_canonica_v1_fronte.jpg`

**Prompt completo:**

```
[STYLESHEET CANONICA SAGA — incolla blocco sopra]

[CHARACTER CANON BRU — incolla blocco sopra]

SCENE: A young badger child (tassino), small but robust, standing alone in three-quarter front view on packed earth at the edge of an island village. Compact sturdy body, soft grey-dark fur (cucciolo-soft, slightly brownish-warm), the canonical white badger stripe on his head — thin and delicate, not the full adult stripe. Small dark rounded paws, soft rounded ears. Black eyes, alert and attentive, with a quiet underlying sadness even though his face is calm. Mouth closed, listening posture. Soft warm late-afternoon light, watercolor and ink linework, gentle painterly atmosphere. Background: soft blurred warm earthy tones, hint of village edge and quiet ground.

NEGATIVE: no center-stage hero pose, no theatrical orphan expression, no visible tears, no thin/delicate body (must be ROBUST/compact), no missing white stripe, no full-thick adult stripe (must be THINNER than Rovo's), no bouncy hyperactive cub, no modern clothing, no cartoon, no manga, no anime, no 3D render, no Pixar, no flat vector, no hard outlines.
```

---

## IMMAGINE 2 — Bru modalità "silenzio attento" (ascolta, imita Rovo)

**Aspect ratio:** 4:5 (verticale leggero)
**Filename atteso al salvataggio:** `bru_canonica_v1_silenzio_ascolto.jpg`

**Prompt completo:**

```
[STYLESHEET CANONICA SAGA — incolla blocco sopra]

[CHARACTER CANON BRU — incolla blocco sopra]

SCENE: The same young badger Bru, sitting at the back/edge of a small wooden island schoolroom (Stria's school) — slightly off-center in the back, NOT in the foreground. Body planted square (imitative of Rovo's compact stance), head slightly tilted in a listening posture, small ears forward. Eyes locked attentively but not staring, mouth closed. Other indistinct cubs in soft blur in the foreground/middle ground (indistinct shapes, no specific identifiable cucciolo). Bru is in the back, not the focus, but his attentive silent presence is the subject. Soft warm light from a window, watercolor and ink linework, painterly storybook atmosphere. The viewer's eye is drawn to him precisely because he is QUIET while others are visibly busy.

NEGATIVE: no Bru in the foreground center, no Bru as star of the scene, no other identifiable cubs (must stay indistinct), no visible tears, no theatrical sad gaze, no hyperactive playmates touching him, no modern clothing, no cartoon, no manga, no anime, no 3D, no Pixar.
```

---

## IMMAGINE 3 — Bru modalità "vicino a Rovo a distanza giusta"

**Aspect ratio:** 4:5 (verticale leggero)
**Filename atteso al salvataggio:** `bru_canonica_v1_vicino_a_rovo.jpg`

**Prompt completo:**

```
[STYLESHEET CANONICA SAGA — incolla blocco sopra]

[CHARACTER CANON BRU — incolla blocco sopra]

SCENE: Bru, the young badger child (compact-robust, soft grey-dark fur, thin white head stripe, sad-attentive black eyes), positioned NEAR but not touching Rovo, his gruff adult badger uncle. Rovo is the bigger figure (full thick white head stripe, weathered grey-brown earth-toned fur, dark bandana around his neck), standing on packed earth at the edge of the village or on a wooden plank. The space BETWEEN them is the gesture — measured, deliberate, neither too close (no clinging, no leaning on Rovo) nor too far. Bru's body is faintly oriented toward Rovo, mid-step (the "due passi piccoli" — two small soft steps of relief that he himself doesn't see himself making). Both characters quiet, walking in the same direction or about to. Soft warm afternoon light, watercolor and ink linework, painterly storybook tone of measured tenderness — never sentimental, never theatrical.

NEGATIVE: no Bru clinging to or hugging Rovo, no overly sentimental hand-on-shoulder gesture, no Rovo bending down theatrically, no Bru in foreground star pose, no visible tears, no Bru running, no missing distance between them (the SPACE is the point), no thick adult stripe on Bru, no modern clothing, no cartoon, no manga, no anime, no 3D, no Pixar.
```

---

## IMMAGINE 4 — Bru turnaround (4 viste)

**Aspect ratio:** 16:9 (orizzontale, 4 figure intere affiancate)
**Filename atteso al salvataggio:** `bru_turnaround_v1.jpg`

**Prompt completo:**

```
[STYLESHEET CANONICA SAGA — incolla blocco sopra]

[CHARACTER CANON BRU — incolla blocco sopra]

SCENE: Character turnaround sheet of Bru, the young badger child. Four full-body views of the same character in a single horizontal image, side by side, evenly spaced, on a neutral warm cream/off-white background: FRONT view, three-quarter LEFT view, SIDE PROFILE view (left side), BACK view. All four views show the same compact-robust young badger: soft grey-dark fur, the thin canonical white head stripe (thinner than adult Rovo's), small dark rounded paws, soft rounded ears, sad-attentive black eyes (visible in front and 3/4 views). Same scale, same proportions, same listening posture across all four views. No color shift between views, no fur-tone drift, no stripe-thickness drift. Watercolor and ink linework, painterly storybook style, model-sheet clarity. NO scene, NO background details, just the four views and a clean cream background.

NEGATIVE: no inconsistencies between views, no different fur colors, no stripe-thickness drift (must be thin in ALL views), no different sizes, no scene details, no props, no Rovo present, no other characters, no modern clothes, no theatrical sad expression, no cartoon, no manga, no anime, no 3D, no Pixar.
```

---

## Note tecniche per Grok Imagine

- Genera ogni immagine con **upload del documento canone Bru** (questo file) o copia-incolla i blocchi STYLESHEET + CHARACTER CANON in cima a ogni prompt.
- **Sempre un solo aspect ratio per immagine** — non far decidere a Grok, specifica esplicitamente.
- **Re-generation policy:** se la prima generazione non è canonica (Bru come star, lacrime visibili, posa eroica, striscia troppo spessa), rigenera fino a 3 volte con piccole variazioni di prompt prima di scartare.
- **Dopo l'approvazione**, salva con il filename canonico esatto in `visual/personaggi/individuali/cuccioli/bru/immagini/`.

---

## Negative prompt globale (incolla in coda a ogni prompt se Grok non rispetta)

```
no manga, no anime, no Pixar, no 3D render, no flat vector art, no hard digital outlines, no cartoon, no chibi, no kawaii, no modern clothing (no t-shirts, no jeans, no sneakers), no logos, no text, no signatures, no watermarks, no extra characters in scene unless required.
```

---

## Negative prompt specifici Bru

```
no Bru as center/star of group scene (he's always at edge or back), no theatrical orphan look, no visible tears (sadness stays in EYES only, never on face), no heroic poses, no bravura gestures, no Bru telling-his-story expression (porta socchiusa rule), no Bru playing loud or hyperactive, no clinging to Rovo, no thin/delicate body (he's ROBUST compact), no thick full adult stripe (must be THINNER than Rovo's), no smiling joyful cucciolo expression (his "happy" still has the slight sadness), no modern clothing.
```

---

## Checklist post-generazione (verifica canone su ogni immagine)

- [ ] Corpo compatto e robusto (mai magro/allungato)?
- [ ] Pelo grigio-scuro, morbido (non adulto)?
- [ ] Striscia bianca sulla testa **sottile** (più sottile di Rovo)?
- [ ] Occhi neri, attenti, con tristezza-sotto-la-calma?
- [ ] Postura silenziosa, in ascolto (mai esibita)?
- [ ] Margine/sfondo (mai centro scena, salvo IMMAGINE 1 ritratto)?
- [ ] Mai lacrime visibili (sadness solo negli occhi)?
- [ ] Mai posa eroica o teatrale?
- [ ] Mai aggrappato a Rovo (distanza misurata in IMMAGINE 3)?
- [ ] Stile acquerello + inchiostro storybook (mai cartoon/anime/3D)?
- [ ] Scala cucciolo (≈ 0.40 GU, robusto-compatto, più piccolo di Rovo)?

---

## Ordine di generazione consigliato

1. **IMMAGINE 4 (turnaround)** per primo — fissa la coerenza anatomica (compattezza, striscia, palette).
2. **IMMAGINE 1 (fronte)** subito dopo — la "carta d'identità" canonica.
3. **IMMAGINE 2 (silenzio attento)** — la modalità più caratteristica di Bru (ascolto, margine).
4. **IMMAGINE 3 (vicino a Rovo)** per ultima — la più complessa (richiede coerenza con Rovo + gestione "distanza giusta").

