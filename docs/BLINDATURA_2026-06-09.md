# BLINDATURA — Report pacchetto 2026-06-09

**Scope:** migliorare, ottimizzare e blindare la repo `isola_i3v_visual`.
**Vincolo rispettato:** `pipeline_narrativa/` non toccata (read-only, CLAUDE.md §2). Le incoerenze trovate nel grafo sono SEGNALATE qui e nella baseline, non corrette in autonomia.
**Stato finale verificato in ambiente pulito:** 78 test veloci PASS (2.5s) · 6 test integrazione PASS (build PDF reale, 45s) · 4/4 audit PASS.

---

## 1. Cosa è stato consegnato

### 1.1 Audit grafo + prosa (il gap dichiarato, chiuso)

`scripts/audit/` passava da README-con-intenzioni a sistema operativo:

| File | Ruolo |
|---|---|
| `audit_1_integrity.py` | parse strict (chiavi duplicate intercettate), versioni attese, 12 storie, migration_log cronologico, **catena backup congelata** via manifest SHA-256 |
| `audit_2_schema.py` | i 16 vincoli del writer replicati **a riposo** + schema cornici (DOC_3) + world_conventions (5 sentieri Tier A, 20 dettagli) + quote_tracker |
| `audit_3_navigability.py` | integrità referenziale completa: hook, campi storia, cornici, seeds, callbacks, path_details ↔ catalogo. Universo luoghi esteso (entities ∪ locations_secondary ∪ path_details ∪ schede visual ∪ quartieri) |
| `audit_4_drift.py` | parte meccanica del drift: quote lessicali `PATTERN_AI_DA_BANDIRE` §6 sulla prosa + coerenza marker `@hook`/`@subhook` ↔ grafo ↔ immagini su disco |
| `run_all_audits.py` | orchestratore (`--fast` salta la prosa) |
| `_data/backup_manifest.sha256` | SHA-256 congelati dei 7 backup del grafo |
| `_data/known_issues.yaml` | baseline a cricchetto delle incoerenze note (vedi §3) |

**Principio a cricchetto:** le 7 incoerenze già presenti nel canone non bloccano la CI (sono in baseline, visibili, in attesa di tua decisione); qualunque incoerenza **nuova** la blocca. Lo stato può solo migliorare.

**Fuori scope dichiarato di audit_4:** ancorabilità `focal_action` ↔ narrazione fattuale e domande qualitative §6 (triadi, pugno emotivo, sguardo adulto-tenero) restano review umana/agente — un grep non le decide.

### 1.2 CI come cancello

- **`.github/workflows/ci.yml`** (nuovo): job `test` (pytest veloce) + job `audit` (1..4) su ogni push/PR; job `integration` (build PDF reale + invarianti KDP) sulle PR verso main.
- **`rebuild-catalogo.yml`** (fix): aggiunto `pip install PyYAML` — il workflow attuale **fallirebbe su runner pulito** (PyYAML non è incluso nel Python di actions/setup-python); aggiunto push con retry+rebase contro race se il branch avanza durante il run; cache pip.

### 1.3 Robustezza scritture

- `write_hooks_to_graph.py` → `save_graph()` ora **atomica** (tmp + `os.replace`): un'interruzione a metà scrittura non può più lasciare il grafo canonico troncato.
- `build_catalogo_web.py` → stessa protezione su `entities.json` (gira in CI, una CI cancellata non lascia file a metà).
- Pattern documentato nei commenti: da riusare in ogni futuro script che scrive sul grafo.

### 1.4 Dipendenze e riproducibilità

- **`requirements.txt`** + **`requirements-dev.txt`** (prima: nessuna dichiarazione a livello repo; `PyMuPDF`, richiesto dai test di integrazione, non era documentato da nessuna parte — i 6 test PDF venivano silenziosamente skippati).
- **`web/package-lock.json`** generato (452 pacchetti, lockfileVersion 3): il `package.json` usa range con caret (`^`), senza lockfile ogni `npm install` può risolvere versioni diverse → build non riproducibili e superficie supply-chain. Da committare.
- **`Makefile`**: `make check` = test + audit (il cancello pre-push), più `audit`, `test`, `test-all`, `catalogo`, `briefs`, `volume1`.

### 1.5 Test degli audit (proteggere i protettori)

`tests/test_audits.py` — 24 test: smoke (gli audit passano sulla repo corrente) + corruzioni sintetiche (9 hook, enum fuori range, 4 signature, focal_action 31 parole, hook fuori sequenza, "piano piano" ×2, marker mancanti, prosa≠grafo, apparato subhook incompleto, marker d'esempio nel frontmatter ignorati). Un refactor che spegne un controllo viene intercettato qui.

### 1.6 Documentazione allineata

- `scripts/audit/README.md` riscritto (stato: implementato, convenzioni, manifest, baseline).
- `CLAUDE.md`: versione 2026-06-09, mappa repo e sezione audit aggiornate.
- `docs/PIPELINE.md`: tappa 5 (audit) da "da implementare" a operativa.
- Docstring `write_hooks_to_graph.py`: 25→30 parole (vedi §3.5).

---

## 2. Verifica eseguita (ambiente pulito, Python 3.11)

```
pytest -m "not slow"      78 passed in 2.54s   (54 esistenti + 24 nuovi)
pytest -m slow             6 passed in 44.98s  (build PDF reale vol.1 + invarianti KDP)
run_all_audits.py          4/4 PASS
build_catalogo_web.py      116 entità, 83 immagini — invariato dopo patch atomica
write_hooks_to_graph.py --story s01 --dry-run   10 hook validi — invariato
npm install --package-lock-only                 lockfile coerente con package.json
```

---

## 3. Incoerenze di canone trovate — DECISIONI RICHIESTE A RAY

Tutte intercettate dalla prima esecuzione di `audit_3` (cioè: il sistema funziona). `pipeline_narrativa/` è read-only → correzioni solo con tua autorizzazione, idealmente via script idempotente stile cornice_mondo. Fino ad allora vivono in `known_issues.yaml`.

### 3.1 `s06.location_primary = "centro_villaggio"`
L'id canonico è **`villaggio_centrale`** (ordine invertito). Riferimento pendente.

### 3.2 Cornici `margine_foresta_intrecciata` (s02_c2, s03_c2, s04_c2, s07_c2)
L'id non esiste in nessun universo (entities, locations_secondary, path_details, schede visual). Il margine come concetto è canonico (`sentiero_casa_salvia_margine_foresta` esiste). Ipotesi: `where.location_id = foresta_intrecciata` + `where.qualifier = "margine"` (il campo qualifier esiste già nello schema cornice). Alternativa: promuovere `margine_foresta_intrecciata` a location.

### 3.3 Cornice `s06_c2: pontile`
Id canonico: **`pontile_bocca`**.

### 3.4 Cornice `s05_c2: who.ref = "pun_e_memolo"`
Ref composito; nel grafo esistono solo `pun` e `memolo` separati. Decisione di schema: splittare il ref in lista oppure ammettere ref compositi nelle cornici (e allora definirne la grammatica).

### 3.5 Drift documentale focal_action: 25 vs 30 parole
Docstring del writer e README audit dicevano **≤25**; il codice del writer ha sempre applicato **≤30** e 59/120 hook nel grafo superano 25. Ho allineato la documentazione a 30 (la regola effettivamente operante, dati conformi). Se la tua intenzione editoriale era 25, va deciso esplicitamente: oggi significherebbe rivedere 59 hook.

### 3.6 Warning informativi (non bloccanti, nessuna azione urgente)
- `villaggio_centrale.contains` usa alias legacy: `piazza_centrale` (canone: `piazza_villaggio`), `casa_memolo` (canone: `casa_memolo_cortile`), `bottega_nodo` (nessuna scheda propria). Campo descrittivo, nessuno script lo consuma.
- `PROJECT_STATE.md` ha la coda ferma all'era cartografia e cita `AGENT_INSTRUCTIONS.md` (oggi `CLAUDE.md`). Da rinfrescare alla prossima sessione di stato.
- `quadrant: "acqua_nord"` esiste nel grafo (oltre ad acqua_sud); l'ho incluso nell'enum valido degli audit come canone esteso — conferma che è intenzionale.

---

## 4. Note di architettura (per i prossimi cicli, nessuna azione ora)

1. **Apparato subhook 1/12.** Solo s01 ha `book_pages_total` + marker `@subhook`/`@page_book`. audit_4 lo tratta come migrazione in corso (`[info]`, pilota s01) e **diventa vincolante automaticamente** su ogni storia che inizia l'apparato. Quando migri s02..s12, il compositore è già coperto.
2. **Bump di versione del grafo** = aggiornare `EXPECTED_SCHEMA`/`EXPECTED_GRAPH` in `audit_1` nello stesso commit (così rollback e bump non autorizzati vengono intercettati). Nuovi backup: `audit_1 --update-manifest`.
3. Gli step `cornice_mondo/step*.py` scrivono ancora non-atomico: sono fase chiusa, non li ho toccati; se mai riusati per Tier B/C, applicare il pattern tmp+replace di `save_graph()`.
4. Azioni GitHub puntate per tag major (`@v4`/`@v5`): per massima blindatura supply-chain si possono pinnare per SHA — costo di manutenzione in più, scelta tua.

---

## 5. Integrazione (Git-native)

```bash
git checkout -b claude/blindatura-audit
# copiare i file del pacchetto (path relativi alla root repo)
make deps && make check        # 78 test + 4/4 audit attesi PASS
git add -A && git commit       # COSA + PERCHÉ: vedi questo report
git push -u origin claude/blindatura-audit
# review → merge ff su main
```

File nuovi: `scripts/audit/audit_{1,2,3,4}_*.py`, `scripts/audit/run_all_audits.py`, `scripts/audit/_data/{backup_manifest.sha256, known_issues.yaml}`, `.github/workflows/ci.yml`, `requirements.txt`, `requirements-dev.txt`, `Makefile`, `tests/test_audits.py`, `web/package-lock.json`, questo report.
File modificati: `scripts/audit/README.md`, `.github/workflows/rebuild-catalogo.yml`, `scripts/write_hooks_to_graph.py`, `scripts/build_catalogo_web.py`, `CLAUDE.md`, `docs/PIPELINE.md`.
Non toccati: `pipeline_narrativa/` (read-only), `_porting_grafo/`, `_pacchetti_consegnati/`, `_starter_kit/`, `visual/`, `cartografia/`, `catalogo_web/` (rigenerabile).
