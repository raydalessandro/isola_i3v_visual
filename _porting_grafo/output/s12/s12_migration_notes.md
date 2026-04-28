# Migration Notes — s12

**Data**: 2026-04-28
**Schema target**: v1.2 (freezato)
**Source**: `pipeline_narrativa/story_graph.json#stories.s12`
**Output**: `s12_canonical.json`
**Validazione finale**: ✅ JSON Schema 0 errori, 5 guardrail PASS

---

## Sintesi

s12 "Quando i Tre Venti Suonano Insieme" è la **chiusura saga**. Concerto tre venti, frammento Grunto unicum, sigillo narratore, cornice forno simmetrica con s1, bloom architrave terna strato 3 (Gabriel TIENE — completamento dire/accettare/tenere). Storia che chiude tutto: 16 debts_closed, 0 debts_opened, 9 callbacks. Migrazione meccanica con 4 categorie di mapping deterministiche (3 hook location composite + 9 debt_id legacy).

## Mapping campi (rinomine deterministiche)

### Top-level
- `attribute_dominant: "sigillo"` → invariato (canonico).
- `block_position: "chiusura_blocco_d"` → invariato.
- `season: "autunno"` → invariato.
- `season_passage: "autunno_inverno"` → invariato (già popolato).
- `wind_active: null` → invariato (concerto tre venti insieme, non vento singolo).
- `pattern_a_active: "bloomed"` → invariato (chiusura saga).
- `when_water_trembles: true` → invariato (2/2 saga, quota chiusa al guado pietre piatte).
- `night_scene: false` + `night_scene_notes` (popolato, transizione crepuscolo→notte percepita dall'interno del Forno) → invariato.
- `key_phrase_indicative: null` (schema permette null) — **eccezione sostanziale chiusura saga**: nessuna frase-chiave puntuale, il sigillo del narratore chiude. `key_phrase_notes` esplicita la decisione.
- `key_phrase_attributed_to: null` → **omesso** dal canonical (campo opzionale schema, schema vuole stringa non null se presente).

### location_primary
- Potatura schema: rimossi `specific_points`, `coordinates_mandala`, `quadrant`. Conservati `id` (`roccia_alta`) + `note`.

### locations_secondary (9)
Tutti già canonici (`forno`, `pontile_bocca`, `fiume_che_gira`, `guado_di_pietre_piatte`, `foresta_intrecciata`, `pascoli_alti`, `burrone`, `piazza_villaggio`, `albero_vecchio`). Niente mapping necessario. `note` preservato dove presente.

### scene_hooks (8)
**Risoluzione location stringhe composite (3 casi, decisione brief)**:

| Hook | Legacy string | Risoluzione |
|---|---|---|
| `hook_02_pontile_bartolo_*` | `pontile_bocca_poi_fiume_che_gira` | `{id: pontile_bocca, qualifier: risalita_verso_fiume_che_gira_sud, legacy_string: <full>}` |
| `hook_04_radura_pini_*` | `foresta_intrecciata_radura_pini_poi_pascoli_alti` | `{id: radura_dei_pini, qualifier: attraversamento_da_foresta_intrecciata_a_pascoli_alti}` |
| `hook_07_discesa_piazza_*` | `piazza_villaggio_con_albero_vecchio` | `{id: piazza_villaggio, qualifier: sotto_albero_vecchio}` |

Gli altri 5 hook hanno location già canonica: risolti a `{id, qualifier:null, legacy_string}`.

- **Quadrant derivato** (assente nel grafo): mappa estesa per s12 — `forno→fuoco_est`, `pontile_bocca→acqua_sud`, `guado_di_pietre_piatte→acqua_nord`, `radura_dei_pini→terra_ovest`, `burrone/roccia_alta→aria_nord`, `piazza_villaggio→centro_villaggio`.
- **Palette**: tutte le 8 palette già presenti nel grafo originale (s12 curato come s10/s11).
- Tutti gli hook hanno solo campi schema, niente `description_visual`/`visual_critique_notes`/`voice_constraint`/`key_phrase_visible` da assorbire.

### debts_opened (0)
Lista vuota nel grafo originale. Saga completa, niente debiti aperti per fase F (eccetto note in seeds_planted già strato 3).

### debts_closed (16) — 9 rinominati, 7 già conformi
**Trasformazione debt_id legacy → pattern canonico** (decisione brief):

Per pattern `s<NN>_<slug>` → `debt_s<NN>_to_s12_<slug>` (single-origin → s12):
- `s01_pagnotta_grunto_cornice_chiusura_saga_al_forno` → `debt_s01_to_s12_pagnotta_grunto_cornice_chiusura_saga_al_forno`
- `s01_cengia_burrone_spatial_echo_cresciuti_lo_sapranno_senza_vederlo` → `debt_s01_to_s12_cengia_burrone_spatial_echo_cresciuti_lo_sapranno_senza_vederlo`
- `s01_grunto_frammento_pre_vento_unico_saga` → `debt_s01_to_s12_grunto_frammento_pre_vento_unico_saga`
- `s04_tum_tum_tum_eco_silenziosa_mani_sulla_terra_forno` → `debt_s04_to_s12_tum_tum_tum_eco_silenziosa_mani_sulla_terra_forno`
- `s04_gesto_palmo_sulla_terra_bloom_finale_saga` → `debt_s04_to_s12_gesto_palmo_sulla_terra_bloom_finale_saga`
- `s05_radura_coi_pini_bloom_passaggio_autunnale_verso_roccia_alta` → `debt_s05_to_s12_radura_coi_pini_bloom_passaggio_autunnale_verso_roccia_alta`

Per pattern `s<NN>_to_<multi>_<slug>` → `debt_s<NN>_to_s12_<slug>` + flag multi-target in `note`:
- `s05_to_s06_s07_s08_s10_s11_s12_pattern_a_bloom_trasversale_saga` → `debt_s05_to_s12_pattern_a_bloom_trasversale_saga` (note: `[multi_target_legacy: s05_to_s06_s07_s08_s10_s11_s12_...]`)
- `s06_to_s07_s08_s10_s11_s12_cornetto_briciole_pattern_a_rinforzo_immagini_trasversali` → `debt_s06_to_s12_cornetto_briciole_pattern_a_rinforzo_immagini_trasversali` (idem)
- `s07_to_s08_s10_s11_s12_pattern_a_continuazione_attivazioni_trasversali` → `debt_s07_to_s12_pattern_a_continuazione_attivazioni_trasversali` (idem)

Tutti i 16 `debt_id` post-trasformazione conformi al pattern schema.

Campi extra assorbiti (per tutti i 16): `closed_in_story` → DROP (= s12), `close_type` → `close_mode`, `close_notes` → `note`.

### callbacks_made (9)
- `to_story` aggiunto come `s12`.
- Riferimenti a s01 (×2 — cornice forno, cengia burrone), s04 (×1), s05 (×2 — pattern A + radura), s06 (×1 — Liu mestiere informale), s07 (×1 — Bartolo modo canonico), s09 (×2 — paura gabriel + fette uguali). Rete narrativa completa attraversa tutti i blocchi.

### characters_in_scene (9)
9 chars in scene (gabriel, elias, noah, liu, fiamma, bartolo, grunto, coltivatori_del_cerchio, pastori) + 6 offscreen (rovo, stria, memolo, nodo, amo, mercato_del_mezzogiorno). Niente campi extra: tutti campi schema-conformi nel grafo.

### Auto-derivazioni 13 campi v1.2
- 5 no_inference: `null` (provvisori in `s12_provisional.json`).
- Da `quote_tracker_per_story.s12`: 
  - `narrator_address: true` (4/6 saga cumulativo, ultimo address al lettore)
  - `narrator_meta_voice: true` (1/2 saga, prima e ultima volta — vincolo "max 2 saga")
  - `grunto_memory_fragment: true` (1/1 saga, **unicum**: "Una volta era visto. Adesso si respira.")
  - `paronomastico_used: false`
  - `onomatopee_firma: []`
- `quartieri_attraversati`: `[acqua_nord, acqua_sud, aria_nord, centro_villaggio, fuoco_est, terra_ovest]` — **6 quartieri** (la saga attraversa l'intera isola, mai successo prima). Manca solo `centro_albero_vecchio` come quadrant separato perché `albero_vecchio` è collassato in qualifier `sotto_albero_vecchio` di `piazza_villaggio` (hook_07).
- `oggetti_simbolo_presenti`: `[]` (pattern P1 deterministico, sweep post-S12).
- `personaggi_vincoli_attivi`: 3 chars con vincoli (`fiamma`, `bartolo`, `grunto`). Gabriel/Elias/Noah/Liu/Coltivatori_del_cerchio/Pastori: niente vincoli "Mai" in tabella.

## Triage debt

I 16 `debts_closed` sono chiusure architettoniche reali. Tutti migrati con assorbimento di `closed_in_story`/`close_type`/`close_notes`. Niente `seed_ref` legacy da archiviare come rumore.

## Verifiche di integrità

- ✅ JSON Schema v1.2: 0 errori
- ✅ 5 guardrail Fase E: tutti PASS
- ✅ Campi narrativi: identici al grafo originale
- ✅ Cross-reference s01-s11 → s12: `seeds_picked_up` (13), `seeds_maturing_here` (0), `seeds_bloomed_here` (10) tutti presenti in storie precedenti
- ✅ Debt_id pattern: 16/16 conformi (9 rinominati + 7 già conformi)
- ✅ Continuità Pattern A: `s11: attivo → s12: bloomed` (chiusura)
- ✅ Continuità wind: `s11: null + tre_venti_staffetta_giorno → s12: null + concerto_tre_venti_insieme_unicum_saga` (escalation finale)
- ✅ Cumulativo `narrator_address` saga dopo s12: **4/6** (s04, s07, s10, s12) — quota saga rispettata, 2 ancora disponibili in C/D
- ✅ Cumulativo `narrator_meta_voice` saga: 1/2 (solo s12) — quota rispettata
- ✅ Cumulativo `grunto_memory_fragment` saga: **1/1** (solo s12, unicum dichiarato in active_constraints)
- ✅ Cumulativo `when_water_trembles` saga: **2/2** (s08 + s12) — quota chiusa
- ✅ `fear_touched.gabriel.status: bloomed` (terna strato 3 completa: Noah dice s10, Elias accetta s11, Gabriel tiene s12)

## Misalignments aggiunti

Nessun nuovo misalignment per s12. Tutte le risoluzioni applicate sono **trasformazioni meccaniche** (debt_id pattern, hook location composite) decise nel brief Fase E s09-s12 — non discrepanze.

## File output

- `s12_canonical.json` (52 campi top-level + 8 hooks risolti)
- `s12_provisional.json` (5 provvisori Famiglia A)
- `s12_catalog_proposals.md`
- `s12_migration_notes.md` (questo file)
- `_provisional_state.json` (rolling aggiornato — saga completa)
- `_canon_misalignments.json` (rolling invariato)

---

## Nota chiusura saga

Con s12 la migrazione delle 12 storie è completa. Riepilogo per chat C/D:

**Quote saga finali**:
- `narrator_address`: 4/6 consumati (s04, s07, s10, s12)
- `narrator_meta_voice`: 1/2 (s12)
- `grunto_memory_fragment`: 1/1 (s12, unicum)
- `when_water_trembles`: 2/2 (s08, s12, quota chiusa)
- `paronomastico_used`: 1 storia (s11)

**Misalignments aperti rimasti** (cumulativi): 2 (mis_004 pallone_di_stoffa_cucita s03, mis_005 radura coi/dei pini s05). Tutti gli altri `resolved` o `resolved_by_design`.

**Lavoro deferred a sweep post-S12**:
- `oggetti_simbolo_presenti` per ogni storia (popolazione dai 13 oggetti canonici in scena, semplice da recuperare)
- Risoluzione misalignments aperti (2 — entrambi bassa severità)
- Punti minori in tracking (vedi conversazione validazione)
