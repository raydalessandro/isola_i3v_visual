# s07 — Migration Notes (Passata 1, carpentiere meccanico)

**Data**: 2026-04-28
**Schema source**: v1.1 → target v1.2
**Output**: `s07_canonical.json` (50 campi top-level, 6 hooks)
**Verifica integrita'**: PASS
**Esecuzione**: P1 via script `migrate_p1.py s07`. Tutte le REGOLE applicate automaticamente.

## Trasformazioni applicate

### REGOLA 0.10 — `season` normalizzato

`estate_piena` → **`season: estate`**. season_passage lasciato `null` (old_node null, storia non ha passaggio narrato).

### REGOLA 0.5 + 0.9 — invariati

`attribute_dominant: cambiare` (gia' canonico, cycle C apertura). `block_position: apertura_blocco_c` (gia' canonico).

### Risoluzione `location` (6 hook)

| hook_id | id catalogo | qualifier | quadrant proposto | quadrant legacy |
|---|---|---|---|---|
| s07_h1 | `guado_di_pietre_piatte` | `partenza_mattino_presto_pietre_piatte` | `acqua_nord` | `acqua_nord` |
| s07_h2 | `fiume_che_gira` | `lato_ovest_tratto_accanto_a_foresta_intrecciata` | `terra_ovest` | `terra_ovest_sponda_interna_fiume` |
| s07_h3 | `fiume_che_gira` | `lato_ovest_tratto_accanto_a_orti_del_cerchio` | `terra_ovest` | `terra_ovest_sponda_interna_fiume` |
| s07_h4 | `fiume_che_gira` | `due_massi_che_stringono_letto_meta_percorso` | `perimetro_fiume_che_gira` | `acqua_anello_fluviale_lato_ovest_meta` |
| s07_h5 | `fiume_che_gira` | `lato_ovest_discesa_verso_bocca` | `acqua_sud` | `acqua_sud_ovest_anello_fluviale` |
| s07_h6 | `pontile_bocca` | `arrivo_tramonto_vista_scogliera_est_amo` | `acqua_sud` | `acqua_sud` |

**Quadrant fix manuale** (3 hook con suffissi non whitelist): `terra_ovest_sponda_interna_fiume` → `terra_ovest`; `acqua_anello_fluviale_lato_ovest_meta` → `perimetro_fiume_che_gira`; `acqua_sud_ovest_anello_fluviale` → `acqua_sud`. Decisione documentata in `_p1_mapping.json#hooks[].._quadrant_note`.

### Callbacks `to_story` (REGOLA 0.7)

5 callbacks tutti senza `to_story`. Script ha derivato `to_story=s07`.

### Filter `oggetti_simbolo_presenti` (REGOLA 0.6)

`recurring_visual_objects: null` (script fallback `[]`). Canonical: `oggetti_simbolo_presenti: []`. Zattera, rametti, erba lunga tenace appaiono nel testo ma non sono tracked nel grafo.

### Debt triage (REGOLA 0ter)

Tutti seed_refs (archived_seed_refs=4, debts_opened_keep=[]). Canonical: `debts_opened: []`, `debts_closed: []`.

## Auto-derivati popolati

- `cycle: C`, `attribute_dominant: cambiare`, `block_position: apertura_blocco_c`
- `season: estate` (rimappato), `season_passage: null`
- `wind_active: vento_intreccio` (continua da blocco B)
- `pattern_a_active: attivo` (PRIMA VOLTA in saga: arc none→pre_eco→seminato→**attivo**)
- `night_scene: false`, `when_water_trembles: false`
- `narrator_address: true` (secondo della saga, primo blocco C, primo post-s4)
- `paronomastico_used: false`, `narrator_meta_voice: false`, `grunto_memory_fragment: false`
- `onomatopee_firma: ["STRAPP"]`
- `quartieri_attraversati: ["acqua_nord", "terra_ovest", "perimetro_fiume_che_gira", "acqua_sud"]` (4 quartieri lungo l'anello fluviale)
- `oggetti_simbolo_presenti: []`
- `personaggi_vincoli_attivi`: 3 (bartolo + toba + amo, prime apparizioni narrative)
- `fear_touched`: assente (scena tecnica + Pattern A, non scena di paura fratello)

## Misalignments rilevati

**Nessuno.** s07 e' la prima storia con catalogo perfettamente allineato dal grafo (14/14 entita' canoniche).

## Note tecniche

- Idempotenza: script deterministico, rilanciando risultato identico.
- Pattern A: arc complete saga finora — none(s01-s03) → pre_eco(s02 effimero) → seminato(s05+s06) → **attivo(s07 STRAPP)**. Bloom previsto s08+s11+s12.
- TAGLIO_ASSENTE_PRIMA_VOLTA_SAGA: s07 e' la prima storia senza Vento Taglio in scena. Eco silenziosa del passaggio climatico a regime estivo pieno.

## Stato: VIA LIBERA P2 (gia' eseguito)

7 provvisori (2A + 2B + 3C). I 5 `no_inference_fields` restano `null`.
