# sotto-skill: compilatore (visual)

Specializzazione operativa della **skill visual**. Compila il *body* delle schede entità (`visual/<famiglia>/.../<id>/scheda.md`) partendo dalle fonti canoniche e completando le sezioni non documentate con inferenza canone-coerente, marcata.

**Premessa:** prima di operare leggi:
1. `skills/README.md` (regole comuni: isolamento `pipeline_narrativa/` read-only, comunicazione, gerarchia fonti).
2. `skills/visual/README.md` (skill visual: struttura, schema scheda, vincoli).
3. Questo file.

---

## 1. Scope di scrittura

Solo: `visual/<famiglia>/.../<id>/scheda.md`, modificando esclusivamente il **body** sotto il secondo `---`. Il frontmatter è derivato da fonti automatiche e gestito dallo script `scripts/build_visual_skeleton.py`: **non toccarlo**. Lo script preserva il body quando rigenera il frontmatter.

Permesso aggiuntivo: aggiungere `<entita>/<id>/note_lavoro.md` (o simili) se serve scratchpad di lavoro per quella entità — ma il deliverable resta `scheda.md`.

---

## 2. Principio fondamentale: "completa, non rimuovere"

Il template ha 14 sezioni. **Tutte vanno compilate.** Anche quando il canone non dichiara nulla su un aspetto, si propone un'inferenza coerente, marcata.

**Razionale:** le schede sono serbatoio attivo per narrativa, social, IA generative, stampa 3D. Una sezione vuota o rimossa è un'occasione persa: la narrativa futura potrà raccogliere da qui un dettaglio coerente già fissato (e validato da Ray).

In casi davvero non applicabili (es. "abbigliamento" per un vento, "espressione del volto" per un oggetto inanimato): **reinterpreta il campo** in coerenza con la natura dell'entità. Esempi: per un vento "abbigliamento" → manifestazione sensibile / vestitura percettiva (suoni, vibrazioni, riflessi); per un oggetto "espressione" → patina d'uso, segni del tempo.

---

## 3. Marcatori di provenienza

Convenzione di marcatura **in linea**, dopo l'affermazione che la richiede:

- **(default, nessun tag):** dato canonico, supportato da citazione precisa in "Riferimenti puntuali".
- **`[inf]`** o **`[inferito]`:** derivato logicamente dai dati canonici. Spiegare brevemente la deduzione subito dopo.
- **`[prop]`** o **`[proposta]`:** scelta visiva creativa coerente col canone, da validare con Ray. Dichiarare brevemente perché serve / da dove nasce.

Esempio di linea con marcatore:

> Stato delle ali: in saga sempre intatte. `[inf]` da apparizioni S6/S8/S9/S12 dove vola sempre normalmente con *frrr* regolare — niente segnali di danno.

---

## 4. Workflow per una scheda (un'entità per volta)

### Step 1 — Identifica entità

Prendi `id`, `famiglia`, `sottotipo` dal frontmatter della scheda da compilare.

### Step 2 — Estrazione mirata dal grafo

**Non leggere `story_graph.json` per intero** (è grande, satura il contesto e fa fallire i sub-agenti). Usa script Python ad-hoc:

```bash
python3 -c "
import json
g = json.load(open('pipeline_narrativa/story_graph.json'))
# Anagrafica
print('=== entity ===')
print(json.dumps(g['entities']['<famiglia>']['<id>'], ensure_ascii=False, indent=2))
# Apparizioni nelle storie
print('=== storie ===')
for sid, s in g['stories'].items():
    blob = json.dumps(s, ensure_ascii=False)
    if '<id>' in blob.lower() or '<nome>' in blob.lower():
        # filtra menzioni precise, non casuali
        ..."
```

### Step 3 — Lettura mirata dei doc canonici

In ordine:
1. `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` — `grep -n -B1 -A20 '<Nome>'` per trovare la sezione del personaggio/luogo (di solito §4 per personaggi, §2 per geografia).
2. `EAR_PERSONAGGI_Manuale_Completo.txt` — solo per personaggi, sezione del personaggio.
3. `EAR_PERSONAGGI_Lezioni_Apprese.txt` — note operative.
4. `PATTERN_AI_DA_BANDIRE_v1.md` — cliché generali; estrai quelli applicabili a questa entità.
5. `GLOSSARIO_ISOLA.md` — controllo nome canonico.
6. `cartografia/geo/island.geojson` (read-only) — per luoghi: note canoniche e materiali.

**Regola di lettura:** leggi solo quello che serve a questa entità. Niente esplorazioni dispersive.

### Step 4 — Compila le 14 sezioni del body

Ordine (vedi `visual/_template_scheda.md`):

1. **Identità visuale (sintesi)** — 1-2 frasi specifiche e situate. Niente cliché.
2. **Aspetto / forma** — fisico/geometrico/materico.
3. **Abbigliamento / stato d'uso** — capi, accessori, segni del tempo. Per non antropomorfi → reinterpretare (ali, marcature, patina).
4. **Espressione / comportamento** — tipico, ricorrente.
5. **Palette e atmosfera** — colori dominanti, qualità della luce.
6. **Contesto e ambientazioni ricorrenti** — dove e quando appare tipicamente.
7. **Coerenza cross-scena (cose che NON cambiano)** — vincoli inderogabili.
8. **Variabilità ammessa** — cosa può variare senza rompere coerenza.
9. **Cliché da evitare** — specifici per questa entità (constraints grafo + voci pertinenti da PATTERN_AI_DA_BANDIRE).
10. **Per stampa 3D** — volumi, proporzioni, scala, orientamento, pose canoniche per le 4 vedute.
11. **Per narrativa e social** — registri d'uso testuale, formule, tono.
12. **Storie / scene di apparizione** — una riga per ciascuna delle 12 storie. Cita il campo grafo che la supporta. "Assente" se non compare (esplicito).
13. **Disallineamenti / domande aperte** — conflitti rilevati (Bible vs grafo vs nome) **senza risolverli**: Ray valida.
14. **Riferimenti puntuali** — ogni dato canonico riportato deve avere qui citazione con path + ancora (`#entities.X`, `§Y.Z`).

### Step 5 — Stato compilazione

In cima al body, subito dopo `# <Nome>`, aggiungi:

```
> **Stato compilazione:** body provvisorio, in attesa revisione Ray. Compilato il YYYY-MM-DD con metodo "compilatore". Marcatori di provenienza: nessun tag = canone (citato in fondo); `[inf]` = inferito dai dati canonici; `[prop]` = proposta visiva da validare.
```

### Step 6 — Frontmatter intatto

Non toccare il frontmatter. Se serve aggiornarlo (es. nome canonico cambiato), il fix va nel grafo o nel GeoJSON, e poi si rilancia `python3 scripts/build_visual_skeleton.py` che propaga.

---

## 5. Vincoli operativi

- **Italiano**, prosa tecnica/descrittiva, niente lubrificazioni narrative.
- **Niente prompt-string pronti** per modelli specifici. Le sezioni descrittive sono fonte multi-uso (IA, 3D, narrativa, social).
- **Tendenzialmente la verità è nel grafo** — se grafo e Bible/altro contraddicono, scegli grafo e segnala in "Disallineamenti / domande aperte".
- **Niente rimozioni di sezioni** — completa con inferenza marcata.
- **Niente improvvisazione narrativa** — se manca un dato e l'inferenza è troppo creativa per essere ragionevole, marcala `[prop]` e lascia decidere a Ray.
- **Niente cliché AI** — applica `PATTERN_AI_DA_BANDIRE_v1.md`.
- **Una entità per volta** — non saturare il contesto con più entità in parallelo, soprattutto se il sub-agente è general-purpose (rischio timeout API).

---

## 6. Esempio canonico

`visual/personaggi/individuali/cuccioli/liu/scheda.md`

Esempio del metodo applicato a una entità minimale (libellulina con info minime nel grafo, `constraints: []` vuoto). Mostra:
- 14 sezioni complete (anche "Abbigliamento", reinterpretato come stato delle ali + accessori effimeri).
- Marcatori `[inf]` e `[prop]` in linea.
- Citazioni puntuali con path + ancora YAML/sezione.
- "Disallineamenti" registrati senza risolverli (es. nome canonico Liù vs id grafo `liu`).

---

## 7. Disclaimer su tempi e contesto

Il workflow di estrazione richiede lettura mirata e attenzione al budget di contesto. Se viene affidato a un sub-agente general-purpose (Claude Agent SDK, Anthropic API, Claude Code), considerare che:

- Letture intere di file grandi (`story_graph.json` ~580kb) possono saturare il contesto e causare timeout.
- Preferire script Python che estraggano solo i campi necessari (vedi step 2).
- Budget di tool calls suggerito: 10-15 per entità singola.
- Se il sub-agente fallisce, l'estrazione manuale (operatore umano o esecuzione diretta) e' sempre il fallback.

Per task massivi (>10 entità) preferire la chat con la zip del repo allegata, dove l'operatore lavora a contesto unificato senza vincoli stringenti di durata.

---

**Ultimo aggiornamento:** 2026-04-25 — prima versione formalizzata.
