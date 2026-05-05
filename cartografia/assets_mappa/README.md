# `cartografia/assets_mappa/`

Asset visivi della **Mappa dell'Isola** (vista navigabile in `catalogo_web/`,
route `#/mappa-isola`).

> **Distinguere**: questi NON sono gli asset del libro illustrato.
> Le illustrazioni del libro stanno in `visual/<famiglia>/<id>/immagini/`
> (4 viste canoniche generate con Grok per personaggi/luoghi).
>
> Quelli qui sono **asset 3D Travian-style** dedicati alla mappa:
> piccoli edifici/landmark in pseudo-3D vista dall'alto, sfondo trasparente,
> per essere sovrapposti all'illustrazione master dell'isola.

---

## Struttura

```
assets_mappa/
├── README.md                       ← questo file
├── _base/
│   └── isola_base_v1.jpg           ← illustrazione master dell'isola (acquerello, no edifici)
└── <id>.png                        ← un PNG 3D per ogni edificio/landmark
                                       (sfondo trasparente, ~200-400 px lato)
```

L'`<id>` deve corrispondere al `properties.id` della feature in
`cartografia/geo/island.geojson`. Esempi: `forno.png`, `albero_vecchio.png`,
`piazza_villaggio.png`, `casa_salvia.png`.

## Specs asset 3D (per Grok / Midjourney / FLUX)

- **Formato**: PNG con alpha (sfondo trasparente).
- **Dimensione**: lato lungo 200-400 px circa (Grok 1024 funziona, poi taglio
  con remove.bg o Photoshop).
- **Prospettiva**: vista isometrica dall'alto, angolo ~30-40° (Travian-style).
  *Non* vista frontale, *non* top-down piatto.
- **Stile**: coerente con l'illustrazione del libro (acquerello morbido +
  contorni a matita), ma 3D-ish. Riferimento mentale: edifici dei giochi
  isometrici classici (Travian, Anno, Settlers) con palette del nostro libro.
- **Composizione**: l'edificio è centrato, base appoggiata in basso. Niente
  ombra dipinta sotto (la aggiunge il CSS via `drop-shadow`).
- **Coerenza**: tutti gli edifici devono avere stessa "mano", stessa palette,
  stessa luce direzionale (sole alto da sud-est). Conviene tenere un prompt
  base e variare solo il soggetto.

### Prompt base suggerito per Grok (modificare il soggetto)

```
isometric 3D illustration of {soggetto}, watercolor style with pencil
outlines, 30-degree top-down angle, transparent background, soft natural
lighting from upper right, no ground shadow, children's picture book
aesthetic, single building isolated, palette earth tones with green accents,
4:5 aspect ratio
```

Esempio per `forno.png`:

```
{soggetto} = a small stone bakery with thatched roof, smoking chimney,
wooden door, warm bread visible in a window, mediterranean village style
```

## Workflow per aggiungere un nuovo asset

1. Scegli l'`<id>` della feature canonica nel geojson (es. `forno`).
2. Genera l'immagine con Grok (usa il prompt base + il soggetto specifico).
3. Rimuovi sfondo se necessario (remove.bg, Photoshop, GIMP).
4. Salva come `cartografia/assets_mappa/<id>.png`.
5. Commit + push. Vercel ridepoia. Refresh `/mappa-isola` → l'asset compare
   automaticamente al posto del placeholder, posizionato secondo il geojson.

Niente da modificare nel codice. Niente JSON di layout da aggiornare.

## Aggiornamento posizioni

Se un asset cade fuori posto sulla mappa, **non si modifica un layout JSON**:
si modifica direttamente il `cartografia/geo/island.geojson` cambiando le
coordinate della feature. Il viewer cartografico
(`cartografia/geo/viewer/`) e la mappa illustrata si aggiornano insieme,
da una sola fonte di verità.

Se invece sono molti gli edifici fuori posto **uniformemente** (es. tutti
spostati a sud-ovest), il problema è la calibrazione globale: si modifica
`MAPPA_CONFIG.bbox_geo` in `catalogo_web/mappa_isola.js` (4 numeri
lon_min/lon_max/lat_min/lat_max).

Per aiutarsi nella calibrazione: aprire `#/mappa-isola?debug` per vedere
griglia + bbox.

## Sostituzione base illustrazione master

Quando arriverà una nuova illustrazione dell'isola dall'alto, basta
sostituire `_base/isola_base_v1.jpg` con `_base/isola_base_v2.jpg` (o nome
nuovo) e aggiornare `MAPPA_CONFIG.base_image` in `mappa_isola.js`.

Se cambia la **proporzione** dell'immagine (oggi 1120x912), aggiornare anche
`image_w` e `image_h` in `MAPPA_CONFIG`. Se cambia l'**inquadratura** (più o
meno mare attorno), ricalibrare `bbox_geo`.

## Stato attuale (snapshot al primo deploy)

- `_base/isola_base_v1.jpg` — illustrazione master generata con Grok,
  aspect ratio 1120×912 (≈1.23:1). Acquerello, isola con due montagne a
  nord, fiume ad anello centrale, foresta a ovest, prato e radure a est,
  spiaggia a sud. **Non rappresenta urbanisticamente l'isola del geojson**:
  è la base estetica, gli edifici verranno sovrapposti come asset 3D.
- 0 asset 3D — tutti gli slot sono placeholder al primo deploy.

29 slot canonici disponibili nel geojson per essere popolati con asset 3D
(edifici, tane, grotte, landmark, piazze).
