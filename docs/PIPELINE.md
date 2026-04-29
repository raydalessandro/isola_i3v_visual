# PIPELINE — Flusso end-to-end per una storia

Questo documento descrive il **flusso operativo** dall'idea autoriale di Ray fino al testo libro committato. Vale per ogni storia s01..s12 (e per future espansioni).

> **Nota:** la repo è **strutturata** e parzialmente **automatizzata**. La fase G (estrazione 10 hook visivi per storia) è stata completata il 2026-04-29 con tooling deterministico (`scripts/write_hooks_to_graph.py` + agenti sub `general-purpose` per la stesura). Stato: ~70% delle tappe meccaniche automatizzate; manca prompt+orchestrazione per la scrittura prosa autoriale (Tappa 6).
>
> **Pipeline parallela visual** (canonizzazione delle 115 schede `visual/` + immagini canoniche per illustrazioni): vedi [`_visual_pipeline/`](../_visual_pipeline/) — flusso a 6 fasi separato dal flusso storia, alimenta il prompt-immagine finale con reference visivi per personaggi/oggetti/luoghi.

---

## Diagramma di flusso

```
┌─────────────────────────────────────────────────────────────────────┐
│  TAPPA 0  — IDEA AUTORIALE (Ray, chat dedicata lunga)               │
│  Input:   testa di Ray + Bible + grafo + ARCHI                      │
│  Output:  conversazione con i fatti della storia                    │
│  Auto:    0%  (umano puro, by design)                               │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│  TAPPA 1  — NARRAZIONE FATTUALE                                     │
│  Input:   conversazione tappa 0                                     │
│  Output:  pipeline_narrativa/narrazione_fattuale/sNN_*.md           │
│  Auto:    20%  (Ray scrive; agente può fare review strutturale)     │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│  TAPPA 2  — ESTRAZIONE 10 HOOK VISIVI                               │
│  Input:   narrazione_fattuale/sNN_*.md                              │
│           + pipeline_narrativa/story_graph.json#stories.sNN         │
│           + Bible + Carta Voce + Pattern AI da bandire              │
│           + cartografia/convenzioni/orientamenti_venti.md           │
│           + visual/ (schede personaggi/luoghi/oggetti)              │
│  Output:  proposta 10 hook in markdown                              │
│  Auto:    80%  (agente con prompt stretto)                          │
│  Prompt:  pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE  │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│  TAPPA 3  — REVIEW HOOK (Ray)                                       │
│  Input:   proposta tappa 2                                          │
│  Output:  OK / edit                                                 │
│  Auto:    0%  (umano, decisioni autoriali)                          │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│  TAPPA 4  — SCRITTURA NEL GRAFO                                     │
│  Input:   hook approvati                                            │
│  Output:  pipeline_narrativa/story_graph.json aggiornato            │
│           (sezione stories.sNN.visual_anchors.scene_hooks)          │
│  Auto:    100%  (agente: edit + bump graph_version + last_updated)  │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│  TAPPA 5  — AUDIT GRAFO                                             │
│  Input:   grafo modificato                                          │
│  Output:  PASS / FAIL                                               │
│  Auto:    100%  (4 script Python, da implementare)                  │
│  Script:  scripts/audit/audit_1_integrity.py                        │
│           scripts/audit/audit_2_schema.py                           │
│           scripts/audit/audit_3_navigability.py                     │
│           scripts/audit/audit_4_drift.py                            │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│  TAPPA 6  — SCRITTURA PROSA LIBRO (voce autoriale)                  │
│  Input:   narrazione fattuale + 10 hook canonici                    │
│           + Bible + Carta Voce + Pattern AI da bandire              │
│           + schede visual/ (palette, vincoli, voci personaggi)      │
│  Output:  libro/sNN_<titolo>.md  (testo prosa per illustrazione)    │
│  Auto:    60%  (agente con prompt stretto + review Ray)             │
│  Prompt:  pipeline_narrativa/prompts/PROMPT_AGENTE_PROSA  (DA SCRIVERE) │
└─────────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│  TAPPA 7  — REVIEW PROSA + COMMIT                                   │
│  Input:   testo proposto                                            │
│  Output:  commit + push su main                                     │
│  Auto:    20%  (review Ray umano, commit/push automatico)           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Tabella sintetica

| # | Tappa | Input | Output | Auto | File chiave |
|---|---|---|---|---|---|
| 0 | Idea autoriale | testa Ray | conversazione | 0% | (chat) |
| 1 | Narrazione fattuale | conversazione | `narrazione_fattuale/sNN.md` | 20% | `pipeline_narrativa/narrazione_fattuale/` |
| 2 | Estrazione 10 hook | narrazione + grafo + Bible | proposta hook | 80% | `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md` |
| 3 | Review hook | proposta | OK/edit | 0% | (Ray) |
| 4 | Scrittura grafo | hook approvati | `story_graph.json` aggiornato | 100% | `pipeline_narrativa/story_graph.json` |
| 5 | Audit grafo | grafo nuovo | PASS/FAIL | 100% | `scripts/audit/*` |
| 6 | Prosa autoriale | grafo + voce + visual | `libro/sNN.md` | 60% | prompt da scrivere |
| 7 | Review + commit | testo | git push | 20% | (git) |

**Totale automatizzazione (escludendo input umano puro tappa 0): ~70%**

---

## Stato attuale (2026-04-29)

### Pronto e funzionante

- **Tappa 1** (narrazione fattuale): 12/12 file `pipeline_narrativa/narrazione_fattuale/sNN_*.md` disponibili (sorgente unico in `_source/Ciclo*.txt` + script `scripts/split_narrazione_fattuale.py` idempotente).
- **Tappa 2** (estrazione hook): prompt operativo + workflow validato. Modalità: agente sub general-purpose con prompt mirato → proposta markdown → review umana → conversione YAML.
- **Tappa 4** (scrittura grafo): `scripts/write_hooks_to_graph.py` con 16 controlli pre-scrittura, idempotente, backup automatico. **Eseguito su tutte le 12 storie il 2026-04-29 — Fase G completata, 120/120 hook v1.3 nel grafo.**
- **Schema bump v1.2 → v1.3**: eseguito via `scripts/migrate_graph_v1_2_to_v1_3.py` (one-shot, retro-compat sui hook legacy).
- **Promozione entità catalogo → grafo**: `scripts/promote_visual_entities_to_graph.py` (idempotente).

### Specificato ma non implementato

- **Tappa 5** (audit grafo): 4 script specificati in `scripts/audit/README.md`. Da implementare prima dell'avvio fase G a regime. **3 di 4 sono Python puro** (integrity/schema/navigability). Il 4° (drift) richiede LLM per controllare pattern AI da bandire.
- **Tappa 6** (prosa autoriale): prompt **da scrivere**. Pattern replicabile dal prompt fase G (stessa struttura: lettura fonti → proposta → review → commit).

### Umano puro (by design)

- **Tappa 0** (idea autoriale): chat lunga dedicata con Ray. Non automatizzare.
- **Tappa 3** (review hook): decisione autoriale, sempre umana.
- **Tappa 7** (review prosa): decisione autoriale, sempre umana.

---

## Esempio: nuova storia s07 (riferimento di flusso)

> Sequenza ipotetica per illustrare l'uso del flusso. Quando arriveranno le narrazioni fattuali reali, queste sono le tappe da seguire.

1. **Ray** (chat dedicata lunga): definisce idea, archi, vincoli per s07.
2. **Ray** scrive `pipeline_narrativa/narrazione_fattuale/s07_la_zattera_dei_tre_rametti.md` (fatti, no voce).
3. **Agente** (con `PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md`): legge narrazione + grafo + Bible + Carta Voce + visual/, propone 10 hook in markdown.
4. **Ray**: review, edit, OK.
5. **Agente**: scrive nel grafo (`story_graph.json#stories.s07.visual_anchors.scene_hooks`), bump `graph_version` 1.0.0 → 1.1.0.
6. **Agente**: lancia 4 audit. Se PASS, conferma. Se FAIL, blocca.
7. **Agente** (con `PROMPT_AGENTE_PROSA` — da scrivere): legge grafo aggiornato + Carta Voce + Bible + schede visual, propone prosa in `libro/s07_la_zattera_dei_tre_rametti.md`.
8. **Ray**: review, edit, OK.
9. **Agente**: commit + push.

Una storia per volta. Mai parallelo. Approvazione Ray tra tappa e tappa critica (3 e 7).

---

## Cosa manca per scalare il flusso (lavoro futuro)

Quando le 12 storie saranno completate manualmente con questo flusso, le 3 cose da preparare per **rendere il processo davvero automatizzato** in futuro (es. revisioni, espansioni, traduzioni) sono:

1. **`scripts/audit/audit_1..4.py`** — implementazione dei 4 audit. Specs già pronte in `scripts/audit/README.md`. Stima: mezza giornata.
2. **`pipeline_narrativa/prompts/PROMPT_AGENTE_PROSA_v1.md`** — prompt operativo per scrittura prosa autoriale. Stesso pattern del prompt hook. Stima: 2-3 iterazioni con Ray sulla Carta Voce.
3. **Skill orchestratore** — un file `skills/pipeline_storia.md` che dato uno `sNN_input.md` esegue le tappe 2-7 in sequenza, fermandosi alle review umane. Stima: 1 giornata.

Stato post-storie: il sistema è documentato, riproducibile, e l'investimento di token speso fin qui (porting grafo + struttura repo + decisioni autoriali) si traduce in un acceleratore stabile per ogni storia futura. Le decisioni autoriali (le idee, le scelte di voce, i vincoli) restano l'unico input umano necessario.

---

## Riferimenti

- Mappa repo + regole non-danno: `CLAUDE.md`
- Stato corrente: `PROJECT_STATE.md`
- Snapshot storico: `cartografia/CHANGELOG.md`, `_porting_grafo/output/` (fase E)
- Sorgenti canoniche: `pipeline_narrativa/documenti_progetto/` (Bible, Carta Voce, ARCHI, Pattern AI da bandire, ecc.)
