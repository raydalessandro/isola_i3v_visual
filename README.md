# isola_i3v_visual — Cartografia e Visual

Repository di lavoro per il progetto **L'Isola dei Tre Venti** (saga di 12 storie illustrate per bambini 4-10 anni, di Ray).

> 🔎 **Visualizzatore catalogo entità (uso interno):** [`catalogo_web/`](./catalogo_web/) — sito statico che mostra tutte le 112 entità della saga (personaggi, luoghi, oggetti, venti, signatures) con sidebar navigabile e gallery immagini. Una volta abilitate le GitHub Pages: `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`. In locale: `python3 -m http.server` dalla radice → `http://localhost:8000/catalogo_web/`.
>
> 🗺 **Viewer cartografia (mappa interattiva):** [`cartografia/geo/viewer/index.html`](./cartografia/geo/viewer/index.html) — apri con doppio click. 104 feature, ricerca, filtri, pannello dettaglio.

Questo repo contiene **due tracce di lavoro** + un input read-only:

```
/
├── cartografia/           tecnica: GeoJSON, schede luogo, viewer, convenzioni
├── visual/                descrizioni visive di tutte le entità (personaggi, luoghi, oggetti, venti, signatures)
├── catalogo_web/          sito statico interno per consultare visual/ da browser (GitHub Pages)
├── pipeline_narrativa/    INPUT read-only: grafo storie + corpus canonico narrativo
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

- **Stato:** 112 schede in struttura frattale (23 personaggi + 41 luoghi + 31 strade + 13 oggetti + 3 venti + 1 visual signature). Body di ciascuna scheda da compilare via metodo `compilatore` (vedi [`skills/visual/compilatore.md`](./skills/visual/compilatore.md)). Esempio compilato: `visual/personaggi/individuali/cuccioli/liu/scheda.md`.

## 3. Catalogo web (sito interno)

Sito statico HTML+JS in [`catalogo_web/`](./catalogo_web/) per **consultare le entità di `visual/` da browser**. Ad uso interno (Ray + collaboratori senza accesso GitHub).

- **Stack:** HTML + CSS + JS vanilla, no build pipeline. `marked.js` da CDN per rendering MD.
- **Aggiornamento:** `python3 scripts/build_catalogo_web.py` rilegge `visual/` e rigenera `catalogo_web/data/entities.json`. Idempotente.
- **Locale:** `python3 -m http.server` dalla radice → `http://localhost:8000/catalogo_web/`.
- **Deploy:** GitHub Pages (Settings → Pages → Source: main / `/`) → URL `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`.

## 4. Pipeline narrativa (read-only)

Corpus narrativo canonico — Bible, Glossario, ARCHI 12 storie, voce, pattern AI da bandire, EAR, apparato — più il grafo storie aggiornato.

- **Grafo corrente:** `pipeline_narrativa/story_graph.json` v0.10.0 (S1-S12).
- **Regola:** mai modificato dalla cartografia o dal visual. Se si rilevano incoerenze, **si segnalano**, non si risolvono in autonomia.

---

## 5. Istruzioni per agenti IA

Vedi `skills/README.md` (orchestratore) e le skill specifiche:
- [`skills/cartografo.md`](./skills/cartografo.md) — manutenzione cartografia.
- [`skills/visual/`](./skills/visual/) — famiglia visual: [`README.md`](./skills/visual/README.md) (skill generale) + sotto-skill specializzate (es. [`compilatore.md`](./skills/visual/compilatore.md) per la compilazione delle schede entità).

In sintesi: l'agente sceglie una skill per task, scrive solo nel proprio scope (`cartografia/` o `visual/`), non tocca mai `pipeline_narrativa/`, non decide canone narrativo, segnala invece di reinterpretare.

## 6. Stato e contesto

- **Snapshot operativo:** `PROJECT_STATE.md`.
- **Autore narrativo e proprietario:** Ray.
- **Manutenzione tecnica:** Ray + agente IA in collaborazione.

---

**Ultimo aggiornamento:** 2026-04-25
**Versione cartografia:** v0.6.0
**Versione grafo storie:** v0.10.0
