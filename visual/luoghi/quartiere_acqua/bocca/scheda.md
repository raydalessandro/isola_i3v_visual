---
id: bocca
name: La Bocca
famiglia: luogo
sottotipo: river_mouth
quartiere: acqua
status: provvisorio
ultima_modifica: 2026-04-29
fonti: ["pipeline_narrativa/story_graph.json#entities.locations.bocca", "cartografia/geo/island.geojson#features.id=bocca"]
appare_in_storie: []
ha_interno: false
ha_esterno: true
ha_cortile_o_annessi: false
cartografia:
  feature_id: bocca
  type_geo: river_mouth
  status_geo: canonico
  quarter: acqua
  category: null
  centroid_m_local: [4005, 900]
  bbox_m_local: [4005, 900, 4005, 900]
  size_m_local: [0, 0]
  altitudine_m: null
  geometry_type: Point
  parent_geo: null
  children_geo: []
  aliases_geo: []
---


# La Bocca

> **Stato compilazione:** body provvisorio, completato 2026-04-29 con derivazione autoriale dalle fonti canoniche (Bible §8 cosmogonia, §8.3, §6; ARCHI_12_STORIE §S7; grafo entities.locations.bocca; Glossario §2.4; cartografia island.geojson). Le sezioni in derivazione sono dichiarate in "Riferimenti puntuali".
>
> **⚠️ STRATEGIA LUOGHI:** questo luogo NON ha immagine di reference per scene multi-personaggio. Il blocco LOCATION testuale è il riferimento per i prompt scena.
>
> **⚠️ LUOGO-CONTENITORE:** La Bocca è un body of water (river mouth, foce). Contiene il Pontile di Bartolo come elemento. Quando una scena è AL Pontile, si usa il blocco LOCATION del Pontile, non quello della Bocca. Si usa il blocco della Bocca per scene che mostrano il canale d'acqua nella sua interezza, eventuali traversate, o il "passaggio dal Fiume al mare".

## Identità visuale (sintesi)

**Tipo:** river mouth (foce del Fiume).
**Quadrante:** acqua_sud.
**Abitante:** nessun abitante diretto (nelle vicinanze: Bartolo sul Pontile, Pescatori nelle Case Basse, Amo sulla scogliera est).
**Ruolo saga:** punto cosmogonico del mondo (apertura sud dell'anello del Fiume, dove l'isola incontra il mare aperto).

La Bocca è il **canale dove il Fiume sfocia nel mare**. Punto di apertura sud dell'anello del Fiume — il Fiume gira intorno alla terra interna come un cerchio quasi chiuso, e La Bocca è uno dei due punti di interruzione (l'altro è il guado di pietre piatte a nord). Qui le **acque dolci e salate si mescolano**, creando l'**acqua mista** caratteristica del luogo. Larga abbastanza per le barche, ospita il Pontile di Bartolo, le Case Basse dei Pescatori sulla riva interna, e si apre verso la Spiaggia delle Conchiglie e la casa di Amo sul lato est.

## Aspetto / forma — geografia generale

**Geometria fisica della Bocca:**

- **Canale d'acqua** che attraversa la fascia costiera sud dell'isola, collegando il Fiume (interno) al mare aperto (esterno).
- **Larghezza** della Bocca: ~80-150 metri al massimo, con punto più stretto verso l'interno e più largo verso il mare.
- **Lunghezza** del canale: ~200-300 metri (dall'inizio del restringimento del Fiume fino al mare aperto).
- **Profondità** variabile: profonda al centro (abbastanza per la barca di Bartolo e altre imbarcazioni piccole), bassa sui lati.
- **Acque miste**: il Fiume porta acqua dolce, il mare entra a marea con acqua salata. Le due si mescolano visibilmente.

**Sponde della Bocca:**

- **Sponda interna nord** (lato terraferma del Fiume): bassa, sabbiosa-melmosa, con erba alta e canneti, dietro cui si vedono le Case Basse dei Pescatori.
- **Sponda ovest**: bassa, sabbiosa, dove parte il Pontile di Bartolo e termina la Via del Pontile dal villaggio.
- **Sponda est**: scogliera che sale dolcemente verso l'alto, dove sopra c'è la casa di Amo. Dalla scogliera est si vede tutta la Bocca dall'alto.
- **Apertura sud**: la Bocca si allarga verso il mare aperto, con due piccoli "promontori" naturali ai lati che la incorniciano. Il **Mar aperto** comincia oltre questi promontori.

**Elementi nella Bocca:**

- **Il Pontile di Bartolo**: dalla sponda ovest, si protende verso il centro della Bocca, lunghezza ~15m. Vedi `pontile_bocca/scheda.md`.
- **Il piccolo ponte di legno**: collega il lato est del Pontile alla Spiaggia delle Conchiglie, attraversando una piccola insenatura interna della Bocca.
- **Acqua sempre**: niente isole, niente scogli affioranti centrali (la Bocca è navigabile).
- **Eventuali piccole barche dei Pescatori**: ormeggiate sulla sponda nord davanti alle Case Basse.

**Posizione**:
- Centroide: `[4005, 900]` (cartografia).
- Confina a nord con la fine del Fiume sud, a sud con il mare aperto, a est con la Spiaggia delle Conchiglie e la scogliera Amo, a ovest con la sponda terrosa-sabbiosa dove si trova il Pontile.

## Espressione / comportamento (dinamica del luogo)

La Bocca è il **luogo di mescolanza** dell'isola — dove l'acqua del Fiume (lenta, dolce, di terra) incontra l'acqua del mare (salata, in movimento più ampio, di altrove). **Marea**: l'acqua sale e scende lentamente con la marea, modificando di poco il livello e la salinità.

**Vento Mulinello** soffia la sera (Bible §8.3) e ha effetti specifici sulla Bocca:
- Sposta le conchiglie sulla Spiaggia delle Conchiglie (canonico Bible).
- Fa cigolare i pali del Pontile.
- Crea piccole onde di superficie nella Bocca, raramente alte (è acqua relativamente protetta dai due promontori).

**Stati tipici:**

- **Mattino**: gabbiani sopra la Bocca, acqua piuttosto calma, riflessi forti del sole basso a est, sponde illuminate.
- **Mezzogiorno**: sole alto, acqua brillante, eventuali pescatori sulle Case Basse al lavoro, Bartolo nella barca o sul Pontile.
- **Pomeriggio**: ombre più lunghe, scogliera est in luce calda, acqua più calma.
- **Sera (Vento Mulinello)**: vento da sud che entra dalla Bocca, increspature visibili, Pontile cigolante, viola-arancione in cielo, conchiglie sulla Spiaggia spostate.
- **Notte**: scuro, qualche fioca luce dalle Case Basse e dalla capanna di Bartolo.

**Stagioni**:
- **Estate**: acqua più trasparente, conchiglie ben visibili sulla Spiaggia, sponde verdi.
- **Autunno**: vento più frequente, acqua leggermente più scura, Spiaggia con foglie portate dal vento.
- **Inverno**: pioggia, acqua agitata, sponde fangose, Spiaggia spesso vuota.
- **Primavera**: ritorno alla limpidezza, prime fioriture sulla scogliera est.

## Palette e atmosfera

**Quartiere d'Acqua a sud** (Bible §6): **verde mare antico, blu-grigio profondo, sabbia chiara, riflessi argentei**.

**Acqua nella Bocca (caratteristica unica):**
- **Verde-blu profondo** dove l'acqua è ancora del Fiume (più verso nord/interno)
- **Blu-grigio chiaro** dove l'acqua è del mare (più verso sud/aperto)
- **Argentato** nei punti di mescolanza, con riflessi della luce
- **Linee di colore visibili in superficie** dove le due acque si incontrano

**Sponde:**
- **Sabbia chiara** (sponda ovest, sponda nord interna)
- **Verde** dell'erba e canneti
- **Grigio-bruno chiaro** della scogliera est (pietra)
- **Verde scuro** della vegetazione bassa sulla scogliera est

**Cielo:**
- **Azzurro chiaro** (giorno limpido)
- **Viola-arancio** (sera Mulinello)
- **Grigio piombo** (giorni di pioggia, S8 stile)

**Tipo di luce**: **luce di acqua larga** — molta luce diffusa dalla superficie ampia, riflessi intensi al sole, ombre lunghe sull'acqua nei pomeriggi. La Bocca è uno dei luoghi più "luminosi" dell'isola di giorno.

**Atmosfera predominante**: **passaggio**. La Bocca è il luogo del **passaggio dell'acqua** dal dentro al fuori — e nella saga è anche metafora di "oltre il mare", la porta socchiusa di Fase F. Composta, fisica, mai sognante. Mai magica.

## Contesto e ambientazioni ricorrenti

Posizione: **Quartiere d'Acqua a sud**, fascia costiera sud dell'isola, foce del Fiume nel mare.

**Vicini diretti**:
- **Pontile di Bartolo**: dentro la Bocca, sponda ovest.
- **Case Basse dei Pescatori**: sponda interna nord, dietro il Pontile.
- **Spiaggia delle Conchiglie**: a est-sud-est, oltre la Bocca, sulla costa-mare.
- **Casa di Amo**: sulla scogliera est, sopra la Spiaggia.
- **Via del Pontile**: arriva dalla Bocca dal nord, terminando alla sponda ovest.
- **Mare aperto**: a sud, oltre i due promontori.

**Vento dominante**: **Vento Mulinello** (sera) — entra dalla Bocca da sud verso l'interno, sale lungo la Via del Pontile.

**Suoni canonici**:
- Acqua contro i pali del Pontile (continuo)
- Gabbiani al mattino
- Cigolio dei pali la sera col Mulinello
- Mai onde grandi che si infrangono (la Bocca è acqua relativamente calma)

**Odori canonici**:
- Sale e alga (Bible §8.3)
- A volte odore di pesce dalle Case Basse o dal Mercato che parte da qui

**Ruolo nelle storie:**
- **S7**: location della risoluzione (i fratelli arrivano camminando lungo il Fiume; la zattera entra nell'acqua mista della Bocca; **uscita finale al mare aperto**, "oltre il mare" implicito).
- **S10**: ricetto notturno per Bartolo (sul Pontile) — la Bocca come acqua scura sotto.
- **S11**: arrivo Bartolo da fuori (la barca attraversa la Bocca al ritorno).
- **S12**: cammeo cammino al passaggio del Pontile.

## Coerenza cross-scena (cose che NON cambiano)

- Posizione: foce del Fiume nel mare, quadrante sud
- Larghezza ~80-150 metri (varia secondo dove si misura)
- Acque miste (dolce + salata) sempre visibili
- Pontile di Bartolo dentro la Bocca, sponda ovest
- Scogliera est che sale verso casa di Amo
- Sponda nord interna sabbiosa-melmosa con canneti
- Apertura sud verso mare aperto incorniciata da due promontori
- Niente isole o scogli affioranti centrali

## Variabilità ammessa

- **Marea**: livello acqua varia di poco con la marea — le sponde possono essere più asciutte o più allagate.
- **Stato dell'acqua**: calma (default) o leggermente increspata (sera Mulinello). Mai onde grandi.
- **Presenza di barche/imbarcazioni**: barca di Bartolo presente o assente; eventuali piccole barche di pescatori sulla sponda nord; mai più di 3-4 barche totali.
- **Conchiglie/relitti naturali**: conchiglie maggiormente sulla Spiaggia delle Conchiglie, ma occasionalmente piccoli detriti di mare nelle sponde della Bocca.
- **Stagione e ora**: vedi sezione precedente.

**Mai variabile:**
- Posizione della Bocca
- Geometria del canale (forma a "imbuto" verso il mare)
- Acque miste sempre presenti

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

**Specifici per la Bocca:**
- Mai foce "drammatica con onde alte e schiuma" — è acqua mista relativamente calma.
- Mai foce "tropicale" con acque turchesi cristalline.
- Mai foce "atlantica fredda" con scogli neri e cielo grigio sempre.
- Mai foce "fantasy" con luce magica, vortici, archi rocciosi che richiamano portali.
- Mai foce "industriale" con strutture moderne sullo sfondo.
- Mai delfini che saltano, balene, animali esotici di passaggio.
- Mai effetti di luce magica sull'acqua mista.
- Mai schiuma drammatica al confine acqua dolce/salata.
- Mai tramonto da poster con sole gigantesco all'orizzonte.
- Mai uccelli marini in formazioni decorative.

---

## ⭐ Descrizione visiva canonica per generazione — ESTERNO

⚠️ **BLOCCO LOCATION ESTERNO** da incollare nei prompt Grok per scene che mostrano La Bocca nella sua interezza (vista d'insieme, traversate, panorami, S7 zattera che esce nel mare).

**Per scene focalizzate sul Pontile**, usare il blocco LOCATION del Pontile (`pontile_bocca/scheda.md`).
**Per scene focalizzate sulla Spiaggia**, usare il blocco LOCATION della Spiaggia (`spiaggia_conchiglie/scheda.md`).

```
LOCATION (EXTERIOR — RIVER MOUTH) — La Bocca:
A wide river mouth on the southern coast of an island, where the river 
meets the open sea. This is "La Bocca" (the Mouth) — the channel where 
fresh and salt water mix, creating visible color differences in the 
surface water.

GEOMETRY:
The mouth is approximately 80-150 meters wide at its widest point and 
extends about 200-300 meters from where the river narrows to where it 
opens fully to the sea. Two small natural rocky promontories frame the 
southern opening to the sea, like rough natural pillars marking the 
threshold. The water is deep enough at the center for small boats, 
shallower at the edges.

WATER (the visual signature):
The surface shows MIXED WATER — clear color differences are visible:
- DEEPER GREENISH-BLUE in the inner part (river water, freshwater)
- PALER SILVER-BLUE toward the open sea (saltwater)
- Visible LINES OF COLOR DIFFERENCE where the two waters meet, 
  creating gentle swirling patterns on the surface. Not magical 
  sparkles — physical color contrast.
The water moves slowly with mild currents, generally calm. In the 
evening with the Mulinello wind, light ripples appear on the surface 
moving from the open sea inward.

SHORES:
- WEST SHORE: low, sandy-muddy with patches of grass, where the 
  Pontile (pier) extends from. The Via del Pontile (path) ends here, 
  meeting the sand. The wooden pier with its small thatched-roof hut 
  at the far end is the most distinctive feature on this side.
- NORTH INNER SHORE (behind the pier): low, sandy with reeds and 
  high grass, behind which the rooftops of the Case Basse (Low 
  Houses) of the Fishermen are visible.
- EAST SHORE: a gradual rocky cliff rising from the water, with 
  scattered low vegetation. Near the top of the cliff, a small wooden 
  house carved into the rock — Amo's house. A small stone staircase 
  descends from the house to the water.
- SOUTH OPENING: opens to the OPEN SEA between the two natural 
  rocky promontories. The horizon extends beyond.

ELEMENTS IN/ON THE WATER:
- The Pontile (wooden pier) extending from the west shore, about 15 
  meters out, ending in Bartolo's hut.
- A small wooden footbridge from the east side of the pier, crossing 
  a small inner inlet, leading to the Shell Beach (Spiaggia delle 
  Conchiglie).
- Possibly Bartolo's small rowboat moored at the pier or rowing in 
  the channel.
- Possibly 1-2 small fisherman boats moored along the north shore.
- Seagulls flying or floating on the water.

ATMOSPHERE: physical, salty, transitional. The Bocca is a real river 
mouth, not a magical portal — but it carries weight as the place where 
the inner world (the island) meets the outer (the open sea).

LIGHTING (depending on scene):
- Morning: low east light from over the cliff, water surface bright 
  with reflections, gulls in flight, golden tones on the west shore 
  and pier.
- Day: full overhead sun, water bright with reflections, distinct 
  color difference between river and sea waters most visible.
- Evening (Vento Mulinello): violet-orange sky, light ripples on 
  the water, the pier silhouetted, posts creaking (sound implied), 
  warm tones on east cliff.
- Night: dark water, faint light from windows of Case Basse and 
  Bartolo's hut.

Color palette: deep greenish-blue (inner mixed water), pale silver-
blue (outer mixed water), sandy-cream (west and north shores), 
gray-brown (east cliff), green (vegetation), dark wood (pier and 
boats), white-gray (gulls), violet-orange or pale blue (sky).

NO crashing waves, NO foam at color boundary, NO tropical turquoise, 
NO magical sparkles, NO leaping fish, NO dramatic seabird formations, 
NO dramatic sunset poster.
```

---

## Per stampa 3D / modello

Modello 3D della Bocca (con sponde, Pontile, ponte di legno, scogliera est) utile per:
- Diorama di scene larghe (S7 zattera che esce verso il mare)
- Modello mondo macro

Indicazioni qualitative:
- Scala: in scala 1:24 o 1:48 per modello mondo. Includere base in resina trasparente o pittura per simulare l'acqua mista (gradient verde-blu → argento).
- Pezzi separabili: Pontile + capanna come pezzo, scogliera est con casa Amo come pezzo, sponda nord con Case Basse come pezzo.
- Punti critici: la transizione cromatica dell'acqua mista, le linee di mescolanza, le piccole onde di superficie nel Mulinello.

_Da fissare quando la scala canonica saga sarà decisa._

## Per narrativa e social

Vedere `descrizione_narrativa_social.md` nella stessa cartella.

**Registri d'uso testuale:**
- Voce narrante: "La Bocca" (sempre con maiuscola, è un nome proprio).
- Mai "la foce" / "l'imbocco" / "l'estuario" da soli — La Bocca è il nome canonico.
- Mai descrizioni nuove fuori canone.
- L'**acqua mista** è elemento canonico, può essere richiamata in narrativa.
- Mai aggettivi morali ("sacra", "magica", "antica", "saggia").

## Storie / scene di apparizione

- s01: assente.
- s02: assente.
- s03: assente.
- s04: assente.
- s05: assente.
- s06: assente.
- s07: location risoluzione (zattera entra nell'acqua mista, esce nel mare aperto).
- s08: assente.
- s09: assente.
- s10: cammeo (acqua scura intorno al Pontile di notte).
- s11: cammeo arrivo Bartolo da fuori (attraversa la Bocca al ritorno).
- s12: cammeo passaggio Pontile.

## Disallineamenti / domande aperte

- **Larghezza esatta della Bocca**: ~80-150 metri stimati. La cartografia ha solo un Point per la Bocca, non un Polygon. Da validare quando la cartografia avrà geometria precisa.
- **Promontori sud**: derivazione autoriale ("incorniciano l'apertura sud"). La Bible non li menziona esplicitamente. Da confermare con Ray.
- **Esistenza di canneti sulla sponda nord**: derivazione autoriale (tipico di river mouth). Bible non lo dice.
- **Eventuale piccola lingua di sabbia centrale**: alcune foci hanno una lingua di sabbia o un banco. Non incluso. Coerente con "Pontile dentro La Bocca, navigabile". Da confermare se Ray vuole un banco di sabbia.

## Riferimenti puntuali (citazioni dirette dalle fonti)

**Fonti canoniche dirette:**
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8 (cosmogonia): "A sud, La Bocca — un canale largo abbastanza per le barche, dove il Fiume sfocia nel mare e dove le acque dolci e salate si mescolano. Dentro La Bocca, sull'acqua mista, sta il Pontile di Bartolo. Qui le barche entrano e escono verso il mare aperto."
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §6 PALETTE VISIVA: "Quartiere d'Acqua (Sud): verde mare antico, blu-grigio profondo, sabbia chiara, riflessi argentei."
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8.3 Quartiere d'Acqua: "Pontile di Bartolo dentro La Bocca... Vento Mulinello la sera sposta le conchiglie sulla Spiaggia, fa cigolare i pali del Pontile. Odore: sale e alga. Suono: acqua contro i pali, gabbiani al mattino."
- `architettura/ARCHI_12_STORIE_v1__1_.md` S7: "Camminano fino alla Bocca... Vede la zattera arrivare nell'acqua mista della Bocca... I fratelli restano a guardare la zattera che oscilla nell'acqua mista, finché non esce nel mare aperto."
- `worldbuilding/GLOSSARIO_ISOLA.md` §2.4 Quartiere d'Acqua: "La Spiaggia delle Conchiglie — sulla costa-mare oltre La Bocca, raggiungibile dal piccolo ponte di legno dietro al Pontile. Le Case Basse dei Pescatori — sulla riva interna della Bocca, dietro il Pontile."
- `pipeline_narrativa/story_graph.json#entities.locations.bocca`
- `cartografia/geo/island.geojson#features.id=bocca`: river_mouth, quarter=acqua, geometry=Point, centroid_m_local: [4005, 900].

**Derivazioni autoriali:**
- *Larghezza ~80-150m, lunghezza canale ~200-300m*: derivata dimensioni isola (~8 km × ~7 km, fascia costiera 500-800m) + funzionalità canale navigabile.
- *Due promontori che incorniciano l'apertura sud*: derivazione autoriale geografica (tipico di river mouth, dà identità al passaggio mare/Fiume).
- *Sponda nord con canneti*: derivazione tipologica (foci con sponda interna spesso hanno vegetazione palustre).
- *Linee di colore visibili dell'acqua mista*: derivazione fisica (le due acque hanno densità diverse, si mescolano lentamente, il confine è visibile).
- *Niente isole/scogli centrali*: derivata da "navigabile per barche" + Pontile esistente.
- *Profondità variabile (centro più profondo, sponde basse)*: derivazione tipologica.

**Cliché da evitare specifici visivi**: derivati da `PATTERN_AI_DA_BANDIRE_v1.md` applicato al caso river-mouth-mediterraneo.
