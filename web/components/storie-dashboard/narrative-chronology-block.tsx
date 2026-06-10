// Cronologia narrativa di una storia: semi piantati/raccolti/maturati/sbocciati
// + callback fatti. Letto dal grafo via narrative_chronology in storie-dashboard.json.
//
// Lo schema visivo riusa il vocabolario stagionale del progetto:
//   🌱 piantati  → set up per future storie
//   🌾 raccolti  → semi originati da storie precedenti
//   🌿 maturano  → passaggi intermedi
//   🌸 sbocciati → payoff / chiusura
//   🔁 callback  → richiami espliciti
//
// Server Component (niente state).

import type { NarrativeChronology } from "@/lib/types-storie-dashboard";

interface Props {
  chronology: NarrativeChronology | undefined;
}

interface SeedRow {
  emoji: string;
  label: string;
  items: string[];
  hint: string;
}

export function NarrativeChronologyBlock({ chronology }: Props) {
  if (!chronology) return null;

  const planted = chronology.seeds_planted ?? [];
  const pickedUp = chronology.seeds_picked_up ?? [];
  const maturing = chronology.seeds_maturing_here ?? [];
  const bloomed = chronology.seeds_bloomed_here ?? [];
  const callbacks = chronology.callbacks_made ?? [];
  const summary = chronology.callback_summary ?? "";

  const totalSeeds =
    planted.length + pickedUp.length + maturing.length + bloomed.length;
  if (totalSeeds === 0 && callbacks.length === 0 && !summary) return null;

  const rows: SeedRow[] = [
    {
      emoji: "🌱",
      label: "Pianta",
      items: planted,
      hint: "set up per future storie",
    },
    {
      emoji: "🌾",
      label: "Raccoglie",
      items: pickedUp,
      hint: "originati da storie precedenti",
    },
    {
      emoji: "🌿",
      label: "Matura",
      items: maturing,
      hint: "passaggi intermedi",
    },
    {
      emoji: "🌸",
      label: "Sboccia",
      items: bloomed,
      hint: "payoff / chiusura",
    },
  ];

  return (
    <section
      aria-label="Cronologia narrativa"
      className="rounded-md border border-rule-soft bg-paper-soft"
    >
      <header className="border-b border-rule-soft px-4 py-3">
        <h2 className="font-mono text-xs uppercase tracking-wider text-ink-soft">
          Cronologia semi
        </h2>
        <p className="text-xs text-ink-faint">
          Posizione della storia nell&apos;arco narrativo: cosa lascia, cosa
          raccoglie, cosa fa fiorire.
        </p>
      </header>

      <div className="grid gap-px bg-rule-soft/40 sm:grid-cols-2">
        {rows.map((r) => (
          <div key={r.label} className="bg-paper-soft px-4 py-3">
            <div className="flex items-baseline gap-2">
              <span aria-hidden className="text-base">
                {r.emoji}
              </span>
              <h3 className="font-serif text-base font-semibold text-ink">
                {r.label}
              </h3>
              <span className="ml-auto font-mono text-xs text-ink-faint">
                {r.items.length}
              </span>
            </div>
            <p className="mb-2 text-xs text-ink-faint">{r.hint}</p>
            {r.items.length > 0 ? (
              <ul className="space-y-0.5 font-mono text-[11px] text-ink-soft">
                {r.items.map((id) => (
                  <li key={id} className="truncate">
                    <code>{id}</code>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="font-serif text-sm italic text-ink-faint">—</p>
            )}
          </div>
        ))}
      </div>

      {(callbacks.length > 0 || summary) && (
        <div className="border-t border-rule-soft px-4 py-3">
          <div className="flex items-baseline gap-2">
            <span aria-hidden className="text-base">
              🔁
            </span>
            <h3 className="font-serif text-base font-semibold text-ink">
              Callback espliciti
            </h3>
            <span className="ml-auto font-mono text-xs text-ink-faint">
              {callbacks.length}
            </span>
          </div>
          {summary && (
            <p className="mt-1 font-serif text-sm italic leading-relaxed text-ink-soft">
              {summary}
            </p>
          )}
          {callbacks.length > 0 && (
            <ul className="mt-2 space-y-1 font-mono text-[11px] text-ink-soft">
              {callbacks.map((cb, i) => (
                <li key={i} className="flex items-baseline gap-2">
                  <span className="text-ink-faint">·</span>
                  <CallbackEntry cb={cb} />
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </section>
  );
}

function CallbackEntry({
  cb,
}: {
  cb: { from_story?: string; type?: string; summary?: string } | string;
}) {
  if (typeof cb === "string") return <code>{cb}</code>;
  const from = cb.from_story ? <code className="text-ink">{cb.from_story}</code> : null;
  return (
    <span className="flex flex-wrap items-baseline gap-2">
      {from}
      {cb.type && <span className="text-ink-faint">[{cb.type}]</span>}
      {cb.summary && (
        <span className="font-serif text-sm italic text-ink-soft">
          {cb.summary}
        </span>
      )}
    </span>
  );
}
