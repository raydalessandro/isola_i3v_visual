# La Bocca — Atlante vedute canoniche (prompt grok)

> **Scopo.** Reference visiva canonica per le scene della saga ambientate alla Bocca (canale dove il Fiume incontra il mare). Workflow: si genera 1 veduta canonica panoramica con Grok Imagine; le scene future con personaggi si compongono sopra questa reference + prompt grok dei character canon.
>
> **Pattern saga (luoghi):** la Bocca è luogo ricorrente del Quartiere d'Acqua, appare in s07 (zattera che esce nel mare), s10 (notte senza luna) e altre cornici. La reference canonica è la vista panoramica.
>
> **Riferimento canonico:** `visual/luoghi/quartiere_acqua/bocca/scheda.md` (BLOCCO LOCATION ESTERNO).

---

## Indice vedute

| # | Veduta | Versione | Status |
|---|---|---|---|
| 1 | Esterno panoramica (mattino) | v1 | ⏳ in iterazione |

---

## 🎨 Veduta 1 — La Bocca, panoramica esterna mattino — v1

**Versione:** 1.0 (prima generazione)
**Tipo:** establishing shot del canale
**Formato:** orizzontale 16:9 (es. 1536×864) per panoramica completa o 4:3 per inquadratura più contenuta
**Layout testo:** opzionale, top third con cielo aperto

**Modalità Grok:** text-to-image

**Filename atteso al salvataggio:** `bocca_canonica_v1_panoramica.jpg`

### 🎯 Obiettivo

Reference panoramica della Bocca (canale fiume-mare) con tutti gli elementi canonici visibili in un solo shot: acqua mista bicromatica, due promontori rocciosi sud, Pontile di Bartolo a ovest, scogliera + casa di Amo a est, Case Basse Pescatori in fondo, mare aperto sud. NESSUN personaggio (la reference è "scena vuota"; le scene con personaggi si compongono dopo).

### ⭐ PROMPT (copia-incolla in Grok)

```
A painterly illustrated landscape scene in the style of Beatrix Potter
and Brian Wildsmith — watercolor and thin sepia ink lines, warm earthy
palette, hand-drawn children's picture book aesthetic. Horizontal 16:9
composition, panoramic establishing shot. NO PEOPLE in the image.
NO text, NO writing, NO signs.

[LOCATION block — incolla integralmente il blocco LOCATION ESTERNO da
`visual/luoghi/quartiere_acqua/bocca/scheda.md`, sezione "Descrizione
visiva canonica per generazione — ESTERNO"]

VIEWPOINT: from a slightly elevated angle, north-east, looking south-
west toward the open sea opening. From this vantage we can see in a
single composition:
- The wooden Pontile (Bartolo's pier) extending from the west shore
  with its small thatched-roof hut at the far end (left foreground)
- The wide central channel with VISIBLE COLOR DIFFERENCES on the
  water surface (greenish-blue inner river water meeting paler
  silver-blue saltwater)
- The two natural rocky promontories framing the south opening
  (middle-distance), beyond which the OPEN SEA extends to the horizon
- The east cliff rising on the right, with Amo's small wooden house
  carved into the rock, and the small stone staircase descending to
  the water
- The Case Basse dei Pescatori (low fisherman houses) visible in the
  background behind the pier on the north-west shore
- The small wooden footbridge from the east side of the pier crossing
  to the Shell Beach (visible just behind the pier)
- A few seagulls in flight or floating

LIGHTING: morning — low east light from over the east cliff, golden
tones touching the west shore and the pier, water surface bright with
reflections, color difference between river and sea most visible,
warm soft shadows.

ATMOSPHERE: physical, salty, transitional, alive. The Bocca is a real
working river mouth, not a magical portal. Quiet, awake, lived-in.

═══════════════════════════════════════════
WHAT MUST NOT APPEAR (CRITICAL):
═══════════════════════════════════════════

- NO PEOPLE, NO characters, NO animals (except distant seagulls), NO
  figures of any kind, NOT EVEN silhouettes
- NO TEXT, NO WRITING, NO SIGNS, NO LETTERS — there is no writing
  on this island
- NO crashing waves, NO foam at the color boundary on the water
- NO tropical turquoise, NO magical sparkles on the water
- NO leaping fish, NO dramatic seabird formations
- NO dramatic sunset poster colors (gold/pink overdrive)
- NO modern boats: only simple wooden rowboats
- NO concrete, NO modern docks, NO iron railings
- NO lighthouse, NO maritime industrial elements
- NO large city or town visible — only the modest cluster of Case
  Basse and the Casa di Amo
- NO Disney/Pixar 3D rendering, NO over-stylized Studio Ghibli
- NO heavy black ink outlines (use thin warm sepia)
- NO ferries, NO sailboats, NO fishing trawlers (just small rowboats)

═══════════════════════════════════════════
STYLE NOTES:
═══════════════════════════════════════════

- TECHNIQUE: traditional watercolor and thin sepia ink illustration,
  hand-drawn quality with slight imperfections
- INK: warm brown-sepia lines, light touch, never harsh black, organic
- WATERCOLOR: soft luminous warm washes, visible texture on shores
  and rocks, slight color bleeds, watercolor pooling on the water
- PALETTE: deep greenish-blue (inner river water), pale silver-blue
  (outer sea water), sandy-cream (west/north shores), grey-brown
  (east cliff), green (low vegetation), dark weathered wood (pier,
  hut, boats), white-grey (gulls), warm gold dawn sky transitioning
  to soft blue overhead
- AESTHETIC: tradition of Beatrix Potter, Brian Wildsmith, classic
  European children's illustration. Coastal landscapes by an island
  illustrator, intimate scale, never grand or postcard-dramatic
- MOOD: alive, working, transitional. The threshold between inland
  river and open sea, captured in a quiet morning.
```

### 📋 Variazioni se Grok sbaglia

#### Se mancano le linee di colore sull'acqua:
> CRITICAL CORRECTION: The water surface MUST show CLEAR COLOR
> DIFFERENCES — DEEPER GREENISH-BLUE in the inner river part, PALER
> SILVER-BLUE toward the sea, with VISIBLE LINES where they meet
> creating gentle swirling patterns. This is the visual signature
> of La Bocca. NOT magical sparkles, just physical color contrast.

#### Se rende il mare troppo aperto (ignora la Bocca):
> CORRECTION: This is a RIVER MOUTH, not the open sea. The view
> shows the CHANNEL where the river meets the sea, with two
> natural rocky promontories framing the southern opening.
> Foreground/middle-ground is the channel itself with its shores;
> the open sea is only visible in the distance beyond the
> promontories.

#### Se mette personaggi:
> CRITICAL: NO PEOPLE in this image. NO Bartolo, NO fishermen, NO
> animal characters. Only the place: the channel, the pier (empty),
> the cliff with Amo's house (empty), the distant Case Basse
> (closed). Only background seagulls allowed. The scene is the
> place itself.

#### Se mette scritte/insegne:
> CRITICAL: NO TEXT, NO WRITING, NO SIGNS, NO LETTERS anywhere.
> The pier hut has no name. The houses have no signs. This is a
> world without writing.

#### Se la palette vira al tropicale:
> CORRECTION: This is a NORTHERN-MEDITERRANEAN-style coast, NOT
> tropical. The water is greenish-blue and silver-blue, NEVER
> turquoise or aquamarine. The rocks are grey-brown, NEVER white-
> tropical. The vegetation is sparse low grass, NEVER palm trees.

### 🎯 Checklist di approvazione

**Geometria della Bocca:**
- [ ] Canale largo (~80-150m) tra due sponde
- [ ] Due promontori rocciosi naturali a sud (frame dell'apertura)
- [ ] Mare aperto sud all'orizzonte oltre i promontori
- [ ] Sponda ovest sabbiosa-erbosa con il Pontile
- [ ] Sponda est rocciosa-cliff con casa di Amo
- [ ] Sponda nord-interna con Case Basse Pescatori (sfondo)

**Acqua (firma visiva):**
- [ ] Colori MISTI visibili: greenish-blue interno + silver-blue verso mare
- [ ] Linee di confine cromatico tra le due acque
- [ ] Movimento calmo (no crashing waves)
- [ ] No tropical turquoise

**Elementi sull'acqua:**
- [ ] Pontile di legno con capanna tetto di paglia in fondo
- [ ] Eventuale ponticello secondario verso Spiaggia delle Conchiglie
- [ ] Eventuali 1-2 piccole barche di legno semplici
- [ ] Qualche gabbiano in volo o sull'acqua

**Atmosfera/luce:**
- [ ] Mattino, luce bassa da est sopra il cliff
- [ ] Toni dorati su sponda ovest e pontile
- [ ] Cielo dawn warm transitioning to soft blue

**Anti-cliché:**
- [ ] NESSUN personaggio
- [ ] NESSUNA scritta
- [ ] No tropical, no magical, no postcard drama
- [ ] No modern boats / concrete / lighthouse
- [ ] Stile painterly watercolor + sepia ink (mai cartoon, mai 3D)

Se 18+ check ok → canonica.

### 🔧 Note tecniche per Grok Imagine

- **Modalità:** realistico/painterly. Mai cartoon, mai 3D.
- **Aspect ratio:** 16:9 orizzontale (panoramic establishing) o 4:3 se preferisci più contenuto.
- **Iterazione:** la difficoltà principale sarà il bicromatismo dell'acqua. Se non torna al primo colpo, usare la prima variazione correttiva.

### 🔗 Riferimento canonico

- `visual/luoghi/quartiere_acqua/bocca/scheda.md` (BLOCCO LOCATION ESTERNO completo)
- Bible §8.5 Quartiere d'Acqua + grafo `entities.locations.bocca`
- Cartografia `island.geojson#features.id=bocca`
