# scripts/

Tool Python condivisi tra le skill `cartografo` e `visual`. Idempotenti: rieseguibili senza effetti collaterali su lavoro esistente.

## Indice

| Script | Scopo | Skill |
|---|---|---|
| `build_visual_skeleton.py` | Genera struttura `visual/` (cartelle frattali, schede stub, catalogo) a partire da `pipeline_narrativa/story_graph.json` + `cartografia/geo/island.geojson`. **Non sovrascrive** schede esistenti. | visual |

## Principi

- **Idempotenza:** ogni script si può rilanciare senza danni.
- **Letture:** consentite ovunque (incluso `pipeline_narrativa/` read-only).
- **Scritture:** ogni script dichiara in testa quali directory tocca.
- **Niente segreti:** mai credenziali o token nei file di questa cartella.
- **Aggiunte future:** quando uno script diventa stabile, citarlo nelle skill (`skills/cartografo.md`, `skills/visual.md`) come metodo uniformante.

## Uso tipico

```bash
# Dalla radice del repo
python3 scripts/build_visual_skeleton.py
```
