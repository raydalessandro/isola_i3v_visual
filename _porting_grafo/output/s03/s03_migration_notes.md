# s03 — Migration Notes (Passata 1, carpentiere meccanico)

**Data**: 2026-04-28
**Schema source**: v1.1 (in `s03_input.old_node`)
**Schema target**: v1.2 (`story_graph_schema_canonical_v1_2.json`)
**Output**: `s03_canonical.json` (51 campi top-level, 5 hooks)
**Verifica integrita'**: PASS (`verify_output_integrity.py`)
**Esecuzione**: P1 via script `_porting_grafo/scripts/migrate_p1.py s03` (parametrico, idempotente, REGOLE 0.5/0.6/0.7 applicate automaticamente).

## File prodotti

- `s03_canonical.json` — nodo canonico v1.2.
- `s03_migration_notes.md` — questo file.
- `s03_catalog_proposals.md` — output P0.
- `_p1_mapping.json` — decisioni manuali P0 (hook resolution + personaggi_vincoli + debt triage).

## Trasformazioni applicate

### Rinomine simboli enum legacy v1.1 → canonical v1.2 (REGOLA 0.5)

| campo | valore old_node | valore canonical |
|---|---|---|
| `attribute_dominant` | `delta` | `distinguere` |

Coerente con cycle A (chiusura_blocco_a_passaggio_stagionale).

### Rinomine campi (uniformi su tutti i 5 hook)

- `palette_local` → `palette`
- `location_precise` → `location` (oggetto canonico v1.2)

### Assorbimenti hook

- `time_of_day` → `moment` (su tutti i 5 hook)

### Aggiunte di campi obbligatori v1.2

- `elements: []` su tutti i 5 hook (mancante nei vecchi)
- `notes: null` su tutti i 5 hook (popolato da P2)
- `onomatopee: []` su tutti i 5 hook

### Risoluzione `location` legacy → oggetto canonico v1.2

Tutti i 5 hook avevano `location_precise: margine_foresta_*`. Mappati a `foresta_intrecciata` con qualifier specifico (location_primary._note dichiara: "Margine: confine tra Orti del Cerchio e Foresta Intrecciata. Non dentro la Foresta — i fratelli si fermano prima del margine. Solo Rovo esce."):

| hook_id | id (catalogo) | qualifier | legacy_string |
|---|---|---|---|
| s03_h1 | `foresta_intrecciata` | `margine_orti_campo_gioco` | `margine_foresta_orti_campo_gioco` |
| s03_h2_signature | `foresta_intrecciata` | `margine_calcio_mal_misurato` | `margine_foresta_momento_del_calcio_mal_misurato` |
| s03_h3 | `foresta_intrecciata` | `margine_chiamare_elias` | `margine_foresta_momento_del_chiamare_elias` |
| s03_h4 | `foresta_intrecciata` | `margine_rovo_esce` | `margine_foresta_rovo_esce` |
| s03_h5 | `foresta_intrecciata` | `margine_rovo_si_volta_per_rientrare` | `margine_foresta_rovo_si_volta_per_rientrare` |

**Guardrail `locations_must_exist`**: PASS (foresta_intrecciata + orti_del_cerchio nel catalogo).

### Quadrant whitelist (REGOLA 0.3)

Tutti i 5 hook avevano gia' `quadrant: terra_ovest` ✓ whitelist. Nessuna rinomina.

### Callbacks `to_story` derivation (REGOLA 0.7)

1 callback nell'old_node senza `to_story`:
- `cb_s03_001` (eco strutturale s01 → s03, "fermarsi_come_gesto_attivo"): `to_story` derivato a `s03` dallo script.

### Filter `oggetti_simbolo_presenti` (REGOLA 0.6)

Input `recurring_visual_objects` = `["pallone_di_stoffa_cucita", "bandana_rovo"]`.
Filtro contro 13 oggetti canonici saga:
- `bandana_rovo` ✓ → kept
- `pallone_di_stoffa_cucita` ✗ → dropped

Output `oggetti_simbolo_presenti = ["bandana_rovo"]`. Misalignment registrato: **mis_004** (severity bassa, status `open`, OPZIONE B scelta da Ray: non aggiunto al catalogo per ora, decisione post-saga).

### Debt triage (REGOLA 0ter)

L'`old_node` aveva 7 `debts_opened` raw e 0 `debts_closed`. Tutti classificati come `seed_ref` (precomputed_context.debt_classification.archived_seed_refs=6, debts_opened_keep=[]):

**Archived seed_refs (NON entrano nel canonical):**
- `s04_rovo_bloom_registro_diverso_abitante_foresta` → ref a `seed_rovo_resistenza_che_protegge`
- `s04_bru_maturing_presenza_concreta` → ref a `seed_bru_presenza_che_custodisce`
- `s04_foresta_tempi_modi_bloom_radici` → ref a `seed_foresta_tempi_modi_propri`
- `s05_bru_maturing_compagno_scoperta` → ref a `seed_bru_presenza_che_custodisce`
- `s05_foresta_tempi_modi_bloom_ponte` → ref a `seed_foresta_tempi_modi_propri`
- `s11_bru_bloom_riconosciuto_da_elias` → ref a `seed_bru_presenza_che_custodisce`
- `s11_pallone_ricomparsa_giochi_cuccioli_tentativo` → ref a `seed_pallone_stoffa_cucita`

Canonical: `debts_opened: []`, `debts_closed: []`. Tracciamento via `seeds_planted/picked_up/maturing_here/bloomed_here` + `callbacks_made`.

## Campi lasciati `null` per Passata 2 (provvisori narrativi)

Totale **6 campi** per P2:
- `season_passage` (top)
- `key_phrase_indicative` (top, con caso speciale: vedi sotto)
- `visual_anchors.scene_hooks[*].notes` (5 hook)

**Caso speciale `key_phrase_indicative`**: a differenza di s01/s02 (frase indicativa, sigillo del narratore), s03 ha **frase-chiave esplicita attribuita a personaggio** (Rovo: "Le cose della Foresta hanno il loro orario"). Eccezione giustificata da `key_phrase_notes` + `structural_notes` (FRASE_CHIAVE_A_PERSONAGGIO). Il provvisorio P2 e' **categoria A** (quote letterale dal grafo). Inoltre s03_provisional.json propone `key_phrase_attributed_to: "rovo"` come provvisorio aggiuntivo (campo opzionale schema v1.2, non popolato dallo script).

## Campi lasciati `null` per fase C/D (no_inference_fields, REGOLA 0.2)

Totale **5 campi top-level**: `entry_point_type`, `closure_type`, `register`, `estimated_length`, `descriptive_pauses_count`. Decisione autoriale Ray.

## Decisioni di triage / ambiguita' risolute in P1

- **`personaggi_vincoli_attivi`**: 2 personaggi con vincoli individuali nel catalogo (rovo + bru), entrambi prima apparizione narrativa in s03. gabriel/elias/noah/coltivatori_del_cerchio non hanno vincoli specifici.
- **`oggetti_simbolo_presenti`**: filtrato a `["bandana_rovo"]` (vedi REGOLA 0.6 sopra).
- **`onomatopee_firma`**: `["TUM-tum (coltivatori)"]` da precomputed_context.flags_quote_tracker.
- **`quartieri_attraversati`**: `["terra_ovest"]` (tutti i 5 hook sullo stesso quartiere).
- **`location_primary.note`**: accorpa `_note` originale + info su specific_points (`margine_foresta_intrecciata`, `orti_del_cerchio_confine`).
- **`wind_active`**: `null` (storia senza vento attivo, pausa tra Taglio e Mulinello — vedi structural_note "VENTO_ASSENTE_TEMPO_SOSPESO").
- **`pattern_a_active`**: `none` (Pattern A non ancora seminato in saga; semina vera in s06, scena attiva s07).

## Misalignments rilevati durante P1

- **mis_004**: `pallone_di_stoffa_cucita` non in catalogo. Status `open`, OPZIONE B scelta da Ray (non aggiunto, decisione post-saga). Vedi `_canon_misalignments.json`.

## Note tecniche

- **Idempotenza**: nodo canonico deterministico. Rilanciando `migrate_p1.py s03` il risultato e' identico.
- **Quartiere**: derivato da `quadrant_assignment.json` per `foresta_intrecciata` → `terra_ovest`.
- **Auto-derivati popolati**: `cycle: A`, `attribute_dominant: distinguere` (rimappato), `pattern_a_active: none`, `night_scene: false`, `when_water_trembles: false`, `wind_active: null`. Tutti i 4 flag quote_tracker = false.

## Stato: VIA LIBERA P2 (gia' eseguito)

Output P1 + P2 pronto. P2 ha popolato 7 provvisori legittimi + proposto `key_phrase_attributed_to: "rovo"` come campo opzionale aggiuntivo. I 5 `no_inference_fields` restano `null` (decisione Ray fase C/D).

## Output di s03: stato file

1. `s03_catalog_proposals.md` (P0) ✓
2. `s03_canonical.json` (P1) ✓
3. `s03_migration_notes.md` (P1) ✓ (questo file)
4. `_p1_mapping.json` (decisioni P0 manuali) ✓
5. `s03_provisional.json` (P2) ✓
6. (rolling) `_provisional_state.json` aggiornato (P2) ✓
7. (rolling) `_canon_misalignments.json` aggiornato (mis_004 open) ✓
