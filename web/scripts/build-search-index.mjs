// build-search-index.mjs — WI-5 catalogo v2.
//
// Genera public/data/search-index.json: indice leggero per il cmd-K palette.
// Entries: tutte le entità del catalogo + le 12 storie.
// Per ogni entry: id, label, categoria, sections [{title, slug}].
//
// Gli slug delle sezioni sono ricavati dal body_md con lo stesso algoritmo
// di lib/markdown.ts (slugify + uniqueSlug), così i link generati dal
// palette combaciano con gli id usati da entity-body.tsx (WI-4).
//
// Gira come prebuild step (dopo copy-data.mjs).

import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = resolve(__dirname, "..");
const PUBLIC_DATA = resolve(WEB_ROOT, "public", "data");

const ENTITIES_FILE = resolve(PUBLIC_DATA, "entities.json");
const STORIE_FILE = resolve(PUBLIC_DATA, "storie.json");
const OUT_FILE = resolve(PUBLIC_DATA, "search-index.json");

// ── Slug (identico a lib/markdown.ts) ──────────────────────────────────────
function slugify(s) {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9\s-]/g, "")
    .trim()
    .replace(/[\s_]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function uniqueSlug(base, used) {
  if (!used.has(base) && base) {
    used.add(base);
    return base;
  }
  let n = 2;
  let slug;
  do {
    slug = `${base || "sezione"}-${n}`;
    n++;
  } while (used.has(slug));
  used.add(slug);
  return slug;
}

/** Estrae i titoli H2 dal markdown e produce slug stabili (1° passata). */
function extractSections(bodyMd) {
  if (!bodyMd) return [];
  const out = [];
  const used = new Set();
  const lines = bodyMd.split("\n");
  for (const line of lines) {
    const m = line.match(/^##\s+(.+?)\s*$/);
    if (m && !line.startsWith("###")) {
      const title = m[1].trim();
      const slug = uniqueSlug(slugify(title), used);
      out.push({ title, slug });
    }
  }
  return out;
}

function main() {
  if (!existsSync(ENTITIES_FILE)) {
    console.error("entities.json mancante — esegui prima copy-data.mjs");
    process.exit(1);
  }

  const data = JSON.parse(readFileSync(ENTITIES_FILE, "utf-8"));
  const entries = [];

  // ── Entità del catalogo ──────────────────────────────────────────────────
  for (const e of data.entities || []) {
    const sections = extractSections(e.body_md);
    entries.push({
      kind: "entity",
      id: e.id,
      label: e.name || e.id,
      categoria: e.categoria || e.famiglia || "",
      sottotipo: e.sottotipo || "",
      quartiere: e.quartiere || "",
      status: e.status || "",
      href: `/catalogo/${e.id}`,
      sections,
    });
  }

  // ── Storie ───────────────────────────────────────────────────────────────
  if (existsSync(STORIE_FILE)) {
    const storie = JSON.parse(readFileSync(STORIE_FILE, "utf-8"));
    const list = Array.isArray(storie)
      ? storie
      : storie.stories || storie.storie || [];
    for (const s of list) {
      const id = s.sid || s.id;
      if (!id) continue;
      entries.push({
        kind: "storia",
        id,
        label: s.title || s.titolo || id,
        categoria: "storia",
        href: `/storie/${id}`,
        sections: [],
      });
    }
  }

  mkdirSync(PUBLIC_DATA, { recursive: true });
  const payload = {
    generated_at: new Date().toISOString(),
    count: entries.length,
    entries,
  };
  writeFileSync(OUT_FILE, JSON.stringify(payload, null, 2), "utf-8");
  console.log(
    `search-index.json: ${entries.length} entries (${
      entries.filter((e) => e.kind === "entity").length
    } entità + ${entries.filter((e) => e.kind === "storia").length} storie)`,
  );
}

main();
