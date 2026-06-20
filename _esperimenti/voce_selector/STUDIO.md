# Studio — il selettore "La Voce" alla prova della scrittura

**Data:** 2026-06-20 · **Branch:** claude/la-voce-selector-ovppf8 · **Stato:** esperimento, NON canone

## Domanda

Il selettore "La Voce" (4 assi: respiro × luce × narratore × verso = 54 voci) promette che
«cambia una sola risposta e sei in una voce adiacente». Due voci sono collaudate (Σ111− Isola,
Σ333+ Soglia); le altre 52 hanno solo una *ricetta di resa*. Domande:

1. Le ricette **reggono** alla scrittura vera, o sono fuffa?
2. Il sistema **discrimina** davvero? Cambiare un asse muove la prosa?
3. I 4 assi pesano **uguale**? Quante voci *percettivamente distinte* esistono davvero?

## Metodo

Stesso hook (`s01_h04`, la nebbia), stesso contesto invariante (fatti, voci dei fratelli, tabù
universali). Unica variabile: il blocco §10 **generato dal selettore stesso** (`gen_brief.js`,
estrazione fedele di `testoBriefer()`). 6 agenti prosa in parallelo, modello identico. Disegno a
un asse di distanza dall'ancora Isola + angolo opposto:

| Σ | mossa dall'ancora | narratore | n. parole | fatto-sigillo prodotto |
|---|---|---|---|---|
| 111− | — (control Isola) | Δ sottrae | 78 | sasso che rotola e tace |
| 211− | respiro: taglio→intreccio | Δ sottrae | 92 | brina sotto le scarpe / pietra che smette |
| 131− | luce: giorno→soglia | Δ sottrae | 96 | pietra che si spegne nel bianco |
| 113− | narratore: sottrae→gira | ⟳ inverte | 104 | bianco «pieno come una notte accesa» |
| 111+ | verso: raccolto→disteso | Δ sottrae | 84 | goccia da un filo d'erba |
| 333+ | — (control Soglia, angolo opposto) | ⟳ inverte | 96 | «pieno che era come la notte» |

Output integrali in `output/raccolta_output.md`.

## Risultati

### 1. Le ricette reggono — sì. (esito netto)
Tutte e 6 le rese sono pubblicabili, on-brand, rispettano i tabù universali (nebbia mai agente,
Gabriel tace come da fatti, nessuna morale, nessun marcatore AI). **Le 4 voci non-collaudate non
sono distinguibili in qualità dalle 2 collaudate.** La ricetta-di-resa funziona come brief: è
sufficiente a produrre voce coerente. È il risultato più importante per la pipeline — il selettore
è usabile *adesso*, non solo sulle 2 voci già scritte.

### 2. I due control si auto-riproducono senza copiare. (validazione)
- Σ111− ha generato «un sasso rotolò e poi tacque», fratello dell'esempio-firma «una capra rispose
  a un'altra capra»: stessa operazione, lessico nuovo.
- Σ333+ ha prodotto «così pieno che era come la notte» contro il riferimento collaudato «così pieno
  che era come il buio». Stessa inversione, parole fresche, anti-copia.

Segnale forte: la §10 codifica l'**operazione**, non l'esempio. La voce è riproducibile.

### 3. I 4 assi NON pesano uguale. (il risultato che conta)

**NARRATORE = asse primario.** È l'unico che cambia la *struttura del senso* della pagina, non
solo la superficie. Le 4 voci a sottrazione (111−, 211−, 131−, 111+) si **assomigliano molto** tra
loro; le 2 a inversione (113−, 333+) staccano nettamente («il bianco pieno come il buio»). Il
selettore lo dice già di sé («è l'operazione più appariscente, va dosata o mangia le altre») — qui
si conferma: **l'asse narratore domina la percezione della voce.**

**RESPIRO = asse secondario, ma compresso dal registro.** L'intreccio (211−) si vede — «un passo
e poi un passo», l'erba legata alla pietra in un periodo solo — ma resta timido: il tabù universale
picture-book (§10.6: «frasi corte, mai subordinate concatenate») **combatte** l'asse intreccio.
Conflitto reale tra un asse del selettore e un invariante della saga. Il ripiegamento (333+) si
vede meglio perché la ripetizione musicale è compatibile col registro breve.

**LUCE = asse scena-dipendente.** Su QUESTA scena (nebbia: niente forno/pane, niente alba/riva) la
luce quasi non si muove. Il giorno (111−) non può mostrare la sua palette (non c'è pane in cima a
una montagna nella nebbia); la soglia (131−) se la cava in astratto col confine («un braccio di
distanza, e poi il niente»), ma è sottile. **Su una scena al Forno o all'alba questo asse
spaccherebbe; qui collassa.** La luce non è una proprietà della voce: è una proprietà
dell'incontro voce×scena.

**VERSO = asse quasi cosmetico.** 111+ disteso differisce da 111− quasi solo per impaginazione (una
frase per riga, più stacchi). Nessun cambio sostanziale di lessico o sintassi: «più aria» = più a
capo. È più un parametro di *typesetting* che un asse di voce.

### 4. Convergenza indesiderata sull'esempio. (difetto di design del brief)
Tre voci a sottrazione su quattro hanno raggiunto lo **stesso identico prop**: una pietra/sasso che
rotola e si spegne. È l'esempio «una capra rispose a un'altra capra» che sovra-ancora: avendo *un
solo* esempio nel blocco §10, le voci-sottrazione convergono. La nebbia + montagna spinge tutti
sul sasso. Effetto-fotocopia da correggere.

## Implicazioni per il selettore

1. **54 voci è il conteggio combinatorio, non quello percettivo.** Stima realistica delle famiglie
   *distinguibili* a orecchio: **~3 (narratore) × 2 (respiro, dove il registro lo concede) ≈ 6**,
   con luce e verso come rifinitura che registra solo sulla scena giusta. Vale la pena dirlo nel
   footer del tool: gli assi non sono ortogonali né equipesati.
2. **Pesare gli assi nella UI.** Narratore andrebbe presentato come la scelta portante (cambia la
   storia), verso come microregolazione. Oggi i 4 assi hanno lo stesso peso visivo: fuorviante.
3. **Conflitto respiro×registro.** Le voci a intreccio/ritorno vanno calibrate contro il tabù
   «frasi corte». O si ammorbidisce il tabù per quelle voci, o si avvisa che intreccio in picture
   book resta sempre un mezzo-intreccio.
4. **Luce va etichettata come scena-dipendente.** Magari il tool potrebbe segnalare «questo asse
   rende molto su scene con palette forte (forno, alba, riva), poco su scene neutre».
5. **L'anteprima/ricetta dovrebbe offrire 2-3 esempi di fatto-sigillo**, non uno, per evitare la
   convergenza sullo stesso prop.

## Limiti dell'esperimento

- Un solo hook, una sola storia, un solo giro per voce (no varianza interna).
- La nebbia è una scena a bassa affordance di palette: penalizza apposta l'asse luce — utile per
  isolarlo, ma non rappresentativo.
- Le frasi-codice dei fratelli non sono bloccate su p4 (Gabriel tace): la pagina misura il
  *narratore* più dei *dialoghi*. Un hook con frase-codice forte (es. p5 «No. Non muoverci.»)
  misurerebbe meglio quanto la voce regge attorno a un vincolo verbale fisso.

## Da decidere con Ray

- Il selettore resta strumento sperimentale o lo si promuove a parte della pipeline brief (§10
  sostituibile da `testoBriefer`)?
- Si tiene il conteggio "54" o si rietichetta in famiglie pesate?
- Questo esperimento si archivia qui (`_esperimenti/`) o si butta?
