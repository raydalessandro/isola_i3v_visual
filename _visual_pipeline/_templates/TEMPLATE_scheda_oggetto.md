---
id: <id_snake_case>
name: <Nome Visualizzato>
famiglia: oggetto
sottotipo: <null|oggetto_naturale_trovato|oggetto_pratico_di_casa|oggetto_rituale_fatto_a_mano|firma_visiva_personaggio|...>
status: provvisorio
ultima_modifica: YYYY-MM-DD
fonti: ["pipeline_narrativa/story_graph.json#entities.objects.<id>"]
appare_in_storie: []
relazioni:
  associato_a_personaggio: <id|null>
  associato_a_luogo: <id|null>
---


# <Nome Visualizzato>

> **Stato compilazione:** body provvisorio, completato YYYY-MM-DD con derivazione autoriale dalle fonti canoniche (Bible §X.Y; grafo entities.objects.<id>; Glossario §X.Y). Le sezioni in derivazione sono dichiarate in "Riferimenti puntuali".

## Identità visuale (sintesi)

**Categoria:** <category>.
**Proprietario:** <id|null>.
**Luogo associato:** <id|null>.

[1 paragrafo: cosa è e cosa rappresenta. 2-4 righe.]

## Aspetto / forma

[Descrizione fisica dettagliata. Travaso 1:1 da Bible se presente + derivazione autoriale. Includere:
- Tipo di oggetto
- Materiali
- Forma e dimensioni
- Lavorazione / tecnica costruttiva
- Eventuali elementi distintivi (bottoni, lacci, fibbie, intagli, ecc.)]

## Abbigliamento / stato d'uso

[Solo per oggetti indossabili o oggetti d'uso quotidiano:
- Come si vede l'oggetto in scena
- Stato d'uso tipico (nuovo / usato / consumato)
- Patine, sporcizia, segni d'uso]

## Espressione / comportamento

[Per oggetti animati/firma visiva: come si comporta nelle scene.
- Posizione tipica (legato, appeso, indossato, posato)
- Movimento (oscilla, sta fermo, si sposta col proprietario)
- Interazione col proprietario (toccato, sistemato, dimenticato)]

## Palette e atmosfera

[Travaso da `_canone/03_SAGA_PALETTE_v1.md`:
- Colori principali dell'oggetto
- Coerenza con palette del proprietario / quartiere associato
- Tipo di luce in cui appare tipicamente]

## Contesto e ambientazioni ricorrenti

[Travaso da Bible / grafo:
- Dove appare normalmente
- Con chi appare
- In quali scene è centrale, in quali è cammeo]

## Coerenza cross-scena (cose che NON cambiano)

- <materiale fisso>
- <colore fisso>
- <forma fissa>
- <dimensioni fisse>
- <stato d'uso fisso (es: "sempre infarinato")>

## Variabilità ammessa

[Cosa PUÒ variare scena per scena:
- Posizione esatta delle macchie / segni d'uso
- Quantità di farina / sporcizia
- Posizione di lacci / nodi
- Posa relativa al proprietario

E cosa NON varia:
- <riepilogo cose immutabili>]

## Cliché da evitare

Riferimento globale: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`.

**Specifici per oggetti:**
- Mai oggetti "magici" / luminescenti / con aura.
- Mai oggetti "sacrali" caricati di simbolismo esplicito.
- Mai oggetti "perfettamente nuovi" o "perfettamente puliti" se sono d'uso quotidiano.
- Mai decorazioni superflue (ricami, pizzi, gemme, intarsi) se non canoniche.
- Mai oggetti drammatici (rotti, sanguinanti, bruciati gravemente) se non canonici.
- Mai personificazioni (oggetti che "raccontano storie", "custodiscono memorie").
- [aggiungere cliché specifici dell'oggetto]

## Per stampa 3D

- **Scala**: dipendente dalla scala canonica saga e dal proprietario (vedi `_canone/02_SAGA_SCALE_v1.md`).
- **Geometria**: [descrizione tecnica del modello 3D]
- **Materiale di stampa consigliato**: [PLA/resina + colore RAL/Pantone]
- **Punti critici**: [parti sottili, fragili]
- **Orientamento di stampa**: [posizione consigliata]

## Per narrativa e social

[Vedere `descrizione_narrativa_social.md` nella stessa cartella.]

**Registri d'uso testuale:**
- Come nominarlo in narrazione: "il <oggetto>" / "<Nome>"
- Mai personificarlo
- Mai usarlo come simbolo esplicito

## Storie / scene di apparizione

[Lista derivata dal grafo + dal proprietario.]

- s01: <ruolo o "assente">.
- ...

## Disallineamenti / domande aperte

[Conflitti, derivazioni non banali, dati mancanti.]

## Riferimenti puntuali (citazioni dirette dalle fonti)

**Fonti canoniche dirette:**
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §<X.Y>: "<citazione>"
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §6 PALETTE VISIVA: "<citazione>"
- `worldbuilding/GLOSSARIO_ISOLA.md` §<X>: "<citazione>"
- `pipeline_narrativa/story_graph.json#entities.objects.<id>`: <campi grafo>

**Derivazioni autoriali:**
- *<elemento derivato>*: derivato da <fonte>. Motivazione: <perché>.
