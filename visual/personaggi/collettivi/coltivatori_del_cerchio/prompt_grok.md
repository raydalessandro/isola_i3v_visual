# Prompt Grok — `coltivatori_del_cerchio`

**Versione:** 1.0 (bozza Claude 2026-06-11 — da validare Ray)
**Scopo:** generare le illustrazioni canoniche di riferimento del gruppo-istituzione **Coltivatori del Cerchio** (lavoro agricolo corale, Orti del Cerchio, Quartiere di Terra ovest).

> **Vincolo canonico (scheda):** gruppo eterogeneo di varie specie; **nessuno è nominato individualmente** (Zolla è affine di mestiere ma è personaggio a parte). Renderli come coralità: figure al lavoro, mai un volto-protagonista.
>
> **Oggetto-simbolo canonico (scheda):** la **zappa con manico curvo** — portata sulla spalla quando attraversano il villaggio; il manico curvo richiama il Cerchio.
>
> **Firma sonora (prosa s03 + grafo):** la **cantilena bassa** mentre zappano e il **TUM-tum-TUM** delle zappe sulle zolle; quando qualcuno passa, la cantilena cambia di un tono per un battito (saluto senza parole).
>
> **Riferimento:** `visual/personaggi/collettivi/coltivatori_del_cerchio/scheda.md` + prosa definitiva s03 h02.

---

## 🎨 STYLESHEET CANONICA SAGA — riusare in OGNI prompt

```
[identico al blocco stylesheet saga — vedi camminanti/prompt_grok.md
o _visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md]
```

---

## 📐 CANONE GRUPPO — Coltivatori del Cerchio

```
GROUP — Coltivatori del Cerchio (the Circle Growers):
A mixed-species collective working the ORTI DEL CERCHIO — vegetable
gardens and small fields arranged in CONCENTRIC BANDS around the
village, west side (Quartiere di Terra). They live in small houses
scattered among the gardens and at the forest's edge.

They are NEVER individuated by name. Render them as WORKING
FIGURES: bent over the soil, seen from behind or in profile,
faces shaded by simple hats or turned to the ground. Mixed
species, interchangeable — the group is the character.

SIGNATURE OBJECT: the HOE WITH A CURVED HANDLE (zappa dal manico
curvo) — carried over the shoulder when crossing the village.
The curve of the handle quietly echoes the Circle of their
gardens. Every Coltivatore has one.

SOUND OF THE GROUP (for scene context, not renderable): a low
shared work-chant while hoeing, and the TUM-tum-TUM of hoes on
the last clods of the day.

CLOTHING: plain earth-toned working clothes (ochre, clay brown,
faded green aprons), worn and practical.
```

---

## 🎨 Posa 1 — Al lavoro negli Orti, fine giornata — v1

**Filename atteso:** `coltivatori_del_cerchio_canonica_v1_lavoro_tramonto.jpg`
**Formato:** orizzontale 16:9
**Modalità Grok:** text-to-image

### ⭐ PROMPT

```
[STYLESHEET + GROUP canon above, then:]

Scene: LATE AFTERNOON in winter, low golden-grey light. THREE OR
FOUR COLTIVATORI working the last clods of the day in the
concentric garden bands — bent figures, curved-handle hoes rising
and falling, no readable faces. The rhythm of shared work made
visible: same gesture at different moments. Garden rows curving
gently (the Circle). Village rooftops hinted far behind.
```

---

## 🎨 Posa 2 — Attraversamento col manico in spalla — v1

**Filename atteso:** `coltivatori_del_cerchio_canonica_v1_attraversamento.jpg`
**Formato:** verticale 2:3
**Modalità Grok:** text-to-image

### ⭐ PROMPT

```
[STYLESHEET + GROUP canon above, then:]

Scene: A SINGLE COLTIVATORE seen from behind / three-quarter
back, crossing toward the village at dusk, the CURVED-HANDLE HOE
over the shoulder — the curve of the handle clearly readable
against the sky. Face not visible. A figure of the working day
ending. Generic, interchangeable, dignified.
```
