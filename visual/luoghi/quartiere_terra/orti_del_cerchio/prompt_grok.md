# Orti del Cerchio — Atlante vedute canoniche (prompt grok)

> **Scopo.** Reference visiva canonica per scene saga agli Orti del Cerchio (3 fasce concentriche di campi/orti attorno al Villaggio centrale, Quartiere di Terra ovest, dimora dei Coltivatori del Cerchio). Luogo ricorrente: s03, s04, s05, s11.
>
> **Riferimento canonico:** `visual/luoghi/quartiere_terra/orti_del_cerchio/scheda.md` (1 blocco LOCATION ESTERNO con descrizione delle 3 fasce concentriche).

---

## Indice vedute

| # | Veduta | Versione | Status |
|---|---|---|---|
| 1 | Panoramica delle 3 fasce | v1 | ⏳ in iterazione |
| 2 | Dettaglio fila di Coltivatori al lavoro (sfondo) | v1 (opzionale) | da fare se serve |

---

## 🎨 Veduta 1 — Orti del Cerchio, panoramica delle 3 fasce — v1

**Filename atteso:** `orti_del_cerchio_canonica_v1_panoramica.jpg`
**Formato:** orizzontale 16:9 (panoramic establishing) — ideale per mostrare la disposizione concentrica
**Modalità Grok:** text-to-image

### ⭐ PROMPT

```
A painterly illustrated landscape scene in the style of Beatrix Potter
and Brian Wildsmith — watercolor + thin sepia ink, warm earthy palette,
hand-drawn children's picture book aesthetic. Horizontal panoramic
composition. NO PEOPLE. NO text, NO writing, NO signs.

[LOCATION block — incolla integralmente il blocco LOCATION (EXTERIOR —
CONCENTRIC GARDEN FIELDS) da
`visual/luoghi/quartiere_terra/orti_del_cerchio/scheda.md`,
sezione "Descrizione visiva canonica per generazione — ESTERNO"]

VIEWPOINT: from a slightly elevated angle on the village side (east),
looking west across the Orti toward the margin of the Foresta
Intrecciata. Three-quarter perspective. The composition shows the
THREE CONCENTRIC RINGS of cultivated fields:
- INNER RING (closest to the village, foreground): smaller plots
  with vegetable rows, herbs, low fruit trees, well-tended
- MIDDLE RING: larger fields with grain crops or root vegetables,
  divided by low stone walls or simple paths, working scale
- OUTER RING (furthest, near forest margin): rougher fields with
  scrubby crops, transitioning to wild grass and the dark green
  edge of the FORESTA INTRECCIATA in the far background

Earth paths radiate between the rings (concentric and radial). Low
dry-stone walls or wooden fences separate the plots, but there is
NO fortification — the rings are visible as organization, not
barrier. Some sentieri (paths) cross the rings, including the
canonical SENTIERO ORTI-TORRENTE-FORESTA (visible heading west from
the inner ring, crossing the outer ring, disappearing into the
forest margin).

ELEMENTS:
- A few small clay water jugs at the edges of plots
- Wooden tools (hoes, baskets) leaning against stone walls
- Wicker baskets here and there with harvest
- Possibly a humble small wooden shelter (proofing/storage) at the
  edge of the middle ring
- Vegetation: rows of healthy crops in inner+middle, transitioning
  to wilder grass at the outer ring
- Low scattered wildflowers along the path edges

LIGHTING: morning or afternoon, warm natural light, the sun coming
from the south/southeast, soft shadows. The light should differentiate
the rings — inner well-lit and tended, middle warmer, outer in
softer tones blending with the forest edge.

ATMOSPHERE: organized, working, alive but currently empty (the
Coltivatori have stepped away or are in a different field). The
"ring of cultivation" feels ancient, generational, lived-in. The
composition should communicate the CIRCULAR organization without
being aggressively geometric — the rings are organic, irregular,
human-built over time.

NOT INCLUDED: NO people (Coltivatori absent in this reference), NO
text, NO modern farm machinery, NO greenhouses, NO plastic, NO
chemical sprays/equipment, NO straight industrial fields, NO
postcard-perfect arrangement, NO bright tropical colors, NO
watermelon-stand colors. Sound implied by silence — the cantilena
of the Coltivatori is NOT singing now (they're absent).

STYLE: traditional watercolor + thin sepia ink, warm earth palette
(deep green crops + ochre soil + sage green grass + dark green
forest edge + warm gold sunlight + grey-brown stone walls).
Beatrix Potter / Brian Wildsmith. Mood: working, ancient, organized.
```

### 🎯 Checklist

- [ ] 3 fasce concentriche distinguibili (interna/media/esterna)
- [ ] Fascia interna: orti piccoli con righe ben curate (verdure, erbe, alberi bassi)
- [ ] Fascia media: campi più grandi (cereali, radici), muretti a secco bassi
- [ ] Fascia esterna: campi più rustici, transitioning verso erba selvatica
- [ ] Margine Foresta Intrecciata visibile in fondo (verde scuro denso)
- [ ] Sentieri radiali e concentrici tra le fasce
- [ ] Sentiero verso Foresta visibile (canonical sentiero_orti_torrente_foresta)
- [ ] Muretti a secco / staccionate in legno (NO recinzioni alte)
- [ ] Eventuali vasi/cesti/attrezzi sui bordi
- [ ] Atmosfera "lavoro in pausa" (Coltivatori assenti)
- [ ] NO personaggi, NO scritte
- [ ] NO modernità (no macchinari, no plastica, no serre)
- [ ] Stile painterly watercolor + sepia ink

### 📋 Variazioni se Grok sbaglia

#### Se non si vedono le 3 fasce concentriche:
> CRITICAL CORRECTION: The garden MUST show THREE CONCENTRIC RINGS,
> visibly different in scale and crop type. INNER ring smallest with
> tended vegetable rows, MIDDLE ring larger with grain/root crops,
> OUTER ring roughest near the forest. The concentric organization
> is the canonical signature of "Orti del Cerchio". Use a slightly
> elevated viewpoint (from east) to make the rings legible across
> the panorama.

#### Se rende troppo "fattoria moderna":
> CORRECTION: This is a PRE-INDUSTRIAL community garden ring, NOT a
> modern farm. NO straight machine-plowed rows, NO greenhouses, NO
> tractors, NO plastic mulch, NO industrial irrigation. The fields
> are organized but irregularly, hand-worked, with low dry-stone
> walls and earth paths. Tools are wooden hoes and wicker baskets.

#### Se manca il margine Foresta:
> CORRECTION: The dark green edge of the FORESTA INTRECCIATA must be
> visible in the BACKGROUND beyond the outer ring. The forest is
> dense, deep green, slightly mysterious. The Orti meet the Foresta
> at the outer ring — this transition is canonical (the sentiero
> goes from Orti through Foresta to Torrente).

#### Se mette personaggi:
> CRITICAL: NO PEOPLE in this image. The Coltivatori are absent
> right now. NO singing figures, NO working bodies. The reference
> shows the place itself, ready for scenes to be composed on top.

---

## 🎨 Veduta 2 — Coltivatori in fila al lavoro (opzionale) — v1

**Filename atteso:** `orti_del_cerchio_canonica_v1_coltivatori_fila.jpg`
**Formato:** orizzontale 16:9
**Note:** questa veduta opzionale serve solo se si vuole una reference già con i Coltivatori in scena (non vuota). Da generare DOPO che il character canon dei Coltivatori del Cerchio sarà definito.

```
[Da scrivere quando il character canon Coltivatori sarà finalizzato.
 Veduta laterale di una fila di Coltivatori al lavoro tra le righe
 del cerchio medio, vista da dietro/laterale. Cantilena implicita
 (in s08 si interrompe → "TUM-tum" delle zappe). Possibile riserva
 per scrittura prosa.]
```

---

## 🔗 Riferimento canonico

- `visual/luoghi/quartiere_terra/orti_del_cerchio/scheda.md`
- Bible §8.4 Quartiere di Terra + §4.X COLTIVATORI DEL CERCHIO
- Cartografia `island.geojson#features.id=orti_del_cerchio`
- Coerenza con `visual/personaggi/collettivi/coltivatori_del_cerchio/scheda.md` (qui hanno la cantilena codificata)

## Note workflow

Apparizioni saga:
- s03: zona di gioco fratelli al margine (cornice S03-C1: Salvia separa erbe in lontananza)
- s04: setting principale (Salvia raccoglie + radici)
- s05: passaggio verso Foresta (cornice + Bru porta i fratelli)
- s08: cantilena interrotta pre-crack (cornice S08-C1, suono di sfondo)
- s09: modulazione cantilena pomeriggio compleanno (cornice S09-C2)
- s11: Coltivatori scendono coi sacchi per la festa

La veduta canonica è "luogo vuoto" — le scene con personaggi/cantilena/azione si compongono sopra.
