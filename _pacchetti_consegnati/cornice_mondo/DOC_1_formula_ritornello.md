# DOC 1 — Formula del ritornello "che animale è"

> **Scopo.** Definire il ritornello con cui i tre fratelli e il narratore identificano l'individuo anonimo di un gruppo-istituzione ogni volta che ne incontrano uno. È un evento ricorrente, riconoscibile a ogni storia, che il bambino impara a aspettare.
>
> **Dove va nel grafo.** Quando lo formalizzeremo: nodo radice del grafo, sezione `world_conventions.refrain_animal_identification` (campo nuovo, additivo). Tracciato per quote_tracker e applicato nelle cornici di ogni storia.
>
> **Stato:** proposta operativa.

---

## §1. La formula scelta

```
Era un/una <ruolo del gruppo> — quale, oggi? Una/Un <animale>.
```

**Esempi:**
- *Era un mantenitore — quale, oggi? Una donnola.*
- *Era una camminante — quale, oggi? Una talpa.*
- *Era un pastore — quale, oggi? Una marmotta.*
- *Era una venditrice del mercato — quale, oggi? Un riccio.*

**Ritmo:** ad alta voce batte un settenario abbastanza pulito, con la pausa-respiro al trattino. La domanda *"quale, oggi?"* è la chiave — il *"oggi"* dice al bambino *che ieri era un altro, domani sarà un altro ancora*. È la seconda lettura.

---

## §2. Variante per gruppi in fila / corale

Quando il gruppo è visto al lavoro corale (Coltivatori in fila negli Orti, Pastori che scendono con le greggi):

```
Erano i/le <gruppo> — chi, oggi? Una/Un <animale>, una/un <animale>, una/un <animale>.
```

**Esempi:**
- *Erano i coltivatori del cerchio — chi, oggi? Una marmotta, una talpa, una lepre.*
- *Erano i pastori che scendevano — chi, oggi? Un cinghiale, un asino, una capra.*

**Vincoli:**
- Tre nomi, mai due, mai quattro. Il ritmo di tre regge il piede.
- Almeno uno degli animali deve essere insolito o specifico (capra è banale, donnola no). Mix di consueto e ricercato.
- Mai più di una formula plurale per storia.

---

## §3. Vincoli di applicazione

### §3.1 A chi si applica

**Solo agli individui anonimi dei 5 gruppi-istituzione:**
- Camminanti
- Mantenitori
- Coltivatori del Cerchio
- Mercato del Mezzogiorno (venditori, non Vecchie del Mercato)
- Pastori

### §3.2 A chi NON si applica

**Mai ai personaggi nominati.** Fiamma è una volpe rossa per sempre, Stria è un airone cenerino per sempre. La specie loro è canone, non si rinomina mai.

**Mai alle Vecchie del Mercato.** Sono umane, è già nel grafo (`representation_constraint: mai_antropomorfizzate_come_vecchiette_personaggio`). Restano coralità silenziosa.

**Mai ai cuccioli protagonisti** (Pun, Toba, Bru, Cardo, Liù). Sono nominati e fissi.

### §3.3 Quando si attiva

- Solo al **primo incontro** di un membro del gruppo nella storia.
  - Se in s06 si vedono tre Camminanti diversi nella stessa giornata, la formula si applica solo al primo.
  - Per gli altri due si dirà semplicemente *"un altro camminante"* o *"una camminante carica"* — niente specie.
- **Eccezione doppia formula:** se nella stessa storia si vedono membri di due gruppi diversi (es. Camminante + Mantenitrice), la formula si applica una volta per ciascun gruppo. Massimo 2 formule per storia.
- Se l'apparizione è puramente di sfondo (es. *"in lontananza tre Coltivatori"* senza interazione), la formula si può **omettere**. Il giudizio sta nel fatto: è incontro o è paesaggio?

### §3.4 Quote saga

- Massimo **2 formule per storia** (1 singolare + 1 plurale, oppure 2 singolari di gruppi diversi).
- Stagionalità nel rispetto del grafo: se in una stagione un gruppo non è attivo (Pastori d'inverno: stanno nelle capanne, raramente scendono), niente formula.
- **Tracciato** in `quote_tracker.refrain_animal_used_per_story` (lista di tuple `[storia, gruppo, animale]`).
- **Vincolo di non-ripetizione di animale:** lo stesso animale non può apparire come individuo del gruppo due volte in tutta la saga. Donnola in s05? Mai più donnola altrove. Forza varietà ecologica.

---

## §4. Pool degli animali assegnabili

Lista di animali utilizzabili come "individui dei gruppi". Si può estendere ma è una base. Vincolo: nessuno di questi è già un personaggio nominato del catalogo.

**Mammiferi piccoli:** talpa, donnola, faina, ermellino, riccio (eccezione: Mèmolo è riccio nominato — usare con cura), arvicola, ghiro, marmotta, scoiattolo (con cautela: Zolla è scoiattolo grigio — non usare scoiattolo grigio per i gruppi).

**Mammiferi medi:** lepre (eccezione: Salvia è lepre — usare con cura per gruppi diversi dal Quartiere di Terra), volpe (eccezione: Fiamma è volpe rossa — usare solo volpi non-rosse: volpe argentata, volpe della sabbia), tasso (eccezione: Rovo è tasso, Bru è tassino — non usare tassi), cinghialino, capriolo, daino.

**Domestici/lavoro:** capra, pecora, asino, mulo (per Pastori e Camminanti soprattutto), cane da pastore.

**Uccelli:** allodola, pettirosso, fringuello, capinera, rondine, gazza, cornacchia, tortora, poiana, gheppio (escludere airone, cenerino: Stria; cormorano: Amo; picchio: Nodo; libellula: Liù — anche se libellula non è uccello, comunque è preso).

**Anfibi/rettili (con cautela, max 1-2 in saga):** rospo, rana di palude, ramarro, lucertola.

### §4.1 Animali da escludere a priori

**Tutti gli animali-personaggio del catalogo** (per evitare confusione tra individuo del gruppo e personaggio canonico):

- volpe rossa (Fiamma)
- airone cenerino (Stria)
- riccio adulto (Mèmolo) — *riccino può apparire con cautela, è specie del cucciolo Pun*
- tartaruga di mare anziana (Bartolo)
- tasso (Rovo) e tassino (Bru)
- stambecco verde vecchio (Grunto)
- lepre (Salvia)
- picchio (Nodo)
- cormorano (Amo)
- scoiattolo grigio anziano (Zolla)
- riccino (Pun) — eccezione: riccino diverso non si distingue facilmente, evitare
- tartarughina (Toba)
- lupacchiotto (Cardo)
- libellulina (Liù)

**E animali canonicamente assenti dal mondo isola** (da grafo/Bible se elencati): se la Bible esclude qualche specie dall'isola, escluderla dal pool.

---

## §5. Esempi applicati alle storie già scritte

> *Solo per mostrare come funzionerebbe inserito nelle narrazioni fattuali. Non sono ancora nel grafo.*

**S07 — La Zattera dei Tre Rametti.** I tre fratelli, scendendo lungo il Fiume, vedono dall'altra parte qualcuno che cammina con la carriola di vimini.

> *Sull'altra sponda passava una camminante. Quale, oggi? Una talpa. Aveva la carriola piena di sacchi.*

**S08 — L'Albero che Cadde di Sera.** Quando i Mantenitori arrivano alla piazza con scale e lanterne dopo il crack del noce.

> *Quattro mantenitori arrivarono con le scale. Quale, oggi? Una donnola, un'arvicola, un ghiro, una faina. Sapevano cosa fare.*

(Variante plurale, perché sono in gruppo.)

**S11 — La Festa del Raccolto.** Una venditrice del mercato porge un frutto a Noah.

> *Era una venditrice del mercato — quale, oggi? Un fringuello. Mise una mela in mano a Noah, senza chiedere.*

---

## §6. Decisioni rimaste aperte

- **Posizione tipografica della formula nel testo finale.** Inline nel paragrafo (come negli esempi sopra), oppure a riga propria/isolata visivamente come le onomatopee della Carta Voce §1.4? Suggerimento: **inline**, ma con il trattino lungo che fa la pausa. La isolata visiva la riserviamo alle onomatopee.
- **Variazione lieve consentita?** Se sì, di che tipo? Es. *"Era un mantenitore — quale, oggi? Una donnola, oggi."* (ripetizione del *"oggi"* per enfasi finale). La mia raccomandazione: **mai variare la formula nei primi 4-5 incontri di saga**, poi ammettere 1-2 micro-varianti nelle ultime storie come "il narratore si scioglie un po'". Ma è scelta autoriale tua.
- **Decidere il pool definitivo degli animali assegnabili.** Quello che ho dato qui è una proposta. Si può rifinire prima di assegnarli alle cornici.
