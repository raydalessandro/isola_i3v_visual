---
id: <id_snake_case>
name: <Nome Visualizzato>
famiglia: personaggio
sottotipo: <bambini | primari | secondari | cuccioli | collettivo>
specie: <specie>
tipo_grafo: <type dal grafo>
ruolo_saga: <role_saga dal grafo>
status: provvisorio
ultima_modifica: YYYY-MM-DD
fonti: ["pipeline_narrativa/story_graph.json#entities.characters.<id>"]
appare_in_storie: []
relazioni:
  dimora: <id_luogo|null>
  quadrante_grafo: <quadrant|null>
  related_to: []
  cross_skill:
    cartografia: <id_feature|null>
---


# <Nome Visualizzato>

> **Stato compilazione:** body provvisorio, completato YYYY-MM-DD con derivazione autoriale dalle fonti canoniche (Bible §X.Y; grafo entities.characters.<id>; Glossario §X.Y). Le sezioni in derivazione sono dichiarate in "Riferimenti puntuali".

## Identità visuale (sintesi)

**Ruolo saga:** <role_saga>.
**Tipo:** <type>.
**Specie:** <specie>.
**Ruolo familiare episodico:** <se applicabile, altrimenti omettere>.
**Dimora:** <id_luogo> (quartiere: <quadrant>).

[1 paragrafo di sintesi: cosa vede a colpo d'occhio chi lo incontra. 3-5 righe. Cita la specie, postura, tratto fisico più distintivo, firma visiva, modalità comportamentali se hanno aspetto visivo.]

## Aspetto / forma

[Descrizione fisica dettagliata. Travaso 1:1 dalla Bible §4.X "Aspetto." + derivazione autoriale per dettagli mancanti. Includere:
- Specie e postura (bipede stabile salvo eccezioni come Grunto)
- Statura relativa (a Gabriel come unità — vedi `02_SAGA_SCALE_v1.md`)
- Corporatura (asciutta, robusta, etc.)
- Pelo/piume/squame: colore, distribuzione, lunghezza, texture
- Dettagli specie-specifici (coda, orecchie, muso, becco, guscio, etc.)
- Occhi: colore, espressione canonica, eventuali pupille particolari
- Mani/zampe: come funzionano, "calzini" scuri se applicabili (volpe, tasso, etc.)
- Età narrativa indicativa (giovane/adulto/anziano + range equivalente umano)]

## Abbigliamento / stato d'uso

**Firma visiva (canone):** [travaso 1:1 da Bible §4.X "Firma visiva"]

**Outfit canonico completo:**
[Derivazione autoriale per il vestiario completo se la Bible nomina solo la firma visiva. Includere:
- Capo principale (camicia/maglia/tunica) — colore, materiale, stile
- Pantaloni / gonna / zona inferiore — colore, materiale, lunghezza
- Calzature (o piedi nudi)
- Eventuali accessori (ma SEMPRE coerenti con cliché da evitare: niente gioielli decorativi)
- Coerenza con palette del quartiere di appartenenza]

**Stato d'uso:**
[Come si vede l'abbigliamento in scena: pulito/sporco, infarinato/asciutto, sgualcito/composto, eventuali macchie/usure tipiche, capelli/pelo della testa.]

## Espressione / comportamento

[Travaso 1:1 da Bible §4.X "Comportamento operativo." + codifica visiva delle modalità.]

**Modalità visivamente distinguibili (se applicabili):**

- **<Modalità A>** (default): [postura, mani, coda, sguardo, sopracciglia]
- **<Modalità B>** (rara): [come sopra]
- **<Modalità C>** (rarissima): [come sopra]

[Il punto è dare a un illustratore/AI uno schema di lettura che permetta di riconoscere a colpo d'occhio in che "stato emotivo/relazionale" è il personaggio in quella scena.]

## Palette e atmosfera

[Travaso da `_canone/03_SAGA_PALETTE_v1.md` per il personaggio. Includere:
- Colori principali del corpo (ordinati: dorso, ventre, dettagli, occhi, accessori)
- Colori dell'abbigliamento canonico
- Quartiere di appartenenza con i suoi toni
- Tipo di luce in cui il personaggio sta naturalmente (calda/fredda/neutra)
- Eventuali contrasti significativi (es: Fiamma porta calore in scene fredde)]

## Contesto e ambientazioni ricorrenti

[Travaso da Bible §4.X (specie/ruolo) + §8.X (atlante) per quartiere di vita. Includere:
- Dimora canonica
- Scene tipiche dove appare (con quartiere, contesto, modalità default)
- Posizione tipica nel frame (dietro al banco, in piedi sulla soglia, etc.)
- Tipo di ambienti dove appare in cammeo (mercato, festa, etc.)]

## Coerenza cross-scena (cose che NON cambiano)

[Lista bullet di tutto ciò che è canonico fisso. Da usare come checklist quando si valuta un'illustrazione nuova.]

- <tratto fisico fisso 1>
- <tratto fisico fisso 2>
- ...
- Postura bipede (o quadrupede per eccezioni)
- Outfit canonico (se non cambia mai)
- Eventuali firme visive intoccabili (cicatrici, marchi, accessori)

## Variabilità ammessa

[Cosa PUÒ variare scena per scena, sempre dentro il canone:
- Pose delle mani (lista delle pose canoniche ammesse)
- Posizione della coda / orecchie
- Espressione del muso (nella gamma delle modalità sopra)
- Stagione (variazioni invernali/estive ammesse)
- Luce (gamma di luci ammesse)
- Età narrativa (se applicabile)

E cosa NON varia mai:
- <riepilogo cose immutabili>]

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

**Da Bible §4.X "Note e vincoli":**
- [travaso 1:1 dei "Mai..."]

**Specifici visivi:**
- Mai <cliché 1 specifico per questo personaggio>
- Mai <cliché 2>
- ...

[Tipici da considerare per personaggi animali antropomorfi:
- Mai disney-cute con occhioni esagerati
- Mai sexy/glamour stylization
- Mai "saggio anziano" con barba bianca melodrammatica
- Mai "mascotte" con simbolo/oggetto magico
- Mai gioielli decorativi (a meno che siano firma visiva)
- Mai posa "eroe in posa" da fumetto
- Mai espressioni sopra le righe (urla, pianti, gioia esagerata)
- Mai effetti magici / aure / sparkle
- Mai posizione a quattro zampe (per bipedi)]

## Per stampa 3D

- **Scala**: dipendente dalla scala canonica saga (toy 1:6 vs miniatura 1:24 — da fissare).
- **Postura canonica per la veduta principale**: [postura neutra di riferimento]
- **4 vedute consigliate**: fronte, retro, profilo dx, profilo sx.
- **Geometria**: [note specifiche al personaggio: posture, parti separate vs integrate, etc.]
- **Materiale di stampa consigliato**: [PLA/resina + indicazioni colore RAL/Pantone]
- **Punti critici**: [parti sottili, fragili, da supportare]
- **Orientamento di stampa**: [posizione consigliata]

_Scala canonica precisa rinviata a definizione saga. Indicazioni qualitative restano valide proporzionalmente._

## Per narrativa e social

[Vedere file `descrizione_narrativa_social.md` nella stessa cartella per i testi standalone. Qui solo regole d'uso interne:]

**Registri d'uso testuale:**
- Voce narrante: <"<Nome>" / "il/la <specie>" / etc. — quale uso è canonico>
- Come lo chiamano i fratelli in dialogo
- Come NON va mai introdotto in narrazione (avverbi vietati, formule cliché)
- Limiti sulla descrizione (mai aggiungere tratti fuori canone in narrativa nuova)

## Storie / scene di apparizione

[Lista derivata dal grafo: per ogni s01..s12 dove l'entità compare, una riga col ruolo/scena breve.]

- s01: <ruolo>.
- s02: <ruolo o "assente">.
- ...
- s12: <ruolo>.

## Disallineamenti / domande aperte

[Conflitti rilevati durante la compilazione, derivazioni che hanno fatto scelte non banali e che andrebbero validate da Ray, dati mancanti che vanno fissati.]

## Riferimenti puntuali (citazioni dirette dalle fonti)

**Fonti canoniche dirette:**
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §<X.Y>: "<citazione esatta>"
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §6 PALETTE VISIVA: "<citazione palette>"
- `worldbuilding/GLOSSARIO_ISOLA.md` §<X.Y>: "<citazione>"
- `pipeline_narrativa/story_graph.json#entities.characters.<id>`: <campi grafo>
- `pipeline_narrativa/story_graph.json#stories.s0X.characters_in_scene[<id>].scene_role`: "<scene_role>"

**Derivazioni autoriali (dichiarate):**
- *<elemento derivato 1>*: derivato da <fonte>. Motivazione: <perché>.
- *<elemento derivato 2>*: derivato da <fonte>. Motivazione: <perché>.
- ...

**Cliché da evitare specifici visivi**: derivati da `PATTERN_AI_DA_BANDIRE_v1.md` applicato al caso specifico <specie + ruolo>.
