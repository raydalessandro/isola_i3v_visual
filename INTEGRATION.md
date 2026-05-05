# Pacchetto integrazione — Mappa dell'Isola (v1)

**Data:** 2026-05-05
**Autore:** Claude (chat Ray)
**Branch suggerito:** `claude/mappa-isola-v1`
**Target deploy:** Vercel

---

## 1. COSA FA QUESTO PACCHETTO

Aggiunge al `catalogo_web/` una nuova route **`#/mappa-isola`** che mostra
una mappa illustrata navigabile dell'isola, con:

- **Sfondo**: l'illustrazione master in stile acquerello dell'isola
  (vista dall'alto leggermente inclinata, no edifici).
- **Slot interattivi**: per ogni edificio/landmark canonico definito in
  `cartografia/geo/island.geojson`, viene mostrato uno slot cliccabile
  posizionato sul centroide della feature.
- **Asset 3D progressivi (Travian-style)**: se in
  `cartografia/assets_mappa/<id>.png` esiste un asset 3D dell'edificio
  con quel `<id>`, viene sovrapposto allo slot. Altrimenti viene
  mostrato un placeholder (cerchio tratteggiato + nome).
- **Click su slot** → naviga alla scheda dell'entità (`#/entity/<id>`).

29 slot canonici sono disponibili (building, burrow, cave, pier,
landmark, water_pool, tree, square). Al primo deploy nessuno ha asset 3D:
tutti sono placeholder. Ray genererà gli asset uno alla volta con Grok
(specs in `cartografia/assets_mappa/README.md`) e ogni nuovo PNG
committato apparirà automaticamente al deploy successivo.

---

## 2. COSA C'È NEL PACCHETTO (file per file)

```
pacchetto_mappa_isola/
├── INTEGRATION.md                                    ← questo file
├── vercel.json                                       ← NUOVO (root repo)
├── catalogo_web/
│   ├── index.html                                    ← MODIFICATO (3 righe)
│   ├── app.js                                        ← MODIFICATO (9 righe)
│   ├── mappa_isola.js                                ← NUOVO
│   └── mappa_isola.css                               ← NUOVO
└── cartografia/
    └── assets_mappa/
        ├── README.md                                 ← NUOVO
        └── _base/
            └── isola_base_v1.jpg                     ← NUOVO (~150 KB)
```

### Dettaglio modifiche

**`catalogo_web/index.html`** — 3 righe aggiunte, 0 rimosse:
1. `<link rel="stylesheet" href="mappa_isola.css">` (riga 9)
2. `<a href="#/mappa-isola">Mappa dell'isola</a>` (riga 46, primo link
   sidebar footer)
3. `<script src="mappa_isola.js"></script>` (riga 76, prima di app.js)

**`catalogo_web/app.js`** — 9 righe aggiunte (un blocco nel router),
0 rimosse:
- All'interno di `function route()`, dopo il check di `#/storie`,
  aggiunto un blocco `if` che gestisce `#/mappa-isola` (anche con
  query string come `?debug`).

**`catalogo_web/mappa_isola.js`** — file nuovo, ~280 righe.
- Modulo isolato, espone `window.renderMappaIsola()`.
- Carica `cartografia/geo/island.geojson` al primo accesso (cached).
- Estrae le feature di tipo slot (building/burrow/cave/pier/landmark/
  water_pool/tree/square), calcola il centroide di ognuna, lo
  riproietta da lon/lat al viewBox SVG.
- Per ogni slot fa una `HEAD` su `cartografia/assets_mappa/<id>.png`
  per decidere se mostrare l'asset 3D o il placeholder.
- Renderizza un grosso `<svg>` con `<image>` di sfondo + `<g>` di slot.

**`catalogo_web/mappa_isola.css`** — file nuovo, ~140 righe.
- Stili dedicati alla pagina mappa (header, stage, slot, label,
  hover, debug, responsive). Nessuna interferenza con `style.css`.

**`cartografia/assets_mappa/README.md`** — file nuovo.
- Specs operative per generare asset 3D con Grok (prompt base,
  formato, risoluzione, prospettiva, naming).

**`cartografia/assets_mappa/_base/isola_base_v1.jpg`** — file nuovo.
- Illustrazione master dell'isola (1120×912, ~150 KB).

**`vercel.json`** — file nuovo, in root repo.
- Configura Vercel per deploy statico.
- Redirect `/` → `/catalogo_web/` (il sito è il catalogo web).
- Headers corretti per `.geojson` e cache `assets_mappa/`.

---

## 3. COME INTEGRARE (procedura per Claude Code)

```bash
# 0. dalla root della repo
cd /path/to/isola_i3v_visual

# 1. branch dedicato
git checkout -b claude/mappa-isola-v1

# 2. copia file dal pacchetto (assumendo lo zip estratto in /tmp/pacchetto_mappa_isola/)
PKG=/tmp/pacchetto_mappa_isola

# file modificati (sovrascrivono quelli esistenti)
cp $PKG/catalogo_web/index.html  catalogo_web/index.html
cp $PKG/catalogo_web/app.js      catalogo_web/app.js

# file nuovi
cp $PKG/catalogo_web/mappa_isola.js   catalogo_web/mappa_isola.js
cp $PKG/catalogo_web/mappa_isola.css  catalogo_web/mappa_isola.css
cp $PKG/vercel.json                   vercel.json

mkdir -p cartografia/assets_mappa/_base
cp $PKG/cartografia/assets_mappa/README.md            cartografia/assets_mappa/README.md
cp $PKG/cartografia/assets_mappa/_base/isola_base_v1.jpg \
   cartografia/assets_mappa/_base/isola_base_v1.jpg

# 3. verifica diff sui file modificati
git diff catalogo_web/index.html catalogo_web/app.js
# atteso:
#  - index.html: +3 righe (link CSS, link sidebar, script tag)
#  - app.js:     +9 righe (blocco router #/mappa-isola)

# 4. test locale (opzionale ma consigliato)
cd catalogo_web
python3 -m http.server 8000
# apri http://localhost:8000/#/mappa-isola
# verifica: si vede l'isola con 29 placeholder
# apri http://localhost:8000/#/mappa-isola?debug
# verifica: si vede griglia rossa con coordinate

# 5. commit
cd ..
git add catalogo_web/{index.html,app.js,mappa_isola.js,mappa_isola.css}
git add cartografia/assets_mappa/
git add vercel.json
git commit -m "feat(mappa-isola): vista mappa illustrata navigabile

Aggiunge route #/mappa-isola al catalogo_web/. Renderizza l'isola
in SVG con illustrazione master come sfondo e slot cliccabili
posizionati dai centroidi del geojson. Asset 3D progressivi:
ogni edificio mostra un placeholder finche' non viene generato il
PNG corrispondente in cartografia/assets_mappa/<id>.png.

- catalogo_web/mappa_isola.{js,css}: modulo isolato
- catalogo_web/{index.html,app.js}: hooks chirurgici (12 righe totali)
- cartografia/assets_mappa/: nuova directory con README e base v1
- vercel.json: deploy statico Vercel con cleanUrls"

# 6. push + PR
git push -u origin claude/mappa-isola-v1
```

---

## 4. DEPLOY SU VERCEL (prima volta)

1. **Vercel dashboard** → New Project → Import Git Repository
   → seleziona `raydalessandro/isola_i3v_visual`.
2. **Framework preset**: `Other` (non React, non Next, è statico).
3. **Build & Output settings**: lascia tutto vuoto, Vercel pesca da
   `vercel.json`.
4. **Root directory**: `./` (radice repo).
5. Deploy.

A regime, ad ogni `push` su `main` Vercel rideploya automaticamente in
~30 secondi. URL atteso (esempio):
`https://isola-i3v-visual.vercel.app/catalogo_web/#/mappa-isola`

Con il redirect in `vercel.json`, `https://<dominio>/` punta direttamente
al catalogo.

---

## 5. CALIBRAZIONE INIZIALE (consigliata, ~10 min)

Al primo accesso a `#/mappa-isola`, gli slot saranno *probabilmente*
fuori posto rispetto all'illustrazione di sfondo, perché:

- La bbox geografica del geojson ha aspect ratio 1.43:1
- L'immagine master ha aspect ratio 1.23:1
- L'isola dipinta non ha posizione corrispondente esattamente al canone
  geojson (è un'illustrazione evocativa)

**Procedura calibrazione:**

1. Apri `#/mappa-isola?debug` → vedi griglia rossa ogni 100px.
2. Identifica 2-3 punti notevoli sulla mappa dipinta che corrispondono
   chiaramente a feature del geojson (es. la spiaggia a sud → "spiaggia"
   nel geojson).
3. Modifica i 4 numeri di `MAPPA_CONFIG.bbox_geo` in `mappa_isola.js`:
   - `lon_min` / `lon_max` per scalare orizzontalmente
   - `lat_min` / `lat_max` per scalare verticalmente
   - allargare il range = isola appare più piccola
4. Per i casi singoli (un edificio fuori posto rispetto al resto),
   modifica le coordinate della feature direttamente in
   `cartografia/geo/island.geojson`.

**NON è bloccante per il deploy**: anche con calibrazione approssimativa
la mappa è già usabile — gli slot stanno comunque sopra l'isola in
posizioni ragionevoli, e Ray ha già detto che le incoerenze geojson
sono "come cambiare CSS, le risolveremo strada facendo".

### Anomalie attese al primo deploy (già verificate in preview)

Lo smoke test in fase di build ha mostrato due cose che Ray vedrà al
primo accesso alla mappa, **entrambe attese e non bloccanti**:

1. **Cluster villaggio sovrapposto**. Tutti gli edifici del villaggio
   centrale (Piazza, Albero Vecchio, Pozzo, Forno, Casa Mèmolo, Casa
   Stria, Bottega Nodo, Scuola, Cespuglio, Panca di Pietra) hanno
   coordinate geojson entro un raggio di ~50 m reali → si sovrappongono
   in pochi pixel sull'immagine 1120×912. Risolvibile in due modi
   (decisione di Ray):
   - **A**: spostare gradualmente le coordinate nel geojson per dare
     respiro visivo (è un'operazione cartografica sana — la "scala di
     rappresentazione" del villaggio non è la stessa dell'isola intera).
   - **B**: introdurre una vista "zoom villaggio" in V2 (sotto-mappa
     dedicata che si attiva al click sull'area centrale).

2. **Case Basse + Capanna Bartolo + Casa Amo cadono nel mare a sud**.
   Le coordinate geojson le mettono a lat ~34.476 ma l'isola dipinta
   finisce prima a sud. È un caso di "geografia canonica più ampia
   dell'illustrazione". Risolvibile spostando le coordinate dentro la
   spiaggia dipinta (aggiornamento puntuale del geojson).

Entrambe le anomalie si vedono chiaramente con `?debug` attivo.

---

## 6. WORKFLOW POST-DEPLOY (per Ray)

### Aggiungere un nuovo asset 3D

1. Genera con Grok (prompt base in `cartografia/assets_mappa/README.md`).
2. Salva PNG trasparente in `cartografia/assets_mappa/<id>.png` dove
   `<id>` è il `properties.id` della feature nel geojson (es. `forno`).
3. Commit + push.
4. Refresh `/catalogo_web/#/mappa-isola` → il placeholder è sostituito
   dall'asset 3D.

### Spostare un edificio

Modifica direttamente le coordinate `geometry.coordinates` della feature
in `cartografia/geo/island.geojson`. Commit + push. Cambia su entrambi:
mappa illustrata + viewer cartografico.

### Sostituire l'illustrazione master

Quando arriverà una versione migliore dell'isola dall'alto:

1. Salva nuova `_base/isola_base_v2.jpg` (o png, conserva il vecchio).
2. In `mappa_isola.js`:
   - aggiorna `MAPPA_CONFIG.base_image`
   - aggiorna `image_w` / `image_h` se cambia la risoluzione
   - ricalibra `bbox_geo` se cambia l'inquadratura
3. Commit + push.

---

## 7. NON-OBIETTIVI DI QUESTA V1 (esplicitati per evitare scope creep)

- **Personaggi sulla mappa**: rinviati. L'architettura è pronta a
  riceverli ma non sono inclusi.
- **Animazioni / micro-storie / interattività avanzata**: rinviate.
- **Editor visuale per posizionare gli slot drag&drop**: non incluso.
  Per ora si aggiusta il geojson a mano (rapido).
- **Generazione automatica asset 3D**: out of scope. Ray fa con Grok.
- **Mini-mappa per ogni storia**: non incluso (stessa idea
  realizzabile in V2 leggendo `appare_in_storie` da `entities.json`).
- **Filtri sidebar**: non inclusi (nella V1 si vedono tutti gli slot).

---

## 8. NOTE TECNICHE / TRADE-OFF

- **HEAD requests sugli asset**: il modulo fa una `HEAD` per ogni slot
  per sapere se l'asset 3D esiste (~30 richieste). Veloci e cached da
  Vercel. Alternativa: precomputare la lista in build, ma il guadagno
  è minimo e la complessità aumenta.
- **Niente Leaflet**: il viewer cartografico usa Leaflet, qui no. La
  mappa illustrata è statica (no zoom/pan): se in futuro servirà
  zoom/pan, è facile aggiungere `panzoom.js` o simile. SVG nativo è
  già più leggero.
- **No frameworks**: vanilla JS in continuità con il resto di
  `catalogo_web/`. Niente React, Vue, npm. Funziona aprendo il file in
  qualsiasi browser.
- **Compatibilità GitHub Pages**: i file sono compatibili anche con
  Pages se in futuro serve fallback. Vercel è il target primario.

---

## 9. CONTATTI / TROUBLESHOOTING

Se la mappa non si carica:
- DevTools console → cerca errori `[mappa]`.
- Verifica che `cartografia/geo/island.geojson` sia raggiungibile via
  HTTP (non solo via filesystem — serve un web server).
- Verifica che `cartografia/assets_mappa/_base/isola_base_v1.jpg`
  esista nella repo.
- Su Vercel: verifica i logs del deploy per errori 404.

Se gli slot sono tutti ammassati in un angolo:
- Hai sbagliato la bbox di calibrazione. Apri `?debug` e ricalibra.

Se vedi solo placeholder anche dopo aver messo gli asset:
- Verifica che il filename sia esattamente `<id>.png` (case-sensitive!).
- Verifica che l'`<id>` corrisponda al `properties.id` nel geojson
  (snake_case, italiano, senza articolo).
- Hard refresh del browser (Ctrl+Shift+R) — il cache potrebbe
  trattenere la HEAD precedente.

---

**Fine pacchetto v1.**
