# Catalog Proposals — s02

**Data**: 2026-04-28
**Schema target**: v1.2
**Catalogo source**: local_snapshot (`catalogo_web/data/entities.json`, 113 entities)
**Catalogo generated_at**: stato locale al 2026-04-28
**Esecuzione**: P0 manuale (sub-agente in stream idle timeout dopo 46 letture senza write — recupero in chat con tool calls mirate)

---

## Sintesi

- Entità inventariate dal nodo s02: **8** (4 personaggi + 3 locations indipendenti + 1 da aggiungere)
- Entità presenti in catalogo: **7 / 8**
- Entità da AGGIUNGERE al catalogo: **1** (`pozza_abbeveratoio_pastori`, vedi §C)
- Schede stub candidate ad arricchimento: tutte le 7 esistenti (status=provvisorio, body con sezioni `_da popolare dal grafo_`). NON proposte arricchimenti specifici in P0: la compilazione dei body delle schede e' lavoro separato (Fase F catalogo) e non blocca P1/P2 della fase E.
- Misalignments rilevati (per `_canon_misalignments.json`): **1** (mis_002, pozza_abbeveratoio_pastori assente dal catalogo)

---

## Tabella inventario

| Tipo | ID | In catalogo? | Status scheda | Azione richiesta |
|---|---|---|---|---|
| personaggio | `gabriel` | si | provvisorio (stub) | nessuna (gia' attivo da s01) |
| personaggio | `elias` | si | provvisorio (stub) | nessuna (gia' attivo da s01) |
| personaggio | `noah` | si | provvisorio (stub) | nessuna (gia' attivo da s01) |
| personaggio | `stria` | si | provvisorio (stub) | nessuna (prima apparizione narrativa) |
| luogo | `pascoli_alti` | si | provvisorio (stub) | nessuna (gia' attivo da s01) |
| luogo | `scuola_stria` | si | provvisorio (stub) | nessuna (prima apparizione narrativa, quartiere=centro) |
| luogo | `pozza_abbeveratoio_pastori` | **NO** | — | aggiunta al catalogo §C |

**Riferimenti hook → location risoluzione (per P1):**

| hook_id | location_precise (legacy) | id catalogo | qualifier proposto | legacy_string |
|---|---|---|---|---|
| s02_h1 | `scuola_stria_cortile_o_margine_pascoli` | `scuola_stria` | `cortile_o_margine_pascoli` | `scuola_stria_cortile_o_margine_pascoli` |
| s02_h2 | `sentiero_in_salita_verso_pascoli_alti` | `pascoli_alti` | `sentiero_in_salita` | `sentiero_in_salita_verso_pascoli_alti` |
| s02_h3_signature | `pozza_ghiacciata_con_velo_d_acqua_sgelato_in_superficie` | `pozza_abbeveratoio_pastori` (NUOVO) | `ghiacciata_con_velo_d_acqua_sgelato` | `pozza_ghiacciata_con_velo_d_acqua_sgelato_in_superficie` |
| s02_h4 | `pozza_dopo_il_gesto_di_noah` | `pozza_abbeveratoio_pastori` (NUOVO) | `dopo_il_gesto_di_noah` | `pozza_dopo_il_gesto_di_noah` |
| s02_h5 | `sentiero_del_ritorno_dai_pastori` | `pascoli_alti` | `sentiero_del_ritorno` | `sentiero_del_ritorno_dai_pastori` |

**Nota metodologica**: i "sentieri" generici dei hook s02_h2 e s02_h5 sono mappati a `pascoli_alti` (come gia' fatto in s01_h2 con `pascoli_alti` + qualifier `salita_verso_sentiero_montagne`). Non sono entita' indipendenti del catalogo ma momenti del cammino sui pascoli; il qualifier descrive la fase del cammino. Decisione coerente con s01.

---

## A/B. Arricchimento schede esistenti

**Nessuna proposta in P0**: tutte le 7 schede esistenti sono `status: provvisorio` con body generato dal travaso meccanico Bible→catalogo (sezioni `_da popolare dal grafo_`). La compilazione narrativa e' lavoro della Fase F catalogo (separata), non blocca P1/P2 di s02.

---

## C. Aggiunta NUOVA entita' al catalogo: `pozza_abbeveratoio_pastori`

**Famiglia**: luogo
**Sottotipo**: water_feature (oppure `pond` / `sub_location_pascoli` — da decidere lo schema esatto in base a categorie esistenti)
**Path proposto scheda**: `visual/luoghi/quartiere_aria/water_features/pozza_abbeveratoio_pastori/scheda.md` (oppure altra collocazione coerente con la struttura attuale)
**Quartiere**: aria (sub-location di `pascoli_alti`)

### Motivazione

Il nodo s02 `location_primary._note` lo dichiara esplicitamente:

> "La pozza e' piccola, d'estate abbeveratoio delle capre dei Pastori, ora ghiacciata con il velo di superficie appena sgelato da una giornata di sole. **Da aggiungere come sub_location di pascoli_alti in ATLANTE quando si raffina (Fase E).**"

E' citata nei `specific_points` di `location_primary` e in 2 dei 5 visual_anchors (signature hook s02_h3 + s02_h4). E' il **focal point** della storia (s02 si chiama "Il Riflesso nella Pozza") e contiene il visual_anchor signature della scena. Non averla nel catalogo creerebbe un buco di tracciabilita' cross-skill.

### Frontmatter proposto

```yaml
---
id: pozza_abbeveratoio_pastori
name: Pozza dell'Abbeveratoio dei Pastori
famiglia: luogo
sottotipo: water_feature
quartiere: aria
parent_location: pascoli_alti
status: provvisorio
ultima_modifica: 2026-04-28
fonti: ["pipeline_narrativa/story_graph.json#stories.s02.location_primary.specific_points"]
appare_in_storie: ["s02"]
cartografia:
  feature_id: null  # da assegnare in cartografia se serve geometry esplicita
  type_geo: point
  status_geo: provvisorio
  quarter: aria
  parent_geo: pascoli_alti
---
```

### Contenuto body iniziale (essenziale)

```markdown
# Pozza dell'Abbeveratoio dei Pastori

> **Stato compilazione:** body provvisorio, generato dal travaso da nodo s02 in fase E (P0). Le sezioni con `_da popolare dal grafo_` saranno completate in fase F catalogo.

## Aspetto / forma

Pozza piccola sui Pascoli Alti. D'estate funge da abbeveratoio per le capre dei Pastori. D'inverno gela; il velo di superficie puo' sgelarsi nelle giornate di sole.

## Contesto e ambientazioni ricorrenti

Sub-location dei Pascoli Alti, quartiere aria. Presso le greggi dei Pastori (off-screen in s02).

## Coerenza cross-scena (cose che NON cambiano)

E' una pozza, non un lago ne' una fonte. Piccola. Funzionale (abbeveratoio). Stagionalmente cambia stato (acqua liquida d'estate, ghiaccio d'inverno con velo sgelabile).

## Storie / scene di apparizione

- s02: **prima apparizione**. Focal point della storia. Citata in `location_primary.specific_points` + visual_anchors signature hook s02_h3 (`ghiacciata_con_velo_d_acqua_sgelato`) e s02_h4 (`dopo_il_gesto_di_noah`).

## Riferimenti puntuali

- `pipeline_narrativa/story_graph.json#stories.s02.location_primary._note`: "La pozza e' piccola, d'estate abbeveratoio delle capre dei Pastori, ora ghiacciata con il velo di superficie appena sgelato da una giornata di sole. Da aggiungere come sub_location di pascoli_alti in ATLANTE quando si raffina (Fase E)."
- `pipeline_narrativa/story_graph.json#stories.s02.visual_anchors.scene_hooks[s02_h3_signature].location_precise`: "pozza_ghiacciata_con_velo_d_acqua_sgelato_in_superficie".
```

---

## D. Misalignments rilevati (per `_canon_misalignments.json`)

```json
{
  "id": "mis_002",
  "discovered_in_story": "s02",
  "discovered_in_phase": "P0",
  "between": "catalog_vs_graph",
  "type": "object_missing_from_catalog",
  "catalog_reference": null,
  "graph_reference": "story_graph.json#stories.s02.location_primary.specific_points[0] (pozza_abbeveratoio_pastori) e visual_anchors.scene_hooks[s02_h3_signature, s02_h4]",
  "bible_reference": null,
  "description": "La pozza_abbeveratoio_pastori e' citata nel grafo s02 come specific_point di location_primary (pascoli_alti) e come location_precise di 2 visual_anchors (signature + 1). E' il focal point della storia (titolo: 'Il Riflesso nella Pozza'). Assente dal catalogo isola_i3v_visual (113 entities). Il nodo s02 stesso anticipa l'azione: location_primary._note dichiara 'Da aggiungere come sub_location di pascoli_alti in ATLANTE quando si raffina (Fase E)'.",
  "severity": "media",
  "proposed_resolution": "Aggiungere al catalogo come location indipendente (famiglia=luogo, sottotipo=water_feature, quartiere=aria, parent_location=pascoli_alti). Vedi sezione §C di questo file per frontmatter + body iniziale proposti.",
  "status": "open"
}
```

---

## Azione richiesta a Ray

PRIMA di passare a Passata 1:

**OPZIONE A (preferita)** — aggiungere `pozza_abbeveratoio_pastori` al catalogo prima di P1:

1. Crea la scheda `visual/luoghi/quartiere_aria/water_features/pozza_abbeveratoio_pastori/scheda.md` con il frontmatter + body proposti in §C.
2. Esegui `python3 scripts/build_catalogo_web.py` per rigenerare `catalogo_web/data/entities.json`.
3. Commit + push: `Fase E s02: aggiunta pozza_abbeveratoio_pastori al catalogo`.
4. P1 puo' procedere; mis_002 va da `open` a `resolved`.

**OPZIONE B (più rapida)** — procedere a P1 con `pozza_abbeveratoio_pastori` mappata comunque ai 2 hook, lasciando mis_002 `open` nel rolling per chiusura post-saga (come pattern fatto per `mis_001` di s01 risolto in retro).

In entrambi i casi P1 puo' partire: il guardrail `locations_must_exist` di MIGRATION_PROMPT_FASE_E.md REGOLA 0.1 verra' validato sia con catalogo aggiornato (A) sia con la mappa nota (B); l'importante e' che P1 sappia che la pozza e' la stessa entita' su entrambi gli hook.

---

## Note operative P0 s02

- Personaggi: tutti gia' nel catalogo. `stria` ha quartiere=`null` nel catalogo (ok, e' un personaggio mobile della scuola).
- Quartieri attraversati in s02: `centro` (scuola_stria, hook s02_h1) + `aria` (pascoli_alti + pozza, hooks s02_h2 / s02_h3 / s02_h4 / s02_h5). Da popolare in `quartieri_attraversati` del canonical.
- `attribute_dominant` nell'old_node e': `"delta"` → applicare REGOLA 0.5 del MIGRATION_PROMPT, rimappare a `"distinguere"` (cycle A continua, Gabriel/Noah-distinguere). Vincolo gia' documentato nel prompt patchato post-s01.
- Nessun bloccante per Ray. Decisione richiesta solo su OPZIONE A vs B.
