# Volume 1 — Ciclo A (s01, s02, s03)

Risorse del **Volume 1** della saga (pubblicazione in 4 volumi × 3 storie = 12 storie totali).

Ciclo A = Inverno che cede alla primavera, Vento Taglio. Vedi `_volumi/introduzioni_cicli.md` per il testo narrativo dell'introduzione.

## Contenuto

```
v01/
└── _hd/                             ← illustrazioni HD specifiche del volume
    └── v01_intro_<slug>_hd.jpg      ← solo file PRODOTTI per il volume (non reference)
```

## Cosa NON sta più qui (decisione 2026-06-10)

I ritratti dei personaggi sono **reference saga riusabili**, non illustrazioni specifiche del volume. Sono stati promossi al catalogo personaggi (`visual/personaggi/individuali/<cat>/<id>/immagini/`) il 2026-06-10 — sia singoli che coppie che collettivi (i 3 fratelli sotto Gabriel).

Regola operativa: **in `_volumi/v0N/_hd/` mettere SOLO le illustrazioni prodotte per il volume e non riusabili come reference saga** (es. composizioni narrative dell'intro che non sono semplici ritratti, decori di sezione, sigilli). Tutti i ritratti — anche se realizzati durante la lavorazione di un volume — vanno al catalogo personaggi.

Vedi `skills/illustratore/SKILL.md` per il processo di classificazione corretto a monte.

## Indice attuale

| File | Soggetto | Stato |
|---|---|---|
| `v01_intro_stria_hd.jpg` | Stria (in volo) | **HOLD** — Ray cerca versione HD non-volante prima di promuoverla a `stria_canonica_v1_ritratto.jpg` |

## Pattern futuro (v02, v03, v04)

Stessa logica: solo illustrazioni prodotte appositamente per il volume e non riusabili come reference. Tutti i ritratti vanno al catalogo personaggi anche se prodotti durante la lavorazione del volume.

```
_volumi/v02/_hd/v02_intro_<slug>_hd.jpg   ← Ciclo B (s04, s05, s06)
_volumi/v03/_hd/v03_intro_<slug>_hd.jpg   ← Ciclo C (s07, s08, s09)
_volumi/v04/_hd/v04_intro_<slug>_hd.jpg   ← Ciclo D (s10, s11, s12)
```

## Compositore libro

Lo script `scripts/build_volume.py` legge le reference personaggio per la sezione "presentazione cast" del volume direttamente dal catalogo (`visual/.../<id>/immagini/<id>_canonica_v1_<vista>.jpg`), preferendo automaticamente la variante HD da `_hd/` quando disponibile.

Per Stria (HOLD) il compositore continua a usare `_volumi/v01/_hd/v01_intro_stria_hd.jpg` come fallback finché non arriva la versione non-volante nel catalogo.
