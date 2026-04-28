# Catalog Proposals — s05

**Data**: 2026-04-28
**Schema target**: v1.2
**Catalogo source**: local_snapshot (`catalogo_web/data/entities.json`, 114 entities)

---

## Sintesi

- Entita' inventariate dal nodo s05: **9** (5 personaggi + 3 luoghi + 1 oggetto)
- Entita' presenti in catalogo: **9 / 9** ✓ (con 1 mismatch nominale, vedi mis_005)
- Entita' da AGGIUNGERE: **0**
- Misalignments rilevati: **1** (mis_005, name_discrepancy `radura_coi_pini` vs `radura_dei_pini`)

---

## Tabella inventario

| Tipo | ID grafo | ID catalogo | In catalogo? | Note |
|---|---|---|---|---|
| personaggio | `gabriel` | `gabriel` | si | nessuna |
| personaggio | `elias` | `elias` | si | nessuna |
| personaggio | `noah` | `noah` | si | nessuna |
| personaggio | `bru` | `bru` | si | terza apparizione, agency attiva (compagno scoperta) |
| personaggio | `nodo` | `nodo` | si | **prima apparizione narrativa** (sottotipo: secondari) |
| personaggio | `coltivatori_del_cerchio` | `coltivatori_del_cerchio` | si | off-screen, gruppo |
| luogo | `torrente_affluente_foresta` | `torrente_affluente_foresta` | si | location_primary, prima apparizione narrativa (sottotipo: stream) |
| luogo | `foresta_intrecciata` | `foresta_intrecciata` | si | locations_secondary, ambiente attraversato |
| luogo | `orti_del_cerchio` | `orti_del_cerchio` | si | confine off-screen (motivo presenza Nodo) |
| luogo | `radura_coi_pini` | **`radura_dei_pini`** | si (con mismatch) | **mis_005**: name_discrepancy graph→catalog. Mappato a id catalogo. |
| oggetto | `corda_nodo` | `corda_nodo` | si (canonico) | recurring_visual_object kept |

**Riferimenti hook → location risoluzione (per P1):**

8 hook (1 in foresta_intrecciata, 6 sul torrente, 1 sulla radura):

| hook_id | id catalogo | qualifier proposto | legacy_string |
|---|---|---|---|
| s05_h1 | `foresta_intrecciata` | `cammino_interno_verso_torrente` | `foresta_intrecciata_cammino_interno_verso_torrente` |
| s05_h2 | `torrente_affluente_foresta` | `punto_vecchio_tronco_portato_via` | `torrente_punto_del_vecchio_tronco_portato_via` |
| s05_h3 | `torrente_affluente_foresta` | `posizione_nodo_50m_a_valle_scaletta` | `posizione_nodo_a_50_metri_al_lavoro_sulla_scaletta` |
| s05_h4 | `torrente_affluente_foresta` | `posizione_nodo_corda_tagliata` | `posizione_nodo_momento_della_corda_tagliata` |
| s05_h5_signature | `torrente_affluente_foresta` | `durante_costruzione_ponte` | `torrente_durante_costruzione_ponte` |
| s05_h6 | `torrente_affluente_foresta` | `ponte_finito_passaggio_elias` | `ponte_finito_momento_passaggio_elias` |
| s05_h7_radura | `radura_dei_pini` | `oltre_torrente_100_150_metri` | `radura_coi_pini_oltre_torrente_100_150_metri` |
| s05_h8 | `torrente_affluente_foresta` | `ritorno_ponte_ancora_li` | `torrente_ritorno_ponte_ancora_li` |

**Quadrant**: tutti `terra_ovest` (whitelist), nessuna rinomina.

---

## D. Misalignments rilevati

```json
{
  "id": "mis_005",
  "discovered_in_story": "s05",
  "discovered_in_phase": "P0",
  "between": "catalog_vs_graph",
  "type": "name_discrepancy",
  "catalog_reference": "catalogo_web/data/entities.json#radura_dei_pini",
  "graph_reference": "story_graph.json#stories.s05.location_primary.specific_points (radura_coi_pini_oltre_il_torrente_a_100_150_metri) + visual_anchors.scene_hooks[s05_h7_radura].location_precise (radura_coi_pini_*)",
  "bible_reference": null,
  "description": "Il grafo s05 cita 'radura_coi_pini' come specific_point + location_precise di hook. Catalogo ha 'radura_dei_pini' (sottotipo: clearing). Stessa entita', name discrepancy preposizione: 'coi' (grafo) vs 'dei' (catalogo). Mappato a id catalogo in P1. Decisione finale: scegliere il nome canonico (preferenzialmente 'radura_dei_pini' del catalogo, gia' usato in fase F catalogo) e aggiornare il grafo nelle storie successive che lo citano.",
  "severity": "bassa",
  "proposed_resolution": "Mappato in P1 di s05 a 'radura_dei_pini' (id catalogo). Decisione finale post-saga: confermare 'radura_dei_pini' come canonico e aggiornare grafo in storie successive (s12 cita 'radura_pini' o simili).",
  "status": "open"
}
```

---

## Note operative P0 s05

- **Cycle B centro**: attribute_dominant=connettere, block_position=centro_blocco_b (entrambi canonici).
- **PATTERN A SEMINATO**: prima semina formale del Pattern A in saga (`pattern_a_active: seminato`). Seed: `seed_pattern_a_rami_caduti_diventano_materia`. Bloom previsto in s06+.
- **Vento intreccio**: continua da s04.
- **`onomatopee_firma`**: `["TOK-TOK-TOK"]` (Nodo che lavora sulla scaletta — vincolo `tok_tok_tok_quota_4_5_storie_saga`).
- **3 callbacks**: tutti da s04 (gesto richiamo bru, principio fisico esteso foresta, sviluppo agency bru).
- **8 debts_opened raw + 1 debts_closed raw**: tutti seed_refs (precomputed_context: archived_seed_refs=8). Canonical: [].
- **Location primary**: `torrente_affluente_foresta` con 4 specific_points (incluso `radura_coi_pini` mis_005).
- Nessun bloccante per Ray.
