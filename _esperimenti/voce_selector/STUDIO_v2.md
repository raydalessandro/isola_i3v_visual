# Studio v2 — il briefer a meccanismo (A/B contro v1)

**Data:** 2026-06-20 · **Branch:** claude/la-voce-selector-ovppf8 · **Stato:** esperimento, NON canone

## Cosa cambia la v2 del selettore

La v2 riscrive il blocco §10 che riceve l'agente: le quattro voci non sono più descritte con
*firma + un esempio d'autore*, ma come **meccanismi** (fenomeno oggettivo, zero prop) + **test di
falsificazione** + **assi etichettati per peso** (narratore primario → respiro → luce
scena-dipendente → verso rifinitura). Gli esempi "caldi" restano solo nell'anteprima umana,
l'agente non li vede. Risponde in pieno ai due difetti che il run v1 aveva isolato:
(1) convergenza sullo stesso prop, (2) assi presentati come equipesati.

A/B pulito: **stesso hook, stesse 6 voci, stesso contesto invariante** del run v1. Unica variabile
cambiata = il briefer v1→v2. Output v2 in `output_v2/`, confronto qui.

## Risultato 1 — la convergenza è SPARITA (l'esito che conta)

Le quattro voci a sottrazione (Δ) producevano in v1, tre su quattro, **lo stesso prop**: una pietra
che rotola e si spegne (eco dell'unico esempio nel blocco). In v2, tolto l'esempio, ognuna istanzia
un correlato **diverso**, scelto sulla scena:

| voce | sigillo Δ in v1 | sigillo Δ in v2 |
|---|---|---|
| 111− | sasso che rotola e tace | **un piede sospeso, riposato dov'era** |
| 211− | brina / pietra che smette | **il fiato veloce che il bianco si beve** |
| 131− | pietra che si spegne nel bianco | **i piedi fermi sul margine del sentiero** |
| 111+ | goccia da un filo d'erba | **la mano sulla manica / l'erba bagnata / il bianco senza rumore** |

Conferma sperimentale: **era l'esempio a fare da calamita, non la scena.** Descrivere l'operazione
come meccanismo e togliere il prop libera l'invenzione. È la prova che il difetto era di
*design del brief*, non un limite del modello.

## Risultato 2 — il test di falsificazione diventa strumento operativo

In v2 gli agenti **applicano attivamente** il test nelle note: «regge anche sostituendo con un
altro fatto fisico (il respiro, le mani sulla giacca), quindi è correlato esterno e non simbolo»
(111−); idem 211−, 131−, 111+. Il test ha spostato l'operazione da *intuizione* a *procedura
verificabile*: l'agente si auto-debugga prima di consegnare. Disciplina più alta, meno rischio di
simbolo-travestito. Miglioria reale, non cosmetica.

## Risultato 3 — la luce "a vuoto" ora è principiata, non un collasso muto

In v1 l'asse luce sulla nebbia collassava in silenzio (nessuno sapeva perché il giorno non
"rendesse"). In v2 il meccanismo dichiara «asse scena-dipendente: sulla nebbia il magazzino è quasi
chiuso e l'asse gira a vuoto» — e gli agenti lo **riconoscono e lo rispettano**: «magazzino diurno
quasi chiuso dalla nebbia, l'asse gira a vuoto come prescritto», senza forzare immagini di forno in
alta quota. Il fallimento dell'asse è diventato un comportamento previsto e corretto, non un bug.
Le voci-soglia (131−, 333+) rendono il confine per **collocazione fisica** («sul margine del bianco,
dove finiva e non finiva»), meglio che in v1.

## Risultato 4 — effetti collaterali e un limite residuo

- **Inversione più astratta.** In v1 333+ diceva «il bianco… come la notte» (ancorato all'esempio
  luce). In v2 il meccanismo parla di saturazione generica («troppa luce, troppo suono, troppo
  pieno») e l'operazione si **generalizza**: «Era tanto pieno che sembrava vuoto» (333+), «tanto
  bianco che era come non vedere più niente» (113−). Più potente e meno copia-incolla; 333+ sfiora
  però la *dichiarazione* dell'equivalenza — al limite del proprio tabù (regge perché resta legata
  al bianco fisico, ma è il punto da sorvegliare).
- **La convergenza si è spostata, non annullata del tutto.** I correlati Δ ora divergono sul
  *narratore*, ma più voci ripiegano su un piccolo paniere di fatti fisici per i personaggi: «piedi
  fermi / restò dov'era» per la stasi di Gabriel, «fiato / freddo sulle mani» per Noah. **Non è un
  difetto del brief: è l'affordance della scena.** Una montagna vuota nella nebbia offre pochissimi
  oggetti; lo spazio dei "fatti laterali" è oggettivamente stretto. Su una scena ricca (Forno,
  Mercato) la divergenza sarebbe più ampia. Conferma indiretta del fatto che **luce/affordance è
  una proprietà della scena, non della voce.**

## Verdetto

La v2 **risolve** entrambi i difetti diagnosticati in v1 senza perdere qualità: le 6 rese restano
pubblicabili, on-brand, coi tabù rispettati, e ora si **distinguono meglio tra loro** (la firma
del narratore non è più mascherata da un prop condiviso). Il passaggio firma→meccanismo è un
miglioramento netto del brief, non un trade-off.

Resta vero il risultato strutturale di v1: **gli assi non pesano uguale** (narratore porta il
senso, verso è quasi tipografico) — ma adesso il selettore lo *dice* (etichette di peso nel blocco
e nel footer), quindi non è più un'insidia: è documentato.

## Da decidere con Ray
1. **Promozione.** La v2 mi pare pronta a sostituire la §10 di default nel `build_writing_brief`
   (blocco puro-meccanismo all'agente; esempi caldi solo nella UI). Vuoi che prepari la proposta di
   integrazione (manutentore, branch dedicata) o resta sperimentale?
2. **Sorveglianza inversione.** Vale la pena stringere il tabù di 333+ per evitare la quasi-
   dichiarazione («tanto pieno che sembrava vuoto»)? O va bene così finché resta legata al dato?
3. **Prossimo test mirato.** Ripetere su un hook a **frase-codice forte** (p5, «No. Non muoverci.»)
   per misurare la voce attorno a un vincolo verbale fisso — la nebbia p4 misura il narratore ma
   lascia liberi i dialoghi.
