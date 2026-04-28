---
id: pallone_di_stoffa_cucita
name: Pallone di Stoffa Cucita
famiglia: oggetto
sottotipo: oggetto_di_scena_ricorrente
status: provvisorio
ultima_modifica: 2026-04-28
fonti: ["pipeline_narrativa/story_graph.json#stories.s03.visual_anchors.recurring_visual_objects", "pipeline_narrativa/story_graph.json#stories.s11.visual_anchors.recurring_visual_objects"]
appare_in_storie: ["s03", "s11"]
relazioni:
  associato_a_personaggio: ["gabriel", "elias", "noah"]
  associato_a_luogo: ["foresta_intrecciata", "piazza_villaggio"]
---

# Pallone di Stoffa Cucita

> **Stato compilazione:** scheda creata in fase E (post-saga, mis_004 OPZIONE B). Distinzione esplicita: `oggetto_di_scena_ricorrente` ≠ `oggetto_simbolo_saga` (i 13 archetipi). Il pallone è oggetto-firma del gruppo cuccioli, ricorrente trasversa s03→s11 ma senza la densità simbolica dei 13 oggetti canonici.

## Identità visuale (sintesi)

Pallone artigianale dei fratelli, fatto di stoffa cucita. Oggetto del gioco quotidiano dei cuccioli sull'isola.

## Aspetto / forma

Stoffa cucita a mano, forma sferica imperfetta. Pesa più di un pallone gonfio (per la stoffa) ma rotola lo stesso. Non rimbalza come un pallone moderno.

## Contesto e ambientazioni ricorrenti

- **s03** (chiusura blocco A, "Il Pallone oltre la Foresta"): oggetto centrale della storia. Calcio mal misurato di Noah, il pallone rotola oltre il margine della Foresta Intrecciata. Rovo lo restituisce posandolo a un passo dal margine.
- **s11** (centro blocco D, "La Festa del Raccolto"): ricomparsa, giochi cuccioli durante la festa. Bloom collettivo del seed seminato in s03.

## Coerenza cross-scena (cose che NON cambiano)

- Stoffa cucita a mano, non gomma né cuoio.
- Forma sferica imperfetta.
- Oggetto di gioco (non strumento, non rito).
- Appartiene al gruppo cuccioli, non a un singolo personaggio.

## Distinzione

`oggetto_di_scena_ricorrente`: oggetto narrativamente ricorrente in più storie ma NON tra i 13 oggetti-simbolo saga (bandana_rovo, bisaccia_zolla, braccialetto_s9, cesto_salvia, cicatrice_grunto, conchiglia_amo, corda_nodo, grembiule_fiamma, lanterna_velata_s10, nido_vuoto_s08, pagnotta_forno, scialle_stria, sciarpa_memolo). Tracciato in `recurring_visual_objects` del grafo legacy. NON entra in `oggetti_simbolo_presenti` del canonical v1.2 (REGOLA 0.6 MIGRATION_PROMPT_FASE_E.md).

## Storie / scene di apparizione

- s01: assente.
- s02: assente.
- s03: **prima apparizione** (recurring_visual_object, oggetto-perno della storia). seed_pallone_stoffa_cucita piantato.
- s04-s10: assente.
- s11: ricomparsa (giochi cuccioli durante festa raccolto). debt_s03_to_s11_pallone_ricomparsa_giochi_cuccioli_tentativo chiuso (bloom).
- s12: assente.

## Riferimenti puntuali

- `pipeline_narrativa/story_graph.json#stories.s03.visual_anchors.recurring_visual_objects` = `["pallone_di_stoffa_cucita"]`
- `pipeline_narrativa/story_graph.json#stories.s11.visual_anchors.recurring_visual_objects` (atteso bloom)
- `_porting_grafo/dossier_fase_e/dossier/_canon_misalignments.json#mis_004` (resolved in fase E OPZIONE B)
