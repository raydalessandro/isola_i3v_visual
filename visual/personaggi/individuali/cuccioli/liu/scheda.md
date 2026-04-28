---
id: liu
name: Liu
famiglia: personaggio
sottotipo: cuccioli
specie: libellulina
tipo_grafo: cucciolo_scuola
ruolo_saga: presenza_aerea_discreta
status: provvisorio
ultima_modifica: 2026-04-28
fonti: ["pipeline_narrativa/story_graph.json#entities.characters.liu"]
appare_in_storie: []
relazioni:
  dimora: null
  quadrante_grafo: null
  related_to: []
  cross_skill:
    cartografia: null
---

# Liu

> **Stato compilazione:** body provvisorio, generato dal travaso meccanico Bible→catalogo il 2026-04-26. Le sezioni con `_da popolare dal grafo_` saranno completate da Ray quando ragionerà sul grafo.

## Identità visuale (sintesi)

_da popolare dal grafo_

## Aspetto / forma

Minuscola — lunga come un dito di un fratello. Le ali trasparenti con riflessi azzurro-verdi, il corpo sottile come un fuscello, gli occhi grandissimi (per la sua taglia). Vola velocissima, si ferma in aria immobile, riparte di scatto.

## Abbigliamento / stato d'uso

_da popolare dal grafo_

## Espressione / comportamento

Liù fa cose-da-libellula. Vola dappertutto — copre l'isola in poco tempo. Sente conversazioni — sta sulle foglie sopra le teste degli abitanti, e gli abitanti la dimenticano lì. Porta notizie — non come Stria che è messaggera ufficiale, ma in modo informale. Si ferma in aria per parlare — il battito d'ali fa un piccolissimo *frrr*.

Sceglie cosa ridire e cosa no. Non è pettegola.

## Palette e atmosfera

_da popolare dal grafo_

## Contesto e ambientazioni ricorrenti

Frequenta la scuola di Stria a modo suo (vola sopra, ascolta da fuori, entra qualche volta). Sta sulle foglie sopra le teste degli abitanti.

## Coerenza cross-scena (cose che NON cambiano)

Taglia minuscola (lunga come un dito di un fratello). Ali trasparenti con riflessi azzurro-verdi. Corpo sottile come un fuscello. Occhi grandissimi per la sua taglia. Volo velocissimo con stop in aria immobile e ripartenza di scatto. Battito d'ali con suono *frrr*.

## Variabilità ammessa

_da popolare dal grafo_

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

Da Bible §4.17 "Note e vincoli":
- Mai Liù che resta in scena a lungo — entra, dice, va.
- Mai Liù che fa la pettegola per cattiveria.
- Mai Liù in scene serie come voce comica.
- Mai Liù che sa cose che il narratore ha esplicitamente nascosto al lettore.

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
- s06: cammeo volante, messaggera — prima apparizione vera.
- s07: assente.
- s08: messaggera aerea — annuncio del fenomeno raro come ipotesi ("Forse l'acqua trema").
- s09: cucciolo scuola, presenza aerea, fonte informale di notizia (vola da scuola al Forno).
- s10: assente.
- s11: assente esplicita (discrepanza archi tabella vs dettaglio risolta a favore "assente").
- s12: cammeo di apertura, portatrice di notizie — prima a chiamare il fenomeno "suonano" (nome installato del Concerto).

## Disallineamenti / domande aperte

- Bible §4.17 usa **"Liù"** (con accento grave). Grafo usa id `liu` senza accento e non ha campo `name` esplicito; lo script genera `name: Liu`. Il display name dovrebbe essere **Liù**? Se sì, il fix va nel grafo (`entities.characters.liu.name = "Liù"`) e poi rilancio dello script visual per propagare.

## Riferimenti puntuali (citazioni dirette dalle fonti)

- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §4.17 LIÙ:
  - "Libellulina. Genitori non in scena. Frequenta la scuola di Stria a modo suo (vola sopra, ascolta da fuori, entra qualche volta)."
  - "Minuscola — lunga come un dito di un fratello. Le ali trasparenti con riflessi azzurro-verdi, il corpo sottile come un fuscello, gli occhi grandissimi (per la sua taglia). Vola velocissima, si ferma in aria immobile, riparte di scatto."
  - "Liù fa cose-da-libellula. Vola dappertutto — copre l'isola in poco tempo. Sente conversazioni — sta sulle foglie sopra le teste degli abitanti, e gli abitanti la dimenticano lì."
  - "Si ferma in aria per parlare — il battito d'ali fa un piccolissimo *frrr*."
  - "Sceglie cosa ridire e cosa no. Non è pettegola."
  - Note e vincoli: "Mai Liù che resta in scena a lungo — entra, dice, va. Mai Liù che fa la pettegola per cattiveria. Mai Liù in scene serie come voce comica. Mai Liù che sa cose che il narratore ha esplicitamente nascosto al lettore."
- `pipeline_narrativa/story_graph.json#entities.characters.liu`: `species: libellulina`, `type: cucciolo_scuola`, `role_saga: presenza_aerea_discreta`, `constraints: []`.
- `pipeline_narrativa/story_graph.json#stories.s06.characters_in_scene[liu].scene_role`: "cammeo_volante_messaggera_prima_apparizione_vera".
- `pipeline_narrativa/story_graph.json#stories.s08.characters_in_scene[liu].scene_role`: "messaggera_aerea_annuncio_fenomeno_raro_come_ipotesi".
- `pipeline_narrativa/story_graph.json#stories.s09.characters_in_scene[liu].scene_role`: "cucciolo_scuola_presenza_aerea_fonte_informale_notizia".
- `pipeline_narrativa/story_graph.json#stories.s11`: "LIU_ASSENTE_S11_DISCREPANZA_ARCHI_TABELLA_VS_DETTAGLIO_RISOLTA_DETTAGLIO_WINS".
- `pipeline_narrativa/story_graph.json#stories.s12.characters_in_scene[liu].scene_role`: "cammeo_apertura_portatrice_notizie_prima_a_chiamarlo_suonano_nome_installato".
