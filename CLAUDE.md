# CLAUDE.md — Router della repo `isola_i3v_visual`

**Versione: 3.0 — 2026-06-12** · costruito su HEAD `7dadd00` (post standard-scene v1.1) (riordino router/skills: questo file contiene solo regole stabili e instradamento. Lo stato vive in `PROJECT_STATE.md`, la storia in `docs/fasi/`. Changelog completo: `git log -- CLAUDE.md`.)

Questo file spiega come funziona la repo e dove andare per ogni tipo di lavoro. **Leggilo sempre per primo.** È un invariante: cambia solo quando cambiano le regole o il routing, mai per aggiornare stato o cronaca.

---

## Cos'è questa repo (30 secondi)

1. **Progetto "L'Isola dei Tre Venti"**: saga di 12 storie illustrate per bambini 4-10 anni. Autore narrativo e proprietario: **Ray**.
2. **Canone macchina:** `saga_config.yaml` (single source of truth machine-readable: id, marker, lessico, vincoli). **Canone narrativo:** `pipeline_narrativa/` — **READ-ONLY**, sempre.
3. **Tracce attive:** `visual/` (catalogo entità), `cartografia/` (mappa), `web/` (catalogo v2 Next.js), `pipeline_narrativa/` (grafo + Bible + brief + storie), `_visual_pipeline/` (canonizzazione schede), `_starter_kit/` (template riusabile — mai contaminare con contenuto saga).
4. **Tracce archiviate:** `_porting_grafo/`, `_pacchetti_consegnati/`, `catalogo_web/` (legacy, solo `data/`). Non toccare.
5. **Spina dorsale:** script Python idempotenti (`scripts/`, `--dry-run` di default) + audit deterministici + Makefile. **L'idempotenza degli script è un requisito, non uno stile.**

## Da dove iniziare

1. Identifica il task → trova la riga nella **tabella di routing** qui sotto.
2. Leggi la skill/doc indicata → **stai nel suo scope**. Una sessione = una skill. Se il task ricade fra due skill, fermati e segnalalo a Ray.
3. Stato corrente: `PROJECT_STATE.md` · Flusso storia end-to-end: `docs/PIPELINE.md` · **Mappa annotata delle directory: `docs/MAPPA_REPO.md`** · Comandi: `make help` · Storia del progetto: `docs/fasi/`.

## Tabella di routing

<!-- ROUTING:BEGIN — generata da `make routing` (scripts/build_routing_table.py) dai frontmatter delle skill. Non editare a mano. -->
| Ruolo | Quando | Scrive in | Comandi | Skill |
|---|---|---|---|---|
| **brieffer** | generare/aggiornare i writing brief delle 12 storie (operatore di estrazione, zero token) | pipeline_narrativa/writing_briefs/ (solo via script) | make briefs | `skills/brieffer/SKILL.md` |
| **prosa** | scrivere il testo finale di una storia in chat collaborativa con Ray, una pagina alla volta | solo chat — non tocca la repo | — | `skills/prosa/SKILL.md` |
| **canonizzatore** | canonizzazione completa di una scheda visual (scheda + prompt grok + descrizione social + immagini canoniche, fase F.2) | visual/ (schede della entità in lavorazione) — via flusso _visual_pipeline/ | make catalogo (dopo ogni scheda) | `skills/canonizzatore/SKILL.md` |
| **visual** | descrizioni visive, vincoli prompt, immagini reference (famiglia visual; per la compilazione schede vedi compilatore.md) | visual/, scripts/ (tool condivisi) | make catalogo | `skills/visual/SKILL.md` |
| **illustratore** | caricamento immagini HD per stampa nei 3 contesti (scene, intro volume, catalogo) | subdir _hd/ via branch dedicata claude/hd-* + PR (mai merge in autonomia) | — | `skills/illustratore/SKILL.md` |
| **atlantista** | produrre le tavole-atlante full-page (prompt Manus + selezione + ingest) per le pagine abitanti/luoghi dei volumi | visual/atlante/ (tavole, prompt; spec SOLO via ingest_tavola.py) — branch claude/atlante-* | python3 scripts/ingest_tavola.py <manifest> · pytest tests/test_atlante.py | `skills/atlantista/SKILL.md` |
| **scenografo** | comporre prompt e generare le immagini di scena (una per subhook/pagina libro) | consegna file via skill illustratore (branch claude/hd-*) | — | `skills/scenografo/SKILL.md` |
| **cartografo** | manutenzione/estensione della cartografia tecnica (geojson, viewer, convenzioni) | cartografia/, scripts/ (tool condivisi) | — | `skills/cartografo/SKILL.md` |
| **contributore** | collaboratore esterno che propone aggiunte/dettagli alle schede (senza permessi di modifica diretta) | contributi/ — SOLO file nuovi datati, mai modificare esistenti | — | `skills/contributore/SKILL.md` |
| **pubblicatore** | preparare il pacchetto di pubblicazione Amazon KDP di un volume (PDF libro + PDF stampa + wrap copertina + bozza listing) | output/ (gitignored) + kdp/listing_volN.md (manuale). NON tocca pipeline_narrativa/, NON tocca visual/, NON pubblica su Amazon | python3 scripts/build_volume.py --volume N · python3 scripts/build_cover.py | `skills/pubblicatore/SKILL.md` |
| **manutentore** | lavoro SULLA repo — refactoring, ottimizzazioni, riordini, integrazione di pacchetti/branch, governance (non un ruolo operativo della pipeline) | trasversale ma dichiarato per intervento (perimetro scritto prima di toccare); branch claude/<scope>; MAI pipeline_narrativa/, MAI merge in autonomia | make sync · make check · make routing | `skills/manutentore/SKILL.md` |
<!-- ROUTING:END -->

**Flussi senza skill dedicata** (instradati a doc/prompt):

| Flusso | Doc operativo | Comandi |
|---|---|---|
| Estrazione 10 hook visivi (fase G, completata; riusabile per saghe nuove) | `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md` | `python3 scripts/write_hooks_to_graph.py --story sNN --dry-run` |
| Composizione PDF libro (KDP) | `pipeline_narrativa/storie_finali/README.md` (marker `@hook`/`@subhook`, asset, output) | `python3 scripts/build_volume.py --volume N` · test: `make test` |
| Pacchetti autoriali sul grafo (pattern "cornice del mondo") | `_pacchetti_consegnati/README.md` + `scripts/cornice_mondo/step*.py` come riferimento di stile | script idempotenti `--dry-run`/`--apply`, backup auto, **autorizzazione Ray esplicita** |
| Starter kit (template riusabile) | `_starter_kit/README.md` | scope di scrittura SOLO `_starter_kit/`; commit prefix `starter_kit:` |
| Audit grafo+prosa | `scripts/audit/README.md` | `make audit` (CI su ogni push) |

## Le tre fonti (architettura informativa — no ridondanze)

| Fonte | Vive in | Contiene |
|---|---|---|
| **Bible** | `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` | Canone narrativo: funzione e voce dei personaggi, vincoli, archi |
| **Grafo storie** | `pipeline_narrativa/story_graph.json` | Dinamica delle storie: scene, ruoli, seeds, callbacks, visual_anchors |
| **Catalogo visual** | `visual/<famiglia>/<...>/<id>/scheda.md` | Visivo: aspetto, palette, materiali, vincoli visivi, prompt, immagini |

**Regola di non-duplicazione:** un dato vive in **una sola** fonte. Dato visivo → catalogo (mai in Bible). Dato narrativo strutturale → Bible. Dato dinamico di scena → grafo. Routing senza ambiguità: aspetto → catalogo, voce → Bible, ruolo nella scena → grafo.

---

## Regole di non-danno (LEGGI PRIMA DI MODIFICARE)

### NEVER

- ❌ **Mai modificare `pipeline_narrativa/` senza autorizzazione esplicita di Ray.** Né grafo, né Bible, né documenti narrativi. Se rilevi un'incoerenza, **segnalala**, non risolverla in autonomia.
- ❌ **Mai modificare `_porting_grafo/` e `_pacchetti_consegnati/`.** Archivi chiusi (trail di audit). Nuovi pacchetti: si integrano, poi si archiviano qui e non si toccano più.
- ❌ **Mai inventare contenuto narrativo.** Niente descrizioni, palette, personaggi, vincoli che non sono nelle fonti (grafo, Bible, schede). Riporta solo dati esistenti o segnala se mancano.
- ❌ **Mai modificare schede in `visual/` aggiungendo info NON presenti nelle fonti.** Riformulare per chiarezza sì; il contenuto semantico deve essere tracciabile a fonte.
- ❌ **Mai eliminare o sovrascrivere lavoro precedente** senza prima leggerlo e capire perché c'era.
- ❌ **Mai `git push --force`, `git reset --hard`, `git checkout -- <file>` su file modificati senza chiedere. Mai `--no-verify`, mai `--amend` su commit altrui. Mai push diretto su `main` per lavori non banali.**
- ❌ **Mai sostituire `story_graph.json`.** Nuove migrazioni: processo tipo fase E (workspace separato + audit trail).
- ❌ **Mai contaminare `_starter_kit/`** con contenuto specifico della saga (prosa, schede reali, prompt del canone, snippet del grafo, immagini canoniche). Esempi solo con placeholder. Mai lavorare in `_starter_kit/` e fuori nella stessa sessione.
- ❌ **Mai modificare il canone visual** (`_visual_pipeline/_canone/*.md`) e **`saga_config.yaml`** senza autorizzazione + bump versione.

### ALWAYS

- ✅ **Sempre verifica lo stato prima di agire**: `git status`, `cat PROJECT_STATE.md`.
- ✅ **Sempre commit con messaggio descrittivo** (COSA + PERCHÉ), branch dedicato `claude/<scope>`, merge fast-forward su main (vedi Convenzioni Git).
- ✅ **Sempre applica la matrice di propagazione** (sezione sotto) dopo ogni modifica: `make sync` per il rigenerabile, entry `SYNC_LOG.md` per l'impatto cross-repo.
- ✅ **Sempre verifica il grafo** se il tuo lavoro lo tocca: `python3 -c "import json; json.load(open('pipeline_narrativa/story_graph.json'))"`.
- ✅ **Sempre preserva `_da popolare dal grafo_`** come marker di sezione vuota nelle schede; sostituisci solo con un dato concreto.

## Dopo ogni modifica — matrice di propagazione

Principio: **non ricordare le conseguenze, rigenerale.** Tutto ciò che è derivato si rigenera con `make sync` (idempotente: il `git status` dopo il sync È il report di cosa era disallineato). Il resto è in tabella.

| Se hai modificato | Allora |
|---|---|
| `visual/**` (schede, prompt_grok, immagini) | `make sync` (rigenera catalogo + brief) |
| `pipeline_narrativa/story_graph.json` (via script autorizzati) | `make sync` + `make audit` |
| `pipeline_narrativa/narrazione_fattuale/` o `documenti_progetto/` (autorizzato) | `make sync` (i brief li incorporano) |
| `pipeline_narrativa/storie_finali/sNN_*.md` | `make audit` + rebuild volume quando serve (`build_volume.py`) |
| `saga_config.yaml` (autorizzato) | bump `config_version` + `make sync` + `make audit` |
| `skills/**` (nuova skill, scope o trigger cambiati) | `make routing` (rigenera la tabella qui sopra) |
| `visual/atlante/` (tavole/manifest) | `ingest_tavola.py` (MAI scrivere lo spec a mano) + `pytest tests/test_atlante.py` |
| `scripts/**` | `make check` (test + audit) |
| `web/**` | test app (`web/`: `npm test` dove previsto) + verifica deploy |
| `CLAUDE.md` / `docs/PIPELINE.md` | bump della versione nell'header del file toccato |
| Qualsiasi modifica con impatto su altre repo / sistemi esterni | entry in `SYNC_LOG.md` (convenzione `SYNC-YYYY-MM-DD-NNN`) |
| Fine sessione significativa | aggiorna `PROJECT_STATE.md` (snapshot: sostituisci, non accumulare — la sessione precedente scivola in `docs/fasi/SESSIONI_ARCHIVIO.md`) |

## Convenzioni Git

- **Branch principale**: `main`. Lavori non banali: branch `claude/<scope>` + merge fast-forward su main.
- **Commit message**: prima riga ≤72 char descrittiva, poi corpo con **perché + cosa**.
- **Push protocol**: `git push -u origin <branch>`; su network error, retry 4 volte con backoff (2s, 4s, 8s, 16s).
- **PR di lavori esterni** (illustratore, contributi): mai mergiare in autonomia — review di Ray.

## Come comunicare con Ray

Ray è esperto e tecnico, preferisce onestà ad adulazione, lavora in italiano (rispondi in italiano).

- Proposte specifiche: "Aggiungo X in Y perché la Bible §Z dice W". Incertezza dichiarata: "non so se X è canonico o inferito". Incoerenze: **segnalale, mai sistemarle in silenzio**. A task finito: mostra diff e file toccati, non riassunti vaghi.
- Niente lubrificazioni sociali ("ottima idea!"), niente spiegazioni elementari, niente disclaimer eccessivi. **Non reinterpretare narrativamente le storie**: il canone lo decide Ray.

**Domande da fare sempre, qualsiasi skill:** "Questo ID nuovo è canonico o provvisorio?" · "Posso promuovere X a canonico?" (sempre, prima di farlo) · "Conflitto Bible vs grafo: vince Bible, giusto?" · "Task a cavallo di due skill: splitto o eccezione?"

**Pattern di rifiuto:** se una richiesta implica modificare il canone, toccare `pipeline_narrativa/`, inventare tratti/eventi, o scrivere prosa fuori dalla skill prosa → rifiuta e redirigi a Ray.

## Quando in dubbio

1. `PROJECT_STATE.md` per lo stato → 2. tabella di routing per la skill → 3. `docs/PIPELINE.md` per il flusso storia → 4. **chiedi a Ray prima di agire**. Meglio una domanda in più che un commit da rollback.

---

**Autore narrativo e proprietario**: Ray. **Manutenzione tecnica**: Ray + agenti IA (Claude Sonnet/Opus tipicamente).
