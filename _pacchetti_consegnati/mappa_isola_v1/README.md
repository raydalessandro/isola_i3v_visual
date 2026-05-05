# Pacchetto `mappa_isola_v1` — integrato 2026-05-05

Archivio del pacchetto consegnato da Ray come `pacchetto_mappa_isola_v1.zip` + `INTEGRATION.md` (caricati su main 2026-05-05).

## Cosa è stato integrato

Nuova route `#/mappa-isola` nel `catalogo_web/` che mostra la mappa illustrata navigabile dell'isola (vista dall'alto in stile acquerello) con slot interattivi posizionati dai centroidi del geojson. Ogni slot è cliccabile e naviga alla scheda dell'entità (`#/entity/<id>`).

**Asset 3D progressivi:** ogni slot mostra un placeholder finché non viene generato il PNG corrispondente in `cartografia/assets_mappa/<id>.png` (workflow Grok lato Ray, specs in `cartografia/assets_mappa/README.md`). Al primo deploy, **30 slot** dal geojson, tutti placeholder.

## File modificati / creati

```
catalogo_web/index.html       MOD (3 righe)   — link CSS + link sidebar + script tag
catalogo_web/app.js           MOD (9 righe)   — blocco router #/mappa-isola
catalogo_web/mappa_isola.js   NEW (~280 righe) — modulo isolato, expose window.renderMappaIsola()
catalogo_web/mappa_isola.css  NEW (~140 righe) — stili dedicati
cartografia/assets_mappa/
  ├── README.md               NEW             — specs Grok per asset 3D
  └── _base/
      └── isola_base_v1.jpg   NEW (~150 KB)   — illustrazione master
vercel.json                   MERGED          — settings cleanUrls/trailingSlash dal pacchetto + headers data/visual/js/css esistenti + headers nuovi geojson/assets_mappa
```

## Decisione di merge `vercel.json`

Esistente aveva header per `catalogo_web/data`, `visual/`, `.js`, `.css` (cache control). Pacchetto aggiunge header per `cartografia/geo/*.geojson` (Content-Type + CORS) e `cartografia/assets_mappa/*.png` + `_base/`.

**Risolto:** merge che conserva tutti gli header esistenti + tutti quelli nuovi. Adottati i settings nuovi `cleanUrls: true` + `trailingSlash: false` (modern Vercel, coerenti con il pacchetto testato). Redirect `/` → `/catalogo_web/` invariato.

## Smoke test eseguiti

- `vercel.json` — JSON valido ✓
- `mappa_isola.js`, `app.js` — `node --check` syntax OK ✓
- 30 slot dal geojson (8 tipi: building/burrow/cave/pier/landmark/water_pool/tree/square) ✓
- Server locale `python3 -m http.server` — index.html, mappa_isola.{js,css}, isola_base_v1.jpg, island.geojson tutti rispondono 200 ✓

## Calibrazione iniziale + anomalie attese

**Non bloccanti per il deploy** (vedi `INTEGRATION.md` §5):

1. **Cluster villaggio sovrapposto** — Piazza, Albero Vecchio, Pozzo, Forno, Casa Mèmolo ecc. hanno coordinate geojson entro un raggio ~50 m → si sovrappongono in pochi pixel sull'immagine 1120×912. Risolvibile spostando coordinate (cartografia) o introducendo zoom-villaggio in V2.
2. **Case Basse + Capanna Bartolo + Casa Amo cadono nel mare a sud** — coordinate a lat ~34.476 ma l'isola dipinta finisce prima a sud. Risolvibile spostando le coordinate dentro la spiaggia dipinta.

Entrambe visibili attivando `?debug` (griglia rossa ogni 100 px).

## Workflow post-deploy (per Ray)

Aggiungere un asset 3D:
1. Genera PNG con Grok (specs in `cartografia/assets_mappa/README.md`)
2. Salva in `cartografia/assets_mappa/<id>.png` (case-sensitive, snake_case)
3. Commit + push → al deploy successivo lo slot mostra l'asset al posto del placeholder

Spostare un edificio:
- Modifica `geometry.coordinates` della feature in `cartografia/geo/island.geojson`. Cambia su entrambi: mappa illustrata + viewer cartografico.

## Non-obiettivi V1

- Personaggi sulla mappa (rinviati)
- Animazioni / micro-storie (rinviate)
- Editor visuale drag&drop (out of scope)
- Generazione automatica asset 3D (Ray fa con Grok)
- Mini-mappa per ogni storia (V2, leggendo `appare_in_storie` da `entities.json`)
- Filtri sidebar (nella V1 si vedono tutti gli slot)

## Trail commit

| Commit | Cosa |
|---|---|
| (questo) | Integrazione completa + archivio pacchetto |

## Origine

Pacchetto consegnato da Ray il 2026-05-05. Originale `pacchetto_mappa_isola_v1.zip` non conservato (file binari ridondanti — la repo contiene già tutti i file finali). `INTEGRATION.md` originale conservato qui come trail. `preview_calibrazione_v1.jpg` (preview di smoke-test del pacchetto stesso) conservata qui.
