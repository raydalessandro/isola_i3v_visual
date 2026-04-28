# s08 — Migration Notes (Passata 1, carpentiere meccanico)

**Data**: 2026-04-28
**Schema source**: v1.1 → target v1.2
**Output**: `s08_canonical.json` (51 campi, 2 hooks)
**Verifica integrita'**: PASS

## Caso speciale: 6 fix applicati

### 1. REGOLA 0.10 — `season_piena_tarda` → `estate`

`estate_piena_tarda` non in enum. Mapped a `estate` (tarda estate = estate). season_passage lasciato null (l'old_node aveva null e la storia non ha passaggio narrato).

### 2. Hooks dict-non-standard (formato `visual` + `stratification`)

I 2 hook old_node hanno format ricco ma non-standard (chiavi `visual`, `stratification`, `palette`, `frase_precisa_visibile`, `voice_constraint`) invece dei canonical (`time_of_day`, `characters_present`, `focal_action`, etc). Hook_id custom (`scene_hook_crack_caduta_noce`, `scene_hook_gabriel_pozzo_duplice_centro`).

Soluzione (post-s06 string_legacy estesa): nel `_p1_mapping.json#hooks[<hook_id>].hook_dict` ho parsato a mano i 2 hook in formato canonical v1.2 completo. Lo script applica fully-override (estesa la branch `hook_dict` per dict non-standard).

Hook_id rinominati a `s08_h1_signature_crack` + `s08_h2_pozzo_duplice_centro` (preservando il senso strutturale: signature + duplice_centro).

### 3. Locations_secondary: mis_007 (ricorrenza mis_006)

`mercato_del_mezzogiorno_panca_di_pietra` non in catalogo → rinominato a `panca_di_pietra` con role esteso (vecchie_del_mercato_cammeo_silenzioso). Stesso fix di mis_006 in s06.

### 4. Quartieri_attraversati override

I 2 hook coprono solo `centro_villaggio` ma il forno (cornice apertura/chiusura) e' in `fuoco_est`. Lo script deriva quartieri solo da hooks; aggiunto `quartieri_attraversati_override: ["centro_villaggio", "fuoco_est"]` nel mapping. Patch script per supportare override (riusabile).

### 5. Debts schema canonical (PRIMA STORIA SAGA con debt_vero_dict)

S08 e' la prima storia con `debts_opened_keep` e `debts_closed_keep` non vuoti nel precomputed_context. 6 debt_vero_dict opened + 4 closed.

**Trasformazioni applicate** (campi old → canonical schema debt_entry):
- `target` → `target_story`
- `description` → `note`
- `close_mechanism` → `close_mode`
- `rilievo`: enum schema = ['alto','medio','basso']. Old aveva 'altissimo' (1 occ.) e 'medio_alto' (2 occ.): mappato entrambi a 'alto'.
- Aggiunto `origin_story` (richiesto deducibile da debt_id pattern).

**Pattern `debt_id`**: `^debt_s\d{2}(_s\d{2})*_to_s\d{2}(_s\d{2})*_[a-z0-9_]+$`. Tutti i 6 opened matchano. 3 dei 4 closed NON matchavano (mancava `_to_sNN`):

| id originale | id retrofitted | origin inferita |
|---|---|---|
| `debt_s08_secondo_bloom_nodo_marinaro` | `debt_s05_to_s08_nodo_marinaro_secondo_bloom` | s05 (semina nodo marinaro) |
| `debt_s08_seed_vecchie_indicare_in_silenzio_primo_bloom_cammeo` | `debt_s06_to_s08_vecchie_indicare_in_silenzio_primo_bloom_cammeo` | s06 (semina firma gestuale) |
| `debt_s08_pattern_a_continuazione_parte_s08` | `debt_s05_to_s08_pattern_a_continuazione_parte` | s05 (prima semina formale Pattern A) |

### 6. Callbacks `to_story` (REGOLA 0.7)

6 callbacks tutti senza `to_story`. Script ha derivato `to_story=s08`.

## Auto-derivati popolati

- `cycle: C`, `attribute_dominant: cambiare`, `block_position: centro_blocco_c`
- `season: estate` (rimappato), `season_passage: null`
- `wind_active: vento_mulinello`
- `pattern_a_active: bloomed` (BLOOM PIENO, seconda scena attiva post-S7)
- `night_scene: true` (PRIMA NOTTE VERA SAGA)
- `when_water_trembles: true` (PRIMA MENZIONE SAGA, 1 di 2)
- `narrator_address: false`, `paronomastico_used: false`, `narrator_meta_voice: false`
- `onomatopee_firma: ["TOK-TOK-TOK", "STRAPP"]` (entrambi ricorrenti, no nuovi)
- `quartieri_attraversati: ["centro_villaggio", "fuoco_est"]` (override mapping)
- `oggetti_simbolo_presenti: []`
- `personaggi_vincoli_attivi`: 4 (memolo + nodo + fiamma + stria)
- `fear_touched`: gabriel (precursore "fratelli_crescono_diversi")

## Misalignments rilevati

- **mis_007**: ricorrenza mis_006 (`mercato_del_mezzogiorno_panca_di_pietra`). Risolto in P1 con stesso fix.

## Stato: VIA LIBERA P2 (gia' eseguito)

2 provvisori P2 (entrambi A high). Numero basso ma alta densita' qualitativa: i 2 hook sono signature/threshold canonical entrambi snodo della storia (CRACK Pattern A bloom + DUPLICE_CENTRO inversione ruoli).

## Aggiornamento post-review Ray (FLAG voice fields dispersi → REGOLA 0.11)

Review Ray ha rilevato che il grafo originale s08 aveva voice tracking duplicato sparso:
- `chars[3] memolo`: `key_phrase_spoken` + `key_phrase_notes` + `frase_precisa_used: true`
- `chars[7] liu`: `key_phrase_spoken` (lore-hook, non frase-chiave) + `key_phrase_notes` + `timing`
- `chars[4] nodo`: `distinct_from_sNN` (campo non-schema, REGOLA 7 esistente)
- 5 chars: `key_action` (singolare, REGOLA 7 esistente)
- `hook[1]`: `frase_precisa_visibile` + `voice_constraint` (campi non-schema, schema additionalProperties: false)

Diagnosi: schema v1.2 e' completo e corretto. Non e' bug schema, e' bug grafo originale.

### Fix applicati (REGOLA 0.11 nuova + REGOLA 7 estesa)

**Top-level (consolidamento)**:
- `key_phrase_indicative` ora popolato: "L'albero ha aspettato che nessuno fosse sotto." (era null)
- `key_phrase_attributed_to`: "memolo" (terzo caso saga dopo s03/rovo + s06/memolo)
- `key_phrase_notes` aggiornato: spiega consolidamento + vincolo Bible §4.7 + chiarisce sigillo del narratore in chiusura per immagine

**characters_in_scene** (script automatico):
- `key_action` → `key_actions` (lista, 5 chars)
- `distinct_from_sNN` → `distinct_from_other_story` (nodo)
- chars[3] memolo: `key_phrase_spoken` + `key_phrase_notes` + `frase_precisa_used` consolidati al top-level e droppati dal char
- chars[7] liu: `key_phrase_spoken` + `key_phrase_notes` + `timing` assorbiti in `note` del char con prefissi descrittivi (lore-hook, non key_phrase saga)

**scene_hooks** (script automatico via `filter_scene_hook_fields`):
- hook[1] `frase_precisa_visibile` + `voice_constraint` → assorbiti in `notes` con prefissi

### Patch script `migrate_p1.py`
- `CHARACTER_IN_SCENE_ALLOWED` set + `SCENE_HOOK_ALLOWED` set con campi schema canonici
- `normalize_characters_in_scene()` esteso: key_action singolare → lista, filter campi non-schema in `note`
- `filter_scene_hook_fields()` nuovo: filter campi non-schema in `notes`
- Mapping options nuovi: `key_phrase_indicative_override`, `key_phrase_notes_override` (oltre a `key_phrase_attributed_to` gia' esistente)

### Patch MIGRATION_PROMPT
REGOLA 0.11 (`voice_fields_consolidation`) aggiunta con procedura completa per characters + hooks. Nota per s10: stessa regola si applica.

### Risultato

`s08_canonical.json` rigenerato: 52 campi (era 51, +key_phrase_attributed_to). PASS verify. Regression test s01-s07: PASS (nessuna regressione).
