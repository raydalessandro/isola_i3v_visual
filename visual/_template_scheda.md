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

> **Stato compilazione:** body provvisorio, in attesa revisione Ray. Compilato il YYYY-MM-DD con metodo "compilatore" (completa-non-rimuovere). Marcatori di provenienza: nessun tag = canone (citato in fondo); `[inf]` = inferito dai dati canonici; `[prop]` = proposta visiva da validare.

## Principio di compilazione (rimuovere prima di salvare)

**Tutte le 14 sezioni vanno compilate.** Anche quando il canone non dichiara nulla su un aspetto, si propone un'inferenza coerente, marcata con `[inf]` (deduzione logica dal canone) o `[prop]` (scelta creativa coerente, da validare con Ray). Non rimuovere sezioni: una sezione vuota e' un'occasione persa per la narrativa futura.

In casi davvero non applicabili (es. "abbigliamento" per un fenomeno acustico come un vento, o "espressione del volto" per un oggetto inanimato), **reinterpretare il campo** in modo coerente con la natura dell'entita' (es. per un vento "abbigliamento" → manifestazione sensibile / vestitura percettiva).

## Identita' visuale (sintesi)

Una-due frasi che fissano l'entita' in modo specifico, niente cliché.

## Aspetto / forma

Per personaggi: volto, corporatura, tratti distintivi.
Per luoghi: morfologia, materiali, scala, dettagli costruttivi.
Per oggetti: forma, dimensioni, materiali, finitura.

## Abbigliamento / stato d'uso

Per personaggi: capi tipici, materiali, colori, accessori, variazioni stagionali.
Per oggetti: nuovo/usurato, segni d'uso.

## Espressione / comportamento

Per personaggi: espressioni tipiche, gestualità, postura, andatura.
Per venti: comportamento canonico, pattern di movimento.

## Palette e atmosfera

Colori dominanti, qualità della luce, atmosfera cromatica ricorrente.

## Contesto e ambientazioni ricorrenti

Luoghi e momenti del giorno in cui l'entita' compare tipicamente.

## Coerenza cross-scena (cose che NON cambiano)

Vincoli inderogabili: dettagli che restano fissi attraverso tutte le storie.

## Variabilita' ammessa

Cose che possono variare per scena/stagione/contesto senza rompere la coerenza.

## Cliche' da evitare

Riferimento: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

Lista specifica dei cliché da non applicare a questa entita'.

## Per stampa 3D

Volumi, proporzioni, scala, orientamento canonico, simmetrie/asimmetrie. Indicazioni utili per modellazione e per le 4 vedute (fronte / retro / profilo_dx / profilo_sx).

## Per narrativa e social

Registri d'uso testuale, parole-chiave da usare/evitare, tono delle descrizioni in didascalie e post.

## Storie / scene di apparizione

Lista per storia (s01..s12) con ruolo/scena breve.

## Disallineamenti / domande aperte

Conflitti rilevati fra fonti, dubbi non risolti, richieste a Ray.

## Riferimenti puntuali (citazioni dirette dalle fonti)

Ogni dato visivo riportato sopra DEVE avere qui una citazione ancorata:

- `pipeline_narrativa/story_graph.json#entities.<famiglia>.<id>` — campo `<x>`: "..."
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §X.Y: "..."
- `cartografia/geo/island.geojson#features.id=<id>` — proprieta' `<x>`: "..."
