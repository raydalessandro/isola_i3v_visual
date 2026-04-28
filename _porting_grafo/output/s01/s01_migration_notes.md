# s01 — Migration Notes (Passata 1, carpentiere meccanico)

**Data**: 2026-04-28
**Schema source**: v1.1 (in `s01_input.old_node`)
**Schema target**: v1.2 (`story_graph_schema_canonical_v1_2.json`)
**Output**: `s01_canonical.json` (306 righe, 12.680 byte)
**Verifica integrita'**: PASS (`verify_output_integrity.py`)

## File prodotti

- `s01_canonical.json` — nodo canonico v1.2.
- `s01_migration_notes.md` — questo file.

## Trasformazioni applicate (da `hook_migration_plans`)

### Rinomine campi (uniformi su tutti i 5 hook)

- `palette_local` → `palette`
- `location_precise` → `location` (poi risolto a oggetto, vedi sotto)

### Assorbimenti hook (campo originale → nuovo campo)

- `time_of_day` → `moment` (su tutti i 5 hook)
- `wind_notes` → `notes` (su s01_h2)
- `wind_visual_details` → `wind_visible` (su s01_h3)

### Risoluzione `location` legacy → oggetto canonico v1.2

I 5 `location_precise` legacy sono stati risolti a oggetti `{id, qualifier, legacy_string}` con `id` vincolato al catalogo. Mapping (passato gia' risolto da P0/Ray):

| hook_id | id (catalogo) | qualifier | legacy_string |
|---|---|---|---|
| s01_h1 | `forno` | `interno` | `forno_interno` |
| s01_h2 | `pascoli_alti` | `salita_verso_sentiero_montagne` | `pascoli_alti_salita_verso_sentiero_montagne` |
| s01_h3 | `sentiero_montagne_gemelle` | `mezzacosta_cengia_sul_burrone` | `sentiero_montagne_gemelle_mezzacosta_cengia_sul_burrone` |
| s01_h4_signature | `grotta_grunto` | `cengia_burrone` | `cengia_grotta_grunto_burrone` |
| s01_h5 | `forno` | `interno_ritorno` | `forno_interno_ritorno` |

**Guardrail `locations_must_exist`**: PASS — tutti i 4 ID location risolti esistono in `catalogo_web/data/entities.json`. Nota: `sentiero_montagne_gemelle` e' stato aggiunto al catalogo durante P0 (cartografia v0.6.1, commit `b5b8473`).

## Campi lasciati `null` per Passata 2 (provvisori narrativi)

Totale: **13 campi** (saranno popolati da co-autore in P2 con valori provvisori motivati):

- `season_passage`
- `key_phrase_indicative`
- `entry_point_type`
- `closure_type`
- `register`
- `estimated_length`
- `descriptive_pauses_count`
- `visual_anchors.scene_hooks[0].notes` (s01_h1)
- `visual_anchors.scene_hooks[0].wind_visible` (s01_h1)
- `visual_anchors.scene_hooks[1].wind_visible` (s01_h2)
- `visual_anchors.scene_hooks[2].notes` (s01_h3)
- `visual_anchors.scene_hooks[3].notes` (s01_h4_signature)
- `visual_anchors.scene_hooks[4].notes` (s01_h5)

## Decisioni di triage / ambiguita' risolute in P1

**Nessuna ambiguita' risolta autonomamente da P1.** L'unica potenziale ambiguita' segnalata da P0 (s01_h3: burrone vs montagne_gemelle vs sentiero_pascoli_burrone_diretto) e' stata risolta da Ray prima di P1 con l'arricchimento del catalogo (`sentiero_montagne_gemelle` aggiunto come canonico). Mapping passato a P1 in input.

## Misalignments rilevati durante P1

Nessuno nuovo rispetto a P0. Il misalignment basso `mis_001` (location_attribute, catalog_vs_graph) sara' tracciato in `_canon_misalignments.json` da P2.

## Note tecniche

- **Idempotenza**: il nodo canonico e' deterministico rispetto all'input + mapping. Rilanciando la migrazione il risultato e' lo stesso.
- **Quartiere**: derivato da `quadrant_assignment.json` per il `location_primary` (montagne_gemelle → quartiere aria).
- **Debt triage**: applicato secondo `debt_classification.json`. Lista classificata nei campi `debts_opened` / `debts_closed` del nodo.
- **Auto-derivati popolati**: `cycle: A`, `attribute_dominant: distinguere` (Gabriel protagonista a inizio saga; rimappato dal simbolo legacy v1.1 `delta`, vedi sezione "Aggiornamento post-review Ray").

## Stato: VIA LIBERA P2

Output pronto per Passata 2 (co-autore consultivo). P2 popolera' i 13 campi `null`, aggiornera' `_provisional_state.json` e `_canon_misalignments.json` (rolling files), e produrra' `s01_provisional.json`.

## Aggiornamento post-P2a (correzione metodologica)

Eseguita P2a in 2 micro-task paralleli (top + hooks). Verifica post-merge contro schema v1.2 + `MIGRATION_PROMPT_FASE_E.md` ha rilevato che **5 campi top-level sono `no_inference_fields`** (vietati alla deduzione automatica, richiedono decisione autoriale di Ray in fase C/D):

- `entry_point_type` (enum A-F, Carta Voce §2.1)
- `closure_type` (enum integer 1-7, Carta Voce §2.3)
- `estimated_length` (integer 800-1200)
- `register` (enum basso/medio/alto, Carta Voce §2.4)
- `descriptive_pauses_count` (integer 0-2)

**Canonical e' corretto** (P1 ha rispettato il vincolo: 5 campi `null`). Provvisorio corretto: i 5 valori proposti da P2a-top sono stati spostati in `s01_provisional.json#rejected_no_inference` con motivazione e schema constraint, **NON** entrano nel canonical.

**Provvisori validi P2a:** 8 totali (2 top legittimi + 6 hook), distribuiti come segue:

- **Top-level (2):** `season_passage` (B), `key_phrase_indicative` (B).
- **Hook-level (6):** `s01_h1.notes` (C), `s01_h1.wind_visible` (C), `s01_h2.wind_visible` (C), `s01_h3.notes` (B), `s01_h4_signature.notes` (A), `s01_h5.notes` (C).

I 5 `no_inference_fields` saranno popolati da Ray in **chat dedicata fase C/D** (post-saga o quando deciso).

## Output di P1: 6 file totali per s01 (al netto P0/P2)

Dopo P0+P1+P2 lo stato di s01 nella `_porting_grafo/output/s01/` sara':
1. `s01_catalog_proposals.md` (P0) ✓
2. `s01_canonical.json` (P1) ✓
3. `s01_migration_notes.md` (P1) ✓ (questo file)
4. `s01_provisional.json` (P2) — ancora da produrre
5. (rolling) `_provisional_state.json` aggiornato (P2) — ancora
6. (rolling) `_canon_misalignments.json` aggiornato (P2) — ancora

Tool calls usate da P1 (sub-agente prima del fail API): 28/30. Nota tecnica: il sub-agente e' fallito con `overloaded_error` dopo aver scritto correttamente `s01_canonical.json`. Non ha scritto il file delle migration_notes ne' eseguito `verify_output_integrity.py`. Ray (operatore) ha eseguito la verifica manualmente (PASS) e ha scritto le migration_notes basandosi sull'output prodotto + mapping pre-validato.

## Aggiornamento post-review Ray (correzioni applicate)

Review di Ray del 2026-04-28 ha rilevato 5 problemi/integrazioni:

### 1. `attribute_dominant` rimappato `delta` → `distinguere`

Lo schema v1.2 ha enum chiuso `["distinguere", "connettere", "cambiare", "sigillo"]`. Il sub-agente P1 aveva copiato pari-pari il valore legacy v1.1 `"delta"` dall'`old_node` (`INPUT_NODES/s01_input.json`), senza rimappare. `verify_output_integrity.py` non ha intercettato il bug (lo script non valida enum stringhe libere contro lo schema, valida la struttura). Correzione manuale applicata al canonical, `verify_output_integrity.py` ri-eseguito: **PASS**.

I riferimenti narrativi nei campi liberi del canonical (`narrative_weight: "portante_del_ciclo_delta"` su Gabriel, structural_note `"DELTA_ESTERNO_E_INTERNO"`) sono lasciati intenzionalmente come label metaforiche — non sono enum, sono descrizioni libere usate da Ray. Decisione conservativa: cambio solo il valore enum.

### 2. Confidence aggiunta ai 8 provvisori

Mappatura: `A` → `high` (1 occ.) | `B` → `medium` (3 occ.) | `C` → `low` (4 occ.). Documentata in `s01_provisional.json#confidence_legend`.

### 3. `quote_consumed` popolato in `s01_provisional.json`

Era `{}` (vuoto). Ora replica la struttura gia' presente nel rolling `_provisional_state.json#stories_log[s01].quote_consumed`, con dettaglio per campo + categoria + confidence. Famiglia A (1 entry: `s01_h4_signature.notes`) esplicitata come `confidence: high`.

### 4. Rolling files aggiornati post-correzione

- `_provisional_state.json#stories_log[s01].quote_consumed.dettaglio[*]`: aggiunto campo `confidence`.
- `_provisional_state.json#stories_log[s01].notes`: aggiunta nota correzione attribute_dominant.
- `_canon_misalignments.json`: nessun nuovo misalignment (la correzione attribute_dominant e' un errore di porting, non un disallineamento tra le 3 sorgenti). `mis_001` resta `resolved`.

### 5. Patch al `MIGRATION_PROMPT_FASE_E.md`

Aggiunta REGOLA 0.5 (`enum_symbols_must_be_canonical: true`) con tabella mapping legacy → canonical e procedura obbligatoria pre-write canonical. Mapping documentati:
- `attribute_dominant: delta` → `distinguere` (s01, s02, s03 — ciclo A)
- `attribute_dominant: connettere_sottile` → `connettere` (s06, con nota in structural_notes della storia: la sfumatura "sottile" e' qualifica narrativa, non estensione enum).

### Decisione su s06 (`connettere_sottile`)

L'`old_node` di s06 ha `attribute_dominant: "connettere_sottile"` che NON e' nell'enum v1.2 chiuso. Decisione (autorizzata da Ray): **mappare a `"connettere"` con nota in `structural_notes`** del canonical s06 (es. `"CONNETTERE_SOTTILE_VARIANTE — qualifica narrativa: connessione discreta/sottile"`) e documentare in `s06_migration_notes.md`. Motivazione: lo schema v1.2 e' canonico, l'enum e' chiuso, "sottile" e' una sfumatura narrativa che non giustifica proliferazione di enum values. Decisione presa prima di s06 per non bloccarsi durante la migrazione.

## Stato finale s01: VALIDATO CON RISERVE DOCUMENTATE

S01 e' validato come pilota del flusso Fase E. Riserve documentate:
- 5 `no_inference_fields` restano `null` per decisione autoriale Ray in fase C/D (non blocca il flusso).
- 8 provvisori validi (1 high + 3 medium + 4 low) da rivedere in fase D dedicata.
- `mis_001` risolto (sentiero_montagne_gemelle aggiunto in cartografia v0.6.1).

Pronti per s02 con flusso standardizzato (briefing sub-agenti includera' sempre `MIGRATION_PROMPT_FASE_E.md` aggiornato + Carta Voce + REGOLA 0.5 enum check).
