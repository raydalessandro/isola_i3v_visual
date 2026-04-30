# Integrazione cornice del mondo — istruzioni per l'agente

> **Per chi legge:** sei l'agente che integra nel grafo e nelle schede del catalogo le decisioni autoriali contenute nei 6 documenti di questo pacchetto. Questo README spiega *cosa fare*, *in che ordine*, e *come risparmiare token leggendo solo lo stretto necessario*.
>
> **Lavoro tuo:** scrivere script idempotenti che applicano le modifiche, lanciare audit, attendere approvazione di Ray tra una fase e la successiva.
>
> **NON sei il tuo lavoro:** non riscrivere narrazioni, non modificare hook visivi, non toccare il core delle storie (premise/problem/threshold/resolution).

---

## 1. Stato del progetto in cui entri

Ray ha completato:
- 12 narrazioni fattuali (`pipeline_narrativa/narrazione_fattuale/s01-s12_*.md`)
- Hook visivi estesi a 10 per storia, schema 1.3, nel grafo
- Catalogo schede personaggi/luoghi/oggetti (provvisorio, popolato meccanicamente)
- Quote tracker attivo nel grafo

**Quello che manca**, e che questo pacchetto consegna come decisioni autoriali:
1. Una formula-ritornello "che animale è" per identificare i membri anonimi dei gruppi-istituzione
2. Saluti distinti per i 5 gruppi-istituzione
3. 24 cornici di sfondo distribuite nelle 12 storie, organizzate in 5 processi del mondo
4. Aggiunta di sentieri "fantasma" alle `locations_secondary` delle storie
5. Dettagli stabili dei sentieri Tier A (ed in seguito B, C)

**Tutto questo deve finire nel grafo o nel catalogo.** Niente prosa nuova — solo strutture dati e sezioni di schede.

---

## 2. Lettura raccomandata (ordine + cosa leggere davvero)

I documenti sono lunghi. **Non li leggere tutti per intero.** Per ciascun task, ti basta una porzione precisa.

| Doc | Scope | Cosa leggere DAVVERO | Cosa saltare |
|---|---|---|---|
| `DOC_1_formula_ritornello.md` | Formula-ritornello identificazione animali | §1 (formula) + §2 (variante plurale) + §3 (vincoli) + §4.1 (pool esclusi) | §4 lista pool intera (la usi solo se serve scegliere animali nuovi) e §5 esempi |
| `DOC_2_saluti_gruppi.md` | Saluti dei 5 gruppi | §3 tabella riepilogativa + §4 regole | tutto §2 dettaglio (basta tabella) |
| `DOC_3_cornici_processi.md` | 24 cornici + 5 processi | §1 (i 5 processi) + §3 (schema dati) + §4 (riepilogo distribuzione) | §2 dettaglio cornice per cornice (è dato, non spiegazione — usa solo quando scrivi nel grafo) |
| `DOC_4_audit_sentieri.md` | Audit del percorrere | §1 (sintesi numerica) + §3 (tier) + §4 (gap) | §2 mappa per storia (usa solo quando esegui il task di aggiunta `locations_secondary`) |
| `DOC_5_index_sentieri.md` | Index sentieri navigabile | §1 (indice inverso) + §2 (indice diretto) + §4 (schema slot) | §6 (decisioni aperte, già risolte) |
| `DOC_6_mercato_idee_tierA.md` | 20 dettagli stabili Tier A | §2-§6 (le 5 sezioni dettagli, già approvate da Ray) + §7 riepilogo | §8 spunti check (già usati) |

**Token-saving rules:**
- Se devi scrivere lo script per un task, leggi PRIMA il riepilogo del doc, POI scendi nel dettaglio solo della sezione operativa.
- Non rileggere la Bible, la Carta Voce, il `PATTERN_AI_DA_BANDIRE`. Non ne hai bisogno per questo pacchetto — è puro lavoro di scrittura strutturale nel grafo.
- Se uno script richiede uno schema, lo schema è in `DOC_3 §3` (cornici) e `DOC_5 §4` (sentieri). Punto.

---

## 3. Mappa operativa: cosa va dove

Tre destinazioni distinte. Tienile separate.

### 3.1 → Grafo (`pipeline_narrativa/story_graph.json`)

| Da quale doc | Cosa | Dove nel grafo |
|---|---|---|
| DOC_1 | Formula ritornello | nuovo nodo root: `world_conventions.refrain_animal_identification` |
| DOC_1 | Tracker animali usati | dentro `quote_tracker`: `refrain_animal_used_per_story` (lista di tuple `[story, group, animal]`) |
| DOC_3 | 24 cornici | nuovo campo per ogni storia: `stories.<sid>.cornice_dettagli` (lista di oggetti, schema in DOC_3 §3) |
| DOC_4 | Sentieri "fantasma" | append a `stories.<sid>.locations_secondary` (vedi DOC_4 §4 per la mappa storia → sentieri da aggiungere) |
| DOC_5 + DOC_6 | Indici sentieri + dettagli | nuovo nodo root: `world_conventions.path_details` (oggetto con `paths: { sentiero_id: { details: [...] } }` — schema in DOC_5 §4) |

### 3.2 → Catalogo schede (`visual/personaggi/collettivi/<gruppo>/scheda.md`)

| Da quale doc | Cosa | Dove |
|---|---|---|
| DOC_2 | Saluto del gruppo | nuova sezione `## Saluto del gruppo` in ogni scheda dei 5 gruppi (camminanti, mantenitori, coltivatori_del_cerchio, mercato_del_mezzogiorno, pastori) |

Niente altro va nelle schede catalogo personaggi.

### 3.3 → Catalogo schede sentieri (`visual/luoghi/.../strade/<sentiero>/scheda.md`)

| Da quale doc | Cosa | Dove |
|---|---|---|
| DOC_6 | Dettagli stabili | sezione `## Coerenza cross-scena (cose che NON cambiano)` di ogni scheda Tier A elencata in DOC_6. Sostituire `_da popolare dal grafo_` con i dettagli in formato compatto (vedi DOC_5 §4 per schema YAML) |

I sentieri Tier B e Tier C arriveranno in pacchetti successivi (DOC_6_tierB, DOC_6_tierC). Per ora, **solo Tier A**.

---

## 4. Ordine di esecuzione raccomandato

Esegui in ordine. Tra uno step e il successivo, **lancia gli audit** (`audit_*.py`) e **fermati** se qualcosa rompe. Aspetta input di Ray.

### Step 1 — `world_conventions` (root del grafo)
- Crea il nodo root `world_conventions`
- Aggiungi `refrain_animal_identification` (DOC_1 §1, §2, §3 in JSON minimale)
- Aggiungi `path_details` (placeholder vuoto, popolato a Step 5)
- Modifica `graph_version` a 1.2.0 (additivo, retrocompatibile)
- Audit: `python audit_2_schema.py`

### Step 2 — `quote_tracker` esteso
- Aggiungi `refrain_animal_used_per_story` (lista vuota, popolata da Step 4)
- Audit: `python audit_2_schema.py`

### Step 3 — Saluti nelle schede catalogo gruppi (DOC_2)
- Per ognuno dei 5 gruppi: aggiungi sezione `## Saluto del gruppo` (testo da DOC_2 §3 + §2)
- Niente audit grafo qui (è catalogo)
- Aggiorna `ultima_modifica:` nel frontmatter

### Step 4 — Cornici (DOC_3)
- Per ognuna delle 12 storie, aggiungi `cornice_dettagli` con le sue cornici (DOC_3 §2)
- Per ogni cornice che applica formula: append in `quote_tracker.refrain_animal_used_per_story`
- Audit: `python audit_2_schema.py` + `python audit_4_drift.py`

### Step 5 — Sentieri "fantasma" (DOC_4 §4)
- Per ognuna delle 12 storie, aggiungi le entry mancanti in `locations_secondary`
- Mappa testuale completa in DOC_4 §4
- Audit: `python audit_3_navigability.py`

### Step 6 — Index sentieri (DOC_5 + DOC_6)
- Popola `world_conventions.path_details.paths` con i 5 sentieri Tier A di DOC_6
- Per ogni sentiero, lista di oggetti `{id, where_along_path, what, appears_in_stories, state_by_story?}`
- Schema in DOC_5 §4 (campo `tipo` rimosso — un dettaglio è un dettaglio, libero)

### Step 7 — Schede sentieri Tier A (DOC_6)
- Per ognuno dei 5 sentieri Tier A, sostituisci la sezione `## Coerenza cross-scena` con i dettagli da DOC_6
- Ogni dettaglio rimanda al grafo via `path_details.paths.<id>.details[]`
- Schede da modificare:
  - `visual/luoghi/quartiere_fuoco/via_dell_alba/scheda.md`
  - `visual/luoghi/quartiere_terra/sentiero_orti_torrente_foresta/scheda.md`
  - `visual/luoghi/quartiere_aria/via_che_sale/scheda.md`
  - `visual/luoghi/quartiere_terra/sentiero_orti_casa_salvia/scheda.md`
  - `visual/luoghi/quartiere_centro/viottolo_perimetrale_piazza/scheda.md` *(verifica path esatto)*

---

## 5. Stile script

Tutti gli script che scrivi in questa fase devono:

1. **Idempotenti** — eseguibili più volte, senza duplicare entry.
2. **Dry-run di default** — `--dry-run` mostra cosa cambierebbe; `--apply` applica davvero.
3. **Backup automatico** — prima di modificare il grafo, salva `story_graph.json.bak.<timestamp>`.
4. **Validazione schema** — leggi lo schema target dai DOC, valida prima di scrivere.
5. **Log umano** — output leggibile: *"Aggiunte 5 cornici a s06. Quote tracker aggiornato."*

Modello di riferimento: `scripts/write_hooks_to_graph.py` esistente nella repo.

---

## 6. Cosa NON fare

- NON scrivere prosa.
- NON modificare hook visivi del grafo.
- NON modificare la voce dei personaggi (lo farà l'agente prosa successivo).
- NON inventare dettagli nuovi: usa SOLO ciò che è in DOC_6.
- NON saltare audit tra Step e Step.
- NON committare se Ray non ha approvato.

---

## 7. Cosa serve a Ray dopo che hai finito

Quando completi tutti gli step:

1. Riassunto in markdown:
   - Quante entry aggiunte al grafo (per tipo)
   - Quante schede catalogo modificate
   - Quale audit ha fallito (se ne ha)
2. Diff sintetico delle versioni del grafo
3. Pronto-da-rifetchare per Ray

Lui rifetcha la repo, controlla, e mi dà il via per costruire il **brieffer per storia** — lo script `build_writing_brief.py` che, dato un sid, produce il dossier completo per l'agente prosa pescando da: grafo, narrazione fattuale, hook, cornici, sentieri, saluti, formula ritornello, catalogo schede.

A quel punto resta un solo passo: **scrivere**.

---

## 8. Files in questo pacchetto

```
docs/
├── DOC_1_formula_ritornello.md       # formula "che animale è"
├── DOC_2_saluti_gruppi.md             # saluti dei 5 gruppi
├── DOC_3_cornici_processi.md          # 24 cornici + 5 processi del mondo
├── DOC_4_audit_sentieri.md            # audit del percorrere reale
├── DOC_5_index_sentieri.md            # index sentieri navigabile
└── DOC_6_mercato_idee_tierA.md        # 20 dettagli stabili Tier A approvati
README.md                              # questo file
```

---

## 9. Decisioni autoriali già prese (referenze rapide)

Ray ha già deciso queste cose. Non chiedere conferma, applica.

- **Formula ritornello:** "Era un/una <gruppo> — quale, oggi? Una/Un <animale>." (singolare) / "Erano i/le <gruppo> — chi, oggi? <animale>, <animale>, <animale>." (plurale)
- **Animali specie dichiarata** (non suggerita)
- **Saluti dei 5 gruppi** come da DOC_2 §3 tabella
- **Schema slot dettaglio sentiero**: campo `tipo` rimosso, slot libero
- **Tier A approvato** come da DOC_6
- **Tier B + Tier C**: in arrivo nei prossimi pacchetti, NON eseguire ora

---

Fine README.
