# `pipeline_narrativa/narrazione_fattuale/`

Narrazione **fattuale** delle 12 storie della saga. Cosa è successo in ogni storia, **senza** la voce autoriale.

> 12/12 file presenti (split meccanico dal sorgente in `_source/Ciclo_a-b-c-d_260429_111628.txt`, fornito da Ray il 2026-04-29).
> Sono la **fonte primaria** per l'agente di estensione hook visivi (vedi `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md`).

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

**12/12 storie presenti** (caricate il 2026-04-29). Ciclo A (s01-s03 inverno · Taglio · distinguere), Ciclo B (s04-s06 primavera · Intreccio · connettere), Ciclo C (s07-s09 estate · cambiare), Ciclo D (s10-s12 autunno · tenere · sigillo).

Sorgente unico: `_source/Ciclo_a-b-c-d_260429_111628.txt`. I 12 file `sNN_*.md` sono derivati meccanicamente con script di split (header + body) e devono essere considerati lo specchio del sorgente. Se Ray modifica il sorgente, ri-eseguire lo split.

## Read-only per agenti

Solo Ray scrive in questa directory. Gli agenti leggono per generare gli hook.
