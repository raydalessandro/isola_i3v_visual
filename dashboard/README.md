# Dashboard di sistema

Vista **meta** della repo: regole, ruoli, stato e debito del sistema che
produce la saga — non il contenuto della saga.

## Uso

```bash
make dashboard            # rigenera dashboard/data/dashboard.js
open dashboard/index.html # funziona da file://, nessun server necessario
```

`make sync` include la rigenerazione della dashboard.

## Architettura

- **`scripts/build_dashboard.py`** — estrattore meccanico, zero LLM, solo
  stdlib. Scansiona la repo e scrive `data/dashboard.js`
  (`window.DASHBOARD_DATA = {...}`). Idempotente: due run senza modifiche
  alla repo producono lo stesso output a meno di `generated_at`.
- **8 pagine HTML statiche** — shell identiche, cambia solo `data-page`.
- **`app.js`** — unico file JS: legge `DASHBOARD_DATA` e renderizza via
  `innerHTML`. Zero framework, zero dipendenze, zero fetch (i dati arrivano
  via `<script>` così la dashboard funziona aprendo il file direttamente,
  dove `fetch()` su `file://` fallirebbe).
- **`style.css`** — palette canonica da `scripts/design_system.py`
  (carta/inchiostro Spirale + i tre venti come sistema di categorizzazione).

## Pagine

| Pagina | Cosa | Per chi |
|---|---|---|
| `index.html` | sistema, 3 fonti, TL;DR | umano nuovo + agente |
| `agent-entry.html` | sequenza di lettura d'ingresso + costo token cumulativo | Ray + orchestratore |
| `skills.html` | card dei ruoli dai frontmatter | umano + agente |
| `pipeline.html` | tappe del flusso storia (da docs/PIPELINE.md) | umano |
| `repo-map.html` | albero annotato (da docs/MAPPA_REPO.md) | umano + agente |
| `documenti.html` | .md di sistema classificati Core/Operativo/Progetto/Archivio, filtrabili | Ray |
| `todo.html` | voci aperte estratte + known_issues.yaml, filtrabili per tipo | Ray (operativo) |
| `make.html` | make help renderizzato | umano |

## Scelte di estrazione (build_dashboard.py)

- **mtime = git**, non filesystem (`git log -1 --format=%cI`).
- **Token stimati** a ~4 byte/token: indicazione grezza, serve per i
  confronti relativi, non per i valori assoluti.
- **Documenti esclusi** (contenuto, non meta): prosa, writing_briefs,
  narrazione_fattuale, `_annotations`, schede `visual/`, `web/`,
  `_visual_pipeline/_esempi` e `_templates`, `contributi/`.
- **Scansione TODO**: esclude anche `SYNC_LOG.md` (i ⚠️ sono cronaca) e
  `CHECKLIST.md` (checkbox operative by design). Le voci sono classificate
  per tipo — `todo` (TODO/FIXME espliciti), `warning` (⚠️), `checklist`
  (`- [ ]`), `sezione`/`voce` (header "TODO/Aperti/Da fare" + items) — e
  filtrabili in pagina, così la decisione su cosa è davvero debito resta
  a Ray. Word boundary su TODO (lezione: "ME**TODO** REVISIONE").
