# 📘 PIPELINE OPERATIVA — Completamento catalogo visual `L'Isola dei Tre Venti`

**Versione:** 1.2
**Data:** 2026-04-29
**Stato:** ✅ **PIPELINE PERSONAGGI VALIDATA** su 2 specie diversissime (Fiamma + Bartolo). ✅ **PIPELINE LUOGHI VALIDATA** su luogo complesso con esterno + interno + cortile (Forno di Fiamma). 🚀 Pronti per scaling a tutto il catalogo.
**Autore:** Ray + Claude Opus 4.7
**Scope:** completamento delle 115 schede `visual/` della saga, con generazione canonica delle immagini di riferimento per AI, illustrazioni e stampa 3D.

---

## 🎯 Obiettivo finale

Completare il catalogo `visual/` della saga **L'Isola dei Tre Venti** in modo che:

1. **Ogni entità (115 totali)** abbia una scheda canonica chiusa, con aspetto fissato una volta per tutte.
2. **Ogni personaggio e oggetto principale** abbia immagini canoniche di riferimento generate con Grok Imagine.
3. **Ogni luogo** abbia un blocco LOCATION testuale dettagliato per uso in prompt scena (no immagini reference per scene multi-personaggio).
4. **Le palette, le proporzioni e lo stile** siano coerenti tra tutte le entità (canone saga unificato).
5. **Il tutto sia pronto** per essere usato in pipeline di generazione delle illustrazioni delle 12 storie.

---

## 🏗️ Architettura del sistema

### Tre livelli di documenti canonici (in `_canone/`)

**Da consultare SEMPRE prima di generare qualsiasi immagine:**

1. **`01_SAGA_STYLESHEET_v1.md`** — lo stile visivo della saga (validato 2026-04-29 con Fiamma). Si incolla in OGNI prompt Grok.
2. **`02_SAGA_SCALE_v1.md`** — le proporzioni canoniche tra personaggi (Gabriel = 1.0 GU). Si incolla nei prompt multi-personaggio.
3. **`03_SAGA_PALETTE_v1.md`** — le palette canoniche per quartiere e personaggio. Si consulta scrivendo le schede e i prompt.

**Regola d'oro:** mai cambiare questi documenti senza consenso esplicito di Ray. Se serve aggiornarli, bumpare versione e tracciare nel changelog interno.

### Tre tipologie di entità → tre template (in `_templates/`)

| Tipologia | Template scheda | Template prompt | Note |
|---|---|---|---|
| **Personaggio** | `TEMPLATE_scheda_personaggio.md` | `TEMPLATE_prompt_grok_personaggio.md` | 4 immagini canoniche (fronte / azione / modalità / turnaround) |
| **Oggetto** | `TEMPLATE_scheda_oggetto.md` | (ad hoc, derivato da quello personaggio ma più semplice) | 1-2 immagini canoniche |
| **Luogo** | `TEMPLATE_scheda_luogo.md` | **NESSUN template prompt** — i luoghi vivono come BLOCCO LOCATION testuale dentro la scheda stessa | 0-1 immagine establishing per atlante (opzionale) |

⚠️ **Pattern "luogo complesso":** alcuni luoghi (case con esterno+interno, edifici con cortile, piazze con annessi) richiedono **PIÙ blocchi LOCATION distinti** dentro la stessa scheda. Esempio: il Forno di Fiamma ha 3 blocchi (ESTERNO / INTERNO / CORTILE). Quando si compone un prompt scena, si usa **un solo blocco** per scena, scelto in base a dove si svolge l'azione. Mai mischiare blocchi (produrrebbe immagini ibride confuse). Il template `TEMPLATE_scheda_luogo.md` v1.1 supporta questo pattern con i flag frontmatter `ha_interno`, `ha_esterno`, `ha_cortile_o_annessi`.

---

## 📋 IL FLUSSO OPERATIVO (per ogni scheda)

### Fase 0 — Setup (una volta sola, a inizio sessione)

Claude legge:
1. `_canone/01_SAGA_STYLESHEET_v1.md`
2. `_canone/02_SAGA_SCALE_v1.md`
3. `_canone/03_SAGA_PALETTE_v1.md`
4. Il template della tipologia di entità su cui sta lavorando (in `_templates/`)
5. La scheda esistente nel repo (in `visual/<famiglia>/.../<id>/scheda.md`)
6. Le fonti canoniche pertinenti:
   - Bible §<X.Y> per il personaggio/luogo/oggetto
   - Glossario §<X.Y>
   - Grafo `pipeline_narrativa/story_graph.json` campi specifici dell'entità
   - `PATTERN_AI_DA_BANDIRE_v1.md`
   - `RIFERIMENTI_OPERATIVI-1.md` per consultazione veloce

### Fase 1 — Compilazione scheda

Claude:
1. Apre il template appropriato (`TEMPLATE_scheda_<famiglia>.md`)
2. Riempie il frontmatter con i dati dal grafo (è già fatto, verificare)
3. Riempie il body sezione per sezione:
   - **Sezioni "fonte Bible"**: travaso 1:1 dalla Bible
   - **Sezioni "derivazione autoriale"**: deriva da fonti coerenti, dichiara la derivazione in "Riferimenti puntuali"
   - **Sezioni "dal grafo"**: lista deterministica (Storie / scene di apparizione)
   - **Sezione "Cliché da evitare"**: travaso da Bible "Note e vincoli" + derivazione da `PATTERN_AI_DA_BANDIRE_v1.md`
4. **Mai inventare contenuto non derivabile.** Se non c'è derivazione possibile, lasciare `_da popolare dal grafo_` con annotazione in "Disallineamenti / domande aperte".
5. Output: file `scheda.md` completo, pronto da pushare al posto della vecchia.

### Fase 2 — Generazione prompt Grok

#### Per personaggi e oggetti:

Claude apre `TEMPLATE_prompt_grok_personaggio.md` (o adatta per oggetto):
1. Incolla il blocco STYLESHEET CANONICA SAGA da `_canone/01`
2. Compila il blocco CHARACTER (o OBJECT) usando la scheda appena scritta
3. Per ogni immagine canonica (4 per personaggio, 1-2 per oggetto):
   - Scrive la SCENE specifica di quella immagine
   - Specifica aspect ratio
   - Specifica filename suggerito
4. Aggiunge negative prompt globale + specifici per quel personaggio/oggetto
5. Aggiunge checklist post-generazione
6. Output: file `prompt_grok.md` pronto da usare

#### Per luoghi:

⚠️ **Strategia diversa.** Per i luoghi NON si genera un prompt Grok come per i personaggi. Si scrive direttamente il blocco LOCATION testuale **DENTRO la scheda** (sezione "Descrizione visiva canonica per generazione").

**Perché:** se diamo a Grok un'immagine reference di luogo + reference di personaggi, le proporzioni si rompono. Il blocco LOCATION testuale, combinato con i reference visivi dei personaggi, mantiene proporzioni stabili.

**Eccezione:** per luoghi importanti (Forno, Pontile, Piazza Villaggio, ecc.) si può generare 1 immagine **establishing** per atlante/preview, ma quella **non si usa come reference** in pipeline scena. Il blocco LOCATION testuale resta il riferimento operativo.

### Fase 3 — Generazione descrizione narrativa/social

Claude apre `TEMPLATE_descrizione_narrativa_social.md`:
1. Compila i 6 livelli di testo (A-G):
   - A: tag breve (1 frase)
   - B: scheda riga (1-2 frasi)
   - C: paragrafo descrittivo (3-5 frasi)
   - D: paragrafo evocativo (5-8 frasi)
   - E: registri d'uso interni
   - F: cosa NON dire mai
   - G: frasi tipiche (solo per personaggi)
2. Output: file `descrizione_narrativa_social.md`

### Fase 4 — Generazione immagini (fa Ray)

Ray:
1. Apre `prompt_grok.md`
2. Genera le immagini canoniche con Grok Imagine
3. Verifica con la checklist post-generazione
4. Salva in `visual/<famiglia>/.../<id>/immagini/<id>_<vista>_v1.png`
5. Se l'immagine non passa la checklist → torna a Claude con feedback per aggiustare il prompt

### Fase 5 — Push su GitHub (fa Ray)

Ray:
1. Crea branch dedicato: `claude/visual-completion-fase-F2-<id>`
2. Sostituisce/aggiunge:
   - `visual/<famiglia>/.../<id>/scheda.md` (sostituisce vecchia)
   - `visual/<famiglia>/.../<id>/prompt_grok.md` (nuovo)
   - `visual/<famiglia>/.../<id>/descrizione_narrativa_social.md` (nuovo)
   - `visual/<famiglia>/.../<id>/immagini/<id>_<vista>_v1.png` (nuovo, solo personaggi/oggetti)
3. Commit con messaggio chiaro
4. Push, merge fast-forward su main
5. Rigenera `catalogo_web/data/entities.json` con `python3 scripts/build_catalogo_web.py`

### Fase 6 — Aggiornamento canone (se necessario)

Se durante la generazione emergono **dettagli che diventano canone saga** (es: "le mani delle volpi sono scure"), Ray aggiorna i file in `_canone/` e lo dichiara nel changelog interno del file canone.

---

## 🛠️ ORDINE DI ESECUZIONE CONSIGLIATO

### Sequenza prioritaria

L'ordine in cui completare le 115 schede è importante perché alcune entità sono "anchor" per altre (es. Gabriel è anchor di scala per tutti i personaggi).

#### Blocco 1 — Test e validazione
1. ⏸️ `grembiule_fiamma` (oggetto) — pilota oggetto, scheda completa, prompt da rigenerare con stylesheet validata
2. ✅ `fiamma` (personaggio primario) — **VALIDATA 2026-04-29** (4 immagini canoniche)
3. ✅ `bartolo` (personaggio primario) — **VALIDATA 2026-04-29** (4 immagini canoniche su specie diversa, conferma robustezza pipeline)
4. ✅ `forno` (luogo) — **VALIDATA 2026-04-29** (3 blocchi LOCATION testuali: esterno + interno + cortile, validato il pattern luogo-complesso)

#### Blocco 2 — Tre fratelli (anchor di scala)
5. `gabriel` — anchor di scala canonica
6. `elias`
7. `noah`

#### Blocco 3 — Personaggi primari rimanenti
8. `rovo` (tasso, foresta)
9. `stria` (airone, scuola)
10. `memolo` (riccio, villaggio)
11. `grunto` (stambecco, montagne — quadrupede, attenzione)

#### Blocco 4 — Personaggi secondari (mestieri)
12. `salvia` (lepre)
13. `nodo` (picchio)
14. `amo` (cormorano)
15. `zolla` (scoiattolo)

#### Blocco 5 — Cuccioli
16-20. `pun`, `toba`, `bru`, `cardo`, `liu`

#### Blocco 6 — Collettivi (5)
21-25. `coltivatori_del_cerchio`, `mercato_del_mezzogiorno`, `mantenitori`, `camminanti`, `pastori`

#### Blocco 7 — Oggetti (14)
26-39. tutti gli oggetti firma visiva + oggetti di scena ricorrenti

#### Blocco 8 — Luoghi principali (per quartiere)
40-95. tutti i luoghi, raggruppati per quartiere per coerenza:
- Centro / Villaggio (Albero Vecchio, Piazza, ecc.)
- Quartiere di Fuoco (Forno, Case del Mattino, Via dell'Alba)
- Quartiere d'Acqua (Pontile, Bocca, Spiaggia, ecc.)
- Quartiere di Terra (Foresta, Orti, Tana di Rovo, ecc.)
- Quartiere d'Aria (Pascoli, Roccia Alta, Burrone, ecc.)
- Perimetro (Fascia Costiera, Fiume, Sentieri)

#### Blocco 9 — Strade
96-115. tutte le strade per quartiere

#### Blocco 10 — Venti + visual_signatures
116-119. `vento_taglio`, `vento_intreccio`, `vento_mulinello`, `quando_acqua_trema`

⚠️ **I venti hanno regole speciali**: mai personificati visivamente, presenza ambientale. Si trattano come "atmosfere" non come "personaggi". Approfondire quando si arriva.

---

## ⚠️ REGOLE NON NEGOZIABILI

### NEVER (mai, sotto nessuna circostanza)

1. ❌ **Mai modificare `pipeline_narrativa/`** (Bible, grafo, documenti progetto). Sono READ-ONLY.
2. ❌ **Mai inventare contenuto narrativo** non derivabile dalle fonti.
3. ❌ **Mai cambiare lo stile della saga** senza autorizzazione di Ray.
4. ❌ **Mai usare `_da popolare dal grafo_` come scusa** per non riempire una sezione che è derivabile.
5. ❌ **Mai pushare su main senza il via di Ray**. Sempre branch dedicato + merge fast-forward.
6. ❌ **Mai modificare il canone (`_canone/*.md`)** senza tracciare il cambiamento e bumpare versione.

### ALWAYS (sempre)

1. ✅ **Sempre leggere le fonti canoniche** prima di scrivere.
2. ✅ **Sempre dichiarare le derivazioni** nei "Riferimenti puntuali".
3. ✅ **Sempre rispettare la stylesheet saga** nei prompt Grok.
4. ✅ **Sempre verificare la checklist post-generazione** sulle immagini.
5. ✅ **Sempre rigenerare `catalogo_web/data/entities.json`** dopo modifiche al `visual/`.
6. ✅ **Sempre commit con messaggio descrittivo** (cosa + perché).

---

## 📁 STRUTTURA DELIVERABLE PER SCHEDA

Per ogni scheda completata, l'output finale nella repo (`visual/<famiglia>/.../<id>/`) contiene:

### Personaggi
```
<id>/
├── scheda.md                              ← scheda canonica (nuova)
├── prompt_grok.md                         ← prompt per generazione 4 immagini
├── descrizione_narrativa_social.md        ← testi standalone A-G
└── immagini/
    ├── <id>_canonica_v1_fronte.jpg        ← img 1
    ├── <id>_canonica_v1_azione.jpg        ← img 2
    ├── <id>_canonica_v1_<modalità>.jpg    ← img 3 (opzionale)
    └── <id>_turnaround_v1.jpg             ← img 4
```

### Oggetti
```
<id>/
├── scheda.md
├── prompt_grok.md
├── descrizione_narrativa_social.md
└── immagini/
    ├── <id>_canonica_v1.jpg               ← img canonica principale
    └── <id>_in_uso_v1.jpg                 ← (opzionale, indossato/in azione)
```

### Luoghi
```
<id>/
├── scheda.md                              ← contiene il BLOCCO LOCATION testuale
├── descrizione_narrativa_social.md        ← testi standalone
└── immagini/
    └── <id>_establishing_v1.jpg           ← (opzionale, solo per atlante/preview)
```

⚠️ **I luoghi NON hanno `prompt_grok.md`** — il blocco LOCATION è dentro la scheda.

---

## 🚀 VISIONE FUTURA — Pipeline scene multi-personaggio

Quando tutte le schede saranno complete, la pipeline per generare una scena di una storia sarà:

```
INPUT:
- Stylesheet saga (fissa)
- Scale reference (fissa, filtrata sui personaggi presenti)
- Reference images dei personaggi presenti (1 per personaggio, da `<id>/immagini/`)
- Blocco LOCATION testuale (da `<id>/scheda.md` del luogo)
- Specifica scena (cosa succede, modalità di ciascun personaggio, ora del giorno, vento attivo, ecc.)

OUTPUT:
- Illustrazione finale della scena per la storia s0X.
```

Questo è il punto d'arrivo. Per arrivarci servono tutte le schede chiuse.

---

## 📚 RIFERIMENTI

### Documenti canonici saga (read-only)
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md`
- `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`
- `pipeline_narrativa/documenti_progetto/CARTA_VOCE_v1_2.md`
- `worldbuilding/GLOSSARIO_ISOLA.md`
- `worldbuilding/RIFERIMENTI_OPERATIVI-1.md`
- `pipeline_narrativa/story_graph.json`

### Documenti operativi pipeline (questa cartella)
- `_canone/01_SAGA_STYLESHEET_v1.md`
- `_canone/02_SAGA_SCALE_v1.md`
- `_canone/03_SAGA_PALETTE_v1.md`
- `_templates/TEMPLATE_scheda_personaggio.md`
- `_templates/TEMPLATE_scheda_luogo.md`
- `_templates/TEMPLATE_scheda_oggetto.md`
- `_templates/TEMPLATE_prompt_grok_personaggio.md`
- `_templates/TEMPLATE_descrizione_narrativa_social.md`
- `_skill/PIPELINE.md` (questo file)
- `_skill/CHECKLIST.md`

### Esempi validati (in `_esempi/`)
- `_esempi/grembiule_fiamma/` — pilota oggetto
- `_esempi/fiamma/` — pilota personaggio + validazione stylesheet

---

**Ultimo aggiornamento:** 2026-04-29
**Prossima revisione:** quando si attacca a Bottino completare i fratelli (Gabriel/Elias/Noah) per fissare gli anchor di scala definitivamente
**Personaggi validati come standard:** Fiamma, Bartolo (vedi `_esempi/`)
**Luoghi validati come standard:** Forno di Fiamma (vedi `_esempi/forno/`)
