# Catalog Proposals — s04

**Data**: 2026-04-28
**Schema target**: v1.2
**Catalogo source**: local_snapshot (`catalogo_web/data/entities.json`, 114 entities)

---

## Sintesi

- Entita' inventariate dal nodo s04: **9** (6 personaggi/cammei + 3 luoghi + 2 oggetti, di cui salvia e' prima apparizione narrativa)
- Entita' presenti in catalogo: **9 / 9** ✓
- Entita' da AGGIUNGERE al catalogo: **0**
- Misalignments rilevati: **0** (recurring_visual_objects entrambi canonici: `cesto_salvia` + `bandana_rovo`)

---

## Tabella inventario

| Tipo | ID | In catalogo? | Note |
|---|---|---|---|
| personaggio | `gabriel` | si | nessuna |
| personaggio | `elias` | si | nessuna |
| personaggio | `noah` | si | nessuna |
| personaggio | `salvia` | si | **prima apparizione narrativa** (sottotipo: secondari) |
| personaggio | `rovo` | si | seconda apparizione (s03 prima volta), bloom s04 (registro abitante foresta) |
| personaggio | `bru` | si | seconda apparizione, da intravisto a presenza concreta |
| personaggio | `coltivatori_del_cerchio` | si | off-screen, gruppo (cantilena piena di semina) |
| luogo | `foresta_intrecciata` | si | location_primary |
| luogo | `orti_del_cerchio` | si | locations_secondary, cornice cantilena |
| luogo | `casa_salvia` | si | implicita, off-screen (Salvia entra/esce) |
| oggetto | `cesto_salvia` | si (canonico) | recurring_visual_object kept |
| oggetto | `bandana_rovo` | si (canonico) | recurring_visual_object kept |

**Riferimenti hook → location risoluzione (per P1):**

7 hook, tutti su `foresta_intrecciata` con qualifier specifico (margine + interno):

| hook_id | id catalogo | qualifier proposto | legacy_string |
|---|---|---|---|
| s04_h1 | `foresta_intrecciata` | `margine_lato_orti` | `margine_foresta_intrecciata_lato_orti` |
| s04_h2 | `foresta_intrecciata` | `interno_primo_tratto_oltre_soglia_salvia` | `interno_foresta_primo_tratto_oltre_soglia_salvia` |
| s04_h3_signature | `foresta_intrecciata` | `interno_radice_esposta_grande_albero` | `interno_foresta_elias_sulla_radice_esposta_grande_albero` |
| s04_h4 | `foresta_intrecciata` | `interno_tra_radici_grande_albero` | `interno_foresta_noah_tra_radici_grande_albero` |
| s04_h5 | `foresta_intrecciata` | `interno_punto_di_ritrovamento` | `interno_foresta_punto_di_ritrovamento` |
| s04_h6 | `foresta_intrecciata` | `interno_arrivo_di_rovo` | `interno_foresta_arrivo_di_rovo` |
| s04_h7 | `foresta_intrecciata` | `margine_ritorno_da_salvia` | `margine_foresta_ritorno_da_salvia` |

**Quadrant**: tutti `terra_ovest` (whitelist), nessuna rinomina.

---

## A/B/C. Arricchimento / Aggiunta entita'

**Nessuna proposta in P0.** Tutte le entita' citate da s04 sono gia' nel catalogo. Le schede di salvia (prima apparizione narrativa) e rovo/bru (sviluppo) saranno arricchite in fase F catalogo con i dati di s03+s04.

---

## D. Misalignments rilevati

**Nessuno.** Sia `cesto_salvia` che `bandana_rovo` sono nei 13 oggetti canonici saga. mis_003 (bastoncino_noah_s1) e mis_004 (pallone) non si ripresentano in s04.

---

## Note operative P0 s04

- **Cycle B inizio**: `attribute_dominant: connettere` (gia' canonico, no rinomina REGOLA 0.5 necessaria).
- **block_position: `apertura_blocco_b`** (gia' canonico, no normalizzazione REGOLA 0.9 necessaria).
- **Pattern A**: `none` (semina vera in s06, scena attiva s07).
- **Vento intreccio**: prima manifestazione del Vento di cycle B in saga (saga ha 3 venti: taglio/intreccio/mulinello).
- **`narrator_address: true`**: PRIMO indirizzo al lettore in saga (1 di <=6 totali). Va popolato nel canonical da precomputed_context flags.
- **`onomatopee_firma`**: `["TUM-tum-TUM (fratelli)", "TUM-tum (coltivatori)"]` — il TUM-tum-TUM dei fratelli e' ECO BLOOM del TUM-tum dei coltivatori (cb_s04_003 callback s03).
- **5 callbacks** (cb_s04_001..005): script applichera' REGOLA 0.7 → to_story=s04 derivato.
- **8 debts_opened raw + 3 debts_closed raw**: tutti seed_refs (precomputed_context: debts_opened_keep=[], archived_seed_refs=11). Canonical: `debts_opened: []`, `debts_closed: []`. Tracking via seeds (3 bloomed_here + 3 maturing_here + 4 planted + 7 picked_up).
- **`key_phrase_indicative: null`**: key_phrase del narratore (sigillo address al lettore). REGOLA 0.8: `key_phrase_attributed_to` lasciato assente nel canonical (popolato in fase D quando Ray decide la frase).
- **`fear_touched`**: maturing della paura di Elias (variante "verso il basso" — micro-sguardo storto).
- Nessun bloccante per Ray. Procedo a P1.
