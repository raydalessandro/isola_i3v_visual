# Catalog Proposals — s12

**Data**: 2026-04-28
**Schema target**: v1.2
**Catalogo source**: github_raw
**Catalogo generated_at**: 2026-04-28T13:19:28
**Totale entità**: 114

---

## Sintesi

- Entità inventariate dal nodo s12: **23** (9 chars in scene + 6 chars offscreen + 11 luoghi distinct + 0 oggetti recurring + 0 vento attivo)
- Entità presenti in catalogo: **23** / 23 ✅
- Entità da AGGIUNGERE al catalogo: **0**
- Schede in catalogo: tutte popolate
- Patches scheda direttamente dal nodo s12: **0**
- Misalignments rilevati: **0 nuovi** (3 hook con location composita risolti per regole brief, non discrepanze)

---

## Tabella inventario

| Tipo | ID | In catalogo? | Stato |
|---|---|---|---|
| personaggi (in scene, 9) | gabriel, elias, noah, liu, fiamma, bartolo, grunto, coltivatori_del_cerchio, pastori | ✅ | tutti canonici |
| personaggi (offscreen, 6) | rovo, stria, memolo, nodo, amo, mercato_del_mezzogiorno | ✅ | tutti canonici |
| luogo primary | roccia_alta | ✅ | canonico |
| luoghi secondary (9) | forno, pontile_bocca, fiume_che_gira, guado_di_pietre_piatte, foresta_intrecciata, pascoli_alti, burrone, piazza_villaggio, albero_vecchio | ✅ | tutti canonici |
| luoghi (hook 02) | pontile_bocca_poi_fiume_che_gira | → pontile_bocca + qualifier | ✅ resolved (brief) |
| luoghi (hook 04) | foresta_intrecciata_radura_pini_poi_pascoli_alti | → radura_dei_pini + qualifier | ✅ resolved (brief) |
| luoghi (hook 07) | piazza_villaggio_con_albero_vecchio | → piazza_villaggio + qualifier sotto_albero_vecchio | ✅ resolved (brief) |
| vento | wind_active=null (concerto tre venti insieme, fenomeno raro) | concerto descritto in wind_transition | ✅ |

---

## A. Patches scheda dal nodo s12 — NESSUNA proposta

s12 contiene info sul concerto tre venti (fenomeno raro allineamento, seed_concerto_tre_venti), sigillo narratore, frammento Grunto unicum saga ("Una volta era visto. Adesso si respira."), bloom architrave Gabriel TIENE (gesto palmo terra). Tutto canonico nelle schede + Bible. Nessuna info canonicamente nuova da assorbire.

**Conclusione**: nessuna patch al catalogo da questa storia.

---

## B. Risoluzione 3 location composite (hooks)

Decisioni brief Fase E s09-s12 applicate:

### B.1 `pontile_bocca_poi_fiume_che_gira` (hook_02)

Hook itinerante: parte dal Pontile e risale la riva sud del Fiume che Gira. Risolto a `{id: pontile_bocca, qualifier: risalita_verso_fiume_che_gira_sud, legacy_string: <full>}`. Centro semantico = pontile_bocca (punto di partenza canonico, cammeo Bartolo). `fiume_che_gira` già in `locations_secondary`.

### B.2 `foresta_intrecciata_radura_pini_poi_pascoli_alti` (hook_04)

Hook itinerante attraversamento autunnale silenzioso. Centro semantico = `radura_dei_pini` (luogo "tra" foresta e pascoli, when_water_trembles_2di2 al guado del passaggio precedente). `foresta_intrecciata` e `pascoli_alti` già in `locations_secondary`.

### B.3 `piazza_villaggio_con_albero_vecchio` (hook_07)

Hook discesa piazza al crepuscolo, echi silenziose. `piazza_villaggio` e `albero_vecchio` sono entrambi canonici. L'albero è centro fisico della piazza (come da scheda catalogo), quindi mapping a `piazza_villaggio` con qualifier `sotto_albero_vecchio` è semanticamente corretto.

---

## C. Trasformazione 9 debt_id legacy → pattern canonico

Decisione brief Fase E s09-s12 applicata: i `debts_closed` con format `s<NN>_<slug>` o `s<NN>_to_<multi>_<slug>` rinominati a `debt_s<NN>_to_s12_<slug>`. Multi-target trasversale conservato come flag `[multi_target_legacy: ...]` nel campo `note`.

9 rinomine totali, 0 perdita di info. Vedi `s12_migration_notes.md` per dettaglio pre/post di ogni id.

---

## D. Nota su `oggetti_simbolo_presenti: []`

Pattern P1 deterministico (filtra da `recurring_visual_objects` del grafo, che è null per s12) → `[]`.

In scena nel narrativo (potenziali oggetti simbolo dei 13 canonici): `pagnotta_forno` (cornice s1↔s12), `grembiule_fiamma` (forno apertura+chiusura), `cicatrice_grunto` (Burrone hook_05 frammento unicum), `cesto_salvia` (cammeo offscreen), `conchiglia_amo` (cammeo Bartolo offscreen).

Decisione **deferred** a sweep post-S12 (decisione Ray): popolazione semplice in fase finale per tutte le 12 storie con review unica.

---

## E. Misalignments rilevati

Nessun nuovo misalignment per s12. Le risoluzioni applicate (3 location composite + 9 debt_id legacy) sono **trasformazioni meccaniche pre-decise nel brief Fase E s09-s12**, non discrepanze emergenti.

---

## Azione richiesta a Ray

**Nessuna**. Tutte le entità sono in catalogo, mapping applicati in P1 secondo brief.

Procedi con caricamento dei 4 file output di s12 nel repo `_porting_grafo/output/s12/` e aggiornamento dei 2 rolling.

---

## Chiusura saga

Con il caricamento di s12, la migrazione Fase E delle 12 storie è completata. Stato finale:
- 12/12 storie canonical schema v1.2 conformi
- 12/12 storie con provvisori P2 per C/D
- Quote saga rispettate
- 8 misalignments tracciati (6 resolved/resolved_by_design, 2 aperti bassa severità)
- Lavoro deferred: oggetti_simbolo_presenti sweep + misalignments residui + finalizzazione 5 no_inference fields da provvisori
