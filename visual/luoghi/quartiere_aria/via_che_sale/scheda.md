---
id: via_che_sale
name: Via che Sale
famiglia: luogo
sottotipo: path
quartiere: aria
status: provvisorio
ultima_modifica: 2026-04-30
fonti: ["pipeline_narrativa/story_graph.json#entities.locations.via_che_sale", "cartografia/geo/island.geojson#features.id=via_che_sale"]
appare_in_storie: []
cartografia:
  feature_id: via_che_sale
  type_geo: path
  status_geo: canonico
  quarter: aria
  category: via_principale
  centroid_m_local: [4065, 4560]
  bbox_m_local: [4005, 3500, 4205, 5300]
  size_m_local: [200, 1800]
  altitudine_m: null
  geometry_type: LineString
  parent_geo: null
  children_geo: []
  aliases_geo: []
---


# Via che Sale

> **Stato compilazione:** body provvisorio, generato dal travaso meccanico Bible→catalogo il 2026-04-28. Le sezioni con `_da popolare dal grafo_` saranno completate da Ray quando ragionerà sul grafo.

## Identità visuale (sintesi)


**Tipo:** via.
**Quadrante:** aria_nord.


## Aspetto / forma

Una delle quattro vie principali in uscita dal Villaggio centrale (§8.1): esce a nord verso il Quartiere d'Aria, attraversa i Pascoli Alti e prosegue fino alla Roccia Alta e oltre verso le Montagne Gemelle. Geometria cartografica: LineString di 1800 m in direzione nord (200 m est-ovest), dalla Piazza fino a Roccia Alta.

## Abbigliamento / stato d'uso

_da popolare dal grafo_

## Espressione / comportamento

_da popolare dal grafo_

## Palette e atmosfera

Quartiere d'Aria (Nord): grigio pietra, blu ghiaccio, vento secco.

## Contesto e ambientazioni ricorrenti

Esce dalla Piazza del Villaggio in direzione nord, sale attraverso i Pascoli Alti del Quartiere d'Aria fino alla Roccia Alta (2 ore) e prosegue verso le Montagne Gemelle e la grotta di Grunto (4-5 ore). Tragitto canonico Villaggio → Pascoli → Roccia Alta → Burrone.

## Coerenza cross-scena (cose che NON cambiano)

Direzione: nord. Origine: Piazza del Villaggio. Tappa intermedia: Pascoli Alti. Tappa di vetta: Roccia Alta (a 2 ore, altitudine 550 m). Continuazione: Burrone e Montagne Gemelle (4-5 ore alla grotta di Grunto).

### Dettagli stabili (path_details Tier A)

Riferimento canonico: `pipeline_narrativa/story_graph.json#world_conventions.path_details.paths.via_che_sale` (DOC_6, decisioni autoriali Ray 2026-04-30).

- **`vcs_d01_pietra_dei_tre_passi`** — *primo terzo della salita, sentiero pianeggia tre passi prima e tre passi dopo*. Pietra piatta posata di traverso. Chi sale di buon ritmo la usa come "fermata" — uno o due secondi per riprendere fiato. Saggezza del corpo, sentiero che insegna il ritmo. *Storie:* s01 (prima volta della saga in ascesa — i fratelli si fermano d'istinto).
- **`vcs_d02_cardo_isolato`** — *tratto medio, ciglio est, da una crepa nella terra*. Cresce solo lui, fiorisce viola in primavera, secco e dorato d'autunno. Non si ricorda da quanti anni è lì. **Oggetto-firma evolvente del sentiero**, "orologio del sentiero". *Storie:* s02 (secco dorato, fine inverno), s11 (secco dorato, autunno), s12 (coperto di brina, punte bianche, vigilia brina). *Evolvente principale Tier A.*
- **`vcs_d03_sasso_del_campanaccio`** — *tratto in alto vicino ai Pascoli, punto di radunamento gregge*. Roccia tonda incassata nel pendio, punto liscio in cima dove il bastone batte sempre. I Pastori in discesa appoggiano il bastone (TIK-TIK-TIIK eco) per radunare il gregge prima della piazza. *Storie:* s11 (Pastori scendono per la festa — il TIK-TIK-TIIK risuona qui prima della piazza). Collega saluto Pastori (DOC_2 §2.5) al sentiero.
- **`vcs_d04_segno_del_passaggio`** — *tratto in alto vicino ai Pascoli, due lati del sentiero*. Erba schiacciata in due righe parallele dalle generazioni di pastori. Non ricresce mai dritta — anche senza passaggi recenti, le righe restano. *Storie:* s12 (vigilia brina: righe ingiallite brillano alla luce del Concerto). *Evolvente.* Memoria geologica del sentiero.

I dettagli sono fonte autorevole della firma visuale e narrativa del sentiero. Ogni illustrazione/scena deve rispettarli.

## Variabilità ammessa

Variazioni stagionali §8.7: salendo si entra nel regime "pietra fredda e vento secco" del Quartiere d'Aria, intensificato in inverno.

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

_da popolare dal grafo_

## Per stampa 3D

_da popolare dal grafo_

## Per narrativa e social

_da popolare dal grafo_

## Storie / scene di apparizione

- s01: assente.
- s02: assente.
- s03: assente.
- s04: assente.
- s05: assente.
- s06: assente.
- s07: assente.
- s08: assente.
- s09: assente.
- s10: assente.
- s11: assente.
- s12: assente.

(Nel grafo non risultano apparizioni esplicite con id `via_che_sale`, pur essendo via principale di accesso al Quartiere d'Aria che compare in s01, s02, s12.)

## Disallineamenti / domande aperte

La Via che Sale è dichiarata via principale del Quartiere d'Aria in §8.1 e in cartografia (`canonico`, `via_principale`), ma il grafo non la lega come `locations_secondary` ad alcuna storia: le storie del Quartiere d'Aria (s01 Montagne Gemelle, s02 Pascoli Alti, s12 Roccia Alta + Burrone) non la citano.

## Riferimenti puntuali (citazioni dirette dalle fonti)

- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8.1 "Il Villaggio": "Quattro vie escono verso i quartieri: Via dell'Alba (est), Via del Pontile (sud), Via degli Orti (ovest), Via che Sale (nord)."
- `ISOLA_TRE_VENTI_BIBLE_v2.md` §8.5 "Il Quartiere d'Aria — a nord": "Lungo la Via che Sale."
- `ISOLA_TRE_VENTI_BIBLE_v2.md` §8.1 "Distanze dal Villaggio centrale": "Roccia Alta: 2 ore. Grotta di Grunto: 4-5 ore (mezza giornata)".
- `ISOLA_TRE_VENTI_BIBLE_v2.md` §6 PALETTE VISIVA "Quartieri": "Quartiere d'Aria (Nord): grigio pietra, blu ghiaccio, vento secco."
- `pipeline_narrativa/story_graph.json#entities.locations.via_che_sale`.
