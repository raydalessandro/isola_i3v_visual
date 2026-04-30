# Pacchetto "Cornice del Mondo" — consegnato 2026-04-30, integrato 2026-04-30

> **Cosa contiene.** 6 documenti DOC_1..DOC_6 con le decisioni autoriali Ray sulla "cornice del mondo" della saga: formula ritornello, saluti dei gruppi, cornici di sfondo distribuite nelle 12 storie, audit sentieri, index sentieri, dettagli stabili Tier A.
>
> **Stato.** ✅ Integrato. I 7 step previsti dal pacchetto sono stati eseguiti il 2026-04-30 con script idempotenti. Tutti i contenuti dei DOC sono stati applicati al grafo o alle schede catalogo. Questi documenti restano come **trail di audit autoriale** + reference per pacchetti futuri analoghi (Tier B/C in arrivo).

---

## Documenti del pacchetto

| Doc | Cosa | Dove è finito |
|---|---|---|
| `DOC_1_formula_ritornello.md` | Formula "che animale è" sg/pl + 6 gruppi eligibili + pool animali + vincoli | `pipeline_narrativa/story_graph.json#world_conventions.refrain_animal_identification` |
| `DOC_2_saluti_gruppi.md` | Saluti distintivi dei 5 gruppi-istituzione (+ 6° creato) | Sezione `## Saluto del gruppo` in 6 schede `visual/personaggi/collettivi/<gruppo>/scheda.md` |
| `DOC_3_cornici_processi.md` | 24 cornici di sfondo (2 per storia) organizzate in 5 processi del mondo | `pipeline_narrativa/story_graph.json#stories.<sid>.cornice_dettagli` |
| `DOC_4_audit_sentieri.md` | Audit del percorrere reale + tier sentieri + mappa "sentieri fantasma" | `stories.<sid>.locations_secondary` (36 entry appese) |
| `DOC_5_index_sentieri.md` | Index navigabile sentieri + schema slot dettaglio | `pipeline_narrativa/story_graph.json#world_conventions.path_details` (placeholder + schema) |
| `DOC_6_mercato_idee_tierA.md` | 20 dettagli stabili approvati per i 5 sentieri Tier A | `world_conventions.path_details.paths.<id>.details[]` + `## Coerenza cross-scena` di 5 schede sentieri |

---

## Decisioni autoriali Ray (2026-04-30)

Decisioni prese in chat e applicate dall'agente IA durante l'integrazione:

1. **6° gruppo "Pescatori delle Case Basse": SI.** Creato come istituzione del Quartiere d'Acqua. Saluto modellato su Camminanti (gesto rubato al lavoro, mano alla rete poi alzata). Apparizioni: cornici S07-C1 e S11-C2.
2. **Pattern A pre-eco s03 (conchiglia): NO incremento `pattern_a_pre_eco_stories`.** Cornice scritta come `oggetto_anomalo` ma minimo invasivo (resta s02 only).
3. **`narrator_address` s09 (cantilena coltivatori modulata): NO incremento `addresses_to_reader`.** Resta a 4 voci. Cornice come fatto narrativo.
4. **Riequilibrio Giro E: SI.** S07-C1 spostata da Giro D a Giro E (la pescatrice è acqua più che stagione). E passa da 2 a 3 cornici.
5. **Schema slot dettaglio sentiero: campo `tipo` rimosso.** Un dettaglio è un dettaglio, libero (non oggetto/pianta/suono/etc).
6. **Vincolo DOC_1 §2 "tre nomi, mai quattro" in plurale:** applicato. s08-c2 plurale Mantenitori = 3 nomi (arvicola, ghiro, faina). Il "ramarra" del DOC_3 era anche un refuso (DOC_1 pool ha "ramarro").
7. **Vincolo DOC_1 §3.4 unicità saga animale:** applicato. s12-c1 Camminanti = ermellino (sostituito da "faina" che era già usata in s08).

---

## Step di integrazione (commit principali)

| Step | Cosa | Commit | Output |
|---|---|---|---|
| 1+2 | nodo radice `world_conventions` + extends `quote_tracker` + bump versioni | `c824496` | `refrain_animal_identification`, `path_details: { paths: {} }`, `quote_tracker.refrain_animal_used_per_story: []` |
| 3 | saluti gruppi nelle 5+1 schede catalogo collettivi | `a3e654e` | `## Saluto del gruppo` + nuova scheda `pescatori_case_basse/` |
| 4 | 24 cornici nelle 12 storie + 8 formule + 2 cantilene | `8b70958` | `stories.<sid>.cornice_dettagli` (2/storia × 12) |
| 5 | sentieri "fantasma" in `locations_secondary` | `92e87b6` | 36 sentieri appesi |
| 6 | path_details Tier A (5 sentieri × 20 dettagli) | `83e361e` | `world_conventions.path_details.paths.<id>` |
| 7 | schede sentieri Tier A aggiornate | `de87ac2` + `9b8c30e` | `## Coerenza cross-scena` con dettagli stabili |

---

## Versione grafo post-integrazione

```
schema_version: 1.3 → 1.4
graph_version:  1.1.0 → 1.2.0
```

Backup chain creata in `pipeline_narrativa/`:
- `story_graph.json.pre_cornice_mondo.backup.json`
- `story_graph.json.pre_step4_cornici.backup.json`
- `story_graph.json.pre_step5_sentieri.backup.json`
- `story_graph.json.pre_step6_path_details.backup.json`

Migration log entries aggiunte: `cornice_mondo_step1_2`, `cornice_mondo_step4`, `cornice_mondo_step5`, `cornice_mondo_step6`.

---

## Tooling persistente in repo

Anche dopo l'integrazione, gli script restano disponibili (idempotenti, rilanciabili):

```
scripts/cornice_mondo/
├── step1_world_conventions.py
├── step4_cornici.py
├── step5_sentieri_fantasma.py
├── step6_path_details.py
├── _data/
│   ├── refrain_animal_identification.yaml
│   ├── cornici_24.yaml
│   ├── sentieri_fantasma.yaml
│   └── path_details_tierA.yaml
└── _audit/    (riservata audit successivi)
```

Pattern degli script: `--dry-run` di default, `--apply` scrive con backup automatico, log umano.

---

## Pacchetti seguiti da questo

- **Tier B + Tier C dettagli sentieri**: in arrivo. Useranno lo stesso pattern (script idempotenti + YAML deterministici + DOC come reference).
- **Brieffer**: installato lo stesso giorno (`2026-04-30`), legge tra l'altro le `cornice_dettagli` e `path_details` per generare i 12 writing brief.

---

## Riferimenti puntuali

- `SYNC_LOG.md` entry `SYNC-2026-04-30-009` — descrizione cumulativa della giornata.
- `PROJECT_STATE.md` — sezione "Sessione 2026-04-30".
- `CLAUDE.md` §3 — fasi del progetto, sezione "Fase Cornice del Mondo".
- `scripts/cornice_mondo/_data/*.yaml` — i dati deterministici derivati da questi DOC.
