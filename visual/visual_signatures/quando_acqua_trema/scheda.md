---
id: quando_acqua_trema
name: Quando Acqua Trema
famiglia: visual_signature
status: provvisorio
ultima_modifica: 2026-04-28
fonti: ["pipeline_narrativa/story_graph.json#entities.visual_signatures.quando_acqua_trema"]
appare_in_storie: []
---


# Quando Acqua Trema

> **Stato compilazione:** body provvisorio, generato dal travaso meccanico Bible→catalogo il 2026-04-28. Le sezioni con `_da popolare dal grafo_` saranno completate da Ray quando ragionerà sul grafo.

## Identità visuale (sintesi)


**Descrizione (grafo):** immagine ricorrente legata al Pattern A.
**Tipo:** firma_visiva_saga.
**Vincolo:** `mai_dichiarata_nel_testo`.
**Pattern A linked:** sì.


## Aspetto / forma

Quando il Vento Mulinello soffia forte la sera, il Fiume si increspa controcorrente per un attimo. È un fenomeno raro che gli abitanti chiamano *quando l'acqua trema*. Si manifesta come una piccola increspatura che va contro il flusso ma non lo rompe.

## Espressione / comportamento

_da popolare dal grafo_

## Palette e atmosfera

_da popolare dal grafo_

## Contesto e ambientazioni ricorrenti

Il fenomeno si manifesta sul Fiume, in particolare al guado nord (Guado di Pietre Piatte), durante la sera di Vento Mulinello forte.

## Coerenza cross-scena (cose che NON cambiano)

- Si manifesta solo quando il Mulinello soffia forte la sera (non il Mulinello seriale di ogni sera).
- È un'increspatura controcorrente che NON rompe il flusso.
- Mai dichiarata esplicitamente nel testo (constraint `mai_dichiarata_nel_testo`).
- Pattern A linked: immagine in miniatura del Pattern A ("cose rotte arrivano lo stesso", come dice la nota in S12).
- Quota saga: massimo 2 menzioni in tutta la saga (chiusa con S12).

## Variabilità ammessa

_da popolare dal grafo_

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

Da `entities.visual_signatures.quando_acqua_trema.constraint`: **mai dichiarata nel testo** — il fenomeno appare ma non viene nominato/spiegato esplicitamente. Vincolo legato al Pattern A: il rilettore coglie, il bambino-lettore no.

## Per stampa 3D

_da popolare dal grafo_

## Per narrativa e social

_da popolare dal grafo_

## Storie / scene di apparizione

- s01: assente.
- s02: assente.
- s03: assente.
- s04: assente.
- s05: assente.
- s06: assente.
- s07: assente.
- s08: **prima menzione saga** (1 di 2). Liù come messaggera porta l'ipotesi, non certezza: *"Il vento sale forte stasera. Forse l'acqua trema."* Cielo color piombo, Mulinello forte (non seriale). Lore-hook tracciato in `quote_tracker.when_water_trembles_stories`.
- s09: assente.
- s10: assente.
- s11: assente.
- s12: **seconda e ultima manifestazione saga** (2 di 2, quota chiusa). Si manifesta al guado di pietre piatte nord, "dove l'acqua trema piano e non rompe il flusso". Pattern A in miniatura. Visual_anchor `hook_03_guado_pietre_piatte_nord_when_water_trembles_2di2`. Callback `cb_s12_007_radura_pini_passaggio_autunnale_when_water_trembles_2_di_2_quota_chiusa`.

## Disallineamenti / domande aperte

- Il `name` nel frontmatter è "Quando Acqua Trema" (Title Case generato dallo script). La forma canonica nella Bible (§8 atlante prima §8.1) e nel testo del grafo è ***quando l'acqua trema*** (lowercase, in corsivo, articolo "l'" incluso). Decisione: il display name dovrebbe essere "Quando l'Acqua Trema" o "*quando l'acqua trema*"? Da risolvere nel grafo (`entities.visual_signatures.quando_acqua_trema.name`).

## Riferimenti puntuali (citazioni dirette dalle fonti)

- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8 (riga prima di §8.1): "Quando il Vento Mulinello soffia forte la sera, il Fiume si increspa controcorrente per un attimo. È un fenomeno raro che gli abitanti chiamano *quando l'acqua trema*."
- `pipeline_narrativa/story_graph.json#entities.visual_signatures.quando_acqua_trema`: `type: firma_visiva_saga`, `description: "immagine ricorrente legata al Pattern A"`, `constraint: mai_dichiarata_nel_testo`, `pattern_a_linked: true`.
- `pipeline_narrativa/story_graph.json#quote_tracker.when_water_trembles_stories`: `["s08", "s12"]`.
- `pipeline_narrativa/story_graph.json#stories.s08`: "Prima menzione saga del fenomeno 'quando l'acqua trema' — 1 di 2 menzioni pianificate saga"; "Liu passa rapida aggrappandosi al cornicione: 'Il vento sale forte stasera. Forse l'acqua trema.' Riparte con la corrente"; "non il Mulinello seriale di ogni sera. Il cielo vira al color piombo".
- `pipeline_narrativa/story_graph.json#stories.s12.visual_anchors.scene_hooks[hook_03]`: "guado_pietre_piatte_nord_when_water_trembles_2di2"; "2a e ultima manifestazione saga when_water_trembles quota <=2 chiusa; Pattern A immagine in miniatura (l'increspatura non rompe il flusso - cose rotte arrivano lo stesso, MAI NOMINATO)".
- `pipeline_narrativa/story_graph.json#stories.s12`: "su per il Fiume fino al guado nord dove l'acqua trema piano e non rompe il flusso".
