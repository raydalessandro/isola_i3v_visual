---
id: <id_snake_case>
name: <Nome Visualizzato>
famiglia: luogo
sottotipo: <building|burrow|cave|clearing|coastal_belt|fields|ford|forest|landmark|mountain_system|path|pier|river|river_mouth|river_system|square|strada|stream|valley|work_area|...>
quartiere: <terra|fuoco|acqua|aria|centro|perimetro>
status: provvisorio
ultima_modifica: YYYY-MM-DD
fonti: ["pipeline_narrativa/story_graph.json#entities.locations.<id>", "cartografia/geo/island.geojson#features.id=<id>"]
appare_in_storie: []
ha_interno: <true|false>                # ⚠️ NUOVO: true se il luogo ha un interno significativo
ha_esterno: <true|false>                # ⚠️ NUOVO: true se il luogo ha un esterno significativo (default per quasi tutto)
ha_cortile_o_annessi: <true|false>      # ⚠️ NUOVO: true se ha cortile, annessi, sotto-aree distinte
cartografia:
  feature_id: <id>
  type_geo: <tipo>
  status_geo: <canonico|provvisorio|stub>
  quarter: <quartiere>
  category: <category|null>
  centroid_m_local: [x, y]
  bbox_m_local: [minx, miny, maxx, maxy]
  size_m_local: [w, h]
  altitudine_m: <m|null>
  geometry_type: <Point|LineString|Polygon|...>
  parent_geo: <id|null>
  children_geo: []
  aliases_geo: []
---


# <Nome Visualizzato>

> **Stato compilazione:** body provvisorio, completato YYYY-MM-DD con derivazione autoriale dalle fonti canoniche (Bible §X.Y; grafo entities.locations.<id>; cartografia island.geojson). Le sezioni in derivazione sono dichiarate in "Riferimenti puntuali".
>
> **⚠️ STRATEGIA LUOGHI:** questo luogo NON ha immagine di reference per scene multi-personaggio (vedi `_skill/PIPELINE.md` §luoghi). Le sezioni "Descrizione visiva canonica per generazione — ESTERNO / INTERNO / CORTILE" sono i **blocchi LOCATION testuali** da incollare nei prompt scena. Eventuale immagine establishing in `immagini/` è solo per atlante/preview, non per riuso in pipeline.
>
> **⚠️ LUOGHI CON ESTERNO + INTERNO (e/o annessi)**: questa scheda contiene **blocchi LOCATION distinti** per ogni "sotto-area" rilevante. Quando si compone un prompt scena, si usa SOLO il blocco corrispondente alla sotto-area in cui si svolge la scena (ESTERNO o INTERNO o CORTILE), mai più di uno per scena.

## Identità visuale (sintesi)

**Tipo:** <type>.
**Quadrante:** <quadrant>.
**Abitante:** <id|null>.
**Ruolo saga:** <ruolo>.

[1 paragrafo: cosa è e cosa fa nel mondo. 3-5 righe. Se ha interno+esterno, accennarlo qui.]

## Aspetto / forma — geografia generale

[Vista di insieme del luogo: cosa contiene, come è organizzato spazialmente. Se ha esterno + interno + cortile/annessi, breve descrizione di tutti, **senza dettaglio**: il dettaglio sta nei blocchi LOCATION più sotto.

Includere:
- Tipo di struttura
- Materiali principali
- Forma generale e dimensioni
- Articolazione in sotto-aree (se applicabile)
- Posizione sull'isola (richiamo al frontmatter cartografico)]

## Espressione / comportamento (dinamica del luogo)

[Cosa succede nel luogo durante la giornata, le stagioni, i momenti chiave.
- Suoni tipici, odori tipici
- Movimento di abitanti / animali / vento
- Variazioni nelle ore (alba/giorno/sera/notte)]

## Palette e atmosfera

[Travaso da `_canone/03_SAGA_PALETTE_v1.md` per il quartiere + dettagli specifici del luogo.]

## Contesto e ambientazioni ricorrenti

[Posizione esatta sull'isola, prossimità ad altri luoghi, distanze indicative, chi ci abita, chi ci passa.]

## Coerenza cross-scena (cose che NON cambiano)

[Lista bullet di tutto ciò che è canonico fisso. Se applicabile, raggruppato in sotto-sezioni:

**Esterno:**
- ...

**Interno:**
- ...

**Cortile / annessi (se presenti):**
- ...]

## Variabilità ammessa

[Cosa PUÒ variare scena per scena. E cosa NON varia mai.]

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

**Specifici visivi per luoghi:**
- Mai "tramonto epico" da poster fantasy.
- Mai luoghi "incantati" con effetti di luce magica, sparkle, glow.
- Mai luoghi "abbandonati e decadenti" se la Bible non li dichiara tali.
- Mai luoghi "perfettamente puliti" da showroom — sono luoghi vissuti.
- Mai dettagli architettonici troppo elaborati / nobili / barocchi.

---

## ⭐ Descrizione visiva canonica per generazione — ESTERNO

⚠️ **BLOCCO LOCATION ESTERNO** da incollare nei prompt Grok delle scene ambientate fuori dal luogo.

```
LOCATION (EXTERIOR) — <Name>:
[1 frase di apertura con tipo di luogo + quartiere + funzione]

[Forma generale dell'edificio/struttura visto da fuori, materiali, dimensioni]

[Disposizione spaziale esterna: orientamento, posizione relativa alla via, strutture annesse visibili]

[Vegetazione e contesto immediato]

[Atmosfera e luce esterna]

[Color palette dell'esterno: 3-5 colori dominanti specifici]
```

---

## ⭐ Descrizione visiva canonica per generazione — INTERNO (solo se applicabile)

⚠️ **BLOCCO LOCATION INTERNO** da incollare nei prompt Grok delle scene ambientate dentro il luogo.

```
LOCATION (INTERIOR) — <Name>:
[1 frase di apertura: tipo di interno, dimensione, funzione]

[Forma e dimensioni della stanza, materiali, altezza soffitto]

[Disposizione spaziale interna ESPLICITA: parete-X, centro, retro, vicino alla porta...]

[Mobili e oggetti caratteristici fissi]

[Atmosfera e luce interna]

[Color palette dell'interno]
```

---

## ⭐ Descrizione visiva canonica per generazione — CORTILE / ANNESSI (solo se applicabile)

⚠️ **BLOCCO LOCATION CORTILE/ANNESSI** da incollare nei prompt Grok delle scene ambientate nel cortile o nelle aree annesse.

```
LOCATION (COURTYARD / ANNEX) — <Name>:
[1 frase: tipo di area annessa + funzione + posizione rispetto all'edificio principale]

[Forma e dimensioni, elementi caratteristici fissi]

[Atmosfera e luce]

[Color palette]
```

---

### ✏️ Regole per scrivere i blocchi LOCATION

1. **Inglese sempre** (Grok funziona meglio).
2. **Disposizione spaziale esplicita** (sinistra/destra/centro/dietro/parete-X). Mai ambigua.
3. **Dimensioni in metri** quando rilevanti (dal frontmatter cartografico).
4. **Oggetti specifici** non generici: "wooden kneading table" non "a table".
5. **No personaggi** nel blocco LOCATION (i personaggi vengono dai loro reference image).
6. **No emozioni** nel blocco LOCATION (l'atmosfera viene dalla scena specifica).
7. **No effetti drammatici di luce** se non funzionali al canone.
8. **Riusabile**: ogni blocco va bene per QUALSIASI scena ambientata in quella sotto-area, in qualunque storia.
9. **Un solo blocco per scena.** Mai mischiare ESTERNO + INTERNO nello stesso prompt — produrrebbe immagini ibride confuse. Per scene di transizione (es: la porta che si apre vista da fuori), scegliere il blocco prevalente e descrivere l'altra zona come "sfondo intravisto".

## Per stampa 3D / modello

[Solo se applicabile.]

## Per narrativa e social

[Vedere file `descrizione_narrativa_social.md`.]

## Storie / scene di apparizione

[Lista derivata dal grafo, con indicazione se la scena è dentro/fuori/cortile.]

- s01: <ruolo o "assente"> [esterno/interno/cortile].
- ...

## Disallineamenti / domande aperte

[Conflitti, derivazioni non banali, dati mancanti.]

## Riferimenti puntuali (citazioni dirette dalle fonti)

**Fonti canoniche dirette:**
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8.<X>: "<citazione>"
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §6 PALETTE VISIVA — Quartieri: "<citazione>"
- `worldbuilding/GLOSSARIO_ISOLA.md` §<X>: "<citazione>"
- `pipeline_narrativa/story_graph.json#entities.locations.<id>`: <campi grafo>
- `cartografia/geo/island.geojson#features.id=<id>`: dati cartografici

**Derivazioni autoriali:**
- *<elemento derivato>*: derivato da <fonte>. Motivazione: <perché>.
