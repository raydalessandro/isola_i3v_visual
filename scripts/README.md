# scripts/

Tool Python condivisi della repo (flusso storia, visual, audit, build libro). Idempotenti: rieseguibili senza effetti collaterali su lavoro esistente. Mappa annotata completa in `docs/MAPPA_REPO.md`.

## Indice

**Canone / grafo**
- `saga_canon.py` — loader e validatore di `saga_config.yaml` (il contratto machine-readable); importato dai 5 audit, dal writer hook, dalla dashboard.
- `write_hooks_to_graph.py` — writer deterministico degli hook nel grafo (16 controlli pre-scrittura, backup, dry-run).
- `compile_visual_from_graph.py` · `promote_visual_entities_to_graph.py` — travaso/promozione catalogo↔grafo (idempotenti).

**Audit** (`scripts/audit/`, vedi suo `README.md`)
- `run_all_audits.py` — runner dei 5 audit (`make audit`); `--fast` salta `audit_4` (drift prosa).

**Brief / catalogo / dashboard / routing**
- `build_writing_brief.py` — genera i 12 writing brief zero-token per la prosa.
- `build_catalogo_web.py` — genera `catalogo_web/data/entities.json` (richiede PyYAML).
- `build_storie_data.py` — genera `catalogo_web/data/storie.json`.
- `build_dashboard.py` — genera i dati della dashboard di sistema (`dashboard/`).
- `build_routing_table.py` — rigenera la tabella di routing in `CLAUDE.md` dai frontmatter skill.

**Build libro / identità visiva**
- `build_volume.py` — compositore PDF libro KDP (A5 300 DPI). `design_system.py` — identità visiva collana (palette, font, glifi, cornici).

**Visual / atlante / narrazione**
- `build_visual_skeleton.py` — struttura `visual/` da grafo + geojson (bootstrap; non in fase F).
- `ingest_tavola.py` — ingest dello spec delle tavole-atlante (skill `atlantista`).
- `split_narrazione_fattuale.py` — split del sorgente `_source/Ciclo*.txt` in 12 narrazioni fattuali.

**One-shot completati (trail, non rieseguire)**
- `migrate_graph_v1_2_to_v1_3.py`, `cornice_mondo/step*.py` — migrazioni del grafo già applicate, tenute come audit trail.

## Principi

- **Idempotenza:** ogni script si può rilanciare senza danni.
- **Letture:** consentite ovunque (incluso `pipeline_narrativa/` read-only).
- **Scritture:** ogni script dichiara in testa quali directory tocca.
- **Niente segreti:** mai credenziali o token nei file di questa cartella.
- **Aggiunte future:** quando uno script diventa stabile, citarlo nelle skill (`skills/cartografo/SKILL.md`, `skills/visual/SKILL.md` o sotto-skill) come metodo uniformante.

## Uso tipico

```bash
# Dalla radice del repo
python3 scripts/build_visual_skeleton.py
```
