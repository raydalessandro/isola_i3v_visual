# Toba — Prompt per generazione immagini canoniche con Grok Imagine

> **Versione:** v1 (prima generazione canonica)
> **Data:** 2026-04-30
> **Scopo:** ottenere 4 immagini canoniche per Toba (`fronte`, `domanda`, `barca_padre`, `turnaround`) coerenti con stylesheet saga + canone personaggio.
> **Statura saga:** cucciola di Bartolo. Tartarughina. Guscio "appena più grande di una mano umana". Significativamente più piccola del padre (Bartolo è già basso/largo: ~0.55 GU). Toba ≈ **0.25 GU** (poco più di un guscio-mano + zampe corte). Cucciolo della domanda che apre.

---

## STYLESHEET CANONICA SAGA (incolla in ogni prompt)

```
STYLE: classic European children's picture book illustration, watercolor and ink linework, hand-painted texture, warm natural light, gentle painterly atmosphere, in the tradition of Beatrix Potter, Brian Wildsmith, Ernest H. Shepard. Soft edges, visible brushstrokes, mild paper grain. Storybook composition, dignified and tender, never cartoonish. Anthropomorphic animal characters with realistic anatomy slightly stylized, expressive but never exaggerated. No outlines hard like vector art. No flat digital colors. No manga, no anime, no 3D render, no Pixar style.
```

---

## CANONE PERSONAGGIO TOBA (incolla in ogni prompt)

```
CHARACTER CANON — TOBA:
- Species: small young tortoise (tartarughina), daughter of Bartolo the old tortoise carpenter.
- Anatomy: shell appena più grande di una mano umana (about the size of a child's hand), CHIARO — paler/lighter than her father's dark sea-green shell, marked with thin yellow stripes on the dome. Short, rounded little legs. Big round eyes for her muzzle, always slightly open with curiosity. Slightly faster than Bartolo but still unmistakably a tortoise — never running, never sprinting.
- Palette: shell pale sea-green with yellow thin stripes (cucciolo rule §6: lighter/softer version of adult Bartolo's deep antique sea-green). Skin warm beige-olive on legs and head. Eyes: dark, big, alert.
- Modalità "domanda concreta" (default): head extended a bit out of shell, eyes wide and direct, mouth slightly open as if just starting to say "Perché?" or "E poi?". Expression curious, never philosophical, never lost in space — always pointed at a concrete thing nearby.
- Modalità "in barca col padre": Toba on a small wooden boat with Bartolo, often watching him work or scanning the water with the same big-eyed curiosity. Adores being on the water with her father.
- NEVER:
  * Never running or sprinting (she's a tortoise, just a bit faster than Bartolo).
  * Never alone on a pier or dock — Toba is never abandoned/solo on the pontile.
  * Never with a "philosophical/dreamy" gaze (eyes lost in space). Her curiosity is always concrete, focused on something specific.
  * Never adult-shaped or rendered as a small adult — she is clearly a CUCCIOLO (cub).
  * Never with a dark adult shell — her shell must be paler than Bartolo's, with the canonical yellow thin stripes.
  * Never modern human clothing (no t-shirts, no sneakers).
- ALWAYS:
  * Always the hand-sized pale shell with thin yellow stripes (THIS IS HER SIGNATURE).
  * Always short rounded legs, never elongated.
  * Always big round alert eyes.
  * Always with the soft tender quality of a young creature.
```

---

## IMMAGINE 1 — Toba canonica fronte (default mode)

**Aspect ratio:** 3:4 (verticale ritratto)
**Filename atteso al salvataggio:** `toba_canonica_v1_fronte.jpg`

**Prompt completo:**

```
[STYLESHEET CANONICA SAGA — incolla blocco sopra]

[CHARACTER CANON TOBA — incolla blocco sopra]

SCENE: A young tortoise child (tartarughina), daughter of an old tortoise carpenter. Standing alone in three-quarter front view, on warm wooden planks of a small island village. Her shell is about the size of a human hand — pale sea-green, decorated with thin yellow stripes running along the dome. Short rounded little legs, warm beige-olive skin. Head extended slightly out of the shell, big round dark eyes wide open with concrete curiosity, mouth just barely parted as if about to ask a small question. Soft warm afternoon light, watercolor and ink linework, gentle painterly atmosphere, dignified and tender. Background: soft blurred warm tones, hint of village wood and sea glow, no distracting elements.

NEGATIVE: no philosophical dreamy gaze, no eyes lost in space, no running pose, no sprinting, no dark adult shell (must be PALE with yellow stripes), no shell larger than a hand, no elongated legs, no adult tortoise proportions, no modern clothing, no cartoon style, no manga, no anime, no 3D render, no Pixar, no flat vector, no hard outlines.
```

---

## IMMAGINE 2 — Toba modalità "domanda concreta"

**Aspect ratio:** 4:5 (verticale leggero)
**Filename atteso al salvataggio:** `toba_canonica_v1_domanda.jpg`

**Prompt completo:**

```
[STYLESHEET CANONICA SAGA — incolla blocco sopra]

[CHARACTER CANON TOBA — incolla blocco sopra]

SCENE: The same young tortoise child Toba (hand-sized pale sea-green shell with thin yellow stripes), standing in front of a low wooden workbench in Bartolo's carpentry corner. Head fully extended out of the shell, neck stretched up, big round eyes locked onto a specific concrete object on the bench (a small carved wooden curl, a chip of wood, a tool) — her gaze is sharply focused on THAT thing, never drifting. Mouth slightly open, mid-question — "Perché?" or "E poi?". Front little legs lifted just barely against the bench edge. Curiosity is concrete, child-like, alive. Watercolor and ink linework, warm light from a workshop window, soft painterly atmosphere.

NEGATIVE: no dreamy/philosophical gaze (eyes must be FOCUSED on a concrete object, never lost in space), no running, no abandoned/solo pier scene, no dark shell, no shell bigger than a hand, no adult proportions, no philosophical-poet pose, no cartoon, no manga, no anime, no 3D, no Pixar.
```

---

## IMMAGINE 3 — Toba modalità "in barca col padre"

**Aspect ratio:** 4:5 (verticale leggero)
**Filename atteso al salvataggio:** `toba_canonica_v1_barca_padre.jpg`

**Prompt completo:**

```
[STYLESHEET CANONICA SAGA — incolla blocco sopra]

[CHARACTER CANON TOBA — incolla blocco sopra]

SCENE: Toba, the young tortoise child (hand-sized pale sea-green shell with thin yellow stripes), on a small wooden island fishing boat together with her father Bartolo (an old, larger tortoise with a deep antique sea-green shell, dark and pale-scarred). Toba is positioned near the edge of the boat, head extended out of her shell, big round eyes wide and curious as she watches her father working with the wood — or scanning the calm water beside the hull. Posture small, attentive, joyful in a quiet way (she ADORES being on the water with him). Bartolo is calm, focused, slightly stooped over his work, the older shell visible behind/beside her as visual contrast (PALE Toba shell + DARK Bartolo shell side by side). Soft warm late-afternoon light over the water, watercolor and ink linework, painterly storybook atmosphere.

NEGATIVE: no Toba alone on a pier or dock (she must be WITH her father), no Toba running, no philosophical dreamy gaze, no shell darker than father's (must be paler), no adult-like Toba, no shell bigger than a hand, no modern clothes, no cartoon, no manga, no anime, no 3D render, no Pixar.
```

---

## IMMAGINE 4 — Toba turnaround (4 viste)

**Aspect ratio:** 16:9 (orizzontale, 4 figure intere affiancate)
**Filename atteso al salvataggio:** `toba_turnaround_v1.jpg`

**Prompt completo:**

```
[STYLESHEET CANONICA SAGA — incolla blocco sopra]

[CHARACTER CANON TOBA — incolla blocco sopra]

SCENE: Character turnaround sheet of Toba, the young tortoise child. Four full-body views of the same character in a single horizontal image, side by side, evenly spaced, on a neutral warm cream/off-white background: FRONT view, three-quarter LEFT view, SIDE PROFILE view (left side), BACK view. All four views show the same young tortoise: hand-sized PALE sea-green shell with thin yellow stripes running along the dome, short rounded beige-olive legs, warm beige-olive head and neck, big round dark alert eyes (visible in front and 3/4 views). Same scale, same proportions, same posture across all four views. No color shift between views, no shell-color drift. Watercolor and ink linework, painterly storybook style, model-sheet clarity. NO scene, NO background details, just the four views and a clean cream background.

NEGATIVE: no inconsistencies between views, no different shell colors, no different sizes, no scene details, no props, no background environment, no modern clothes, no philosophical gaze, no running pose, no shell bigger than a hand, no dark adult shell, no cartoon, no manga, no anime, no 3D, no Pixar.
```

---

## Note tecniche per Grok Imagine

- Genera ogni immagine con **upload del documento canone Toba** (questo file) o copia-incolla i blocchi STYLESHEET + CHARACTER CANON in cima a ogni prompt.
- **Sempre un solo aspect ratio per immagine** — non far decidere a Grok, specifica esplicitamente.
- **Re-generation policy:** se la prima generazione non è canonica (guscio scuro come padre, occhi persi, in fuga, troppo grande, modalità sbagliata), rigenera fino a 3 volte con piccole variazioni di prompt prima di scartare.
- **Dopo l'approvazione**, salva con il filename canonico esatto in `visual/personaggi/individuali/cuccioli/toba/immagini/`.

---

## Negative prompt globale (incolla in coda a ogni prompt se Grok non rispetta)

```
no manga, no anime, no Pixar, no 3D render, no flat vector art, no hard digital outlines, no cartoon, no chibi, no kawaii, no modern clothing (no t-shirts, no jeans, no sneakers), no logos, no text, no signatures, no watermarks, no extra characters in scene unless required.
```

---

## Negative prompt specifici Toba

```
no Toba running or sprinting (she's a tortoise — slow with cub-fretta, never racing), no Toba alone on a pier or dock (she's never abandoned/solo on the pontile), no philosophical dreamy gaze with eyes lost in space (curiosity must be CONCRETE — pointed at a specific object/person), no shell darker than her father Bartolo's (her shell is PALER, with thin yellow stripes), no shell bigger than a human hand, no elongated adult legs, no adult tortoise proportions, no missing yellow stripes (signature visual), no modern human clothing.
```

---

## Checklist post-generazione (verifica canone su ogni immagine)

- [ ] Guscio piccolo (poco più di una mano umana)?
- [ ] Guscio PIÙ CHIARO di Bartolo (verde mare antico)?
- [ ] Righe gialle sottili sulla cupola del guscio (firma)?
- [ ] Zampe corte e tonde (mai allungate)?
- [ ] Occhi grandi e tondi, vigili e curiosi?
- [ ] Sguardo CONCRETO (mai perso nel vuoto, mai filosofico-sognante)?
- [ ] Postura tartaruga (mai in corsa, mai sprint)?
- [ ] Mai sola al pontile (in IMMAGINE 3 deve essere CON Bartolo)?
- [ ] Stile acquerello + inchiostro storybook (mai cartoon/anime/3D)?
- [ ] Scala cucciola (≈ 0.25 GU, significativamente più piccola di Bartolo già basso/largo)?

---

## Ordine di generazione consigliato

1. **IMMAGINE 4 (turnaround)** per primo — fissa la coerenza anatomica (scala, guscio, zampe, palette).
2. **IMMAGINE 1 (fronte)** subito dopo — la "carta d'identità" canonica.
3. **IMMAGINE 2 (domanda)** — la modalità più caratteristica di Toba.
4. **IMMAGINE 3 (in barca col padre)** per ultima — la più complessa (richiede coerenza con Bartolo).

