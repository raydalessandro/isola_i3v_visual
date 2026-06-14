# TODO — Spread orizzontali (sessione dedicata `build_volume.py`)

**Stato:** ✅ RISOLTO — 2026-06-14, sessione Ray + Claude.

## Esito (decisione presa)

Adottata di fatto una via che combina A e B: **1 sola immagine landscape sorgente**
(semantica chiara "è uno spread") che lo script **taglia a metà** in **2 facciate A5
indipendenti** per la stampa (KDP-friendly, nessun problema di bleed sul taglio centrale).

Implementazione in `scripts/build_volume.py`:
- `compose_spread_horizontal()` — cover-fit del landscape su canvas continuo
  `(IMG_W*2 + gutter) × IMG_H`, **testo solo sulla pagina sinistra** (riusa
  `_overlay_text`, helper estratto da `compose_story_page`).
- `build_story_pages()` instrada i subhook `@layout double_spread` (o con
  `@page_book [N, N+1]`) alla nuova funzione.
- `build_stampa_pdf` (già esistente) taglia lo spread a `width//2` → 2 pagine A5.
- `build_spread_pdf` (già esistente) lo rende come doppia pagina continua (digitale).
- `_facciate`/`ensure_recto` (già esistenti) contano lo spread come 2 facciate.
- **Bugfix regex parser**: `@page_book [N, N+1]` con lo spazio ora viene riconosciuto
  (prima `s02_h05a` veniva silenziosamente saltato → s02 si montava senza h05).
- Banner "sotto spec" attivo: i landscape attuali sono a bassa risoluzione per il
  full-bleed A5 (s01 2560×1440, s02 1672×941) → da rigenerare ≥3328×2496 per la stampa
  finale (si lega ai 4 miglioramenti standard generazione).
- Test: `tests/test_spread_horizontal.py` (parser, dimensioni, split, facciate, testo-sx).

Marker aggiornati: `s01_h07a` e `s02_h05a` → `@layout double_spread` + `@image` al
landscape. Annotation `_annotations/s01.yaml`, `s02.yaml` allineate.

---

## (storico) Contesto originale

L'illustratore (Manus) sta consegnando alcune scene come **immagini orizzontali** pensate per **spread doppia pagina** invece che come singola pagina verticale. Casi attuali:

| Storia | Subhook | File | Dimensioni | Contenuto |
|---|---|---|---|---|
| s01 | h07 (era h07a) | `_scene/s01/_pending/s01_h07_spread_landscape.jpg` | 2560×1440 | paesaggio cengia (sx) + tre bambini sulla cengia (dx) |
| s02 | h05 (era h05a) | `_scene/s02/_pending/s02_h05_spread_landscape.jpg` | 1672×941 | scena spread Vol 2 |

In entrambi i casi:
- Il vecchio HD verticale resta in `_hd/` (Vol continua a buildare regolarmente)
- L'immagine landscape sta in `_pending/` in attesa che lo script sappia gestirla

## Da decidere (decisione editoriale + tecnica)

### Opzione A — 1 immagine sola che diventa 2 pagine

Lo script taglia in 2 al volo durante il render:
- Half sinistra (0..1280 px) → pagina sinistra full-bleed
- Half destra (1280..2560 px) → pagina destra full-bleed
- Testo sovrapposto sulla sinistra (zona quieta paesaggio)

**Pro**: 1 sorgente, semantica chiara ("è uno spread"). **Contro**: KDP potrebbe non accettare l'immagine spread come singolo file PDF (verificare le specifiche bleed/safe area sul taglio centrale).

### Opzione B — 2 immagini affiancate come 2 file separati

Pre-tagliata in fase di consegna o nello script:
- `s01_h07a_hd.jpg` (verticale, 1280×1440 con eventuale upscaling a min HD)
- `s01_h07b_hd.jpg` (verticale)
- Lo script le piazza una accanto all'altra come pagine consecutive (pari + dispari)

**Pro**: KDP-friendly (gestisce 2 pagine indipendenti). **Contro**: il taglio è "vetro" e Manus potrebbe perdere un po' di pixel centrali se la composizione lo prevede ai bordi.

### Opzione C (più sicura per ora) — pensata da Ray

Verificare cosa fa KDP con immagini double-page-spread:
- Pagine al vivo (con bleed): KDP unisce le 2 pagine in un file PDF di 296×210 mm?
- Oppure tratta sempre 2 file PDF distinti a 148×210 mm ciascuno?

→ Specifiche KDP da consultare prima di decidere.

## Cosa serve nello script

In `scripts/build_volume.py`:

1. **Riconoscere il marker `@subhook`** che indica spread orizzontale (forse `@layout double_spread` già esistente — verificare uso in `_annotations/s01.yaml` per s01_h07).
2. **Funzione `make_subhook_spread_horizontal()`**: prende l'immagine landscape, la splitta logicamente in 2 mezzi, mantiene il bleed sui bordi esterni, e produce 2 facciate PDF affiancate.
3. **Sovrapposizione testo solo sulla pagina sinistra** (riusa `_scegli_fascia_v2` per la zona quieta del paesaggio).
4. **Test in `tests/test_atlante.py`** o nuovo `test_spread_h07.py`:
   - dimensioni post-split
   - parità facciate (lo spread aggiunge 2 facciate, non 1: ricalcolare `_facciate()`)
   - testo sovrapposto solo sulla pagina sinistra
5. **Aggiornare `_annotations/s01.yaml`** per s01_h07 con metadati spread (es. `layout: spread_horizontal`, `image_path: _pending/s01_h07_spread_landscape.jpg`).

## Quando si fa

Sessione dedicata Ray + Claude, una volta che Ray decide A vs B vs C dopo verifica KDP. Per ora `_pending/` mantiene il file pronto da spostare in `_hd/` (o splittato in 2 file) appena lo script saprà gestirlo.

## Riferimenti

- Branch `claude/hd-storia-s01` (illustratore originale, 16 HD + 1 landscape)
- Branch `claude/illustratore-s01-hd-refresh` (questa: 15 HD applicate + landscape in `_pending/`)
- Skill scenografo v1.1 PR #26 (scene consistency block)
- Pattern spread doppia isola di PR #30 (`make_isola_doppia` — utile come riferimento per fascia quieta + amalgama colori dall'immagine)
