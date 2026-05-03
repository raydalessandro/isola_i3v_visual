# Forno di Fiamma — Prompt Grok per vedute reference

> **Scopo.** Generare una serie di **3-4 vedute canoniche** del Forno (esterne + interne) con Grok Imagine, da usare come reference visiva per le scene successive con personaggi (s01-s12 dove il Forno appare).
>
> **Workflow:** Ray itera prompt + immagine finché la veduta non è canonica → carica in `immagini/` con naming `forno_canonica_v1_<vista>.jpg`. Le immagini canoniche restano intoccabili come reference; le scene con personaggi vengono generate poi assemblando questi reference con i prompt grok dei personaggi.
>
> **Pattern saga:** questo workflow vale per i **luoghi ricorrenti** (Forno, Albero Vecchio, Pontile, Pozzo, Casa fratelli, etc. — quelli che appaiono in più storie). I luoghi una-tantum non avranno reference dedicate: si generano direttamente al momento dell'hook.
>
> **Riferimento canonico:** `visual/luoghi/quartiere_fuoco/forno/scheda.md` (BLOCCO LOCATION) + Bible §8.2 Quartiere di Fuoco + §4.4 FIAMMA.

---

## Indice vedute

| # | Veduta | Versione | Status |
|---|---|---|---|
| 1 | Esterno (alba) | v2 | ⏳ in iterazione |
| 2 | Interno (kneading area) | — | da fare |
| 3 | Cortile retro | — | da fare |
| 4 | (4ª veduta da decidere insieme) | — | da fare |

---

## 🎨 Veduta 1 — Esterno del Forno all'alba (v2)

**Versione:** 2.0 (correzione: forno più grande in inquadratura + contesto Quartiere di Fuoco visibile)
**Tipo:** scena di apertura, esterno
**Formato:** verticale 3:4 (es. 1024×1365)
**Layout testo:** **testo overlay nella metà superiore** dell'immagine (gestito a posteriori via script)

**Modalità Grok:** text-to-image

**Filename atteso al salvataggio (quando canonica):** `forno_canonica_v1_esterno_alba.jpg`

### 🔄 Cosa cambia rispetto a v1

| Problema in v1 | Fix in v2 |
|---|---|
| Forno troppo piccolo nell'inquadratura | Quantità esplicita: occupa 50-60% dei due terzi inferiori |
| Casa "nel nulla" senza contesto | Quartiere di Fuoco come scenario abitato attorno |
| Mancavano le Case del Mattino | Inserite ESPLICITAMENTE come cluster di 3-4 case dietro il Forno (verso est) |
| Mancava il cortile retro canonico | Visibile dal lato sinistro del Forno con legna catastata |
| Mancava ambiente agricolo | Erba spontanea, cespugli, piccolo orto adiacente, un albero |
| Tutto troppo "isolato pittoresco" | Composizione di villaggio rurale, modesto ma abitato |

### ⭐ PROMPT (copia-incolla in Grok)

```
A painterly illustrated landscape scene in the style of Beatrix Potter
and Brian Wildsmith — watercolor and thin sepia ink lines, warm earthy
palette, hand-drawn children's picture book aesthetic. Vertical 3:4
composition. NO PEOPLE in the image. NO text, NO writing, NO signs.

Scene: A small rural artisan bakery at dawn — the first light of day on
a Mediterranean-style island village. The bakery is the first building
along the village's east-facing main path (Via dell'Alba). The bakery
is silent but awake — smoke rises gently from the chimney, the rest of
the small village still sleeps. View from outside, three-quarter angle
from the north-west.

═══════════════════════════════════════════
CRITICAL COMPOSITIONAL CONSTRAINT (for text overlay):
═══════════════════════════════════════════

The IMAGE IS DIVIDED VERTICALLY:
- The UPPER THIRD of the image (top 33%) must be MOSTLY EMPTY DAWN SKY
  with WARM UNIFORM TONES (rose-orange-gold gradient), with LOW CONTRAST
  and FEW DETAILS. This space will be used for text overlay later. The
  chimney top of the bakery may peek into the lower edge of this upper
  third, with a thin trail of smoke rising. NOTHING ELSE in the upper
  third — no trees, no mountains, no birds, no clouds with strong
  contrast.
- The LOWER TWO-THIRDS (bottom 67%) contain the bakery, the village
  context around it, the path, and the rural surroundings.

═══════════════════════════════════════════
THE BAKERY (DOMINANT element — must occupy ~50-60% of the lower 2/3):
═══════════════════════════════════════════

The bakery is the MAIN SUBJECT and must be PROMINENTLY VISIBLE — close
enough to read its details clearly. It should occupy approximately 50%
to 60% of the lower two-thirds height of the image, positioned slightly
to the right of center.

THE BUILDING:
A SMALL LOW STONE COTTAGE-BAKERY, single-story, rectangular, about 7×8
meters in real-world scale. Seen from a 3/4 angle: we see the WEST
FACADE (facing us, where the front door is) AND the NORTH SIDE (left of
the building, slightly receding into perspective). The east side
(behind, partially visible) catches the first dawn light.

- WALLS: rough hand-applied OCHRE PLASTER, slightly uneven, warm and
  worn (NOT bare red brick, NOT smooth stucco)
- ROOF: pitched roof with DARK TERRACOTTA TILES (irregular old tiles,
  slightly mossy in places)
- A STONE CHIMNEY rising from the roof on the back-right corner —
  thin smoke rising gently, drifting north-west in the still dawn air
- THE FRONT DOOR (on the west facade, facing us): simple weathered
  wooden plank door with iron hinges. Currently CLOSED.
- A SMALL SQUARE WINDOW beside the door (west side): wooden shutters
  CLOSED.
- ON THE EAST SIDE (visible in 3/4 perspective, on the right side of
  the building): another small window — partially visible in
  perspective, showing a SOFT WARM AMBER GLOW from inside (the kneading
  area is lit, the day's work has begun).
- A LOW WOODEN BENCH against the north wall (worn smooth by years of
  use)

═══════════════════════════════════════════
THE REAR COURTYARD (visible from the north angle):
═══════════════════════════════════════════

Because we view from the north-west angle, we can see PART OF THE BACK
COURTYARD on the left side of the bakery — a small open courtyard with:
- A STACK OF SPLIT FIREWOOD organized against the bakery's east wall,
  about a meter high
- A small WOODEN AXE leaning against a chopping block
- Packed earth ground

This grounds the bakery as a WORKING dwelling, not isolated. Just a
glimpse, not the focus.

═══════════════════════════════════════════
THE QUARTIERE DI FUOCO CONTEXT (CRITICAL — bakery is NOT alone):
═══════════════════════════════════════════

The bakery is the FIRST building of a small cluster — the Quartiere
di Fuoco (Fire Quarter). The other buildings of the quarter stretch
out to the EAST behind/past the bakery, along the same earth path.

BEHIND THE BAKERY (visible to the right and slightly behind in
perspective):
- 3 to 4 SMALL OTHER STONE COTTAGES in similar pre-industrial style —
  these are the CASE DEL MATTINO (Houses of the Morning). They are
  SIMPLER and SMALLER than the bakery, with similar ochre plaster
  walls and dark terracotta roofs. They are positioned along the
  continuing earth path, receding into the distance toward the rising
  sun.
- The other houses are STILL SLEEPING — closed doors, closed shutters,
  no smoke from their chimneys (only the bakery's chimney smokes).
- One of the distant houses might have a small visible adjacent feature
  hinting at its trade: e.g., a small dark anvil shape outside one
  (the blacksmith), or some low racks (the tanner). VERY subtle, just
  hints.
- The houses get smaller and more atmospheric as they recede into the
  distance.

═══════════════════════════════════════════
THE VIA DELL'ALBA (the path):
═══════════════════════════════════════════

The earth path (Via dell'Alba) runs in front of the bakery, slightly
diagonal, leading the eye into the scene from the lower-left foreground
and continuing past the bakery and beyond to the east where it
disappears in the distance toward the dawn light.

- Packed earth surface, slightly uneven, with patches of grass at the
  edges
- A few WILDFLOWERS (tiny dots of pale yellow/white) at the path edges
- Slight wear in the middle of the path (where feet pass)

═══════════════════════════════════════════
THE RURAL SURROUNDINGS:
═══════════════════════════════════════════

- TO THE LEFT/FOREGROUND of the bakery: low GENTLE PASTURELAND with
  sage-green grass and a few patches of wildflowers
- A SINGLE MODEST TREE near the bakery (perhaps an olive tree or an
  almond tree, characteristic of Mediterranean countryside) on the
  left foreground area, providing a natural anchor and depth
- A SMALL VEGETABLE PATCH adjacent to the bakery (north or west side)
  — just a humble plot with rows, low and simple, bordered with a few
  stones
- IN THE FAR DISTANCE (left, beyond the bakery): hint of the rest of
  the island's gentle countryside, very low rolling pastures

═══════════════════════════════════════════
LIGHT (CRITICAL):
═══════════════════════════════════════════

DAWN — the first hour. The sun has just begun rising in the EAST
(behind/right of the bakery, behind the cluster of Case del Mattino).
The light:
- Catches the EAST SIDE of the bakery and the eastern walls of the
  distant houses, making them glow warm
- The WEST FACADE of the bakery (facing us) is in soft cool shadow
  but warmed by reflected dawn glow
- The path is partially in warm light where the dawn reaches between
  buildings
- The chimney smoke rises softly through warm-tinted air

The SKY (upper third) is the warmest part: a calm gradient of rose,
peach, and gold, with maybe one or two thin wispy clouds.

The mood is QUIET, ALIVE, EXPECTANT. The bakery has woken up first.
The rest of the village still sleeps. Something is about to begin.

═══════════════════════════════════════════
WHAT MUST NOT APPEAR (CRITICAL):
═══════════════════════════════════════════

- NO PEOPLE, NO characters, NO foxes, NO animals, NO figures of any
  kind, NOT EVEN silhouettes
- NO TEXT, NO WRITING, NO SIGNS, NO LETTERS, NO INSCRIPTIONS — there
  is no writing on this island, ever
- NO "PANIFICIO" sign, NO "BAKERY" sign, NO names on the building
- NO SEA visible (the bakery is INLAND east, not on coast)
- NO MOUNTAINS visible (mountains are far north, not from this
  perspective)
- NO WINDMILLS
- NO MODERN ELEMENTS: no aluminum frames, no glass doors, no electric
  cables, no street lights, no concrete, no plastic, no electric power
- NO RED BRICK FACADE (walls are ochre plaster)
- NO COMMERCIAL DISPLAY: no shop window, no goods displayed outside,
  no produce in front
- NO HOBBIT/elf-style architecture (no curved doorways, no round
  windows)
- NO Disney/Pixar 3D rendering
- NO over-stylized Studio Ghibli
- NO heavy black ink outlines (use thin warm sepia)
- NO sparkles, no glow effects, no magical light particles
- NO postcard sunset/sunrise drama (this is a calm humble dawn, not
  an epic sunrise)
- NO LARGE TOWN OR CITY visible in the background — only the small
  cluster of Case del Mattino (3-4 houses), nothing more
- NO walled village, NO town gate, NO fortifications
- NO bell towers, NO church spires
- NO dense vegetation in the upper third (kept clear for text)
- NO flying birds
- NO ISOLATED LONELY BAKERY IN AN EMPTY FIELD (the bakery is part of
  a small village quarter — there must be the cluster of Case del
  Mattino visible behind/past it)

═══════════════════════════════════════════
STYLE NOTES (CRITICAL):
═══════════════════════════════════════════

- TECHNIQUE: traditional watercolor and thin sepia ink illustration,
  hand-drawn quality with slight imperfections
- INK: warm brown-sepia lines, light touch, never harsh black, organic
- WATERCOLOR: soft luminous warm washes, visible texture, slight
  color bleeds at edges, watercolor pooling on paper
- PALETTE: warm ochre walls, dark terracotta roof tiles, light
  weathered wood (door, shutters), pale gray-blue chimney smoke,
  rose-peach-gold dawn sky in the upper third, sage green pastures,
  warm earth-brown path. Cool soft shadows on the west facade.
  Amber glow from the east window only.
- AESTHETIC: tradition of Beatrix Potter, Brian Wildsmith, classic
  European children's illustration. Think the village views in
  "The Tale of Mrs. Tiggy-Winkle" or "Tom Kitten" — humble, alive,
  dignified, with a sense of community settlement.
- MOOD: quiet, awake, expectant. The first hour of the day. The
  village is still asleep. The bakery has woken up first.
```

### 📋 Variazioni se Grok sbaglia ancora

#### Se il forno è ancora troppo piccolo:
> CRITICAL CORRECTION: The bakery must DOMINATE the image. It should be
> CLEARLY READABLE in detail — close enough that you can see the
> texture of the ochre plaster, the wooden grain of the door, the
> individual roof tiles. The bakery occupies AT LEAST half the height
> of the lower 2/3 of the image. NOT a tiny distant building.

#### Se la scena è ancora "casa nel nulla":
> CRITICAL CORRECTION: The bakery is NOT isolated. Behind it, to the
> east, there must be 3-4 OTHER SMALL HOUSES (Case del Mattino) along
> the same earth path, receding into the distance. The bakery is part
> of a small village quarter. Show this small cluster of similar
> stone cottages behind the bakery — sleeping, closed, smaller and
> more atmospheric as they recede.

#### Se mette personaggi:
> CRITICAL: NO PEOPLE in this image. NO Fiamma, NO baker, NO foxes,
> NO children, NO figures, NOT EVEN silhouettes. The bakery is silent
> on the outside. Only the buildings, the path, the surroundings.

#### Se mette scritte:
> CRITICAL: NO TEXT, NO WRITING, NO SIGNS, NO LETTERS anywhere. The
> bakery has no name plate, no shop sign. The other houses have no
> signs either. This is a world without writing.

#### Se la parte alta è troppo dettagliata:
> CRITICAL: The upper third of the image must be MOSTLY EMPTY DAWN
> SKY with very few details — just a soft gradient of rose-peach-gold.
> NO trees in upper third, NO mountains, NO birds, NO clouds with
> strong contrast. Just calm uniform warm sky. The bakery's chimney
> top can peek into the lower edge of upper third with thin smoke.
> Nothing else.

#### Se rende un villaggio troppo grande:
> CORRECTION: The cluster behind the bakery must be SMALL — only 3 to
> 4 modest houses (Case del Mattino), NOT a town. They are similar to
> the bakery but slightly smaller. NO town walls, NO fortifications,
> NO bell towers, NO churches. Just a humble line of small rural
> stone cottages along the path.

#### Se trasforma il forno in un casolare/villa rustica:
> CORRECTION: The bakery is a SIMPLE PRE-INDUSTRIAL STONE COTTAGE —
> rectangular, modest, single-story. NOT a Tuscan villa, NOT a stately
> farm house with multiple stories, NOT decorative. Just a humble
> ochre-plastered cottage with a terracotta roof. 7×8 meters in real
> scale.

### 🎯 Checklist di approvazione

**Composizione per overlay testo:**
- [ ] Terzo superiore mostly empty con cielo warm gradient
- [ ] Cima camino + filo di fumo ammessi nella zona di transizione
- [ ] Spazio leggibile per testo overlay

**Forno (DOMINANTE):**
- [ ] Forno occupa 50-60% dell'altezza dei due terzi inferiori
- [ ] Dettagli leggibili (texture intonaco, grana legno, tegole)
- [ ] Vista 3/4 dall'angolo nord-ovest
- [ ] Pareti ocra grezzo, tetto terracotta scuro
- [ ] Camino fumante
- [ ] Porta principale chiusa
- [ ] Finestra ovest con imposte chiuse
- [ ] Finestra est intravista con bagliore caldo interno

**Cortile retro (sinistra del forno):**
- [ ] Catasta di legna visibile
- [ ] Eventuale ascia/ceppo
- [ ] Senza recinzione

**Case del Mattino (dietro il forno):**
- [ ] 3-4 piccole case dietro/oltre il forno
- [ ] Stesso stile (ocra plaster + terracotta)
- [ ] Più piccole e atmosferiche con la distanza
- [ ] Tutte chiuse (camini non fumanti)
- [ ] NON formano una città/villaggio grande

**Ambiente:**
- [ ] Sentiero (Via dell'Alba) in primo piano
- [ ] Erba sage-green ai bordi
- [ ] Piccolo orto adiacente al forno
- [ ] Un albero solitario nei pressi (olivo/mandorlo)
- [ ] Eventuale panchina contro la parete nord

**Luce:**
- [ ] Alba calda, sole appena sorto a est (dietro forno + Case del Mattino)
- [ ] Cielo rosa-pesca-oro nell'upper third
- [ ] Facciata ovest in ombra soffusa cool, warmata da riflesso
- [ ] Bagliore caldo dalla finestra est
- [ ] Fumo grigio-azzurrino dal camino

**Anti-cliché:**
- [ ] NESSUN personaggio
- [ ] NESSUNA scritta
- [ ] NO mare, NO mulini, NO montagne
- [ ] NO infissi moderni
- [ ] NO Hobbit-style
- [ ] NO postcard drama
- [ ] NO villaggio fortificato/grande
- [ ] NO casolare rustico tipo villa toscana

**Stile:**
- [ ] Painterly watercolor + sepia ink (Beatrix Potter)
- [ ] Palette warm earthy
- [ ] Vista verticale 3:4

Se 22+ check ok → composizione canonica.
Se 16-21 check ok → iteriamo con prompt correttivo specifico.
Se <16 check ok → riscriviamo prompt principale.

### 🔧 Note tecniche per l'overlay testo

- Area testo: rettangolo nei top 33%
- Margini: ~5% da ogni lato
- Font suggerito: serif classico (Garamond, Caslon, Bembo)
- Colore testo: nero o seppia molto scuro (#2a1810)
- Allineamento: sinistra o giustificato
- Interlinea: 1.4-1.5x

### 🔗 Riferimento canonico

Derivata da:
- `visual/luoghi/quartiere_fuoco/forno/scheda.md` — blocco LOCATION ESTERNO + cortile retro
- Bible §4.4 FIAMMA + §8.2 Quartiere di Fuoco ("Case del Mattino — fabbro, conceria, essiccatoio")
- ARCHI_12_STORIE S1 (cornice apertura saga)
- Pipeline visual layer A

---

## Vedute successive

Spazi riservati per le prossime vedute, da popolare iterativamente:

### 🎨 Veduta 2 — Interno del Forno (kneading area)
*da fare — quando Ray porta il prompt, si aggiunge qui come sezione completa con prompt + checklist + variazioni*

### 🎨 Veduta 3 — Cortile retro
*da fare*

### 🎨 Veduta 4 — (da decidere)
*da fare*

---

## Note di workflow

- **Iterazione:** quando una veduta è canonica (≥22 check ok), Ray salva l'immagine in `immagini/forno_canonica_v1_<vista>.jpg`. Le canoniche v1 restano intoccabili come reference.
- **Scene con personaggi:** una volta che le 3-4 vedute reference esistono, le scene degli hook che includono il Forno (s01-s12 dove appare) si generano combinando la veduta reference + i prompt grok dei personaggi in scena. Il Forno mantiene così coerenza visiva cross-storia.
- **Modifiche al canone:** se durante l'iterazione emerge un dettaglio nuovo non presente in `scheda.md`, va aggiornata la scheda PRIMA di canonizzare la veduta (la scheda resta fonte autorevole).
