import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, BookOpen } from "lucide-react";

import { getAllStorie } from "@/lib/storie";
import { CYCLE_LABEL } from "@/lib/types-storie";
import { Badge } from "@/components/ui/badge";

export const metadata: Metadata = {
  title: "Storie del libro — L'Isola dei Tre Venti",
  description:
    "Le 12 storie illustrate della saga: prosa definitiva + immagini-scena pagina per pagina.",
};

function asStr(v: unknown): string | null {
  return typeof v === "string" && v.trim() ? v : null;
}

export default async function StorieIndexPage() {
  const storie = await getAllStorie();

  // Raggruppa per ciclo (A/B/C/D), conservando ordine sNN.
  const byCycle = new Map<string, typeof storie>();
  for (const s of storie) {
    const cycle = asStr(s.frontmatter.cycle) ?? "?";
    if (!byCycle.has(cycle)) byCycle.set(cycle, []);
    byCycle.get(cycle)!.push(s);
  }
  const cycleOrder = ["A", "B", "C", "D"].filter((c) => byCycle.has(c));
  // eventuali cicli ignoti li accodiamo
  for (const c of byCycle.keys()) if (!cycleOrder.includes(c)) cycleOrder.push(c);

  const totalPages = storie.reduce((acc, s) => acc + s.pages.length, 0);

  return (
    <main className="mx-auto max-w-5xl px-6 py-10 space-y-10">
      <header className="space-y-3 border-b border-rule-soft pb-6">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-wider text-ink-faint hover:text-accent"
        >
          <ArrowLeft className="h-3 w-3" aria-hidden />
          Home cruscotto
        </Link>
        <div className="flex items-center gap-2 text-accent-warm">
          <BookOpen className="h-5 w-5" aria-hidden />
          <span className="font-mono text-xs uppercase tracking-wider">
            Storie del libro
          </span>
        </div>
        <h1 className="font-serif text-4xl font-semibold tracking-tight text-ink">
          Le 12 storie della saga
        </h1>
        <p className="font-serif text-lg italic text-ink-soft max-w-2xl">
          Prosa definitiva, suddivisa per pagina libro fisica. {storie.length}{" "}
          storie · {totalPages} pagine totali.
        </p>
      </header>

      {cycleOrder.map((cycle) => (
        <section key={cycle} aria-label={`Ciclo ${cycle}`} className="space-y-4">
          <h2 className="font-serif text-2xl font-semibold text-ink">
            {CYCLE_LABEL[cycle] ?? `Ciclo ${cycle}`}
          </h2>
          <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {byCycle.get(cycle)!.map((s) => {
              const status = asStr(s.frontmatter.status);
              const season = asStr(s.frontmatter.season);
              const wind = asStr(s.frontmatter.wind);
              const block = asStr(s.frontmatter.block);
              return (
                <li key={s.sid}>
                  <Link
                    href={`/storie/${s.sid}`}
                    className="group block h-full rounded-lg border border-rule-soft bg-paper-soft p-4 transition-colors hover:border-accent/40"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-mono text-[10px] uppercase tracking-wider text-ink-faint">
                        {s.sid.toUpperCase()}
                      </span>
                      <Badge variant="secondary" className="font-mono">
                        Ciclo {cycle}
                      </Badge>
                    </div>
                    <h3 className="mt-2 font-serif text-lg font-semibold text-ink leading-snug group-hover:text-accent">
                      {s.title}
                    </h3>
                    <div className="mt-3 flex flex-wrap items-center gap-1.5">
                      {status && (
                        <Badge
                          variant={status === "definitiva" ? "canonico" : "provvisorio"}
                        >
                          {status}
                        </Badge>
                      )}
                      {season && (
                        <Badge variant="warm">{season}</Badge>
                      )}
                      {wind && (
                        <Badge variant="accent">{wind}</Badge>
                      )}
                      {block && (
                        <Badge variant="outline">{block}</Badge>
                      )}
                    </div>
                    <div className="mt-3 flex items-center justify-between font-mono text-[11px] text-ink-faint">
                      <span>{s.hooks.length} hook narrativi</span>
                      <span>{s.pages.length} pagine libro</span>
                    </div>
                  </Link>
                </li>
              );
            })}
          </ul>
        </section>
      ))}
    </main>
  );
}
