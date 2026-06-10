"use client";

import * as React from "react";
import {
  ChevronDown,
  ChevronsDownUp,
  ChevronsUpDown,
  Check,
  Link as LinkIcon,
} from "lucide-react";

import type { MarkdownSection } from "@/lib/markdown";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface EntityBodyProps {
  preambleHtml: string;
  sections: MarkdownSection[];
}

/**
 * Body markdown: preambolo aperto + sezioni `##` collassabili (default chiuse).
 * Toolbar in cima con Espandi tutto / Comprimi tutto.
 *
 * WI-4 catalogo v2:
 *   - su mount, se `location.hash` matcha una sezione → la apre + scrolla;
 *   - hover su ogni titolo mostra icona "link" che copia il permalink
 *     `/catalogo/<id>#<sezione>` negli appunti.
 */
export function EntityBody({ preambleHtml, sections }: EntityBodyProps) {
  const [openMap, setOpenMap] = React.useState<Record<string, boolean>>({});

  const allOpen =
    sections.length > 0 && sections.every((s) => openMap[s.id] === true);
  const allClosed =
    sections.length > 0 && sections.every((s) => !openMap[s.id]);

  // Apri + scrolla alla sezione indicata dal hash. Esegue una volta sul mount
  // e su ogni cambio di hash (back/forward del browser).
  React.useEffect(() => {
    function openFromHash() {
      const raw = window.location.hash.replace(/^#/, "");
      if (!raw) return;
      const target = sections.find((s) => s.id === raw);
      if (!target) return;
      setOpenMap((m) => ({ ...m, [target.id]: true }));
      // Attendi il prossimo frame: la sezione deve essere espansa prima di
      // poter scrollare correttamente.
      requestAnimationFrame(() => {
        const el = document.getElementById(`section-${target.id}`);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }
    openFromHash();
    window.addEventListener("hashchange", openFromHash);
    return () => window.removeEventListener("hashchange", openFromHash);
  }, [sections]);

  function expandAll() {
    const next: Record<string, boolean> = {};
    for (const s of sections) next[s.id] = true;
    setOpenMap(next);
  }

  function collapseAll() {
    setOpenMap({});
  }

  function toggle(id: string) {
    setOpenMap((m) => ({ ...m, [id]: !m[id] }));
  }

  return (
    <section aria-label="Scheda" className="space-y-4">
      {preambleHtml && (
        <div
          className="prose-saga"
          dangerouslySetInnerHTML={{ __html: preambleHtml }}
        />
      )}

      {sections.length > 0 && (
        <>
          <div className="flex items-center justify-between gap-2 border-b border-rule-soft pb-2">
            <span className="font-mono text-[10px] uppercase tracking-wider text-ink-faint">
              {sections.length} sezion{sections.length === 1 ? "e" : "i"}
            </span>
            <div className="flex gap-1">
              <Button
                size="sm"
                variant="ghost"
                onClick={expandAll}
                disabled={allOpen}
                className="font-mono text-xs"
              >
                <ChevronsUpDown className="h-3.5 w-3.5" />
                Espandi tutto
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={collapseAll}
                disabled={allClosed}
                className="font-mono text-xs"
              >
                <ChevronsDownUp className="h-3.5 w-3.5" />
                Comprimi tutto
              </Button>
            </div>
          </div>

          <div className="space-y-2">
            {sections.map((s) => (
              <SectionCollapsible
                key={s.id}
                section={s}
                open={!!openMap[s.id]}
                onToggle={() => toggle(s.id)}
              />
            ))}
          </div>
        </>
      )}
    </section>
  );
}

interface SectionCollapsibleProps {
  section: MarkdownSection;
  open: boolean;
  onToggle: () => void;
}

function SectionCollapsible({
  section,
  open,
  onToggle,
}: SectionCollapsibleProps) {
  return (
    <div
      id={`section-${section.id}`}
      className="rounded-md border border-rule-soft bg-paper-soft scroll-mt-20"
    >
      <div className="group flex items-center gap-1 px-4 py-3 hover:bg-rule-soft/30 rounded-md">
        <button
          type="button"
          onClick={onToggle}
          aria-expanded={open}
          aria-controls={`section-body-${section.id}`}
          className="flex flex-1 items-center justify-between gap-3 text-left"
        >
          <h2 className="font-serif text-lg font-semibold text-ink truncate">
            {section.title}
          </h2>
          <ChevronDown
            aria-hidden
            className={cn(
              "h-4 w-4 shrink-0 transition-transform",
              open && "rotate-180",
            )}
          />
        </button>
        <PermalinkButton sectionId={section.id} />
      </div>
      {open && (
        <div
          id={`section-body-${section.id}`}
          className="prose-saga border-t border-rule-soft px-4 py-4"
          dangerouslySetInnerHTML={{ __html: section.bodyHtml }}
        />
      )}
    </div>
  );
}

function PermalinkButton({ sectionId }: { sectionId: string }) {
  const [copied, setCopied] = React.useState(false);

  const onClick = React.useCallback(
    async (e: React.MouseEvent) => {
      e.stopPropagation();
      try {
        const url = `${window.location.origin}${window.location.pathname}#${sectionId}`;
        await navigator.clipboard.writeText(url);
        // aggiorna anche l'URL nella barra senza ricaricare
        history.replaceState(null, "", `#${sectionId}`);
        setCopied(true);
        setTimeout(() => setCopied(false), 1500);
      } catch {
        // clipboard non disponibile: ignora silenziosamente
      }
    },
    [sectionId],
  );

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={copied ? "Permalink copiato" : "Copia permalink sezione"}
      className={cn(
        "shrink-0 rounded p-1 opacity-0 transition-opacity group-hover:opacity-100 focus:opacity-100",
        copied ? "text-accent" : "text-ink-faint hover:text-accent",
      )}
    >
      {copied ? (
        <Check className="h-3.5 w-3.5" />
      ) : (
        <LinkIcon className="h-3.5 w-3.5" />
      )}
    </button>
  );
}
