# isola_i3v_visual — Cartografia e Visual

Repository di lavoro per il progetto **L'Isola dei Tre Venti** (saga di 12 storie illustrate per bambini 4-10 anni, di Ray).

> 🔎 **Visualizzatore catalogo entità (uso interno):** [`catalogo_web/`](./catalogo_web/) — sito statico che mostra tutte le 115 entità della saga (personaggi, luoghi, oggetti, venti, signatures) con sidebar navigabile e gallery immagini. Una volta abilitate le GitHub Pages: `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`. In locale: `python3 -m http.server` dalla radice → `http://localhost:8000/catalogo_web/`.
>
> 🗺 **Viewer cartografia (mappa interattiva):** [`cartografia/geo/viewer/index.html`](./cartografia/geo/viewer/index.html) — apri con doppio click. 104 feature, ricerca, filtri, pannello dettaglio.
>
> 🔁 **Pipeline operativa (flusso end-to-end per una storia):** [`docs/PIPELINE.md`](./docs/PIPELINE.md) — diagramma + tabella delle 7 tappe (idea autoriale → narrazione fattuale → 10 hook → grafo → audit → prosa → commit). Fissa cosa è automatizzabile e cosa resta umano (~70% auto, by design). Stato attuale: la repo è strutturata ma il flusso non è ancora automatizzato end-to-end — il documento mappa cosa serve per scalare quando le 12 storie saranno completate.

Questo repo contiene **due tracce di lavoro** + un input read-only + un workspace di porting completato:

```
/
├── cartografia/           tecnica: GeoJSON, schede luogo, viewer, convenzioni
├── visual/                descrizioni visive di tutte le entità (personaggi, luoghi, oggetti, venti, signatures) + immagini canoniche
├── _visual_pipeline/      pipeline operativa per completare il catalogo visual (canone, template, esempi, skill)
├── catalogo_web/          sito statico interno per consultare visual/ da browser (GitHub Pages)
├── pipeline_narrativa/    INPUT read-only: grafo storie + corpus canonico narrativo
│   ├── documenti_progetto/         Bible, Carta Voce, ARCHI, Glossario, Pattern AI da bandire, ecc.
│   ├── narrazione_fattuale/        12 narrazioni fattuali s01..s12 (input fase G, Ray)
│   ├── hooks_proposals/            input deterministici fase G (YAML per ciclo/storia)
│   ├── prompts/                    prompt operativi versionati per agenti (es. fase G)
│   ├── story_graph.json            grafo v1.1.0 schema 1.3 (fase G completata: 120/120 hook)
│   └── story_graph.v0.10.0.backup.json  backup pre-fase E
├── _porting_grafo/        ARCHIVIO una-tantum: workspace migrazione grafo v1.1 → v1.2 (fase E completata)
├── contributi/            proposte aggiunte schede da collaboratori esterni (file datati, mai modifica diretta)
├── skills/                skill dell'agente IA (cartografo, visual con sotto-skill) + regole comuni
├── scripts/               tool Python condivisi (idempotenti) tra le skill
│   ├── build_catalogo_web.py            rigenera catalogo_web da visual/
│   ├── compile_visual_from_graph.py     travaso meccanico grafo → schede (fase F.1)
│   ├── split_narrazione_fattuale.py     split sorgente Ciclo*.txt → 12 sNN_*.md
│   ├── migrate_graph_v1_2_to_v1_3.py    bump schema fase G (one-shot, idempotente)
│   ├── promote_visual_entities_to_graph.py  promozione catalogo visual → grafo entities
│   ├── write_hooks_to_graph.py          writer deterministico fase G (input YAML)
│   └── audit/                           audit grafo (4 script da implementare)
├── docs/                  documentazione di processo (es. PIPELINE.md)
├── CLAUDE.md              istruzioni per istanze IA (LEGGI PRIMA DI MODIFICARE)
├── PROJECT_STATE.md       snapshot operativo
└── SYNC_LOG.md            log dei cambiamenti da riflettere altrove
```

---

## 1. Cartografia

Cartografia tecnica canonica dell'Isola. Alimenta la pipeline immagini con coerenza geografica e valida le storie nuove rispetto al canone fisico.

- **Stato:** v0.5 — 103 feature, 36 sentieri, viewer Leaflet, backward-compat 100% con grafo v0.6.0.
- **Punto d'ingresso umano:** `cartografia/geo/viewer/index.html` (doppio click).
- **Architettura e regole:** `cartografia/README.md`.
- **Storia versioni:** `cartografia/CHANGELOG.md`.

## 2. Visual

Serbatoio di **descrizioni visive e vincoli per prompt** per tutte le entità della saga (personaggi, luoghi, oggetti, venti, visual signatures). Fonte unica per IA generative, illustrazioni di riferimento, stampa 3D (4 vedute), narrativa, campagne social.

- **Stato:** 115 schede in struttura frattale (23 personaggi + 43 luoghi + 31 strade + 14 oggetti + 3 venti + 1 visual signature). 11 schede già canonizzate via `_visual_pipeline/` (Fiamma, Bartolo, Forno + 7 luoghi + grembiule_fiamma + Gabriel parziale). 8 immagini canoniche generate (4 Fiamma + 4 Bartolo). Le restanti schede da completare seguendo la pipeline.
- **Esempi validati:** `visual/personaggi/individuali/primari/{fiamma,bartolo}/` (con immagini canoniche v1) e `visual/luoghi/quartiere_fuoco/forno/` (luogo complesso 3 blocchi LOCATION).

## 3. Visual pipeline (`_visual_pipeline/`)

Pacchetto operativo per **completare il catalogo visual** (le 115 schede) con canone chiuso e immagini canoniche generate, in modo coerente, scalabile e riproducibile. Sviluppata da Ray in chat dedicata, validata su 2 specie diversissime (Fiamma + Bartolo) e 1 luogo complesso (Forno).

- **Entry point:** [`_visual_pipeline/README.md`](./_visual_pipeline/README.md)
- **Flusso 6 fasi:** [`_visual_pipeline/_skill/PIPELINE.md`](./_visual_pipeline/_skill/PIPELINE.md) (Setup → scheda → prompt Grok → descrizione social → immagini → push → canone)
- **Canone saga (3 doc):** stylesheet, scale (Gabriel = 1.0 GU), palette per quartiere e personaggio
- **Template (5):** scheda personaggio/oggetto/luogo + prompt grok + descrizione social
- **Esempi validati:** `_visual_pipeline/_esempi/{fiamma,bartolo,forno,grembiule_fiamma}/`
- **Versione:** v1.2 (2026-04-29). Pipeline personaggi e pipeline luoghi entrambe considerate robuste.

## 4. Catalogo web (sito interno)

Sito statico HTML+JS in [`catalogo_web/`](./catalogo_web/) per **consultare le entità di `visual/` da browser**. Ad uso interno (Ray + collaboratori senza accesso GitHub).

- **Stack:** HTML + CSS + JS vanilla, no build pipeline. `marked.js` da CDN per rendering MD.
- **Aggiornamento:** `python3 scripts/build_catalogo_web.py` rilegge `visual/` e rigenera `catalogo_web/data/entities.json`. Idempotente.
- **Locale:** `python3 -m http.server` dalla radice → `http://localhost:8000/catalogo_web/`.
- **Deploy:** GitHub Pages (Settings → Pages → Source: main / `/`) → URL `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`.

## 5. Pipeline narrativa (read-only per cartografia/visual; modificabile solo da agente di fase dedicato)

Corpus narrativo canonico — Bible, Glossario, ARCHI 12 storie, voce, pattern AI da bandire, EAR, apparato — più il grafo storie aggiornato.

- **Grafo corrente:** `pipeline_narrativa/story_graph.json` **v1.1.0-pre schema 1.3** (S1-S12, fase E completata + schema bump fase G eseguito). Promuove a v1.1.0 stabile alla prima scrittura di hook `extended_v2`. Backup pre-bump: `story_graph.json.pre_v1_3.backup.json`.
- **Documenti progetto:** `pipeline_narrativa/documenti_progetto/` (Bible, Carta Voce, ARCHI, Glossario, Pattern AI da bandire, ecc.).
- **Narrazione fattuale:** `pipeline_narrativa/narrazione_fattuale/` — 12 file `s01_*.md` ... `s12_*.md` con cronaca fattuale di ogni storia (input fase G, **completi al 2026-04-29**, derivati meccanicamente dal sorgente unico in `_source/Ciclo_a-b-c-d_*.txt` via `scripts/split_narrazione_fattuale.py`).
- **Prompt operativi:** `pipeline_narrativa/prompts/` — prompt versionati per agenti dedicati (es. `PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md`).
- **Backup pre-migrazione:** `pipeline_narrativa/story_graph.v0.10.0.backup.json` (snapshot v0.10.0 schema 0.1).
- **Regola:** mai modificato dalla cartografia o dal visual. Solo agenti di fase dedicati (con prompt specifico) toccano il grafo, e solo le sezioni autorizzate dal prompt.

## 6. Fase G — Estensione hook visivi (completata)

Ampliamento dei `visual_anchors.scene_hooks` di ogni storia da N (2–8 attuali) a esattamente **10**. Bump grafo v1.0.0 → v1.1.0 + schema v1.2 → v1.3 (estensione additiva). **Completata il 2026-04-29: 120/120 hook v1.3 scritti.**

- **Prompt operativo:** `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md`.
- **Input principale:** `pipeline_narrativa/narrazione_fattuale/s0X_*.md` (12/12).
- **Tooling:** `scripts/migrate_graph_v1_2_to_v1_3.py`, `scripts/promote_visual_entities_to_graph.py`, `scripts/write_hooks_to_graph.py` (writer deterministico con 16 controlli pre-scrittura).
- **Workflow validato:** agente sub legge fonti → propone in markdown → review Ray → conversione YAML in `pipeline_narrativa/hooks_proposals/<ciclo>/sNN.yaml` → dry-run → write → commit + merge main. Storia per storia.
- **Output finale:** 120 hook validati totali (10 × 12). 31 signature (max 3/storia).

Vedi `CLAUDE.md` sezione "Fase G" per dettagli.

## 7. Porting grafo (archivio una-tantum, non pipeline)

`_porting_grafo/` contiene il workspace della **fase E**: migrazione del story_graph dalla schema v1.1 (legacy) alla schema canonica v1.2. Lavoro **una-tantum**, completato il 2026-04-28. Non entra nella pipeline operativa, ma resta nel repo come trail di audit.

Cosa c'è dentro:

```
_porting_grafo/
├── dossier_fase_e/
│   └── dossier/
│       ├── MIGRATION_PROMPT_FASE_E.md     prompt operativo (11 regole + REGOLA 7), usato dall'agente migrante
│       ├── story_graph_schema_canonical_v1_2.json   schema target
│       ├── INPUT_NODES/                   12 nodi v1.1 in input (s01_input.json…)
│       ├── _provisional_state.json        rolling state P2 (12 entries finali)
│       ├── _canon_misalignments.json      8 misalignments tracciati (tutti resolved)
│       └── verify_output_integrity.py     validatore schema v1.2
├── output/
│   └── s01..s12/                          per ogni storia: canonical, provisional, migration_notes, catalog_proposals, _p1_mapping
└── scripts/
    └── migrate_p1.py                      script P1 (carpentiere meccanico) parametrico per story_id
```

Stato finale fase E:
- 12/12 canonical PASS verify schema v1.2
- 60 no_inference_fields decisi via Q1-Q6 autoriali Ray (entry_point/closure/register/length/pauses)
- 87 provvisori P2 (22A + 47B + 18C)
- 8/8 misalignments resolved
- Catalogo isola_i3v_visual: 114 → **115 entities** (aggiunto `pallone_di_stoffa_cucita` come `oggetto_di_scena_ricorrente`)

L'output canonico finale è promosso in `pipeline_narrativa/story_graph.json` v1.0.0 schema 1.2. Il workspace `_porting_grafo/` resta come riferimento (mapping, trasformazioni applicate, regole patchate, decisioni archiviate).

---

## 8. Istruzioni per agenti IA

Vedi `skills/README.md` (orchestratore) e le skill specifiche:
- [`skills/cartografo.md`](./skills/cartografo.md) — manutenzione cartografia.
- [`skills/visual/`](./skills/visual/) — famiglia visual: [`README.md`](./skills/visual/README.md) (skill generale) + sotto-skill specializzate (es. [`compilatore.md`](./skills/visual/compilatore.md) per la compilazione delle schede entità).

In sintesi: l'agente sceglie una skill per task, scrive solo nel proprio scope (`cartografia/` o `visual/`), non tocca mai `pipeline_narrativa/` (eccezione: la migrazione una-tantum di `_porting_grafo/`, ora chiusa), non decide canone narrativo, segnala invece di reinterpretare.

## 9. Stato e contesto

- **Snapshot operativo:** `PROJECT_STATE.md`.
- **Autore narrativo e proprietario:** Ray.
- **Manutenzione tecnica:** Ray + agente IA in collaborazione.

---

**Ultimo aggiornamento:** 2026-04-29
**Versione cartografia:** v0.6.2
**Versione grafo storie:** v1.1.0 schema 1.3 (fase E + fase G completate; 120/120 hook scritti)
**Versione visual pipeline:** v1.2 (Fiamma + Bartolo + Forno validati come standard; 8 immagini canoniche)
**Catalogo entità:** 115 (23 personaggi + 43 luoghi + 31 strade + 14 oggetti + 3 venti + 1 visual signature)
