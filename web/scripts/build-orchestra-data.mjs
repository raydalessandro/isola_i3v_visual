// Prebuild: estrae il modello dati per l'atlante saga (vista Orchestra)
// dal grafo canonico in `pipeline_narrativa/story_graph.json` e produce
// `web/public/data/orchestra.json`.
//
// Idempotente. ESM. Tollera errori per singolo elemento (warn + skip),
// non blocca il build complessivo.
//
// Schema output:
//   {
//     generated_at: ISO,
//     graph_version, schema_version,
//     stories:    OrchestraStory[]      // 12 storie s01..s12
//     characters: OrchestraCharacter[]  // entità grafo + appearances calcolate
//     locations:  OrchestraLocation[]   // entità grafo + appearances calcolate
//     seeds:      OrchestraSeed[]       // top-level seeds (40)
//   }

import {
  existsSync,
  mkdirSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = resolve(__dirname, "..");
const REPO_ROOT = resolve(WEB_ROOT, "..");
const GRAPH_PATH = resolve(REPO_ROOT, "pipeline_narrativa/story_graph.json");
const OUT_DIR = resolve(WEB_ROOT, "public/data");
const OUT_FILE = resolve(OUT_DIR, "orchestra.json");

// Helpers
const BLOCK_RE = /^(apertura|centro|chiusura)_blocco_[abcd]$/;

function normalizeBlock(bp) {
  if (typeof bp !== "string") return null;
  const m = BLOCK_RE.exec(bp);
  return m ? m[1] : null;
}

function normalizeWind(w) {
  if (!w) return null;
  if (typeof w === "string") return w;
  if (typeof w === "object" && typeof w.id === "string") return w.id;
  return null;
}

function humanizeId(id) {
  if (typeof id !== "string" || !id) return "";
  return id.split(/[_\s]+/).filter(Boolean)
    .map((t) => t.charAt(0).toUpperCase() + t.slice(1)).join(" ");
}

function pickName(meta, id) {
  if (!meta || typeof meta !== "object") return humanizeId(id);
  const candidates = [meta.name, meta.displayName, meta.display_name, meta.nome, meta.label, meta.title, meta.title_provvisorio];
  for (const c of candidates) if (typeof c === "string" && c.trim()) return c.trim();
  return humanizeId(id);
}

function mapLocationType(meta) {
  if (!meta || typeof meta !== "object") return "abitato";
  const t = String(meta.type || "").toLowerCase();
  const q = String(meta.quadrant || "").toLowerCase();
  if (/(spiaggia|foce|guado|water_feature|corso_acqua|fiume|pozzo|water)/.test(t))
    return /(spiaggia|foce)/.test(t) || q === "acqua_sud" ? "costa" : "acqua";
  if (/(rilievo|sperone_panoramico|prato_in_pendenza|gola)/.test(t)) return "alto";
  if (q === "aria_nord") return "alto";
  if (/(foresta|tana|grotta|clearing|radura|fascia|zona_coltivata)/.test(t)) return "selvatico";
  if (/(quartiere_parziale)/.test(t) && q === "acqua_sud") return "costa";
  return "abitato";
}

function characterIdFromEntry(entry) {
  if (typeof entry === "string") return entry;
  if (entry && typeof entry === "object" && typeof entry.id === "string") return entry.id;
  return null;
}

function locationIdFromPrimary(lp) {
  if (typeof lp === "string") return lp;
  if (lp && typeof lp === "object" && typeof lp.id === "string") return lp.id;
  return null;
}

function asStringList(v) {
  if (!v) return [];
  if (Array.isArray(v)) return v.map((x) => {
    if (typeof x === "string") return x;
    if (x && typeof x === "object" && typeof x.id === "string") return x.id;
    return null;
  }).filter((x) => typeof x === "string" && x.length > 0);
  if (typeof v === "string") return [v];
  return [];
}

function normalizeFear(f) {
  if (!f || typeof f !== "object") return null;
  return {
    brother: typeof f.brother === "string" ? f.brother : null,
    fear_id: typeof f.fear_id === "string" ? f.fear_id : null,
    status: typeof f.status === "string" ? f.status : null,
    mode_of_touch: typeof f.mode_of_touch === "string" ? f.mode_of_touch : null,
  };
}

function build() {
  if (!existsSync(GRAPH_PATH)) {
    // Vercel scenario (Root Directory = web/): grafo fuori root,
    // ma orchestra.json committato e' valido.
    if (existsSync(OUT_FILE)) {
      console.log(
        `[build-orchestra] sorgente assente, uso mirror committato: ${OUT_FILE}`,
      );
      return;
    }
    console.error(`[build-orchestra] grafo non trovato: ${GRAPH_PATH}`);
    process.exit(1);
  }

  let g;
  try { g = JSON.parse(readFileSync(GRAPH_PATH, "utf-8")); }
  catch (err) { console.error(`[build-orchestra] errore parsing grafo: ${err.message}`); process.exit(1); }

  const graphVersion = g.graph_version || null;
  const schemaVersion = g.schema_version || null;
  const storiesRaw = g.stories || {};
  const charactersMeta = (g.entities && g.entities.characters) || {};
  const locationsMeta = (g.entities && g.entities.locations) || {};
  const seedsRaw = g.seeds || {};

  // Stories
  const sids = Object.keys(storiesRaw).filter((k) => /^s\d{2}$/.test(k)).sort();
  const stories = [];
  for (const sid of sids) {
    const s = storiesRaw[sid];
    if (!s || typeof s !== "object") { console.warn(`[build-orchestra] ${sid}: invalida, skip`); continue; }
    try {
      const charIds = (Array.isArray(s.characters_in_scene) ? s.characters_in_scene : [])
        .map(characterIdFromEntry).filter((x) => typeof x === "string" && x.length > 0);
      const locId = locationIdFromPrimary(s.location_primary);
      const seedsPlanted = asStringList(s.seeds_planted);
      const seedsBloomed = asStringList(s.seeds_bloomed_here);
      const debtsOpened = asStringList(s.debts_opened);
      const debtsClosed = asStringList(s.debts_closed);
      const callbacks = asStringList(s.callbacks_made);
      stories.push({
        sid,
        title: typeof s.title_provvisorio === "string" ? s.title_provvisorio : sid,
        season: typeof s.season === "string" ? s.season : null,
        cycle: typeof s.cycle === "string" ? s.cycle : null,
        block: normalizeBlock(s.block_position),
        wind: normalizeWind(s.wind_active),
        premise: typeof s.premise === "string" ? s.premise : null,
        fear: normalizeFear(s.fear_touched),
        location_id: locId,
        character_ids: charIds,
        seeds_planted_ids: seedsPlanted,
        seeds_bloomed_ids: seedsBloomed,
        seeds_planted_count: seedsPlanted.length,
        seeds_bloomed_count: seedsBloomed.length,
        debts_opened_count: debtsOpened.length,
        debts_closed_count: debtsClosed.length,
        callbacks_count: callbacks.length,
      });
    } catch (err) { console.warn(`[build-orchestra] ${sid}: errore (${err.message}), skip`); }
  }

  const storyBySid = new Map(stories.map((s) => [s.sid, s]));

  // Characters
  const allCharIds = new Set(Object.keys(charactersMeta));
  for (const s of stories) for (const cid of s.character_ids) allCharIds.add(cid);
  const characters = [];
  for (const cid of Array.from(allCharIds).sort()) {
    if (cid.startsWith("_")) continue;
    const meta = charactersMeta[cid] || {};
    const appearances = stories.filter((s) => s.character_ids.includes(cid)).map((s) => s.sid);
    characters.push({
      id: cid,
      name: pickName(meta, cid),
      role: meta.role_saga || meta.role || meta.type || null,
      species: meta.species || null,
      age_band: meta.age_band || null,
      appearances,
    });
  }

  // Locations
  const allLocIds = new Set(Object.keys(locationsMeta));
  for (const s of stories) if (s.location_id) allLocIds.add(s.location_id);
  const locations = [];
  for (const lid of Array.from(allLocIds).sort()) {
    if (lid.startsWith("_")) continue;
    const meta = locationsMeta[lid] || {};
    const appearances = stories.filter((s) => s.location_id === lid).map((s) => s.sid);
    locations.push({
      id: lid,
      name: pickName(meta, lid),
      type: mapLocationType(meta),
      raw_type: typeof meta.type === "string" ? meta.type : null,
      quadrant: typeof meta.quadrant === "string" ? meta.quadrant : null,
      role_saga: typeof meta.role_saga === "string" ? meta.role_saga : null,
      appearances,
    });
  }

  // Seeds
  const seeds = [];
  let multiBloom = 0, singleBloom = 0, zeroBloom = 0;
  const seedEntries = Array.isArray(seedsRaw)
    ? seedsRaw.map((s) => [s && typeof s.seed_id === "string" ? s.seed_id : null, s])
    : Object.entries(seedsRaw);
  for (const [sidKey, s] of seedEntries) {
    if (!s || typeof s !== "object") continue;
    const id = (typeof s.seed_id === "string" && s.seed_id) || sidKey;
    if (!id) continue;
    const planted = typeof s.origin_story === "string" ? s.origin_story : null;
    let blooms = s.bloom_target_stories;
    if (typeof blooms === "string") blooms = [blooms];
    if (!Array.isArray(blooms)) blooms = [];
    blooms = blooms.filter((x) => typeof x === "string" && x.length > 0);
    if (blooms.length === 0) zeroBloom += 1;
    else if (blooms.length === 1) singleBloom += 1;
    else multiBloom += 1;
    seeds.push({
      id,
      description: typeof s.description === "string" ? s.description : null,
      planted,
      bloom_targets: blooms,
      type: typeof s.type === "string" ? s.type : null,
      bloom_type: typeof s.bloom_type === "string" ? s.bloom_type : null,
      status: typeof s.status === "string" ? s.status : null,
    });
  }
  seeds.sort((a, b) => {
    const pa = a.planted || "zzz"; const pb = b.planted || "zzz";
    if (pa !== pb) return pa.localeCompare(pb);
    return a.id.localeCompare(b.id);
  });

  const out = {
    generated_at: new Date().toISOString(),
    graph_version: graphVersion,
    schema_version: schemaVersion,
    stories, characters, locations, seeds,
  };

  mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(OUT_FILE, JSON.stringify(out, null, 2) + "\n", "utf-8");

  const sizeKb = (Buffer.byteLength(JSON.stringify(out)) / 1024).toFixed(1);
  console.log(`[build-orchestra] ${stories.length} storie, ${characters.length} pers, ${locations.length} luoghi, ${seeds.length} semi (multi=${multiBloom}, single=${singleBloom}, zero=${zeroBloom}) → public/data/orchestra.json (${sizeKb} KB)`);

  if (stories.length !== 12)
    console.warn(`[build-orchestra] WARNING: ${stories.length} storie, atteso 12.`);
  const missing = ["s01","s02","s03","s04","s05","s06","s07","s08","s09","s10","s11","s12"]
    .filter((s) => !storyBySid.has(s));
  if (missing.length) console.warn(`[build-orchestra] WARNING: storie mancanti: ${missing.join(",")}`);
}

build();
