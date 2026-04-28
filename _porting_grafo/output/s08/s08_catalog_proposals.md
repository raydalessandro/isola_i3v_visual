# Catalog Proposals — s08

**Data**: 2026-04-28
**Schema target**: v1.2

---

## Sintesi

- Entita' inventariate: **15** (9 personaggi + 7 luoghi)
- Entita' presenti in catalogo: **14 / 15** (con 1 mismatch nominale, mis_007)
- Entita' da AGGIUNGERE: **0**
- Misalignments rilevati: **1** (mis_007, name_discrepancy `mercato_del_mezzogiorno_panca_di_pietra` — stesso pattern di mis_006 in s06)

---

## Tabella inventario

| Tipo | ID | In catalogo? | Note |
|---|---|---|---|
| personaggio | gabriel/elias/noah | si | nessuna |
| personaggio | memolo, nodo, fiamma, stria | si | gia' attivi (s01-s07) |
| personaggio | mantenitori | si | **prima apparizione narrativa attiva** (lavoro notturno post-caduta) |
| personaggio | liu | si | cammeo aerea (s06 prima volta, qui prima MENZIONE quando_acqua_trema) |
| luogo | piazza_villaggio | si | location_primary (sottotipo: square, q: centro) |
| luogo | forno, scuola_stria, casa_memolo_cortile, albero_vecchio, pozzo_piazza, via_scuola | si | tutti q: centro/fuoco_est |
| luogo | `mercato_del_mezzogiorno_panca_di_pietra` | NO (mismatch) | **mis_007**: stesso pattern di mis_006 (s06). Mappato a `panca_di_pietra` (id catalogo) + role esteso. |

---

## D. Misalignments rilevati

```json
{
  "id": "mis_007",
  "discovered_in_story": "s08",
  "between": "catalog_vs_graph",
  "type": "name_discrepancy",
  "catalog_reference": "catalogo_web/data/entities.json#panca_di_pietra (sottotipo: landmark, q: centro)",
  "graph_reference": "story_graph.json#stories.s08.locations_secondary[6].id = 'mercato_del_mezzogiorno_panca_di_pietra'",
  "description": "Stesso pattern di mis_006 (s06): id composito grafo (gruppo_persone + luogo) invece di id luogo separato. Rinominato in P1 a 'panca_di_pietra' + role esteso 'vecchie_del_mercato_cammeo_silenzioso_quando_noce_cade_una_alza_mano_altre_annuiscono_zero_parole'. Il riferimento alle vecchie del mercato e' preservato nel role.",
  "severity": "bassa",
  "proposed_resolution": "RISOLTO in P1 s08 via locations_secondary_id_renames + role_extras. Stesso fix di mis_006. Decisione post-saga: aggiornare grafo nelle storie dove ricorre per uniformare a 'panca_di_pietra' canonico.",
  "status": "resolved",
  "resolved_in_phase": "P1"
}
```

---

## Note operative P0 s08

- **Centro blocco C**: cycle C cambiare in fase culminante. Pattern A bloom pieno.
- **night_scene: TRUE**: prima notte vera saga (post s01 notte parziale). Mantenitori e Nodo lavorano fino a notte sotto lanterne.
- **when_water_trembles: TRUE**: prima manifestazione del fenomeno saga (1 di 2, l'altra in s12). Lore-hook via Liù: "Forse l'acqua trema." (ipotesi non certezza, vincolo Bible).
- **Pattern A: bloomed pieno**: il noce che cade ma non ferisce nessuno (ramo leva su pozzo deflette traiettoria). 'L'albero ha aspettato che nessuno fosse sotto'.
- **6 debt_vero_dict opened + 4 closed**: prima storia saga con debt non-archived (precomputed_context.debts_keep popolati). Tutti normalizzati allo schema canonical (target → target_story, description → note, close_mechanism → close_mode, rilievo altissimo/medio_alto → alto). 3 debts_closed con id retrofittato per pattern schema (origin inferita: s05 nodo marinaro, s06 vecchie indicare, s05 pattern_a).
- **2 hooks dict-non-standard**: format `visual` + `stratification` (non `time_of_day` + `characters_present`). Parsati in P0 in `_p1_mapping.json#hook_dict` con campi canonici v1.2. Lo script applica fully-override.
- **6 callbacks** (5 a s05/s06, tutte tracciate).
- **fear_touched: gabriel** (precursore paura "fratelli_crescono_diversi", seed-gesto secondo germoglio).
- 14/15 entita' nel catalogo (mis_007 risolto in P1).
