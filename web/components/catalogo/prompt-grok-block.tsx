"use client";

// PromptGrokBlock — WI-1 catalogo v2.
//
// La collaboratrice che genera immagini deve copiare il prompt esatto di
// UNA vista con un click. Prima questo blocco mostrava solo l'HTML reso
// del file md (niente copia). Ora: parser strutturato + CopyButton per
// ogni vista + scorciatoia "Copia con negative globale" + "Copia tutto il
// file" in testa. Le viste sono aperte di default (lo scopo del blocco
// è renderle accessibili in un click).

import * as React from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

import { cn } from "@/lib/utils";
import { CopyButton } from "@/components/storie-dashboard/copy-button";
import {
  parsePromptGrok,
  concatWithGlobals,
  type ParsedPromptGrok,
} from "@/lib/prompt-grok";

interface PromptGrokBlockProps {
  promptMd: string;
}

export function PromptGrokBlock({ promptMd }: PromptGrokBlockProps) {
  const parsed: ParsedPromptGrok = React.useMemo(
    () => parsePromptGrok(promptMd),
    [promptMd],
  );

  if (parsed.views.length === 0 && parsed.globals.length === 0) {
    // File senza H2 con fenced (raro / malformato): fallback al raw md
    // come <pre> per non perdere contenuto.
    return (
      <section className="rounded-md border border-rule-soft bg-paper-soft p-4">
        <p className="mb-2 font-mono text-xs uppercase tracking-wider text-ink-soft">
          Prompt Grok (raw)
        </p>
        <pre className="overflow-x-auto whitespace-pre-wrap text-sm text-ink-soft">
          {promptMd}
        </pre>
      </section>
    );
  }

  return (
    <section
      aria-label="Prompt Grok"
      className="rounded-md border border-rule-soft bg-paper-soft"
    >
      <header className="flex flex-wrap items-center justify-between gap-3 border-b border-rule-soft px-4 py-3">
        <div>
          <p className="font-mono text-xs uppercase tracking-wider text-ink-soft">
            Prompt Grok
          </p>
          <p className="text-xs text-ink-faint">
            {parsed.views.length}{" "}
            {parsed.views.length === 1 ? "vista" : "viste"}
            {parsed.globals.length > 0 && (
              <>
                {" · "}
                {parsed.globals.length} blocchi globali
              </>
            )}
          </p>
        </div>
        <CopyButton text={promptMd} label="Copia tutto il file" />
      </header>

      <div className="divide-y divide-rule-soft/60">
        {parsed.views.map((v, i) => (
          <ViewCard
            key={`view-${i}`}
            title={v.title}
            prompt={v.prompt}
            filenameAtteso={v.filenameAtteso}
            checklist={v.checklist}
            globals={parsed.globals}
            defaultOpen={i === 0}
          />
        ))}
      </div>

      {parsed.globals.length > 0 && (
        <GlobalsSection globals={parsed.globals} />
      )}
    </section>
  );
}

// ─── ViewCard ───────────────────────────────────────────────────────────────

interface ViewCardProps {
  title: string;
  prompt: string;
  filenameAtteso?: string;
  checklist?: string;
  globals: ParsedPromptGrok["globals"];
  defaultOpen?: boolean;
}

function ViewCard({
  title,
  prompt,
  filenameAtteso,
  checklist,
  globals,
  defaultOpen,
}: ViewCardProps) {
  const [open, setOpen] = React.useState(!!defaultOpen);
  const promptWithGlobals = React.useMemo(
    () => concatWithGlobals(prompt, globals),
    [prompt, globals],
  );

  return (
    <article className="px-4 py-3">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-3 text-left"
      >
        <span className="flex items-center gap-2">
          {open ? (
            <ChevronDown className="h-4 w-4 shrink-0 text-ink-faint" aria-hidden />
          ) : (
            <ChevronRight className="h-4 w-4 shrink-0 text-ink-faint" aria-hidden />
          )}
          <span className="font-medium text-ink">{title}</span>
        </span>
        {filenameAtteso && (
          <code className="hidden truncate font-mono text-xs text-ink-faint md:inline">
            {filenameAtteso}
          </code>
        )}
      </button>

      {open && (
        <div className="mt-3 space-y-3 pl-6">
          {filenameAtteso && (
            <p className="font-mono text-xs text-ink-faint md:hidden">
              Filename: {filenameAtteso}
            </p>
          )}
          <pre className="overflow-x-auto whitespace-pre-wrap rounded border border-rule-soft bg-paper px-3 py-2 text-sm text-ink">
            {prompt}
          </pre>
          <div className="flex flex-wrap items-center gap-2">
            <CopyButton text={prompt} label="Copia prompt" />
            {globals.length > 0 && (
              <CopyButton
                text={promptWithGlobals}
                label={`Copia con ${globals.length} blocchi globali`}
              />
            )}
          </div>
          {checklist && (
            <details className="text-sm text-ink-soft">
              <summary className="cursor-pointer font-mono text-xs uppercase tracking-wider text-ink-faint">
                Checklist / note
              </summary>
              <pre className="mt-2 whitespace-pre-wrap text-sm">{checklist}</pre>
            </details>
          )}
        </div>
      )}
    </article>
  );
}

// ─── GlobalsSection ─────────────────────────────────────────────────────────

function GlobalsSection({
  globals,
}: {
  globals: ParsedPromptGrok["globals"];
}) {
  const [open, setOpen] = React.useState(false);
  return (
    <div className="border-t border-rule-soft">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-3 px-4 py-2.5 text-left hover:bg-rule-soft/30"
      >
        <span className="font-mono text-xs uppercase tracking-wider text-ink-soft">
          Blocchi globali ({globals.length})
        </span>
        <ChevronDown
          className={cn(
            "h-4 w-4 shrink-0 text-ink-faint transition-transform",
            open && "rotate-180",
          )}
          aria-hidden
        />
      </button>
      {open && (
        <ul className="divide-y divide-rule-soft/60">
          {globals.map((g, i) => (
            <li key={`g-${i}`} className="px-4 py-3">
              <div className="flex items-center justify-between gap-2">
                <span className="text-sm font-medium text-ink">{g.title}</span>
                <CopyButton text={g.text} label="Copia" />
              </div>
              <pre className="mt-2 overflow-x-auto whitespace-pre-wrap rounded border border-rule-soft bg-paper px-3 py-2 text-sm text-ink-soft">
                {g.text}
              </pre>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
