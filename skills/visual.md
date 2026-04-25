# skill: visual

**Scope:** costruisci e mantieni il **serbatoio di descrizioni visive e vincoli per prompt** di tutte le entità della storia (luoghi, personaggi, oggetti, venti-spiriti). Cura le immagini di riferimento per i modelli generativi. Costruisci il **piccolo sito web interno** ordinato per sezioni di entità, ad uso interno.

**Scrivi in:** `visual/` (tutto). **Non tocchi:** `cartografia/`, `pipeline_narrativa/`, file di radice (a meno che il task non lo richieda esplicitamente).

**Premessa:** prima di operare, leggi sempre `skills/README.md` per le **regole comuni** (autorità, isolamento `pipeline_narrativa/` read-only, comunicazione con Ray, pattern di rifiuto).

---

## 0. Stato attuale

**In bootstrap.** La directory `visual/` è stata creata vuota il 2026-04-25. Materiale, struttura interna, formato schede, vincoli prompt, criteri di selezione immagini di riferimento, e architettura del sito interno **saranno definiti da Ray in un brief separato**.

Quando Ray fornisce il brief:
1. Aggiorna questo file con: schema schede entità, lista categorie, formato prompt, struttura sito.
2. Definisci `visual/README.md` con istruzioni d'uso.
3. Crea le sotto-directory ragionevoli (ipotesi indicativa, non vincolante: `entita/luoghi/`, `entita/personaggi/`, `entita/oggetti/`, `entita/venti/`, `immagini/`, `sito/`).

---

## 1. Cosa leggere quando opererai (dopo il brief Ray)

### Sempre, prima di qualsiasi task visual

1. `skills/README.md` — regole comuni.
2. Questo file.
3. `visual/README.md` (quando esisterà) — schema schede e formato prompt.

### Per ricavare descrizioni visive coerenti

4. `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` — fonte primaria su mondo, personaggi, atmosfere.
5. `pipeline_narrativa/documenti_progetto/GLOSSARIO_ISOLA.md` — nomi canonici.
6. `pipeline_narrativa/documenti_progetto/CARTA_VOCE_v1_2.md` e `VOCE_AUTORE_ESTRATTA_v1_1.md` — registro stilistico (utile anche per il tono delle descrizioni visive).
7. `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md` — cliché visivi/narrativi da evitare anche in prompt.
8. `pipeline_narrativa/story_graph.json` — campo `visual_anchors.scene_hooks` per ogni storia: già contiene aggancio visivo.
9. `pipeline_narrativa/documenti_progetto/EAR_PERSONAGGI_Manuale_Completo.txt` — caratterizzazione personaggi.
10. `cartografia/geo/island.geojson` (read-only dal punto di vista visual) — note canoniche e materiali per coerenza con la cartografia.

### Per vincoli prompt e generazione immagini

11. (Quando Ray brifferà) — modello di riferimento (BFL FLUX, Grok), formato prompt, vincoli stilistici, palette, stile illustrativo target.

---

## 2. Principi non negoziabili (specifici visual)

### Principio 1 — Coerenza con il canone narrativo e cartografico

Le descrizioni visive **non possono contraddire** Bible, grafo storie, cartografia. Se rilevi conflitti:
- Bible vs. apparato → vince Bible.
- Bible vs. cartografia → vince Bible (la cartografia dettaglia senza contraddire).
- Cartografia vs. tua intuizione visiva → vince cartografia (materiali, colori, orientamenti, dimensioni).

Se la fonte canonica non dice nulla su un dettaglio visivo, **non inventarlo come se fosse canonico**: marcalo `provvisorio` (o equivalente nel formato scheda) e segnala come domanda aperta a Ray.

### Principio 2 — Niente cliché AI

Applica `PATTERN_AI_DA_BANDIRE_v1.md` anche in dominio visivo: niente "tramonto epico", "occhi che brillano di saggezza", "antico e magico" generico. Le descrizioni visive devono essere **specifiche e situate** sull'Isola, non template fantasy.

### Principio 3 — Vincoli prompt = contratto

I vincoli per prompt (negative prompts, stile fisso, palette obbligata, character consistency tokens) sono **contratto operativo**. Una volta concordati con Ray, vanno applicati uniformemente. Se proponi una modifica, segnalala come proposta — non la cambi in silenzio.

### Principio 4 — Immagini di riferimento

Le immagini generate o curate come riferimento per i modelli **non sono illustrazioni finali del libro**. Servono a fissare modello visivo per i personaggi, materiali, atmosfere. Vivono in `visual/immagini/` con metadati che ne dichiarano: entità rappresentata, prompt usato, modello, seed, stato (riferimento approvato / candidato / scartato).

---

## 3. Task tipici (template, da rifinire dopo brief Ray)

### Task A — Compilare scheda entità

1. Identifica entità (es. personaggio Gabriel, luogo Forno, oggetto braccialetto S9, vento Mulinello).
2. Estrai descrizione canonica da Bible / grafo / cartografia.
3. Scrivi scheda secondo schema definito in `visual/README.md`.
4. Aggiungi vincoli prompt (positivi + negativi + stile + palette).
5. Se mancano dati canonici, marca `[da definire]` e annota domanda aperta.
6. Commit con riferimento alle fonti citate.

### Task B — Generare immagine di riferimento

1. Scrivi prompt completo a partire dalla scheda.
2. Genera (modello e workflow definiti nel brief).
3. Cura: salva versione approvata + metadati (prompt, modello, seed, data).
4. Linka l'immagine alla scheda dell'entità.

### Task C — Aggiornare il sito interno

1. Il sito è ad uso interno (non per lettori finali). Sezionato per categorie di entità.
2. Mostra schede + immagini per consultazione rapida.
3. Tecnologia: da decidere col brief Ray (probabile static site, simile per spirito al viewer cartografia).

---

## 4. Pattern di rifiuto (specifici visual)

Oltre alle regole comuni in `skills/README.md` §5, **rifiuta** se la richiesta:
- Ti chiede di modificare la cartografia per giustificare una scelta visual → vai in skill cartografo o segnala a Ray.
- Ti chiede di scrivere prosa narrativa o riformulare seed/callback.
- Ti chiede di pubblicare immagini come illustrazioni finali del libro (la pipeline finale è altro flusso, fuori scope di questa skill).

---

## 5. Domande specifiche da fare a Ray (visual)

(Oltre a quelle comuni in `skills/README.md` §6:)

- "Il modello generativo target è BFL FLUX, Grok, altro? Workflow?"
- "Schema schede entità: campi obbligatori, opzionali, formato (Markdown? YAML frontmatter? altro)?"
- "Sito interno: solo HTML statico, o serve generatore (MkDocs, Astro, ecc.)?"
- "Per le immagini di riferimento: quale percentuale di coerenza dobbiamo raggiungere prima di considerare un personaggio 'fissato'?"
- "Le descrizioni visive sono in italiano, inglese, o doppia lingua (italiano per lettura interna, inglese per prompt)?"

---

**Ultimo aggiornamento:** 2026-04-25 — placeholder, in attesa brief Ray.
