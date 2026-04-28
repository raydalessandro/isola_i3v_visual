# s02 — Migration Notes (Passata 1, carpentiere meccanico)

**Data**: 2026-04-28
**Schema source**: v1.1 (in `s02_input.old_node`)
**Schema target**: v1.2 (`story_graph_schema_canonical_v1_2.json`)
**Output**: `s02_canonical.json` (51 campi top-level, 5 hooks)
**Verifica integrita'**: PASS (`verify_output_integrity.py`)
**Esecuzione**: P1 manuale via script `_porting_grafo/scripts/migrate_p1.py s02`. Sub-agente non usato (3/3 timeout in s01-s02). Approccio scriptato: idempotente, riproducibile, niente Write giganti.

## File prodotti

- `s02_canonical.json` — nodo canonico v1.2.
- `s02_migration_notes.md` — questo file.
- `_p1_mapping.json` — decisioni manuali P0 (hook resolution, quadrant whitelist, vincoli personaggi).
- `_porting_grafo/scripts/migrate_p1.py` — script generico di P1 per s02-s12 (parametrico su story_id).

## Trasformazioni applicate

### Rinomine campi (uniformi su tutti i 5 hook)

- `palette_local` → `palette`
- `location_precise` → `location` (poi risolto a oggetto, vedi sotto)

### Assorbimenti hook (campo originale → nuovo campo)

- `time_of_day` → `moment` (su tutti i 5 hook)

### Aggiunte di campi obbligatori v1.2 (con default)

- `elements: []` su tutti i 5 hook (mancante nei vecchi)
- `notes: null` su tutti i 5 hook (mancante nei vecchi, sara' popolato da P2)
- `onomatopee: []` su tutti i 5 hook (mancante nei vecchi)

### Risoluzione `location` legacy → oggetto canonico v1.2

I 5 `location_precise` legacy sono stati risolti a oggetti `{id, qualifier, legacy_string}` con `id` vincolato al catalogo (mapping da P0):

| hook_id | id (catalogo) | qualifier | legacy_string |
|---|---|---|---|
| s02_h1 | `scuola_stria` | `cortile_o_margine_pascoli` | `scuola_stria_cortile_o_margine_pascoli` |
| s02_h2 | `pascoli_alti` | `sentiero_in_salita` | `sentiero_in_salita_verso_pascoli_alti` |
| s02_h3_signature | `pozza_abbeveratoio_pastori` | `ghiacciata_con_velo_d_acqua_sgelato` | `pozza_ghiacciata_con_velo_d_acqua_sgelato_in_superficie` |
| s02_h4 | `pozza_abbeveratoio_pastori` | `dopo_il_gesto_di_noah` | `pozza_dopo_il_gesto_di_noah` |
| s02_h5 | `pascoli_alti` | `sentiero_del_ritorno` | `sentiero_del_ritorno_dai_pastori` |

**Guardrail `locations_must_exist`**: PASS — tutti i 3 ID location risolti (`scuola_stria`, `pascoli_alti`, `pozza_abbeveratoio_pastori`) esistono in `catalogo_web/data/entities.json`. Nota: `pozza_abbeveratoio_pastori` aggiunto al catalogo durante P0 OPZIONE A (2026-04-28, commit `9c930db`), risolvendo `mis_002`.

### Rinomina simboli enum legacy v1.1 → canonical v1.2 (REGOLA 0.5)

| campo | valore old_node (v1.1) | valore canonical (v1.2) |
|---|---|---|
| `attribute_dominant` | `delta` | `distinguere` |

Coerente con cycle A (centro_blocco_a, Gabriel-distinguere). REGOLA 0.5 patchata in `MIGRATION_PROMPT_FASE_E.md` post-s01: lo script `migrate_p1.py` applica il mapping automaticamente.

### Quadrant whitelist (REGOLA 0.3)

Mapping applicato a 3 dei 5 hook (quadrant non in whitelist):

| hook_id | quadrant old_node | quadrant canonical | nota |
|---|---|---|---|
| s02_h1 | `centro_villaggio_o_via_che_sale` | `centro_villaggio` | scuola_stria.quartiere=centro nel catalogo; scelto centro_villaggio (whitelist). |
| s02_h3_signature | `aria_nord_pascoli` | `aria_nord` | suffisso `_pascoli` non in whitelist; mappato a aria_nord. |
| s02_h4 | `aria_nord_pascoli` | `aria_nord` | stesso. |

Hook s02_h2 e s02_h5 avevano gia' `aria_nord` (whitelist). Decisione documentata in `_p1_mapping.json#hooks[hid]._quadrant_note`.

### Debt triage (REGOLA 0ter)

L'`old_node` aveva 4 `debts_opened` e 1 `debts_closed`. Tutti classificati come `seed_ref` in `precomputed_context.debt_classification.archived_seed_refs`:

**Archived seed_refs (NON entrano nel canonical):**
- `s11_paura_elias_bloom_accettazione_via_vecchie` → ref a `seed_paura_elias_piccolo`
- `s04_s05_s06_s09_paura_elias_maturing_micro_sguardi` → ref a `seed_paura_elias_piccolo`
- `s06_s09_stria_vede_prima_maturing` → ref a `seed_stria_vede_prima`
- `s11_stria_vede_prima_bloom_quattro_coni_a_elias` → ref a `seed_stria_vede_prima`
- `s01_bastoncino_noah_cade_e_diventa_oggetto_fantasma` → ref a `seed_s01_bastoncino_noah` (era debts_closed)

Canonical: `debts_opened: []`, `debts_closed: []`. La storia narrativa di questi seed-ref e' tracciata via `seeds_planted/picked_up/maturing_here/bloomed_here` e `callbacks_made` (entrambi popolati nel canonical).

## Campi lasciati `null` per Passata 2 (provvisori narrativi)

Totale: **8 campi** (popolati da P2 con valori provvisori motivati):

- `season_passage` (top)
- `key_phrase_indicative` (top)
- `visual_anchors.scene_hooks[0].notes` (s02_h1)
- `visual_anchors.scene_hooks[1].notes` (s02_h2)
- `visual_anchors.scene_hooks[2].notes` (s02_h3_signature)
- `visual_anchors.scene_hooks[3].notes` (s02_h4)
- `visual_anchors.scene_hooks[4].notes` (s02_h5)

Inoltre, **5 `wind_visible`** restano `null` per 4/5 hook (s02_h4 ha gia' valore dal vecchio: `vento_taglio_folata_cerchi_argentei`; gli altri 4 sono null e potrebbero ricevere un provvisorio in P2 se motivato dal vento_active = vento_taglio).

## Campi lasciati `null` per fase C/D (no_inference_fields, REGOLA 0.2)

Totale: **5 campi top-level** (NON deducibili automaticamente, decisione autoriale Ray):

- `entry_point_type` (enum A-F, Carta Voce §2.1)
- `closure_type` (enum integer 1-7, Carta Voce §2.3)
- `register` (enum basso/medio/alto, Carta Voce §2.4)
- `estimated_length` (integer 800-1200)
- `descriptive_pauses_count` (integer 0-2)

## Decisioni di triage / ambiguita' risolute in P1

- **`personaggi_vincoli_attivi`**: solo `stria` ha vincoli individuali in `character_constraints.json` tra i 4 character_in_scene di s02 (gabriel/elias/noah non hanno vincoli specifici nel catalogo). Fiamma non e' in scena, quindi non inclusa. `active_constraints_touched` cita `detti_fiamma_esclusivi_qui_non_presente` come constraint by-design da rispettare (Fiamma assente).
- **`oggetti_simbolo_presenti`**: derivato da `visual_anchors.recurring_visual_objects` = `["scialle_stria", "bastoncino_noah_s1"]`.
- **`quartieri_attraversati`**: derivato dai quadrant degli hook (distinct, ordine apparizione) = `["centro_villaggio", "aria_nord"]`.
- **`location_primary.note`**: accorpa `_note` originale + info su `specific_points` (`pozza_abbeveratoio_pastori`) per non perdere il dato strutturato.

## Misalignments rilevati durante P1

Nessuno nuovo. Il misalignment `mis_002` (P0) e' gia' resolved (pozza aggiunta al catalogo in OPZIONE A).

## Note tecniche

- **Idempotenza**: nodo canonico deterministico rispetto a input + mapping. Rilanciando `migrate_p1.py s02` il risultato e' identico (testato).
- **Quartiere primario**: derivato da `quadrant_assignment.json` per `pascoli_alti` → `aria_nord`.
- **Auto-derivati popolati**: `cycle: A`, `attribute_dominant: distinguere` (rimappato), `pattern_a_active: pre_eco`, `night_scene: false`, `when_water_trembles: false`. Tutti i 4 flag quote_tracker = false.
- **Script P1**: `_porting_grafo/scripts/migrate_p1.py` (parametrico, applica REGOLA 0.5 + rinomine + hook resolution da `_p1_mapping.json`). Riusabile per s03-s12.

## Aggiornamento post-review Ray (FLAG 1 + FLAG 2)

Review di Ray del 2026-04-28 (post-P2) ha rilevato 2 bug nello script `migrate_p1.py`. Entrambi corretti, script aggiornato, s02_canonical.json rigenerato e ri-verificato (PASS). Patch al MIGRATION_PROMPT applicate per evitare ricaduta su s03-s12.

### FLAG 1 — `to_story` mancante nei `callbacks_made[*]` (severity media)

**Bug**: schema v1.2 di `callback_entry` richiede 4 campi (`callback_id`, `from_story`, `to_story`, `type`). Lo script copiava i callbacks dell'old_node senza derivare `to_story`. `verify_output_integrity.py` ha PASSato comunque (lo script di verify non valida lo schema callback per intero).

**Fix script** (`migrate_p1.py#normalize_callbacks`): per ogni callback:
- Se ha `to_story`: invariato.
- Se ha `registered_in_story` ma non `to_story`: copia `registered_in_story` → `to_story`.
- Se manca entrambi: deriva `to_story` = `story_id` corrente (il callback e' fatto IN questa storia).

**Fix retroattivo s02**: i 2 callbacks_made hanno ora `to_story: "s02"`.

**Patch MIGRATION_PROMPT**: nuova **REGOLA 0.7** (`callbacks_to_story_must_be_present: true`).

### FLAG 2 — `bastoncino_noah_s1` in `oggetti_simbolo_presenti` (severity bassa)

**Bug**: lo script copiava pari-pari `recurring_visual_objects` come `oggetti_simbolo_presenti`. Concettualmente sbagliato:
- `recurring_visual_objects` (grafo legacy): qualsiasi oggetto narrativamente ricorrente (incluso oggetti-firma personaggio).
- `oggetti_simbolo_presenti` (canonical v1.2): RISTRETTO ai 13 oggetti-simbolo saga (`famiglia=oggetto` nel catalogo).

`bastoncino_noah_s1` e' oggetto-firma personaggio (gesto-firma di Noah che raccoglie), tracciato in `seed_noah_raccoglie_oggetti` + `callbacks_made` + `structural_notes`. Per design NON entra in `oggetti_simbolo_presenti`.

**Fix script** (`migrate_p1.py#filter_oggetti_simbolo` + `load_canonical_oggetti`): legge i 13 oggetti canonici dal catalogo (`famiglia=oggetto`) e filtra `recurring_visual_objects` mantenendo solo quelli. Stampa a stdout gli ID droppati per gestione manuale del misalignment.

**Fix retroattivo s02**: `oggetti_simbolo_presenti = ["scialle_stria"]` (era `["scialle_stria", "bastoncino_noah_s1"]`).

**Misalignment registrato**: `mis_003` in `_canon_misalignments.json` (severity bassa, status resolved). Il tracking narrativo dell'oggetto-firma resta in `seeds_planted/picked_up` + `callbacks_made` + `structural_notes`.

**Patch MIGRATION_PROMPT**: nuova **REGOLA 0.6** (`oggetti_simbolo_presenti_must_be_canonical: true`) + chiarimento §8.2 con la lista esplicita dei 13 oggetti canonici.

### Verifica post-fix

```
$ python3 _porting_grafo/scripts/migrate_p1.py s02
Wrote: s02_canonical.json
Top-level fields: 51
Hooks: 5
attribute_dominant: distinguere
callbacks_made: 2 (to_story derivato dove mancante)
oggetti_simbolo_presenti (canonici): ['scialle_stria']
  WARN: dropped: ['bastoncino_noah_s1'] -> mis_003

$ python3 verify_output_integrity.py s02_canonical.json
[PASS]
```

## Stato: VIA LIBERA P2

Output P1 pronto per Passata 2 (co-autore consultivo). P2 popolera' i 7 provvisori legittimi (2 top + 5 hook notes), aggiornera' `_provisional_state.json` e `_canon_misalignments.json` (rolling files), e produrra' `s02_provisional.json`. I 5 `no_inference_fields` restano `null` (decisione Ray fase C/D).

## Output di s02: stato file

Dopo P0+P1 (e prima di P2):

1. `s02_catalog_proposals.md` (P0) ✓
2. `s02_canonical.json` (P1) ✓ (questo passaggio)
3. `s02_migration_notes.md` (P1) ✓ (questo file)
4. `_p1_mapping.json` (decisioni P0 manuali) ✓
5. `s02_provisional.json` (P2) — ancora da produrre
6. (rolling) `_provisional_state.json` aggiornato (P2) — ancora
7. (rolling) `_canon_misalignments.json` (gia' aggiornato in P0 con mis_002 resolved) ✓
