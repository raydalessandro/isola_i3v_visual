# Catalog Proposals — s06

**Data**: 2026-04-28
**Schema target**: v1.2
**Catalogo source**: local_snapshot (`catalogo_web/data/entities.json`, 114 entities)
**Caso speciale**: hooks in formato **string_legacy** (REGOLA 3 MIGRATION_PROMPT) — parsati a mano in P0 per fornire `hook_dict` completi al script P1.

---

## Sintesi

- Entita' inventariate dal nodo s06: **15** (11 personaggi/cammei + 4 luoghi/landmark)
- Entita' presenti in catalogo: **14 / 15** (con 1 mismatch nominale, vedi mis_006)
- Entita' da AGGIUNGERE: **0**
- Misalignments rilevati: **1** (mis_006, name_discrepancy `vecchie_del_mercato` vs `mercato_del_mezzogiorno`)

---

## Tabella inventario

| Tipo | ID grafo | ID catalogo | In catalogo? | Note |
|---|---|---|---|---|
| personaggio | `gabriel` | si | si | nessuna |
| personaggio | `elias` | si | si | nessuna |
| personaggio | `noah` | si | si | nessuna |
| personaggio | `memolo` | `memolo` | si | **prima apparizione narrativa** (sottotipo: primari) |
| personaggio | `pun` | `pun` | si | **prima apparizione narrativa** (sottotipo: cuccioli) |
| personaggio | `stria` | si | si | continua (s02 prima volta) |
| personaggio | `fiamma` | si | si | continua (s01 prima volta) |
| personaggio | `salvia` | si | si | continua (s04 prima volta) |
| personaggio | `zolla` | si | si | **prima apparizione narrativa** (sottotipo: secondari) |
| personaggio | `vecchie_del_mercato` | (`mercato_del_mezzogiorno`?) | mismatch | **mis_006**: id grafo vs id catalogo |
| personaggio | `liu` | `liu` | si | continua (cammeo cuccioli) |
| luogo | `scuola_stria` | si | si | nessuna |
| luogo | `forno` | si | si | nessuna |
| luogo | `casa_salvia` | si | si | nessuna |
| luogo | `casa_zolla` | si | si | **prima apparizione narrativa** |
| luogo | `panca_di_pietra` | si | si | landmark centro, prima apparizione |
| luogo | `cespuglio_dietro_albero_vecchio` | si | si | landmark centro, prima apparizione |
| luogo | `casa_memolo_cortile` | si | si | landmark centro, prima apparizione |
| oggetto | `sciarpa_memolo` | si (canonico) | si | menzionata in h7 ma NON in recurring_visual_objects (None nel grafo). |

**Nota recurring_visual_objects**: l'old_node ha `recurring_visual_objects: null` (non `[]`). Lo script gestisce con fallback a `[]`. `oggetti_simbolo_presenti: []` nel canonical. La sciarpa_memolo, il cornetto, e la scatoletta_dente_da_latte appaiono nel testo ma non sono tracked come recurring (dettaglio del grafo, non bloccante).

---

## D. Misalignments rilevati

```json
{
  "id": "mis_006",
  "discovered_in_story": "s06",
  "discovered_in_phase": "P0",
  "between": "catalog_vs_graph",
  "type": "name_discrepancy",
  "catalog_reference": "catalogo_web/data/entities.json#mercato_del_mezzogiorno (personaggio collettivo, sottotipo: collettivo)",
  "graph_reference": "story_graph.json#stories.s06.characters_in_scene[*].id = 'vecchie_del_mercato' (NON in catalogo) + characters_offscreen[*].id = 'mercato_del_mezzogiorno' (in catalogo)",
  "bible_reference": null,
  "description": "Il grafo s06 cita due id distinti per gruppi collettivi del mercato: 'vecchie_del_mercato' (in scena, panca di pietra, gesto del dito) e 'mercato_del_mezzogiorno' (off-screen, ambiente sociale). Il catalogo ha solo 'mercato_del_mezzogiorno' (personaggio.collettivo). Probabilmente le 'vecchie' sono SOTTOGRUPPO del mercato (le vecchie sedute sulla panca, parte del mercato come istituzione). P1 ha preservato 'vecchie_del_mercato' nel canonical characters_in_scene (decisione conservativa: l'id stringa non e' validato dallo schema, characters_must_exist e' regola del prompt non enforced).",
  "severity": "bassa",
  "proposed_resolution": "Decisione post-saga: o aggiungere 'vecchie_del_mercato' al catalogo come personaggio_sottogruppo di 'mercato_del_mezzogiorno', oppure unificare il grafo a 'mercato_del_mezzogiorno' con qualifier nel narrative_weight ('vecchie_sedute_sulla_panca_indicano_in_silenzio'). Ray decide.",
  "status": "open",
  "resolved_in_phase": null
}
```

---

## Note operative P0 s06

### Caso speciale 1: hooks in string_legacy (REGOLA 3)

Tutti gli 8 hooks dell'old_node sono stringhe narrative descrittive (non dict). Parsati a mano in P0 in `_p1_mapping.json#hooks[hid].hook_dict` con campi canonici v1.2 (hook_id, moment, location, quadrant, characters_present, elements, palette, notes, focal_action, focal_object, atmosphere, wind_visible, onomatopee). Lo script P1 ha aggiunto `FONTE_LEGACY: <stringa originale>` come prima entry di `elements` per tracciabilita' (notes resta null per popolazione P2 narrativa).

### Caso speciale 2: attribute_dominant `connettere_sottile` (REGOLA 0.5)

Il grafo dichiara `attribute_dominant: connettere_sottile`, valore non nell'enum v1.2 `["distinguere","connettere","cambiare","sigillo"]`. Decisione Ray: **mappare a `connettere`** (la sfumatura "sottile" e' qualifica narrativa, non estensione enum). Lo script applica il mapping automaticamente. Sfumatura documentata in **migration_notes** (NON in structural_notes, decisione Ray esplicita).

### Caso speciale 3: block_position legacy esteso (REGOLA 0.9)

`chiusura_blocco_b_connessione_come_cura_della_rete` → `chiusura_blocco_b` (troncamento). L'info estesa "connessione_come_cura_della_rete" resta in structural_notes dell'old_node (gia' presente come "CHIUSURA_BLOCCO_B").

### Caso speciale 4: season `passaggio_primavera_estate` (REGOLA 0.10)

`passaggio_primavera_estate` → `season: primavera` + `season_passage` preservato dall'old_node (era gia' popolato narrativamente: "prime_giornate_calde_sole_piu_alto_finestre_che_si_aprono_primi_tigli_in_fiore"). Decisione: storia inizia ancora in primavera, primavera->estate in transito.

### Multi-quartiere

Primo giro completo quattro-quartieri saga (escluso aria_nord = Pascoli, "troppo lontano per Memolo"). Quartieri attraversati: `centro_villaggio` (h1, h5, h6, h7, h8) + `fuoco_est` (h2 forno) + `terra_ovest` (h3 casa_salvia, h4 casa_zolla) = **3 quartieri**.

### Altri auto-derivati notevoli

- `pattern_a_active: seminato` (continua da s05)
- `paronomastico_used: true` (primo della saga? — flags_quote_tracker)
- 5 callbacks (1 a s05, 1 a s04, 1 a s01, 2 a s02)
- 2 seeds_planted (vecchie_indicare_in_silenzio + cornetto_briciole_pattern_a_rinforzo)
- 0 seeds_bloomed_here, 1 maturing (paura_elias_piccolo: variante capire-senza-avere)
- 0 fear_touched (Pun riconosce dente, NON e' paura di un fratello in scena)

### Bloccanti per Ray

Nessuno. mis_006 logged status open, decisione post-saga.
