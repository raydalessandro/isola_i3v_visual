# isola_i3v_visual — Cartografia e Visual

Repository di lavoro per il progetto **L'Isola dei Tre Venti** (saga di 12 storie illustrate per bambini 4-10 anni, di Ray).

> 🔎 **Visualizzatore catalogo entità (uso interno):** [`catalogo_web/`](./catalogo_web/) — sito statico che mostra tutte le 115 entità della saga (personaggi, luoghi, oggetti, venti, signatures) con sidebar navigabile e gallery immagini. Una volta abilitate le GitHub Pages: `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`. In locale: `python3 -m http.server` dalla radice → `http://localhost:8000/catalogo_web/`.
>
> 🗺 **Viewer cartografia (mappa interattiva):** [`cartografia/geo/viewer/index.html`](./cartografia/geo/viewer/index.html) — apri con doppio click. 104 feature, ricerca, filtri, pannello dettaglio.

Questo repo contiene **due tracce di lavoro** + un input read-only + un workspace di porting completato:

```
/
├── cartografia/           tecnica: GeoJSON, schede luogo, viewer, convenzioni
├── visual/                descrizioni visive di tutte le entità (personaggi, luoghi, oggetti, venti, signatures)
├── catalogo_web/          sito statico interno per consultare visual/ da browser (GitHub Pages)
├── pipeline_narrativa/    INPUT read-only: grafo storie + corpus canonico narrativo
├── _porting_grafo/        ARCHIVIO una-tantum: workspace migrazione grafo v1.1 → v1.2 (fase E completata)
├── skills/                skill dell'agente IA (cartografo, visual con sotto-skill) + regole comuni
├── scripts/               tool Python condivisi (idempotenti) tra le skill
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

- **Stato:** 115 schede in struttura frattale (23 personaggi + 43 luoghi + 31 strade + 14 oggetti + 3 venti + 1 visual signature). Body di ciascuna scheda da compilare via metodo `compilatore` (vedi [`skills/visual/compilatore.md`](./skills/visual/compilatore.md)). Esempio compilato: `visual/personaggi/individuali/cuccioli/liu/scheda.md`.

## 3. Catalogo web (sito interno)

Sito statico HTML+JS in [`catalogo_web/`](./catalogo_web/) per **consultare le entità di `visual/` da browser**. Ad uso interno (Ray + collaboratori senza accesso GitHub).

- **Stack:** HTML + CSS + JS vanilla, no build pipeline. `marked.js` da CDN per rendering MD.
- **Aggiornamento:** `python3 scripts/build_catalogo_web.py` rilegge `visual/` e rigenera `catalogo_web/data/entities.json`. Idempotente.
- **Locale:** `python3 -m http.server` dalla radice → `http://localhost:8000/catalogo_web/`.
- **Deploy:** GitHub Pages (Settings → Pages → Source: main / `/`) → URL `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`.

## 4. Pipeline narrativa (read-only)

Corpus narrativo canonico — Bible, Glossario, ARCHI 12 storie, voce, pattern AI da bandire, EAR, apparato — più il grafo storie aggiornato.

- **Grafo corrente:** `pipeline_narrativa/story_graph.json` **v1.0.0 schema 1.2** (S1-S12, fase E completata).
- **Backup pre-migrazione:** `pipeline_narrativa/story_graph.v0.10.0.backup.json` (snapshot v0.10.0 schema 0.1, conservato come trail di audit).
- **Regola:** mai modificato dalla cartografia o dal visual. Se si rilevano incoerenze, **si segnalano**, non si risolvono in autonomia.

## 5. Porting grafo (archivio una-tantum, non pipeline)

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

## 6. Istruzioni per agenti IA

Vedi `skills/README.md` (orchestratore) e le skill specifiche:
- [`skills/cartografo.md`](./skills/cartografo.md) — manutenzione cartografia.
- [`skills/visual/`](./skills/visual/) — famiglia visual: [`README.md`](./skills/visual/README.md) (skill generale) + sotto-skill specializzate (es. [`compilatore.md`](./skills/visual/compilatore.md) per la compilazione delle schede entità).

In sintesi: l'agente sceglie una skill per task, scrive solo nel proprio scope (`cartografia/` o `visual/`), non tocca mai `pipeline_narrativa/` (eccezione: la migrazione una-tantum di `_porting_grafo/`, ora chiusa), non decide canone narrativo, segnala invece di reinterpretare.

## 7. Stato e contesto

- **Snapshot operativo:** `PROJECT_STATE.md`.
- **Autore narrativo e proprietario:** Ray.
- **Manutenzione tecnica:** Ray + agente IA in collaborazione.

---

**Ultimo aggiornamento:** 2026-04-28
**Versione cartografia:** v0.6.1
**Versione grafo storie:** v1.0.0 schema 1.2 (fase E completata)
**Catalogo entità:** 115 (23 personaggi + 43 luoghi + 31 strade + 14 oggetti + 3 venti + 1 visual signature)
