# CLAUDE.md — Istruzioni per istanze IA + collaboratori

Questo file spiega come funziona la repo `isola_i3v_visual` e cosa devi (e non devi) fare quando ci lavori. **Leggilo sempre per primo.**

Versione: 2026-04-28 (post-fase E grafo v1.0.0).

---

## TL;DR (in 30 secondi)

1. **Repo del progetto "L'Isola dei Tre Venti"** (saga 12 storie illustrate per bambini 4-10, autore: Ray).
2. **Tre tracce di lavoro attive**: `cartografia/` (mappa), `visual/` (descrizioni entità), `pipeline_narrativa/` (grafo + Bible — **read-only**).
3. **Una traccia archiviata**: `_porting_grafo/` (migrazione una-tantum del grafo, completata, NON toccare).
4. **Una traccia per contributi esterni**: `contributi/` (proposte di aggiunta schede — solo create file nuovi datati, mai modificare esistenti).
5. **Mai modificare** `pipeline_narrativa/` (grafo + Bible) senza autorizzazione esplicita.
6. **Mai inventare contenuto narrativo**. Riporta solo dati esistenti nelle fonti canoniche o segnala se mancano.
7. **Sempre fare commit chiari** sul branch corrente, **mai push --force**, **mai modificare commit altrui**.

---

## 1. Mappa della repo

```
isola_i3v_visual/
│
├── pipeline_narrativa/        ⚠️ READ-ONLY (canone narrativo)
│   ├── story_graph.json              v1.0.0 schema 1.2 (12 storie + entities + seeds + callbacks + quote_tracker)
│   ├── story_graph.v0.10.0.backup.json  backup pre-migrazione fase E
│   └── documenti_progetto/           Bible, Carta Voce, ARCHI, Glossario, EAR, Pattern AI da bandire
│
├── visual/                    ✅ scrittura su scheda.md per arricchimento (con cautela)
│   ├── personaggi/                   23 schede (3 fratelli, 5 primari, 5 secondari, 5 cuccioli, 5 collettivi)
│   ├── luoghi/                       74 schede (per quartiere: aria/acqua/fuoco/terra/centro + perimetro + strade)
│   ├── oggetti/                      14 schede (13 oggetti-simbolo saga + 1 oggetto_di_scena_ricorrente)
│   ├── venti/                        3 schede (Taglio/Intreccio/Mulinello)
│   └── visual_signatures/            1 scheda (quando_acqua_trema)
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
├── contributi/                ✅ scrittura per collaboratori esterni (proposte/aggiunte)
│   └── (file .md datati, vedi sezione 5)
│
├── scripts/                   ✅ tool Python condivisi (idempotenti)
│   ├── build_catalogo_web.py         rigenera catalogo_web/data/entities.json da visual/
│   ├── build_visual_skeleton.py      ricrea schede stub da grafo (non usare in fase F)
│   └── compile_visual_from_graph.py  travaso meccanico grafo → schede (fase F.1)
│
├── skills/                    ✅ skill agente IA
│   ├── README.md                     orchestratore
│   ├── cartografo.md                 manutenzione cartografia
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
- ❌ **Mai inventare contenuto narrativo.** Niente descrizioni di scene, palette, personaggi, vincoli che non sono nelle fonti (grafo, Bible, character_constraints, canonical, schede esistenti).
- ❌ **Mai modificare schede in `visual/` aggiungendo info NON presenti nelle fonti.** È accettabile riformulare per chiarezza, ma il contenuto semantico deve essere tracciabile a fonte.
- ❌ **Mai eliminare o sovrascrivere lavoro precedente** senza prima leggerlo e capire perché c'era.
- ❌ **Mai `git push --force`, mai `git reset --hard`, mai `git checkout -- <file>` su file modificati senza chiedere.**
- ❌ **Mai committare con `--no-verify` o `--amend` su commit altrui.**
- ❌ **Mai sostituire il `story_graph.json` corrente.** Se serve una nuova migrazione, segui un processo come fase E (workspace separato + audit trail).

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
- **12/12 storie** in `pipeline_narrativa/story_graph.json` v1.0.0 schema 1.2
- **60 no_inference_fields decisi** via Q1-Q6 autoriali Ray (entry_point_type, closure_type, register, estimated_length, descriptive_pauses_count per ogni storia)
- **87 provvisori P2** (22A + 47B + 18C) tracciati nei provisional file di `_porting_grafo/output/`
- **8 misalignments tutti resolved** (mis_001..mis_007 + mis_008)
- **Catalogo isola_i3v_visual: 115 entities** (114 visual + 1 nuovo `pallone_di_stoffa_cucita` come `oggetto_di_scena_ricorrente`)
- **Backup pre-migrazione**: `pipeline_narrativa/story_graph.v0.10.0.backup.json`

### Fase F — IN CORSO (2026-04-28+)

Compilazione body schede `visual/` usando il grafo v1.0.0 come fonte autorevole:
- **F.1 (fatto, meccanico)**: `scripts/compile_visual_from_graph.py` ha travasato dati grafo → 56 sezioni stub compilate (Identità visuale, Espressione/comportamento, Cliché da evitare, Storie/scene di apparizione).
- **F.2 (in corso)**: Ray + collaboratori esterni aggiungono dettagli autoriali alle schede (`Variabilità ammessa`, `Per stampa 3D`, `Per narrativa e social` + arricchimenti narrativi).
- **F.3 (pianificata)**: travaso inverso visual → grafo per dettagliare gli `entities` del grafo dove le schede hanno info aggiuntiva.

---

## 4. Modalità operative (chi fa cosa)

### Modalità "agente cartografo"
Manutenzione cartografia. Solo `cartografia/`. Vedi `skills/cartografo.md`.

### Modalità "agente visual / compilatore"
Compilazione schede `visual/`. Vedi `skills/visual/compilatore.md`.
- Travaso meccanico fonte → scheda (no inferenza)
- Sostituisce solo placeholder `_da popolare dal grafo_`
- Rigenera `catalogo_web/data/entities.json` dopo modifiche

### Modalità "lettore + commentatore" (collaboratore esterno)
Vedi sezione 5 (regole rigorose).

### Modalità "porting grafo"
**Non più attiva.** Fase E completata. Riferimento storico in `_porting_grafo/`.

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

# Verifica grafo (deve essere JSON valido v1.2)
python3 -c "import json; g=json.load(open('pipeline_narrativa/story_graph.json')); print('schema:', g['schema_version'], 'graph:', g['graph_version'], 'stories:', len(g['stories']))"

# Avvia catalogo web in locale
python3 -m http.server  # poi browser → http://localhost:8000/catalogo_web/

# Apri viewer cartografia (no server, doppio click)
# cartografia/geo/viewer/index.html
```

---

## 8. Quando in dubbio

1. Leggi `README.md` per la panoramica.
2. Leggi `PROJECT_STATE.md` per stato operativo.
3. Cerca skill specifica in `skills/`.
4. Se ancora non chiaro: **chiedi a Ray prima di agire**. Meglio una domanda in più che un commit da rollback.

---

**Autore narrativo e proprietario**: Ray.
**Manutenzione tecnica**: Ray + agenti IA in collaborazione (Claude Sonnet/Opus tipicamente).
**Ultimo aggiornamento istruzioni**: 2026-04-28.
