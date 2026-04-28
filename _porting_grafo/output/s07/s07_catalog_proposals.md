# Catalog Proposals — s07

**Data**: 2026-04-28
**Schema target**: v1.2
**Catalogo source**: local_snapshot (`catalogo_web/data/entities.json`, 114 entities)

---

## Sintesi

- Entita' inventariate dal nodo s07: **14**
- Entita' presenti in catalogo: **14 / 14** ✓
- Entita' da AGGIUNGERE: **0**
- Misalignments rilevati: **0**

s07 e' la prima storia con catalogo perfettamente allineato dal grafo. Tutte le entita' (personaggi, luoghi, oggetti) hanno id che matchano il catalogo.

---

## Tabella inventario

| Tipo | ID | In catalogo? | Note |
|---|---|---|---|
| personaggio | `gabriel`, `elias`, `noah` | si | nessuna |
| personaggio | `bartolo` | si | **prima apparizione narrativa** (sottotipo: primari, vincoli: mai_morale + mai_correre + mai_arrabbiato + mai_traghetta_abitanti_nominati) |
| personaggio | `toba` | si | **prima apparizione narrativa** (sottotipo: cuccioli) |
| personaggio | `amo` | si | **prima apparizione narrativa** (sottotipo: secondari, presenza iconica dalla riva opposta) |
| personaggio | `nodo` | si | off-screen, callback s05 |
| personaggio | `camminanti` | si | off-screen, gruppo collettivo (no vincoli) |
| personaggio | `coltivatori_del_cerchio` | si | off-screen, gruppo |
| luogo | `fiume_che_gira` | si | location_primary (sottotipo: river_system, quartiere: perimetro) |
| luogo | `guado_di_pietre_piatte` | si | locations_secondary (sottotipo: ford, quartiere: aria) — punto partenza |
| luogo | `foresta_intrecciata` | si | locations_secondary (vista da fuori, sponda) |
| luogo | `orti_del_cerchio` | si | locations_secondary (sponda) |
| luogo | `bocca` | si | locations_secondary (sottotipo: river_mouth, quartiere: acqua) |
| luogo | `pontile_bocca` | si | locations_secondary (sottotipo: pier) |
| luogo | `spiaggia_conchiglie` | si | locations_secondary (sottotipo: beach) — passaggio |
| luogo | `casa_amo` | si | locations_secondary (presenza iconica dalla riva opposta) |

---

## Riferimenti hook → location risoluzione (per P1)

6 hook lungo l'anello del Fiume da nord (guado) a sud (bocca). Quadrant non-whitelist normalizzati a valori canonici:

| hook_id | id catalogo | qualifier | quadrant proposto | quadrant legacy |
|---|---|---|---|---|
| s07_h1 | `guado_di_pietre_piatte` | `partenza_mattino_presto_pietre_piatte` | `acqua_nord` | `acqua_nord` (gia' canonico) |
| s07_h2 | `fiume_che_gira` | `lato_ovest_tratto_accanto_a_foresta_intrecciata` | `terra_ovest` | `terra_ovest_sponda_interna_fiume` |
| s07_h3 | `fiume_che_gira` | `lato_ovest_tratto_accanto_a_orti_del_cerchio` | `terra_ovest` | `terra_ovest_sponda_interna_fiume` |
| s07_h4 | `fiume_che_gira` | `due_massi_che_stringono_letto_meta_percorso` | `perimetro_fiume_che_gira` | `acqua_anello_fluviale_lato_ovest_meta` |
| s07_h5 | `fiume_che_gira` | `lato_ovest_discesa_verso_bocca` | `acqua_sud` | `acqua_sud_ovest_anello_fluviale` |
| s07_h6 | `pontile_bocca` | `arrivo_tramonto_vista_scogliera_est_amo` | `acqua_sud` | `acqua_sud` (gia' canonico) |

**Mapping quadrant suffix legacy → whitelist** (REGOLA 0.3 estesa, fix manuale in mapping s07):
- `terra_ovest_sponda_interna_fiume` → `terra_ovest`
- `acqua_anello_fluviale_lato_ovest_meta` → `perimetro_fiume_che_gira`
- `acqua_sud_ovest_anello_fluviale` → `acqua_sud`

**Quartieri attraversati** (derivati): `acqua_nord` + `terra_ovest` + `perimetro_fiume_che_gira` + `acqua_sud` (4 quartieri lungo l'anello fluviale).

---

## A/B/C/D

**Nessuna proposta arricchimento** (tutte schede esistenti, status provvisorio, fase F catalogo).
**Nessuna nuova entita'** da aggiungere.
**Nessun misalignment** rilevato.

---

## Note operative P0 s07

- **Cycle C apertura**: `attribute_dominant: cambiare` (gia' canonico, no rinomina), `block_position: apertura_blocco_c` (gia' canonico).
- **Pattern A: ATTIVO** (prima storia con `pattern_a_active: attivo`). Saga arc: none(s01-s04) → pre_eco(s02 effimero) → seminato(s05-s06) → **attivo(s07)**.
- **Vento intreccio** continua. Onomatopea `STRAPP` (probabilmente lo strappo della zattera che parte).
- **`narrator_address: true`** (secondo della saga, primo del blocco C, primo post-S4).
- **season: estate_piena** → REGOLA 0.10 → `season: estate` (script applica automaticamente).
- **5 callbacks** (cb_s07_001..005): a s05 (capacita_tecnica + pattern_a), s06 (pattern_a + bartolo sviluppo), s04 (gesto invertito).
- **Recurring_visual_objects: null** → script gestira' con fallback []. Possibili oggetti scena (zattera tre rametti, etc) non tracciati come canonici.
- **Niente fear_touched**.
- **Prime apparizioni narrative**: bartolo (4 vincoli), toba (3 vincoli), amo (4 vincoli).

Nessun bloccante per Ray. Procedo a P1.
