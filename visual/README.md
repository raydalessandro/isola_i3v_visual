# visual/ — Serbatoio descrizioni visive dell'Isola

Fonte unica per tutto ciò che è **visivo** nel progetto *L'Isola dei Tre Venti*: descrizioni ricche per IA generative, riferimenti per illustratori, modelli per stampa 3D, dettagli per narrativa e campagne social.

**Per il workflow operativo dell'agente IA:** vedi [`skills/visual/README.md`](../skills/visual/README.md) e le sotto-skill in [`skills/visual/`](../skills/visual/) (es. `compilatore.md` per la compilazione delle schede).

## Struttura

Albero frattale che rispecchia la struttura dell'isola. Ogni entità è una **cartella autocontenuta** con `scheda.md` + `immagini/` + eventuali file di espansione (prompt dedicati, varianti).

```
visual/
├── catalogo.md                      indice generato (rigenerabile via script)
├── _template_scheda.md              template scheda (riferimento)
├── personaggi/
│   ├── individuali/{bambini,primari,cuccioli,secondari}/<id>/
│   └── collettivi/<id>/
├── luoghi/<quartiere>/<luogo>/[sotto-luogo/]
├── oggetti/<id>/
├── venti/<id>/
├── visual_signatures/<id>/
└── sito/                            static site futuro
```

## Stato

**Bootstrap completo (2026-04-25):** 81 schede stub create automaticamente. Frontmatter YAML compilato da grafo + GeoJSON (per i luoghi: coords, bbox, dimensioni, quartiere, parent/children). Body da popolare via estrazione (sub-agenti, una famiglia per volta).

## Rigenerare/aggiornare

Lo script principale è **idempotente**:

```bash
python3 scripts/build_visual_skeleton.py
```

- Crea cartelle e schede mancanti.
- Su schede esistenti: rigenera SOLO il frontmatter (derivato da fonti); preserva il body (lavoro umano/agenti).
- Rigenera `catalogo.md`.

Quindi quando il GeoJSON viene aggiornato (es. nuova altitudine), basta rilanciare lo script.

## Convenzioni file

- **Lingua:** italiano per tutto (descrizioni, frontmatter, sezioni).
- **Status scheda:** `stub` → `provvisorio` → `canonico` (approvato Ray).
- **Naming immagini:** `<id>_<vista>_<varianteN>.{png|jpg}` (es. `gabriel_fronte_v1.png`); le 4 vedute canoniche per stampa 3D sono **fronte / retro / profilo_dx / profilo_sx**.
- **Metadati immagini:** opzionale file `<id>_<vista>_<varianteN>.meta.md` con prompt usato, modello, seed, data, stato.
