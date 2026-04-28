---
id: <id_snake_case>
name: <Nome Visualizzato>
famiglia: personaggio                # personaggio | luogo | oggetto | vento | visual_signature
sottotipo: <es: bambini | primari | cuccioli | secondari | collettivo | building | forest | clearing | ...>
status: stub                         # stub | provvisorio | canonico
ultima_modifica: YYYY-MM-DD
fonti:
  - pipeline_narrativa/story_graph.json#entities.<famiglia>.<id>
  - pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md §X.Y
  - cartografia/geo/island.geojson#features.id=<id>          # solo per luoghi
appare_in_storie: []                  # lista [s01, s02, ...] popolata dall'agente

# Campi specializzati (eliminare quelli non applicabili):

# Personaggio:
specie: <species>
tipo_grafo: <type>
ruolo_saga: <role_saga>
relazioni:
  dimora: <id_luogo|null>
  quadrante_grafo: <quadrant|null>
  related_to: []
  cross_skill:
    cartografia: <id_feature|null>

# Luogo:
quartiere: <terra|fuoco|acqua|aria|centro|perimetro>
cartografia:
  feature_id: <id>
  type_geo: <tipo>
  status_geo: <canonico|provvisorio|stub>
  quarter: <quartiere>
  category: <category|null>
  centroid_m_local: [x, y]
  bbox_m_local: [minx, miny, maxx, maxy]
  size_m_local: [w, h]
  altitudine_m: <m|null>
  geometry_type: <Point|LineString|Polygon|...>
  parent_geo: <id|null>
  children_geo: []
  aliases_geo: []

# Oggetto:
relazioni:
  associato_a_personaggio: <id|null>
  associato_a_luogo: <id|null>
---

# <Nome Visualizzato>

> **Stato compilazione:** body provvisorio, generato dal travaso meccanico Bible→catalogo il YYYY-MM-DD. Le sezioni con `_da popolare dal grafo_` saranno completate da Ray quando ragionera' sul grafo.

## Principio di compilazione (rimuovere prima di salvare)

**Travaso meccanico** dalla Bible (`pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md`) e da `story_graph.json` al catalogo.

- Sezioni del template che combaciano con campi Bible (Aspetto, Comportamento, Cliche'/vincoli): **copia/parafrasi 1:1**.
- Sezione "Storie / scene di apparizione": **automatizzata dal grafo** (lista delle storie in cui appare l'entita').
- Sezioni che la Bible non copre (Palette, Variabilita', Per stampa 3D, Per narrativa e social, Identita' visuale sintesi, ecc.): **placeholder uniforme `_da popolare dal grafo_`**. Niente inferenze, niente proposte. Saranno completate da Ray quando ragionera' sul grafo.
- Cio' che la Bible ha "in piu'" (Funzione narrativa, Voce tipica, archi narrativi, vincoli narrativi non visivi): **non si porta nel catalogo**, resta nella Bible.

## Identita' visuale (sintesi)

_da popolare dal grafo_

## Aspetto / forma

[travaso da Bible "Aspetto."]

## Abbigliamento / stato d'uso

[travaso da Bible se presente; altrimenti `_da popolare dal grafo_`]

## Espressione / comportamento

[travaso da Bible "Comportamento operativo."]

## Palette e atmosfera

_da popolare dal grafo_

## Contesto e ambientazioni ricorrenti

[travaso da Bible se presente; altrimenti `_da popolare dal grafo_`]

## Coerenza cross-scena (cose che NON cambiano)

[derivato da Bible "Aspetto." (dettagli fisici fissi); altrimenti `_da popolare dal grafo_`]

## Variabilita' ammessa

_da popolare dal grafo_

## Cliche' da evitare

[travaso da Bible "Note e vincoli." parte cliche'/"mai..."]. Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

## Per stampa 3D

_da popolare dal grafo_

## Per narrativa e social

_da popolare dal grafo_

## Storie / scene di apparizione

[lista automatizzata dal grafo: per ogni s01..s12 dove l'entita' appare, una riga col ruolo/scena breve]

## Disallineamenti / domande aperte

[fatti rilevati durante il travaso: conflitti Bible vs grafo, ambiguita' di nome, ecc. Vuoto se nulla.]

## Riferimenti puntuali (citazioni dirette dalle fonti)

Ogni dato canonico riportato sopra DEVE avere qui una citazione ancorata:

- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §X.Y: "..."
- `pipeline_narrativa/story_graph.json#entities.<famiglia>.<id>` — campo `<x>`: "..."
- `pipeline_narrativa/story_graph.json#stories.s0X.<campo>`: "..."
