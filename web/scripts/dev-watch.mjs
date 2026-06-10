// dev-watch.mjs — WI-7 catalogo v2.
//
// Lancia `next dev` e in parallelo guarda i file sorgente del catalogo:
// quando Ray modifica una scheda visual o un testo storia, rigenera
// entities.json + storie.json + orchestra.json + search-index.json.
// Il browser non si auto-aggiorna (next dev fa hot-reload solo sui file di
// `web/`, non sui dati in public/data), ma F5 entro ~2s mostra i dati nuovi.
//
// Zero dipendenze extra: fs.watch ricorsivo + child_process spawn.
//
// Usato come: `npm run dev:live`

import { spawn, spawnSync } from "node:child_process";
import { watch } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = resolve(__dirname, "..");
const REPO_ROOT = resolve(WEB_ROOT, "..");

const WATCH_PATHS = [
  resolve(REPO_ROOT, "visual"),
  resolve(REPO_ROOT, "pipeline_narrativa", "storie_finali"),
  resolve(REPO_ROOT, "pipeline_narrativa", "story_graph.json"),
];

const DEBOUNCE_MS = 500;

const COLOR = {
  reset: "\x1b[0m",
  dim: "\x1b[2m",
  cyan: "\x1b[36m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  red: "\x1b[31m",
};

function log(tag, msg, color = COLOR.dim) {
  const t = new Date().toLocaleTimeString();
  console.log(`${COLOR.dim}[${t}]${COLOR.reset} ${color}${tag}${COLOR.reset} ${msg}`);
}

// ── Rigenerazione dati ──────────────────────────────────────────────────────

function regen(reason) {
  log("regen", `triggered by ${reason}`, COLOR.yellow);
  // 1) Python: rigenera catalogo_web/data/entities.json
  const py = spawnSync(
    "python3",
    [resolve(REPO_ROOT, "scripts/build_catalogo_web.py")],
    { cwd: REPO_ROOT, stdio: "pipe", encoding: "utf-8" },
  );
  if (py.status !== 0) {
    log("regen", `build_catalogo_web.py FAIL\n${py.stderr || py.stdout}`, COLOR.red);
    return;
  }
  // 2) Node: copia + storie + orchestra + search-index
  const steps = [
    "copy-data.mjs",
    "build-storie.mjs",
    "build-orchestra-data.mjs",
    "build-search-index.mjs",
  ];
  for (const s of steps) {
    const r = spawnSync("node", [resolve(__dirname, s)], {
      cwd: WEB_ROOT,
      stdio: "pipe",
      encoding: "utf-8",
    });
    if (r.status !== 0) {
      log("regen", `${s} FAIL\n${r.stderr || r.stdout}`, COLOR.red);
      return;
    }
  }
  log("regen", "OK — premi F5 nel browser", COLOR.green);
}

// ── Watcher con debounce ────────────────────────────────────────────────────

let debounceTimer = null;
let pendingReason = "";

function scheduleRegen(reason) {
  pendingReason = reason;
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    regen(pendingReason);
    debounceTimer = null;
  }, DEBOUNCE_MS);
}

function startWatchers() {
  for (const p of WATCH_PATHS) {
    try {
      watch(p, { recursive: true }, (event, filename) => {
        if (!filename) return;
        // Filtro: ignora file temporanei, dotfile, .pyc, ecc.
        const name = basename(filename.toString());
        if (
          name.startsWith(".") ||
          name.endsWith(".tmp") ||
          name.endsWith(".swp") ||
          name.endsWith(".pyc")
        )
          return;
        scheduleRegen(`${event}:${filename}`);
      });
      log("watch", `${p}`, COLOR.cyan);
    } catch (err) {
      log("watch", `cannot watch ${p}: ${err.message}`, COLOR.red);
    }
  }
}

// ── Avvio next dev in parallelo ─────────────────────────────────────────────

function startNextDev() {
  const next = spawn("npx", ["next", "dev"], {
    cwd: WEB_ROOT,
    stdio: "inherit",
    env: process.env,
  });
  next.on("exit", (code) => {
    log("next", `exited (${code})`, COLOR.red);
    process.exit(code || 0);
  });
  return next;
}

// ── Main ────────────────────────────────────────────────────────────────────

log("dev:live", "build iniziale dati...", COLOR.cyan);
regen("startup");
log("dev:live", "avvio next dev + watcher", COLOR.cyan);
startWatchers();
const child = startNextDev();

process.on("SIGINT", () => {
  if (debounceTimer) clearTimeout(debounceTimer);
  child.kill("SIGINT");
  process.exit(0);
});
