---
role: contributore
trigger: collaboratore esterno che propone aggiunte/dettagli alle schede (senza permessi di modifica diretta)
scope_write: "contributi/ — SOLO file nuovi datati, mai modificare esistenti"
commands: "—"
order: 80
---

# Skill — Contributore esterno (proposte di aggiunta alle schede)


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
