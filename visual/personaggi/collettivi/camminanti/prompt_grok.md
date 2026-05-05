# Prompt Grok — `camminanti`

**Versione:** 1.0
**Data:** 2026-05-05
**Scopo:** generare le illustrazioni canoniche di riferimento del gruppo-istituzione **Camminanti** (trasporto interno dell'isola).

> **Vincolo canonico critico (Bible §4.21):** i Camminanti sono **mai individuati per nome**, **mai un volto distinguibile come protagonista**, **mai si fermano a chiacchierare**. Sono presenza di sfondo / passaggio: una sagoma con la carriola che attraversa la scena. La reference canonica deve quindi rappresentarli come **figura archetipica anonima**, non come personaggio individuale.
>
> **Oggetto-firma assoluto:** la **carriola di vimini intrecciato** — MAI di legno (la carriola di legno è dei Mantenitori, vincolo di differenziazione). L'intreccio richiama la Foresta Intrecciata e il Vento Intreccio.
>
> **Riferimento:** `visual/personaggi/collettivi/camminanti/scheda.md` + Bible §4.21 + DOC_2 §2.1 (saluto del gruppo).

---

## 🎨 STYLESHEET CANONICA SAGA — riusare in OGNI prompt

```
ART STYLE — fixed for the whole saga "L'Isola dei Tre Venti":
Children's picture book illustration. Hand-drawn ink linework with
a fine, slightly textured pen — visible but soft, not heavy or graphic.
Watercolor painting on top of the linework, with gentle washes, soft
gradients, and visible paper grain texture. Earthy natural color
palette: sage greens, warm ochres, terracotta browns, cream and ivory
backgrounds, muted sky blue, soft gray stone tones. Saturation always
restrained — never neon, never glossy, never plastic.

Anthropomorphic animals in the British picture book tradition (Beatrix
Potter, Brian Wildsmith) updated with contemporary warmth and gentle
realism. Most characters stand and walk on two legs, wear simple
working clothes, have expressive faces.

Lighting: soft natural light, warm and diffuse, gentle shadows in
watercolor wash, no harsh contrasts, no dramatic chiaroscuro.

NEGATIVE: NO 3D render, NO photorealistic detail, NO oil painting
heaviness, NO anime, NO manga, NO chibi, NO disney cartoon, NO pixar,
NO flat vector, NO comic book style, NO airbrush gloss, NO neon colors,
NO dark gothic, NO horror, NO grim. European picture book for ages 4-10.
```

---

## 📐 CANONE GRUPPO — Camminanti

```
GROUP — Camminanti (the Walkers):
A loose collective on the island who carry things on foot from one
quartiere to another — the inner transport of the world. They cover
INSIDE-the-island movement (Stria flies messages, Bartolo ferries
seaward; Camminanti walk goods between places). They are NEVER
individuated by name in the saga. They appear as ANONYMOUS FIGURES
who pass — a silhouette, a back turning, a figure on a path.

SPECIES: VARIOUS — Camminanti are a mixed collective, not one species.
A given Camminante may be a hare, a fox, a hedgehog, a marten, a
generic small mammal, a bird that walks (less common), etc. But for
canonical reference render the figure with FACE PARTLY OBSCURED
(turning, hooded, in profile, looking down at the path) so as to
remain READABLE AS GENERIC. The reference must NOT lock a single
species to "the Camminante" — keep it interchangeable.

POSTURE & SCALE: bipedal, walking. Adult-sized abitante on the saga
scale — roughly 0.9-1.1 GU (similar height to a brother or slightly
larger). Always shown WALKING, never seated, never stopping.

CLOTHING: simple working garments — sturdy trousers / leggings, a
plain tunic or short jacket, a small shoulder cloth or scarf, sturdy
walking shoes/boots. Earth-tone palette: muted browns, ochres, faded
greens, dust-greys. Never bright colors, never decorative. Clothes
are visibly USED, dust on the lower trousers, lived-in.

SIGNATURE OBJECT — THE WICKER WHEELBARROW:
- Material: WOVEN WICKER (vimini intrecciato), NOT WOOD. The wicker
  is light tan / pale honey-color, with the visible plait pattern
  showing. The weave gives the wheelbarrow its characteristic
  airy-light look.
- Form: a single-wheel wheelbarrow with two long handles. The body
  (the basket) is the woven wicker — open-topped, holding the load.
- Wheel: simple wooden wheel (only the wheel may be wood — the body
  is always wicker), worn from use.
- Handles: smooth wooden poles, polished by hands.
- Load: VARIES (each Camminante carries something different) — could
  be a folded cloth bundle, a basket of fish, a sack of flour, a
  bundle of firewood, a small parcel. For the canonical reference
  render a NEUTRAL LOAD: a cloth-covered bundle or a generic cloth
  sack.
- Critically: the wicker pattern must be CLEARLY VISIBLE. The
  wheelbarrow must read AS WICKER, not as wooden plank construction
  (that is the Mantenitori wheelbarrow, distinct).

EXPRESSION & GAZE: focused, calm, slightly turned away or down. The
eyes look at the path or the load, not at the viewer. The face is
not the subject — the FIGURE-WITH-WHEELBARROW is the subject. If the
face is shown, it is gentle, weathered by air, neither smiling broadly
nor frowning.

GESTURE — THE CAMMINANTE'S GREETING (DOC_2 §2.1):
The signature gesture: WHILE WALKING (never stopping), one hand
LEAVES the wheelbarrow handle, RAISES into the air, and FALLS BACK to
the handle in a single fluid motion. The wheelbarrow continues briefly
on one hand for the duration of the greeting, then both hands return
to the handles. The greeting is a "gesture stolen from the work" —
movement is the Camminante's essence, never an interruption. NEVER
a stop, never a wave-with-both-hands, never a turn-toward-the-greeted.

COLOR PALETTE FOR THE CAMMINANTE FIGURE:
- Clothing: muted browns, faded ochre, dust-grey, soft olive
- Wheelbarrow: pale honey-tan wicker + worn wood handles
- Whatever fur/feathers (species-dependent): natural earthy tones
- Optional small scarf at neck: a single soft-saturation accent color
  (faded blue, dusty rose, dim gold) to suggest individuality
  without naming
```

---

## 🎨 Veduta 1 — Camminante archetipico in cammino — v1

**Filename atteso:** `camminanti_canonica_v1_archetipico.jpg`
**Formato:** verticale 3:4 (figura intera + carriola)
**Modalità Grok:** text-to-image

### ⭐ PROMPT

```
[STYLESHEET — paste the SAGA STYLESHEET block above]

[CHARACTER CANON — paste the CAMMINANTI canon block above]

SCENE: A SINGLE CAMMINANTE IN MID-WALK, archetypal anonymous figure
of the Walkers collective. Three-quarter back-side view (so the
figure reads as "passing through" rather than as an individuated
character facing us). The Camminante walks on a PACKED-EARTH PATH
between fields/meadows on the island — a generic transit shot, not
a specific quartiere.

POSE: in motion, mid-stride. One leg forward, one back. Both hands
ON THE WHEELBARROW HANDLES (resting state, not in greeting). Slight
forward lean, the natural posture of someone walking with a wheeled
load. Face is partly obscured by the angle (three-quarter back) — we
see the side of the head, perhaps a small scarf, the ear, a hint of
profile, NOT a full frontal portrait.

THE WHEELBARROW (signature, prominent): single-wheel wicker
wheelbarrow with visible PLAIT PATTERN, light tan / pale honey, two
wooden handles, worn wooden wheel. The basket carries a NEUTRAL
CLOTH-COVERED LOAD (a folded bundle, dust-cream cloth wrapped).
Wicker pattern clearly readable — this is the visual identifier of
the Camminanti, not the figure's species.

CONTEXT (path + landscape):
- A NARROW PACKED-EARTH PATH winding gently through low grass and
  shrub. A few small stones along the edges.
- Background: SOFT WATERCOLOR LANDSCAPE — generic rolling fields,
  hint of trees in middle distance, hint of distant village rooftops
  or hills on the horizon. NOT specific to any quartiere — the
  Camminante is "between places".
- A LIGHT BREEZE moves the grass at the path's edges (suggests Vento
  Intreccio, in keeping with the wicker symbolism).

LIGHTING: late morning or early afternoon, warm soft natural light
from the side. The Camminante's wicker wheelbarrow catches the light
and reads as luminous-tan against the muted greens and earths.

ATMOSPHERE: ORDINARY, ON-THE-MOVE, ANONYMOUS-IN-A-GOOD-WAY. The
Camminante is one of many — a figure that the village sees pass
every day without remarking. Quiet, working, used to the road.
Never tragic, never heroic, never cute.

NOT INCLUDED:
- NO INDIVIDUATED FACE — never a full frontal portrait, never a clear
  identifying species feature dominant. Three-quarter back, profile,
  hooded, looking down, partially turned — anything that keeps the
  figure ARCHETYPAL.
- NO STOPPING / NO SITTING — Camminanti are always in motion.
- NO CONVERSATION SETUP — never two figures facing each other, never
  a chat/greeting-in-progress as the subject (the canonical greeting
  is the one-hand-lifted gesture in passing — see Veduta 2 if needed).
- NO WOODEN PLANK WHEELBARROW — that is the Mantenitori. The body
  of the Camminante's wheelbarrow MUST be wicker, woven, with visible
  plait pattern.
- NO MULTIPLE WHEELS, no cart, no animal-drawn vehicle — only single-
  wheel wheelbarrow, hand-pushed.
- NO TEXT, NO writing, NO labels on the load, NO signs along the path
- NO BRIGHT COLORS on the Camminante's clothing — earth tones only.
- NO MAGICAL ELEMENT, NO sparkles, NO dramatic light, NO heroic pose
- NO MODERN ELEMENTS (no plastic, no metal cart parts, no industrial
  fasteners — the wheelbarrow is artisanal pre-industrial).
- NO POSTCARD-PRETTY background — just generic working countryside.
- NEVER refer to a specific named Camminante — this figure is
  archetypal.
```

### 🎯 Checklist Veduta 1

**Figura (anonimato canonico):**
- [ ] Sagoma in cammino, mid-stride
- [ ] Three-quarter back / profilo (NO frontale pieno)
- [ ] Volto parzialmente obscured (angolo, sciarpa, cappuccio, profilo)
- [ ] Specie generica / non locked (lettori non devono dire "è una volpe specifica")
- [ ] Postura naturale di chi spinge una carriola
- [ ] Vestiti working: bruno, ocra spento, olive, dust-grey

**Carriola di vimini (signature):**
- [ ] Materiale: VIMINI intrecciato, NON legno (CRITICO)
- [ ] Pattern dell'intreccio chiaramente visibile
- [ ] Color: pale honey-tan
- [ ] 1 ruota (di legno consumato, OK), 2 manici di legno polished
- [ ] Carico neutro: bundle di stoffa dust-cream

**Contesto:**
- [ ] Sentiero packed-earth tra prati / arbusti
- [ ] Sfondo soft watercolor generico (non quartiere-specifico)
- [ ] Brezza leggera (richiamo Vento Intreccio)
- [ ] Luce naturale warm side, mai dramatic

**Anti-cliché (Bible §4.21):**
- [ ] NO volto individuato pieno
- [ ] NO Camminante fermo / seduto
- [ ] NO conversazione in corso
- [ ] NO carriola di legno (= Mantenitori)
- [ ] NO scritte / etichette / segnaletica
- [ ] NO colori brillanti
- [ ] NO pose eroica / magica / dramatic

### 📋 Variazioni se Grok sbaglia

#### Se la carriola risulta di legno (errore Mantenitori):
> CRITICAL CORRECTION: The wheelbarrow body MUST BE WICKER (vimini
> intrecciato), NOT wooden planks. The wicker has a visible PLAIT
> PATTERN — woven strands of pale honey-tan plant material, light and
> airy. Wooden plank wheelbarrows belong to the Mantenitori, a
> different group; the Camminanti's wheelbarrow is wicker. The wicker
> echoes the Foresta Intrecciata and the Vento Intreccio symbolically.
> Only the WHEEL and HANDLES may be wood — the body/basket is wicker.

#### Se rende un volto frontale individuato:
> CORRECTION: NEVER show the Camminante's face frontally as the
> subject. The figure must read as ARCHETYPAL / ANONYMOUS — Bible
> §4.21 forbids "Camminante individuato come personaggio nominato".
> Use three-quarter back view, profile turned away, head looking down
> at the path or load, hood, partially obscured by the wheelbarrow.
> The figure is "one of many", a passer-by, not a hero.

#### Se la postura è statica / Camminante fermo:
> CORRECTION: A Camminante is ALWAYS WALKING — never stopped, never
> seated, never resting in pose. The whole identity of the group is
> "in motion". The pose must read as MID-STRIDE, with weight on one
> foot, the other lifted. The wheelbarrow is in transit, not parked.

#### Se aggiunge un secondo personaggio per dialogo:
> CORRECTION: The reference is a SINGLE Camminante archetype, alone
> on the path. NO second figure, NO conversation, NO greeting between
> two characters in the reference. (The canonical greeting gesture
> is one-hand-lifted-from-handle while still walking — that is
> Veduta 2 if needed, but Veduta 1 is the figure passing in resting
> state.)

#### Se il colore è troppo saturo:
> CORRECTION: The Camminante palette is EARTH-MUTED — faded ochre,
> dust-brown, soft olive, dim grey. Never bright. The wicker
> wheelbarrow is the brightest element (pale honey-tan), and even
> that is restrained. Working clothes, used, lived-in. The Camminante
> blends with the landscape, doesn't stand out.

---

## 🎨 Veduta 2 (opz.) — Camminante con saluto in passaggio — v1

**Filename atteso:** `camminanti_canonica_v1_saluto.jpg`
**Formato:** orizzontale 4:3 (per il movimento laterale)
**Modalità Grok:** text-to-image

### ⭐ PROMPT (compatto)

```
[STYLESHEET + CHARACTER CANON CAMMINANTI]

SCENE: a single Camminante crossing the frame from left to right
(or in profile passing through), CONTINUING TO WALK. ONE HAND HAS
LEFT THE WHEELBARROW HANDLE, raised mid-air at shoulder/head height
in a brief greeting gesture — palm open, fingers relaxed, NOT a wave,
just a hand-lifted-and-already-falling. The wheelbarrow tips slightly
because only one hand is on it, but it continues forward. The other
hand stays on its handle.

The face is in PROFILE or three-quarter forward, NOT looking at any
target — the greeting is "to whoever is there", abstract.

CONTEXT: a generic island path or piazza-edge — packed earth,
suggestion of village rooftops to one side, open path/landscape to
the other. The Camminante is passing through, not stopping.

ATMOSPHERE: the gesture is "stolen from the work" — fluid, brief,
already half-finished by the time we see it. Never a stop, never a
turn toward the greeted, never a smile-at-camera.

LIGHTING: warm side natural light, soft. Same earth-muted palette as
Veduta 1.

NOT INCLUDED:
- NO STOPPING POSE
- NO TURN-TO-FACE-VIEWER, NO smile-at-camera
- NO double wave, NO both-hands-up
- NO greeted figure visible (the gesture is to "whoever is there",
  abstract — keeping the Camminante archetypal)
- NO INDIVIDUATED FACE FRONTAL
- NO WOODEN PLANK WHEELBARROW (still wicker)
- NO TEXT, NO signs, NO modernity, NO bright colors

STYLE: as Veduta 1.
```

### 🎯 Checklist Veduta 2

- [ ] Camminante in cammino (mid-stride, mai fermo)
- [ ] Una mano staccata dal manico, alzata, palm open, fingers relaxed
- [ ] Altra mano resta sul manico (carriola continua avanti)
- [ ] Gesto "rubato al lavoro": fluido, breve
- [ ] NO volto frontale individuato
- [ ] NO figura salutata visibile
- [ ] Carriola di vimini (signature)
- [ ] Atmosfera ordinary, on-the-move

---

## 🔗 Riferimento canonico

- `visual/personaggi/collettivi/camminanti/scheda.md`
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §4.21 I CAMMINANTI (gruppo-istituzione, vincoli "mai individuati")
- `pipeline_narrativa/documenti_progetto/DOC_2_saluti_gruppi.md` §2.1 Camminanti + §3 (saluto canonico)
- `pipeline_narrativa/story_graph.json#entities.characters.camminanti` (`type: gruppo_istituzione`, `signature_object: carriola_di_vimini`)
- Differenziazione: vedi `mantenitori/scheda.md` per la carriola di legno (oggetto-firma diverso)
- Apparizione testuale canonica DOC_2 §2.1:
  > *"Una camminante attraversò la piazza con la carriola. Una mano si staccò dal manico, salì, ricadde. Gabriel alzò la sua. La carriola passò."*

## Note workflow

I Camminanti sono presenza ricorrente di sfondo / cornici (cornici DOC_4):
- s01 cornice S01-C1 (Giro D): Camminante anonimo con carriola attraversa la piazza all'alba (testuale s01, già scritto: vedi quote DOC_2 sopra)
- Possibili apparizioni come cornici saga in s06, s11 e altre dove la piazza-edge è in scena

Per scene specifiche, comporre la reference Camminante (Veduta 1 o 2) + reference luogo + character canon di altri personaggi presenti. Il Camminante resta sempre **figura di sfondo / passaggio**, mai centro narrativo dell'inquadratura.
