# s05 — Migration Notes (Passata 1, carpentiere meccanico)

**Data**: 2026-04-28
**Schema source**: v1.1 (in `s05_input.old_node`)
**Schema target**: v1.2 (`story_graph_schema_canonical_v1_2.json`)
**Output**: `s05_canonical.json` (51 campi top-level, 8 hooks)
**Verifica integrita'**: PASS (`verify_output_integrity.py`)
**Esecuzione**: P1 via script `migrate_p1.py s05`. Tutte le REGOLE applicate automaticamente.

## File prodotti

`s05_canonical.json`, `s05_migration_notes.md`, `s05_catalog_proposals.md`, `_p1_mapping.json`, `s05_provisional.json`.

## Trasformazioni applicate

### Rinomine simboli enum (REGOLA 0.5)

Nessuna: `attribute_dominant: connettere` gia' canonico.

### block_position pattern (REGOLA 0.9)

Nessuna: `centro_blocco_b` gia' canonico.

### Risoluzione `location` legacy → oggetto canonico v1.2 (con mis_005)

8 hook risolti. Caso speciale **mis_005**: legacy `radura_coi_pini` (grafo) mappato a `radura_dei_pini` (id catalogo) per `s05_h7_radura`. Stessa entita' con preposizione discrepant.

| hook_id | id catalogo | qualifier |
|---|---|---|
| s05_h1 | `foresta_intrecciata` | `cammino_interno_verso_torrente` |
| s05_h2 | `torrente_affluente_foresta` | `punto_vecchio_tronco_portato_via` |
| s05_h3 | `torrente_affluente_foresta` | `posizione_nodo_50m_a_valle_scaletta` |
| s05_h4 | `torrente_affluente_foresta` | `posizione_nodo_corda_tagliata` |
| s05_h5_signature | `torrente_affluente_foresta` | `durante_costruzione_ponte` |
| s05_h6 | `torrente_affluente_foresta` | `ponte_finito_passaggio_elias` |
| s05_h7_radura | **`radura_dei_pini`** | `oltre_torrente_100_150_metri` (mis_005) |
| s05_h8 | `torrente_affluente_foresta` | `ritorno_ponte_ancora_li` |

`locations_must_exist` PASS: torrente_affluente_foresta + foresta_intrecciata + orti_del_cerchio + radura_dei_pini tutti nel catalogo.

### Quadrant whitelist (REGOLA 0.3)

Tutti i 8 hook gia' `terra_ovest` ✓ whitelist.

### Callbacks `to_story` (REGOLA 0.7)

3 callbacks nell'old_node (tutti da s04), nessuno con `to_story`. Script ha derivato `to_story=s05`:
- cb_s05_001 (gesto richiamo: bru indica col mento direzione radura)
- cb_s05_002 (principio fisico esteso: foresta che ha suoi modi)
- cb_s05_003 (personaggio sviluppo agency: bru presenza che custodisce)

### Filter `oggetti_simbolo_presenti` (REGOLA 0.6)

Input `recurring_visual_objects` = `["corda_nodo"]` ✓ canonico → kept. Nessun drop.

### Debt triage (REGOLA 0ter)

8 `debts_opened` raw + 1 `debts_closed` raw, tutti seed_refs (precomputed_context: archived_seed_refs=8, debts_opened_keep=[]). Canonical: `debts_opened: []`, `debts_closed: []`. Tracking via seeds (1 bloomed_here + 2 maturing_here + 5 planted + 3 picked_up).

### Auto-derivati popolati

- `cycle: B`, `attribute_dominant: connettere`
- `pattern_a_active: seminato` (PRIMA SEMINA FORMALE saga, structural PATTERN_A_PRIMA_SEMINA_FORMALE)
- `night_scene: false`, `when_water_trembles: false`
- `narrator_address: false` (in s04 era true, qui non c'e')
- `onomatopee_firma: ["TOK-TOK-TOK"]`
- `quartieri_attraversati: ["terra_ovest"]`
- `oggetti_simbolo_presenti: ["corda_nodo"]`
- `personaggi_vincoli_attivi`: nodo (4 vincoli, prima apparizione) + bru (4 vincoli)

## Campi lasciati `null` per Passata 2

10 campi (popolati da P2 in s05_provisional.json): `season_passage` (top), `key_phrase_indicative` (top), 8 hook `notes`. wind_visible su hook resta null (nessuna inferenza forte oltre h5 dove vento Intreccio gia' descritto in atmosphere/structural).

## Campi lasciati `null` per fase C/D (no_inference_fields)

I 5 standard. `key_phrase_attributed_to`: assente nel canonical (REGOLA 0.8) — popolato come `"narratore"` quando Ray decide la frase in fase D.

## Misalignments rilevati

- **mis_005**: `radura_coi_pini` (grafo) vs `radura_dei_pini` (catalogo). Severity bassa, status open. Mappato in P1, decisione finale post-saga (preferenzialmente confermare nome catalogo e aggiornare grafo nelle storie successive che lo citano).

## Note tecniche

- **Idempotenza**: nodo deterministico, rilanciando script risultato identico.
- **Quartiere primario**: `torrente_affluente_foresta` → `terra_ovest` (cluster terra_ovest che continua da s03/s04).
- **PATTERN A**: prima semina formale, da qui in poi cammina (mai nominato, vive nelle azioni e in 1 inciso narratore max).

## Stato: VIA LIBERA P2 (gia' eseguito)

10 provvisori (4A + 5B + 1C — distribuzione confidence altissima grazie a 4 hook signature/canonical: NODO_PRIMA_APPARIZIONE h3, EREDITA_TECNICA_E_MATERIALE h4, PATTERN_A_PRIMA_SEMINA h5, PONTE_TIENE h8). I 5 `no_inference_fields` restano `null`.
