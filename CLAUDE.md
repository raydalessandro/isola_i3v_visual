# CLAUDE.md — Istruzioni per istanze IA + collaboratori

Questo file spiega come funziona la repo `isola_i3v_visual` e cosa devi (e non devi) fare quando ci lavori. **Leggilo sempre per primo.**

Versione: 2026-06-10 (blindatura completa: 7 incoerenze del canone risolte via `scripts/cornice_mondo/step8_fix_canonical_refs.py`, baseline `known_issues.yaml` svuotata, cancello CI alzato). Versione precedente: 2026-06-09 (pacchetto blindatura: 4 audit + manifest + baseline + CI + scritture atomiche + Makefile). 2026-06-08 (script definitivo impaginazione volumi KDP).

---

## TL;DR (in 30 secondi)

1. **Repo del progetto "L'Isola dei Tre Venti"** (saga 12 storie illustrate per bambini 4-10, autore: Ray).
2. **Tre tracce di lavoro attive**: `cartografia/` (mappa), `visual/` (descrizioni entità), `pipeline_narrativa/` (grafo + Bible — **read-only**).
3. **Una traccia archiviata**: `_porting_grafo/` (migrazione una-tantum del grafo, completata, NON toccare).
4. **Una traccia per contributi esterni**: `contributi/` (proposte di aggiunta schede — solo create file nuovi datati, mai modificare esistenti).
5. **Una traccia di starter kit (template di sistema)**: `_starter_kit/` (scheletro riusabile del framework per chi vuole farsi la propria "isola" — directory dedicata, **mai contaminare** con contenuto narrativo specifico della saga).
6. **Una traccia di illustratore esterno** (caricamento immagini HD per stampa): branch dedicate `claude/hd-*` con subdir `_hd/`. Vedi sezione 9 + `skills/illustratore/SKILL.md`.
7. **Mai modificare** `pipeline_narrativa/` (grafo + Bible) senza autorizzazione esplicita.
8. **Mai inventare contenuto narrativo**. Riporta solo dati esistenti nelle fonti canoniche o segnala se mancano.
9. **Sempre fare commit chiari** sul branch corrente, **mai push --force**, **mai modificare commit altrui**.

## Pipeline operativa (per nuova storia)

Per il **flusso end-to-end** dall'idea autoriale di Ray al testo libro committato (7 tappe, ~70% automatizzabile), vedi **[`docs/PIPELINE.md`](./docs/PIPELINE.md)**.

In sintesi: idea autoriale (Ray, chat) → narrazione fattuale → estrazione 10 hook visivi → review hook → scrittura grafo → audit → prosa autoriale → review → commit. Ad ogni tappa il documento dice quale prompt/script usare e che file produce.

---

## 1. Mappa della repo

```
isola_i3v_visual/
│
├── pipeline_narrativa/        ⚠️ READ-ONLY (canone narrativo)
│   ├── story_graph.json              v1.2.0 schema 1.4 (post-cornice-del-mondo: world_conventions root + cornice_dettagli + path_details)
│   ├── story_graph.v0.10.0.backup.json  backup pre-migrazione fase E
│   ├── story_graph.json.pre_v1_3.backup.json  backup pre-bump schema 1.2->1.3
│   ├── story_graph.json.pre_fase_g.backup.json  backup pre-hook estesi
│   ├── story_graph.json.pre_cornice_mondo.backup.json  backup pre-Step 1+2 (2026-04-30)
│   ├── story_graph.json.pre_step4_cornici.backup.json  backup pre-Step 4 (2026-04-30)
│   ├── story_graph.json.pre_step5_sentieri.backup.json backup pre-Step 5 (2026-04-30)
│   ├── story_graph.json.pre_step6_path_details.backup.json backup pre-Step 6 (2026-04-30)
│   ├── story_graph.json.pre_step8_canonical_refs.backup.json backup pre-Step 8 (2026-06-10)
│   ├── hooks_proposals/<ciclo>/sNN.yaml  input deterministici per write_hooks_to_graph.py
│   ├── narrazione_fattuale/sNN_*.md  12/12 file narrazione fattuale derivati dal sorgente _source/
│   ├── writing_briefs/sNN_writing_brief.md  12 brief autosufficienti per agente prosa (output zero-token brieffer)
│   ├── writing_briefs/_reference/    s01_writing_brief_FINAL.md (reference Ray, validato)
│   ├── storie_finali/sNN_<slug>.md   12 testi prosa DEFINITIVI con frontmatter YAML + marker @hook (narrativo, 1..10) + marker @subhook (pagina libro fisica, 1..book_pages_total) machine-readable per script compositore libro futuro (vedi storie_finali/README.md)
│   ├── storie_finali/_annotations/   YAML autoriali Ray (sNN.yaml) — note di scena
│   ├── storie_finali/_inventory/     inventari testuali derivati (audit/QA prosa)
│   ├── storie_finali/_scene/sNN/     immagini-scena composte per pagina libro fisica (sNN_hMMx.jpg low-res, x ∈ {a,b,c,...}), referenziate dal marker @subhook ... @image. Subdir `_hd/sNN_hMMx_hd.jpg` per versione HD stampa (JPG q95, ≥1664×2496 px). NON sono reference catalogo (quelle stanno in visual/<categoria>/<id>/immagini/)
│   ├── storie_finali/_volumi/        cornice editoriale 4 volumi (3 storie/volume, 1:1 con cicli A/B/C/D): soglia, introduzioni_cicli, stato_zero_e_sigilli, presentazione_completa, presentazioni_parziali, porte, congedo + _elementi_fissi/ (riferimenti read-only) + v0N/_hd/v0N_intro_<slug>_hd.jpg per illustrazioni HD intro volume. Marker ## VOLUME N interni per compositore libro
│   └── documenti_progetto/           Bible, Carta Voce, ARCHI, Glossario, EAR, Pattern AI da bandire
│
├── visual/                    ✅ scrittura su scheda.md per arricchimento (con cautela) + immagini canoniche + prompt_grok.md
│   ├── personaggi/                   24 schede (3 fratelli, 5 primari, 5 secondari, 5 cuccioli, 6 collettivi inclusi pescatori_case_basse)
│   │   │  ⚠️ NB: la Bible usa "Abitanti maggiori" per gli stessi 5 di `primari/` — stesso insieme, vocabolari diversi (narrativo vs filesystem)
│   │   ├── individuali/{bambini,primari,secondari,cuccioli}/<id>/  scheda.md + prompt_grok.md (28 prompt grok pubblicati al 2026-04-30) + immagini/
│   │   └── collettivi/{camminanti,mantenitori,coltivatori_del_cerchio,mercato_del_mezzogiorno,pastori,pescatori_case_basse}/scheda.md  con sezione `## Saluto del gruppo` (DOC_2)
│   ├── luoghi/                       74 schede (per quartiere: aria/acqua/fuoco/terra/centro + perimetro + strade)
│   │   └── 5 schede sentieri Tier A (via_dell_alba, sentiero_orti_torrente_foresta, via_che_sale, sentiero_orti_casa_salvia, viottolo_perimetrale_piazza) con `## Coerenza cross-scena` aggiornata con dettagli stabili da `path_details.paths.<id>` del grafo
│   ├── oggetti/                      14 schede (13 oggetti-simbolo + 1 oggetto_di_scena_ricorrente) — tutte con prompt_grok.md
│   ├── venti/                        3 schede (Taglio/Intreccio/Mulinello)
│   └── visual_signatures/            1 scheda (quando_acqua_trema)
│
├── _visual_pipeline/          ✅ pacchetto operativo (canone, template, esempi, skill)
│   ├── README.md                     entry point pipeline
│   ├── _canone/                      3 doc canone saga (stylesheet, scale, palette)
│   ├── _templates/                   5 template (scheda + prompt grok + descrizione social)
│   ├── _skill/                       PIPELINE.md (flusso 6 fasi) + CHECKLIST.md
│   └── _esempi/                      bartolo, fiamma, forno, grembiule_fiamma (validati)
│
├── cartografia/               ✅ scrittura tecnica
│   ├── geo/island.geojson            104 feature, sistema cartesiano locale
│   ├── geo/viewer/                   viewer Leaflet
│   └── README.md                     architettura cartografica
│
├── catalogo_web/              ✅ output rigenerabile (NON modificare a mano)
│   └── data/entities.json            generato da `scripts/build_catalogo_web.py`
│
├── _porting_grafo/            🗄️  ARCHIVIO una-tantum (fase E completata 2026-04-28)
│   ├── dossier_fase_e/               kit migrazione + MIGRATION_PROMPT + schema v1.2 + INPUT_NODES (12 nodi v1.1)
│   ├── output/s01..s12/              per ogni storia: canonical, provisional, migration_notes, catalog_proposals, _p1_mapping
│   └── scripts/migrate_p1.py         script P1 (carpentiere meccanico)
│
├── _pacchetti_consegnati/     🗄️  ARCHIVIO pacchetti autoriali Ray gia integrati (2026-04-30)
│   ├── README.md                     orchestratore + pattern di integrazione futura
│   └── cornice_mondo/                pacchetto integrato 2026-04-30 (DOC_1..DOC_6 + README dedicato)
│
├── contributi/                ✅ scrittura per collaboratori esterni (proposte/aggiunte)
│   └── (file .md datati, vedi sezione 5)
│
├── _starter_kit/              ✅ template di sistema riusabile (scheletro, NO contenuto saga)
│   └── README.md                     entry point (setup nuova "isola" da zero)
│
├── scripts/                   ✅ tool Python condivisi (idempotenti)
│   ├── build_catalogo_web.py            rigenera catalogo_web/data/entities.json da visual/
│   ├── build_visual_skeleton.py         ricrea schede stub da grafo (non usare in fase F)
│   ├── compile_visual_from_graph.py     travaso meccanico grafo → schede (fase F.1)
│   ├── split_narrazione_fattuale.py     split sorgente Ciclo*.txt → 12 sNN_*.md
│   ├── migrate_graph_v1_2_to_v1_3.py    bump schema fase G (one-shot, idempotente)
│   ├── promote_visual_entities_to_graph.py  promozione catalogo visual → grafo entities
│   ├── write_hooks_to_graph.py          writer deterministico fase G (input YAML hooks_proposals/)
│   ├── build_writing_brief.py           ⭐ NEW (2026-04-30) generatore zero-token brief writing per agente prosa
│   ├── build_volume.py                  ⭐ NEW (2026-06-08, v2) compositore libro stampa KDP (A5 300 DPI bleed) — output PDF in _output/
│   ├── design_system.py                 ⭐ NEW (2026-06-08) identita visiva collana (palette tre venti + 6 quartieri, font, ornamenti, glifi, cornici, camuni)
│   ├── cornice_mondo/                   ⭐ NEW (2026-04-30) pacchetto 7 step "cornice del mondo"
│   │   ├── step1_world_conventions.py   crea nodo radice world_conventions + extends quote_tracker
│   │   ├── step4_cornici.py             scrive 24 cornice_dettagli + 8 formule + 2 cantilene
│   │   ├── step5_sentieri_fantasma.py   appende 36 sentieri a locations_secondary
│   │   ├── step6_path_details.py        popola path_details.paths con 5 sentieri Tier A
│   │   ├── step8_fix_canonical_refs.py  ⭐ NEW (2026-06-10) uniforma 7 ref ad id canonici (foresta, pontile, villaggio, who.refs)
│   │   ├── _data/                       4 YAML deterministici (refrain, cornici_24, sentieri_fantasma, path_details_tierA)
│   │   └── _audit/                      riservata audit successivi
│   └── audit/                           ⭐ NEW (2026-06-09) audit grafo+prosa IMPLEMENTATI (4 script + runner + manifest backup + baseline known_issues). `python3 scripts/audit/run_all_audits.py`
│
├── assets/                    ⭐ NEW (2026-06-08) asset condivisi per build (font collana)
│   └── fonts/                        7 TTF OFL: Fraunces, Nunito, Fredoka, Lora — usati da build_volume.py + design_system.py
│
├── tests/                     ⭐ NEW (2026-06-08) suite test impaginazione (60 test, ~4s)
│   ├── test_build_volume.py          struttura/robustezza/decori/coerenza 4 volumi/determinismo
│   ├── test_integration.py           build PDF reale + invarianti KDP (slow, ~60s)
│   └── README.md                     come eseguire i test
│
├── pytest.ini                 ⭐ NEW (2026-06-08) config pytest (marker `slow` per integration)
│
├── skills/                    ✅ skill agente IA
│   ├── README.md                     orchestratore
│   ├── cartografo.md                 manutenzione cartografia
│   ├── brieffer/                     genera writing_briefs autosufficienti (2026-04-30)
│   │   └── SKILL.md
│   ├── prosa/                        ⭐ NEW (2026-04-30) agente prosa: scrive il testo finale delle storie
│   │   └── SKILL.md                  da incollare in chat Claude.ai per attivare modalita scrittura
│   ├── illustratore/                 ⭐ NEW (2026-05-19) agente illustratore: workflow upload HD per stampa
│   │   └── SKILL.md                  pattern branch + naming + commit per immagini HD pronte al merge
│   └── visual/
│       ├── README.md                 skill visual generale
│       └── compilatore.md            sotto-skill compilazione schede
│
├── README.md                  panoramica generale
├── PROJECT_STATE.md           snapshot operativo
├── SYNC_LOG.md                log cambiamenti cross-skill
└── CLAUDE.md                  questo file
```

---

## 2. Regole di non-danno (LEGGI PRIMA DI MODIFICARE)

### NEVER

- ❌ **Mai modificare `pipeline_narrativa/` senza autorizzazione esplicita di Ray.** Né il grafo, né la Bible, né i documenti narrativi. Se rilevi un'incoerenza, **segnalala**, non risolverla in autonomia.
- ❌ **Mai modificare `_porting_grafo/`.** È un archivio chiuso. La fase E è completata. Se serve rifare la migrazione, parla con Ray.
- ❌ **Mai modificare `_pacchetti_consegnati/`.** È un archivio dei pacchetti autoriali Ray già integrati (trail di audit). I documenti sono fonte autorevole storica e si consultano in lettura. Se Ray consegna un nuovo pacchetto, l'integrazione fa parte del lavoro normale; al termine, i documenti del pacchetto vanno archiviati qui (e non più toccati).
- ❌ **Mai inventare contenuto narrativo.** Niente descrizioni di scene, palette, personaggi, vincoli che non sono nelle fonti (grafo, Bible, character_constraints, canonical, schede esistenti).
- ❌ **Mai modificare schede in `visual/` aggiungendo info NON presenti nelle fonti.** È accettabile riformulare per chiarezza, ma il contenuto semantico deve essere tracciabile a fonte.
- ❌ **Mai eliminare o sovrascrivere lavoro precedente** senza prima leggerlo e capire perché c'era.
- ❌ **Mai `git push --force`, mai `git reset --hard`, mai `git checkout -- <file>` su file modificati senza chiedere.**
- ❌ **Mai committare con `--no-verify` o `--amend` su commit altrui.**
- ❌ **Mai sostituire il `story_graph.json` corrente.** Se serve una nuova migrazione, segui un processo come fase E (workspace separato + audit trail).
- ❌ **Mai contaminare `_starter_kit/` con contenuto specifico de "L'Isola dei Tre Venti".** Niente prosa della saga, niente schede di personaggi/luoghi/oggetti reali, niente prompt grok del canone, niente snippet del grafo, niente immagini canoniche. Lo starter kit deve restare **scheletro generico riusabile** (template vuoti, script idempotenti, skill agente IA, README di setup). Se devi mostrare un esempio, usa nomi placeholder (`<personaggio_esempio>`, `<luogo_esempio>`, ecc.).
- ❌ **Mai lavorare in `_starter_kit/` e fuori contemporaneamente.** Una sessione = uno scope. Se sei in modalità starter kit, non modificare `pipeline_narrativa/`, `visual/`, `cartografia/`, `catalogo_web/`. Se sei in modalità saga, non modificare `_starter_kit/`.

### ALWAYS

- ✅ **Sempre verifica lo stato corrente prima di agire**: `git status`, `cat README.md`, `cat PROJECT_STATE.md`.
- ✅ **Sempre commit con messaggio descrittivo** che spiega COSA + PERCHÉ.
- ✅ **Sempre push su branch dedicato + merge fast-forward su main** (vedi sezione 6).
- ✅ **Sempre rigenera `catalogo_web/data/entities.json` con `python3 scripts/build_catalogo_web.py`** dopo aver modificato `visual/`.
- ✅ **Sempre verifica il grafo** se modifichi qualcosa che lo tocca: `python3 -c "import json; json.load(open('pipeline_narrativa/story_graph.json'))"` (non deve dare errori).
- ✅ **Sempre preserva `_da popolare dal grafo_`** come marker di sezione vuota nelle schede. Sostituisci solo se hai un dato concreto da metterci.

---

## 3. Stato corrente del progetto (cosa è già stato fatto)

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

## 5. Regole per collaboratori esterni che aggiungono dettagli alle schede

Caso d'uso: una persona vuole proporre aggiunte/dettagli alle schede di `visual/` ma **NON** ha autorizzazione a modificare direttamente file esistenti né a toccare grafo/Bible.

### Cosa può fare

✅ **Leggere tutto** il repo (visual, cartografia, pipeline_narrativa, catalogo_web).

✅ **Creare file nuovi datati in `contributi/`** — UN file per sessione di lavoro. Pattern del nome:
```
contributi/<YYYY-MM-DD>_<nome_collaboratore>_<scope>.md
```
Esempi:
- `contributi/2026-05-03_anna_aggiunte_schede_personaggi.md`
- `contributi/2026-05-10_anna_proposte_oggetti.md`

✅ **Dentro il file** scrive in markdown libero le sue proposte. Schema consigliato:

```markdown
# Aggiunte schede — <NOME> — <DATA>

## Per scheda: visual/personaggi/individuali/primari/grunto/scheda.md
### Sezione: Espressione / comportamento

**Aggiunta proposta:**
> [Testo che la persona vorrebbe aggiungere]

**Fonte/motivazione:**
- [Da Bible §X.Y, oppure: "ricordo di chat con Ray del DD/MM", oppure: "intuizione da revisione del catalogo + grafo"]

---

## Per scheda: visual/luoghi/quartiere_aria/burrone/scheda.md
### Sezione: Variabilità ammessa

[etc...]
```

### Cosa NON può fare

❌ **Mai modificare schede esistenti in `visual/`.** Solo creare nuovi file in `contributi/`.

❌ **Mai modificare `pipeline_narrativa/`** (grafo + Bible).

❌ **Mai modificare `_porting_grafo/`** (archivio chiuso).

❌ **Mai modificare `cartografia/`** (compito di altro agente).

❌ **Mai modificare `catalogo_web/`** (rigenerato automaticamente).

❌ **Mai modificare `scripts/`, `skills/`, `README.md`, `CLAUDE.md`, `PROJECT_STATE.md`, `SYNC_LOG.md`.**

❌ **Mai creare branch nuovi.** Lavora su `main` (o sul branch attivo se Ray glielo dice). Solo crea il file, fa commit, push.

❌ **Mai eseguire script.** Lascia il run a chi gestisce il merge.

### Workflow per il collaboratore

1. `git pull origin main` per allinearsi.
2. Crea il file `contributi/<data>_<nome>_<scope>.md`.
3. Scrive le sue proposte in markdown.
4. `git add contributi/<file>.md`
5. `git commit -m "contributi: <nome> aggiunte schede <scope>"`
6. `git push origin main`
7. Apre eventualmente una issue / messaggio a Ray per dire "ho proposto X".

### Cosa succede dopo

Ray (o un agente IA in modalità "integratore") legge il file, valuta le proposte, integra quelle approvate nelle schede `visual/` con commit dedicati. Il file `contributi/<data>_<nome>_<scope>.md` resta nel repo come trail di audit (chi ha proposto cosa, quando, perché).

---

## 6. Convenzioni Git

- **Branch principale**: `main`. Per lavori grandi: branch dedicato `claude/<scope>` con merge fast-forward su main.
- **Commit message**: prima riga ≤72 char descrittiva, poi corpo che spiega **perché** + **cosa** + eventuali link/riferimenti.
  ```
  fase F.1: travaso meccanico grafo → schede visual

  Compilatore idempotente in scripts/compile_visual_from_graph.py.
  Per ogni scheda con marker '_da popolare dal grafo_', popola sezioni
  con SOLO dati esistenti nel grafo. NO inferenza, NO invenzione.
  ...
  ```
- **Push protocol**: `git push -u origin <branch>`. Se network error, retry 4 volte con backoff (2s, 4s, 8s, 16s).
- **Mai `--force`, mai `--no-verify`, mai amend di commit altrui.**
- **Mai pre-commit hooks bypassati**: se un hook fallisce, capisci perché e fixa.

---

## 7. Quick reference — comandi tipici

```bash
# Check stato
git status
git log --oneline main -10

# Rigenera catalogo dopo modifiche visual/
python3 scripts/build_catalogo_web.py

# Travaso grafo → schede (fase F.1, idempotente)
python3 scripts/compile_visual_from_graph.py

# Verifica grafo (deve essere JSON valido schema 1.4, graph 1.2.0 post-cornice del mondo)
python3 -c "import json; g=json.load(open('pipeline_narrativa/story_graph.json')); print('schema:', g['schema_version'], 'graph:', g['graph_version'], 'stories:', len(g['stories']), 'world_conventions keys:', sorted(g.get('world_conventions', {}).keys()))"

# Fase G — workflow hook visivi (gia completata)
python3 scripts/migrate_graph_v1_2_to_v1_3.py            # bump schema (one-shot, idempotente)
python3 scripts/promote_visual_entities_to_graph.py      # promuove entita' catalogo->grafo
python3 scripts/write_hooks_to_graph.py --story s01 --dry-run    # validazione
python3 scripts/write_hooks_to_graph.py --story s01              # scrittura
python3 scripts/write_hooks_to_graph.py --cycle A                # batch ciclo

# Fase Cornice del Mondo — completata 2026-04-30 (rilanciabile per idempotenza)
python3 scripts/cornice_mondo/step1_world_conventions.py        # dry-run
python3 scripts/cornice_mondo/step1_world_conventions.py --apply
python3 scripts/cornice_mondo/step4_cornici.py --apply
python3 scripts/cornice_mondo/step5_sentieri_fantasma.py --apply
python3 scripts/cornice_mondo/step6_path_details.py --apply

# Brieffer — generazione writing briefs (zero token, idempotente)
python3 scripts/build_writing_brief.py --story s01    # un brief
python3 scripts/build_writing_brief.py --all          # tutti i 12 brief

# Compositore libro (KDP, A5 300 DPI bleed) — output in _output/
pip install Pillow reportlab --break-system-packages
python3 scripts/build_volume.py --volume 1 --storie s01      # singola storia
python3 scripts/build_volume.py --volume 1                    # tutto il volume
python3 scripts/build_volume.py --volume 1 --presentazione dopo   # presentazione personaggi DOPO la storia

# Test suite impaginazione
pip install pytest pymupdf --break-system-packages
python3 -m pytest tests/ -v -m "not slow"     # veloci (~4s)
python3 -m pytest tests/ -v                    # tutto inclusa integrazione (~60s)

# Avvia catalogo web in locale
python3 -m http.server  # poi browser → http://localhost:8000/catalogo_web/

# Apri viewer cartografia (no server, doppio click)
# cartografia/geo/viewer/index.html
```

---

## 9. Standard immagini HD per stampa (Fase Illustratore — 2026-05-19)

Le immagini per **stampa del libro** convivono con i reference digitali low-res in una struttura **`_hd/`** dedicata, per non sostituire i low-res e mantenere ortogonalità (browsing veloce vs file pesanti).

### Convivenza low-res + HD

```
<cartella canonica>/<id>.jpg          ← LOW-RES reference digitale (browsing, catalogo web)
<cartella canonica>/_hd/<id>_hd.jpg   ← HD per stampa (JPG q95, ≥1664×2496 px)
```

I marker `@image` nei file `.md` puntano SEMPRE al low-res. Lo script compositore libro (futuro) cerca prima `_hd/<id>_hd.jpg`, fallback su low-res.

### I 3 contesti di destinazione

| Contesto | Path HD |
|---|---|
| **Hook di storia** | `pipeline_narrativa/storie_finali/_scene/sNN/_hd/sNN_hMMx_hd.jpg` |
| **Intro volume** | `pipeline_narrativa/storie_finali/_volumi/v0N/_hd/v0N_intro_<slug>_hd.jpg` |
| **Catalogo reference canoniche** | `visual/<categoria>/<id>/immagini/_hd/<id>_canonica_v1_<vista>_hd.jpg` |

### Specifiche file HD (obbligatorie)

- **Formato:** JPEG (estensione `.jpg`), qualità 95
- **Profilo colore:** RGB sRGB (la conversione CMYK è dello stampatore)
- **Risoluzione minima:** 1664×2496 px verticale (ideale 2000×3000 px)
- **Peso file:** 300-700 KB tipico, fino a ~1 MB
- **Naming:** lowercase, snake_case, suffisso obbligatorio `_hd`, mai `.jpeg`/`.JPG`/spazi/maiuscole

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

---

## 10. Quando in dubbio

1. Leggi `README.md` per la panoramica.
2. Leggi `PROJECT_STATE.md` per stato operativo.
3. Cerca skill specifica in `skills/`.
4. Se ancora non chiaro: **chiedi a Ray prima di agire**. Meglio una domanda in più che un commit da rollback.

---

**Autore narrativo e proprietario**: Ray.
**Manutenzione tecnica**: Ray + agenti IA in collaborazione (Claude Sonnet/Opus tipicamente).
**Ultimo aggiornamento istruzioni**: 2026-06-08 (script definitivo impaginazione volumi KDP installato — `scripts/build_volume.py` v2, `scripts/design_system.py`, `assets/fonts/`, `tests/`).
