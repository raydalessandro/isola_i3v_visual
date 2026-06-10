// /stato — Board canonizzazione F.2 (WI-6 catalogo v2).
//
// Per ogni "gruppo" del catalogo (fratelli/primari/secondari/cuccioli/
// collettivi/oggetti/luoghi-per-quartiere/venti/signatures): conteggio
// schede totali, con prompt grok, con immagini canoniche complete (4 per
// personaggio, 1-2 per oggetto). Tutto derivato da entities.json.

import Link from "next/link";
import {
  ArrowLeft,
  Check,
  Circle,
  CircleDashed,
} from "lucide-react";

import { getEntitiesData } from "@/lib/data";
import type { Entity } from "@/lib/types";

export const dynamic = "force-static";
export const metadata = {
  title: "Stato canonizzazione — L'Isola dei Tre Venti",
};

interface Group {
  label: string;
  expectedImages: number; // soglia "immagini complete"
  filter: (e: Entity) => boolean;
}

const GROUPS: Group[] = [
  {
    label: "Personaggi · fratelli",
    expectedImages: 4,
    filter: (e) =>
      e.famiglia === "personaggio" &&
      e.scheda_path.includes("/individuali/bambini/"),
  },
  {
    label: "Personaggi · primari",
    expectedImages: 4,
    filter: (e) =>
      e.famiglia === "personaggio" &&
      e.scheda_path.includes("/individuali/primari/"),
  },
  {
    label: "Personaggi · secondari",
    expectedImages: 4,
    filter: (e) =>
      e.famiglia === "personaggio" &&
      e.scheda_path.includes("/individuali/secondari/"),
  },
  {
    label: "Personaggi · cuccioli",
    expectedImages: 4,
    filter: (e) =>
      e.famiglia === "personaggio" &&
      e.scheda_path.includes("/individuali/cuccioli/"),
  },
  {
    label: "Personaggi · collettivi",
    expectedImages: 1,
    filter: (e) =>
      e.famiglia === "personaggio" &&
      e.scheda_path.includes("/collettivi/"),
  },
  {
    label: "Oggetti",
    expectedImages: 1,
    filter: (e) => e.famiglia === "oggetto",
  },
  {
    label: "Venti",
    expectedImages: 1,
    filter: (e) => e.famiglia === "vento",
  },
  {
    label: "Signatures",
    expectedImages: 1,
    filter: (e) => e.famiglia === "visual_signature",
  },
  {
    label: "Luoghi · centro",
    expectedImages: 1,
    filter: (e) => e.famiglia === "luogo" && e.quartiere === "centro",
  },
  {
    label: "Luoghi · fuoco",
    expectedImages: 1,
    filter: (e) => e.famiglia === "luogo" && e.quartiere === "fuoco",
  },
  {
    label: "Luoghi · acqua",
    expectedImages: 1,
    filter: (e) => e.famiglia === "luogo" && e.quartiere === "acqua",
  },
  {
    label: "Luoghi · aria",
    expectedImages: 1,
    filter: (e) => e.famiglia === "luogo" && e.quartiere === "aria",
  },
  {
    label: "Luoghi · terra",
    expectedImages: 1,
    filter: (e) => e.famiglia === "luogo" && e.quartiere === "terra",
  },
  {
    label: "Luoghi · perimetro",
    expectedImages: 1,
    filter: (e) => e.famiglia === "luogo" && e.quartiere === "perimetro",
  },
  {
    label: "Luoghi · altri",
    expectedImages: 1,
    filter: (e) =>
      e.famiglia === "luogo" &&
      !["centro", "fuoco", "acqua", "aria", "terra", "perimetro"].includes(
        e.quartiere || "",
      ),
  },
];

export default async function StatoPage() {
  const data = await getEntitiesData();

  return (
    <main className="mx-auto max-w-6xl space-y-8 px-6 py-10">
      <header className="space-y-2 border-b border-rule-soft pb-4">
        <Link
          href="/"
          className="inline-flex items-center gap-1 font-mono text-xs text-ink-faint hover:text-accent"
        >
          <ArrowLeft className="h-3 w-3" aria-hidden />
          Home
        </Link>
        <h1 className="font-serif text-3xl font-semibold text-ink md:text-4xl">
          Stato canonizzazione (F.2)
        </h1>
        <p className="text-sm text-ink-soft">
          Una riga per gruppo. Cerchio pieno = scheda con almeno la soglia di
          immagini canoniche; cerchio tratteggiato = ha prompt ma mancano
          immagini; cerchio vuoto = ancora da lavorare.
        </p>
      </header>

      <div className="space-y-6">
        {GROUPS.map((g) => {
          const list = data.entities.filter(g.filter);
          if (list.length === 0) return null;
          const conPrompt = list.filter((e) => e.has_prompt_grok).length;
          const conImg = list.filter(
            (e) => (e.n_images || 0) >= g.expectedImages,
          ).length;
          const canonico = list.filter((e) => e.status === "canonico").length;
          const sorted = [...list].sort((a, b) => {
            const sa = score(a, g.expectedImages);
            const sb = score(b, g.expectedImages);
            if (sb !== sa) return sb - sa;
            return a.name.localeCompare(b.name);
          });
          return (
            <section
              key={g.label}
              aria-label={g.label}
              className="rounded-md border border-rule-soft bg-paper-soft"
            >
              <header className="flex flex-wrap items-baseline justify-between gap-2 border-b border-rule-soft px-4 py-3">
                <h2 className="font-serif text-lg font-semibold text-ink">
                  {g.label}
                </h2>
                <p className="font-mono text-[11px] text-ink-faint">
                  {canonico}/{list.length} canoniche · {conPrompt}/{list.length}{" "}
                  con prompt · {conImg}/{list.length} immagini complete
                </p>
              </header>
              <ul className="divide-y divide-rule-soft/60">
                {sorted.map((e) => (
                  <li key={e.id}>
                    <Link
                      href={`/catalogo/${e.id}`}
                      className="flex items-center gap-3 px-4 py-2 hover:bg-rule-soft/30"
                    >
                      <StatusDot
                        nImages={e.n_images || 0}
                        expected={g.expectedImages}
                        hasPrompt={!!e.has_prompt_grok}
                      />
                      <span className="flex-1 truncate text-sm text-ink">
                        {e.name}
                      </span>
                      <span className="font-mono text-[10px] text-ink-faint">
                        {e.n_images || 0} img
                      </span>
                      <span
                        className={
                          e.status === "canonico"
                            ? "rounded bg-accent/15 px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-accent"
                            : "rounded border border-rule-soft px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-ink-faint"
                        }
                      >
                        {e.status}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </section>
          );
        })}
      </div>
    </main>
  );
}

function score(e: Entity, expected: number): number {
  // Ordina mettendo prima le entità più "avanti" nel lavoro:
  // canonico > immagini complete > ha prompt > nulla.
  let s = 0;
  if (e.status === "canonico") s += 100;
  if ((e.n_images || 0) >= expected) s += 50;
  if (e.has_prompt_grok) s += 10;
  s += Math.min(e.n_images || 0, expected);
  return s;
}

function StatusDot({
  nImages,
  expected,
  hasPrompt,
}: {
  nImages: number;
  expected: number;
  hasPrompt: boolean;
}) {
  if (nImages >= expected) {
    return (
      <Check
        className="h-3.5 w-3.5 shrink-0 text-accent"
        aria-label="completo"
      />
    );
  }
  if (hasPrompt) {
    return (
      <CircleDashed
        className="h-3.5 w-3.5 shrink-0 text-ink-soft"
        aria-label="ha prompt"
      />
    );
  }
  return (
    <Circle
      className="h-3.5 w-3.5 shrink-0 text-ink-faint"
      aria-label="da lavorare"
    />
  );
}
