---
id: memolo
name: Memolo
famiglia: personaggio
sottotipo: primari
specie: riccio
tipo_grafo: abitante_maggiore
ruolo_saga: cambio_di_registro_colpo_di_coda
status: provvisorio
ultima_modifica: 2026-04-28
fonti: ["pipeline_narrativa/story_graph.json#entities.characters.memolo"]
appare_in_storie: []
relazioni:
  dimora: casetta_tonda_piazza_centrale
  quadrante_grafo: centro_villaggio
  related_to: [pun]
  cross_skill:
    cartografia: null
---

# Memolo

> **Stato compilazione:** body provvisorio, generato dal travaso meccanico Bible→catalogo il 2026-04-28. Le sezioni con `_da popolare dal grafo_` saranno completate da Ray quando ragionerà sul grafo.

## Identità visuale (sintesi)

_da popolare dal grafo_

## Aspetto / forma

Piccolo, tondo, con le spine corte e morbide del riccio adulto che non ha più paura di niente. Il muso lungo, gli occhi neri e attenti — più attenti di quanto si direbbe da come cammina. Si confonde nei propri passi quando va di fretta.

## Abbigliamento / stato d'uso

**Firma visiva:** una piccola sciarpa annodata sul collo, sempre annodata male, che sistema mille volte al giorno e non resta mai dritta.

## Espressione / comportamento

Mèmolo fa cose-da-riccio. Esce piano, esita sulla soglia. Si arrotola quando una cosa lo spaventa o lo confonde — gesto fisico vero, brevissimo. Trotterella veloce per piccoli tratti, poi si ferma e dimentica perché è uscito. Inciampa nelle proprie spine — *"ahi"* — e poi ride. Conosce le buche e le radici della piazza meglio di chiunque, perché ci passa da sotto. Sta vicino alla terra.

Confonde i nomi degli abitanti, si dimentica le commissioni. Ma una volta a storia, nel mezzo della confusione, dice una cosa **incredibilmente precisa** — come se per un attimo avesse visto tutto chiaramente. Poi torna confuso. Lui per primo non si accorge di averlo detto.

## Palette e atmosfera

_da popolare dal grafo_

## Contesto e ambientazioni ricorrenti

Abitante del villaggio centrale — sta in una casetta tonda nascosta dietro un cespuglio sulla piazza, vicino all'Albero Vecchio. Non ha mestiere fisso. Padre di Pun.

## Coerenza cross-scena (cose che NON cambiano)

Piccolo e tondo. Spine corte e morbide del riccio adulto. Muso lungo, occhi neri attenti. Sciarpa annodata male sul collo, sistemata mille volte e mai dritta.

## Variabilità ammessa

_da popolare dal grafo_

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

Da Bible §4.7 "Note e vincoli":
- Mai un Memolo "sapientemente confuso" che fa il finto tonto per insegnare. La sua precisione deve sembrare casuale.
- Mai due frasi-precise nella stessa storia.
- Mai usare Memolo per *risolvere* un problema della trama — può aprire una via, mai chiuderla.
- Pun (suo cucciolo) non lo addomestica.

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
- s06: oggetto del dono e cornice di apertura/chiusura.
- s07: assente.
- s08: zio buffo in confusione seria.
- s09: cammeo tenero — primo bloom parziale (seed Memolo sul Pozzo con Gabriel).
- s10: assente.
- s11: zio buffo, presenza confusa alla festa.
- s12: assente.

## Disallineamenti / domande aperte

- Il grafo usa l'id `memolo` (senza accento). La Bible §4.7 usa **"Mèmolo"** (con accento grave su È). Il display name nel frontmatter dovrebbe essere "Mèmolo"? Se sì, il fix va nel grafo (`entities.characters.memolo.name = "Mèmolo"`) e poi rilancio dello script visual per propagare.

## Riferimenti puntuali (citazioni dirette dalle fonti)

- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §4.7 MÈMOLO:
  - "Riccio. Abitante del villaggio centrale — sta in una casetta tonda nascosta dietro un cespuglio sulla piazza, vicino all'Albero Vecchio. Non ha mestiere fisso. Padre di Pun."
  - "Piccolo, tondo, con le spine corte e morbide del riccio adulto che non ha più paura di niente. Il muso lungo, gli occhi neri e attenti — più attenti di quanto si direbbe da come cammina. Si confonde nei propri passi quando va di fretta."
  - "Firma visiva: una piccola sciarpa annodata sul collo, sempre annodata male, che sistema mille volte al giorno e non resta mai dritta."
  - "Mèmolo fa cose-da-riccio. Esce piano, esita sulla soglia. Si arrotola quando una cosa lo spaventa o lo confonde... Trotterella veloce per piccoli tratti, poi si ferma e dimentica perché è uscito. Inciampa nelle proprie spine — 'ahi' — e poi ride. Conosce le buche e le radici della piazza meglio di chiunque, perché ci passa da sotto. Sta vicino alla terra."
  - "Confonde i nomi degli abitanti, si dimentica le commissioni. Ma una volta a storia, nel mezzo della confusione, dice una cosa incredibilmente precisa — come se per un attimo avesse visto tutto chiaramente. Poi torna confuso. Lui per primo non si accorge di averlo detto."
  - Note e vincoli: "Mai un Mèmolo 'sapientemente confuso' che fa il finto tonto per insegnare. La sua precisione deve sembrare casuale. Mai due frasi-precise nella stessa storia. Mai usare Mèmolo per risolvere un problema della trama — può aprire una via, mai chiuderla. Pun (suo cucciolo) non lo addomestica."
- `pipeline_narrativa/story_graph.json#entities.characters.memolo`: `species: riccio`, `type: abitante_maggiore`, `role_saga: cambio_di_registro_colpo_di_coda`, `home_location: casetta_tonda_piazza_centrale`.
- `pipeline_narrativa/story_graph.json#stories.s06.characters_in_scene[memolo].scene_role`: "oggetto_del_dono_e_cornice_apertura_chiusura".
- `pipeline_narrativa/story_graph.json#stories.s08.characters_in_scene[memolo].scene_role`: "zio_buffo_in_confusione_seria".
- `pipeline_narrativa/story_graph.json#stories.s09.characters_in_scene[memolo].scene_role`: "cammeo_tenero_primo_bloom_parziale_seed_memolo_sul_pozzo_con_gabriel".
- `pipeline_narrativa/story_graph.json#stories.s11.characters_in_scene[memolo].scene_role`: "zio_buffo_presenza_confusa_festa".
