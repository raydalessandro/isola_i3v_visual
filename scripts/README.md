# scripts/

Tool Python condivisi tra le skill `cartografo` e `visual`. Idempotenti: rieseguibili senza effetti collaterali su lavoro esistente.

## Indice

| Script | Scopo | Skill |
|---|---|---|
| `build_visual_skeleton.py` | Genera struttura `visual/` (cartelle frattali, schede stub, catalogo, indice strade) a partire da `pipeline_narrativa/story_graph.json` + `cartografia/geo/island.geojson`. Idempotente: rigenera frontmatter, preserva body. | visual |
| `build_catalogo_web.py` | Scansiona `visual/` ricorsivamente, parsa frontmatter YAML + body MD, raccoglie immagini, scrive `catalogo_web/data/entities.json` per il sito interno. Richiede `PyYAML`. | governance |

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
