// Copia idempotente di entities.json (e di altri file dati selezionati)
// dal catalogo statico (../catalogo_web/data) dentro public/data/.
// Eseguito come `prebuild` dal package.json. Idempotente: ricopia ogni volta.
//
// Filosofia: NON committiamo public/data/ (gitignored). Lo build pipeline
// pesca i dati live dal repo. Quando faremo cutover, il path sorgente
// resterà identico finché esiste catalogo_web/data/entities.json.

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
    required: true,
  },
];

let failed = false;
for (const { from, to, required } of FILES) {
  if (!existsSync(from)) {
    const msg = `[copy-data] sorgente non trovato: ${from}`;
    if (required) {
      console.error(msg);
      failed = true;
    } else {
      console.warn(msg + " (skip)");
    }
    continue;
  }
  mkdirSync(dirname(to), { recursive: true });
  copyFileSync(from, to);
  const size = statSync(to).size;
  const rel = to.replace(WEB_ROOT + "/", "");
  console.log(`[copy-data] ${rel} (${(size / 1024).toFixed(1)} KB)`);
}

if (failed) process.exit(1);
