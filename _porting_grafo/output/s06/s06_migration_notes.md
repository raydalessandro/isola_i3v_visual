# s06 — Migration Notes (Passata 1, carpentiere meccanico)

**Data**: 2026-04-28
**Schema source**: v1.1 (in `s06_input.old_node`)
**Schema target**: v1.2 (`story_graph_schema_canonical_v1_2.json`)
**Output**: `s06_canonical.json` (51 campi top-level, 8 hooks)
**Verifica integrita'**: PASS (`verify_output_integrity.py`)
**Esecuzione**: P1 via script `migrate_p1.py s06`. **Caso speciale**: tutti gli hook in formato string_legacy (REGOLA 3) parsati a mano in `_p1_mapping.json#hook_dict`.

## File prodotti

`s06_canonical.json`, `s06_migration_notes.md`, `s06_catalog_proposals.md`, `_p1_mapping.json`, `s06_provisional.json`.

## Trasformazioni applicate

### REGOLA 0.5 — `attribute_dominant: connettere_sottile` → `connettere`

Decisione Ray (anticipata): **mappare a `connettere`** + nota in migration_notes (NON in structural_notes). La sfumatura "sottile" e' qualifica narrativa, non estensione enum chiuso v1.2 `["distinguere","connettere","cambiare","sigillo"]`. Il blocco B chiude con tre forme di connettere completate:
- s04: connettere in ascolto (radici sotterraneo, CANALE_VIBRAZIONE)
- s05: connettere in azione fisica (ponte di rami)
- **s06: connettere come cura muta della rete (giro multi-quartiere + capire-e-tirarsi-indietro)**

La sottigliezza di s06 sta nel "sentire quando farsi da parte" — capire senza avere, restituire senza spiegare. Non serve enum dedicato: la profondita' vive in structural_notes ("CHIUSURA_BLOCCO_B_CONNETTERE_COMPIUTO") + nelle azioni dei personaggi.

### REGOLA 0.9 — `block_position` normalizzato

`chiusura_blocco_b_connessione_come_cura_della_rete` → **`chiusura_blocco_b`**. Suffisso "connessione_come_cura_della_rete" preservato in structural_notes dell'old_node (gia' presente come "CHIUSURA_BLOCCO_B_CONNETTERE_COMPIUTO. ...connettere come cura muta della rete...").

### REGOLA 0.10 — `season` normalizzato (post-s06, prima applicazione)

`passaggio_primavera_estate` → **`season: primavera`** (storia inizia in primavera, transito verso estate). `season_passage` preservato dall'old_node: "prime_giornate_calde_sole_piu_alto_finestre_che_si_aprono_primi_tigli_in_fiore". REGOLA 0.10 introdotta nel MIGRATION_PROMPT, lo script gestisce automaticamente s07-s10 con stessa logica.

### REGOLA 3 — Hooks string_legacy

L'old_node ha `scene_hooks` come 8 stringhe narrative descrittive (non dict). Parsate a mano in P0 in `_p1_mapping.json#hooks[hid].hook_dict` con campi canonici v1.2 completi. Lo script:
- Aggiunge `FONTE_LEGACY: <stringa originale>` come prima entry di `elements` (tracciabilita').
- Lascia `notes: null` (P2 popola narrativamente).

| hook_id | id catalogo | quadrant |
|---|---|---|
| s06_h1 | `scuola_stria` | `centro_villaggio` |
| s06_h2 | `forno` | `fuoco_est` |
| s06_h3 | `casa_salvia` | `terra_ovest` |
| s06_h4 | `casa_zolla` | `terra_ovest` |
| s06_h5 | `panca_di_pietra` | `centro_villaggio` |
| s06_h6_signature | `cespuglio_dietro_albero_vecchio` | `centro_villaggio` |
| s06_h7 | `casa_memolo_cortile` | `centro_villaggio` |
| s06_h8 | `casa_memolo_cortile` | `centro_villaggio` |

PRIMO_GIRO_COMPLETO_QUATTRO_QUARTIERI saga (escluso aria_nord = Pascoli, "troppo lontano per Memolo"). 3 quartieri attraversati: `centro_villaggio` + `fuoco_est` + `terra_ovest`.

### REGOLA 0.8 — `key_phrase_attributed_to: "memolo"`

L'old_node ha `key_phrase_indicative: null` MA voice_notes_essential dichiara esplicito FRASE_PRECISA_MEMOLO_UNA: "Le cose che si perdono non si perdono. Si nascondono dove non sai cercare." structural_notes 'MECCANICA_ISTITUITA_MEMOLO_FRASE_PRECISA' istituita qui. Caso simile a s03 (Rovo).

Mapping aggiunto: `key_phrase_attributed_to: "memolo"` promosso al canonical via `_p1_mapping.json`. Provvisorio P2 propone il valore: `key_phrase_indicative` come categoria A high.

### Callbacks `to_story` (REGOLA 0.7)

5 callbacks tutti senza `to_story`. Script ha derivato `to_story=s06`:
- cb_s06_001 (s05: bru menzione offscreen + noah intasca cornetto)
- cb_s06_002 (s04: ambiente calendario stagionale, salvia pianta diversa)
- cb_s06_003 (s01: voce ricorrente fiamma modalita' chiacchiera)
- cb_s06_004 (s02: gesto ricorrente stria archetipo rilancia)
- cb_s06_005 (s02: chiusura debt offscreen messaggio pastori)

### Filter `oggetti_simbolo_presenti` (REGOLA 0.6)

`recurring_visual_objects: null` (non `[]`). Script gestisce con fallback `[]`. Canonical: `oggetti_simbolo_presenti: []`. La sciarpa_memolo (canonica), cornetto, scatoletta_dente_da_latte appaiono nel testo ma non sono tracked come recurring nel grafo (dettaglio non bloccante).

### Debt triage (REGOLA 0ter)

5 debts_opened raw + ? debts_closed raw, tutti seed_refs (precomputed_context: archived_seed_refs=3, debts_opened_keep=[]). Canonical: `debts_opened: []`, `debts_closed: []`. Tracking via seeds (2 planted + 0 bloomed_here + 1 maturing_here + 2 picked_up).

## Auto-derivati popolati

- `cycle: B`, `attribute_dominant: connettere` (rimappato), `block_position: chiusura_blocco_b` (rimappato)
- `season: primavera` (rimappato), `season_passage: "prime_giornate_calde..."` (preservato)
- `pattern_a_active: seminato` (continua da s05 — PATTERN_A_DUE_IMMAGINI: cornetto portante, dente eco)
- `night_scene: false`, `when_water_trembles: false`
- `narrator_address: false` (in s04 era true; quota saga preservata)
- `paronomastico_used: true` (PARONOMASTICO_FISICO_MEMOLO leggero, primo della saga)
- `onomatopee_firma: []` (TOK-TOK-TOK di s05 non si ripresenta)
- `quartieri_attraversati: ["centro_villaggio", "fuoco_est", "terra_ovest"]`
- `oggetti_simbolo_presenti: []` (recurring null)
- `key_phrase_attributed_to: "memolo"` (promosso via mapping)
- `personaggi_vincoli_attivi`: 6 personaggi con vincoli (memolo + pun + stria + fiamma + salvia + zolla)
- `fear_touched`: assente (Pun riconosce dente, NON e' paura di un fratello)

## Misalignments rilevati

- **mis_006**: `vecchie_del_mercato` (grafo characters_in_scene) vs `mercato_del_mezzogiorno` (catalogo personaggio collettivo). Le vecchie sono SOTTOGRUPPO del mercato. Severity bassa, status open. P1 ha preservato l'id del grafo nel canonical (decisione conservativa).

## Aggiornamento post-review Ray (3 FLAG fix)

Review Ray ha rilevato 3 fix di uniformazione (decisione: 'fai quello che non rompe il grafo, uniforma'):

### FLAG 1 — `vecchie_del_mercato` → `mercato_del_mezzogiorno`
characters_in_scene[*].id rinominato. Sfumatura "vecchie sedute sulla panca" preservata in narrative_weight + focal_action di h5. Query interrogabile, niente proliferazione id.

### FLAG 2 — `mercato_del_mezzogiorno_panca_di_pietra` → `panca_di_pietra`
locations_secondary[4].id rinominato. role esteso a `tappa_quattro_giro_vecchie_indicano_silenzio_firma_gestuale_istituita_al_mercato_del_mezzogiorno | <role_originale>` per preservare contesto narrativo.

### FLAG 3 — `tutta_isola_quattro_quartieri_attraversati` → `centro_villaggio`
location_primary.id sostituito (id grafo originale era semantico, non in catalogo). Apertura aula scuola_stria + chiusura cortile_memolo entrambi quartiere centro. Info giro completo 4 quartieri preservata in `location_primary.note` come prefisso "FIX_RAY_REVIEW: ...".

### Implementazione

3 nuove funzionalita' in `migrate_p1.py`:
- `location_primary_override` (mapping): sostituisce id, preserva note storica.
- `locations_secondary_id_renames` + `_role_extras` (mapping): rinomina id + estende role.
- `characters_id_renames` (mapping): rinomina id legacy a id catalogo.

Pattern riusabile per casi simili in s07-s12. mis_006 → resolved.

`verify_output_integrity.py` post-fix: PASS. Regression test s01-s05: PASS.

## Stato: VIA LIBERA P2 (gia' eseguito)

9 provvisori (3A + 4B + 2C). I 5 `no_inference_fields` restano `null`.

## Note tecniche

- Idempotenza: rilanciando script risultato identico.
- Quartiere primario: tutta_isola_quattro_quartieri_attraversati (location_primary id) — caso unico saga.
