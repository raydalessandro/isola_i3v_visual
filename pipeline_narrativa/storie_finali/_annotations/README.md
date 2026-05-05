# `_annotations/` — Annotazioni operative per hook

> **Scopo.** Per ogni storia, un file YAML deterministico che dice, **per ognuno dei 10 hook narrativi**, **dove succede la scena** (1 location esatta) e **chi è fisicamente in scena**. Sostituisce il NER fuzzy del precedente `build_storie_data.py`.

## Pattern

Un file per storia: `sNN.yaml`.

```yaml
sid: s01
title: La Nebbia delle Montagne Gemelle

hooks:
  s01_h01:
    location: forno              # id luogo canonico (1 solo, deve esistere in entities.locations)
    characters_in_scene: [fiamma, gabriel, elias, noah]   # personaggi fisicamente in scena
    characters_offscreen_or_distant: []                    # personaggi citati ma non in scena
    objects_in_scene: [pagnotta_forno, grembiule_fiamma]   # oggetti visibili
    canonical_details:                                     # note operative + frasi canoniche
      - "..."
    subhooks: []                                           # sotto-hook se l'hook è splittato in più pagine libro
```

## Campi

| Campo | Significato |
|---|---|
| `location` | id luogo canonico in cui succede la scena. **Uno solo**. È **dove** succede l'azione, non dove vengono nominati toponimi nel dialogo. |
| `location_variant` | (opzionale) variante atmosferica/temporale (es. `nebbia`, `tramonto_discesa`, `cengia_in_mezzaroccia`). Aiuta chi genera l'immagine a sapere se serve usare una variante del prompt grok base. |
| `characters_in_scene` | personaggi fisicamente presenti nell'inquadratura. |
| `characters_offscreen_or_distant` | personaggi citati / sagome lontane / sonori implicit. Non vanno in scena ma sono parte del mondo della scena. |
| `objects_in_scene` | oggetti canonici visibili nell'inquadratura. |
| `canonical_details` | note operative: dettagli stabili (Tier A path_details), frasi-codice da preservare, vincoli specifici (variante atmosferica, dettaglio sensoriale). |
| `subhooks` | lista di sotto-hook se l'hook è splittato in più pagine libro. Default vuoto = 1 pagina. |

## Sotto-hook

Quando un hook narrativo viene rappresentato su 2+ pagine fisiche del libro:

```yaml
hooks:
  s01_h05:
    location: pascoli_alti
    location_variant: nebbia
    characters_in_scene: [gabriel, elias, noah]
    objects_in_scene: []
    subhooks:
      - id: s01_h05a
        page_book: 5
        text_split_marker: "primo paragrafo"   # come ricondurlo al testo
        image_status: TBD
        note: "i tre seduti, prima parte (decisione di fermarsi)"
      - id: s01_h05b
        page_book: 6
        text_split_marker: "dopo La nebbia continuò"
        image_status: TBD
        note: "i tre fermi, sonori implicit (pietra, capra, vento)"
```

I marker corrispondenti vanno aggiunti anche nel testo della storia (`pipeline_narrativa/storie_finali/sNN_*.md`) come:

```markdown
## Pagina 5
<!-- @hook s01_h05 | @page 5 | @subhooks [s01_h05a, s01_h05b] | @image TBD -->

<!-- @subhook s01_h05a | @page_book 5 | @image TBD -->
[testo prima parte]

<!-- @subhook s01_h05b | @page_book 6 | @image TBD -->
[testo seconda parte]
```

## Aggiunte da prosa al canone

Sezione opzionale `canon_additions_todo` in fondo al file: lista di update necessari al catalogo (mai al grafo) emersi dalla prosa definitiva. Ogni entry indica `location`/`character`/`object` + `note` + `priority`.

Esempio:
```yaml
canon_additions_todo:
  - object: pagnotta_forno
    note: "Aggiungi 'cornetto' come variante in scheda Variabilità ammessa"
    priority: medium
  - location: pascoli_alti
    note: "Aggiungi variante 'nebbia improvvisa' al prompt grok"
    priority: medium
```

## Stato

| Storia | Annotazioni | Status |
|---|---|---|
| s01 | [`s01.yaml`](./s01.yaml) | ✅ creato (10 hook, 6 todo canone) |
| s02..s12 | da fare | ⏳ |

## Workflow

1. Ray + persona esterna leggono la storia e decidono i sotto-hook (split testo + pagine libro)
2. Ray crea/aggiorna `_annotations/sNN.yaml` con location + chi + sotto-hook
3. Ray aggiorna i marker `@subhook` nel file della storia (`sNN_*.md`)
4. Si rilancia `python3 scripts/build_storie_data.py` → rigenera `catalogo_web/data/storie.json`
5. La dashboard catalogo_web mostra dati corretti (con annotazioni invece di NER)

## Vincoli

- **NON modificare il grafo** (`pipeline_narrativa/story_graph.json`). Le annotazioni sono **operative per la composizione**, non sono canone narrativo (il canone vive nel grafo + Bible).
- Le annotazioni sono il riferimento per il team che genera le immagini su Grok Imagine.
- I `canon_additions_todo` sono input per Ray quando aggiorna le schede catalogo.
