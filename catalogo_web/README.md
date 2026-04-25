# catalogo_web/

Sito statico **interno** che mostra in modo navigabile tutte le entità della saga catalogate in `visual/`. Pensato per consultazione rapida da parte di Ray e collaboratori senza passare da GitHub.

**Stack:** HTML + CSS + JS vanilla. Niente build, niente dipendenze npm. Markdown rendering via `marked.js` da CDN.

## Struttura

```
catalogo_web/
├── index.html              entry point + layout 2 colonne
├── style.css               minimal, ispirato al viewer cartografia
├── app.js                  vanilla JS: fetch JSON, render albero, hash routing, search
├── data/
│   └── entities.json       generato dallo script Python (~390 KB)
└── README.md               (questo file)
```

## Aggiornare il catalogo

Quando aggiungi/modifichi una scheda in `visual/`, oppure aggiungi un'immagine in una `<entita>/immagini/`, basta rilanciare lo script Python:

```bash
python3 scripts/build_catalogo_web.py
```

Lo script:
- Scansiona ricorsivamente `visual/` cercando ogni `scheda.md`.
- Estrae frontmatter YAML (richiede PyYAML: `pip install pyyaml`) e body markdown.
- Raccoglie i path delle immagini in `<entita>/immagini/`.
- Costruisce un albero gerarchico riflesso della struttura folder.
- Sovrascrive `catalogo_web/data/entities.json` (idempotente).

Dopo: refresh del browser ⇒ il sito riflette i cambiamenti.

## Vedere il sito in locale

Per evitare problemi di CORS con `fetch()` da `file://`, servi la repo da web server:

```bash
# dalla radice del repo
python3 -m http.server 8000
# poi apri http://localhost:8000/catalogo_web/
```

## Deploy su GitHub Pages

1. Settings → Pages → **Source: Deploy from a branch**.
2. Branch: **main**, Folder: **`/`** (root).
3. Salva. Dopo qualche minuto il sito è raggiungibile a:
   `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`

Pages serve l'intera repo, quindi `app.js` può fare `fetch("data/entities.json")` e il browser può caricare le immagini con path relativo `../visual/<entita>/immagini/<file>.png`.

Ad ogni `git push` su `main`, Pages rideploya automaticamente. Il flusso suggerito:

```
modifica scheda  →  python3 scripts/build_catalogo_web.py  →  git commit + push  →  refresh sito
```

## Funzionalità V1

- **Sidebar ad albero** con stessa gerarchia di `visual/`: famiglie collassabili, sotto-categorie, entità foglia.
- **Search testuale** (per nome o id) che filtra l'albero.
- **Pagina entità**: titolo, tag (famiglia, sottotipo, status, quartiere/categoria_strada), frontmatter dettagliato (collassabile), body markdown renderizzato, gallery immagini.
- **Indice strade** dedicato (legge `visual/luoghi/_strade_index.md`).
- **Link al viewer cartografia** esistente in `cartografia/geo/viewer/`.
- Routing client-side via hash (`#/`, `#/entity/<id>`, `#/strade`).

## Limiti noti / migliorie future

- Le immagini sono lette dal filesystem repo: serve un web server (locale o Pages).
- Nessun lightbox sulle immagini (V1).
- Nessuna paginazione: con 112 entità il filtro testuale basta. Se cresce sopra le 500, valutare virtualizzazione.
- Nessun mini-mappa per i luoghi: per ora il link al viewer cartografia.
- Il body MD usa `marked.js` da CDN — se la connessione è offline non renderizza. Per uso 100% offline, scaricare `marked.min.js` localmente.
