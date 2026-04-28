---
id: pozza_abbeveratoio_pastori
name: Pozza dell'Abbeveratoio dei Pastori
famiglia: luogo
sottotipo: water_feature
quartiere: aria
status: provvisorio
ultima_modifica: 2026-04-28
fonti: ["pipeline_narrativa/story_graph.json#stories.s02.location_primary.specific_points", "pipeline_narrativa/story_graph.json#stories.s02.visual_anchors.scene_hooks"]
appare_in_storie: ["s02"]
cartografia:
  feature_id: null
  type_geo: point
  status_geo: provvisorio
  quarter: aria
  category: water_feature
  centroid_m_local: null
  bbox_m_local: null
  size_m_local: null
  altitudine_m: null
  geometry_type: Point
  parent_geo: pascoli_alti
  children_geo: []
  aliases_geo: []
relazioni:
  parent_location: pascoli_alti
  related_to: ["pastori"]
---

# Pozza dell'Abbeveratoio dei Pastori

> **Stato compilazione:** body provvisorio, generato dal porting fase E (P0 di s02) il 2026-04-28. Le sezioni con `_da popolare dal grafo_` saranno completate da Ray quando ragionerà sul grafo (fase F catalogo).

## Identità visuale (sintesi)

_da popolare dal grafo_

## Aspetto / forma

Pozza piccola sui Pascoli Alti, sub-location dei Pascoli (quartiere aria). D'estate funge da abbeveratoio per le greggi dei Pastori. D'inverno gela; nelle giornate di sole il velo di superficie può sgelarsi parzialmente, mostrando l'acqua sotto.

## Espressione / comportamento

_da popolare dal grafo_

## Palette e atmosfera

Quartiere d'Aria (Nord): grigio pietra, blu ghiaccio, vento secco. La pozza in inverno: ghiaccio chiaro con velo d'acqua sgelata in superficie quando c'è sole; riflessi mobili.

## Contesto e ambientazioni ricorrenti

Sub-location dei Pascoli Alti, quartiere aria. Vicino alle greggi dei Pastori (off-screen in s02). Cammino di accesso: sentiero in salita dalla Scuola di Stria / dal Villaggio.

## Coerenza cross-scena (cose che NON cambiano)

È una pozza piccola, non un lago né una fonte. Funzione: abbeveratoio (estate). Stagionalmente cambia stato: acqua liquida d'estate, ghiaccio d'inverno con velo sgelabile nelle giornate di sole. Posizione fissa sui Pascoli Alti, quartiere aria.

## Variabilità ammessa

Stato dell'acqua secondo stagione e meteo: liquida (estate) → ghiaccio totale (inverno freddo) → ghiaccio con velo sgelato in superficie (inverno con sole). Riflessi della superficie variano con luce e vento.

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`. Lista specifica `_da popolare dal grafo_`.

## Per stampa 3D

_da popolare dal grafo_

## Per narrativa e social

_da popolare dal grafo_

## Storie / scene di apparizione

- s01: assente.
- s02: **prima apparizione (focal point)**. Citata in `location_primary.specific_points` come unica sub-location di pascoli_alti. Visual_anchor signature hook s02_h3 (`pozza_ghiacciata_con_velo_d_acqua_sgelato_in_superficie`) e visual_anchor s02_h4 (`pozza_dopo_il_gesto_di_noah`). La storia si chiama "Il Riflesso nella Pozza".
- s03-s12: `_da popolare dal grafo_` (verifica eventuali altre apparizioni nelle migrazioni successive).

## Disallineamenti / domande aperte

- Il `_note` di `location_primary` in s02 dichiarava: "Da aggiungere come sub_location di pascoli_alti in ATLANTE quando si raffina (Fase E)." Aggiunta eseguita in fase E, P0 di s02 (2026-04-28). Misalignment `mis_002` di `_canon_misalignments.json` → resolved.
- Cartografia: feature_id ancora `null`. Da assegnare se serve geometria esplicita (probabilmente Point sui Pascoli Alti). Decisione cartografica successiva, non blocca il porting fase E.

## Riferimenti puntuali (citazioni dirette dalle fonti)

- `pipeline_narrativa/story_graph.json#stories.s02.location_primary._note`: "La pozza è piccola, d'estate abbeveratoio delle capre dei Pastori, ora ghiacciata con il velo di superficie appena sgelato da una giornata di sole. Da aggiungere come sub_location di pascoli_alti in ATLANTE quando si raffina (Fase E)."
- `pipeline_narrativa/story_graph.json#stories.s02.location_primary.specific_points[0]`: `pozza_abbeveratoio_pastori`.
- `pipeline_narrativa/story_graph.json#stories.s02.visual_anchors.scene_hooks[s02_h3_signature].location_precise`: `pozza_ghiacciata_con_velo_d_acqua_sgelato_in_superficie`.
- `pipeline_narrativa/story_graph.json#stories.s02.visual_anchors.scene_hooks[s02_h4].location_precise`: `pozza_dopo_il_gesto_di_noah`.
- `_porting_grafo/output/s02/s02_catalog_proposals.md` §C (P0 fase E, 2026-04-28).
