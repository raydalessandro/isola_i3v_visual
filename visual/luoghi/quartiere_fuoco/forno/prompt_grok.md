# Forno di Fiamma — Atlante vedute canoniche

> **STATO: ✅ SET CANONICO CHIUSO (2026-05-03).** 5 vedute reference + 1 bonus + 1 planimetria selezionate da Ray e salvate in `immagini/`. **NON rigenerare.**
>
> **Workflow scene future:** prendere la veduta canonica come BASE → comporre la scena aggiungendo i personaggi tramite character canon dei rispettivi prompt grok. Stile da replicare: painterly watercolor + ink linework, palette warm earth, tradizione picture book inglese-mediterraneo (Beatrix Potter / Brian Wildsmith).
>
> **Pattern saga:** questo set di reference vale per i **luoghi ricorrenti** (Forno = 7 storie). I luoghi una-tantum NON avranno reference dedicate, si generano direttamente al momento dell'hook.
>
> **Riferimento canonico:** `visual/luoghi/quartiere_fuoco/forno/scheda.md` (planimetria a 2 sale + sotto-aree) + Bible §8.2 Quartiere di Fuoco + §4.4 FIAMMA.
>
> **Archivio iterazioni prompt:** in fondo al file restano le iterazioni v2 dei prompt per Esterno e Sala Laboratorio — utili come reference di stile e vincoli editoriali quando si generano nuove scene (es. quando serve combinare un'immagine canonica con i character canon dei personaggi).

---

## ✅ SET CANONICO ATTIVO (5 vedute + 1 bonus + planimetria)

| # | Veduta | File reference | Quando usarla |
|---|---|---|---|
| 1 | **Esterno alba** | `immagini/forno_canonica_v1_esterno_alba.jpg` | s01 apertura, s10 cammeo all'alba, qualsiasi scena di Fiamma sulla soglia o vista da fuori |
| 2 | **Sala Laboratorio panoramica** | `immagini/forno_canonica_v1_laboratorio_panoramica.jpg` | s06 cornetti, s08 apertura, s11 banco dolci, s12 mattino — establishing shot della sala col lavoro pane |
| 3 | **Sala Laboratorio dettaglio forno** | `immagini/forno_canonica_v1_laboratorio_dettaglio.jpg` | close-up scene di azione con uno dei due forni, impasti, pala, alcove legna (Fiamma all'opera) |
| 4 | **Sala Dispensa-Pranzo** | `immagini/forno_canonica_v1_dispensa_pranzo.jpg` | s09 compleanno Gabriel, s12 sera (chiusura saga, dolce 4 fette + candela), s8 ritorno fratelli |
| 5 | **Cortile retro** | `immagini/forno_canonica_v1_cortile_retro.jpg` | cammei rari (Fiamma che prende legna, sfondo per scene di transizione) |
| 2-bis | **Sala Laboratorio verticale** (bonus) | `immagini/forno_canonica_v1_laboratorio_verticale.jpg` | scene 3:4 con overlay testo (la finestra centrale dà sull'esterno = vista canonica est) |
| 0 | **Planimetria canonica** (documentazione) | `immagini/forno_planimetria_canonica.jpg` | reference di disposizione delle 2 sale comunicanti — non per generare |

### Mappa scene saga → veduta canonica

Vedi `scheda.md` sezione "✏️ Note d'uso operative" per la mappa completa storia→veduta. Sintesi:

| Storia | Sala/area | Veduta principale |
|---|---|---|
| s01 (apertura saga) | Esterno (Fiamma soglia, fratelli partono) | 1 (Esterno alba) |
| s06 (cornetti, detto popolare) | Sala Laboratorio (Fiamma impastando) | 2 (Lab panoramica) o 3 (Lab dettaglio) |
| s08 (apertura cornetto + chiusura imposte) | Sala Laboratorio + Sala Dispensa | 2, poi 4 al ritorno |
| s09 (location primary, compleanno Gabriel) | Sala Dispensa-Pranzo | 4 |
| s10 (cammeo all'alba) | Esterno | 1 |
| s11 (cammeo banco dolci festa) | Sala Laboratorio (banco esposto) o Esterno | 2 |
| s12 mattino (pagnotta a Grunto) | Sala Laboratorio | 2 o 3 |
| s12 sera (chiusura saga, 4 fette + candela) | Sala Dispensa-Pranzo | 4 |

### Vincoli di stile per scene future composte sopra le canoniche

Quando si genera una scena con personaggi sopra una di queste reference:

1. **Stile**: replicare painterly watercolor + thin sepia ink linework, palette warm earth (ocra, terracotta, ember, beige). Mai cartoon, mai 3D, mai photoreal-iper.
2. **Coerenza con la veduta**: rispettare disposizione, scale, palette della reference. Se la dispensa ha mensole stipate a sinistra, non spostarle a destra.
3. **Personaggi**: usare i character canon dai prompt grok in `visual/personaggi/individuali/.../prompt_grok.md`. Mai improvvisare aspetto.
4. **Niente scritte** (canone saga): no insegne, no etichette, no testi.
5. **Multi-personaggio funziona**: lo spazio canonico delle sale è ampio, 4-5 personaggi entrano comodi.

---

## 📜 Archivio iterazioni prompt (reference per generazioni future)

> Le sezioni successive sono **archivio storico** dei prompt iterativi che hanno portato al set canonico. Restano utili come reference di stile e vincoli editoriali per generare scene complesse (es. multi-personaggio + cornice cross-storia) o eventualmente nuove vedute extra in futuro.
>
> **NON rigenerare le canoniche** dal prompt — il set è chiuso.

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

## 🎨 Veduta 2 — Interno del Forno (alba, kneading area attiva) — v2

**Versione:** 2.0 (correzione: scala forno comune di borgo, spazio ampio per multi-personaggio, vista canonica dalla finestra est)
**Tipo:** scena interna, momento canonico della saga ("primo posto dell'isola dove c'è luce calda al mattino")
**Formato:** verticale 3:4 (es. 1024×1365)
**Layout testo:** **testo overlay nella metà superiore** dell'immagine (gestito a posteriori via script). L'upper third sarà il soffitto alto con travi a vista — tonalità uniforme legno scuro, basso contrasto, leggibile per overlay.

**Modalità Grok:** text-to-image

**Filename atteso al salvataggio (quando canonica):** `forno_canonica_v1_interno_alba.jpg`

### 🔄 Cosa cambia rispetto a v1

| Problema in v1 | Fix in v2 |
|---|---|
| Stanza piccola (~6×5m) → "casa privata", non forno comune | Stanza ampia (~9×7m) — forno comune di borgo |
| Soffitto basso (2.5m) → claustrofobico per multi-personaggio | Soffitto alto (~3.2m) → arioso, per Fiamma + 3 fratelli con margine |
| Forno con bocca piccola (~80cm) da forno domestico | Forno con bocca grande (~1.5-1.8m) da forno comunitario, cupola architettonica imponente |
| Finestra est mostra solo "hint di esterno" | Vista canonica dalla finestra est: cortile retro in primo piano + erba + silhouette Case del Mattino in controluce + alba rosa-oro |
| Mensole nord con pochi elementi | Molte ceste di proofing (è forno comunitario, cuoce per tutti gli abitanti) |
| Stanza affollata di mobili | Zona centrale aperta libera (circolazione per personaggi) |

### 🎯 Obiettivo della veduta

Reference canonica dell'**interno del Forno all'alba**: forno comune di borgo acceso (bagliore brace), finestra est che porta la prima luce ambra sul banco da impasto e mostra l'alba con le silhouette delle Case del Mattino, atmosfera ACCOGLIENTE-LAVORATIVA-VIVA-AMPIA. NESSUN personaggio in scena (la stanza è "appena lasciata o appena aperta"). Da usare come reference per le scene interne con personaggi (s01 cornice, s06 cornetti, s08 apertura, s09 compleanno, s12 chiusura) — lo spazio deve poter ospitare comodamente Fiamma + i 3 fratelli + eventualmente altri.

### ⭐ PROMPT (copia-incolla in Grok)

```
A painterly illustrated interior scene in the style of Beatrix Potter
and Brian Wildsmith — watercolor and thin sepia ink lines, warm earthy
palette, hand-drawn children's picture book aesthetic. Vertical 3:4
composition. NO PEOPLE in the image. NO text, NO writing, NO signs.

Scene: The interior of a COMMUNITY-SCALE rural stone bakery at dawn,
on a Mediterranean-style island. NOT a small private home kitchen —
this is the COMMUNAL OVEN of a small village, where bread for the
WHOLE ISLAND is baked daily. Single large room, AIRY and SPACIOUS,
with a high beamed ceiling. The first warm light of the day is just
entering through the east window, falling on the long kneading table
and showing the dawn breaking outside. The large stone oven is lit,
embers glow softly from its wide mouth. The room is empty of people
but visibly inhabited — the day's work has just begun or paused for
a moment. Quiet, warm, lived-in, GENEROUSLY SIZED.

═══════════════════════════════════════════
CRITICAL COMPOSITIONAL CONSTRAINT (for text overlay):
═══════════════════════════════════════════

The IMAGE IS DIVIDED VERTICALLY:
- The UPPER THIRD of the image (top 33%) shows the HIGH BEAMED CEILING
  with exposed dark wooden beams — uniform dark warm tone, low contrast,
  few details. The beams run across in slight perspective but stay
  visually calm. NO chandeliers, NO hanging baskets crowding the upper
  third, NO bright highlights up there. This space is reserved for
  text overlay.
- The LOWER TWO-THIRDS (bottom 67%) contain the room's working
  elements: oven, kneading table, dining table, shelves, floor.

═══════════════════════════════════════════
SCALE AND SPACE (CRITICAL — defining feature of v2):
═══════════════════════════════════════════

This is a COMMUNITY OVEN, not a home kitchen. Scale references:
- Room dimensions: approximately 9 × 7 METERS (large open space)
- Ceiling height: approximately 3.2 METERS (high enough for air to
  circulate around the oven heat)
- The room must FEEL SPACIOUS — visible OPEN FLOOR AREA in the center,
  free of furniture, allowing room for the baker and 3-4 visiting
  characters to move comfortably with margin around them
- This is the COMMUNAL OVEN of the island — Fiamma bakes bread for
  every household. The room reads as "village bakery", intermediate
  scale between private home and craft workshop
- Reference: medieval-Mediterranean village communal oven, generous
  but humble

NEVER claustrophobic. NEVER home-kitchen-sized. NEVER with furniture
crammed together. The OPEN CENTRAL FLOOR is essential.

═══════════════════════════════════════════
VIEWPOINT (CRITICAL — fixed angle for canonical reference):
═══════════════════════════════════════════

Three-quarter angle from the NORTH-WEST corner of the room, looking
toward the SOUTH-EAST corner. With this angle, in a single view we see:
- the EAST WALL on the right (with the east window and the long
  kneading table beneath it, plus the back door near the oven)
- the SOUTH-EAST CORNER straight ahead-right (where the LARGE stone
  oven is — the dome is a substantial architectural presence)
- the NORTH WALL on the left (with generous wooden shelves)
- a partial glimpse of the WEST WALL / front door area at lower-left
  foreground (slightly cut off — the dining table edge may be visible
  in the lower-left foreground for depth)
- WIDE PACKED EARTH FLOOR extending across the lower part of the
  frame, with a clear OPEN CENTRAL AREA (no furniture in the middle)
- HIGH exposed dark wooden ceiling beams across the upper part

Camera height: child-perspective (about 1.2–1.4 meters from the floor)
— slightly low, intimate.

═══════════════════════════════════════════
THE ROOM (single large rectangular space, ~9×7 meters):
═══════════════════════════════════════════

WALLS: rough hand-applied OCHRE PLASTER, slightly uneven, warm and
worn (NOT smooth stucco, NOT painted patterns, NOT wallpaper).
Texture of hand-applied plaster visible. Walls subtly dusted with
flour in patches near the kneading table.

CEILING: HIGH (~3.2 m), with EXPOSED DARK WOODEN BEAMS running across.
Beams are plain, structural, slightly weathered wood, dark warm brown.
NO ornaments, NO carvings, NO hanging chandeliers. A few iron hooks
may hang from a beam holding strings of dried herbs or a single
copper pot — minimal.

FLOOR: WIDE area of PACKED EARTH, smooth from years of use, slightly
dusted with FLOUR especially near the kneading table. Color: warm
earth-brown, slightly variegated. NOT tile, NOT wood, NOT polished.
A CLEAR OPEN AREA in the middle of the room, free of furniture.

═══════════════════════════════════════════
THE STONE OVEN (south-east wall — DOMINANT focal element, COMMUNITY-SCALE):
═══════════════════════════════════════════

Built directly into the SOUTH-EAST WALL, the stone oven is the heart
of the room AND a substantial architectural feature. Construction:
- LARGE DOMED MOUTH OPENING about 1.5 to 1.8 METERS wide and ~1 meter
  tall, slightly arched at the top — this is a COMMUNITY OVEN, not a
  home oven. The mouth is generously sized, an adult character could
  almost stand inside it
- The DOME of the oven rises prominently from the wall, a
  substantial rounded shape made of fieldstone — visible as
  architectural mass, not a small recess
- Built of ROUGH FIELDSTONE (irregular pieces of natural stone, not
  regular masonry bricks), held together with earth mortar
- The stone around the mouth is SOOT-DARKENED from years of fires,
  black-grey gradient outward, with a clear darker ring around the
  opening
- Inside the oven: WARM ORANGE-BRICK GLOW from embers and a small
  active fire — the glow spills out from the mouth onto the floor
  and the nearby wall, casting warm reflected light into the room.
  Strong enough to read as a distinct light source on top of the
  window light
- A LONG WOODEN PEEL (bread paddle) about 2 meters long leans
  against the wall beside the oven — flat wooden blade, very long
  handle (community-scale tool), weathered wood
- A neat STACK OF SPLIT FIREWOOD on the floor next to the oven
  mouth, ready to feed the fire
- A pair of iron tools (poker, ash rake) hangs nearby

The oven occupies a significant portion of the right side of the
image, dominating the south-east corner with architectural weight.
NOT a tiny background detail — the dome is clearly the room's
defining architectural element.

═══════════════════════════════════════════
THE KNEADING TABLE (under the east window — second focal element):
═══════════════════════════════════════════

Positioned UNDER THE EAST WINDOW (the window that brings the first
dawn light). This is the heart of Fiamma's daily work and is
GENEROUS in size (community-scale, not home-scale).

- LONG WOODEN TABLE, weathered light wood with visible grain,
  rectangular, about 2.0 × 0.9 meters (long enough to prep many
  loaves at once), modest height
- Surface heavily DUSTED WITH FLOUR — pale ivory color, slightly
  uneven coverage
- ON THE TABLE:
  - a STONEWARE BOWL in terracotta color, about 30 cm diameter,
    containing a mound of pale dough being prepared
  - perhaps a SECOND smaller bowl with a different dough preparation
    (this is community baking — multiple loaves)
  - a WOODEN ROLLING PIN beside the bowl
  - a folded LINEN CLOTH (cream-white, slightly rumpled) to one side
  - a SMALL CLAY POT of flour, half-open
  - a few scattered crumbs/pieces of dough
  - perhaps a ball of risen dough resting on the floured surface
- The work is MID-PROCESS: someone has just been here, working on
  multiple things. Not staged, not perfectly arranged. Lived-in.

═══════════════════════════════════════════
THE EAST WINDOW AND ITS VIEW (CRITICAL — defines the canonical morning):
═══════════════════════════════════════════

The window is on the EAST WALL, directly above the kneading table.
- Medium-sized (~80×80 cm), wooden frame, dark weathered wood,
  simple construction
- Wooden shutters OPEN (folded inward against the wall)

THROUGH THE WINDOW, the canonical view is (this is what the island
looks like to the east of the bakery — DO NOT IMPROVISE other
landscapes):

1. FOREGROUND (closest, just outside the window): the REAR COURTYARD
   of the bakery (forno_cortile) — packed earth ground, neat stacks
   of split firewood against the back wall (visible at the bottom
   of the window view).
2. MIDDLE DISTANCE: low grass and gentle pastureland extending east.
3. FAR DISTANCE: SOFT SILHOUETTES of 3-4 SMALL STONE COTTAGES — the
   CASE DEL MATTINO (Houses of the Morning), with their pitched
   terracotta roofs barely visible, atmospheric and backlit by the
   rising sun. They are receding into the distance along the
   continuing path.
4. SKY (filling the upper portion of the window view): the DAWN —
   rose-peach-gold gradient, the sun just emerging behind the
   silhouetted houses (or about to). This is the canonical sunrise
   from the bakery's perspective.

The view through the window is SOFT, BACKLIT, ATMOSPHERIC — not a
detailed landscape painting. It contributes the CANONICAL DAWN to
the room: the reason this room is "the first warm point of the
island in the morning".

The window may also have a tiny clay water jug on its sill.

THE LIGHT FROM THIS WINDOW is the PRIMARY LIGHT SOURCE of the scene:
a SHAFT OF WARM AMBER LIGHT falls diagonally onto the kneading
table, illuminating the flour, the dough, the wood grain.

═══════════════════════════════════════════
THE DINING TABLE (west side, partial in foreground):
═══════════════════════════════════════════

Toward the WEST WALL, partially visible at the LOWER-LEFT FOREGROUND
of the frame (slightly cut off, providing depth):
- SIMPLE RECTANGULAR WOODEN TABLE, weathered light wood, about
  1.4×0.9 meters, modest, scratched from years of use
- 4 WOODEN CHAIRS or STOOLS visible around it (simple, plain)
- On the table: a small CLAY CANDLE HOLDER (unlit at this hour),
  a wooden cup, perhaps a small loaf of bread on a wooden board
- WITH OPEN SPACE around the table — chairs not crammed against
  walls, room to walk past

═══════════════════════════════════════════
THE NORTH WALL SHELVES (community-scale quantity):
═══════════════════════════════════════════

On the LEFT SIDE of the image (the NORTH WALL), generous wooden
shelves at varying heights, running for a substantial portion of the
wall (this is a community bakery — quantity matters):
- MANY WICKER PROOFING BASKETS containing rising dough (rounded
  shapes, draped with linen) — at least 8-12 visible, not just a
  handful
- Several STONEWARE JARS in terracotta color (flour, salt, honey,
  oil) of varying sizes, with simple wooden lids
- A stack of CLEAN LINEN CLOTHS, folded
- IRON HOOKS holding wooden ladles, wooden spoons, peels of varying
  sizes, a few iron pans
- Everything organized for daily use but not perfectly aligned —
  it's a working community bakery, abundance is part of its identity

═══════════════════════════════════════════
THE BACK DOOR (east wall, near the oven):
═══════════════════════════════════════════

On the EAST WALL, beside the oven (to its left in our view, between
the kneading table and the oven), a SIMPLE WOODEN BACK DOOR — closed,
weathered planks, iron hinges. It leads to the rear courtyard with
stacked firewood (visible in part through the east window view).
Unobtrusive, just a feature.

═══════════════════════════════════════════
NEAR THE FRONT DOOR AREA (lower-left edge, partial):
═══════════════════════════════════════════

At the very lower-left edge of the frame, we may glimpse:
- A WOODEN COAT HOOK on the wall holding a SPARE TERRACOTTA-RED
  APRON (Fiamma's signature, hung up — not worn)
- A LOW WOODEN BENCH against the wall
- A BROOM leaning against the wall corner

These are partial, atmospheric — they ground the room as a working
community space. The front door (west wall) may be partially visible
or fully off-frame.

═══════════════════════════════════════════
ATMOSPHERE (CRITICAL):
═══════════════════════════════════════════

The AIR is slightly HAZY with FINE FLOUR PARTICLES catching the warm
amber light from the east window — visible as a soft haze in the
shaft of light, never as bright sparkles. The air is faintly smoky
near the oven, but not heavy. The HIGH CEILING means the air feels
fresh, not stuffy.

The MOOD is QUIET, ALIVE, EXPECTANT, and SPACIOUS. Someone has just
been here (the dough is mid-knead, the linen cloth is rumpled, the
flour is freshly dusted) — but the scene is empty of figures right
now. This is the FIRST WARM POINT OF THE ISLAND IN THE MORNING.
Hospitable, working, honest, GENEROUSLY SIZED. Not solemn, not
monumental. A village's communal bakery that has woken up first.

═══════════════════════════════════════════
LIGHT (CRITICAL):
═══════════════════════════════════════════

TWO COEXISTING WARM LIGHT SOURCES:
1. PRIMARY: the warm amber DAWN LIGHT through the EAST WINDOW,
   falling diagonally onto the kneading table. This is the sharper,
   more directional light. Behind the window, the dawn sky and the
   silhouettes of the Case del Mattino are visible.
2. SECONDARY: the soft ORANGE-BRICK GLOW from the LARGE OVEN MOUTH,
   spilling onto the floor and lower wall near it. Strong enough to
   read as a distinct second light source, illuminating a generous
   portion of the floor around the oven.

The TWO LIGHTS DO NOT COMPETE — they coexist warmly. Where they
overlap (near the kneading table area, in the open central floor),
the warmth intensifies.

The CORNERS of the room (especially the upper corners and the
shadow side of the dining table) are in DEEPER WARM SHADOW — never
cool, never blue. Always warm earth-tones in the shadows.

NO cool light, NO blue tones, NO white "kitchen lighting". Warmth
everywhere, contrast between bright lit areas and warm shadows.

═══════════════════════════════════════════
WHAT MUST NOT APPEAR (CRITICAL):
═══════════════════════════════════════════

- NO PEOPLE, NO Fiamma, NO foxes, NO animals, NO figures of any
  kind, NOT EVEN silhouettes or hands entering the frame
- NO TEXT, NO WRITING, NO SIGNS, NO LETTERS, NO INSCRIPTIONS, NO
  recipes on chalkboards, NO labels on jars
- NO MODERN APPLIANCES: no electric oven, no metal stovetop, no
  refrigerator, no electric lights, no microwaves, no coffee makers
- NO MODERN COOKWARE: no shiny stainless steel, no aluminum, no
  silicone, no plastic
- NO ELECTRIC LIGHT FIXTURES: no chandeliers, no lamps with cords,
  no light bulbs, no switches
- NO CLEAN POLISHED SURFACES (everything is weathered, used, with
  patina)
- NO DECORATIVE ELEMENTS: no painted tiles, no flowery curtains, no
  tablecloths with patterns, no doilies, no ornaments, no framed
  pictures
- NO WALLPAPER, NO PAINTED PATTERNS on walls
- NO COMMERCIAL BAKERY ELEMENTS: no display case, no glass
  storefront, no menu boards, no cash register, no pricing
- NO MAGICAL ELEMENTS: no glowing dough, no sparkles, no light
  particles beyond the natural haze, no symbols carved on the oven
- NO HOBBIT/elf-style architecture: no curved doorways, no round
  windows, no ornamental woodwork
- NO Disney/Pixar 3D rendering, NO over-stylized Studio Ghibli
- NO heavy black ink outlines (use thin warm sepia)
- NO bright artificial tones, NO neon colors
- NO PASTRY-SHOP ELEGANCE: no croissants in fan arrangements, no
  cake stands, no decorative pastries, no piped icing
- NO French/German/Northern Italian regional stylization — this is
  a generic pre-industrial Mediterranean rural baker's home
- NO REGULAR MASONRY BRICKS for the oven (must be rough fieldstone)
- NO CHEERFUL "GOOD MORNING" POSTCARD VIBE — the mood is quiet and
  working, not theatrical
- NO HOME-KITCHEN SCALE: this is NOT a small private home kitchen.
  The room is GENEROUSLY SIZED, the oven is COMMUNITY-SCALE (mouth
  1.5-1.8 m wide), the ceiling is HIGH (~3.2 m). Reject any
  composition that reads as "cottage kitchen" or "domestic bakery"

═══════════════════════════════════════════
STYLE NOTES (CRITICAL):
═══════════════════════════════════════════

- TECHNIQUE: traditional watercolor and thin sepia ink illustration,
  hand-drawn quality with slight imperfections
- INK: warm brown-sepia lines, light touch, never harsh black,
  organic — the ink defines edges of beams, oven, table, shelves
  but lets the watercolor breathe
- WATERCOLOR: soft luminous warm washes, visible texture, slight
  color bleeds at edges, watercolor pooling on paper. The flour-dusted
  surfaces should read as soft pale color washes, not hard white
- PALETTE: warm ochre walls, dark warm brown ceiling beams, light
  weathered wood (kneading table, dining table), terracotta (oven
  stone, bowls, jars, hanging apron), ember orange (oven glow),
  pale ivory (flour dust, linen), amber-gold (warm light from east
  window), warm earth-brown floor, deep warm shadow in corners.
  Apron color (if visible): TERRACOTTA RED with a hand-stitched feel.
- AESTHETIC: tradition of Beatrix Potter, Brian Wildsmith, classic
  European children's illustration. Think the cozy interiors in
  "The Tale of Mrs. Tiggy-Winkle" (the laundry kitchen) — humble,
  alive, dignified, deeply warm, with a sense of work just paused.
- MOOD: quiet, awake, expectant, hospitable. The first hour of the
  day. The bread will be ready soon. The day has begun.
```

### 📋 Variazioni se Grok sbaglia

#### Se mette personaggi:
> CRITICAL: NO PEOPLE in this image. NO Fiamma, NO baker, NO foxes,
> NO children, NO figures, NOT EVEN silhouettes or hands entering
> the frame. The room is EMPTY of figures right now — someone has
> just been there but has stepped away momentarily. Show only the
> room, the oven, the work surfaces, the warm light.

#### Se mette scritte (su barattoli, lavagne, etc.):
> CRITICAL: NO TEXT, NO WRITING, NO SIGNS, NO LETTERS, NO LABELS
> anywhere. The jars have NO labels. There are NO chalkboards with
> recipes. NO writing on the walls or shelves. This is a world
> without writing.

#### Se l'upper third è troppo affollato:
> CRITICAL: The upper third of the image must show only the LOW
> CEILING with dark wooden beams in calm uniform tone. NO hanging
> baskets cluttering the top third, NO bunches of dried herbs in
> heavy quantity, NO chandeliers, NO bright highlights. Just the
> dark warm beams running across, low contrast, leggible space for
> text overlay later. The hanging hooks with herbs/pots can stay
> minimal or move to a lower beam.

#### Se la luce è troppo "magica" o sparkly:
> CRITICAL: The light is NATURALISTIC dawn light — warm amber from
> the east window, warm orange-brick glow from the oven mouth. NO
> sparkles, NO light particles beyond a soft natural haze of flour
> dust catching the light. NO glowing dough, NO magical effects.
> Just two warm coexisting light sources, with deep warm shadows
> in the corners.

#### Se rende un forno con masonry brick regolare:
> CORRECTION: The oven is built of ROUGH FIELDSTONE — irregular
> stones of different sizes, held together with earth mortar, not
> regular bricks. Soot-darkened around the mouth from years of
> fires. The shape is a rough dome, not a perfect arch. This is a
> pre-industrial rural bakery, not a medieval-stylized brick oven.

#### Se mette elementi commerciali / pasticceria elegante:
> CORRECTION: This is a HUMBLE FAMILY BAKERY interior, not a
> commercial pastry shop. NO display cases, NO glass storefronts,
> NO arranged pastry trays, NO piped icing, NO cake stands, NO
> decorative pastries. The bread on the kneading table is rough
> dough mid-knead. Everything is simple, working, humble.

#### Se la stanza è troppo piccola / sembra una casa privata:
> CRITICAL CORRECTION: This is the COMMUNITY OVEN of the village —
> Fiamma bakes bread for the WHOLE ISLAND here. The room is LARGE
> and SPACIOUS, ~9×7 meters with a HIGH BEAMED CEILING of 3.2 meters.
> The oven mouth is 1.5-1.8 m wide (community scale), the dome rises
> as a substantial architectural feature. There must be a CLEAR OPEN
> CENTRAL FLOOR AREA where 4 characters could move comfortably. NOT
> a cottage kitchen, NOT a home bakery, NOT crammed with furniture.

#### Se la finestra est mostra il paesaggio sbagliato:
> CRITICAL CORRECTION: Through the east window, the canonical view
> is: in the foreground the rear courtyard with neat stacks of split
> firewood; middle distance low grass and pastureland; far distance
> SOFT SILHOUETTES OF 3-4 SMALL STONE COTTAGES (Case del Mattino)
> backlit by the rising sun; above them a rose-peach-gold dawn sky
> with the sun just emerging. NO sea visible, NO mountains visible,
> NO trees in front of the window blocking the view, NO empty
> landscape. Just: cortile + grass + silhouetted cottages + dawn.

#### Se la palette è troppo fredda / con tonalità blu:
> CORRECTION: The entire palette is WARM — ochre, terracotta,
> ember orange, amber gold, warm earth brown, deep warm shadow.
> NO blue tones, NO cool white, NO grey-blue shadows. Even the
> shadows are warm earth-toned. The room is "the first warm
> point of the island in the morning" — heat in every surface.

#### Se Grok aggiunge una porta arched / hobbit-style:
> CORRECTION: Doors are SIMPLE WOODEN PLANK doors with iron
> hinges, rectangular shape, weathered dark wood. NO arched
> doorways, NO curved frames, NO Hobbit-style ornamental wood.
> The oven mouth has a rough natural arch (because it's built
> of stone) but doors are square and plain.

### 🎯 Checklist di approvazione

**Composizione per overlay testo:**
- [ ] Upper third = soffitto ALTO con travi a vista in legno scuro warm
- [ ] Tonalità uniforme/calma nell'upper third (basso contrasto)
- [ ] NO chandeliers/lampadari/oggetti pendenti che affollano l'upper third
- [ ] Spazio leggibile per testo overlay

**Scala / spazio (CRITICO v2):**
- [ ] Stanza AMPIA (~9×7 m), NON casa privata piccola
- [ ] Soffitto ALTO (~3.2 m), NON basso
- [ ] **Zona centrale del pavimento APERTA** (libera da mobili, circolazione)
- [ ] Lo spazio fa percepire "forno comune di borgo", non "cucina di casa"
- [ ] 4 personaggi (Fiamma + 3 fratelli) ci entrerebbero comodi con margine

**Punto di vista:**
- [ ] Vista 3/4 dall'angolo NORD-OVEST verso SUD-EST
- [ ] Nello stesso shot: forno (sud-est), banco impasto (sotto finestra est), mensole nord (sinistra), tavolo ovest (in primo piano basso parziale)
- [ ] Camera ad altezza child-perspective (~1.2-1.4m)

**Stanza:**
- [ ] Pareti ocra grezzo (intonaco hand-applied)
- [ ] Soffitto HIGH con travi a vista warm-dark
- [ ] Pavimento di terra battuta WIDE (NON piastrelle, NON parquet)
- [ ] Velo di farina sulla zona vicino al banco impasto

**Forno (focal element, COMMUNITY-SCALE v2):**
- [ ] Sulla parete sud-est, **bocca a cupola GRANDE (1.5-1.8 m wide)**
- [ ] Cupola architettonicamente imponente (massa visibile, non recess piccolo)
- [ ] Pietra grezza a fieldstone (non mattoni regolari)
- [ ] Bocca annerita di fuliggine
- [ ] Bagliore arancio-brace dalla bocca, distinct light source
- [ ] Catasta di legna spaccata accanto sul pavimento
- [ ] Pala di legno LUNGA (~2m) appoggiata al muro accanto
- [ ] Eventuali attrezzi forno (poker, ash rake) appesi vicino

**Banco da impasto (focal element, GENEROSO v2):**
- [ ] Sotto la finestra est, lungo (~2 m)
- [ ] Asse infarinata, legno chiaro consumato
- [ ] Ciotola in terracotta + impasto + mattarello + panno di lino + vasetto farina + eventuale seconda ciotola/palla di impasto in lievitazione
- [ ] Stato mid-process (qualcuno è appena stato qui, lavorazione multipla)
- [ ] Luce dell'alba dalla finestra est cade direttamente qui

**Finestra est e VISTA (CRITICA v2):**
- [ ] Media ~80×80cm, legno scuro
- [ ] Imposte aperte ripiegate verso l'interno
- [ ] **Vista canonica attraverso la finestra**:
  - [ ] Foreground: cortile retro con cataste di legna
  - [ ] Middle distance: erba bassa
  - [ ] Far distance: silhouette 3-4 Case del Mattino in controluce
  - [ ] Sky: alba rosa-oro con sole che sorge dietro le silhouette
- [ ] PRIMARY LIGHT della scena, shaft ambra diagonale sul banco

**Tavolo da pranzo (in primo piano parziale):**
- [ ] Verso parete ovest, in lower-left foreground
- [ ] Legno semplice, sgabelli/sedie
- [ ] Eventuale candela spenta + cup + piccolo pane
- [ ] Spazio aperto attorno (sedie non incastrate ai muri)
- [ ] Quietness (non è la zona attiva all'alba)

**Mensole nord (sinistra, COMMUNITY-QUANTITY v2):**
- [ ] **MOLTI cesti di vimini** (8-12+) con impasto in lievitazione + lino sopra (è forno comune che cuoce per tutti)
- [ ] Più vasi in terracotta di varie misure (farina, sale, miele, olio)
- [ ] Strofinacci di lino piegati
- [ ] Ganci di ferro con utensili in legno (mestoli, cucchiai, peels di varie misure, pentolini)
- [ ] Run generoso lungo la parete (non solo poche mensoline)

**Porta retro (parete est, accanto al forno):**
- [ ] Visibile, semplice tavole in legno, chiusa

**Zona porta principale (lower-left edge, parziale):**
- [ ] Hook con grembiule terracotta di scorta visibile (firma Fiamma) — opzionale
- [ ] Panchetta bassa + scopa appoggiata — opzionale

**Atmosfera:**
- [ ] Aria velata di pulviscolo di farina che cattura la luce
- [ ] Mood quieto/lavorativo/vivo
- [ ] Stanza "appena lasciata o appena aperta", NON staged

**Luce:**
- [ ] Two coexisting warm light sources (finestra est + bocca forno)
- [ ] Shaft ambra diagonale dalla finestra est sul banco impasto
- [ ] Bagliore arancio-brace dal forno sul pavimento + parete
- [ ] Ombre profonde negli angoli, sempre WARM (mai blu/cool)
- [ ] NO sparkles / NO magical light / NO neon

**Anti-cliché:**
- [ ] NESSUN personaggio, nemmeno mani/silhouette
- [ ] NESSUNA scritta (no labels su barattoli, no lavagne, no scritte)
- [ ] NO modern appliances / cookware (no inox, no plastic, no electric)
- [ ] NO commercial bakery (no display case, no menu)
- [ ] NO magical elements (no glowing dough, no sparkles)
- [ ] NO Hobbit-style (no round windows, no curved doors)
- [ ] NO postcard cheerfulness — quiet working mood
- [ ] NO regular masonry bricks (oven = rough fieldstone)
- [ ] NO arched doorways for non-oven openings
- [ ] NO cool palette / blue shadows
- [ ] NO pastry-shop elegance
- [ ] **NO home-kitchen scale (CRITICO v2): se sembra una cucina di casa → KO**
- [ ] **NO bocca forno piccola (CRITICO v2): bocca <1m = KO, deve essere 1.5-1.8m**
- [ ] **NO stanza piena di mobili senza spazio centrale (CRITICO v2)**

**Stile:**
- [ ] Painterly watercolor + sepia ink (Beatrix Potter)
- [ ] Palette dominante calda (ocra, terracotta, ember, amber, warm earth)
- [ ] Vista verticale 3:4

Se 35+ check ok → composizione canonica.
Se 25-34 check ok → iteriamo con prompt correttivo specifico.
Se <25 check ok → riscriviamo prompt principale.

**CHECK CRITICI v2 (i 3 vincoli centrali da Ray):**
- [ ] Scala forno comune di borgo (non casa privata)?
- [ ] Spazio interno arioso (4 personaggi entrano comodi)?
- [ ] Vista canonica dalla finestra est (cortile + Case del Mattino + alba)?
Se anche solo 1 di questi 3 fallisce → riscriviamo.

### 🔧 Note tecniche per l'overlay testo

Stesso schema dell'esterno:
- Area testo: rettangolo nei top 33% (sopra il soffitto a travi)
- Margini: ~5% da ogni lato
- Font suggerito: serif classico (Garamond, Caslon, Bembo)
- Colore testo: nero o seppia molto scuro (#2a1810)
- Allineamento: sinistra o giustificato
- Interlinea: 1.4-1.5x

NB: con soffitto a travi warm-dark uniforme, il contrasto del testo overlay
si gestisce bene. Se il soffitto risulta troppo scuro, considerare un sotto-banner semitrasparente warm-cream sotto il testo.

### 🔗 Riferimento canonico

Derivata da:
- `visual/luoghi/quartiere_fuoco/forno/scheda.md` — blocco LOCATION INTERNO + spatial layout canonico
- Bible §4.4 FIAMMA + §6 palette Quartiere di Fuoco + §8.2 Quartiere di Fuoco
- ARCHI_12_STORIE S1, S6, S8, S9, S12 (apparizioni interne)
- Pipeline visual layer A
- Pattern di luce derivato da "primo posto dell'isola dove c'è luce calda al mattino" (Bible §4.4 + §8.2)

### 🎨 Veduta 3 — Cortile retro
*da fare*

### 🎨 Veduta 4 — (da decidere)
*da fare*

---

## Note di workflow

- **Iterazione:** quando una veduta è canonica (≥22 check ok), Ray salva l'immagine in `immagini/forno_canonica_v1_<vista>.jpg`. Le canoniche v1 restano intoccabili come reference.
- **Scene con personaggi:** una volta che le 3-4 vedute reference esistono, le scene degli hook che includono il Forno (s01-s12 dove appare) si generano combinando la veduta reference + i prompt grok dei personaggi in scena. Il Forno mantiene così coerenza visiva cross-storia.
- **Modifiche al canone:** se durante l'iterazione emerge un dettaglio nuovo non presente in `scheda.md`, va aggiornata la scheda PRIMA di canonizzare la veduta (la scheda resta fonte autorevole).
