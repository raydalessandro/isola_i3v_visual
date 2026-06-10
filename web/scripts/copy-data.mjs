// Copia idempotente dei dati da `../catalogo_web/data/` a `public/data/`.
//
// FLUSSO DUALE (cutover Vercel 2026-06-10):
//
//   1. Sviluppo locale (Ray o agente da repo root):
//      - `python3 scripts/build_catalogo_web.py` genera SIA
//        `catalogo_web/data/entities.json` SIA `web/public/data/entities.json`
//        (mirror diretto, no copy-data necessario).
//      - `python3 scripts/build_storie_data.py` idem per `storie-dashboard.json`.
//      - Comunque questo script resta come *fallback* idempotente per
//        `npm run dev` / `npm run dev:live` dove il dev parte da web/ e
//        vuole essere sicuro che public/data/ sia in sync con catalogo_web/data/.
//
//   2. CI / Vercel (Root Directory = web/):
//      - I file `.json` sono **committati** in `web/public/data/` (tracciati
//        nel repo, vedi web/.gitignore aggiornato).
//      - Vercel build non vede `../catalogo_web/` (fuori dalla Root Directory).
//      - Questo script in fase prebuild trova i sorgenti mancanti, NON fallisce
//        ma logga il fallback ai file già presenti in `public/data/`.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = resolve(__dirname, "..");
const REPO_ROOT = resolve(WEB_ROOT, "..");

const FILES = [
  {
    from: resolve(REPO_ROOT, "catalogo_web/data/entities.json"),
    to: resolve(WEB_ROOT, "public/data/entities.json"),
  },
  {
    // Dashboard di lavoro illustrazioni: stats, audit entità, hook accordion,
    // canon todo, saga style reference. Generato da
    // `scripts/build_storie_data.py` nel catalogo statico (~291 KB).
    // NB: distinto da `public/data/storie.json` (vista pagine libro,
    // generato da `scripts/build-storie.mjs` di Next).
    from: resolve(REPO_ROOT, "catalogo_web/data/storie.json"),
    to: resolve(WEB_ROOT, "public/data/storie-dashboard.json"),
  },
];

let copied = 0;
let kept = 0;
for (const { from, to } of FILES) {
  const rel = to.replace(WEB_ROOT + "/", "");
  if (!existsSync(from)) {
    if (existsSync(to)) {
      // Caso CI/Vercel: sorgente fuori root, ma il mirror committato c'è.
      console.log(`[copy-data] ${rel} (sorgente esterno assente, uso copia committata)`);
      kept++;
      continue;
    }
    console.error(
      `[copy-data] ERRORE: ne' ${from} ne' ${to} esistono. ` +
        `Esegui: python3 scripts/build_catalogo_web.py (e build_storie_data.py).`,
    );
    process.exit(1);
  }
  mkdirSync(dirname(to), { recursive: true });
  copyFileSync(from, to);
  const size = statSync(to).size;
  console.log(`[copy-data] ${rel} (${(size / 1024).toFixed(1)} KB)`);
  copied++;
}

if (kept > 0) {
  console.log(
    `[copy-data] ${copied} copiati, ${kept} usati dal mirror committato.`,
  );
}
