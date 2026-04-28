# Dossier Fase E — Migrazione nodi al schema canonico v1.1

Questa cartella contiene tutto ciò che serve a una chat fresca per migrare un nodo storia al formato canonico.

## Workflow consigliato

### Per Ray (preparazione)

1. Apri una chat nuova in Claude (app o web).
2. Carica come allegati i file di questa cartella:
   - **`MIGRATION_PROMPT_FASE_E.md`** — il prompt master da incollare come primo messaggio
   - **`story_graph_schema_canonical_v1_1.json`** — schema target
   - **`read_helpers.py`** — script di sola lettura
   - **5 tabelle JSON pre-calcolate** (seeds_index, quadrant_assignment, quote_tracker_per_story, character_constraints, debt_classification)
   - **`GOLD_STANDARDS/s12_gold_standard.json`** (e/o `s11_gold_standard.json`) — esempi di nodo già conforme
   - **`INPUT_NODES/sNN_input.json`** del nodo da migrare (uno per chat, o più se contesto residuo)
3. Incolla il prompt come primo messaggio.
4. La chat risponderà "Ho letto il prompt. Pronto per ricevere il story_id da migrare."
5. Tu rispondi: `Migra s05` (o il nodo che vuoi).
6. La chat lavora, fa eventuali domande, produce due output: `sNN_canonical.json` + `sNN_migration_notes.md`.

### Per Ray (verifica)

1. Leggi rapidamente il `migration_notes.md` per vedere cosa è stato fatto.
2. Se ok, salva i due file.
3. Passa al prossimo nodo (nuova chat o stessa se contesto < 75%).

### Per Ray (chiusura, da rimandare a me)

Quando hai i 12 `sNN_canonical.json`, mandameli e:
- Reintegro nel grafo
- Bumpo a v1.0.0
- Lancio audit finali
- Ti consegno grafo canonico definitivo

## Struttura cartella

```
dossier/
├── README.md                                 ← questo file
├── MIGRATION_PROMPT_FASE_E.md                ← prompt master
├── story_graph_schema_canonical_v1_1.json    ← schema target FREEZATO
├── validation_checklist.json                 ← guardrail bloccanti pre-output
├── read_helpers.py                           ← funzioni Python sola lettura
│
├── seeds_index.json                          ← tabella metadata seeds
├── quadrant_assignment.json                  ← location/character → quadrant
├── quote_tracker_per_story.json              ← flag B/C pre-calcolati
├── character_constraints.json                ← vincoli "Mai" personaggi
├── debt_classification.json                  ← triage 107 entries debt (USO LIMITATO)
│
├── GOLD_STANDARDS/
│   ├── s11_gold_standard.json                ← reference variante
│   └── s12_gold_standard.json                ← reference primario
│
└── INPUT_NODES/
    ├── s01_input.json                        ← bundle: old_node + context + hook plans
    ├── s02_input.json
    ├── ...
    └── s12_input.json                        ← (già conforme, copia 1:1)
```

## Decisioni Fase E già fissate (per la chat fresca)

Da `MIGRATION_PROMPT_FASE_E.md`:

- **Schema scene_hook**: 8 obbligatori + 6 opzionali
- **Filosofia null**: opzione (b) — campi opzionali sempre presenti come `null`/`[]` per uniformità visiva
- **Quadrant rename**: `centro` → `centro_villaggio` (canonizzazione)
- **Triage debt**: 60 dict mantenuti + 2 stringhe retrofittate + 45 archiviate come rumore
- **13 nuovi campi narrativi**: 5 categoria A (null), 5 categoria B (auto da quote_tracker), 3 categoria C (auto da entities)
- **Mai modificare narrativa**: premise, threshold_moment, resolution_mode, ecc. copiati identici dal nodo vecchio
- **Schema freezato**: nessuna chat fresca può modificarlo

### Guardrail bloccanti (validation_checklist.json)

Prima di consegnare ogni nodo, la chat fresca DEVE applicare:

1. **`no_new_ids`** — vietato inventare ID di qualsiasi tipo
2. **`no_inference_fields`** — entry_point_type, closure_type, estimated_length restano null
3. **`quadrant_must_match`** — solo valori canonici dello schema
4. **`characters_must_exist`** — ogni personaggio citato deve esistere nel grafo

Se anche un solo guardrail fallisce → fermarsi e chiedere a Ray.

### Filosofia stretta del null

> Per TUTTI i campi: se l'informazione non è esplicitamente presente nei dati di input, valore = `null` (o `[]` per liste, `false` per bool). NON inferire da contesto narrativo, common sense, altre storie o conoscenza implicita.

### Uso ristretto debt_classification.json

Solo per triage (mantieni / retrofitta / archivia). NON per arricchire contenuto narrativo del nodo nuovo.

## Casi speciali

### s12 — già conforme

Il nodo S12 è stato creato direttamente nel formato canonico. La chat fresca per s12 deve essenzialmente:
- Aggiungere i 13 nuovi campi (A=null, B+C=auto)
- Aggiungere i 6 opzionali scene_hook (`null` se non popolati)
- Triage debt (S12 ha 16 debt closed dict canonici già, da mantenere)

Lavoro veloce.

### s06 — scene_hooks string-legacy

S6 ha gli scene_hooks come stringhe narrative libere invece che dict. La chat fresca deve **parsare** ogni stringa e **ricostruire** un hook dict canonico. Vedi REGOLA 3 nel prompt master.

Lavoro più impegnativo, **chiedere a Ray quando in dubbio sull'interpretazione di una stringa**.

### s01-s05 — drift schema chat A

S1-S5 hanno il vecchio schema scene_hook (location_precise, palette_local, atmosphere, focal_action, ecc.). Mapping diretto via REGOLA 3.

I nodi sono **più scarni** narrativamente di S6+ (Ray arricchirà in Fase D). NON arricchire ora, copia identico.

## Test del read_helpers

```bash
cd dossier/
python3 read_helpers.py s05
```

Stampa il summary completo per S5: seeds, flag, debt classification.
