// Singolo hook visivo come <details> espandibile.
// Server component: <details>/<summary> nativi gestiscono lo stato senza JS.
// Summary: P{n} · hook_id · location.id · status badges (loc dot, X/Y chars,
//   N sub, img ✓/TBD).
// Body: luogo, personaggi in scena, cammei offscreen, oggetti, note canoniche,
//   sotto-hook, testo (estratto).

import { ChevronRight } from "lucide-react";

import { cn } from "@/lib/utils";
import type {
  AuditedEntities,
  DashboardHook,
} from "@/lib/types-storie-dashboard";
import { EntityRow } from "@/components/storie-dashboard/entity-row";

interface HookItemProps {
  hook: DashboardHook;
  audited: AuditedEntities;
}

export function HookItem({ hook, audited }: HookItemProps) {
  const loc = hook.location ?? { id: "", variant: "" };
  const charsInScene = hook.characters_in_scene ?? [];
  const charsOff = hook.characters_offscreen_or_distant ?? [];
  const objsInScene = hook.objects_in_scene ?? [];
  const details = hook.canonical_details ?? [];
  const subhooksAnn = hook.subhooks_annotated ?? [];
  const text = hook.text_preview ?? hook.text_full ?? "";

  // Status summary
  const charsTotal = charsInScene.length + charsOff.length;
  const charsReady = charsInScene.filter(
    (cid) => (audited.personaggi[cid]?.n_images ?? 0) > 0,
  ).length;
  const locAud = loc.id ? audited.luoghi[loc.id] : undefined;
  const locDot: "ok" | "warn" | "missing" = !loc.id
    ? "missing"
    : (locAud?.n_images ?? 0) > 0
      ? "ok"
      : locAud?.prompt_grok
        ? "warn"
        : "missing";
  const imgReady = !!hook.image && hook.image !== "TBD";

  return (
    <details className="group rounded-md border border-rule-soft bg-paper open:bg-paper-soft">
      <summary
        className="flex cursor-pointer list-none flex-wrap items-center gap-x-3 gap-y-1 px-3 py-2.5 text-ink hover:bg-paper-soft"
      >
        <ChevronRight
          className="h-4 w-4 shrink-0 text-ink-faint transition-transform group-open:rotate-90"
          aria-hidden
        />
        <span className="inline-flex h-6 w-10 shrink-0 items-center justify-center rounded-full bg-rule-soft font-mono text-xs text-ink">
          P{hook.page}
        </span>
        <code className="font-mono text-xs text-ink-soft">{hook.hook_id}</code>
        <span className="font-mono text-sm text-ink">
          {loc.id ? (
            <>
              {loc.id}
              {loc.variant ? (
                <em className="font-serif text-ink-faint">
                  {" "}
                  ({loc.variant})
                </em>
              ) : null}
            </>
          ) : (
            <em className="font-serif italic text-accent-warm">no loc</em>
          )}
        </span>
        <span className="ml-auto flex flex-wrap items-center gap-1.5">
          <Dot tone={locDot} title={`luogo: ${locDot}`} />
          <span
            className="font-mono text-[10px] uppercase tracking-wider text-ink-faint"
            title="personaggi pronti / personaggi totali"
          >
            <span className="text-ink-soft">{charsReady}</span>/{charsTotal}{" "}
            char
          </span>
          {subhooksAnn.length > 0 && (
            <span className="rounded-full bg-rule-soft px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-ink-soft">
              {subhooksAnn.length} sub
            </span>
          )}
          <ImgStatusBadge ready={imgReady} />
        </span>
      </summary>

      <div className="space-y-4 border-t border-rule-soft px-4 py-4">
        {/* Luogo */}
        <Section title="Luogo (dove succede la scena)" emoji="📍">
          {loc.id ? (
            <EntityRow
              id={loc.id}
              kind="luogo"
              audit={audited.luoghi[loc.id]}
              variantNote={loc.variant}
            />
          ) : (
            <Empty>Location non specificata nelle annotazioni.</Empty>
          )}
        </Section>

        {/* Personaggi in scena */}
        <Section
          title={`Personaggi in scena (${charsInScene.length})`}
          emoji="👤"
        >
          {charsInScene.length > 0 ? (
            <div className="space-y-2">
              {charsInScene.map((cid) => (
                <EntityRow
                  key={cid}
                  id={cid}
                  kind="personaggio"
                  audit={audited.personaggi[cid]}
                />
              ))}
            </div>
          ) : (
            <Empty>nessun personaggio in scena</Empty>
          )}

          {charsOff.length > 0 && (
            <div className="mt-3 rounded-md border border-rule-soft bg-paper-soft/40 p-3">
              <h5 className="mb-2 font-mono text-[11px] uppercase tracking-wider text-ink-soft">
                Cammei / sagome / sonori
              </h5>
              <div className="space-y-2">
                {charsOff.map((cid) => (
                  <EntityRow
                    key={cid}
                    id={cid}
                    kind="personaggio"
                    audit={audited.personaggi[cid]}
                    isOffscreen
                  />
                ))}
              </div>
            </div>
          )}
        </Section>

        {/* Oggetti */}
        {objsInScene.length > 0 && (
          <Section
            title={`Oggetti in scena (${objsInScene.length})`}
            emoji="📦"
          >
            <div className="space-y-2">
              {objsInScene.map((oid) => (
                <EntityRow
                  key={oid}
                  id={oid}
                  kind="oggetto"
                  audit={audited.oggetti[oid]}
                />
              ))}
            </div>
          </Section>
        )}

        {/* Note canoniche */}
        {details.length > 0 && (
          <Section title="Note canoniche" emoji="📌">
            <ul className="list-disc space-y-1 pl-5 font-serif text-sm text-ink-soft">
              {details.map((d, i) => (
                <li key={`${i}-${d.slice(0, 12)}`}>{d}</li>
              ))}
            </ul>
          </Section>
        )}

        {/* Sotto-hook */}
        {subhooksAnn.length > 0 && (
          <Section
            title={`Sotto-hook (${subhooksAnn.length}) — pagine libro fisiche`}
          >
            <ul className="space-y-1.5">
              {subhooksAnn.map((sh) => {
                const ready =
                  !!sh.image_status &&
                  sh.image_status !== "TBD" &&
                  !sh.image_status.toLowerCase().startsWith("tbd");
                return (
                  <li
                    key={sh.id}
                    className="flex flex-wrap items-center gap-x-3 gap-y-1 rounded-md border border-rule-soft bg-paper px-3 py-2"
                  >
                    <code className="font-mono text-xs text-ink">{sh.id}</code>
                    <span className="font-mono text-[11px] text-ink-faint">
                      pag. libro {String(sh.page_book)}
                    </span>
                    <ImgStatusBadge ready={ready} />
                    {sh.note && (
                      <span className="basis-full font-serif text-sm italic text-ink-soft">
                        {sh.note}
                      </span>
                    )}
                  </li>
                );
              })}
            </ul>
          </Section>
        )}

        {/* Testo */}
        {text && (
          <Section title="Testo (estratto)">
            <p className="whitespace-pre-line font-serif text-sm leading-relaxed text-ink">
              {text}
            </p>
          </Section>
        )}
      </div>
    </details>
  );
}

function Section({
  title,
  emoji,
  children,
}: {
  title: string;
  emoji?: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <h4 className="mb-2 font-mono text-[11px] uppercase tracking-wider text-ink-soft">
        {emoji && <span className="mr-1">{emoji}</span>}
        {title}
      </h4>
      {children}
    </div>
  );
}

function Empty({ children }: { children: React.ReactNode }) {
  return (
    <p className="font-serif text-sm italic text-ink-faint">{children}</p>
  );
}

function Dot({
  tone,
  title,
}: {
  tone: "ok" | "warn" | "missing";
  title: string;
}) {
  return (
    <span
      title={title}
      aria-hidden
      className={cn(
        "inline-block h-2.5 w-2.5 rounded-full",
        tone === "ok" && "bg-accent",
        tone === "warn" && "bg-accent-warm",
        tone === "missing" && "bg-rule",
      )}
    />
  );
}

function ImgStatusBadge({ ready }: { ready: boolean }) {
  return (
    <span
      className={cn(
        "rounded-full px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wider",
        ready
          ? "bg-accent/15 text-accent"
          : "bg-rule-soft text-ink-soft",
      )}
    >
      {ready ? "img ✓" : "img TBD"}
    </span>
  );
}
