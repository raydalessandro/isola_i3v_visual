# TODO — Spread orizzontale per s01_h07 (sessione dedicata `build_volume.py`)

**Stato:** in attesa — sessione dedicata Ray + Claude · registrato 2026-06-14 · branch `claude/illustratore-s01-hd-refresh`

## Contesto

L'illustratore (Manus) ha rifatto le scene di s01 con stile coerente al resto. Per **s01_h07** (originariamente 1 sola immagine verticale `s01_h07a` con testo nella pagina) ha consegnato una composizione diversa: **un'immagine orizzontale 2560×1440** pensata come **spread doppia pagina**:

- **Pagina sinistra**: paesaggio della cengia (zona quieta → ospita il testo)
- **Pagina destra**: i tre bambini sulla cengia (zona piena, niente testo)

Il file landscape è in:

```
pipeline_narrativa/storie_finali/_scene/s01/_pending/s01_h07_spread_landscape.jpg   (2560×1440)
```

Non è stato collocato in `_hd/` perché `scripts/build_volume.py` **non sa ancora gestire** uno spread con immagine landscape divisa su 2 pagine. Il vecchio HD verticale `s01_h07a_hd.jpg` (524 KB, verticale) **resta in `_hd/`** come fallback finché lo script non viene esteso — Vol 1 continua a buildare regolarmente.

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
