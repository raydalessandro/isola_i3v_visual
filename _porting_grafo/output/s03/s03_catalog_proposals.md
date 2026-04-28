# Catalog Proposals — s03

**Data**: 2026-04-28
**Schema target**: v1.2
**Catalogo source**: local_snapshot (`catalogo_web/data/entities.json`, 114 entities post-s02)
**Catalogo generated_at**: stato locale al 2026-04-28
**Esecuzione**: P0 manuale (sub-agenti falliti 3/3, approccio scriptato)

---

## Sintesi

- Entita' inventariate dal nodo s03: **6** (5 personaggi/luoghi narrativi + 1 oggetto)
- Entita' presenti in catalogo: **5 / 6**
- Entita' da AGGIUNGERE al catalogo: **0 obbligatorie** + **1 candidata** (`pallone_di_stoffa_cucita`, vedi §C — decisione di design Ray)
- Misalignments rilevati: **1** (mis_004, pallone come potenziale 14° oggetto-simbolo saga)

---

## Tabella inventario

| Tipo | ID | In catalogo? | Status scheda | Azione richiesta |
|---|---|---|---|---|
| personaggio | `gabriel` | si | provvisorio (stub) | nessuna |
| personaggio | `elias` | si | provvisorio (stub) | nessuna |
| personaggio | `noah` | si | provvisorio (stub) | nessuna |
| personaggio | `rovo` | si | provvisorio (stub) | nessuna (prima apparizione narrativa) |
| personaggio | `bru` | si | provvisorio (stub) | nessuna (prima apparizione narrativa) |
| personaggio | `coltivatori_del_cerchio` | si | provvisorio (stub) | nessuna (off-screen, gruppo) |
| luogo | `foresta_intrecciata` | si | provvisorio (stub) | nessuna |
| luogo | `orti_del_cerchio` | si | provvisorio (stub) | nessuna |
| oggetto | `pallone_di_stoffa_cucita` | **NO** | — | **decisione Ray** (vedi §C) |

**Riferimenti hook → location risoluzione (per P1):**

Tutti i 5 hook hanno `location_precise: margine_foresta_*` e `quadrant: terra_ovest`. Mappati a `foresta_intrecciata` con qualifier specifico (location_primary._note dichiara: "Margine: confine tra Orti del Cerchio e Foresta Intrecciata. Non dentro la Foresta — i fratelli si fermano prima del margine. Solo Rovo esce dalla Foresta.").

| hook_id | location_precise (legacy) | id catalogo | qualifier proposto | legacy_string |
|---|---|---|---|---|
| s03_h1 | `margine_foresta_orti_campo_gioco` | `foresta_intrecciata` | `margine_orti_campo_gioco` | `margine_foresta_orti_campo_gioco` |
| s03_h2_signature | `margine_foresta_momento_del_calcio_mal_misurato` | `foresta_intrecciata` | `margine_calcio_mal_misurato` | `margine_foresta_momento_del_calcio_mal_misurato` |
| s03_h3 | `margine_foresta_momento_del_chiamare_elias` | `foresta_intrecciata` | `margine_chiamare_elias` | `margine_foresta_momento_del_chiamare_elias` |
| s03_h4 | `margine_foresta_rovo_esce` | `foresta_intrecciata` | `margine_rovo_esce` | `margine_foresta_rovo_esce` |
| s03_h5 | `margine_foresta_rovo_si_volta_per_rientrare` | `foresta_intrecciata` | `margine_rovo_si_volta_per_rientrare` | `margine_foresta_rovo_si_volta_per_rientrare` |

**Quadrant**: tutti `terra_ovest` (whitelist), nessuna rinomina necessaria.

---

## A/B. Arricchimento schede esistenti

**Nessuna proposta in P0** (status di tutte le schede esistenti = `provvisorio` con body stub; arricchimento e' lavoro fase F catalogo).

---

## C. Aggiunta NUOVA entita' al catalogo: `pallone_di_stoffa_cucita` (DECISIONE RAY)

**Famiglia**: oggetto
**Sottotipo**: oggetto_simbolo_saga (proposto)
**Path proposto scheda**: `visual/oggetti/pallone_di_stoffa_cucita/scheda.md`

### Motivazione

Il nodo s03 ha:
- `recurring_visual_objects: ['pallone_di_stoffa_cucita', 'bandana_rovo']` (visual_anchors)
- `seeds_planted: ['seed_pallone_stoffa_cucita', ...]`
- `debts_opened` (archived_seed_refs): `s11_pallone_ricomparsa_giochi_cuccioli_tentativo` — il pallone **ricompare in s11** come tentativo dei cuccioli di rievocare il gioco.

Questo lo rende un OGGETTO RICORRENTE TRANSAGA: da s03 a s11. Potenziale 14° oggetto-simbolo (i 13 attuali sono: bandana_rovo, bisaccia_zolla, braccialetto_s9, cesto_salvia, cicatrice_grunto, conchiglia_amo, corda_nodo, grembiule_fiamma, lanterna_velata_s10, nido_vuoto_s08, pagnotta_forno, scialle_stria, sciarpa_memolo).

**Tre opzioni:**

**OPZIONE A** — aggiungere al catalogo come 14° oggetto-simbolo, frontmatter `famiglia: oggetto`, status `provvisorio`. P1 di s03 lo mette in `oggetti_simbolo_presenti` insieme a `bandana_rovo`. mis_004 → resolved.

**OPZIONE B** (default scriptato) — non aggiungere al catalogo per ora, P1 di s03 lo droppa da `oggetti_simbolo_presenti` (resta solo `bandana_rovo`). mis_004 resta `open`. Tracking narrativo del pallone resta in `seeds_planted` + `seeds_picked_up` di s11. Risoluzione post-saga.

**OPZIONE C** — non aggiungere come oggetto-simbolo saga (riserva quei 13 per archetipi forti) ma comunque registrare nel catalogo come oggetto narrativo `famiglia: oggetto, sottotipo: oggetto_di_scena_ricorrente`. Distinzione esplicita nel catalogo.

**Mia raccomandazione**: OPZIONE B. Motivazione: il pallone e' un oggetto-firma del gruppo bambini in s03+s11, non ha la stessa densita' simbolica dei 13 (es. cicatrice_grunto, nido_vuoto_s08, lanterna_velata_s10). Lasciare la lista canonica chiusa. Risoluzione post-saga puo' decidere se promuoverlo. Stesso pattern usato in s02 per `bastoncino_noah_s1` (mis_003, oggetto-firma personaggio non in catalogo).

### Frontmatter proposto (se OPZIONE A o C)

```yaml
---
id: pallone_di_stoffa_cucita
name: Pallone di Stoffa Cucita
famiglia: oggetto
sottotipo: oggetto_simbolo_saga  # OPZIONE A
# oppure: sottotipo: oggetto_di_scena_ricorrente  # OPZIONE C
status: provvisorio
ultima_modifica: 2026-04-28
fonti: ["pipeline_narrativa/story_graph.json#stories.s03"]
appare_in_storie: ["s03", "s11"]
---
```

---

## D. Misalignments rilevati (per `_canon_misalignments.json`)

```json
{
  "id": "mis_004",
  "discovered_in_story": "s03",
  "discovered_in_phase": "P0",
  "between": "catalog_vs_graph",
  "type": "other",
  "catalog_reference": "catalogo_web/data/entities.json (13 oggetti canonici, famiglia=oggetto)",
  "graph_reference": "story_graph.json#stories.s03.visual_anchors.recurring_visual_objects[0] = 'pallone_di_stoffa_cucita'",
  "bible_reference": null,
  "description": "Il grafo s03 lista 'pallone_di_stoffa_cucita' tra recurring_visual_objects. Non e' nel catalogo come famiglia=oggetto. Diverso da bastoncino_noah_s1 (mis_003, oggetto-firma personaggio): il pallone e' oggetto di gruppo, ricorrente trasversalmente s03 -> s11 (debt: s11_pallone_ricomparsa_giochi_cuccioli_tentativo). Potenziale 14° oggetto-simbolo saga oppure oggetto_di_scena_ricorrente. Decisione di design Ray richiesta.",
  "severity": "bassa",
  "proposed_resolution": "Tre opzioni in s03_catalog_proposals.md §C. Default scriptato (OPZIONE B): pallone droppato da oggetti_simbolo_presenti, tracking narrativo resta in seeds + callbacks, decisione post-saga.",
  "status": "open"
}
```

---

## Azione richiesta a Ray

Decisione su `pallone_di_stoffa_cucita`:
- **OPZIONE A** (aggiungi catalogo, 14° oggetto-simbolo): se OK, scrivo la scheda, rigenero entities.json, mis_004 → resolved.
- **OPZIONE B** (default scriptato, non aggiungere ora): procedo a P1 subito, pallone droppato, mis_004 open.
- **OPZIONE C** (aggiungi catalogo come oggetto_di_scena_ricorrente, non come oggetto-simbolo saga): scheda con sottotipo distinto.

**Mia raccomandazione**: OPZIONE B (coerente con mis_003 di s02). Decisione finale a Ray.

---

## Note operative P0 s03

- Personaggi: tutti gia' nel catalogo. **Prima apparizione narrativa di rovo + bru** (entrambi gia' come stub).
- `coltivatori_del_cerchio` come gruppo off-screen (cantilena sommessa "TUM-tum"). Esiste nel catalogo come `personaggio.collettivo`.
- Quartieri attraversati: solo `terra_ovest` (tutti i 5 hook + location_primary). Saga primissima storia in terra_ovest.
- `attribute_dominant`: legacy `delta` → REGOLA 0.5 → `distinguere`. Coerente con cycle A chiusura blocco.
- `wind_active: null`: storia senza vento attivo (terra_ovest e' quartiere chiuso, foresta).
- `pattern_a_active: none`: nessuna manifestazione Pattern A in s03.
- `night_scene: false` (anche se la fear_touched evoca "buio della Foresta di sera" — non e' scena notturna piena).
- `onomatopee_firma`: `["TUM-tum (coltivatori)"]` da precomputed_context.flags_quote_tracker.
- 1 callback (cb_s03_001 da s01, eco strutturale "fermarsi_come_gesto_attivo"): script applichera' REGOLA 0.7 → to_story=s03.
- 7 debts_opened raw → tutti archived_seed_refs (precomputed_context confirms: debts_opened_keep=[]). Canonical: `debts_opened: []`.
- 0 debts_closed.
- Nessun bloccante per Ray oltre a OPZIONE A/B/C su pallone.
