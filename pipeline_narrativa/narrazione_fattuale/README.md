# `pipeline_narrativa/narrazione_fattuale/`

Narrazione **fattuale** delle 12 storie della saga. Cosa è successo in ogni storia, **senza** la voce autoriale.

> Ray sta preparando questi 12 file (uno per storia: `s01_*.md` ... `s12_*.md`).
> Sono la **fonte primaria** per l'agente di estensione hook visivi (vedi `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE.md`).

## Pattern dei file

```
s01_<titolo_breve>.md
s02_<titolo_breve>.md
...
s12_<titolo_breve>.md
```

Esempio: `s01_la_nebbia_delle_montagne_gemelle.md`

## Cosa contengono

Cronaca neutra, in italiano, dei fatti che accadono nella storia. Inizio → fine, in ordine temporale. NIENTE:
- prosa autoriale
- metafore
- voce narrante
- lessico stilistico

SOLO:
- cosa accade
- chi fa cosa
- dove
- quando (momento del giorno)
- oggetti coinvolti

Servono all'agente per identificare **i 10 momenti illustrabili** che diventano hook visivi nel grafo.

## Cosa NON contengono

- testo del libro (voce autoriale)
- inferenze su palette/atmosfera (vengono dal grafo, non da qui)
- decisioni narrative aperte (quelle stanno in `story_graph.json` come provvisori P2)

## Stato

Le 12 narrazioni fattuali sono in produzione (Ray). Saranno aggiunte qui mano mano, una storia alla volta.

## Read-only per agenti

Solo Ray scrive in questa directory. Gli agenti leggono per generare gli hook.
