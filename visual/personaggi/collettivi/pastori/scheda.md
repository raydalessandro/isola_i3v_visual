---
id: pastori
name: Pastori
famiglia: personaggio
sottotipo: collettivo
specie: animali_misti_pastori_stagionali
tipo_grafo: gruppo_istituzione
ruolo_saga: sfondo_stagionale_coltivatori_del_vento_nord
status: provvisorio
ultima_modifica: 2026-04-30
fonti: ["pipeline_narrativa/story_graph.json#entities.characters.pastori"]
appare_in_storie: []
relazioni:
  dimora: pascoli_alti
  quadrante_grafo: aria_nord
  related_to: []
  cross_skill:
    cartografia: null
---


# Pastori

> **Stato compilazione:** body provvisorio, generato dal travaso meccanico Bible→catalogo il 2026-04-28. Le sezioni con `_da popolare dal grafo_` saranno completate da Ray quando ragionerà sul grafo.

## Identità visuale (sintesi)


**Ruolo saga:** sfondo_stagionale_coltivatori_del_vento_nord.
**Tipo:** gruppo_istituzione.
**Specie:** animali_misti_pastori_stagionali.
**Dimora:** pascoli_alti (quartiere: aria_nord).


## Aspetto / forma

Gruppo-istituzione di animali misti, pastori stagionali, che vive sui **Pascoli Alti** — prati estesi in pendenza dolce dove pascolano capre e pecore di alcune famiglie. D'estate stanno in capanne stagionali sui Pascoli Alti.

## Abbigliamento / stato d'uso

_da popolare dal grafo_

## Espressione / comportamento

Scendono con le greggi in autunno (S11). Non individuati. Funzionano come "Coltivatori del Vento Nord" — sfondo stagionale del Quartiere d'Aria.

## Saluto del gruppo

**Saluto:** uno scuotere del bastone da pastore, tre volte: due brevi e una lunga. **TIK-TIK-TIIK.** È il loro segnale di lavoro (orientare il gregge) che diventa anche segnale sociale.

**Logica.** I Pastori vivono sui Pascoli Alti. Il bastone è il loro strumento principale — guida il gregge, segna il passo, tiene d'equilibrio in pendenza. Il **TIK-TIK-TIIK** è un riadattamento del loro segnale di richiamo a uso sociale.

**Risposta dei fratelli.** Quando passano vicino, alzano una mano (come per i Camminanti), oppure picchiano due volte un sasso contro un altro sasso se ne hanno uno in mano (eco del bastone con strumenti diversi).

**Quote saga:** TIK-TIK-TIIK è onomatopea-firma nuova (non in lista §1.4 Carta Voce). Quota: max 3-4 storie su 12. Sentita più sui Pascoli (s02, s12) che altrove.

> *Esempio testuale (DOC_2 §2.5):*
> *Sui Pascoli, due pastori si fermarono per qualche secondo. Il bastone scese a terra: TIK-TIK-TIIK. I fratelli alzarono una mano.*

Fonte: `DOC_2_saluti_gruppi.md` §2.5 + §3.

## Palette e atmosfera

_da popolare dal grafo_

## Contesto e ambientazioni ricorrenti

**Pascoli Alti** (Quartiere d'Aria, nord): prati estesi in pendenza dolce, capre/pecore di alcune famiglie, capanne stagionali di Pastori d'estate. Nelle vicinanze: **Roccia Alta** (sperone panoramico a 2 ore di cammino), **Montagne Gemelle**.

## Coerenza cross-scena (cose che NON cambiano)

Gruppo di animali misti, mai individuati. Stagionalità: capanne sui Pascoli Alti d'estate, discesa con le greggi in autunno. Sempre come gruppo-istituzione, mai come singoli.

## Variabilità ammessa

Stagionalità: capanne sui Pascoli Alti d'estate; scendono con greggi in autunno (S11).

Altre variabilità: _da popolare dal grafo_

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

Vincolo dal grafo (`note`): "Gruppo-istituzione come coltivatori_del_cerchio. Scendono con greggi in autunno (S11). Non individuati."

Altri vincoli specifici: _da popolare dal grafo_

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
- s11: sfondo festa, scendono dai pascoli alti all'alba.
- s12: sfondo pascoli, brevissimi, Stria assente.

## Disallineamenti / domande aperte

- I Pastori NON hanno una sezione §4 dedicata nella Bible v2 (le sezioni §4.18-§4.21 coprono Coltivatori del Cerchio, Mercato del Mezzogiorno, Mantenitori, Camminanti; non c'è §4.22). L'unico riferimento Bible è in §8 ATLANTE (Pascoli Alti, "capanne stagionali di Pastori d'estate"). La scheda nasce in massima parte da `entities.characters.pastori` del grafo. Da chiarire con Ray se sia il caso di promuovere i Pastori a §4.22 in Bible v2.x oppure mantenerli come gruppo-istituzione tracciato solo nel grafo.

## Riferimenti puntuali (citazioni dirette dalle fonti)

- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §8 ATLANTE (Pascoli Alti):
  - "Pascoli Alti (prati estesi in pendenza dolce, capre/pecore di alcune famiglie, capanne stagionali di Pastori d'estate), Roccia Alta (sperone panoramico a 2 ore di cammino, da qui si vede tutta l'isola, Stria ci passa al mattino), Montagne Gemelle..."
- `pipeline_narrativa/story_graph.json#entities.characters.pastori`: `type: gruppo_istituzione`, `species: animali_misti_pastori_stagionali`, `home_location: pascoli_alti`, `quadrant: aria_nord`, `role_saga: sfondo_stagionale_coltivatori_del_vento_nord`, `note: "Gruppo-istituzione come coltivatori_del_cerchio. Scendono con greggi in autunno (S11). Non individuati."`
- `pipeline_narrativa/story_graph.json#stories.s11.characters_in_scene[pastori].scene_role`: "sfondo_festa_scendono_dai_pascoli_alti_alba".
- `pipeline_narrativa/story_graph.json#stories.s12.characters_in_scene[pastori].scene_role`: "sfondo_pascoli_brevissimi_stria_assente".
