---
id: forno
name: Forno di Fiamma
famiglia: luogo
sottotipo: building
quartiere: fuoco
status: provvisorio
ultima_modifica: 2026-05-03
fonti: ["pipeline_narrativa/story_graph.json#entities.locations.forno", "cartografia/geo/island.geojson#features.id=forno"]
appare_in_storie: []
ha_interno: true
ha_esterno: true
ha_cortile_o_annessi: true
cartografia:
  feature_id: forno
  type_geo: building
  status_geo: canonico
  quarter: fuoco
  category: bakery
  centroid_m_local: [5106, 3500]
  bbox_m_local: [5106, 3500, 5106, 3500]
  size_m_local: [0, 0]
  altitudine_m: null
  geometry_type: Point
  parent_geo: null
  children_geo: []
  aliases_geo: []
---


# Forno di Fiamma

> **Stato compilazione:** body provvisorio, completato 2026-04-29 con derivazione autoriale dalle fonti canoniche (Bible §4.4, §6, §8.1, §8.2; ARCHI_12_STORIE §S1, §S6, §S8, §S11, §S12; grafo entities.locations.forno; Glossario §2.3; cartografia island.geojson). Aggiornato 2026-04-30 con scala "forno comune di borgo". Aggiornato 2026-05-03 con **planimetria a 2 sale comunicanti** (laboratorio + dispensa-pranzo) + set di **5 immagini canoniche reference** in `immagini/`.
>
> **⚠️ STRATEGIA LUOGHI RICORRENTI:** il Forno appare in 7 storie (s01, s06, s08, s09, s10, s11, s12). Per questo è uno dei pochi luoghi con un **set canonico di 5 vedute pre-generate** (vedi `immagini/forno_canonica_v1_*.jpg`). Le scene future con personaggi si compongono SOPRA queste reference + prompt grok dei character canon. NON rigenerare le canoniche.
>
> **⚠️ LUOGO CON 2 SALE INTERNE + ESTERNO + CORTILE:** scegliere la veduta corretta in base a dove si svolge la scena. Vedi mappa scene → veduta in fondo.

## Identità visuale (sintesi)

**Tipo:** edificio (forno comune di borgo).
**Quadrante:** fuoco_est.
**Abitante:** fiamma.
**Ruolo saga:** cornice_s1_s12 (apertura e chiusura saga, simmetria strutturale).

**Forno comune dell'isola** — Fiamma cuoce pane per tutti gli abitanti, ogni giorno. NON è una panetteria di casa né un forno domestico: è il forno comunitario, intermediate tra casa privata e bottega. Casa-forno bassa di pietra grezza con tetto inclinato e camino che fuma prima dell'alba. **Primo posto dell'isola dove c'è luce calda al mattino**, presenza di calore relazionale ed elementare. Cornice strutturale della saga: apertura S1, chiusura S12.

**Articolato in 4 sotto-aree** (vedi planimetria canonica `immagini/forno_planimetria_canonica.jpg`):
1. **Esterno** — facciata ovest sulla Via dell'Alba, camino fumante
2. **Sala Laboratorio** (sala A, interna) — 2 forni a cupola + tavolone impasto + mensole utensili, sala con tetto a falda alto
3. **Sala Dispensa-Pranzo** (sala B, interna, comunicante con A) — mensole stipate di cesti+vasi + tavolo+panche, porta sul cortile retro
4. **Cortile retro** — tettoia con legna catastata, ceppi spaccati, prospettiva sul retro casa

## Planimetria canonica a 2 sale (sintesi schematica)

```
ESTERNO ovest (facciata, Via dell'Alba)
      │
      ▼
┌──────────────────────────────────────┐
│   SALA LABORATORIO (sala A)           │
│   tetto a falda alto, travi a vista   │
│   - tavolone impasto sulla parete sx │
│   - 2 forni cupola sulla parete dx   │
│   - mensole utensili a dx accanto ai │
│     forni                             │
│   - finestra est sopra il tavolone    │
│     (vista alba + Case del Mattino)   │
└──────────────────────────────────────┘
            │ porta interna │
            ▼               ▼
┌──────────────────────────────────────┐
│   SALA DISPENSA-PRANZO (sala B)       │
│   - mensole stipate cesti+vasi sx    │
│   - tavolo+panche al centro          │
│   - porta che dà sul cortile retro    │
└──────────────────────────────────────┘
      │
      ▼
CORTILE RETRO est
- tettoia con legna catastata
- ceppi spaccati a terra
- retro casa visibile
```

Ogni sala ha **almeno 2 vedute canoniche** generate in `immagini/`.

## Aspetto / forma — geografia generale

Costruzione di pietra grezza intonacata, tetto a falda con embrici di terracotta scura, **2 sale interne comunicanti via porta interna** (laboratorio + dispensa-pranzo) + cortile retro. La pianta complessiva è **rettangolare allungata** sul piano nord-sud, indicativamente **~9×12 metri** totali (sala laboratorio ~9×7, sala dispensa-pranzo ~6×5, comunicanti). **Soffitto interno alto ~3.2 metri** con travi a vista in legno scuro nella sala laboratorio (struttura a falda visibile dall'interno).

**Scala canonica**: il Forno NON è una "panetteria di casa" né un forno domestico. È il **forno comune dell'isola** — Fiamma cuoce pane per tutti gli abitanti, ogni giorno. Riferimento mentale: forno comune di borgo medievale-mediterraneo, intermediate tra casa privata e bottega comunitaria. Spazio interno **arioso**: 4-5 personaggi (Fiamma + 3 fratelli + eventuale ospite) si muovono comodamente con margine, mai claustrofobia.

**Quattro sotto-aree distinte** (con vedute canoniche in `immagini/`):

### 1. Esterno (facciata ovest sulla Via dell'Alba)
Facciata principale sulla **Via dell'Alba**, orientata a ovest verso il villaggio centrale. Porta principale di legno scuro + piccola finestra ovest con imposte. Sul lato est della casa c'è una **finestra orientata a est** da cui entra la prima luce dell'alba (fondamentale, "primo posto dell'isola dove c'è luce calda al mattino"). **Camino** che sporge dal tetto, fuma prima dell'alba.
→ Reference: `immagini/forno_canonica_v1_esterno_alba.jpg`

### 2. Sala Laboratorio (sala A, interna)
La sala del lavoro pane. Tetto a falda alto con travi a vista in legno scuro (~3.2 m), pareti intonacate ocra grezzo, pavimento di terra battuta velata di farina.

**Layout canonico:**
- **Parete sinistra (ovest)**: lungo **tavolone da impasto** in legno (~2 m), asse infarinata, ciotole, mattarello, lino. Sotto la finestra principale che porta luce.
- **Parete destra (est)**: **2 grandi forni a cupola di pietra** affiancati, costruiti in fieldstone, ciascuno con bocca ~1.5-1.8 m di larghezza. Banchetta separatrice tra i due forni. Cappa/canna fumaria centrale che sale al tetto.
- **Mensole** sulla parete destra accanto ai forni e/o tra i forni: utensili in legno e ferro, pale lunghe, ciotole.
- **Finestra est** (sopra il tavolone o sulla parete est): porta la prima luce dell'alba sul tavolone. Vista canonica attraverso: cortile retro + erba + silhouette Case del Mattino in controluce + cielo rosa-oro.
- **Zona centrale** del pavimento aperta (circolazione personaggi).
- **Porta interna** sul lato sud che porta alla Sala Dispensa-Pranzo.
- Possibile alcove sotto la base dei forni per legna catastata pronta all'uso.

→ Reference principali:
- `immagini/forno_canonica_v1_laboratorio_panoramica.jpg` (establishing shot frontale, 2 forni)
- `immagini/forno_canonica_v1_laboratorio_dettaglio.jpg` (close-up uno dei forni acceso + impasti)
- `immagini/forno_canonica_v1_laboratorio_verticale.jpg` (vista verticale 3:4 con finestra centrale, utile per overlay testo)

### 3. Sala Dispensa-Pranzo (sala B, interna, comunicante con sala A)
La sala "domestica" dove Fiamma vive e dove avvengono le scene intime (compleanno Gabriel s09, dolce serale s12). Pavimento in pietra (cotto/lastricato) o terra battuta, soffitto più contenuto.

**Layout canonico:**
- **Parete sinistra (ovest)**: **mensole stipate** floor-to-ceiling di cesti di vimini + vasi terracotta + anfore (provviste della dispensa). Quantità abbondante = "comunità".
- **Centro stanza**: **tavolo rettangolare in legno** + 2 panche (4-6 posti). Tavolo del pranzo + delle scene intime serali.
- **Parete sud / dx**: porta che dà sul **cortile retro** (visibile aperta nelle scene diurne).
- Possibili: piccolo banco aggiuntivo, alcove con anfore, candela sul tavolo di sera.

→ Reference principale: `immagini/forno_canonica_v1_dispensa_pranzo.jpg`

### 4. Cortile retro (esterno, lato est)
Piccolo cortile sul retro (lato est), senza recinzione, raggiungibile dalla porta posteriore della Sala Dispensa-Pranzo. **Tettoia in legno** che protegge cataste regolari di **legna spaccata** (provviste per il forno). **Ceppi spaccati** a terra, ascia. Retro casa visibile in pietra. Da qui parte un sentiero che si perde nell'erba verso est (in direzione Case del Mattino, Fiume, fascia costiera).

→ Reference: `immagini/forno_canonica_v1_cortile_retro.jpg`

---

**Posizione**: **Quartiere di Fuoco a est**, lungo la **Via dell'Alba**, **30 minuti** a piedi dal Villaggio centrale (Bible §8.1). Vicine ci sono le **Case del Mattino** (fabbro, conceria, essiccatoio per la frutta in autunno) — 3-4 case lungo la via, ma il Forno è la prima e la più importante del quartiere.

## Espressione / comportamento (dinamica del luogo)

Il Forno si sveglia **prima del resto dell'isola**. Il camino comincia a fumare quando è ancora buio — il fumo è il primo segno che la giornata sull'isola sta cominciando. Quando il sole sorge a est, la prima luce calda dell'alba (Vento Taglio entra da est, taglia la nebbia) entra dalla finestra est e illumina il banco da impasto. Tutta la mattina, l'odore del pane caldo si diffonde lungo la Via dell'Alba e oltre. Il **suono caratteristico** è il **TOK-TOK ovattato** dell'impasto sull'asse di Fiamma (Bible §8.2 — uno dei suoni-firma del Quartiere di Fuoco, insieme al battito metallico del fabbro più giù sulla via).

**Stati tipici della giornata:**

- **Alba**: forno acceso da prima dell'alba, camino fumante, finestra est inizia ad accogliere la prima luce, Fiamma in piena attività di impasto. Stato canonico di apertura S1, S8, S10, S12.
- **Mattino**: pane appena sfornato, banco con cornetti e pagnotte, finestra a est illuminata pienamente, calore alto in stanza.
- **Mezzogiorno**: forno meno attivo, Fiamma può andare al Mercato o restare in casa a sistemare. Calore residuo.
- **Pomeriggio**: pausa o lavoro lento. In autunno (S11), banco dolci preparato per la festa.
- **Sera**: forno spento ma ancora caldo. Stanza in modalità ferma. Stato canonico di chiusura S12 (lampada accesa, candela sul tavolo, sera che diventa notte).
- **Notte**: imposte chiuse (vedi S8: "Fiamma chiude le imposte: 'a casa veloci'"), camino spento. Mai mostrato.

## Palette e atmosfera

**Quartiere di Fuoco a est** (Bible §6): **terracotta, rosso brace, oro**.

**Esterno**: terracotta degli embrici, ocra dell'intonaco, marrone-scuro del legno della porta e degli infissi, verde tenue della vegetazione spontanea attorno (erba, qualche cespuglio), azzurro tenue del cielo a est, fumo grigio-azzurrino dal camino al mattino.

**Interno**: **dominante calda** — ocra delle pareti, **rosso brace** del fuoco nel forno, **oro** della luce dall'est al mattino, marrone caldo del legno (banco, tavolo, mensole), bianco-avorio della farina ovunque, terracotta delle ciotole, grigio-fumo soffuso dell'aria carica di pulviscolo. Quando il forno è acceso, c'è un **bagliore arancio-brace** che proviene dalla bocca del forno.

**Cortile**: ocra del terreno battuto, marroni del legno catastato, verde tenue dell'erba spontanea, cielo azzurro tenue.

**Tipo di luce dominante**: SEMPRE CALDA. Il Forno non vede mai luce fredda dentro (anche di sera la candela e il forno residuo tengono il caldo). All'esterno la luce varia col giorno ma è **sempre dominante calda al mattino** (alba a est).

**Atmosfera predominante**: ACCOGLIENTE, LAVORATIVA, VIVA. Mai solenne, mai monumentale. Sempre "casa di chi lavora il pane".

## Contesto e ambientazioni ricorrenti

Posizione precisa: **Quartiere di Fuoco a est, lungo la Via dell'Alba, 30 minuti a piedi dal Villaggio centrale**. La Via dell'Alba esce dalla Piazza del Villaggio verso est e arriva al Forno; oltre il Forno, la via prosegue per le **Case del Mattino** (fabbro, conceria, piccolo essiccatoio per frutta in autunno) e poi degrada verso il Fiume e la fascia costiera est.

**Vento dominante**: **Vento Taglio** entra da est all'alba — taglia la nebbia, rende le cose nitide. Il Forno è il primo edificio dell'isola che riceve il Vento Taglio ogni mattina.

**Vicini**:
- A est della Via dell'Alba (più verso il Fiume): **Case del Mattino**
- A ovest (più verso il Villaggio): la Via dell'Alba che continua, eventualmente prima casa di un Camminatore o di un Mantenitore
- A nord/sud immediato: campi/erba, niente edifici diretti

**Ruolo nelle storie:**
- **Cornice S1 ↔ S12**: apertura e chiusura saga (sigillo strutturale, decisione #22)
- **S6**: tappa uno del giro, modalità chiacchiera Fiamma, cornetti, detto popolare
- **S8**: cornice apertura (cornetto, vento alzarsi, "a casa veloci") + cornice ritorno
- **S9**: location_primary (compleanno Gabriel)
- **S10**: cammeo all'alba al ritorno (cuore caldo)
- **S11**: cammeo banco dolci durante la festa
- **S12**: cornice apertura mattino (pagnotta a Grunto) + chiusura sera (dolce normale, quattro fette, sigillo della saga)

## Coerenza cross-scena (cose che NON cambiano)

**Esterno:**
- Casa bassa di pietra grezza intonacata ocra
- Tetto a falda con embrici di terracotta scura
- Camino che fuma prima dell'alba (in ogni scena di mattino canonico)
- Porta principale di legno scuro sul lato ovest (verso la Via dell'Alba)
- Finestra piccola sul fronte (lato ovest)
- Finestra orientata a est (la finestra "che porta la prima luce")
- Posizione lungo la Via dell'Alba, primo edificio del Quartiere di Fuoco
- Niente recinzione

**Sala Laboratorio (sala A):**
- Sala AMPIA (~9×7 m), soffitto ALTO ~3.2 m con travi a vista
- Sensazione di SPAZIO ARIOSO (4 persone si muovono comodamente, mai claustrofobia)
- Pavimento di terra battuta velata di farina
- Pareti intonacate ocra grezzo
- **2 grandi forni a cupola** affiancati sulla parete EST (forno comune di borgo), ciascuno con bocca ~1.5-1.8 m, fieldstone, banchetta separatrice tra i due
- **Cappa/canna fumaria centrale** che sale al tetto
- **Lungo tavolone da impasto** (~2 m) sulla parete OVEST sotto la finestra principale
- **Finestra est** sopra il tavolone (o sulla parete est) che dà sul cortile retro + vista alba con silhouette delle Case del Mattino in controluce
- **Mensole** sulla parete EST accanto/tra i forni con utensili, pale lunghe, ciotole
- **Zona centrale aperta** (circolazione)
- Pavimento e ogni superficie leggermente velata di farina

**Sala Dispensa-Pranzo (sala B, comunicante con A via porta interna):**
- Sala più contenuta (~6×5 m), soffitto un po' più basso
- **Mensole stipate** floor-to-ceiling sulla parete OVEST (cesti di vimini, vasi terracotta, anfore — quantità abbondante = forno comunitario)
- **Tavolo rettangolare in legno + 2 panche** al centro stanza (4-6 posti)
- **Porta** sulla parete sud/est che dà sul **cortile retro** (visibile aperta nelle scene diurne)
- Pavimento in pietra/cotto o terra battuta
- Possibili: piccolo banco accessorio, candela sul tavolo nelle scene serali

**Cortile retro:**
- **Tettoia in legno** che protegge cataste regolari di legna spaccata
- Ceppi spaccati a terra
- Retro casa visibile in pietra
- Niente recinzione, sentiero che si perde nell'erba verso est

**Cortile retro:**
- Cataste di legna regolari contro la parete posteriore
- Terra battuta
- Niente recinzione, sentiero che si perde nell'erba

## Variabilità ammessa

**Stagione:**
- **Primavera**: erba spontanea fiorita attorno, finestre più aperte, cataste di legna meno alte (consumate dall'inverno).
- **Estate**: cataste di legna basse, porta posteriore aperta nelle ore calde.
- **Autunno** (S6, S11): cataste di legna ricostituite, banco dolci esposto in casa o fuori per la festa, foglie cadute attorno.
- **Inverno** (S5? S8?): cataste molto alte, fumo del camino sempre presente di giorno, eventualmente brina o neve sul tetto, embrici scuri di umidità.

**Ora del giorno:**
- **Alba**: camino fumante, finestra est che si illumina, dentro buio caldo con bagliore brace.
- **Mattino**: luce piena dalla finestra est, dentro caldo dorato, banco coperto di pane fresco.
- **Pomeriggio**: luce neutra, dentro più calmo, forno meno attivo.
- **Sera**: lampada/candela sul tavolo, fuori scuro, finestre con luce gialla che esce.
- **Notte**: imposte chiuse, finestre che mostrano solo eventuale fessura di luce, camino spento.

**Stato del forno**: **acceso** (default in scene mattutine, fumo + bagliore arancio dalla bocca) o **ancora caldo** (sera tarda, forno spento ma luce calda residua) o **spento** (rare, mai mostrato pieno).

**Presenza di pane/dolci**: pagnotte, cornetti, dolci sul banco a seconda della scena. In S12 chiusura: dolce normale tagliato in 4 fette, candela sul tavolo.

**Mai variabile:**
- Posizione del forno (parete sud-est)
- Posizione del banco (sotto finestra est)
- Disposizione generale (stanza unica)
- Materiali di costruzione
- Orientamento della casa
- Presenza del camino

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

**Specifici per il Forno:**
- Mai forno "magico" / con luce dorata sovrannaturale che esce dalla bocca / con simboli incisi sulla pietra.
- Mai forno "a tema fiabesco" con decorazioni elaborate, tegole colorate, finestre tonde alla Hobbit.
- Mai panetteria "pittoresca da cartolina" con bandierine, fiori dipinti sulle imposte, festoni.
- Mai forno "industriale" o "moderno" — è pre-industriale, popolare, funzionale.
- Mai forno "abbandonato" o "sporco" in modo drammatico — è ben tenuto e vissuto.
- Mai vetrate grandi o porte ad arco elaborate.
- Mai segnaletica/insegne dipinte ("Forno di Fiamma" scritto sulla porta, ecc.) — non c'è scrittura sul mondo dell'isola.
- Mai folla davanti al forno — è un luogo di intimità e cammei, non di affollamento.
- Mai cornetti/dolci "da pasticceria europea elegante" — pane e dolci sono semplici, rustici, casalinghi.
- Mai ombre lunghe drammatiche all'esterno — luce calda diffusa.
- Mai panificio "tedesco" / "francese" / "italiano del nord" stilizzato — l'isola ha un suo registro pre-industriale generico mediterraneo.
- Mai forno con pietre regolari da masonry medievale — la pietra è grezza, irregolare.
- **Mai interno "da casa privata" piccolo e claustrofobico** — è un forno comune di borgo, ampio, ariato, alto. Mai stanza dove 4 personaggi si pestano i piedi.
- **Mai bocca del forno piccola da forno domestico** (50-80cm) — è grande (1.5-1.8m), da forno comunitario.
- Mai pochi cesti di proofing (è forno comune che cuoce pane per tutti gli abitanti — le ceste sono molte).

---

## ⭐ Descrizione visiva canonica per generazione — ESTERNO

⚠️ **BLOCCO LOCATION ESTERNO** da incollare nei prompt Grok delle scene ambientate **fuori dal Forno** (sulla Via dell'Alba, davanti alla porta, viste dall'esterno).

```
LOCATION (EXTERIOR) — Forno di Fiamma:
A small low stone bakery house in the Eastern Quarter of an island, facing 
the Via dell'Alba (Dawn Way) — the path that runs east from the village. 
This is the first building of the morning, the first place on the island 
where warm light appears at dawn.

The building is a single-story rectangular structure, approximately 6 by 
5 meters at the base. Walls of rough-plastered stone in warm ochre color, 
showing texture and slight irregularity (hand-built, pre-industrial). 
A pitched roof covered in dark terracotta tiles, with a stone chimney 
rising from the back-right corner — smoke rises gently from the chimney 
in the early morning. The chimney has a slightly tapered shape, simple 
construction.

On the front facade (facing west, toward the Via dell'Alba), there is a 
single wooden door — dark weathered wood, simple plank construction with 
iron hinges — and a small square window beside the door with wooden 
shutters and small panes. On the EAST side of the building (the side 
facing the rising sun), there is a slightly larger window — this is the 
"window that brings the first light", oriented to catch the dawn directly 
each morning.

In front of the building, the unpaved Via dell'Alba — a packed earth 
path with grass growing at the edges — runs past. To the right of the 
building (further east along the path), other simple low houses can be 
glimpsed in the distance: the Houses of Morning (Case del Mattino), where 
a blacksmith and other early-rising workers live. To the left, the path 
continues toward the village.

Around the bakery: low grass, a few wild flowers in spring, perhaps a 
clay water jug or a wooden bucket near the door, a wooden bench against 
the front wall (worn smooth by years of use). No fence, no decorative 
elements, no signage on the door (writing does not appear in this world).

Atmosphere: serene, lived-in, dignified. The first warm point of the day. 
Lighting depends on the scene's time:
- Dawn: orange-pink eastern sky, smoke from chimney visible against pale 
  light, the east-facing window glowing softly from inside, front of 
  building still in dawn shadow.
- Morning: full warm sunlight on the building, smoke trail thinner, 
  shadows soft.
- Evening: building silhouette against violet-orange western sky, warm 
  yellow light visible through the windows.

Color palette: terracotta brown (roof tiles), warm ochre (stone walls), 
dark weathered brown (wooden door and shutters), pale gold (warm window 
light spilling outside), soft sage green (surrounding grass and 
vegetation), muted sky blue or warm dawn orange (sky depending on scene), 
gray-blue (chimney smoke).

NO sign, NO Hobbit-style round windows, NO arched doorways, NO painted 
shutters with flowers, NO bunting, NO crowds outside, NO industrial 
elements.
```

---

## ⭐ Descrizione visiva canonica per generazione — INTERNO

⚠️ **BLOCCO LOCATION INTERNO** da incollare nei prompt Grok delle scene ambientate **dentro il Forno** (impasto, pranzo, sera, S1, S6, S9, S12 chiusura, ecc.).

```
LOCATION (INTERIOR) — Forno di Fiamma:
The interior of a community-scale rural bakery — Fiamma's workplace
where bread for the WHOLE ISLAND is baked daily. NOT a small private 
home kitchen. A single large rectangular room about 9 by 7 meters, with 
a relatively HIGH CEILING (about 3.2 meters) showing dark wooden exposed 
beams running across. The room must FEEL SPACIOUS — air can circulate 
around the oven heat, four characters can move around comfortably with 
margin. Reference: the communal oven of a small medieval-Mediterranean 
village, intermediate scale between private home and craft workshop.

The floor is packed earth, smooth from years of use, slightly dusted 
with flour everywhere. The walls are rough-plastered in warm ochre, 
showing the texture of hand-applied plaster. A generous OPEN CENTRAL 
AREA between oven, kneading table and dining table — circulation space.

SPATIAL LAYOUT (very specific, do not vary):

- On the SOUTH-EAST WALL: a LARGE STONE BREAD OVEN — community-scale, 
  not a home oven. The dome is a substantial architectural feature, 
  rising prominently from the wall. The DOMED MOUTH OPENING is about 
  1.5 to 1.8 meters wide and ~1 meter tall, slightly arched at the top. 
  The oven is built of rough fieldstone with earth mortar, soot-darkened 
  around the mouth. When lit, embers and a small fire inside cast a 
  warm orange-brick glow into the room — strong enough to read as a 
  distinct light source. A LONG WOODEN PEEL (bread paddle, ~2 m long) 
  leans against the wall beside the oven. A stack of split firewood 
  ready to feed the fire rests on the floor nearby.

- Under the EAST WINDOW (the window that brings the first dawn light): 
  a LONG WOODEN KNEADING TABLE, generous in size — about 2 m long, 
  0.9 m deep, modest height. Heavily floured surface, weathered light 
  wood with visible grain. On the table: a stoneware bowl (terracotta 
  color), a mound of pale dough, a wooden rolling pin, a linen cloth 
  folded to one side, a small clay pot of flour, perhaps a second 
  bowl with a different dough preparation. The amber dawn light from 
  the east window falls directly on this table — this is the canonical 
  "first warm point of the island in the morning".

- THE EAST WINDOW (CRITICAL — defines the canonical morning light):
  Positioned on the EAST WALL, directly above the kneading table. 
  Medium-sized (~80×80 cm), wooden frame, dark weathered wood, simple 
  shutters folded open inward. THROUGH THIS WINDOW, the view is:
  * Foreground: the REAR COURTYARD (forno_cortile) with neat stacks 
    of split firewood against the back wall, packed earth ground.
  * Middle distance: low grass and gentle pastureland extending east.
  * Far distance: SILHOUETTES OF THE CASE DEL MATTINO (Houses of the 
    Morning — 3-4 small stone cottages further east along the path), 
    backlit by the rising sun, very soft and atmospheric.
  * Sky: the dawn, rose-peach-gold gradient, the sun just emerging 
    behind the silhouetted houses (or about to). This is what makes 
    the room "the first warm point of the island in the morning".
  The window may also have a tiny clay water jug on its sill.

- AGAINST THE WEST WALL: a WOODEN DINING TABLE, weathered light wood, 
  rectangular, with 4 to 6 wooden chairs/stools around it. Modest, 
  scratched from use, with a small clay candle holder and a few cups. 
  Positioned with enough open space around it for people to sit and 
  walk past comfortably.

- ON THE NORTH WALL: a generous run of wooden shelves at varying 
  heights, holding many wicker proofing baskets with rising dough 
  (a community bakery has DOZENS, not a few), stoneware jars (flour, 
  salt, honey), a stack of clean linen cloths, kitchen utensils hanging 
  from iron hooks (ladles, wooden spoons, peels of varying sizes, a 
  few iron pans). The quantity reads "this is a working community 
  bakery", not a home kitchen.

- NEAR THE FRONT DOOR (west wall, opposite the kneading table area): 
  a wooden coat hook with a spare TERRACOTTA-RED APRON (Fiamma's 
  signature) and a shawl, a low wooden bench, a broom leaning against 
  the wall. The front door itself: simple wooden plank door, dark 
  weathered wood, iron hinges, currently closed (or ajar depending 
  on scene).

- THE BACK DOOR is on the EAST WALL (next to the oven, opposite the 
  kneading table), leading out to the rear courtyard with stacked 
  firewood. Simple wooden plank door, currently closed.

- The chimney is built into the south-east wall above the oven, rising 
  internally through the back of the room and exiting through the roof.

- CENTRAL FLOOR: a WIDE OPEN AREA in the middle of the room, free of 
  furniture — the natural circulation space where the baker (and 
  visiting characters) move between oven, kneading table, dining 
  table. This emptiness is essential to the scene's feel of breath 
  and capacity.

ATMOSPHERE:
The air is slightly hazy with flour particles catching the light, and 
faintly smoky from the oven. The smell of baking bread is implied 
visually by the warm color of the walls and the soft glow.

LIGHTING (default — adjust for specific scene):
- Dawn / morning: WARM AMBER LIGHT streams from the east window onto 
  the kneading table, soft warm glow from the open oven mouth. Strong 
  contrast between the bright lit areas and the deeper warm shadows in 
  the corners.
- Day: full warm light from both the east window and the front (west) 
  window, more even illumination.
- Evening: oven still warm but not bright, a single CANDLE on the dining 
  table provides the main light, the room is in soft amber shadow, the 
  windows show dim purple-blue exterior light.
- Night: oven dim or out, candle on table, very soft light, deep warm 
  shadows.

Color palette: warm ochre (walls), dark brown (ceiling beams), light 
weathered wood (kneading table, dining table), terracotta (oven, bowls), 
ember orange (oven glow when lit), pale ivory (flour dust, linen), 
amber-gold (warm light), deep warm shadow (corners).

NO industrial appliances, NO metal cookware that looks modern, NO bright 
artificial lighting, NO clean polished surfaces, NO decorative wallpaper 
or painted patterns, NO writing on the walls. Everything is rustic, 
hand-made, used.
```

---

## ⭐ Descrizione visiva canonica per generazione — CORTILE RETRO

⚠️ **BLOCCO LOCATION CORTILE** da incollare nei prompt Grok delle scene ambientate **nel cortile retro del Forno** (cammei rari — Fiamma che prende legna, ecc.).

```
LOCATION (REAR COURTYARD) — Forno di Fiamma:
The small rear courtyard of the bakery, on the EAST side of the building 
(behind the oven wall). An open, unfenced area, about 5 by 4 meters, with 
packed earth ground.

Against the back wall of the bakery (the east-facing wall): NEAT STACKS 
OF SPLIT FIREWOOD, organized in long parallel rows, reaching about 1.5 
meters high. The wood is weathered light brown, with visible cut ends 
showing pale wood grain. The stacks are well-organized, the work of 
someone who tends them daily — not chaotic, but practical.

Other elements:
- A weathered wooden axe stuck in a chopping block near the wood pile
- A small lean-to structure or wooden shelter for keeping the wood dry 
  in rain (simple, wooden posts and a small thatched or shingled roof)
- Perhaps a few clay jars or wooden buckets stacked nearby
- A back door (the rear door of the bakery) opens directly onto this 
  courtyard

Beyond the courtyard, looking east: low grass, a faint earthen path that 
fades into the open countryside as it moves toward the Fiume (river) and 
the eastern coastal belt — but the path quickly disappears within 30-50 
meters into rough grass. The horizon shows distant hills or the eastern 
sea, depending on framing.

Atmosphere: utilitarian, practical, simple. Not picturesque, not 
decorated. The place where the daily work happens that supports the 
bakery's life.

Lighting (depending on scene):
- Morning: full warm east light directly on the wood stacks (the courtyard 
  faces east, gets the rising sun directly).
- Day: even warm light.
- Evening: in shadow, the bakery wall blocks the western light.

Color palette: warm light brown (firewood), darker brown (axe handle, 
wooden lean-to), ochre (rear bakery wall), packed earth brown (ground), 
sage green (grass beyond), muted sky.

NO fancy garden, NO flowers in pots, NO decorative elements, NO 
recreational furniture. This is a working space.
```

---

### ✏️ Note d'uso operative

**Mappa scene → veduta canonica da usare come reference:**

| Scena | Veduta canonica | File reference |
|---|---|---|
| S1 apertura: Fiamma sulla soglia, fratelli partono, pagnotta | **Esterno alba** (eventualmente "porta aperta" + cenno interno) | `forno_canonica_v1_esterno_alba.jpg` |
| S6 cammeo: Fiamma che parla impastando, cornetti, detto popolare | **Sala Laboratorio panoramica** o **dettaglio forno** (Fiamma al tavolone) | `forno_canonica_v1_laboratorio_panoramica.jpg` o `_dettaglio.jpg` |
| S8 apertura: fratelli finiscono cornetto, Fiamma chiude imposte | **Sala Laboratorio panoramica** (Fiamma al banco, fratelli al tavolo dispensa o entrano dalla porta interna) | `forno_canonica_v1_laboratorio_panoramica.jpg` |
| S8 ritorno: rifugio dei fratelli al Forno | **Sala Dispensa-Pranzo** (intimità) | `forno_canonica_v1_dispensa_pranzo.jpg` |
| S9 location primary: compleanno Gabriel al Forno | **Sala Dispensa-Pranzo** (tavolo + 4 fratelli + Fiamma) | `forno_canonica_v1_dispensa_pranzo.jpg` |
| S10 cammeo all'alba al ritorno: Fiamma sulla soglia o vista da fuori | **Esterno alba** | `forno_canonica_v1_esterno_alba.jpg` |
| S11 cammeo banco dolci festa | **Sala Laboratorio panoramica** (banco dolci esposto) o esterno (festa in piazza, da decidere) | `forno_canonica_v1_laboratorio_panoramica.jpg` |
| S12 mattino: pagnotta a Grunto | **Sala Laboratorio dettaglio** o panoramica | `forno_canonica_v1_laboratorio_dettaglio.jpg` |
| S12 sera (chiusura saga): dolce normale, 4 fette, candela | **Sala Dispensa-Pranzo** (tavolo + candela + Fiamma) | `forno_canonica_v1_dispensa_pranzo.jpg` |

**Cammei opzionali al cortile retro** (se mai servisse — Fiamma che prende legna, fratelli che spaccano legna): `forno_canonica_v1_cortile_retro.jpg`.

**Scene su 2 sale insieme** (raro, es. Fiamma alla porta interna che chiama i fratelli dalla sala dispensa): scegliere la sala dove avviene l'azione principale.

**Workflow scene future:** prendere la veduta canonica come BASE → comporre la scena aggiungendo i personaggi tramite character canon dei rispettivi prompt grok. NON rigenerare le canoniche.

**Per stile coerente nelle generazioni:** lo stile del set canonico è painterly watercolor + ink linework, palette warm earth, tradizione picture book inglese-mediterraneo (Beatrix Potter / Brian Wildsmith). Replicare questo stile in tutte le scene.

## Per stampa 3D / modello

Modello 3D del Forno utile per:
- Diorama di scene
- Modello di mondo per stampa libro

Indicazioni qualitative:
- Scala: coerente con personaggi (se Gabriel = ~28 cm in scala toy 1:6, il Forno misura ~84 cm di lato per 70 di altezza al colmo).
- Pezzo separabile: tetto rimovibile per vedere l'interno.
- Materiali: PLA / resina con post-stampa per texture pietra e legno.
- Forno interno: con LED arancio per simulare brace.

_Da fissare quando la scala canonica saga sarà decisa._

## Per narrativa e social

Vedere `descrizione_narrativa_social.md` nella stessa cartella.

**Registri d'uso testuale:**
- Voce narrante: "il Forno", "il Forno di Fiamma" (mai "la panetteria", mai "la casa di Fiamma" da solo).
- Mai descrizioni nuove fuori canone.
- Mai aggettivi morali ("magico", "incantato", "sacro", "rifugio dell'anima").
- L'odore del pane può essere richiamato in narrativa, ma con misura.

## Storie / scene di apparizione

- s01: secondary — cornice di apertura e chiusura **[esterno + interno]**.
- s02: assente.
- s03: assente.
- s04: assente.
- s05: assente.
- s06: secondary — tappa uno del giro, Fiamma modalità chiacchiera, cornetti, detto popolare **[interno]**.
- s07: assente.
- s08: secondary — cornice apertura (cornetto, vento alzarsi, Fiamma chiude imposte: "a casa veloci") + cornice ritorno **[interno principalmente]**.
- s09: location_primary — compleanno Gabriel **[interno + eventuale esterno per arrivo]**.
- s10: cammeo all'alba al ritorno — cuore caldo **[esterno o interno, da decidere D]**.
- s11: secondary — banco dolci durante la festa **[interno o festa esterna in Piazza, da decidere D]**.
- s12: secondary — cornice di apertura mattino + chiusura sera, simmetria s1↔s12 **[interno entrambe le cornici]**.

## Disallineamenti / domande aperte

- **Pianta interna a 2 sale (RISOLTO 2026-05-03)**: confermata con Ray la planimetria a 2 sale comunicanti (laboratorio + dispensa-pranzo) + cortile retro. 2 forni nella sala laboratorio, mensole stipate nella dispensa. Vedi `immagini/forno_planimetria_canonica.jpg` + sezione "Aspetto / forma — geografia generale".
- **Dimensioni 9×7 m sala laboratorio + 6×5 m sala dispensa (parz. RISOLTO)**: scala "forno comune di borgo" approvata. La cartografia (`bbox_m_local: [5106, 3500, 5106, 3500]`) resta a punto — non blocca le scene.
- **Numero forni interni (RISOLTO 2026-05-03)**: 2 forni a cupola affiancati nella sala laboratorio (canone planimetria). Niente forno esterno separato.
- **Banco dolci S11 dentro o fuori**: ancora aperto. Bible/ARCHI suggeriscono banco dolci durante la festa in Piazza centrale; il Forno potrebbe avere banco dolci interno ma per S11 la scena potrebbe spostarsi al Mercato. Fissare in fase D scrittura.
- **Cortile retro come spazio scena (parz. RISOLTO)**: ora ha veduta canonica `forno_canonica_v1_cortile_retro.jpg`. Resta da decidere se appare come cammeo in alcuna delle 12 storie (probabile no, ma reference disponibile per scene future di estensione saga).

## Riferimenti puntuali (citazioni dirette dalle fonti)

**Fonti canoniche dirette:**
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §4.4 FIAMMA: "Vive nel Quartiere di Fuoco a est, nella casa-forno col tetto basso e il camino che fuma prima dell'alba. La porta sul retro dà su un piccolo cortile di legna catastata."
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §6 PALETTE VISIVA — Quartieri: "Quartiere di Fuoco (Est): terracotta, rosso brace, oro."
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8.1 Distanze: "Forno di Fiamma: 30 minuti."
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8.2 Quartiere di Fuoco: "Lungo la Via dell'Alba. Primo quartiere che il sole tocca, primo che si sveglia. Contiene: Forno di Fiamma (la casa-forno col camino che fuma prima dell'alba), il cortile di legna catastata sul retro, le Case del Mattino (3-4 case di abitanti che lavorano col fuoco — un fabbro, una conceria, un piccolo essiccatoio per la frutta in autunno). Vento Taglio entra da est all'alba, taglia la nebbia, rende le cose nitide. Luce più chiara dell'isola al mattino. Odore: pane caldo. Suono: TOK-TOK ovattato dell'impasto sull'asse di Fiamma + battito metallico del fabbro."
- `architettura/ARCHI_12_STORIE_v1__1_.md` S8: "Fiamma chiude le imposte: 'a casa veloci'" (canonico imposte presenti).
- `architettura/ARCHI_12_STORIE_v1__1_.md` S12 chiusura saga: "Una lampada accesa al Forno di Fiamma, in fondo alla Via dell'Alba... Fiamma è dentro, non sta cuocendo — sta rimettendo a posto la cucina prima della notte... Tira fuori dal forno (ancora caldo) un piccolo dolce... Quattro fette... Una candela. Il dolce mangiato a metà." (canonico interno serale).
- `worldbuilding/GLOSSARIO_ISOLA.md` §2.3 Quartiere di Fuoco: "Il Forno di Fiamma — casa-forno col camino che fuma prima dell'alba. Il cortile di legna catastata — sul retro del Forno."
- `pipeline_narrativa/story_graph.json#entities.locations.forno`
- `pipeline_narrativa/story_graph.json#stories.s01.locations_secondary`: forno — "cornice_apertura_e_chiusura"
- `pipeline_narrativa/story_graph.json#stories.s06.locations_secondary`: forno — "tappa_uno_giro_fiamma_modalita_chiacchiera_cornetti_detto_popolare"
- `pipeline_narrativa/story_graph.json#stories.s08.locations_secondary`: forno — "cornice_apertura_finire_cornetto_fratelli_sentono_vento_alzarsi_fiamma_chiude_imposte_a_casa_veloci_piu_cornice_ritorno"
- `pipeline_narrativa/story_graph.json#stories.s09.location_primary`: forno
- `pipeline_narrativa/story_graph.json#stories.s11.locations_secondary`: forno
- `pipeline_narrativa/story_graph.json#stories.s12.locations_secondary`: forno — "cornice_apertura_mattino_chiusura_sera_simmetria_s1_s12"
- `cartografia/geo/island.geojson#features.id=forno`: building, quarter=fuoco, category=bakery, centroid_m_local: [5106, 3500].

**Derivazioni autoriali:**
- *Dimensioni 6×5 metri*: derivata da scala saga + pratica edifici rurali pre-industriali.
- *Pianta interna (forno parete sud-est, banco sotto finestra est, tavolo ovest, mensole nord)*: derivazione autoriale coerente con funzionalità (banco vicino alla luce della finestra est = "primo posto con luce calda"; forno separato dal banco; tavolo nella zona più "domestica" verso ovest).
- *Materiali (pietra grezza intonacata ocra, embrici terracotta scura, legno scuro)*: derivati da palette Quartiere di Fuoco + registro pre-industriale dell'isola.
- *Due finestre (ovest fronte, est laterale)*: derivata da §8.2 "Vento Taglio entra da est all'alba" + funzionalità (luce per impastare al mattino).
- *Imposte sulle finestre*: validato dal canone S8 "Fiamma chiude le imposte".
- *Niente segnaletica/insegne*: derivata dal registro pre-industriale + assenza di scrittura sul mondo dell'isola.
- *Cortile aperto senza recinzione*: derivato da "campagna" attorno + registro pre-industriale.
- *Tre sotto-aree distinte (esterno/interno/cortile) con tre blocchi LOCATION*: scelta operativa pipeline per stabilità delle scene multi-personaggio in spazi diversi.

**Cliché da evitare specifici visivi**: derivati da `PATTERN_AI_DA_BANDIRE_v1.md` (categorie generali) applicate al caso specifico forno-panetteria-rurale (mai magico, mai Hobbit, mai pittoresco da cartolina, mai industriale, mai pasticceria europea elegante).
