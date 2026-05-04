# Casa di Amo — Atlante vedute canoniche (prompt grok)

> **Scopo.** Reference visiva canonica per scene saga alla Casa di Amo (dimora scavata sulla scogliera est della Bocca). Workflow standard luoghi.
>
> **Riferimento canonico:** `visual/luoghi/quartiere_acqua/casa_amo/scheda.md` (3 blocchi LOCATION: ESTERNO scogliera, INTERNO dimora, ANNESSI scaletta di pietra).

---

## Indice vedute

| # | Veduta | Versione | Status |
|---|---|---|---|
| 1 | Esterno scogliera (vista dal mare/Bocca) | v1 | ⏳ in iterazione |
| 2 | Interno dimora scavata | v1 | ⏳ in iterazione |
| 3 | Scaletta di pietra (annesso) | v1 (opzionale) | da fare se serve |

---

## 🎨 Veduta 1 — Casa di Amo, esterno scogliera — v1

**Filename atteso:** `casa_amo_canonica_v1_esterno.jpg`
**Formato:** verticale 3:4 (mette in scala la scogliera) o orizzontale 4:3
**Modalità Grok:** text-to-image

### ⭐ PROMPT

```
A painterly illustrated landscape scene in the style of Beatrix Potter
and Brian Wildsmith — watercolor + thin sepia ink, warm earthy palette,
hand-drawn children's picture book aesthetic. NO PEOPLE. NO text.

[LOCATION block — incolla integralmente il blocco LOCATION (EXTERIOR —
CLIFF DWELLING) da `visual/luoghi/quartiere_acqua/casa_amo/scheda.md`,
sezione "Descrizione visiva canonica per generazione — ESTERNO"]

VIEWPOINT: from the water (or near it) looking east-up toward the
cliff. We see the rocky east cliff rising from the water's edge,
with the SMALL WOODEN HOUSE OF AMO carved/built into the upper part
of the cliff (a humble single-room dwelling with weathered wood
boards, a small window facing the water, a simple plank door, a low
stone-tile or wood roof). The STONE STAIRCASE descending from the
house to the water visible on the cliff face — natural stone steps,
worn smooth from use. Some sparse low vegetation on the cliff (small
plants, lichen). The water of the Bocca channel at the base.

LIGHTING: late morning or afternoon, warm light catching the cliff
face from the south-west, the wooden house glowing slightly with
amber tone, water below with reflections.

ATMOSPHERE: solitary, working, austere. Amo lives separate from the
village by choice. The dwelling reads as a fisherman's hermit-house,
not picturesque-tourist.

NOT INCLUDED: NO people, NO text, NO bright tropical colors, NO
crashing waves, NO lighthouse, NO modern dwelling, NO concrete, NO
ornate decoration, NO ladder (only the stone staircase).

STYLE: traditional watercolor + thin sepia ink, warm coastal palette
(grey-brown rock + dark weathered wood + sea blue/silver below +
soft sky), Beatrix Potter / Brian Wildsmith.
```

### 🎯 Checklist

- [ ] Scogliera rocciosa che sale dall'acqua
- [ ] Casa piccola in legno scuro consumato sulla parte alta della scogliera
- [ ] Tetto basso in tegole di pietra o assi di legno
- [ ] Piccola finestra rivolta verso l'acqua
- [ ] Porta semplice in legno
- [ ] Scaletta di pietra (gradini naturali) che scende dalla casa all'acqua
- [ ] Vegetazione bassa sparsa sulla scogliera (no lussureggiante)
- [ ] Acqua della Bocca alla base
- [ ] Atmosfera solitaria, austera (mai picturesque)
- [ ] NO personaggi, NO scritte, NO modernità

---

## 🎨 Veduta 2 — Interno Casa di Amo — v1

**Filename atteso:** `casa_amo_canonica_v1_interno.jpg`
**Formato:** verticale 3:4 o orizzontale 4:3

### ⭐ PROMPT

```
A painterly illustrated interior scene in the style of Beatrix Potter
and Brian Wildsmith — watercolor + thin sepia ink. NO PEOPLE. NO text.

[LOCATION block — incolla integralmente il blocco LOCATION (INTERIOR —
CLIFF DWELLING) da `visual/luoghi/quartiere_acqua/casa_amo/scheda.md`,
sezione "Descrizione visiva canonica per generazione — INTERNO"]

VIEWPOINT: three-quarter angle from the entrance looking inward,
child-perspective. We see the single-room cliff dwelling: weathered
wood walls partly carved into the rock face (so one side is bare
stone and the other is wood planks), a small window over the water,
a simple wooden bench or low bed/cot, a small fishing-tools shelf
with a few items (hooks, lines, a wooden bucket), a small fire pit
or hearth, perhaps a single oil lamp. Floor: wood planks worn smooth
or stone slabs.

LIGHTING: filtered window light from the south, warm soft amber
falling on the floor. Quiet, austere. Amo just stepped out (or is
out fishing).

ATMOSPHERE: hermit-fisherman's room. Spartan, used, alive but quiet.

NOT INCLUDED: NO people, NO text, NO modern furnishings, NO bright
artificial light, NO decorative wallpaper, NO ornate items.

STYLE: warm watercolor + thin sepia ink, palette of weathered wood +
grey rock + soft amber light + sea blue glow from window.
```

### 🎯 Checklist

- [ ] Stanza singola, parte legno parte roccia (signature: scavata nella scogliera)
- [ ] Piccola finestra con vista acqua
- [ ] Banco/giaciglio basso semplice
- [ ] Mensoletta con pochi attrezzi pesca
- [ ] Eventuale piccolo focolare/lampada a olio
- [ ] Pavimento in legno o pietra
- [ ] Atmosfera spartana, "appena lasciata"
- [ ] NO personaggi, NO scritte, NO modernità

---

## 🎨 Veduta 3 — Scaletta di pietra (annesso) — v1 (opzionale)

**Filename atteso:** `casa_amo_canonica_v1_scaletta.jpg`
**Formato:** verticale 3:4

### ⭐ PROMPT (compatto)

```
A painterly illustrated detail scene in the style of Beatrix Potter
and Brian Wildsmith — watercolor + sepia ink. NO PEOPLE. NO text.

A natural stone staircase carved into a rocky cliff face, descending
from upper cliff (where Amo's small wooden house is partly visible
top of frame) to the water at the base. The steps are weathered,
uneven, smooth from years of use. Some sparse plants growing in
crevices, lichen on the stones. A weathered wooden post or rope
handhold here and there. At the bottom: the water of La Bocca
channel.

LIGHTING: warm afternoon side light, soft shadows on the steps.

NO people, NO text, NO modern handrails, NO concrete steps.

STYLE: warm watercolor + thin sepia ink, palette grey-brown rock +
green moss + silver-blue water below.
```

---

## 🔗 Riferimento canonico

- `visual/luoghi/quartiere_acqua/casa_amo/scheda.md` (3 blocchi LOCATION)
- Bible §4.X AMO + §8.5 Quartiere d'Acqua
- Cartografia `island.geojson#features.id=casa_amo`

## Note workflow

- Veduta 1 (esterno) per scene "Amo sulla scogliera/casa", s07/s10/s11/s12
- Veduta 2 (interno) rara, eventuali cammei
- Veduta 3 (scaletta) per scene di transizione, Amo che scende all'acqua
