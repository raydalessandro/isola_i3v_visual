# Volume 1 — Ciclo A (s01, s02, s03)

Risorse del **Volume 1** della saga (pubblicazione in 4 volumi × 3 storie = 12 storie totali).

Ciclo A = Inverno che cede alla primavera, Vento Taglio. Vedi `_volumi/introduzioni_cicli.md` per il testo narrativo dell'introduzione.

## Contenuto

```
v01/
└── _hd/                             ← illustrazioni HD per stampa intro Volume 1
    └── v01_intro_<slug>_hd.jpg      ← JPEG q95, RGB sRGB, ~1664×2496 px
```

## Naming

```
v01_intro_<slug>_hd.jpg
```

| Token | Significato |
|---|---|
| `v01` | id volume (`v01`..`v04`) |
| `intro` | sezione del volume — qui è l'introduzione (apre il libro, precede s01) |
| `<slug>` | slug del soggetto rappresentato: nome personaggio singolo (`fiamma`, `nodo`) o coppia umano-animale (`bartolo_toba`, `memolo_pun`) |
| `_hd` | suffisso versione HD stampa |

## Cosa sono queste illustrazioni

Sono illustrazioni **derivate** delle reference canoniche di catalogo, **rielaborate per l'introduzione del volume**. Compaiono nelle pagine di apertura prima della storia s01 (presentazione cast/relazioni del Ciclo A).

NON sostituiscono le reference catalogo (che restano in `visual/personaggi/individuali/<cat>/<id>/immagini/`). Sono produzioni autonome, agganciate al **volume**, non all'**entità**.

## Indice attuale

| File | Soggetto |
|---|---|
| `v01_intro_bambini_hd.jpg` | i 3 fratelli (Gabriel, Elias, Noah) insieme |
| `v01_intro_bartolo_toba_hd.jpg` | coppia umano-cucciolo: Bartolo (fornaio) + Toba |
| `v01_intro_bru_hd.jpg` | cucciolo Bru (compagno di Rovo) |
| `v01_intro_fiamma_hd.jpg` | Fiamma (panettiera) |
| `v01_intro_grunto_hd.jpg` | Grunto |
| `v01_intro_memolo_pun_hd.jpg` | coppia umano-cucciolo: Mèmolo + Pun |
| `v01_intro_nodo_hd.jpg` | Nodo |
| `v01_intro_pun_hd.jpg` | cucciolo Pun (compagno di Mèmolo) |
| `v01_intro_rovo_bru_hd.jpg` | coppia umano-cucciolo: Rovo + Bru |
| `v01_intro_salvia_hd.jpg` | Salvia |
| `v01_intro_stria_hd.jpg` | Stria |
| `v01_intro_zolla_hd.jpg` | Zolla |

L'**ordine di apparizione** nelle pagine di intro è decisione editoriale di Ray (non desumibile dal naming). Quando definito, va annotato qui o in un file YAML di mappatura `v01_intro_layout.yaml`.

## Pattern futuro (v02, v03, v04)

Stessa struttura per i volumi successivi:

```
_volumi/v02/_hd/v02_intro_<slug>_hd.jpg   ← Ciclo B (s04, s05, s06)
_volumi/v03/_hd/v03_intro_<slug>_hd.jpg   ← Ciclo C (s07, s08, s09)
_volumi/v04/_hd/v04_intro_<slug>_hd.jpg   ← Ciclo D (s10, s11, s12)
```

Altre sezioni di un volume (porte, congedo, sigilli, presentazioni parziali) hanno controparti testuali in `_volumi/*.md` — se in futuro avranno illustrazioni HD, vanno in `v0N/_hd/v0N_<sezione>_<slug>_hd.jpg` (es. `v01_porta_<slug>_hd.jpg`).

## Vincoli

- Formato HD: **JPEG q95**, RGB profilo **sRGB**, min **1664×2496 px** (verticale).
- Naming **deterministico**: solo lowercase, snake_case, slug univoco.
- Mai cambiare slug di file esistenti senza aggiornare l'indice qui sopra.
- Aggiunte: ADD-only, mai sostituire/sovrascrivere file canonici.
