# Fasi completate — trail di audit (estratto integrale dal CLAUDE.md v2.x)

> **Archivio storico.** Questo file conserva, senza modifiche, le sezioni cronologiche del CLAUDE.md
> pre-riordino (v2.x, ultima revisione 2026-06-10 notte tarda). Il CLAUDE.md attuale è un router:
> regole stabili + tabella di instradamento. Lo **stato corrente** vive in `PROJECT_STATE.md`;
> le **procedure operative vive** vivono nelle skill (`skills/<ruolo>/SKILL.md`) e nei README dedicati
> (`pipeline_narrativa/storie_finali/README.md` per il compositore, `docs/PIPELINE.md` per il flusso storia).
> Niente di ciò che segue è stato perso: è stato ricollocato.

## Header e changelog del CLAUDE.md v2.x

Versione: 2026-06-10 notte tarda (4 PR consecutive: canonizzazione 11 personaggi `status: canonico`, 7 luoghi promossi al catalogo dalla branch illustratore, cronologia semi ricomparsa nel sito storia, riordino layout hook per workflow Manus; 101 immagini catalogate, 15 canonici. TODO domani: debug Vercel deploy fermo alle 16:23 UTC). Versioni precedenti: 2026-06-10 sera (promozione 11 reference dal volume al catalogo + fix SKILL); 2026-06-10 pomeriggio (catalogo v2 Next.js + cutover Vercel mirror dati); 2026-06-10 mattina (blindatura completa, 7 incoerenze canone risolte, cancello CI alzato); 2026-06-09 (pacchetto blindatura); 2026-06-08 (impaginazione volumi KDP).

---


### Fase E — COMPLETATA (2026-04-28)

Migrazione una-tantum del grafo da schema legacy v1.1 a schema canonico v1.2:
- **12/12 storie** in `pipeline_narrativa/story_graph.json` v1.1.0-pre schema 1.3 (post-bump fase G)
- **60 no_inference_fields decisi** via Q1-Q6 autoriali Ray (entry_point_type, closure_type, register, estimated_length, descriptive_pauses_count per ogni storia)
- **87 provvisori P2** (22A + 47B + 18C) tracciati nei provisional file di `_porting_grafo/output/`
- **8 misalignments tutti resolved** (mis_001..mis_007 + mis_008)
- **Catalogo isola_i3v_visual: 115 entities** (114 visual + 1 nuovo `pallone_di_stoffa_cucita` come `oggetto_di_scena_ricorrente`)
- **Backup pre-migrazione**: `pipeline_narrativa/story_graph.v0.10.0.backup.json`

### Fase F — IN CORSO (2026-04-28+)

Compilazione body schede `visual/` usando il grafo come fonte autorevole + canonizzazione completa via `_visual_pipeline/`:
- **F.1 (fatto, meccanico)**: `scripts/compile_visual_from_graph.py` ha travasato dati grafo → 56 sezioni stub compilate (Identità visuale, Espressione/comportamento, Cliché da evitare, Storie/scene di apparizione).
- **F.2 (in corso, in collaborazione con Ray)**: completamento delle 115 schede a canone chiuso via `_visual_pipeline/` (vedi sezione dedicata sotto). 11/115 schede già canonizzate al 2026-04-29 (Fiamma, Bartolo, Forno, 7 luoghi, grembiule_fiamma, Gabriel parziale). 8 immagini canoniche generate (4 Fiamma + 4 Bartolo).
- **F.3 (pianificata)**: travaso inverso visual → grafo per dettagliare gli `entities` del grafo dove le schede hanno info aggiuntiva.

### Visual pipeline (`_visual_pipeline/`) — Fase F.2 operativa

Pacchetto operativo a livello root della repo per **completare le 115 schede `visual/`** con canone chiuso e immagini canoniche generate. Sviluppato da Ray in chat dedicata, validato.

- **Entry point:** `_visual_pipeline/README.md`
- **Flusso 6 fasi (per scheda):** Setup (lettura canone + template + fonti) → scheda.md → prompt_grok.md (per personaggi/oggetti) o blocco LOCATION testuale (per luoghi) → descrizione_narrativa_social.md → generazione immagini con Grok Imagine (Ray) → push GitHub → eventuale aggiornamento canone
- **Canone saga (read-only, 3 doc):** `_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md`, `02_SAGA_SCALE_v1.md` (Gabriel = 1.0 GU), `03_SAGA_PALETTE_v1.md`
- **Template (5):** `_visual_pipeline/_templates/TEMPLATE_scheda_{personaggio,oggetto,luogo}.md`, `TEMPLATE_prompt_grok_personaggio.md`, `TEMPLATE_descrizione_narrativa_social.md`
- **Esempi validati:** `_visual_pipeline/_esempi/{fiamma,bartolo,forno,grembiule_fiamma}/` — pipeline personaggi e luoghi entrambe robuste (testate su 2 specie diversissime + 1 luogo complesso 3 blocchi LOCATION)
- **Output deliverable per scheda:**
  - **Personaggi:** scheda + prompt_grok + descrizione_social + 4 immagini canoniche in `immagini/`
  - **Oggetti:** scheda + prompt_grok + descrizione_social + 1-2 immagini
  - **Luoghi:** scheda con BLOCCO LOCATION testuale + descrizione_social (NO immagini reference, le proporzioni si rompono — strategia "blocco LOCATION testuale + reference personaggi")
  - **Luoghi complessi (es. Forno):** PIÙ blocchi LOCATION distinti nella stessa scheda (esterno/interno/cortile). Mai mischiare blocchi nel prompt scena.
- **Naming immagini canoniche:** `<id>_canonica_v1_<vista>.jpg` (es. `fiamma_canonica_v1_fronte.jpg`) + `<id>_turnaround_v1.jpg`. Le `_canonica_v1_*` sono intoccabili come reference.
- **Vincoli operativi:** mai modificare `pipeline_narrativa/` (read-only), mai inventare contenuto non derivabile, mai modificare `_canone/*.md` senza autorizzazione + bump versione, mai pushare su main senza il via di Ray, sempre rigenerare `catalogo_web/data/entities.json` dopo modifiche a `visual/`.
- **Ordine consigliato di completamento:** test/validazione → tre fratelli (anchor scala) → primari → secondari → cuccioli → collettivi → oggetti → luoghi per quartiere → strade → venti+signatures.

Vedi `_visual_pipeline/README.md` + `_visual_pipeline/_skill/PIPELINE.md` per il flusso completo.

### Fase G — COMPLETATA (2026-04-29)

Estensione hook visivi: ogni storia da N (2–8 attuali) a esattamente **10** `visual_anchors.scene_hooks`.

**Schema bump GIÀ ESEGUITO** (2026-04-29): grafo v1.0.0 → v1.1.0-pre + schema v1.2 → v1.3 (estensione additiva). Nuovi campi obbligatori su hook `extended_v2`: `type`, `is_signature`, `provenance`, `composition_zone`. I 70 hook legacy esistenti sono ora `provenance: original_v1` (campi additivi opzionali). Promuove a v1.1.0 stabile alla prima scrittura. Vedi `scripts/migrate_graph_v1_2_to_v1_3.py`.

- **Input fattuale**: `pipeline_narrativa/narrazione_fattuale/s0X_*.md` (12/12 disponibili al 2026-04-29; sorgente unico in `_source/Ciclo*.txt`, split via `scripts/split_narrazione_fattuale.py`).
- **Prompt operativo**: `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md`.
- **Workflow per ciclo (modalità deterministica):**
  1. agente legge narrazione fattuale + grafo + Bible + Carta Voce + visual + cartografia
  2. agente propone i 10 hook in markdown a Ray (vedi prompt)
  3. su OK Ray → l'agente (o Ray stesso) crea `pipeline_narrativa/hooks_proposals/<ciclo>/sNN.yaml` con i 10 hook in formato deterministico
  4. validazione: `python3 scripts/write_hooks_to_graph.py --story sNN --dry-run` (16 controlli, vincoli editoriali del prompt)
  5. scrittura: `python3 scripts/write_hooks_to_graph.py --story sNN` oppure `--cycle <A|B|C|D>` per batch
  6. il writer fa backup automatico (one-shot), bumpa graph_version a 1.1.0 stabile, appende migration_log
- **Tipologie hook** (campo `type`): `panorama|azione|introspettivo|atmosferico|transizione|interno|dettaglio` (rinominato da `interno_caldo` il 2026-04-29).
- **Audit grafo posteriore** (separato dal writer): `scripts/audit/audit_1..4.py` — **implementati 2026-06-09** (vedi `scripts/audit/README.md`). Girano in CI su ogni push/PR; in locale: `make audit`. NB regola operativa: focal_action ≤ **30** parole (il writer ha sempre applicato 30; le docstring storiche dicevano 25).
- **Modalità**: una storia alla volta, con approvazione Ray tra storia e storia.
- **Output finale atteso**: `pipeline_narrativa/story_graph.json` con 120 hook totali (10 × 12 storie), tutti validati.

**Stato fase G: COMPLETATA il 2026-04-29.**
- Tutti e 4 i cicli scritti (A: s01-s03, B: s04-s06, C: s07-s09, D: s10-s12)
- 120/120 hook v1.3 nel grafo (10 × 12 storie), 31 signature totali (max 3/storia)
- Workflow validato: Ciclo A scritto direttamente da Ray, Cicli B-D estratti via agente sub general-purpose con prompt mirato + review umana + edit minimi
- Tempo medio per storia: ~3-5 min agente sub + ~5 min review + write
- Backup chain: `pre_v1_3.backup.json` → `pre_fase_g.backup.json` → grafo corrente

### Fase F.2 visual prompt grok — IN CORSO (28/115 al 2026-04-30)

Generazione prompt grok canonici per le 115 schede `visual/`. Workflow esterno: Ray estrae prompt da GitHub e genera con **Grok Imagine** (sostituisce piano Flux precedente — Grok rispetta meglio lo stile saga).

**Pubblicato al 2026-04-30 (28 prompt grok totali):**
- 14 personaggi: 3 fratelli (Gabriel/Elias/Noah, opzione B fittizio canonico), 4 primari (Rovo/Stria/Mèmolo/Grunto), 4 secondari (Salvia/Nodo/Amo/Zolla), 5 cuccioli (Pun/Toba/Bru/Cardo/Liù). Fiamma e Bartolo già canonizzati con immagini in 2026-04-29.
- 14 oggetti: 13 oggetti-simbolo + grembiule_fiamma + pallone_di_stoffa_cucita.

**Restano da fare (al 2026-04-30):**
- 5 collettivi (Camminanti, Mantenitori, Coltivatori, Mercato, Pastori) + Pescatori delle case basse
- 3 venti (Taglio, Intreccio, Mulinello) + 1 visual_signature (quando_acqua_trema)
- 74 luoghi (per quartiere, strade)

### Fase Cornice del Mondo — COMPLETATA (2026-04-30)

Pacchetto consegnato da Ray come 6 documenti DOC_1..DOC_6 + README in root. **7 step eseguiti** con script idempotenti dry-run/--apply, backup automatico, idempotenza verificata.

| Step | Cosa | Commit | Output principale |
|---|---|---|---|
| 1+2 | nodo radice `world_conventions` + extends `quote_tracker` + bump versioni | `c824496` | `refrain_animal_identification` (formula sg/pl), `path_details: { paths: {} }`, `quote_tracker.refrain_animal_used_per_story: []` |
| 3 | saluti gruppi nelle 5+1 schede catalogo collettivi | `a3e654e` | `## Saluto del gruppo` + nuova scheda `pescatori_case_basse/` (6° gruppo) |
| 4 | 24 cornici nelle 12 storie + 8 formule + 2 cantilene | `8b70958` | `stories.<sid>.cornice_dettagli` (2 per storia) |
| 5 | sentieri "fantasma" in `locations_secondary` | `92e87b6` | 36 sentieri appesi |
| 6 | path_details Tier A (5 sentieri × 20 dettagli) | `83e361e` | `world_conventions.path_details.paths.<id>` |
| 7 | schede sentieri Tier A aggiornate | `de87ac2` + `9b8c30e` | `## Coerenza cross-scena` con dettagli stabili |

**Decisioni autoriali Ray applicate (2026-04-30):** 6° gruppo Pescatori SI; Pattern A pre-eco s03 NO; narrator_address s09 NO; riequilibrio Giro E SI; schema slot dettaglio senza campo `tipo`; vincolo "tre nomi" in plurale; vincolo unicità saga animale.

**Tooling cornice del mondo:** `scripts/cornice_mondo/{step1,step4,step5,step6}*.py` (idempotenti, --dry-run di default, backup auto), `scripts/cornice_mondo/_data/*.yaml` (4 file dati deterministici).

**Stato grafo finale:** schema 1.4, graph 1.2.0. **Backup chain:** + 4 nuovi backup canonici (`pre_cornice_mondo`, `pre_step4_cornici`, `pre_step5_sentieri`, `pre_step6_path_details`).

### Fase Brieffer — COMPLETATA (2026-04-30)

Pacchetto `brieffer_pkg` installato. Generatore meccanico (zero token LLM) di brief writing autosufficienti per agente prosa.

- **Script:** `scripts/build_writing_brief.py` (1128 righe). Usa: `--story sNN` o `--all`. Output in `pipeline_narrativa/writing_briefs/sNN_writing_brief.md`.
- **Skill:** `skills/brieffer/SKILL.md`.
- **12 brief generati** (16k-32k parole/brief, idempotente).
- **Reference Ray validato:** `pipeline_narrativa/writing_briefs/_reference/s01_writing_brief_FINAL.md` — `s01_writing_brief.md` generato dallo script è IDENTICO (1730 righe, diff vuoto).
- **13 sezioni standard** per brief: frontmatter operativo, core narrativo, narrazione fattuale integrale, 10 hook visivi, cast in scena (voci + canone visivo), cornici del mondo, sentieri attraversati con dettagli, saluti, formula ritornello, vincoli universali (PATTERN_AI_DA_BANDIRE integrale), quote tracker awareness, echi/callback/semi, istruzione operativa.

**Quando rilanciare lo script:** dopo modifiche a grafo / schede catalogo / prompt grok / narrazione fattuale. Idempotente: sovrascrive con versione aggiornata.

**Cosa NON fa:** non scrive prosa (compito agente prosa, oggi gestito a mano da Ray), non modifica il grafo, non chiama API LLM.

---

## 4. Modalità operative (chi fa cosa)

### Modalità "agente cartografo"
Manutenzione cartografia. Solo `cartografia/`. Vedi `skills/cartografo.md`.

### Modalità "agente visual / compilatore"
Compilazione schede `visual/`. Vedi `skills/visual/compilatore.md`.
- Travaso meccanico fonte → scheda (no inferenza)
- Sostituisce solo placeholder `_da popolare dal grafo_`
- Rigenera `catalogo_web/data/entities.json` dopo modifiche

### Modalità "agente visual pipeline" (canonizzazione schede + immagini)
Completamento canonico delle schede `visual/` via `_visual_pipeline/`. Vedi `_visual_pipeline/README.md` + `_visual_pipeline/_skill/PIPELINE.md`.
- **Lettura obbligatoria**: 3 doc canone saga (`_visual_pipeline/_canone/`), template della tipologia, esempio validato (`_visual_pipeline/_esempi/`)
- **Output per scheda (personaggio):** `scheda.md` + `prompt_grok.md` + `descrizione_narrativa_social.md` (Claude) → 4 immagini canoniche con Grok Imagine (Ray)
- **Output per scheda (luogo):** `scheda.md` con BLOCCO LOCATION testuale (anche multipli per luoghi complessi) + `descrizione_narrativa_social.md`. NO `prompt_grok.md` per luoghi.
- **Output per scheda (oggetto):** scheda + prompt + descrizione + 1-2 immagini canoniche
- **Naming immagini canoniche:** `<id>_canonica_v1_<vista>.jpg` + `<id>_turnaround_v1.jpg`
- **Vincoli:** mai modificare canone (`_visual_pipeline/_canone/*.md`) senza autorizzazione + bump versione, sempre rigenerare `catalogo_web/` dopo modifiche, sempre branch dedicato + merge ff su main

### Modalità "lettore + commentatore" (collaboratore esterno)
Vedi sezione 5 (regole rigorose).

### Modalità "porting grafo"
**Non più attiva.** Fase E completata. Riferimento storico in `_porting_grafo/`.

### Modalità "estensione hook visivi" (fase G)
Ampliamento dei `visual_anchors.scene_hooks` da N a 10 per storia. Vedi `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md`.

- **Lettura**: 7 fonti di verità nell'ordine prescritto (vedi prompt).
- **Scrittura**: SOLO `pipeline_narrativa/story_graph.json#stories.s0X.visual_anchors.scene_hooks` + metadati `graph_version`, `last_updated`, `phase`. Nient'altro.
- **Step obbligatori**: lettura → inventario candidati → selezione 10 → compilazione → proposta a Ray → ATTESA approvazione → scrittura → audit (4 script) → conferma.
- **Una storia alla volta.** Mai parallelo. Mai saltare l'approvazione.

### Modalità "cornice del mondo" (fase 2026-04-30)
**COMPLETATA.** Pacchetto `cornice_mondo` consegnato + 7 step eseguiti. Pattern di lavoro replicabile per pacchetti futuri tipo Tier B/Tier C dettagli sentieri.

- **Pattern script:** idempotente, `--dry-run` di default, `--apply` scrive con backup auto, log umano, dati separati in YAML deterministici.
- **Vincoli:** SEMPRE additivo + retrocompatibile (mai rinomi/rimozioni nel grafo). Backup canonici con nome esplicito (es. `pre_step4_cornici.backup.json`). Audit posteriore.
- **Approvazione Ray esplicita richiesta** prima di toccare il grafo (eccezione alla regola "pipeline_narrativa read-only").

### Modalità "brieffer" (zero-token writing brief generator)
Genera brief autosufficienti per agente prosa (oggi: Ray scrive a mano).

- **Comando:** `python3 scripts/build_writing_brief.py --story sNN` o `--all`.
- **Output:** `pipeline_narrativa/writing_briefs/sNN_writing_brief.md`.
- **Skill:** `skills/brieffer/SKILL.md` (procedura standard).
- **Quando rilanciare:** dopo modifiche a grafo / schede catalogo / prompt grok / narrazione fattuale. Idempotente.

### Modalità "compositore libro" (script attivo dal 2026-06-08)
Lo script `scripts/build_volume.py` + modulo `scripts/design_system.py` assemblano i PDF per stampa Amazon KDP (A5, 300 DPI, bleed 3.175 mm, pagine sempre pari) leggendo i testi definitivi e le immagini composte.

- **Output (in `_output/`, ignorato da git):**
  - `vol{N}_libro.pdf` — spread affiancati (sfogliabile a video)
  - `vol{N}_stampa.pdf` — pagine singole A5 (file di stampa KDP)
  - `vol{N}_LAYOUT_WARNINGS.md` — testi troncati o immagini sotto spec da correggere
- **Mappatura volumi:** Vol1=Ciclo A (s01-s03), Vol2=B (s04-s06), Vol3=C (s07-s09), Vol4=D (s10-s12). 3 storie per volume.
- **Asset richiesti:**
  - Font in `assets/fonts/` (Fraunces, Nunito, Fredoka, Lora — OFL, già in repo)
  - Immagini scena: usa `_hd/sNN_hMMx_hd.jpg` se esiste, altrimenti fallback low-res `sNN_hMMx.jpg`
  - Immagini intro volume: `pipeline_narrativa/storie_finali/_volumi/v0N/_hd/v0N_intro_<slug>_hd.jpg`
  - Reference catalogo: `visual/<categoria>/<id>/immagini/<id>_canonica_v1_*.jpg` con `_hd/` opzionale
- **Esecuzione:** `pip install Pillow reportlab --break-system-packages` poi `python3 scripts/build_volume.py --volume 1` (vedi sezione 7).
- **Test:** suite `tests/` (60 test, ~4s veloci + ~60s integration). Eseguire `python3 -m pytest tests/ -m "not slow"` prima di ogni release/modifica allo script. Vedi `tests/README.md`.
- **Input:** `pipeline_narrativa/storie_finali/sNN_<slug>.md` (12 file con frontmatter YAML + 10 marker `@hook` narrativi + N marker `@subhook` pagina libro fisica per storia).
- **Due livelli di marker (machine-readable):**
  - **`@hook` (livello narrativo, 10 per storia):**
    ```
    <!-- @hook sNN_hMM | @page MM | @subhooks [sNN_hMMa, sNN_hMMb] | @image TBD -->
    ```
    `@page` = numero hook (1..10), `@subhooks` = lista figli, `@image` = (legacy) path composto a livello hook.
  - **`@subhook` (livello pagina libro, 1+ per hook):**
    ```
    <!-- @subhook sNN_hMMx | @page_book K | @image pipeline_narrativa/storie_finali/_scene/sNN/sNN_hMMx.jpg -->
    ```
    `x ∈ {a,b,c,...}`, `@page_book` = pagina libro fisica (1..book_pages_total, total nel frontmatter), `@layout` (opz.) = `double_spread` per spread doppia, `@image` = path immagine-scena composta.
- **Pattern `_scene/`:** immagini-scena composte in `pipeline_narrativa/storie_finali/_scene/sNN/sNN_hMMx.jpg`. Naming deterministico, una pagina libro = un file. **NON sono reference catalogo** (quelle stanno in `visual/<categoria>/<id>/immagini/<id>_canonica_v1_<vista>.jpg`). Le `_scene/` sono il prodotto finale composto per il libro.
- **Documentazione completa:** `pipeline_narrativa/storie_finali/README.md` (include esempio parsing Python a 2 livelli).
- **Vincoli:** mai modificare `@hook` né `@subhook` id (stabili, legati a brief / prompt grok / `_scene/` / pipeline composizione). `@image` aggiornabile da `TBD` al path reale quando immagine pronta.

### Modalità "agente prosa" (scrittura collaborativa)
Scrive il testo finale di una delle 12 storie in chat collaborativa con Ray, una pagina alla volta.

- **Skill:** `skills/prosa/SKILL.md`. Si incolla all'inizio di una chat Claude.ai (è prompt autoiniziante).
- **Workflow:** chat Claude.ai → incolla SKILL → Ray dice quale storia → agente fetcha brief da GitHub raw → conferma + piano → scrive pagina 1 → aspetta "vai" di Ray → pagina 2 → ... → consuntivo dopo pagina 10.
- **Input canonico:** `pipeline_narrativa/writing_briefs/sNN_writing_brief.md` (autosufficiente, generato da `build_writing_brief.py`).
- **Output:** testo finale del libro, voce autoriale picture book 3-6 anni, italiano. Mai prosa fuori dai 10 blocchi-pagina.
- **Vincoli forti:** frasi-codice dei personaggi inalterabili, formula ritornello solo dove brief la indica, pattern AI da bandire integrale, una pagina = un hook visivo, mai 2 pagine in fila senza pausa Ray.
- **Modalità ortogonale alle altre:** non tocca grafo, non tocca catalogo, non tocca cartografia. Lavora solo nella chat.

### Modalità "starter kit" (template di sistema riusabile)
Costruzione e manutenzione del template scaricabile in `_starter_kit/`. Concetto: chi scarica quella directory deve poter avviare il proprio progetto narrativo tipo-isola (saga, libro illustrato, mondo di fantasia) senza alcun residuo del contenuto specifico de "L'Isola dei Tre Venti". Punto d'ingresso: `_starter_kit/README.md`.

- **Scope di scrittura:** SOLO `_starter_kit/`. Tutto il resto della repo (`pipeline_narrativa/`, `visual/`, `cartografia/`, `catalogo_web/`, `_visual_pipeline/`, `_porting_grafo/`, `_pacchetti_consegnati/`, `contributi/`, `scripts/`, `skills/`, `docs/`) è **read-only**. Si può **leggere** per capire pattern (es. struttura di un brief, stile di uno script idempotente con `--dry-run`, naming convention dei marker `@hook`/`@subhook`), si può **scrivere solo** dentro `_starter_kit/`.
- **Cosa va dentro:** scheletro cartelle (`pipeline_narrativa/`, `visual/`, `cartografia/`, `catalogo_web/`, `scripts/`, `skills/` vuoti o con `.gitkeep`), template di scheda (personaggio/luogo/oggetto), template di brief writing, prompt operativi generici, script idempotenti adattati (con placeholder per nomi progetto), skill agente IA (`SKILL.md` per ogni modalità riusabile), README di setup passo-passo.
- **Cosa NON va dentro:** prosa della saga, schede di personaggi/luoghi/oggetti reali (Gabriel, Fiamma, Forno, ecc.), prompt grok del canone, snippet di `story_graph.json`, immagini canoniche di entità reali, contenuto di `pipeline_narrativa/documenti_progetto/` (Bible, Carta Voce, ARCHI, Glossario, EAR, Pattern AI da bandire). Se serve un esempio concreto, usa nomi placeholder (`<personaggio_esempio>`, `<luogo_esempio>`, `<id_oggetto>`).
- **Pattern script:** idempotenti, `--dry-run` di default, `--apply` per scrivere, backup automatico, log umano (vedi `scripts/cornice_mondo/step*.py` per riferimento di stile).
- **Vincoli:** mai modificare `CLAUDE.md`, `README.md`, `PROJECT_STATE.md`, `SYNC_LOG.md` in root della repo (sono file di stato della saga, non parte del template). La directory `_starter_kit/` ha un proprio README interno autosufficiente.
- **Branch:** branch dedicato `claude/starter-kit-<scope>` con merge fast-forward su `main`.
- **Commit prefix:** `starter_kit:` per riconoscibilità (es. `starter_kit: scheletro cartelle iniziale`).

---

## [dal CLAUDE.md v2.x §9] Standard immagini HD per stampa (aggiornato a standard scene v1.1)

> Fonte viva: `skills/illustratore/SKILL.md` e `skills/scenografo/SKILL.md` (la sezione sotto è la copia storica).

Le immagini per **stampa del libro** convivono con i reference digitali low-res in una struttura **`_hd/`** dedicata, per non sostituire i low-res e mantenere ortogonalità (browsing veloce vs file pesanti).

### Convivenza low-res + HD

```
<cartella canonica>/<id>.jpg          ← LOW-RES reference digitale (browsing, catalogo web)
<cartella canonica>/_hd/<id>_hd.jpg   ← HD per stampa (JPG q95, ≥1824×2736 px, DPI metadata 300)
```

I marker `@image` nei file `.md` puntano SEMPRE al low-res. Lo script compositore libro `scripts/build_volume.py` (attivo dal 2026-06-08, in attivo affinamento) cerca prima `_hd/<id>_hd.jpg`, fallback su low-res.

### I 3 contesti di destinazione

| Contesto | Path HD |
|---|---|
| **Hook di storia** | `pipeline_narrativa/storie_finali/_scene/sNN/_hd/sNN_hMMx_hd.jpg` |
| **Intro volume** | `pipeline_narrativa/storie_finali/_volumi/v0N/_hd/v0N_intro_<slug>_hd.jpg` |
| **Catalogo reference canoniche** | `visual/<categoria>/<id>/immagini/_hd/<id>_canonica_v1_<vista>_hd.jpg` |

### Specifiche file HD (obbligatorie)

- **Formato:** JPEG (estensione `.jpg`), qualità 95
- **Profilo colore:** RGB sRGB (la conversione CMYK è dello stampatore)
- **Risoluzione minima:** **1824×2736 px** verticale 2:3 — calcolata sul fit reale di `scripts/build_volume.py` (pagina al vivo A5 + bleed 3.175 mm = 1824×2556 px a 300 DPI, l'immagine 2:3 più piccola che copre quel rettangolo è 1824×2736). Ideale 2000×3000 px o superiore.
- **DPI metadata:** **impostare il metadato DPI del JPEG a 300** (informativo per lo stampatore; il rendering del compositore usa pixel + dimensione fisica)
- **Peso file:** 300-700 KB tipico, fino a ~1 MB
- **Naming:** lowercase, snake_case, suffisso obbligatorio `_hd`, mai `.jpeg`/`.JPG`/spazi/maiuscole
- **Standard precedente:** 1664×2496 accettato per le scene di s01 consegnate a 2026-05 (resta valido come v1); dal 2026-06 nuovo minimo 1824×2736.

### Workflow upload (per illustratore — IA o umano)

1. **Branch dedicata** `claude/hd-<scope>` (es. `claude/hd-storia-s02`, `claude/hd-intro-v02`, `claude/hd-catalogo-primari`)
2. **Crea `_hd/`** nel contesto giusto e copia i file con suffisso `_hd.jpg`
3. **Un solo commit** per branch, messaggio standard (vedi `skills/illustratore/SKILL.md`)
4. **Push + PR** verso main, NON mergiare in autonomia
5. **Review** (Ray o agente review) verifica path/naming/formato/diff pulito prima del merge

### Vincoli

- ❌ Mai **sostituire** i low-res esistenti con la HD (HD va in `_hd/`, low-res resta dov'era)
- ❌ Mai mischiare HD + codice app web + modifiche `.md` nella stessa branch (uno scope = una branch)
- ❌ Mai 34 commit atomici "Aggiunge X / Rimuove Y" (un commit per branch)
- ❌ Mai cambiare estensione dei marker `@image` nei `.md` (restano puntati al low-res)
- ❌ Mai PNG (5-10 MB cad.) — solo JPEG q95 (300-700 KB cad.)
- ❌ Mai push diretto su `main`

### Skill di riferimento

**Sempre** `skills/illustratore/SKILL.md` per il workflow completo (passo-passo + esempi + checklist).

### Stato applicato (2026-05-19)

- `_scene/s01/_hd/` — 17 file HD storia 1 (Ciclo A, prima storia) ✅
- `_volumi/v01/_hd/` — 11 file HD intro Volume 1 (Ciclo A apre il libro) ✅
- Da fare: 11 storie restanti, 3 volumi restanti, catalogo completo HD
