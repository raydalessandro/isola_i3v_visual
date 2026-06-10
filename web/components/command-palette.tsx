"use client";

// CommandPalette — WI-5 catalogo v2.
//
// Cmd+K / Ctrl+K apre un dialog con input di ricerca + lista risultati che
// indicizza tutte le entità del catalogo e le 12 storie (più i titoli delle
// loro sezioni). Match testuale semplice su label / id / sezioni — niente
// dipendenze esterne (la spec lo vieta esplicitamente).
//
// Lo scope è "navigazione veloce", non full-text search del body — è il
// tradeoff esplicito della spec.

import * as React from "react";
import { useRouter } from "next/navigation";
import { Search, Sparkles, BookOpen, MapPin } from "lucide-react";

import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { cn } from "@/lib/utils";

interface SearchSection {
  title: string;
  slug: string;
}
interface SearchEntry {
  kind: "entity" | "storia";
  id: string;
  label: string;
  categoria: string;
  sottotipo?: string;
  quartiere?: string;
  status?: string;
  href: string;
  sections: SearchSection[];
}
interface SearchIndex {
  generated_at: string;
  count: number;
  entries: SearchEntry[];
}

/**
 * Risultato di ricerca normalizzato: ogni voce è o l'entità intera o una
 * sezione di una entità (così l'utente atterra sulla sezione giusta).
 */
interface ResultItem {
  key: string;
  kind: SearchEntry["kind"] | "section";
  label: string;
  context: string;
  href: string;
}

function norm(s: string): string {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "");
}

/** Score molto semplice: bonus se il match è a inizio parola. */
function matches(needle: string, haystack: string): number {
  const n = norm(needle.trim());
  if (!n) return 0;
  const h = norm(haystack);
  const idx = h.indexOf(n);
  if (idx === -1) return 0;
  // bonus se a inizio stringa o inizio parola
  if (idx === 0) return 100;
  if (idx > 0 && /\s|[-_/]/.test(h[idx - 1])) return 50;
  return 10;
}

function search(index: SearchEntry[], query: string, max = 30): ResultItem[] {
  if (!query.trim()) {
    // Default: prime 12 entità + 12 storie come "tutto"
    return index.slice(0, max).map((e) => ({
      key: `e-${e.id}`,
      kind: e.kind,
      label: e.label,
      context:
        e.kind === "storia"
          ? "storia"
          : `${e.categoria}${e.sottotipo ? ` · ${e.sottotipo}` : ""}${
              e.quartiere ? ` · ${e.quartiere}` : ""
            }`,
      href: e.href,
    }));
  }

  const scored: { item: ResultItem; score: number }[] = [];
  for (const e of index) {
    const labelScore = matches(query, e.label) + matches(query, e.id) * 0.5;
    if (labelScore > 0) {
      scored.push({
        item: {
          key: `e-${e.id}`,
          kind: e.kind,
          label: e.label,
          context:
            e.kind === "storia"
              ? "storia"
              : `${e.categoria}${e.sottotipo ? ` · ${e.sottotipo}` : ""}${
                  e.quartiere ? ` · ${e.quartiere}` : ""
                }`,
          href: e.href,
        },
        score: labelScore + 1, // bias verso l'entità prima delle sue sezioni
      });
    }
    for (const sec of e.sections) {
      const s = matches(query, sec.title);
      if (s > 0) {
        scored.push({
          item: {
            key: `s-${e.id}-${sec.slug}`,
            kind: "section",
            label: sec.title,
            context: `${e.label} · sezione`,
            href: `${e.href}#${sec.slug}`,
          },
          score: s,
        });
      }
    }
  }
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, max).map((s) => s.item);
}

export function CommandPalette() {
  const router = useRouter();
  const [open, setOpen] = React.useState(false);
  const [query, setQuery] = React.useState("");
  const [activeIdx, setActiveIdx] = React.useState(0);
  const [index, setIndex] = React.useState<SearchEntry[] | null>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  // Carica l'indice solo al primo open (non blocca initial load).
  React.useEffect(() => {
    if (!open || index !== null) return;
    let cancelled = false;
    fetch("/data/search-index.json", { cache: "force-cache" })
      .then((r) => r.json() as Promise<SearchIndex>)
      .then((data) => {
        if (!cancelled) setIndex(data.entries);
      })
      .catch(() => {
        if (!cancelled) setIndex([]);
      });
    return () => {
      cancelled = true;
    };
  }, [open, index]);

  // ⌘K / Ctrl+K toggle
  React.useEffect(() => {
    function onKey(ev: KeyboardEvent) {
      if ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === "k") {
        ev.preventDefault();
        setOpen((v) => !v);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  // Focus input quando si apre
  React.useEffect(() => {
    if (open) {
      setQuery("");
      setActiveIdx(0);
      // Il Dialog di shadcn fa il focus management; rinforzo dopo paint.
      setTimeout(() => inputRef.current?.focus(), 30);
    }
  }, [open]);

  const results = React.useMemo(
    () => (index ? search(index, query) : []),
    [index, query],
  );

  React.useEffect(() => {
    setActiveIdx(0);
  }, [query]);

  const navigate = React.useCallback(
    (href: string) => {
      setOpen(false);
      router.push(href);
    },
    [router],
  );

  function onInputKey(ev: React.KeyboardEvent<HTMLInputElement>) {
    if (ev.key === "ArrowDown") {
      ev.preventDefault();
      setActiveIdx((i) => Math.min(i + 1, results.length - 1));
    } else if (ev.key === "ArrowUp") {
      ev.preventDefault();
      setActiveIdx((i) => Math.max(i - 1, 0));
    } else if (ev.key === "Enter") {
      ev.preventDefault();
      const r = results[activeIdx];
      if (r) navigate(r.href);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="top-[20%] max-w-2xl translate-y-0 p-0 sm:rounded-lg">
        <div className="sr-only">
          <DialogTitle>Cerca</DialogTitle>
          <DialogDescription>
            Cerca tra entità, storie e sezioni del catalogo
          </DialogDescription>
        </div>

        <div className="flex items-center gap-2 border-b border-rule-soft px-4 py-3">
          <Search className="h-4 w-4 shrink-0 text-ink-faint" aria-hidden />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={onInputKey}
            placeholder="Cerca entità, storie, sezioni…"
            className="flex-1 bg-transparent text-sm outline-none placeholder:text-ink-faint"
            aria-label="Cerca"
          />
          <kbd className="hidden rounded border border-rule-soft px-1.5 py-0.5 font-mono text-[10px] text-ink-faint sm:inline">
            esc
          </kbd>
        </div>

        <ul
          className="max-h-[60vh] overflow-y-auto py-1"
          role="listbox"
          aria-label="Risultati"
        >
          {index === null && (
            <li className="px-4 py-6 text-sm text-ink-faint">Caricamento…</li>
          )}
          {index !== null && results.length === 0 && (
            <li className="px-4 py-6 text-sm text-ink-faint">
              Nessun risultato. Prova un titolo di sezione (es. &quot;coerenza&quot;).
            </li>
          )}
          {results.map((r, i) => (
            <li key={r.key}>
              <button
                type="button"
                onClick={() => navigate(r.href)}
                onMouseEnter={() => setActiveIdx(i)}
                className={cn(
                  "flex w-full items-start gap-3 px-4 py-2.5 text-left",
                  i === activeIdx
                    ? "bg-rule-soft/50 text-ink"
                    : "text-ink-soft hover:bg-rule-soft/30",
                )}
                role="option"
                aria-selected={i === activeIdx}
              >
                <ResultIcon kind={r.kind} />
                <span className="flex-1 min-w-0">
                  <span className="block truncate text-sm font-medium">
                    {r.label}
                  </span>
                  <span className="block truncate text-xs text-ink-faint">
                    {r.context}
                  </span>
                </span>
              </button>
            </li>
          ))}
        </ul>

        <div className="flex items-center justify-between border-t border-rule-soft px-4 py-2 font-mono text-[10px] text-ink-faint">
          <span>
            <kbd className="rounded border border-rule-soft px-1">↑↓</kbd> per
            navigare · <kbd className="rounded border border-rule-soft px-1">⏎</kbd>{" "}
            per aprire
          </span>
          <span>
            {index ? `${results.length} risultati` : ""}
          </span>
        </div>
      </DialogContent>
    </Dialog>
  );
}

function ResultIcon({ kind }: { kind: ResultItem["kind"] }) {
  if (kind === "storia")
    return <BookOpen className="h-4 w-4 shrink-0 text-ink-faint" aria-hidden />;
  if (kind === "section")
    return <Sparkles className="h-4 w-4 shrink-0 text-ink-faint" aria-hidden />;
  return <MapPin className="h-4 w-4 shrink-0 text-ink-faint" aria-hidden />;
}
