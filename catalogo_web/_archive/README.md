# Catalogo statico — archiviato 2026-06-10

Questi file erano la UI del **catalogo statico** servito a `/catalogo_web/`.

Sono stati **archiviati** (non eliminati) dopo il merge della PR
`claude/catalogo-v2`: la UI del catalogo vive ora interamente nell'app
Next.js in `web/`. Vedi `docs/SPEC_CATALOGO_V2.md` per il dettaglio.

## Cosa è ancora vivo

- `catalogo_web/data/entities.json` (e `storie.json`) — il **contratto
  dati** generato da `scripts/build_catalogo_web.py`, letto dalla app
  Next via `web/scripts/copy-data.mjs`. **Non toccare.**

## File archiviati

- `index.html` — 1131 righe vanilla JS (catalogo)
- `app.js`     — logica routing/rendering catalogo
- `style.css`  — 1895 righe stile monolitico
- `mappa_isola.js` + `mappa_isola.css` — vista mappa illustrata (Leaflet
  embedded), spostata in `web/app/mappa/page.tsx`

## Cutover deploy

Per spegnere completamente il deploy statico:

1. Aggiornare `vercel.json` root: rimuovere il redirect `/` → `/catalogo_web/`
   o puntarlo alla app Next.
2. Configurare il dominio principale verso il deploy `web/`.

L'archivio resta in repo come trail di audit e per eventuale rollback.
