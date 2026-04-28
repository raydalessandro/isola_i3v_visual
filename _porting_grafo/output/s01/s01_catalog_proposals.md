# Catalog Proposals — s01

**Data**: 2026-04-28
**Schema target**: v1.2
**Catalogo source**: `/home/user/isola_i3v_visual/catalogo_web/data/entities.json` (live, locale)
**Catalogo generated_at**: 2026-04-28T07:45:06
**Totale entita' catalogo**: 112 (luoghi 72, personaggi 23, oggetti 13, venti 3, visual_signature 1; tutte status `provvisorio`)

---

## Sintesi

- Entita' inventariate dal nodo s01: **15** (5 personaggi + 6 luoghi + 3 oggetti + 1 vento; visual_signature non attivata: `when_water_trembles=false`).
- Entita' presenti in catalogo: **14 / 15**.
- Entita' da AGGIUNGERE al catalogo: **0** (vedi §D — il caso `sentiero_montagne_gemelle` e' classificato come label legacy non canonico, NON nuova entita').
- Schede compilate (>= 500 char): **14 / 14** delle entita' presenti.
- Schede stub (< 500 char) candidate ad arricchimento: **0**.
- Proposte di promozione contenuti nodo -> catalogo: **0** (tutto il contenuto canonico di s01 sui personaggi e luoghi e' gia' presente nelle schede attuali; quanto resta nel nodo e' specifico-di-scena).
- Misalignments rilevati: **1** (bassa severita', label legacy non risolvibile a un id canonico).

---

## Tabella inventario

| Tipo | ID | In catalogo? | Stato scheda | body_size_chars | Azione richiesta |
|---|---|---|---|---|---|
| personaggio | gabriel | si | compilata | 5679 | nessuna |
| personaggio | elias | si | compilata | 5506 | nessuna |
| personaggio | noah | si | compilata | 5675 | nessuna |
| personaggio | fiamma | si | compilata | 5971 | nessuna |
| personaggio | grunto | si | compilata | 6554 | nessuna |
| luogo | montagne_gemelle | si | compilata | 3073 | nessuna |
| luogo | forno | si | compilata | 4248 | nessuna |
| luogo | pascoli_alti | si | compilata | 2948 | nessuna |
| luogo | burrone | si | compilata | 2948 | nessuna |
| luogo | grotta_grunto | si | compilata | 2945 | nessuna |
| luogo | sentiero_montagne_gemelle | NO | — | — | NON aggiungere: label legacy (vedi §D, misalignment) |
| oggetto | pagnotta_forno | si | compilata | 2532 | nessuna |
| oggetto | grembiule_fiamma | si | compilata | 2757 | nessuna |
| oggetto | cicatrice_grunto | si | compilata | 2876 | nessuna |
| vento | vento_taglio | si | compilata | 6597 | nessuna |

### Visual signature

`when_water_trembles = false` nel nodo s01 e `visual_signatures_touched = []`. Nessuna entita' visual_signature attivata. Scheda `quando_acqua_trema` (4547 char) presente ma non referenziata da s01.

### Hook locations legacy (mappatura indicativa per Passata 1, NON azione P0)

Le 5 stringhe `location_precise` presenti in `visual_anchors.scene_hooks` non sono ID canonici diretti, ma sono tutte risolvibili a id catalogo gia' esistenti via prefix/qualifier (regola P1 §7.1 del prompt v3.0):

| Hook | legacy_string | id catalogo (target P1) | qualifier proposto |
|---|---|---|---|
| s01_h1 | `forno_interno` | `forno` | `interno` |
| s01_h2 | `pascoli_alti_salita_verso_sentiero_montagne` | `pascoli_alti` | `salita_verso_sentiero_montagne` |
| s01_h3 | `sentiero_montagne_gemelle_mezzacosta_cengia_sul_burrone` | `burrone` (oppure `montagne_gemelle`) | `mezzacosta_cengia_sul_burrone` (vedi nota in §D) |
| s01_h4_signature | `cengia_grotta_grunto_burrone` | `grotta_grunto` | `cengia` |
| s01_h5 | `forno_interno_ritorno` | `forno` | `interno_ritorno` |

Nota: la mappatura definitiva per s01_h3 spetta a P1; potrebbe essere ambigua tra `burrone` e `montagne_gemelle` o `sentiero_pascoli_burrone_diretto` -> in tal caso P1 sospende e chiede a Ray.

---

## A. Arricchimento scheda `<entity_id>` (stub -> compilato)

**Nessuna scheda stub coinvolta in s01.** Tutte le 14 entita' presenti hanno body >= 2500 char e contengono gia' le sezioni canoniche (Aspetto/forma, Espressione/comportamento, Palette e atmosfera, Contesto, Coerenza cross-scena, Variabilita').

Scan dei contenuti del nodo s01 confrontati con le schede: tutte le info canoniche su personaggi e luoghi citate nel nodo (es. cengia di Grunto sulla parete del Burrone; pelo verde di Grunto che si confonde col lichene; pendici nord ripide e quasi impraticabili; pagnotta come oggetto-rito) **sono gia' presenti** nelle schede `grotta_grunto`, `burrone`, `montagne_gemelle`, `grunto`, `pagnotta_forno`. Nessuna patch richiesta.

---

## B. Arricchimento scheda `<entity_id>`

**Vuoto.** Vedi §A.

---

## C. Aggiunta NUOVA entita' al catalogo: `<proposed_id>`

**Vuota — nessuna nuova entita' da creare.**

Il caso candidato (`sentiero_montagne_gemelle`) e' stato valutato e **scartato**: non risulta presente come entita' ne' nel grafo (`entities.locations`), ne' nel catalogo, ne' nella Bible §8 / convenzioni come ID canonico. Compare solo:

1. Come elemento di `location_primary.specific_points[]` nel nodo s01 (etichetta descrittiva del percorso).
2. Come prefisso della legacy_string `sentiero_montagne_gemelle_mezzacosta_cengia_sul_burrone` nell'hook s01_h3.

Il sistema di sentieri canonico (29 sentieri presenti in catalogo, prefisso `sentiero_*`) non include un sentiero dedicato fra Pascoli Alti e Montagne Gemelle: i candidati semantici piu' vicini sono `sentiero_pascoli_burrone_diretto` (1956 char) e `sentiero_roccia_burrone` (2564 char). Trattandosi di scelta cartografica/canonica, **non e' ruolo della P0 inventare un id**: si registra come misalignment (§D) e si lascia che P1 risolva la legacy_string a un id esistente con qualifier, oppure chieda a Ray.

---

## D. Misalignments rilevati (per `_canon_misalignments.json`)

Da NON aggiornare in P0 al rolling file (regola: solo P2 aggiorna). Si annotano qui per memoria, da promuovere in P2.

```json
{
  "id": "mis_001",
  "discovered_in_story": "s01",
  "between": "catalog_vs_graph",
  "type": "location_attribute",
  "catalog_reference": "catalogo_web/data/entities.json#<nessun id specifico: assenza>",
  "graph_reference": "story_graph.json#stories.s01.location_primary.specific_points[1] (sentiero_montagne_gemelle) e visual_anchors.scene_hooks[2].location_precise",
  "bible_reference": "§8.5 (sistema Pascoli/Montagne/Burrone)",
  "description": "Il nodo s01 cita 'sentiero_montagne_gemelle' come specific_point del percorso e come prefisso della legacy_string dell'hook s01_h3. Nessuna entita' con questo id esiste nel catalogo (72 luoghi, 29 sentieri canonici) ne' fra le entities.locations del grafo. I candidati semantici sono 'sentiero_pascoli_burrone_diretto' o 'sentiero_roccia_burrone', oppure il tratto va assorbito come qualifier di 'burrone' o 'montagne_gemelle'. Decisione cartografica/canonica: lasciata aperta. P1 risolvera' la legacy_string (regola 7.1) a un id esistente con qualifier o chiedera' a Ray.",
  "severity": "bassa",
  "proposed_resolution": null,
  "status": "open"
}
```

---

## Azione richiesta a Ray

**NESSUNA modifica al repo `isola_i3v_visual` e' richiesta prima di Passata 1.**

Il catalogo (generated_at 2026-04-28T07:45:06) copre tutte le entita' canoniche citate da s01 con schede compilate sopra la soglia stub. L'unica anomalia (`sentiero_montagne_gemelle`) e' una label legacy non canonica, gestibile in P1 via qualifier o domanda a Ray, e annotata come misalignment a bassa severita'.

### Decisione di proseguire

**VIA LIBERA per Passata 1.** Nessun blocco. P1 dovra':

1. Risolvere le 5 `location_precise` legacy a oggetti `{id, qualifier, legacy_string}` come da tabella in §inventario. Per s01_h3, se l'ambiguita' fra `burrone` / `montagne_gemelle` / `sentiero_pascoli_burrone_diretto` non si risolve univocamente, sospendere e chiedere a Ray (regola 7.1.4).
2. Validare il guardrail `locations_must_exist` e `characters_must_exist` contro il catalogo letto sopra (ID confermati).
3. P2 promuovera' il misalignment §D al rolling `_canon_misalignments.json`.
