# Pozza dell'Abbeveratoio dei Pastori — Atlante vedute canoniche (prompt grok)

> **Scopo.** Reference visiva canonica per le scene saga alla pozza (sub-location dei Pascoli Alti, Quartiere d'Aria nord). Location centrale di s02 (6 hook su 10): la superficie della pozza ha QUATTRO stati canonici che vanno coperti.
>
> **Riferimento:** `scheda.md` + `story_graph.json#stories.s02.location_primary` + prosa definitiva s02.
>
> **Bozza Claude 2026-06-11 — da validare Ray.**

---

## Indice vedute

| # | Veduta | Stato superficie | Uso s02 | Status |
|---|---|---|---|---|
| 1 | Specchio fermo (inverno, ghiaccio sgelato) | acqua ferma, lucida | h04, h05 | ⏳ da generare |
| 2 | Increspata dal Taglio | pieghe piccole, riflessi spezzati | h07b | ⏳ da generare |
| 3 | Calma ricomposta (primo pomeriggio) | riflessi tornati, fedeli | h08 | ⏳ da generare |
| 4 | Sera piatta e dura | superficie spenta, metallica | h10b | ⏳ da generare |

---

## 🎨 Veduta 1 — Specchio fermo — v1

**Filename atteso:** `pozza_abbeveratoio_pastori_canonica_v1_specchio.jpg`
**Formato:** verticale 2:3 (per spread h05 generare anche variante orizzontale 16:9)
**Modalità Grok:** text-to-image

### ⭐ PROMPT

```
A painterly illustrated landscape scene in the style of Beatrix Potter
and Brian Wildsmith — watercolor + thin sepia ink, warm earthy palette,
hand-drawn children's picture book aesthetic. NO PEOPLE. NO text.

Scene: A SMALL MOUNTAIN POOL (pozza) inside a SHELTERED HOLLOW
halfway up the high meadows path, on a Mediterranean island. The
summer drinking pool of the shepherds' goats, now in winter.

LANDSCAPE:
- A SHALLOW ROUND-ISH POOL, a few meters wide, set in a natural
  hollow (conca riparata) protected from the wind by low grassy
  banks and a few stones
- THE ICE MELTED AWAY DURING THE NIGHT: the water is PERFECTLY
  STILL and GLOSSY, a flat mirror reflecting the pale winter sky
- Around the rim: WINTER-DEAD LEAVES (dark, wet, matted), hard
  short grass, frost traces in the shaded edges
- A few flat stones at the rim where animals drink in summer;
  faint animal tracks in the cold mud
- Beyond the hollow's edge: the open slope of the high meadows
  (Pascoli Alti), hinted, out of focus

LIGHTING: late morning winter light, cold and clear, low sun.
The pool surface catches the sky: pale grey-blue, luminous.

ATMOSPHERE: stillness, suspension, quiet expectancy. The pool is
a mirror waiting to be looked into.

PALETTE (Quartiere d'Aria): stone grey, ice blue, pale winter sky,
sage-dry grass, dark wet leaf browns. Saturation restrained.

NEGATIVE: NO 3D render, NO photorealism, NO anime, NO disney, NO
neon, NO people, NO reflections of figures in the water.
```

---

## 🎨 Veduta 2 — Increspata dal Taglio — v1

**Filename atteso:** `pozza_abbeveratoio_pastori_canonica_v1_increspata.jpg`
**Formato:** verticale 2:3
**Modalità Grok:** text-to-image (o img2img dalla Veduta 1)

### ⭐ PROMPT

```
[Stessa scena e stile della Veduta 1 — same hollow, same rim, same
winter light shifted to early afternoon.]

CHANGE — THE SURFACE:
- A LOW GUST OF WIND (the Vento Taglio) has just passed: the whole
  surface is covered in SMALL TIGHT RIPPLES ("pieghe piccole"),
  like folded cloth
- NO mirror: the reflections are BROKEN into fragments — slivers
  of sky and cloud pieces scattered across the ripples
- One or two faint silvery rings still widening near the center
  (where something small just fell in)
- Grass on the hollow's rim bending in one direction, marking the
  wind's low passage

ATMOSPHERE: interruption, breath of wind, the mirror refusing to
return. Movement without drama.
```

---

## 🎨 Veduta 3 — Calma ricomposta — v1

**Filename atteso:** `pozza_abbeveratoio_pastori_canonica_v1_ricomposta.jpg`
**Formato:** verticale 2:3
**Modalità Grok:** img2img dalla Veduta 1

### ⭐ PROMPT

```
[Same as Veduta 1, with these changes:]

- Light: EARLY AFTERNOON winter sun, slightly warmer than morning
- The surface has JUST SETTLED back to stillness: mirror restored,
  but a faint memory of motion at the far edge (one last fading
  ripple line)
- A SMALL STICK (rough little wooden twig) floating tilted at the
  surface near the center, half-sunk, about to go under

ATMOSPHERE: quiet after agitation. Things returning to their place,
one small thing leaving.
```

---

## 🎨 Veduta 4 — Sera piatta e dura — v1

**Filename atteso:** `pozza_abbeveratoio_pastori_canonica_v1_sera.jpg`
**Formato:** verticale 2:3
**Modalità Grok:** text-to-image

### ⭐ PROMPT

```
[Same hollow as Veduta 1, at the end of the day.]

CHANGE — LIGHT AND SURFACE:
- LOW SUN, almost gone: long cold shadows fill the hollow, the
  light grazes only the upper rim of the banks
- The surface is FLAT and HARD-looking, like dull spent metal —
  no ripples, no luminous mirror, just a cold opaque sheen
  beginning to skin over for the night
- Colors shifted to evening: deep grey-blues, a last band of pale
  gold on the far slope

ATMOSPHERE: closed, sealed, finished for the day. A pool nobody
looks into anymore. Beneath that surface, unseen, something small
rests on the bottom.
```
