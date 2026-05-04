# `_inventory/` — Inventari hook→prompt→immagine per storia

> **Scopo.** Per ogni storia (s01..s12) un file `sNN_inventory.md` mappa **ogni hook visivo** ai suoi elementi (personaggi/luogo/oggetti) e verifica lo **stato di disponibilità** dei prompt grok e delle immagini canoniche già generate. È la **checklist operativa** per assemblare le composizioni finali del libro.

## Struttura

Un file per storia: `sNN_inventory.md`.

### Sezioni standard

1. **Riepilogo** — metriche aggregate (hook totali, personaggi/luoghi distinti, % prompt pronti, % img pronte, gap critici)
2. **Hook per hook** — per ognuno dei 10 hook, una tabella con elementi visivi × stato prompt + immagini canoniche
3. **Aggiunte dalla prosa al canone** — elementi nuovi introdotti dalla prosa definitiva che NON erano nel grafo: vanno integrati nel catalogo (`visual/.../scheda.md`) o segnalati alla Bible. **MAI nel grafo** (read-only).
4. **Gap operativi** — divisi per priorità (🔴 critica, 🟡 minore, 🟢 bassa)
5. **Cosa serve per concludere** — todo list operativa (genera img personaggi, scrivi prompt mancanti, aggiungi varianti atmosferiche)
6. **Riferimenti** — link a testo definitivo, brief writing, grafo

## Pattern di lavoro

Quando si approccia una storia:

1. Leggere `pipeline_narrativa/storie_finali/sNN.md` (testo definitivo)
2. Leggere `pipeline_narrativa/story_graph.json#stories.sNN.visual_anchors.scene_hooks` (10 hook pre-definiti)
3. Per ogni hook (1-10):
   - Identificare personaggi in scena (lettura prosa)
   - Identificare luogo (idem)
   - Identificare oggetti canonici visibili (idem)
4. Verificare nel repo:
   - `visual/personaggi/.../prompt_grok.md` esiste?
   - `visual/personaggi/.../immagini/*.jpg` ci sono?
   - `visual/luoghi/.../prompt_grok.md` esiste?
   - `visual/luoghi/.../immagini/*.jpg` ci sono?
   - `visual/oggetti/.../prompt_grok.md` esiste?
5. Identificare aggiunte dalla prosa NON canoniche → catalogo update list
6. Listare gap operativi divisi per priorità

## Aggiunte da prosa: regola di routing

La prosa definitiva può introdurre dettagli sensoriali, gesti, varianti atmosferiche, oggetti minori. Pattern di routing:

| Tipo aggiunta | Dove va |
|---|---|
| Dettaglio visuale di un luogo (es. vapore alle finestre) | `visual/luoghi/.../scheda.md` |
| Dettaglio visuale di un personaggio (es. gesto ricorrente) | `visual/personaggi/.../scheda.md` |
| Variante di un oggetto canonico (es. cornetto = sotto-tipo pagnotta) | `visual/oggetti/.../scheda.md` (sezione Variabilità ammessa) |
| Frasi-codice / vocalizzazioni / suoni | Già nel grafo (visual_anchors / quote_tracker) — se nuove, segnalare alla Bible |
| Trama / vincoli narrativi nuovi | NON inserire da soli. Segnalare a Ray. |
| Decisioni autoriali strutturali | Solo via pacchetto autoriale Ray. |

**MAI** modificare `pipeline_narrativa/story_graph.json` da prosa: il grafo è read-only post-pacchetti autoriali.

## Stato

| Storia | Inventario | Status |
|---|---|---|
| s01 — La Nebbia delle Montagne Gemelle | [`s01_inventory.md`](./s01_inventory.md) | ✅ creato (manuale, primo pattern) |
| s02..s12 | da fare | ⏳ |

## Automazione futura

Lo schema è deterministico. Un script Python (`scripts/build_hook_inventory.py`) potrà generare lo skeleton automaticamente:

1. Parsa il testo della storia (`pipeline_narrativa/storie_finali/sNN.md`) per identificare:
   - Pagine/hook (10 marker `## Pagina N` + commento `<!-- @hook ...` )
   - Frasi-codice (caratteri tra `«»`)
   - Riferimenti a personaggi (NER + matching contro `entities.characters`)
   - Riferimenti a luoghi (matching contro `entities.locations`)
   - Riferimenti a oggetti (matching contro `entities.objects`)
2. Cross-check con il filesystem:
   - `visual/personaggi/*/*/*/prompt_grok.md` (esiste?)
   - `visual/personaggi/*/*/*/immagini/*.jpg` (n. img canoniche)
   - `visual/luoghi/**/prompt_grok.md` (esiste?)
   - `visual/luoghi/**/immagini/*.jpg` (n. img canoniche)
   - `visual/oggetti/*/prompt_grok.md`
3. Genera `_inventory/sNN_inventory.md` skeleton riempito con 80% delle info; Ray valida e completa il 20% (frasi-codice, gap minori, aggiunte da prosa che richiedono giudizio).

## Integrazione con catalogo_web

L'inventario può essere esposto nel viewer web (su Vercel) come **dashboard checklist** per ogni storia:
- 📊 Progress bar (% hook con composizione pronta)
- 🔗 Link rapidi ai prompt grok di ogni elemento
- 🖼️ Anteprima delle immagini canoniche disponibili
- ⚠️ Highlights dei gap critici da colmare

Il viewer web parsa direttamente i file `_inventory/sNN_inventory.md` e li renderizza come tabelle interattive.

## Riferimenti

- Storia definitiva: `pipeline_narrativa/storie_finali/sNN.md` + `pipeline_narrativa/storie_finali/README.md`
- Catalogo personaggi/luoghi/oggetti: `visual/`
- Catalogo web: `catalogo_web/` (deploy Vercel)
- Grafo: `pipeline_narrativa/story_graph.json`
