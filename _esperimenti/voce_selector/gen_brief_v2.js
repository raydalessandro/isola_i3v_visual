/* v2 — Estrazione fedele del selettore "La Voce" v2 (meccanismo + falsificazione + assi pesati).
   testoBriefer v2: usa firma (meccanismo) + simbolo + falsif. NON include 'caldo' (esempi) né tabu per-asse.
   Uso: node gen_brief_v2.js 113−   (minus = U+2212) */

const RESPIRO = [
  {v:1, key:"taglio", t:"taglio", nome:"asciutta",
   firma:"Segmentazione massima del flusso: una proposizione porta una sola unità informativa, poi si chiude. Subordinazione ammessa solo quando la dipendenza è portante (causale o temporale reale), mai per accumulo. Confini di frase netti e frequenti.",
   falsif:"Applicata male se compaiono periodi con due o più subordinate concatenate, o se la frase corta è spezzata a effetto senza che il confine corrisponda a un confine informativo.",
   simbolo:""},
  {v:2, key:"intreccio", t:"intreccio", nome:"intrecciata",
   firma:"Coordinazione e subordinazione usate come legature: la frase tiene insieme due unità informative mettendole in relazione (apertura, ipotesi, richiamo a qualcosa di già detto). Il legame è la funzione, non l'ornamento. NB: confligge col taglio universale «frasi corte» — registro e asse vanno bilanciati, l'intreccio resta semplice.",
   falsif:"Applicata male se l'intreccio diventa arabesco (subordinate per estetica) o se, schiacciato dal tabù-frasi-corte, collassa di fatto in taglio: in quel caso l'asse non sta registrando.",
   simbolo:""},
  {v:3, key:"ritorno", t:"ritorno", nome:"che ritorna",
   firma:"Ripetizione parziale di un sintagma con variazione minima, a breve distanza: la seconda occorrenza riprende la prima e la sposta di poco, creando eco. Meccanismo prosodico, non semantico: aggiunge ritmo e chiusura, non informazione nuova.",
   falsif:"Applicata male se i ripiegamenti superano 1-2 per pagina o sono consecutivi (diventa cantilena), o se la variazione è nulla (ripetizione pura, non eco).",
   simbolo:""}
];
const LUCE = [
  {v:1, key:"giorno", t:"giorno", nome:"del giorno",
   firma:"Vincola il magazzino di immagini al campo semantico diurno-domestico: forno, pane, mercato, calore, lavoro, luce piena. Le cose sono date alla massima visibilità. NB asse scena-dipendente: registra solo se la scena offre quel campo (al Forno spacca; sulla nebbia il magazzino è quasi chiuso e l'asse gira a vuoto).",
   falsif:"Applicata male se il campo diurno è forzato in una scena che non lo contiene (immagini di forno in alta quota), o se il calore diventa morale (cibo-caldo-che-consola).",
   simbolo:""},
  {v:2, key:"notte", t:"notte", nome:"della notte",
   firma:"Vincola il magazzino al campo notturno: candela, buio, riflesso, acqua scura. Le cose sono date al lume piccolo o nel nero, dunque parzialmente. Asse scena-dipendente come sopra.",
   falsif:"Applicata male se la notte diventa agente (ascolta, si china) invece di ambiente, o se è decorativa e non cambia il modo in cui le cose sono date alla percezione.",
   simbolo:""},
  {v:3, key:"soglia", t:"soglia", nome:"della soglia",
   firma:"Vincola il magazzino al campo del confine: alba, tramonto, riva, margine, porta, mezz'ombra. Ogni cosa è data sul bordo tra due stati, mai in uno stato pieno. Asse scena-dipendente.",
   falsif:"Applicata male se la soglia diventa agente (il Burrone «chiama», l'acqua «vuole»), o se il «tra» è asserito invece di mostrato attraverso la collocazione fisica sul bordo.",
   simbolo:""}
];
const NARRATORE = [
  {v:1, key:"sottrazione", t:"sottrazione · Δ", nome:"che sottrae",
   firma:"Uno stato interno non è osservabile direttamente: si inferisce da correlati esterni. Dove la scena nominerebbe uno stato interno (paura, sollievo, attesa), rimuoverlo e lasciare sul posto un evento esterno concomitante e indipendente, dal quale l'osservatore ricostruisce lo stato senza che sia nominato.",
   falsif:"Applicata male se l'evento-sostituto è causato dallo stato o ne è metafora trasparente (correlazione spuria = simbolo). Test: sostituisci l'evento con un altro evento fisico qualunque della stessa scena; se l'operazione regge, è corretta; se solo quel preciso evento funziona, hai scritto un simbolo.",
   simbolo:""},
  {v:2, key:"nominazione", t:"nominazione · ⇄", nome:"che nomina",
   firma:"Una regione di un continuo percettivo priva di confine fisico discreto può riceverne uno linguistico: nominare un tratto continuo lo rende entità discreta, manipolabile, memorizzabile, ripetibile. Prendere un segmento non ancora segmentato (un'ora del giorno, una zona di luce, un punto di un percorso) e assegnargli un nome che lo discretizza; il nome entra nel lessico del mondo e diventa richiamabile.",
   falsif:"Applicata male se il nome descrive una cosa già discreta (ha già un nome comune) invece di tagliare un continuo, o se è ornamentale e non può tornare. Test: il nome dato deve poter essere riusato in una storia successiva come riferimento condiviso; se non è richiamabile, è decorazione.",
   simbolo:"Affine all'atto adamitico del nominare: dare nome è prendere possesso conoscitivo di una cosa prima indistinta."},
  {v:3, key:"inversione", t:"inversione · ⟳", nome:"che gira",
   firma:"Quando uno stimolo satura il canale percettivo (troppa luce, troppo suono, troppo pieno), il sistema perde la capacità di discriminare: l'eccesso di segnale produce lo stesso effetto della sua assenza. Registrare il punto di equivalenza in cui il massimo di una qualità coincide funzionalmente col suo opposto, sempre attraverso il dato fisico che lo causa, mai nominando l'equivalenza.",
   falsif:"Applicata male se l'equivalenza è dichiarata («capirono che la luce era come il buio») invece di prodotta dal dato fisico, o se compare più di 2 volte (satura essa stessa e schiaccia gli altri assi). Test: togliendo la frase che enuncia, l'inversione deve restare nell'immagine fisica; se sparisce, era spiegazione.",
   simbolo:"Affine alla coincidentia oppositorum: agli estremi i contrari si toccano. Usare solo come struttura sotto il dato, mai come affermazione."}
];
const VERSO = [
  {v:"+", key:"disteso", t:"+ disteso", nome:"distesa",
   firma:"Abbassa la densità di informazione per unità di riga: una proposizione per riga, più spazio bianco tra i blocchi, ritmo dilatato. Opera sulla resa tipografica e sul respiro, non sulla materia della frase.",
   falsif:"Applicata male se la dilatazione diventa riempitivo (parole in più senza funzione) invece che aria. Resta picture book: disteso non vuol dire lungo.",
   simbolo:""},
  {v:"−", key:"raccolto", t:"− raccolto", nome:"raccolta",
   firma:"Alza la densità di informazione per unità di riga: più proposizioni ravvicinate, bianco tipografico fitto, ritmo concentrato. Opera sulla resa, non sulla materia.",
   falsif:"Applicata male se la concentrazione è spezzettamento a effetto invece che densità reale di senso.",
   simbolo:""}
];
const COLLAUDATE = {"111−":{nome:"La voce dell'Isola"}, "333+":{nome:"La voce della Soglia"}};
const g=(a,v)=>a.find(o=>o.v===v);
function nomeVoce(k){ if(COLLAUDATE[k]) return COLLAUDATE[k].nome; const r=g(RESPIRO,+k[0]),l=g(LUCE,+k[1]); return "La voce "+r.nome+" "+l.nome; }
function testoBriefer(k){
  const r=g(RESPIRO,+k[0]), l=g(LUCE,+k[1]), n=g(NARRATORE,+k[2]), v=g(VERSO,k[3]);
  const linea=(label,o)=>{ let s="**"+label+".** Meccanismo: "+o.firma+"\n"; if(o.simbolo) s+="  · Strato simbolico: "+o.simbolo+"\n"; s+="  · Falsificazione: "+o.falsif+"\n"; return s; };
  let out = "## §10. VOCE — "+nomeVoce(k)+" (Σ"+k+")\n\n";
  out += "> Sostituisce la §10 di default del writing brief. Fatti, hook, cornici, frasi-codice (§§2-9) restano invariati: cambia solo la resa.\n";
  out += "> Le quattro voci sono descritte come MECCANISMI, non con esempi. Istanziare ogni meccanismo sulla scena presente. Non cercare un modello da imitare: applicare l'operazione.\n\n";
  out += "**Principio.** Una voce "+r.nome+", "+l.nome+", "+n.nome+", "+v.nome+". Stessi fatti del mondo, prodotti da queste operazioni.\n\n";
  out += "### Operazioni (in ordine di peso strutturale)\n\n";
  out += linea("NARRATORE — "+n.t+" · operazione PRIMARIA (struttura del senso)", n) + "\n";
  out += linea("RESPIRO — "+r.t+" · secondaria (sintassi)", r) + "\n";
  out += linea("LUCE — "+l.t+" · scena-dipendente (lessico)", l) + "\n";
  out += linea("VERSO — "+v.t+" · rifinitura (resa)", v) + "\n";
  out += "### Tabù universali\n";
  out += "Niente morale esplicita, niente framework EAR che affiora, niente marcatori AI, ambiente (notte/soglia) mai agente.\n\n";
  out += "### Invarianti (dal grafo, non modificabili)\n";
  out += "Voci dei tre fratelli: Gabriel Δ (decide netto, nei silenzi prima di parlare) · Elias ⇄ (apre, propone, il ponte) · Noah ⟳ (sente prima di vedere, frasi spezzate).\n";
  out += "Test di riconoscibilità: togliendo i nomi dai dialoghi, 7/10 attribuibili al fratello giusto.\n";
  return out;
}
process.stdout.write(testoBriefer(process.argv[2]));
