# s04 — Migration Notes (Passata 1, carpentiere meccanico)

**Data**: 2026-04-28
**Schema source**: v1.1 (in `s04_input.old_node`)
**Schema target**: v1.2 (`story_graph_schema_canonical_v1_2.json`)
**Output**: `s04_canonical.json` (51 campi top-level, 7 hooks)
**Verifica integrita'**: PASS (`verify_output_integrity.py`)
**Esecuzione**: P1 via script `migrate_p1.py s04`. Tutte le REGOLE applicate automaticamente.

## File prodotti

- `s04_canonical.json`, `s04_migration_notes.md` (questo), `s04_catalog_proposals.md`, `_p1_mapping.json`, `s04_provisional.json`.

## Trasformazioni applicate

### Rinomine simboli enum (REGOLA 0.5)

Nessuna: `attribute_dominant: connettere` e' gia' canonico (cycle B).

### block_position pattern (REGOLA 0.9)

Nessuna normalizzazione: `apertura_blocco_b` e' gia' canonico.

### Risoluzione `location` legacy → oggetto canonico v1.2

Tutti i 7 hook avevano `location_precise: <margine|interno>_foresta_*`. Mappati a `foresta_intrecciata` con qualifier specifico:

| hook_id | id catalogo | qualifier |
|---|---|---|
| s04_h1 | `foresta_intrecciata` | `margine_lato_orti` |
| s04_h2 | `foresta_intrecciata` | `interno_primo_tratto_oltre_soglia_salvia` |
| s04_h3_signature | `foresta_intrecciata` | `interno_radice_esposta_grande_albero` |
| s04_h4 | `foresta_intrecciata` | `interno_tra_radici_grande_albero` |
| s04_h5 | `foresta_intrecciata` | `interno_punto_di_ritrovamento` |
| s04_h6 | `foresta_intrecciata` | `interno_arrivo_di_rovo` |
| s04_h7 | `foresta_intrecciata` | `margine_ritorno_da_salvia` |

`locations_must_exist` PASS: foresta_intrecciata + orti_del_cerchio + casa_salvia tutti nel catalogo.

### Quadrant whitelist (REGOLA 0.3)

Tutti i 7 hook gia' `terra_ovest` ✓ whitelist.

### Callbacks `to_story` (REGOLA 0.7)

5 callbacks nell'old_node, tutti senza `to_story`. Script ha derivato `to_story=s04` per tutti:
- cb_s04_001 (gesto trasferito da s01: fermarsi → pensiamo)
- cb_s04_002 (frase eco diretta da s01: aspettiamo → pensiamo)
- cb_s04_003 (bloom sonoro da s03: cantilena coltivatori sommessa → piena)
- cb_s04_004 (rovo registro diverso da s03: guardiano → abitante)
- cb_s04_005 (bru sviluppo da s03: intravisto → presenza concreta)

### Filter `oggetti_simbolo_presenti` (REGOLA 0.6)

Input `recurring_visual_objects` = `["cesto_salvia", "bandana_rovo"]`. Entrambi nei 13 oggetti canonici saga → kept. Nessun drop, nessun nuovo misalignment.

### Debt triage (REGOLA 0ter)

8 `debts_opened` raw + 3 `debts_closed` raw, tutti seed_refs (precomputed_context: archived_seed_refs=11, debts_opened_keep=[]). Canonical: `debts_opened: []`, `debts_closed: []`. Tracciamento via seeds (3 bloomed_here + 3 maturing_here + 4 planted + 7 picked_up).

### Auto-derivati popolati

- `cycle: B` (apertura blocco B, ciclo connettere)
- `attribute_dominant: connettere`
- `pattern_a_active: none` (semina vera s06)
- `night_scene: false`, `when_water_trembles: false`
- `narrator_address: true` (PRIMO della saga, 1 di <=6)
- `paronomastico_used: false`, `narrator_meta_voice: false`, `grunto_memory_fragment: false`
- `onomatopee_firma: ["TUM-tum-TUM (fratelli)", "TUM-tum (coltivatori)"]`
- `quartieri_attraversati: ["terra_ovest"]`
- `oggetti_simbolo_presenti: ["cesto_salvia", "bandana_rovo"]`
- `personaggi_vincoli_attivi`: salvia (3 vincoli) + rovo (4) + bru (4)

## Campi lasciati `null` per Passata 2

8 campi (popolati da P2): `season_passage` (top), `key_phrase_indicative` (top), 7 hook `notes`. Inoltre `wind_visible` resta null sui 7 hook (nessuno ha valore esplicito nell'old_node, e nessuna inferenza forte: P2 lo lascia null per sicurezza).

## Campi lasciati `null` per fase C/D (no_inference_fields, REGOLA 0.2)

`entry_point_type`, `closure_type`, `register`, `estimated_length`, `descriptive_pauses_count`. Decisione autoriale Ray.

`key_phrase_attributed_to`: lasciato assente nel canonical (REGOLA 0.8) perche' `key_phrase_indicative` e' `null`. Sara' popolato come `"narratore"` quando Ray decide la frase precisa in fase D (sigillo del narratore in chiusura, ADDRESS AL LETTORE primo della saga).

## Decisioni di triage

- **personaggi_vincoli_attivi**: 3 personaggi con vincoli (salvia + rovo + bru). gabriel/elias/noah/coltivatori_del_cerchio nessun vincolo specifico.
- **quartieri_attraversati**: `["terra_ovest"]` (tutti i 7 hook + locations primary/secondary).
- **vento_intreccio**: prima manifestazione del Vento del cycle B in saga.

## Misalignments rilevati

Nessuno. mis_004 (pallone_di_stoffa_cucita) di s03 non si ripresenta in s04.

## Note tecniche

- **Idempotenza**: nodo deterministico, rilanciando `migrate_p1.py s04` risultato identico.
- **Quartiere primario**: `foresta_intrecciata` → `terra_ovest` (terra_ovest gia' confermato in s03, conferma in s04).

## Stato: VIA LIBERA P2 (gia' eseguito)

Output P1 + P2 di s04 pronto. 9 provvisori legittimi (2A + 5B + 2C — distribuzione piu' larga grazie al specchio visivo h3+h4 signature). I 5 `no_inference_fields` restano `null`.

## Output di s04: stato file

1. `s04_catalog_proposals.md` (P0) ✓
2. `s04_canonical.json` (P1) ✓
3. `s04_migration_notes.md` (P1) ✓
4. `_p1_mapping.json` ✓
5. `s04_provisional.json` (P2) ✓
6. (rolling) `_provisional_state.json` aggiornato ✓
7. (rolling) `_canon_misalignments.json`: nessun nuovo misalignment in s04.
