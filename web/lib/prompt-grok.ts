// Parser markdown per i file `prompt_grok.md` del catalogo.
//
// Due dialetti riconosciuti:
//   - personaggi/oggetti:  `## IMMAGINE N — <titolo>`
//   - luoghi:              `## 🎨 Veduta N — <titolo>`  (anche senza emoji)
//
// Una "vista" = sezione H2 il cui titolo matcha il pattern sopra; il prompt
// è il contenuto del PRIMO fenced code block dentro quella sezione.
// Le altre sezioni H2 con fenced block (es. stylesheet, canone personaggio,
// negative globale/specifici) confluiscono in `globals`: testo riutilizzabile
// che la UI può concatenare al prompt vista.
//
// `filenameAtteso` (luoghi): estratto da una riga `**Filename atteso:** \`...\``
// nel preambolo della vista.
//
// Parser puro, niente dipendenze: usato lato server in next build e lato test
// con `node --test --experimental-strip-types`.

export interface PromptView {
  /** Titolo nudo (senza il `## ` né l'emoji). */
  title: string;
  /** Filename canonico atteso (dialetto luoghi). */
  filenameAtteso?: string;
  /** Contenuto del primo fenced block — testo da incollare in Grok. */
  prompt: string;
  /** Eventuale checklist successiva al fenced (testo grezzo, opzionale). */
  checklist?: string;
}

export interface PromptGlobal {
  /** Titolo della sezione H2 (es. "Negative prompt globale"). */
  title: string;
  /** Contenuto del primo fenced block della sezione. */
  text: string;
}

export interface ParsedPromptGrok {
  views: PromptView[];
  globals: PromptGlobal[];
}

const VIEW_TITLE_RE = /^(?:🎨\s*)?(?:IMMAGINE|Veduta)\s+\d+\b/i;
const FENCED_RE = /```(?:[a-zA-Z0-9_-]+)?\n([\s\S]*?)```/;
const FILENAME_RE = /\*\*Filename atteso:\*\*\s*`([^`\n]+)`/;

/** Split del markdown in sezioni H2: ritorna array di `{ rawTitle, body }`. */
function splitH2(md: string): Array<{ rawTitle: string; body: string }> {
  const lines = md.split("\n");
  const sections: Array<{ rawTitle: string; body: string }> = [];
  let cur: { rawTitle: string; body: string[] } | null = null;
  for (const line of lines) {
    const h2 = line.match(/^##\s+(.+?)\s*$/);
    if (h2 && !line.startsWith("###")) {
      if (cur) sections.push({ rawTitle: cur.rawTitle, body: cur.body.join("\n") });
      cur = { rawTitle: h2[1], body: [] };
    } else if (cur) {
      cur.body.push(line);
    }
    // righe prima del primo H2 vengono ignorate (preambolo)
  }
  if (cur) sections.push({ rawTitle: cur.rawTitle, body: cur.body.join("\n") });
  return sections;
}

/** Estrae il primo fenced block; ritorna null se assente. */
function firstFenced(body: string): { code: string; afterIndex: number } | null {
  const m = FENCED_RE.exec(body);
  if (!m) return null;
  return { code: m[1], afterIndex: m.index + m[0].length };
}

/** Pulisce un titolo da emoji decorativi iniziali (mantiene il resto). */
function cleanTitle(raw: string): string {
  // Flag `u` necessaria: le emoji sono surrogate pairs UTF-16.
  return raw.replace(/^[🎨🖼️📸✨⭐]\s*/u, "").trim();
}

/**
 * Parser principale.
 *
 * Una sezione H2 con fenced block è:
 *   - una `view` se il titolo matcha `IMMAGINE N` o `Veduta N` (case insensitive,
 *     emoji opzionale);
 *   - altrimenti un `global` (stylesheet, canone, negative prompts, ecc.).
 *
 * Sezioni H2 SENZA fenced block vengono ignorate (sono solo testo narrativo).
 */
export function parsePromptGrok(md: string): ParsedPromptGrok {
  const views: PromptView[] = [];
  const globals: PromptGlobal[] = [];

  for (const sec of splitH2(md)) {
    const fenced = firstFenced(sec.body);
    if (!fenced) continue;
    const title = cleanTitle(sec.rawTitle);
    const isView = VIEW_TITLE_RE.test(sec.rawTitle.trim());
    if (isView) {
      const filenameMatch = sec.body.match(FILENAME_RE);
      const after = sec.body.slice(fenced.afterIndex).trim();
      views.push({
        title,
        ...(filenameMatch ? { filenameAtteso: filenameMatch[1] } : {}),
        prompt: fenced.code.trim(),
        ...(after ? { checklist: after } : {}),
      });
    } else {
      globals.push({ title, text: fenced.code.trim() });
    }
  }

  return { views, globals };
}

/**
 * Helper per la UI: concatena il prompt di una vista con uno o più globals
 * (es. "Copia con negative globale"). Il separatore è una riga vuota.
 */
export function concatWithGlobals(
  prompt: string,
  globals: PromptGlobal[],
): string {
  if (globals.length === 0) return prompt;
  return [prompt, ...globals.map((g) => g.text)].join("\n\n");
}
