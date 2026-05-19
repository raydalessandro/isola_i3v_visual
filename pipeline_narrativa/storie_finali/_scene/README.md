# `_scene/` — immagini-scena composte per pagina libro fisica

Cartella sorella di `_annotations/` e `_inventory/`. Contiene le **illustrazioni finali** che andranno nel libro stampato, una per pagina libro fisica.

## Naming deterministico

```
_scene/sNN/sNN_hMMx.jpg          ← LOW-RES reference (browsing digitale)
_scene/sNN/_hd/sNN_hMMx_hd.jpg   ← HD per stampa (JPG q95, ~1664×2496 px)
```

| Token | Significato | Range |
|---|---|---|
| `sNN` | id storia | `s01`..`s12` |
| `hMM` | id hook narrativo (1..10 zero-padded) | `h01`..`h10` |
| `x` | suffisso subhook = pagina libro fisica all'interno dell'hook | `a`, `b`, `c`, ... |
| `_hd` | suffisso versione HD stampa (presente SOLO nella subdir `_hd/`) | — |

Esempi:
- `s01/s01_h01b.jpg` — low-res reference, s01, hook 1, pagina libro 2
- `s01/_hd/s01_h01b_hd.jpg` — HD stampa stessa scena, JPG q95
- `s07/s07_h05a.jpg` + `s07/_hd/s07_h05a_hd.jpg` — coppia low-res + HD di s07 hook 5 subhook a

**Le due versioni convivono.** Il marker `@image` nel testo storia punta SEMPRE alla low-res (`_scene/sNN/sNN_hMMx.jpg`); lo script compositore libro (futuro) cerca prima `_hd/sNN_hMMx_hd.jpg` per la stampa, fallback su low-res se assente.

## Relazione con il marker `@subhook`

Una immagine `_scene/sNN/sNN_hMMx.jpg` corrisponde **1:1** al marker `@subhook` con id `sNN_hMMx` nel testo storia (`pipeline_narrativa/storie_finali/sNN_<slug>.md`).

Quando l'illustrazione è pronta, si popola il campo `@image` del marker:

```diff
- <!-- @subhook s01_h01b | @page_book 2 | @image TBD -->
+ <!-- @subhook s01_h01b | @page_book 2 | @image pipeline_narrativa/storie_finali/_scene/s01/s01_h01b.jpg -->
```

## NON sono reference catalogo

Le reference catalogo (faccia personaggio, esterno luogo, oggetto isolato) stanno in:

```
visual/<categoria>/<id>/immagini/<id>_canonica_v1_<vista>.jpg
```

Le `_scene/` sono il **prodotto finale composto** della scena nel libro. Pattern ortogonali, non confondere.

## Vincoli

- Naming **deterministico**: mai inventare suffissi diversi da `<sid>_<hook_id><subhook_letter>.jpg`.
- Una pagina libro = un file. Per **spread doppia**: stesso file referenziato da entrambi i subhook con `@layout: double_spread`.
- Mai modificare i `@subhook` id (stabili, legati al testo prosa + brief + prompt grok).
- Mai rinominare i file `_scene/` esistenti senza aggiornare il marker `@image` corrispondente.
- **Le HD vanno SEMPRE in `_hd/`, mai nella cartella padre.** Mai sostituire un low-res con la sua versione HD.
- **Formato HD:** JPEG qualità 95, RGB profilo sRGB, risoluzione minima 1664×2496 px (formato verticale).

## Stato (2026-05-05)

- 1/N immagini popolate: `s01/s01_h01b.jpg`
- Documentazione completa: vedi `pipeline_narrativa/storie_finali/README.md`
