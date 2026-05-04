# pipeline_narrativa/storie_finali/

Testi prosa **finiti e definitivi** delle 12 storie del libro "L'Isola dei Tre Venti".

## Struttura

Ogni file:
```
sNN_<slug>.md           es. s01_la_nebbia_delle_montagne_gemelle.md
```

dove `NN ∈ {01..12}` e `slug` è il titolo della storia in minuscolo con underscore.

## Schema canonico per script futuri

Ogni file ha:

### 1. Frontmatter YAML

```yaml
---
sid: s01
title: La Nebbia delle Montagne Gemelle
slug: la_nebbia_delle_montagne_gemelle
cycle: A                     # A, B, C o D (cicli saga di 3 storie)
total_pages: 10              # sempre 10 (canone saga: 10 pagine = 10 hook visivi)
total_hooks: 10
status: definitiva
ultima_modifica: 2026-05-04
fonti:
  - pipeline_narrativa/narrazione_fattuale/{sid}_*.md
  - pipeline_narrativa/writing_briefs/{sid}_writing_brief.md
  - pipeline_narrativa/story_graph.json#stories.{sid}
schema_marker: |
  [descrizione del marker hook, vedi sotto]
---
```

### 2. Titolo H1

```markdown
# S01 — La Nebbia delle Montagne Gemelle
```

### 3. 10 sezioni pagina con marker machine-readable

Ogni pagina ha:

```markdown
## Pagina N

<!-- @hook sNN_hMM | @page MM | @subhooks [] | @image TBD -->

[testo prosa della pagina N, in voce autoriale finale]

---
```

dove:

| Campo | Significato | Esempio |
|---|---|---|
| `@hook` | id univoco dell'hook visivo della pagina (formato: `sNN_hMM`, MM = 01..10 zero-padded) | `s01_h01` |
| `@page` | numero pagina libro (1..10) | `1` |
| `@subhooks` | lista (vuota inizialmente) per future scomposizioni della pagina (es. testo + immagine in più tipi/varianti) | `[]` o `[s01_h01a, s01_h01b]` |
| `@image` | path dell'immagine **composta finale** del libro (testo + grafica già montati). `TBD` finché non popolato. | `pipeline_narrativa/composizioni/s01_h01.jpg` |

## Workflow per script futuri

### Compositore libro finale (futuro)

Lo script che assembla il libro finale può:

1. Leggere il frontmatter per metadati globali (sid, titolo, ciclo, ecc.)
2. Iterare sulle 10 sezioni `## Pagina N`
3. Per ogni pagina, parsare il commento `<!-- @hook ... | @image ... -->` per ottenere:
   - L'id hook → cerca prompt grok corrispondente in `visual/luoghi/.../prompt_grok.md` o equivalente
   - Il path immagine composta → se `TBD`, fallback su placeholder o segnalazione
4. Estrarre il testo prosa puro (rimuovendo titolo H1, frontmatter, marker, separator `---`)
5. Comporre PDF/EPUB/HTML del libro finale

### Esempio parsing in Python

```python
import re
import yaml

def parse_storia(path):
    content = path.read_text(encoding="utf-8")

    # 1. Frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.S)
    metadata = yaml.safe_load(fm_match.group(1)) if fm_match else {}

    # 2. Pagine
    body = content[fm_match.end():] if fm_match else content
    pages = []
    for page_match in re.finditer(
        r"^## Pagina (\d+)\s*\n+<!-- @hook (\S+) \| @page (\d+) \| @subhooks (\[.*?\]) \| @image (\S+) -->\s*\n+(.*?)(?=^## Pagina|\Z)",
        body, re.M | re.S
    ):
        pages.append({
            "page_num": int(page_match.group(1)),
            "hook_id": page_match.group(2),
            "subhooks": page_match.group(4),
            "image": page_match.group(5),
            "text": page_match.group(6).strip().rstrip("---").strip(),
        })

    return {"meta": metadata, "pages": pages}
```

### Compositore immagine pagina (futuro)

Per generare l'immagine composta finale di una pagina (testo overlay + immagine):

1. Trova il prompt grok dell'hook (es. `visual/.../prompt_grok.md`) per generare l'immagine se non c'è
2. Genera o pesca l'immagine canonica della scena
3. Layouta il testo della pagina come overlay (font, margini, dimensioni concordate)
4. Salva in `pipeline_narrativa/composizioni/sNN_hMM.jpg`
5. Aggiorna il marker `@image` da `TBD` al path effettivo

## Sotto-hook (futuro)

Alcune pagine potrebbero avere bisogno di **sotto-hook** (es. doppia spread con due immagini, o variante stagionale). Pattern:

```markdown
<!-- @hook s01_h05 | @page 5 | @subhooks [s01_h05a, s01_h05b] | @image TBD -->
```

Quando arrivano i sotto-hook, lo script di splitting/composizione li gestisce in pipeline.

## Vincoli

- **NON modificare il testo prosa** se non per correzioni autoriali esplicite di Ray.
- **NON modificare il frontmatter** se non per aggiornare `ultima_modifica` o `status`.
- **NON modificare gli `@hook` id**: sono stabili e legati ai prompt grok / pipeline composizione.
- **Il marker `@image`** può essere aggiornato da `TBD` al path reale quando l'immagine composta è pronta.
- **`@subhooks` vuoti** vanno lasciati `[]` finché non si decide di scomporre.

## Storie (12)

| sid | Ciclo | Titolo | Stato |
|---|---|---|---|
| s01 | A | La Nebbia delle Montagne Gemelle | definitiva |
| s02 | A | Il Riflesso nella Pozza | definitiva |
| s03 | A | Il Pallone oltre la Foresta | definitiva |
| s04 | B | Le Radici che Parlano | definitiva |
| s05 | B | Il Ponte di Rami | definitiva |
| s06 | B | Il Dono per Mèmolo | definitiva |
| s07 | C | La Zattera dei Tre Rametti | definitiva |
| s08 | C | L'Albero che Cadde di Sera | definitiva |
| s09 | C | Quel Pomeriggio di Ottobre | definitiva |
| s10 | D | La Notte senza Luna | definitiva |
| s11 | D | La Festa del Raccolto | definitiva |
| s12 | D | Quando i Tre Venti Suonano Insieme | definitiva |
