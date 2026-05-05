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

### 3. 10 sezioni hook narrativo con marker machine-readable

Ogni `## Pagina N` corrisponde a **un hook narrativo** (1..10), che a sua volta si scompone in **uno o più subhook = pagine libro fisiche** (1..book_pages_total).

```markdown
## Pagina N

<!-- @hook sNN_hMM | @page MM | @subhooks [sNN_hMMa, sNN_hMMb] | @image TBD -->

<!-- @subhook sNN_hMMa | @page_book K | @image TBD -->
[testo prosa della prima pagina libro associata a questo hook]

<!-- @subhook sNN_hMMb | @page_book K+1 | @image pipeline_narrativa/storie_finali/_scene/sNN/sNN_hMMb.jpg -->
[testo prosa della seconda pagina libro associata a questo hook]

---
```

**Marker @hook (parent):**

| Campo | Significato | Esempio |
|---|---|---|
| `@hook` | id univoco hook narrativo (formato: `sNN_hMM`, MM = 01..10 zero-padded) | `s01_h01` |
| `@page` | numero hook (1..10) — **non è la pagina libro fisica** | `1` |
| `@subhooks` | lista sotto-hook (1+ subhook = 1+ pagina libro fisica) | `[s01_h01a, s01_h01b]` |
| `@image` | (legacy) path immagine composta libro a livello hook. `TBD` da popolare | `TBD` |

**Marker @subhook (figli, uno per pagina libro fisica):**

| Campo | Significato | Esempio |
|---|---|---|
| `@subhook` | id sotto-hook (formato: `sNN_hMMx`, x ∈ {a, b, c, ...}) | `s01_h01b` |
| `@page_book` | numero pagina libro fisica (1..book_pages_total). Per spread doppia: `[N, N+1]` | `2` |
| `@layout` | (opz.) `double_spread` per immagini che attraversano 2 pagine fisiche | — |
| `@image` | path immagine-scena composta della pagina (vedi `_scene/` sotto). `TBD` finché non popolato. | `pipeline_narrativa/storie_finali/_scene/s01/s01_h01b.jpg` |

## Cartelle gemelle (parallele ai 12 file storia)

| Cartella | Contenuto | Pattern |
|---|---|---|
| `_annotations/` | YAML autoriali Ray (es. `s01.yaml`) — note di scena, decisioni autoriali | `_annotations/sNN.yaml` |
| `_inventory/` | inventari testuali derivati (per audit/QA prosa) | `_inventory/sNN_*.{md,yaml}` |
| `_scene/` | **immagini-scena composte** (illustrazione singola pagina libro), referenziate dal marker `@subhook ... @image` | `_scene/sNN/sNN_hMMx.jpg` |
| `_volumi/` | **cornice editoriale dei 4 volumi** (Soglia / Introduzione / Stato Zero / Presentazione / Porte / Sigilli / Congedo). Marker `## VOLUME N` interni per il compositore libro | `_volumi/<sezione>.md` |

### `_scene/` — pattern in dettaglio

Una pagina libro fisica = un subhook (`sNN_hMMx`) = un'immagine-scena. Quando arriva l'illustrazione composta dal generatore (oggi: Grok Imagine), va in:

```
pipeline_narrativa/storie_finali/_scene/sNN/sNN_hMMx.jpg
```

esempi:
- `_scene/s01/s01_h01b.jpg` — Fiamma consegna pagnotta a Gabriel (s01, hook 1, subhook b, page_book 2)
- `_scene/s01/s01_h05a.jpg` — (futuro) prima pagina libro associata all'hook 5 di s01

E si aggiorna **solo** il marker `@image` del corrispondente `@subhook` nel testo storia, da `TBD` al path:

```diff
- <!-- @subhook s01_h01b | @page_book 2 | @image TBD -->
+ <!-- @subhook s01_h01b | @page_book 2 | @image pipeline_narrativa/storie_finali/_scene/s01/s01_h01b.jpg -->
```

Vincoli:
- Naming **deterministico**: `<sid>_<hook_id><subhook_letter>.jpg`. Mai inventare suffissi.
- Una scena = una immagine. Per spread doppia: stesso file referenziato da entrambi i subhook con `@layout: double_spread`.
- Mai modificare gli `@subhook` id (stabili, legati al testo prosa).
- Le immagini-scena NON sono reference catalogo — quelle stanno in `visual/<categoria>/<id>/immagini/<id>_canonica_v1_<vista>.jpg` (vedi `_visual_pipeline/`). Le `_scene/` sono il **prodotto finale composto** per il libro.

## Workflow per script futuri

### Compositore libro finale (futuro)

Lo script che assembla il libro finale può:

1. Leggere il frontmatter per metadati globali (sid, titolo, ciclo, `book_pages_total`, ecc.)
2. Iterare sulle 10 sezioni `## Pagina N` (hook narrativi)
3. Per ogni hook, iterare sui marker `@subhook` interni (1+ per hook = pagine libro fisiche)
4. Per ogni subhook parsare `<!-- @subhook ... | @page_book ... | @image ... -->` per ottenere:
   - L'id subhook → cerca eventuale prompt grok / scena in `_scene/sNN/sNN_hMMx.jpg`
   - Il path immagine-scena → se `TBD`, fallback su placeholder o segnalazione
   - Il numero pagina libro fisica (`@page_book`) → posizione nel libro finale
5. Estrarre il testo prosa puro per ogni subhook (testo tra il marker `@subhook` e il successivo marker o `---`)
6. Comporre PDF/EPUB/HTML del libro finale rispettando l'ordine `@page_book`

### Esempio parsing in Python

```python
import re
import yaml
from pathlib import Path

def parse_storia(path: Path):
    content = path.read_text(encoding="utf-8")

    # 1. Frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.S)
    metadata = yaml.safe_load(fm_match.group(1)) if fm_match else {}

    body = content[fm_match.end():] if fm_match else content

    # 2. Hook narrativi (## Pagina N + @hook)
    HOOK_RE = re.compile(
        r"^## Pagina (\d+)\s*\n+"
        r"<!-- @hook (\S+) \| @page (\d+) \| @subhooks \[(.*?)\] \| @image (\S+) -->",
        re.M
    )
    SUB_RE = re.compile(
        r"<!-- @subhook (\S+) \| @page_book (\S+)(?: \| @layout (\S+))? \| @image (\S+) -->\s*\n+(.*?)(?=<!-- @subhook|\Z)",
        re.S
    )

    hooks = []
    hook_matches = list(HOOK_RE.finditer(body))
    for i, m in enumerate(hook_matches):
        start = m.end()
        end = hook_matches[i + 1].start() if i + 1 < len(hook_matches) else len(body)
        hook_body = body[start:end]
        subhooks = []
        for s in SUB_RE.finditer(hook_body):
            subhooks.append({
                "subhook_id": s.group(1),
                "page_book": s.group(2),
                "layout": s.group(3),
                "image": s.group(4),
                "text": s.group(5).strip().rstrip("-").strip(),
            })
        hooks.append({
            "page_num": int(m.group(1)),
            "hook_id": m.group(2),
            "subhooks_decl": [x.strip() for x in m.group(4).split(",") if x.strip()],
            "subhooks": subhooks,
        })

    return {"meta": metadata, "hooks": hooks}
```

### Compositore immagine pagina libro (futuro)

Per generare l'immagine-scena composta di una pagina libro fisica (subhook):

1. Trova il prompt scena (es. derivabile da hook + brief) per generare l'illustrazione se non c'è
2. Genera con generatore immagini (oggi: Grok Imagine, Ray) usando reference canoniche da `visual/<categoria>/<id>/immagini/<id>_canonica_v1_*.jpg`
3. Salva il file con naming deterministico in `pipeline_narrativa/storie_finali/_scene/sNN/sNN_hMMx.jpg`
4. Aggiorna il marker `@subhook ... @image` da `TBD` al path effettivo
5. (Futuro) Layout testo overlay + grafica → file finale di stampa

## Vincoli

- **NON modificare il testo prosa** se non per correzioni autoriali esplicite di Ray.
- **NON modificare il frontmatter** se non per aggiornare `ultima_modifica` o `status` o `book_pages_total` (se cambia la scomposizione).
- **NON modificare gli `@hook` né `@subhook` id**: sono stabili, legati a brief / prompt grok / `_scene/` / pipeline composizione.
- **Il marker `@image`** (sia `@hook` che `@subhook`) può essere aggiornato da `TBD` al path reale quando l'immagine è pronta.
- **`@subhooks` `[]` vuoti** sono ammessi solo per hook non ancora scomposti in pagine libro.
- **File `_scene/`** seguono naming deterministico `sNN_hMMx.jpg` — mai inventare suffissi.

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
