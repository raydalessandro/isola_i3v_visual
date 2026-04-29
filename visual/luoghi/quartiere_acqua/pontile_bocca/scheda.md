---
id: pontile_bocca
name: Pontile di Bartolo
famiglia: luogo
sottotipo: pier
quartiere: acqua
status: provvisorio
ultima_modifica: 2026-04-29
fonti: ["pipeline_narrativa/story_graph.json#entities.locations.pontile_bocca", "cartografia/geo/island.geojson#features.id=pontile_bocca"]
appare_in_storie: []
ha_interno: true
ha_esterno: true
ha_cortile_o_annessi: true
cartografia:
  feature_id: pontile_bocca
  type_geo: pier
  status_geo: canonico
  quarter: acqua
  category: null
  centroid_m_local: [4015, 925]
  bbox_m_local: [4015, 850, 4015, 1000]
  size_m_local: [0, 150]
  altitudine_m: null
  geometry_type: LineString
  parent_geo: null
  children_geo: []
  aliases_geo: []
---


# Pontile di Bartolo

> **Stato compilazione:** body provvisorio, completato 2026-04-29 con derivazione autoriale dalle fonti canoniche (Bible §4.3, §6, §8.1, §8.3; ARCHI_12_STORIE §S7, §S10, §S11, §S12; grafo entities.locations.pontile_bocca; Glossario §2.4; cartografia island.geojson). Le sezioni in derivazione sono dichiarate in "Riferimenti puntuali".
>
> **⚠️ STRATEGIA LUOGHI:** questo luogo NON ha immagine di reference per scene multi-personaggio. I 3 blocchi LOCATION testuali (esterno / interno / annessi) sono il riferimento per i prompt scena.
>
> **⚠️ LUOGO CON ESTERNO + INTERNO + ANNESSI:** il Pontile è una struttura complessa che include il pontile di assi sull'acqua (esterno), la capanna di Bartolo "in cima al Pontile" (interno), e annessi (la barca di Bartolo + il piccolo ponte di legno verso la Spiaggia delle Conchiglie). Mai più di un blocco per scena.

## Identità visuale (sintesi)

**Tipo:** edificio (pontile + capanna integrata sull'acqua).
**Quadrante:** acqua_sud.
**Abitante:** bartolo.
**Ruolo saga:** dimora canonica di Bartolo, snodo del Quartiere d'Acqua, **architrave di "oltre il mare"** (porta socchiusa Fase F).

Il Pontile è una struttura di legno che si protende dentro **La Bocca** — il punto in cui il Fiume sfocia nel mare e le acque dolci e salate si mescolano. Pali piantati nell'acqua mista, assi scure consumate dal sale, un camminamento di circa 15 metri sopra l'acqua. **In cima al Pontile**, sull'estremità verso il mare aperto, sta la **capanna di Bartolo** — bassa, col tetto di canne, dimora del traghettatore. **Dietro al Pontile**, sulla riva interna della Bocca, parte un piccolo ponte di legno che porta alla Spiaggia delle Conchiglie. La barca di Bartolo è quasi sempre ormeggiata al Pontile; quando Bartolo è in viaggio, è in mare aperto.

## Aspetto / forma — geografia generale

**Struttura del Pontile**:

- Camminamento di legno costituito da **assi scure** consumate dal sale e dal sole. Le assi sono inchiodate trasversalmente su travi longitudinali, un po' irregolari per età, con qualche fessura tra un asse e l'altro da cui si vede l'acqua sotto.
- **Pali piantati nell'acqua**, di legno scuro tendente al nero per anni di immersione, leggermente inclinati nei punti dove le correnti li spingono. I pali emergono dall'acqua di 30-50 cm e portano il piano del pontile.
- **Lunghezza**: circa 15 metri (stima da bbox cartografica `size_m_local: [0, 150]` ridotta — è LineString, lo interpreto come ~15m perché il geojson è in scala 1:10 sul valore Y).
- **Larghezza**: ~2 metri, abbastanza per due abitanti che si incrociano o per il passaggio di un cesto.
- **Direzione**: il pontile parte dalla riva nord interna della Bocca (lato terraferma) e si protende verso sud, dentro la Bocca, verso il mare aperto. Non arriva al mare aperto vero e proprio — finisce dove l'acqua è già abbastanza profonda per la barca di Bartolo.

**Capanna di Bartolo**:

- In cima al Pontile (estremità sud, verso il mare).
- **Capanna bassa, col tetto di canne** (Bible §4.3, Glossario §2.4) — copertura di canne legate insieme, leggermente disordinate ma fitte abbastanza da reggere la pioggia.
- Pianta circolare o ottagonale piccola (~3 metri di diametro), una sola stanza.
- Costruzione di assi di legno chiaro-scuro (più chiaro delle assi del pontile, perché meno esposto direttamente all'acqua), montate verticalmente.
- Una porta semplice di legno (apertura verso il pontile, lato nord) e **una piccola finestra orientata a sud** (verso il mare aperto) — Bartolo guarda il mare da dentro casa.
- L'altezza al colmo è intorno a 2 metri — bisogna chinarsi un attimo per entrare. Bartolo, con il guscio, ci sta dentro comodamente perché è basso.
- Il tetto di canne sporge un po' oltre le pareti, fa un piccolo riparo sotto il quale Bartolo a volte si siede su uno sgabello a guardare il mare.

**Annessi**:

1. **Barca di Bartolo**: ormeggiata al Pontile, lato est della struttura. Una piccola barca da pesca/traghetto, di legno scuro come il Pontile, con due remi semplici, una panca centrale, niente vela (Bartolo rema). Lunga ~3 metri. Quando Bartolo è in viaggio è in mare; quando è ormeggiata, è legata con una cima a un palo del Pontile (nodo Marinaro, opera di Nodo).
2. **Piccolo ponte di legno verso la Spiaggia delle Conchiglie**: parte dalla riva nord-est del Pontile, attraversa una piccola insenatura interna, e arriva alla Spiaggia delle Conchiglie sulla costa-mare oltre la Bocca. Lunghezza ~10-15 metri. Più semplice del Pontile, una sola passerella con una corda-corrimano da un lato.

**Posizione**:
- **Quartiere d'Acqua a sud**, dentro **La Bocca** (centroide cartografico `[4015, 925]`).
- 40 minuti di cammino dalla Piazza del Villaggio centrale, lungo la **Via del Pontile**.

## Espressione / comportamento (dinamica del luogo)

Il Pontile è un luogo di **acqua e silenzio**. **Vento Mulinello** soffia la sera, sposta le conchiglie sulla Spiaggia e **fa cigolare i pali del Pontile** (Bible §8.3 — il cigolio è suono-firma del Pontile alla sera). Di giorno l'acqua picchia piano contro i pali, costantemente. I gabbiani gridano al mattino. Le acque dolce e salata si mescolano sotto il pontile creando linee visibili di colore diverso (l'acqua dolce è più scura, la salata più chiara con riflessi argentati).

**Stati tipici della giornata:**

- **Mattino**: sole basso a est che illumina il Pontile dal lato della Spiaggia, gabbiani attivi, Bartolo seduto sotto il riparo della capanna o nella barca. Acqua più calma.
- **Mezzogiorno**: sole alto, riflessi forti sull'acqua, Pontile spesso vuoto (Bartolo in viaggio o nella capanna), pochi pescatori che passano per ritirare attrezzi.
- **Pomeriggio**: luce calda, ombra lunga del Pontile sull'acqua, eventuale arrivo o partenza della barca.
- **Sera**: **Vento Mulinello** si alza, **i pali del Pontile cigolano**, conchiglie sulla Spiaggia spostate dal vento. Suono molto evocativo, presente in tutte le scene serali del Pontile.
- **Notte**: scuro, capanna con eventuale luce di candela visibile dalla finestra a sud (rara — Bartolo dorme presto). **In S10 il Pontile è ricetto notturno** (canonico).

**Stagioni**:
- **Primavera/estate**: legno secco, conchiglie più visibili, acqua più trasparente.
- **Autunno** (S11, S12): vento più forte, pali più cigolanti, prima brina mai sul Pontile (sempre umido).
- **Inverno**: pioggia frequente, assi scivolose, capanna chiusa più spesso, fumo da un piccolo camino interno (Bartolo accende un piccolo fuoco — solo invernale).

## Palette e atmosfera

**Quartiere d'Acqua a sud** (Bible §6): **verde mare antico, blu-grigio profondo, sabbia chiara, riflessi argentei**.

**Esterno (Pontile su acqua)**:
- **Marrone-nero** delle assi scure consumate dal sale
- **Nero scuro** dei pali immersi
- **Verde-blu profondo** dell'acqua dolce del Fiume
- **Blu-grigio chiaro** dell'acqua salata mista
- **Argentato** dei riflessi della luce sull'acqua mista
- Verde scuro delle alghe sui pali sotto la linea dell'acqua
- **Bianco-grigio** dei gabbiani
- Cielo: blu chiaro / azzurro tenue (giorno) o viola-arancio (sera Mulinello)

**Interno (capanna di Bartolo)**:
- **Marrone caldo** del legno delle pareti (più chiaro dell'esterno)
- **Beige-paglia** del tetto di canne dall'interno (intreccio visibile)
- Sfumature **verdi** date dalla luce filtrata dalla finestra a sud (l'acqua riflette verde)
- Toni **caldi** soffusi del legno e degli oggetti di Bartolo
- Niente colori vivaci

**Annessi**:
- **Barca**: marrone-nero scuro come il Pontile, panca leggermente più chiara
- **Ponte di legno verso Spiaggia**: marrone più chiaro (legno più nuovo), corda chiara di canapa

**Tipo di luce**: **luce di acqua** — molta luce riflessa dall'acqua sotto, sempre presente ma diffusa; ombre meno nette che a terra. Sera con Vento Mulinello: viola-arancio epico (canonico, nelle scene serali del Quartiere d'Acqua). Mai luce verdastra/aliena.

**Atmosfera predominante**: **dilatazione del tempo** (il Pontile è il luogo di Bartolo, dove il tempo si distende). Composta, salina, lenta. Mai drammatica. Mai magica.

## Contesto e ambientazioni ricorrenti

Posizione: **Quartiere d'Acqua a sud, dentro La Bocca** (il punto dove il Fiume sfocia nel mare). 40 minuti dal Villaggio lungo la Via del Pontile.

**Vicini**:
- **La Bocca** (river_mouth): è il "contenitore" del Pontile — l'acqua del Pontile è La Bocca.
- **Spiaggia delle Conchiglie**: a est-sud-est, raggiungibile dal piccolo ponte di legno.
- **Casa di Amo**: a est, sulla scogliera che sovrasta la Spiaggia, visibile in lontananza dal Pontile.
- **Case Basse dei Pescatori**: a nord, dietro il Pontile sulla riva interna della Bocca.
- **Mare aperto**: a sud, oltre il Pontile.

**Vento dominante**: **Vento Mulinello** (sera) — sposta conchiglie sulla Spiaggia, fa cigolare i pali del Pontile (Bible §8.3). Suono-firma del luogo.

**Suoni canonici** (Bible §8.3):
- Acqua contro i pali (continuo, di giorno)
- Gabbiani al mattino
- Cigolio dei pali la sera col Vento Mulinello

**Odori canonici** (Bible §8.3):
- Sale e alga

**Ruolo nelle storie**:
- **S7 risoluzione**: Bartolo "semi-disteso nella barca", la zattera dei fratelli arriva nell'acqua mista, Bartolo non la raccoglie, Toba (cucciola) sul Pontile chiede "E poi?" (canonico).
- **S10**: ricetto notturno, Bartolo presenza silenziosa zero parole.
- **S11**: cammeo, arrivo Pontile con frutti da fuori, sera (Bartolo torna da oltre-il-mare).
- **S12**: cammeo Pontile mattino, "mano alzata che ricade"; nel sigillo finale: presenza nella barca implicita, mai mostrata.

## Coerenza cross-scena (cose che NON cambiano)

**Esterno (Pontile su acqua):**
- Pontile di assi scure consumate dal sale, pali piantati nell'acqua
- Lunghezza ~15 metri, larghezza ~2 metri, direzione nord (riva) → sud (mare)
- Pali emergono ~30-50 cm sopra l'acqua, color nero-scuro per immersione
- Acqua mista (dolce + salata) sotto il pontile
- Capanna di Bartolo all'estremità sud
- Posizione dentro La Bocca

**Interno (capanna di Bartolo):**
- Capanna bassa col **tetto di canne** (canonico Bible)
- Pianta piccola (~3 metri diametro), una sola stanza
- Una porta semplice (lato nord, verso il pontile)
- Una piccola finestra (lato sud, verso il mare)
- Mobili semplici: uno sgabello di legno, un giaciglio basso (Bartolo "dorme nella barca quando fa caldo" — Bible §4.3 — quindi nella capanna dorme col freddo)
- Una piccola dispensa per cibo conservato
- Forse una piccola stufa-camino di pietra per il fuoco invernale (derivazione)
- **Niente lusso, niente decorazioni**: è una capanna di un traghettatore anziano che vive sull'acqua

**Annessi:**
- Barca di Bartolo ormeggiata al Pontile (lato est), piccola, di legno scuro, due remi
- Piccolo ponte di legno verso la Spiaggia (lato nord-est della struttura), ~10-15 metri, con corda-corrimano

## Variabilità ammessa

**Stagione:**
- **Primavera/estate**: pontile asciutto al sole, conchiglie sulla riva, acqua più trasparente, capanna con porta aperta nelle ore calde, Bartolo che dorme nella barca.
- **Autunno** (S11, S12): vento più forte, pali più cigolanti, capanna chiusa di sera, leggera nebbiolina sull'acqua al mattino.
- **Inverno**: pioggia frequente, capanna sempre chiusa, Bartolo dentro al riparo, acqua più scura grigia.

**Ora del giorno:**
- **Mattino**: gabbiani, sole basso a est, riflessi forti.
- **Giorno**: luce piena, riflessi alti.
- **Sera**: Vento Mulinello, cigolio dei pali, viola-arancio del cielo.
- **Notte** (S10): scuro, eventuale fioca luce dalla finestra a sud della capanna.

**Stato della barca**: **ormeggiata al Pontile** (default — Bartolo è in casa o sul Pontile) o **assente** (Bartolo è in viaggio).

**Stato di Bartolo (per coerenza scene)**: Bartolo può essere visibile **sul Pontile in piedi**, **seduto sotto il riparo della capanna**, **semi-disteso nella barca** (canonico S7), **dentro la capanna** (sera/notte/freddo), oppure **assente** (in viaggio in mare aperto).

**Mai variabile:**
- Posizione del Pontile dentro La Bocca
- Direzione del Pontile (nord-sud)
- Capanna in cima al Pontile, lato sud
- Tetto di canne della capanna
- Lunghezza/larghezza del Pontile

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

**Specifici per il Pontile:**
- Mai pontile "di un porto turistico" con tante barche colorate, ringhiere decorate.
- Mai pontile "fantasy" con lanterne accese ovunque, vele decorate, pirati.
- Mai pontile "di pescatori italiani" con reti stese ovunque a seccare in modo pittoresco.
- Mai pontile "decadente romantico" con pali rotti, assi spaccate in modo drammatico.
- Mai capanna "abbandonata" — è la casa di Bartolo, ben tenuta nella sua semplicità.
- Mai capanna "dei sette nani" / "stile fantasy" / "tetto di paglia idilliaco".
- Mai effetti di luce magica sull'acqua, sparkle, riflessi soprannaturali.
- Mai gabbiani "in formazione drammatica" o uccelli marini esotici.
- Mai onde grandi tipo costa atlantica — La Bocca è acqua mista relativamente calma.
- Mai pesci visibili che saltano in modo decorativo.
- Mai conchiglie "perfettamente disposte" da decoratore.
- Mai barche "rustiche da cartolina mediterranea" decorate, con nomi dipinti.
- Mai pontile come "luogo di malinconia romantica" con figura solitaria al tramonto in posa.

---

## ⭐ Descrizione visiva canonica per generazione — ESTERNO (Pontile su acqua)

⚠️ **BLOCCO LOCATION ESTERNO** da incollare nei prompt Grok delle scene ambientate **sul Pontile** (camminamento, arrivo della barca, vista d'insieme, scene di Bartolo seduto sul Pontile, scene S7/S11/S12 sulle assi).

```
LOCATION (EXTERIOR — PIER) — Pontile di Bartolo:
A wooden pier extending into a river mouth where freshwater meets the sea, 
in the Southern Quarter (Quartiere d'Acqua) of an island. The pier is part 
of "La Bocca" (the Mouth), the channel where the river finally meets the 
open sea.

The pier is made of dark, salt-weathered wooden planks, laid crosswise 
on longitudinal beams, with visible gaps between some planks where water 
glints below. Length approximately 15 meters, width 2 meters. The 
direction runs north-south: it starts from the inner shore (north) and 
extends outward toward the open sea (south). Wooden posts driven into 
the water support the pier — these posts are very dark, almost black, 
from years of immersion in salt water. They rise about 30-50 cm above 
the water surface and lean slightly where currents push them. The pier 
does not have side railings — just the open planks above the water.

At the FAR END of the pier (south, toward the sea), there is a small 
LOW HUT — Bartolo's dwelling. The hut has a thatched cane roof (woven 
reeds, slightly disheveled but tightly bound), walls of vertical wooden 
planks (a lighter brown than the pier itself), one simple wooden door 
facing north (toward the pier), and a small window facing south (toward 
the open sea). The hut is round or octagonal, about 3 meters across, 
the roof rising to about 2 meters at the peak. The roof overhangs the 
walls slightly, creating a small sheltered area where one might sit on 
a wooden stool.

A SMALL BOAT is moored to the east side of the pier — a simple rowing 
boat about 3 meters long, dark wood like the pier, with two simple oars 
and a central plank seat. No sail. Tied to a post with a hemp rope.

The water under and around the pier is "MIXED WATER" — fresh river 
water meets salt sea water here, creating visible color differences: 
the freshwater is a deeper greenish-blue, the saltwater is paler and 
more silver-reflective. Lines of color difference can be seen on the 
surface where the two waters mix. Under the water line, the posts have 
dark green algae growing on them.

To the NORTH (toward shore), the riverbank with low grass, sandy mud, 
and beyond it: the houses of the fishermen (Case Basse) glimpsed in 
the distance.
To the EAST, a small wooden footbridge (about 10-15 meters long) leads 
across a small inner inlet toward the Shell Beach (Spiaggia delle 
Conchiglie) — this footbridge is simpler than the pier, a single 
walkway with one rope handrail.
To the SOUTH, beyond the hut, the open sea with the horizon in the 
distance.
To the EAST, on the cliff above the shell beach, the silhouette of 
Amo's house (legno scavato sulla scogliera) can be glimpsed in the 
distance.

SOUNDS (implied visually): water lapping against the posts continuously, 
seagulls in the morning, the creaking of the posts in the evening when 
the Mulinello wind blows.

LIGHTING (default — adjust for scene):
- Morning: low east light, strong reflections on the water, seagulls 
  in flight, golden tones on the planks.
- Day: full overhead light, bright reflections, neutral warm tones.
- Evening (Vento Mulinello): violet-orange sky, posts creaking, 
  reflections deepening, Bartolo's silhouette possibly visible against 
  the hut.
- Night: dark, faint candle light from the south window of the hut.

Color palette: dark brown-black (pier planks and posts), greenish-blue 
(river water), pale silver-blue (sea water), warm light brown (hut 
walls), beige-straw (cane roof), white-gray (gulls), green (algae on 
underwater posts), violet-orange or pale blue (sky depending on time).

NO decorative lanterns, NO multiple colorful boats, NO drying nets 
arranged picturesquely, NO romantic decay, NO fantasy elements, NO 
sparkles on water, NO leaping fish.
```

---

## ⭐ Descrizione visiva canonica per generazione — INTERNO (capanna di Bartolo)

⚠️ **BLOCCO LOCATION INTERNO** da incollare nei prompt Grok delle scene ambientate **dentro la capanna di Bartolo**. Scene rare ma possibili (Bartolo in casa di sera, Bartolo che riposa, eventuali cammei interni).

```
LOCATION (INTERIOR — HUT) — Capanna di Bartolo on Pontile:
The interior of a small low fisherman's hut, situated at the end of a 
wooden pier on the water. The room is a single small space, round or 
octagonal in shape, about 3 meters across, with a low ceiling rising 
to about 2 meters at the central peak.

WALLS: vertical wooden planks of warm light brown wood, weathered but 
solid. The wood shows visible grain and the narrow gaps between planks 
let in slivers of light from outside. The walls curve slightly inward 
toward the roof.

ROOF (visible from inside): the underside of a thatched cane ceiling — 
woven reeds bound together in tight bundles, light beige-straw color, 
showing the texture of the weaving. Some support beams of dark wood 
visible underneath.

FLOOR: rough wooden planks, slightly worn, perhaps a small woven mat 
near the door.

SPATIAL LAYOUT:
- The DOOR is on the north wall (facing the pier), a simple wooden 
  plank door with iron hinges.
- The WINDOW is on the south wall (facing the open sea), a small 
  square opening with shutters that can close, no glass — open during 
  the day. Through the window, glimpse of the sea and sky.
- A LOW WOODEN STOOL or two stools, simple, rough-hewn.
- A LOW SLEEPING PLATFORM along the east curved wall, with a thin 
  woven blanket and a folded sailcloth as cover. Bartolo sleeps here 
  in cold weather (in summer he sleeps in the boat).
- A SIMPLE WOODEN CHEST against the west curved wall, where Bartolo 
  keeps his few belongings.
- A SMALL STONE HEARTH in the center or on the floor near a wall, 
  with a small chimney going up through the cane roof — used only in 
  winter for a small fire.
- A FEW HOOKS on the walls holding: a worn cloak, a fishing rod, a 
  spare oar, a coil of rope.
- ON A SHELF or in the chest: a few clay bottles (water, possibly 
  fermented something), a few dried fish hanging, simple wooden bowls 
  and cups, a small bag of salt.

ATMOSPHERE: the smell of salt and old wood implied. The light is 
diffused — some from the small south window, some filtering through 
the gaps in the cane roof and wall planks, creating a soft mottled 
light. Quiet — even more than outside, because the hut absorbs the 
sounds.

LIGHTING (depending on scene):
- Day: soft mottled light from the gaps and the south window.
- Evening: dim, perhaps one small candle.
- Night: very dim, a single candle on the chest or near the bed.
- Winter: small fire glow from the hearth.

Color palette: warm light brown (walls), darker brown (beams, chest, 
furniture), beige-straw (cane ceiling), pale gray-blue (light from 
window), soft warm shadow, perhaps pale ember-orange (winter fire).

NO decorative items, NO abundance, NO luxury, NO modern elements, NO 
fishing trophies, NO maps on walls, NO writing. The hut is the dwelling 
of an old turtle who lives simply on the water.
```

---

## ⭐ Descrizione visiva canonica per generazione — ANNESSI (barca + ponte di legno)

⚠️ **BLOCCO LOCATION ANNESSI** per scene specifiche: focus sulla barca di Bartolo (es. S7 "Bartolo semi-disteso nella barca") o sul piccolo ponte di legno verso la Spiaggia (transizione tra Pontile e Spiaggia).

```
LOCATION (ANNEX — BOAT or FOOTBRIDGE) — Pontile di Bartolo:

[OPTION A — Bartolo's BOAT moored at the pier]
A small simple rowing boat moored to the east side of a wooden pier, 
in calm mixed water (fresh meets salt). The boat is about 3 meters 
long, made of dark weathered wood (similar tone to the pier planks), 
with a single central plank seat and two simple oars resting on the 
seat or in their oarlocks. The boat is rounded at both ends, low 
profile, no sail, no decorations. A coil of hemp rope ties the boat 
to a dark post of the pier with a marine knot. Inside the boat, a 
worn folded sailcloth (used as a blanket or cushion), perhaps a small 
clay bottle of water, a wooden bucket. The boat rocks gently on the 
mixed water. Algae and sea growth visible on the lower hull near the 
waterline.

[OPTION B — small WOODEN FOOTBRIDGE to Shell Beach]
A simple wooden footbridge crossing a small inner inlet, connecting 
the rear of the pier (north-east side) to the Shell Beach 
(Spiaggia delle Conchiglie) on the open sea coast. The footbridge is 
about 10-15 meters long, made of weathered wooden planks placed on 
two longitudinal beams supported by short posts driven into the 
shallow water below. There is one ROPE HANDRAIL of pale hemp rope on 
ONE SIDE only (the seaward side), tied to thin wooden uprights spaced 
along the bridge. The footbridge is older than the pier — the wood 
is paler from less salt exposure, perhaps with some grass growing 
from the cracks where it nears the shore. At the end of the footbridge 
on the beach side, the wooden planks meet packed sand and small shells 
scattered around.

ATMOSPHERE: utilitarian, practical, quietly functional. Not 
picturesque, not romantic.

Color palette: dark brown-black (boat, pier posts), pale weathered wood 
(footbridge), pale hemp (rope), greenish-blue and silver (water), 
sandy-cream (beach end), green (algae).

NO decorative carvings, NO painted names on boat, NO multiple boats, 
NO drying nets, NO fishing equipment scattered for picturesque effect.
```

---

### ✏️ Note d'uso operative

**Mappa scene → blocco LOCATION da usare:**

| Scena | Blocco LOCATION |
|---|---|
| S7 risoluzione: Bartolo nella barca, zattera dei fratelli, Toba sul Pontile | ESTERNO (vista d'insieme) o ANNESSI option A (focus barca) |
| S10 ricetto notturno | ESTERNO (notte) o INTERNO (se dentro la capanna) |
| S11 cammeo: Bartolo arriva al Pontile con frutti da fuori | ESTERNO |
| S12 mattino: cammeo Bartolo "mano alzata che ricade" | ESTERNO |
| S12 sigillo: presenza nella barca implicita, mai mostrata | NESSUNO (off-screen) |
| Eventuale scena dentro la capanna | INTERNO |
| Transizione Pontile ↔ Spiaggia | ANNESSI option B |

**Mai mischiare blocchi.** Se la scena è "Bartolo esce dalla capanna sul Pontile" → ESTERNO con cenno alla porta della capanna sullo sfondo.

## Per stampa 3D / modello

Modello 3D del Pontile + capanna utile per:
- Diorama scene (S7 zattera, S10 notte)
- Modello mondo per stampa libro

Indicazioni qualitative:
- Scala: coerente con personaggi. Se Bartolo = ~30 cm in scala toy 1:6 (1.05 GU), il Pontile misura ~2.5 m in scala (15 m reali / 6).
- Pezzi separabili: capanna con tetto di canne rimovibile per vedere l'interno; barca rimovibile dal Pontile.
- Materiali: PLA o resina con post-stampa per texture legno e acqua. Base in resina trasparente per simulare l'acqua mista.
- Punti critici: il tetto di canne (texture), i pali sotto il pontile (geometria), l'acqua mista trasparente.

_Da fissare quando la scala canonica saga sarà decisa._

## Per narrativa e social

Vedere `descrizione_narrativa_social.md` nella stessa cartella.

**Registri d'uso testuale:**
- Voce narrante: "il Pontile", "il Pontile di Bartolo", "la capanna" (riferendosi a quella di Bartolo).
- Mai descrizioni nuove fuori canone.
- Mai aggettivi morali ("sacro", "magico", "ancestrale", "ultimo avamposto").
- L'odore di sale e alga (Bible §8.3) può essere richiamato in narrativa, ma con misura.
- Il **cigolio dei pali** è canonico (Bible §8.3) — può essere usato come marker sonoro del Pontile alla sera.

## Storie / scene di apparizione

- s01: assente.
- s02: assente.
- s03: assente.
- s04: assente.
- s05: assente.
- s06: assente.
- s07: location risoluzione — Bartolo + Toba + zattera dei fratelli **[esterno]**.
- s08: assente.
- s09: assente.
- s10: ricetto notturno **[esterno e/o interno]**.
- s11: cammeo arrivo Bartolo con frutti da fuori, sera **[esterno]**.
- s12: cammeo mattino "mano alzata che ricade" **[esterno]**; sigillo finale presenza implicita **[off-screen]**.

## Disallineamenti / domande aperte

- **Lunghezza esatta del Pontile**: ~15 metri stimati da `bbox_m_local` interpretato come ~150 in unità ridotte. Da validare quando la cartografia avrà scala precisa.
- **Forma esatta della capanna** (tonda vs ottagonale): la Bible non lo specifica, derivazione "tonda od ottagonale piccola". **Probabilmente tonda** (più naturale per una capanna di canne); confermare.
- **Presenza di stufa/camino interno**: derivazione autoriale (Bartolo deve scaldarsi d'inverno). La Bible non lo dice. Posto al centro / lato come piccolo focolare.
- **Esistenza del piccolo ponte di legno verso la Spiaggia come "annesso del Pontile" o entità separata**: il Glossario §2.4 dice "raggiungibile dal piccolo ponte di legno dietro al Pontile" — quindi è funzionalmente associato al Pontile. Lo gestisco come annesso. Eventuale scheda separata per il ponte non sembra necessaria.
- **Presenza di un piccolo "casotto" o ricovero attrezzi sulla riva interna**: non menzionato in Bible ma plausibile. Lasciato fuori canone, da aggiungere se Ray vuole.

## Riferimenti puntuali (citazioni dirette dalle fonti)

**Fonti canoniche dirette:**
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §4.3 BARTOLO: "Vive sul Pontile, Quartiere d'Acqua a sud, in una capanna bassa col tetto di canne accanto al punto in cui il Fiume sfocia nel mare attraverso La Bocca. Dorme nella barca quando fa caldo."
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §6 PALETTE VISIVA — Quartieri: "Quartiere d'Acqua (Sud): verde mare antico, blu-grigio profondo, sabbia chiara, riflessi argentei."
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8.1 Distanze: "Pontile di Bartolo: 40 minuti."
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8.3 Quartiere d'Acqua: "Pontile di Bartolo dentro La Bocca (assi scure, pali nell'acqua, capanna in cima)... Vento Mulinello la sera sposta le conchiglie sulla Spiaggia, fa cigolare i pali del Pontile. Odore: sale e alga. Suono: acqua contro i pali, gabbiani al mattino."
- `architettura/ARCHI_12_STORIE_v1__1_.md` S7: "Bartolo è al Pontile, semi-disteso nella barca. Vede la zattera arrivare nell'acqua mista della Bocca... Toba (cammeo, una sola scena) è seduta sul Pontile vicino al padre."
- `architettura/ARCHI_12_STORIE_v1__1_.md` S12: "Bartolo (cammeo Pontile mattino, mano alzata che ricade; nel sigillo finale: presenza nella barca implicita, mai mostrata)."
- `worldbuilding/GLOSSARIO_ISOLA.md` §2.4 Quartiere d'Acqua: "Il Pontile di Bartolo — dentro La Bocca, assi scure, pali piantati nell'acqua. La capanna di Bartolo — in cima al Pontile, bassa, col tetto di canne. La Spiaggia delle Conchiglie — sulla costa-mare oltre La Bocca, raggiungibile dal piccolo ponte di legno dietro al Pontile."
- `pipeline_narrativa/story_graph.json#entities.locations.pontile_bocca`
- `cartografia/geo/island.geojson#features.id=pontile_bocca`: pier, quarter=acqua, geometry=LineString, centroid_m_local: [4015, 925], bbox_m_local: [4015, 850, 4015, 1000], size_m_local: [0, 150].

**Derivazioni autoriali:**
- *Dimensioni 15m × 2m*: derivata da `bbox_m_local` interpretata in scala ridotta + funzionalità (un pontile di traghettatore non è gigante).
- *Direzione nord-sud*: derivata da topologia (Pontile dentro La Bocca, La Bocca apre il Fiume verso il mare a sud).
- *Pianta capanna tonda od ottagonale ~3m diametro*: derivata da "capanna bassa" + funzionalità abitativa minima per Bartolo.
- *Porta a nord, finestra a sud*: derivazione autoriale coerente (porta verso il pontile dove arrivano gli ospiti, finestra verso il mare aperto che Bartolo guarda).
- *Stufa/camino interno*: derivazione necessaria (inverno).
- *Barca ormeggiata lato est*: derivazione autoriale (lato est preferibile per il vento meno forte rispetto al lato ovest che riceve il Mulinello sera).
- *Piccolo ponte di legno con corda-corrimano da un lato*: derivazione autoriale per sicurezza minima + registro pre-industriale.
- *Acqua mista visibilmente di colori diversi (verde-blu vs argentato)*: derivazione da Bible §8 "acque dolci e salate si mescolano" + palette quartiere.

**Cliché da evitare specifici visivi**: derivati da `PATTERN_AI_DA_BANDIRE_v1.md` applicato al caso pontile-pescatore-mediterraneo.
