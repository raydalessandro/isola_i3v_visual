// Test del parser `prompt-grok` sui due dialetti reali della repo.
// Esecuzione: `npm run test` (usa node --test --experimental-strip-types).
//
// La spec WI-1 (catalogo v2) richiede esplicitamente questo test perché
// il parser è l'unico pezzo fragile: due dialetti markdown leggermente
// diversi (IMMAGINE per personaggi/oggetti, Veduta per luoghi).

import { test } from "node:test";
import { strict as assert } from "node:assert";
import { readFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

import { parsePromptGrok, concatWithGlobals } from "../prompt-grok.ts";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(__dirname, "..", "..", "..");

// ─── Dialetto 1: personaggi (IMMAGINE) ─────────────────────────────────────

const PERSONAGGIO_MD = `# Titolo
## STYLESHEET CANONICA SAGA (incolla in ogni prompt)

\`\`\`
STYLE: classic European watercolor.
\`\`\`

## CANONE PERSONAGGIO X

\`\`\`
CHARACTER CANON: small dragonfly.
\`\`\`

## IMMAGINE 1 — fronte default

Preambolo descrittivo.

\`\`\`
PROMPT IMG 1 — full text here.
\`\`\`

Checklist: occhi grandi, ali blu.

## IMMAGINE 2 — modalità stop in aria

\`\`\`
PROMPT IMG 2 — second view.
\`\`\`

## Negative prompt globale (incolla in coda)

\`\`\`
NEGATIVE: no anime, no 3D.
\`\`\`
`;

test("parser personaggio: estrae 2 viste + 3 globals", () => {
  const parsed = parsePromptGrok(PERSONAGGIO_MD);
  assert.equal(parsed.views.length, 2);
  assert.equal(parsed.globals.length, 3);
});

test("parser personaggio: titolo vista pulito + prompt byte-identico al fenced", () => {
  const parsed = parsePromptGrok(PERSONAGGIO_MD);
  assert.equal(parsed.views[0].title, "IMMAGINE 1 — fronte default");
  assert.equal(parsed.views[0].prompt, "PROMPT IMG 1 — full text here.");
  assert.equal(parsed.views[1].prompt, "PROMPT IMG 2 — second view.");
});

test("parser personaggio: checklist catturata dopo il fenced", () => {
  const parsed = parsePromptGrok(PERSONAGGIO_MD);
  assert.ok(parsed.views[0].checklist);
  assert.match(parsed.views[0].checklist!, /occhi grandi/);
});

test("parser personaggio: niente filenameAtteso (dialetto IMMAGINE)", () => {
  const parsed = parsePromptGrok(PERSONAGGIO_MD);
  assert.equal(parsed.views[0].filenameAtteso, undefined);
});

// ─── Dialetto 2: luoghi (Veduta + Filename atteso) ─────────────────────────

const LUOGO_MD = `# Foresta
## Indice vedute

- Veduta 1, Veduta 2

## 🎨 Veduta 1 — Foresta interno — v1

**Filename atteso:** \`foresta_canonica_v1_interno.jpg\`

### ⭐ PROMPT

\`\`\`
PROMPT VEDUTA 1 — interno foresta.
\`\`\`

### 🎯 Checklist
- intreccio rami
- luce filtrata

## 🎨 Veduta 2 — Margine

**Filename atteso:** \`foresta_canonica_v1_margine.jpg\`

\`\`\`
PROMPT VEDUTA 2 — margine.
\`\`\`

## 🔗 Riferimento canonico

Solo testo, niente fenced. Va ignorato.
`;

test("parser luogo: estrae 2 vedute con filenameAtteso", () => {
  const parsed = parsePromptGrok(LUOGO_MD);
  assert.equal(parsed.views.length, 2);
  assert.equal(parsed.views[0].filenameAtteso, "foresta_canonica_v1_interno.jpg");
  assert.equal(parsed.views[1].filenameAtteso, "foresta_canonica_v1_margine.jpg");
});

test("parser luogo: titolo Veduta pulito (emoji rimosso)", () => {
  const parsed = parsePromptGrok(LUOGO_MD);
  assert.equal(parsed.views[0].title, "Veduta 1 — Foresta interno — v1");
});

test("parser: sezione senza fenced viene ignorata", () => {
  const parsed = parsePromptGrok(LUOGO_MD);
  // "🔗 Riferimento canonico" non deve apparire né in views né in globals
  const allTitles = [...parsed.views, ...parsed.globals].map((x) => x.title);
  assert.equal(allTitles.some((t) => t.includes("Riferimento")), false);
});

// ─── Edge cases ────────────────────────────────────────────────────────────

test("parser: input vuoto → views=[] globals=[]", () => {
  assert.deepEqual(parsePromptGrok(""), { views: [], globals: [] });
});

test("parser: solo preambolo (no H2) → views=[] globals=[]", () => {
  const md = "# Titolo\n\nSolo preambolo.\n\nAltro testo.";
  assert.deepEqual(parsePromptGrok(md), { views: [], globals: [] });
});

test("concatWithGlobals: prompt + 2 globals separati da riga vuota", () => {
  const out = concatWithGlobals("PROMPT", [
    { title: "neg", text: "NEGATIVE" },
    { title: "extra", text: "EXTRA" },
  ]);
  assert.equal(out, "PROMPT\n\nNEGATIVE\n\nEXTRA");
});

test("concatWithGlobals: prompt + zero globals = prompt invariato", () => {
  assert.equal(concatWithGlobals("PROMPT", []), "PROMPT");
});

// ─── Smoke test sui file reali della repo ──────────────────────────────────
//
// Garantiscono che il parser regga sui due file di reference citati nella spec
// (liu + foresta_intrecciata). Se la struttura dei file cambia in modo
// incompatibile, questi test si rompono subito.

test("smoke: liu/prompt_grok.md ha 4 IMMAGINE + almeno 3 globals", () => {
  const md = readFileSync(
    resolve(REPO, "visual/personaggi/individuali/cuccioli/liu/prompt_grok.md"),
    "utf-8",
  );
  const parsed = parsePromptGrok(md);
  assert.equal(parsed.views.length, 4, "attese 4 viste IMMAGINE");
  assert.ok(
    parsed.globals.length >= 3,
    `attesi >= 3 globals, trovati ${parsed.globals.length}`,
  );
  // Le viste devono avere prompt non vuoto
  for (const v of parsed.views) {
    assert.ok(v.prompt.length > 0, `vista ${v.title} ha prompt vuoto`);
  }
});

test("smoke: foresta_intrecciata/prompt_grok.md — viste con filenameAtteso", () => {
  const md = readFileSync(
    resolve(REPO, "visual/luoghi/quartiere_terra/foresta_intrecciata/prompt_grok.md"),
    "utf-8",
  );
  const parsed = parsePromptGrok(md);
  assert.ok(parsed.views.length >= 1, "attesa almeno 1 Veduta");
  // Almeno una vista ha filenameAtteso (campo dialetto luoghi)
  assert.ok(
    parsed.views.some((v) => v.filenameAtteso),
    "almeno una Veduta deve avere filenameAtteso",
  );
});
