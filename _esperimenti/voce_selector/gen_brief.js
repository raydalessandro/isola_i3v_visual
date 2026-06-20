/* Estrazione fedele della logica del selettore "La Voce" (assi + testoBriefer + nomeVoce).
   Genera il blocco §10 VOCE per un dato codice Σ. Uso: node gen_brief.js 113-  */

const RESPIRO = [
  {v:1, key:"taglio", t:"taglio", nome:"asciutta",
   firma:"Frase corta come unità base. Soggetto-verbo-complemento. Subordinata solo quando porta peso reale. Pause nette.",
   tabu:"Niente subordinate concatenate. Niente periodo lungo."},
  {v:2, key:"intreccio", t:"intreccio", nome:"intrecciata",
   firma:"Frasi che aprono ad altri («Possiamo…», «E se…»), citano, ricordano cose dette prima. La frase lega due cose.",
   tabu:"Niente intreccio che diventa arabesco: l'apertura resta semplice, da bambino che ha già ascoltato favole."},
  {v:3, key:"ritorno", t:"ritorno", nome:"che ritorna",
   firma:"La frase si ripiega: torna su sé con una piccola variazione («Girava intorno. Girava, e basta»). Eco, ripetizione musicale.",
   tabu:"Max 1-2 ripiegamenti per pagina, mai consecutivi: oltre, è cantilena."}
];
const LUCE = [
  {v:1, key:"giorno", t:"giorno", nome:"del giorno",
   firma:"Palette diurna: forno, pane, mercato, calore, lavoro. La cosa si vede alla luce piena.",
   tabu:"Niente notturno gratuito. Il calore non è mai morale (cibo-caldo-che-consola)."},
  {v:2, key:"notte", t:"notte", nome:"della notte",
   firma:"Palette notturna: candela, buio, riflesso, il fiume che gira nel buio. La cosa si vede al lume piccolo, o nel nero.",
   tabu:"La notte è ambiente, mai agente: non «ascolta», non «si china». Niente Quarto Vento, niente spiriti della notte."},
  {v:3, key:"soglia", t:"soglia", nome:"della soglia",
   firma:"Palette del tra: alba, tramonto, riva, margine, porta. «L'ora che non è più notte e non è giorno». La cosa è descritta sempre su un confine.",
   tabu:"La soglia è luogo, non agente: il Burrone non «chiama», l'acqua non «vuole». Il tra è una proprietà dello sguardo."}
];
const NARRATORE = [
  {v:1, key:"sottrazione", t:"sottrazione · Δ", nome:"che sottrae",
   firma:"Sigilla per sottrazione (Δ): dove la frase chiederebbe l'emozione o il significato, compare al suo posto un fatto fisico e laterale del mondo — un suono, un gesto, un movimento. Non tace: SOSTITUISCE. Il senso resta nel lettore, non sulla pagina. («Stettero zitti. Più giù, una capra rispose a un'altra capra.»)",
   tabu:"Il fatto-sostituto non è un simbolo trasparente (no «una foglia morta cadde» per dire tristezza): è laterale, quasi indifferente. Se il fatto spiega l'emozione, è morale travestita. Niente framework che affiora, niente sguardo adulto-tenero."},
  {v:2, key:"nominazione", t:"nominazione · ⇄", nome:"che nomina",
   firma:"Sigilla per nominazione (⇄): prende una cosa comune e le dà un nome come se la vedesse per la prima volta — e il nome resta, entra nel mondo, può tornare. Il nome contiene la qualità, o posiziona, o fissa un'azione ricorrente. («L'ora che non è più notte e non è giorno.»)",
   tabu:"Non è entusiasmo da adulto («che meraviglia!»), non è didattica: è un dito che nomina e si ritira. Quota: 1-2 nomi nuovi per storia, non di più, o il mondo si ingolfa. Ogni nome deve poter tornare in una storia successiva."},
  {v:3, key:"inversione", t:"inversione · ⟳", nome:"che gira",
   firma:"Sigilla per inversione (⟳): almeno una volta a storia luce e buio (o pieno/vuoto, fermo/movimento) si scambiano funzione, reso SEMPRE concreto. Il bianco pieno come il buio; il vento che toglie e nel togliere fa vedere.",
   tabu:"L'inversione non si dichiara MAI («capirono che il vero era nel riflesso» = vietato): si fa col fatto fisico. Niente lessico esoterico (energia, anima, cosmico). Quota stretta: 1 per storia, max 2 — è l'operazione più appariscente, va dosata o mangia le altre."}
];
const VERSO = [
  {v:"+", key:"disteso", t:"+ disteso", nome:"distesa",
   firma:"Verso espanso: la frase si concede una parola in più, il respiro è leggero, musicale. Più aria tra i blocchi.",
   tabu:"Disteso non vuol dire lungo: resta picture book. L'aria è respiro, non riempitivo."},
  {v:"−", key:"raccolto", t:"− raccolto", nome:"raccolta",
   firma:"Verso contratto: la frase si stringe, niente di superfluo, il peso è concentrato. Bianco tipografico più fitto.",
   tabu:"Raccolto non vuol dire spezzettato a effetto: la concentrazione è di senso, non di stile."}
];
const COLLAUDATE = {
  "111−": {nome:"La voce dell'Isola"},
  "333+": {nome:"La voce della Soglia"}
};
const g=(a,v)=>a.find(o=>o.v===v);
function nomeVoce(k){
  if(COLLAUDATE[k]) return COLLAUDATE[k].nome;
  const r=g(RESPIRO,+k[0]), l=g(LUCE,+k[1]);
  return "La voce "+r.nome+" "+l.nome;
}
function testoBriefer(k){
  const r=g(RESPIRO,+k[0]), l=g(LUCE,+k[1]), n=g(NARRATORE,+k[2]), v=g(VERSO,k[3]);
  let out = "## §10. VOCE — "+nomeVoce(k)+" (Σ"+k+")\n\n";
  out += "> Sostituisce la §10 di default del writing brief. Fatti, hook, cornici, frasi-codice (§§2-9) restano invariati: cambia solo la resa.\n\n";
  out += "**Principio.** Una voce "+r.nome+", "+l.nome+", "+n.nome+", "+v.nome+". Stessi fatti del mondo, detti in questo modo.\n\n";
  out += "**Firma (sempre presente):**\n";
  out += "- Respiro — "+r.firma+"\n";
  out += "- Luce — "+l.firma+"\n";
  out += "- Narratore — "+n.firma+"\n";
  out += "- Verso — "+v.firma+"\n\n";
  out += "**Tabù:**\n";
  out += "- "+r.tabu+"\n- "+l.tabu+"\n- "+n.tabu+"\n- "+v.tabu+"\n";
  out += "- Universali saga: niente morale esplicita, niente framework EAR che affiora, niente marcatori AI, notte come ambiente non agente.\n\n";
  if(n.key==="inversione"){
    out += "**Quota inversione luce/buio (⟳):** 1 per storia, max 2. Resa SEMPRE con fatto fisico, mai dichiarata. È l'operazione più appariscente: oltre le 2 occorrenze diventa maniera e schiaccia gli altri assi. (Su una storia diurna, il punto naturale è la nebbia / il riflesso / il controluce.)\n\n";
  } else if(n.key==="sottrazione"){
    out += "**Operazione di sottrazione (Δ):** dove la frase chiederebbe l'emozione, mettere al suo posto un fatto fisico laterale del mondo (suono, gesto, movimento), quasi indifferente. Mai un simbolo trasparente. Il senso resta nel lettore.\n\n";
  } else if(n.key==="nominazione"){
    out += "**Operazione di nominazione (⇄):** 1-2 nomi nuovi per storia. Il narratore lega un nome a una cosa comune come se la vedesse ora; il nome contiene la qualità o posiziona o fissa un'azione, suona antico, e può tornare in una storia successiva. Registrare i nomi nuovi nel glossario.\n\n";
  }
  out += "**Voci dei tre fratelli (invariate):** Gabriel Δ (decide netto, nei silenzi prima di parlare) · Elias ⇄ (apre, propone, il ponte) · Noah ⟳ (sente prima di vedere, frasi spezzate).\n";
  out += "**Test:** togliendo i nomi dai dialoghi, 7/10 riconoscibili.\n";
  return out;
}
const k = process.argv[2];
process.stdout.write(testoBriefer(k));
