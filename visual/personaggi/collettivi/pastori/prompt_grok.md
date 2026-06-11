# Prompt Grok — `pastori`

**Versione:** 1.0 (bozza Claude 2026-06-11 — da validare Ray)
**Scopo:** generare le illustrazioni canoniche di riferimento del gruppo-istituzione **Pastori** (pastori stagionali dei Pascoli Alti, Quartiere d'Aria nord).

> **Vincolo canonico critico (grafo s02, decisione B3):** i Pastori sono **sfondo costante delle storie, mai individuati**. Niente nomi, niente volti caratterizzati come protagonisti. Appaiono come figure collettive: sagome al margine, profili controluce, presenze a distanza rispettosa.
>
> **Oggetto-firma:** il **bastone da pastore** — battuto a terra come saluto/segnale sonoro: **TIK-TIK-TIIK** (DOC_2 §2.5). Il grafo registra anche il "sasso del campanaccio": roccia tonda nel pendio con un punto liscio in cima dove il bastone batte sempre, per radunare il gregge prima di scendere in piazza.
>
> **Riferimento:** `visual/personaggi/collettivi/pastori/scheda.md` (provvisoria) + `story_graph.json#stories.s02` + prosa definitiva s01/s02.

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

## 📐 CANONE GRUPPO — Pastori

```
GROUP — Pastori (the Shepherds):
A seasonal collective living on the HIGH MEADOWS (Pascoli Alti),
herding the goats and sheep of several families. In summer they
stay in small seasonal stone-and-wood huts on the meadows. They
are the steady background of the high paths: present, working,
never intrusive.

They are NEVER individuated by name in the saga. Render them as
GENERIC COLLECTIVE FIGURES: profiles, backs, figures against the
light, faces partly obscured (hood, distance, looking at the
flock). The reference must NOT lock a single species — Pastori
are MIXED SPECIES (sturdy mid-sized mammals suited to mountain
work). Keep them interchangeable.

SIGNATURE OBJECT: the SHEPHERD'S STAFF (long wooden walking
staff). Their greeting/signal is striking it on stone or hard
ground: TIK-TIK-TIIK. A Pastore without a staff is not readable
as a Pastore.

CLOTHING: simple heavy outdoor working clothes in wool tones
(undyed greys, ochres, earth browns) suited to wind and cold —
nothing decorative, nothing individual.
```

---

## 🎨 Posa 1 — Due Pastori al margine (saluto del bastone) — v1

**Filename atteso:** `pastori_canonica_v1_margine_saluto.jpg`
**Formato:** verticale 2:3
**Modalità Grok:** text-to-image

### ⭐ PROMPT

```
[STYLESHEET + GROUP canon above, then:]

Scene: TWO SHEPHERDS standing at the edge of a high clearing,
winter early afternoon. They have just stopped: one lowers his
staff to the ground (the TIK-TIK-TIIK greeting). Seen at a slight
distance, three-quarter or profile, faces NOT readable — hood
shadow, angle, attention turned slightly aside. Calm, unhurried,
rooted. Behind them, hints of the high meadows and a few grazing
animals as distant shapes.
```

---

## 🎨 Posa 2 — Sagome con gregge sui pendii — v1

**Filename atteso:** `pastori_canonica_v1_pendii_gregge.jpg`
**Formato:** orizzontale 16:9
**Modalità Grok:** text-to-image

### ⭐ PROMPT

```
[STYLESHEET + GROUP canon above, then:]

Scene: WIDE VIEW of the high meadows; TWO OR THREE SHEPHERD
FIGURES as small silhouettes on the slopes, staffs in hand,
among scattered white-grey goats and sheep (small distant
shapes). No faces at this distance. The group reads as part of
the landscape — the steady presence of the high paths.
```
