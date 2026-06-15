# L'Isola dei Tre Venti — repo `isola_i3v_visual`

Saga di **12 storie illustrate per bambini 4-10**, autore: **Ray**.

Questo repository unifica:
- **`pipeline_narrativa/`** — canone narrativo (grafo storie + Bible + writing briefs). **Read-only di default**, modificabile solo con autorizzazione esplicita di Ray.
- **`visual/`** — descrizioni canoniche (schede + prompt grok + immagini) di personaggi, luoghi, oggetti, venti.
- **`cartografia/`** — mappa tecnica dell'isola (`geo/island.geojson` + viewer Leaflet).
- **`catalogo_web/`** — sito statico interno per consultazione di tutte le entità (auto-pubblicato su GitHub Pages).
- **`scripts/`** — tooling Python condiviso (idempotente, dry-run di default per script che toccano il grafo).
- **`skills/`** — istruzioni operative per agenti IA per ogni modalità di lavoro.

> **Punto di ingresso obbligatorio per agenti IA:** [`CLAUDE.md`](./CLAUDE.md). Spiega chi può modificare cosa, come, e in che ordine.

---

## Stato del progetto (2026-04-30)

### Canone fissato

| Tappa | Stato | Output |
|---|---|---|
| Fase E — migrazione grafo schema legacy → v1.2 | ✅ completata 2026-04-28 | grafo canonico, 12 storie + 115 entità |
| Fase F.1 — travaso meccanico grafo → schede visual | ✅ completata 2026-04-28 | 56 sezioni stub popolate |
| Fase G — hook visivi estesi a 10/storia | ✅ completata 2026-04-29 | 120 hook v1.3, schema 1.3, 31 signature totali |
| Fase F.2 — visual prompt grok | 🔄 in corso (28/115 al 2026-04-30) | 14 personaggi + 14 oggetti |
| Fase Cornice del Mondo — 7 step | ✅ completata 2026-04-30 | grafo v1.2.0 schema 1.4 |
| Fase Brieffer — generatore brief writing | ✅ completata 2026-04-30 | 12 brief autosufficienti |

### Stato grafo

```
schema_version: 1.4
graph_version:  1.2.0
stories:        12
entities:       116 (catalogo visual: 115 → 116 con +pescatori_case_basse 6° gruppo)
hook visivi:    120 (10 × 12 storie)
cornici:        24 (2 × 12 storie)
sentieri Tier A: 5 con 20 dettagli stabili
formule ritornello applicate: 8 (5 SG + 2 PL + 1 doppia s11) — 11 animali distinti unici saga
```

### Backup chain `pipeline_narrativa/`

```
story_graph.v0.10.0.backup.json              pre-fase E
story_graph.json.pre_v1_3.backup.json        pre-bump schema 1.3
story_graph.json.pre_fase_g.backup.json      pre-hook estesi
story_graph.json.pre_cornice_mondo.backup.json    pre-Step 1+2 (2026-04-30)
story_graph.json.pre_step4_cornici.backup.json    pre-Step 4 (2026-04-30)
story_graph.json.pre_step5_sentieri.backup.json   pre-Step 5 (2026-04-30)
story_graph.json.pre_step6_path_details.backup.json pre-Step 6 (2026-04-30)
```

---

## Workflow per Ray

### Per generare brief writing per una storia

```bash
python3 scripts/build_writing_brief.py --story s01    # un brief
python3 scripts/build_writing_brief.py --all          # tutti i 12 brief
```

I brief vivono in `pipeline_narrativa/writing_briefs/sNN_writing_brief.md`. Sono **autosufficienti**: contengono narrazione fattuale + hook + cornici + sentieri + saluti + formula ritornello + cast + canone visivo + vincoli universali. Token budget per brief: 16k-32k parole.

**Quando rilanciare:** dopo modifiche a grafo, schede catalogo, prompt grok, narrazione fattuale. Idempotente.

### Per generare immagini canoniche con Grok Imagine

I prompt sono pubblicati in:
- `visual/personaggi/individuali/<gruppo>/<id>/prompt_grok.md`
- `visual/oggetti/<id>/prompt_grok.md`

Workflow esterno: estrai prompt da GitHub, genera con Grok Imagine, carica le 4 immagini canoniche in `immagini/<id>_canonica_v1_<vista>.jpg` (+ `<id>_turnaround_v1.jpg`).

### Per consultare il catalogo

- **Sito statico interno:** `python3 -m http.server` → `http://localhost:8000/catalogo_web/`
- **Online (GitHub Pages):** `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`
- **Viewer cartografia:** doppio click su `cartografia/geo/viewer/index.html`

---

## Pipeline operativa per nuova storia

Per il flusso end-to-end dall'idea autoriale di Ray al testo libro committato (7 tappe), vedi **[`docs/PIPELINE.md`](./docs/PIPELINE.md)** — in sintesi:

1. Idea autoriale (Ray, chat)
2. Narrazione fattuale (in `pipeline_narrativa/narrazione_fattuale/`)
3. Estrazione 10 hook visivi (`scripts/write_hooks_to_graph.py`)
4. Review hook (Ray)
5. Audit grafo (`scripts/audit/`)
6. Brief writing (`scripts/build_writing_brief.py`)
7. **Prosa autoriale** — oggi gestita a mano da Ray a partire dal brief

---

## Pubblicazione KDP

Il libro stampato Amazon KDP si compone con due script paralleli:

```bash
python3 scripts/build_volume.py --volume 1   # PDF libro + stampa (A5 + bleed, 300 DPI)
python3 scripts/build_cover.py               # wrap copertina (fronte+dorso+quarta+bleed) in PNG
```

La scheda prodotto Amazon (titolo, sottotitolo, descrizione, keywords KDP,
categorie BISAC) si scrive a mano in [`kdp/listing_volN.md`](./kdp/).

Una skill `pubblicatore` che orchestra il tutto (PDF + copertina + listing
+ checklist KDP) è in fase di progettazione — design doc:
[`docs/DESIGN_SKILL_PUBBLICATORE.md`](./docs/DESIGN_SKILL_PUBBLICATORE.md).

---

## File di stato

| File | Cosa contiene |
|---|---|
| **[`CLAUDE.md`](./CLAUDE.md)** | istruzioni operative complete per agenti IA (regole non-danno, modalità, comandi). Punto di ingresso obbligatorio. |
| [`PROJECT_STATE.md`](./PROJECT_STATE.md) | snapshot operativo cumulativo per sessioni di lavoro |
| [`SYNC_LOG.md`](./SYNC_LOG.md) | log cambiamenti che impattano altre repo del sistema (archivio storico, pipeline immagini esterna) |
| [`docs/PIPELINE.md`](./docs/PIPELINE.md) | flusso end-to-end nuova storia |

## Pacchetti operativi consegnati da Ray

Quando Ray consegna un pacchetto operativo (es. file in zip o documenti in root), l'agente IA esegue gli step di integrazione (script idempotenti + commit puntuali) e poi sposta i documenti in [`_pacchetti_consegnati/<nome_pacchetto>/`](./_pacchetti_consegnati/) come trail di audit autoriale.

Pacchetti integrati:

- **`_pacchetti_consegnati/cornice_mondo/`** (2026-04-30) — formula ritornello, saluti gruppi, 24 cornici, audit sentieri, index sentieri, dettagli stabili Tier A. 7 step integrati nel grafo + catalogo. Vedi [`_pacchetti_consegnati/cornice_mondo/README.md`](./_pacchetti_consegnati/cornice_mondo/README.md).

Per i tooling permanenti correlati (script idempotenti rilanciabili), vedi `scripts/cornice_mondo/`.

---

## Convenzioni Git

- Branch principale: `main`. Per lavori grandi: branch dedicato `claude/<scope>` con merge fast-forward su `main`.
- Commit message: prima riga ≤72 char, poi corpo che spiega COSA + PERCHÉ.
- Push protocol: `git push -u origin <branch>`. Mai `--force`, mai `--no-verify`, mai amend di commit altrui.
- Backup grafo: nome canonico esplicito (`story_graph.json.<tag>.backup.json`).

---

## Contributi esterni

Collaboratori esterni che vogliono proporre dettagli alle schede `visual/` lavorano in `contributi/` (file datati). Vedi `CLAUDE.md` §5 per le regole.

---

## Starter kit (per nuovi progetti tipo-isola)

Chi vuole usare questo framework per realizzare un proprio progetto narrativo (saga, libro illustrato, mondo di fantasia con grafo + canone visivo + cartografia) trova in [`_starter_kit/`](./_starter_kit/) il template scaricabile dello scheletro: struttura cartelle, template di scheda, prompt operativi, script idempotenti, skill agente IA. Punto d'ingresso: [`_starter_kit/README.md`](./_starter_kit/README.md).

> Il **contenuto narrativo specifico** de "L'Isola dei Tre Venti" (`pipeline_narrativa/`, `visual/`, `cartografia/`, `catalogo_web/`) **non fa parte dello starter kit** — è il prodotto autoriale di Ray, non riusabile. Lo starter kit contiene solo lo scheletro generico riusabile.
