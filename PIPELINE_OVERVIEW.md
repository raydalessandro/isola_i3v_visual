---
scope: snapshot-pipeline
status: temporaneo (eliminabile dopo lettura)
ultima_modifica: 2026-05-06
---

# PIPELINE OVERVIEW — L'Isola dei Tre Venti

> Snapshot operativo del processo end-to-end "idea → libro illustrato" come lo abbiamo costruito su questa repo. Non sostituisce `CLAUDE.md` / `docs/PIPELINE.md` / `PROJECT_STATE.md` — è una **lettura compatta** per guardare il sistema da fuori e prepararci all'automazione finale.
>
> File temporaneo. Quando lo hai letto puoi cancellarlo: tutta l'informazione resta nei doc canonici della repo.

---

## 1. La forma del sistema in una immagine mentale

Pensa a tre **strati di dati** che si alimentano in cascata, e a un **prodotto finale** (il libro) che ne è la composizione:

```
┌──────────────────────────────────────────────────────────────┐
│ STRATO 1 — CANONE NARRATIVO  (read-only, fonte di verità)    │
│                                                              │
│  pipeline_narrativa/                                         │
│   ├── story_graph.json        schema 1.4, graph 1.2.0        │
│   │     ├─ stories.s01..s12   12 storie + 10 hook ciascuna   │
│   │     ├─ entities           ~120 entità promosse           │
│   │     ├─ world_conventions  cornice del mondo + sentieri   │
│   │     └─ quote_tracker      contatori unicità saga         │
│   ├── narrazione_fattuale/    12 narrazioni fattuali (Ray)   │
│   ├── documenti_progetto/     Bible, Carta Voce, ARCHI,      │
│   │                           Pattern AI da bandire, Glossa- │
│   │                           rio, EAR                       │
│   └── prompts/                prompt operativi agenti        │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ STRATO 2 — CANONE VISIVO  (alimentato dal grafo + autoriale) │
│                                                              │
│  visual/   116 schede (personaggi, luoghi, oggetti, venti)   │
│   ├── scheda.md               14 sezioni, marker provenienza │
│   ├── prompt_grok.md          prompt Grok Imagine canonico   │
│   └── immagini/               <id>_canonica_v1_*.jpg ref     │
│                                                              │
│  cartografia/geo/island.geojson    104 feature, sistema      │
│                                    cartesiano locale         │
│                                                              │
│  catalogo_web/  output rigenerabile (browser)                │
│  _visual_pipeline/  pacchetto canonizzazione (canone+templ.) │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ STRATO 3 — LIBRO  (prosa + immagini-scena composte)          │
│                                                              │
│  pipeline_narrativa/writing_briefs/sNN_writing_brief.md      │
│      brief autosufficienti (16k-32k parole) per agente prosa │
│                                                              │
│  pipeline_narrativa/storie_finali/                           │
│   ├── sNN_<slug>.md          prosa definitiva con marker     │
│   │                          @hook (1..10 narrativi)         │
│   │                          @subhook (1..N pagine libro)    │
│   ├── _scene/sNN/*.jpg       immagini-scena composte         │
│   │                          (una per pagina libro fisica)   │
│   ├── _annotations/sNN.yaml  note autoriali Ray              │
│   └── _volumi/               cornice editoriale 4 volumi     │
└──────────────────────────────────────────────────────────────┘
                              ↓
                   COMPOSITORE LIBRO  (manca)
                   PDF/EPUB/HTML finale
```

**Regola d'oro**: mai modificare strati a monte da uno strato a valle. Mai inventare contenuto non derivabile dal canone.

---

## 2. Le 7 tappe del flusso "una storia"

Per ogni nuova storia (o revisione), il flusso è sempre questo. Ogni tappa ha un input chiaro, un output verificabile, e un livello di automazione misurato.

| # | Tappa | Auto | Input | Output | Tooling |
|---|---|---|---|---|---|
| 0 | **Idea autoriale** | 0% | testa di Ray | conversazione fattuale | (chat lunga, umano puro) |
| 1 | **Narrazione fattuale** | 20% | conversazione | `narrazione_fattuale/sNN.md` | `scripts/split_narrazione_fattuale.py` |
| 2 | **Estrazione 10 hook** | 80% | narrazione + grafo + Bible + visual | proposta 10 hook in markdown | `prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md` + agente sub |
| 3 | **Review hook** | 0% | proposta | OK / edit | (Ray) |
| 4 | **Scrittura grafo** | 100% | hook approvati (YAML) | `story_graph.json` aggiornato | `scripts/write_hooks_to_graph.py --story sNN` |
| 5 | **Audit grafo** | 100%* | grafo nuovo | PASS / FAIL | `scripts/audit/audit_1..4.py` *(3/4 da implementare)* |
| 6 | **Scrittura prosa** | 60% | brief autosufficiente | `storie_finali/sNN.md` con marker | `skills/prosa/SKILL.md` + `scripts/build_writing_brief.py` |
| 7 | **Review + commit** | 20% | prosa | git push | (Ray + git) |

**Tappe critiche con review umana obbligatoria**: 3 (hook) e 7 (prosa). Mai saltarle.

**Stato fase G (estrazione hook)**: completata 2026-04-29 sulle 12 storie. 120/120 hook nel grafo.

**Stato prosa**: 12/12 storie scritte (definitive in `storie_finali/`), oggi a mano da Ray con la skill `prosa/SKILL.md` come prompt autoinizializzante in chat Claude.ai.

---

## 3. Le fasi macro che hanno costruito il sistema (storia)

Queste sono le fasi una-tantum che hanno portato la repo allo stato attuale. Non vanno rieseguite: i loro script sono **idempotenti** e i loro output sono **canone**.

### Fase E — Porting grafo (2026-04-28)
Migrazione schema legacy v1.1 → schema canonico v1.2. 60 no_inference_fields decisi via Q1-Q6 con Ray. 87 provvisori P2 tracciati. 8 misalignments resolved.
**Workspace archiviato**: `_porting_grafo/` (read-only).
**Output**: 12/12 storie nel grafo + 115 entities catalogo.

### Fase F.1 — Travaso meccanico grafo → schede (2026-04-28)
Compilazione automatica delle 56 sezioni stub di `visual/` da dati grafo. Idempotente.
**Script**: `scripts/compile_visual_from_graph.py`.

### Fase F.2 — Canonizzazione schede + immagini (in corso)
Pipeline a 6 fasi per ogni scheda: setup → scheda → prompt grok → descrizione social → immagini Grok Imagine (Ray) → push.
**Pacchetto**: `_visual_pipeline/` (canone saga + 5 template + 4 esempi validati).
**Stato**: 28 prompt grok pubblicati al 2026-04-30 (14 personaggi + 14 oggetti). 11/116 schede canonizzate complete con immagini.
**Restano**: 5 collettivi + 3 venti + 1 visual signature + 74 luoghi + strade.

### Fase G — Estensione hook visivi a 10 per storia (2026-04-29)
Ogni storia da N hook (2-8) a esattamente 10. Schema bump v1.2 → v1.3 (additivo: campi `type`, `is_signature`, `provenance`, `composition_zone`).
**Tooling**: `migrate_graph_v1_2_to_v1_3.py`, `promote_visual_entities_to_graph.py`, `write_hooks_to_graph.py` (16 controlli, dry-run/apply, backup auto).
**Output**: 120/120 hook v1.3 nel grafo (10 × 12 storie), 31 signature hook.

### Fase Cornice del Mondo — 7 step (2026-04-30)
Pacchetto autoriale Ray DOC_1..DOC_6 integrato in 7 step idempotenti.
**Tooling**: `scripts/cornice_mondo/step{1,4,5,6}*.py` + 4 YAML deterministici in `_data/`.
**Output**: nodo radice `world_conventions` (refrain animale + path_details Tier A 5 sentieri × 20 dettagli), 24 cornice_dettagli (2/storia), 36 sentieri fantasma in `locations_secondary`, 5+1 saluti gruppi collettivi (nuovo: `pescatori_case_basse`).
**Schema finale**: 1.4, graph 1.2.0.

### Fase Brieffer — Generatore zero-token writing brief (2026-04-30)
Script meccanico (no LLM) che genera brief autosufficienti per agente prosa leggendo grafo + schede + narrazione fattuale + Bible + Carta Voce.
**Script**: `scripts/build_writing_brief.py` (1128 righe). Idempotente.
**Output**: 12 brief in `writing_briefs/sNN_writing_brief.md` (16k-32k parole/brief, 13 sezioni standard).
**Reference Ray**: `_reference/s01_writing_brief_FINAL.md` — diff vuoto vs versione generata.

### Fase Prosa — 12/12 storie scritte (2026-04-30 → 2026-05-06)
Workflow: chat Claude.ai con `skills/prosa/SKILL.md` come prompt autoinizializzante → fetch brief da GitHub raw → pagina-per-pagina con review Ray.
**Output**: 12 file in `storie_finali/sNN_<slug>.md` con frontmatter YAML + marker `@hook` (10 narrativi) + marker `@subhook` (1+ pagine libro fisiche per hook).

### Fase Immagini-scena — Composizione visiva pagine libro (in corso)
Naming deterministico `_scene/sNN/sNN_hMMx.jpg` (x ∈ {a,b,c,...}). Generazione manuale Ray con Grok Imagine usando reference canonici `visual/<id>/immagini/<id>_canonica_v1_*.jpg`. Marker `@image` aggiornato da `TBD` al path reale quando l'immagine è pronta.

---

## 4. Cosa manca: il compositore libro

L'ultimo pezzo. Tutto il resto è in posizione, deterministico, machine-readable.

**Input disponibili oggi**:
- 12 file `storie_finali/sNN_<slug>.md` con marker `@hook` + `@subhook` machine-readable (parsing Python pronto in `storie_finali/README.md`)
- N immagini-scena in `_scene/sNN/sNN_hMMx.jpg` (man mano che Ray le genera)
- Cornice editoriale 4 volumi in `_volumi/` (3 storie/volume) con marker `## VOLUME N`
- Frontmatter YAML con `total_pages`, `book_pages_total`, `cycle`, `sid`, `title`

**Cosa deve fare lo script** (sintesi dalle prove di Ray):
1. Iterare sulle 12 storie in ordine canonico (cicli A/B/C/D × 3 storie)
2. Per ogni storia parsare frontmatter + marker `@hook` + `@subhook`
3. Per ogni `@subhook` recuperare:
   - testo prosa puro (tra il marker e il successivo)
   - immagine-scena dal path `@image` (fallback se `TBD`)
   - layout (singola pagina o `double_spread`)
4. Comporre PDF/EPUB/HTML rispettando l'ordine `@page_book` + cornici volume da `_volumi/`
5. Output finale impaginato

**Stato**: Ray ha già fatto prove. Manca solo l'**integrazione nella repo** (script in `scripts/composer/` o simile + dati di test + invocazione idempotente). Lavoro stimato: 1 giornata di pair Ray ↔ agente.

---

## 5. Come si fa girare il sistema oggi (comandi)

Sequenza completa per una storia ipotetica nuova `sNN`:

```bash
# 1. Stato iniziale sano
git status
python3 -c "import json; g=json.load(open('pipeline_narrativa/story_graph.json')); print('schema:', g['schema_version'], 'graph:', g['graph_version'])"

# 2. Split narrazione fattuale (se sorgente unico aggiornato)
python3 scripts/split_narrazione_fattuale.py

# 3. (Tappa 2-4) Estrazione hook → review Ray → scrittura grafo
#    Dopo che l'agente ha prodotto hooks_proposals/<ciclo>/sNN.yaml:
python3 scripts/write_hooks_to_graph.py --story sNN --dry-run
python3 scripts/write_hooks_to_graph.py --story sNN

# 4. (Tappa 5) Audit grafo — 3/4 da implementare
# python3 scripts/audit/audit_1_integrity.py
# python3 scripts/audit/audit_2_schema.py
# python3 scripts/audit/audit_3_navigability.py

# 5. Generazione brief writing per agente prosa
python3 scripts/build_writing_brief.py --story sNN
# oppure tutti:
python3 scripts/build_writing_brief.py --all

# 6. (Tappa 6) Scrittura prosa
#    Chat Claude.ai con skills/prosa/SKILL.md come prompt iniziale
#    → output: storie_finali/sNN_<slug>.md

# 7. Manutenzione strato visivo (se cambiano schede)
python3 scripts/build_catalogo_web.py

# 8. (Futuro) Composizione libro
# python3 scripts/composer/build_book.py --story sNN --format pdf
```

**Backup**: ogni script che tocca `story_graph.json` fa backup automatico con nome esplicito (es. `pre_step4_cornici.backup.json`). Catena di backup attualmente nel grafo: 6 livelli.

---

## 6. Punti di attenzione per l'automazione completa

Quando arriverà il momento di "premere un bottone e generare il libro", queste sono le tre cose che mancano e in che ordine farle:

| Priorità | Cosa | Dove | Stima |
|---|---|---|---|
| 1 | **Compositore libro** (PDF/EPUB) | `scripts/composer/` (nuovo) — Ray ha già le prove | 1 giornata |
| 2 | **4 audit grafo** (`audit_1..4.py`) | `scripts/audit/` (specs in `README.md`) | 1/2 giornata (3/4 sono Python puro; il 4° drift richiede LLM) |
| 3 | **Skill orchestratore pipeline storia** | `skills/pipeline_storia.md` (nuovo) — esegue tappe 2-7 fermandosi alle review | 1 giornata |

Tutto il resto è già in posizione: schemi stabili, script idempotenti, marker machine-readable, brief autosufficienti, canone visivo in costruzione strutturata.

---

## 7. Forze del sistema attuale (perché regge)

- **Determinismo**: tutti gli script sono idempotenti, dry-run di default, backup automatico, log umano.
- **Additività**: ogni bump di schema è retro-compatibile (mai rinomi/rimozioni di campi nel grafo).
- **Trail di audit**: `_porting_grafo/`, `_pacchetti_consegnati/`, `contributi/`, `migration_log` nel grafo, backup chain.
- **Separazione responsabilità**: 3 strati (canone / visual / libro) con regole di non-danno chiare; `pipeline_narrativa/` read-only salvo autorizzazione esplicita.
- **Zero-token dove possibile**: brieffer, compilatore, writer hook, sentieri, cornici → tutti meccanici. LLM solo dove serve davvero (estrazione hook, prosa).
- **Marker machine-readable**: `@hook` + `@subhook` nelle storie finali → compositore può lavorare senza ambiguità.

---

## 8. Punti di fragilità (cose da tenere d'occhio)

- **Audit grafo**: 3/4 specificati ma non implementati. Oggi i controlli stanno dentro il writer hook; per scalare servono fuori.
- **Coerenza visual ↔ grafo**: travaso inverso (Fase F.3) non ancora fatto. Le schede `visual/` in canonizzazione possono accumulare dettagli che il grafo non conosce.
- **Generazione immagini esterna**: Grok Imagine non è scriptabile via API stabile. Ray fa il loop a mano. Se cambia il provider, le 4 immagini canoniche per personaggio sono la barriera contro drift di stile.
- **Compositore mancante**: senza di lui, le storie e le immagini-scena restano file isolati.

---

## 9. Riferimenti per chi entra a freddo

- `CLAUDE.md` — **leggi sempre per primo**. Mappa repo + regole di non-danno.
- `docs/PIPELINE.md` — flusso 7 tappe in dettaglio.
- `PROJECT_STATE.md` — snapshot operativo (cronologico).
- `_visual_pipeline/README.md` — pipeline visual canonizzazione.
- `pipeline_narrativa/storie_finali/README.md` — schema marker `@hook` / `@subhook` + parsing Python d'esempio.
- `skills/prosa/SKILL.md` — agente prosa.
- `skills/brieffer/SKILL.md` — agente brieffer.
- `scripts/cornice_mondo/` — pacchetto cornice del mondo (pattern replicabile per future estensioni Tier B/C).

---

**TL;DR**: la pipeline è completa al ~90%. Le 12 storie sono scritte, il canone è stabile, gli script sono deterministici, i marker sono machine-readable. Manca solo il compositore libro finale (lavoro di 1 giornata) e gli audit grafo a regime (1/2 giornata). Quando questi due tasselli saranno in posto, il flusso "idea Ray → libro PDF" sarà eseguibile in un singolo run end-to-end.
