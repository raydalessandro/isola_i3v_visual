// Home — workbench operativo (WI-6 catalogo v2).
//
// Sostituisce le card editoriali della v0.4.0 con un cruscotto orientato al
// lavoro: stato versione grafo, contatori canonico/provvisorio per categoria,
// quick links alle viste, ultime entità con immagini. I dati arrivano dal
// blocco `meta` di entities.json (WI-8).

import Link from "next/link";
import Image from "next/image";
import {
  ArrowRight,
  BookOpen,
  Compass,
  Layers,
  Map as MapIcon,
  Search,
  Activity,
} from "lucide-react";

import { getEntitiesData } from "@/lib/data";
import { imageUrl } from "@/lib/image-url";
import { FAMIGLIA_ORDER } from "@/lib/types";

export const dynamic = "force-static";

function formatDate(iso: string): string {
  if (!iso) return "—";
  return iso.slice(0, 10);
}

export default async function HomePage() {
  const data = await getEntitiesData();
  const meta = data.meta;
  const totals = data.totals;
  const byStatus = data.by_status;

  const perFamiglia = FAMIGLIA_ORDER.map((fam) => {
    const list = data.entities.filter((e) => e.famiglia === fam);
    const canonico = list.filter((e) => e.status === "canonico").length;
    const provvisorio = list.filter((e) => e.status === "provvisorio").length;
    const conImmagini = list.filter((e) => (e.n_images || 0) > 0).length;
    const conPrompt = list.filter((e) => e.has_prompt_grok).length;
    return {
      fam,
      totale: list.length,
      canonico,
      provvisorio,
      conImmagini,
      conPrompt,
    };
  }).filter((r) => r.totale > 0);

  const conImmagini = data.entities
    .filter((e) => (e.n_images || 0) > 0)
    .slice()
    .sort((a, b) => (b.n_images || 0) - (a.n_images || 0))
    .slice(0, 8);

  return (
    <main className="mx-auto max-w-6xl space-y-10 px-6 py-10">
      <header className="space-y-3 border-b border-rule-soft pb-6">
        <h1 className="font-serif text-4xl font-semibold tracking-tight text-ink md:text-5xl">
          L&apos;Isola dei Tre Venti
        </h1>
        <p className="font-serif italic text-lg text-ink-soft">
          Cruscotto editoriale
        </p>
        <div className="flex flex-wrap items-center gap-x-5 gap-y-1 font-mono text-xs text-ink-faint">
          {meta && (
            <>
              <span>
                Grafo{" "}
                <strong className="text-ink-soft">v{meta.graph_version}</strong>
                {" · schema "}
                <strong className="text-ink-soft">{meta.schema_version}</strong>
              </span>
              <span>
                Aggiornato:{" "}
                <strong className="text-ink-soft">
                  {formatDate(meta.graph_last_updated)}
                </strong>
              </span>
              <span>
                Build:{" "}
                <strong className="text-ink-soft">
                  {formatDate(meta.generated_at)}
                </strong>
              </span>
            </>
          )}
          <span className="ml-auto inline-flex items-center gap-1 text-ink-faint">
            <kbd className="rounded border border-rule px-1.5 py-0.5">⌘K</kbd>
            <span>per cercare ovunque</span>
          </span>
        </div>
      </header>

      <section aria-label="Sezioni" className="grid gap-3 md:grid-cols-3">
        <QuickLink
          href="/catalogo"
          icon={<Layers className="h-4 w-4" aria-hidden />}
          title="Catalogo"
          desc={`${totals.totale} entità · ${byStatus.canonico} canoniche · ${byStatus.provvisorio} in lavorazione`}
        />
        <QuickLink
          href="/storie"
          icon={<BookOpen className="h-4 w-4" aria-hidden />}
          title="Storie"
          desc="12 storie · 4 cicli · dashboard hook"
        />
        <QuickLink
          href="/mappa"
          icon={<MapIcon className="h-4 w-4" aria-hidden />}
          title="Mappa"
          desc="atlante illustrato dell'isola"
        />
        <QuickLink
          href="/orchestra"
          icon={<Compass className="h-4 w-4" aria-hidden />}
          title="Orchestra"
          desc="atlante narrativo a quadranti"
        />
        <QuickLink
          href="/strade"
          icon={<MapIcon className="h-4 w-4" aria-hidden />}
          title="Strade"
          desc="indice 5 sentieri Tier A"
        />
        <QuickLink
          href="/stato"
          icon={<Activity className="h-4 w-4" aria-hidden />}
          title="Stato F.2"
          desc="board canonizzazione per gruppo"
        />
      </section>

      <section aria-label="Workbench canonizzazione" className="space-y-3">
        <header className="flex items-end justify-between border-b border-rule-soft pb-2">
          <h2 className="font-serif text-2xl font-semibold text-ink">
            Lavorazione catalogo
          </h2>
          <Link
            href="/stato"
            className="inline-flex items-center gap-1 font-mono text-xs uppercase tracking-wider text-ink-faint hover:text-accent"
          >
            Board completa
            <ArrowRight className="h-3 w-3" aria-hidden />
          </Link>
        </header>
        <div className="grid gap-3 md:grid-cols-2">
          {perFamiglia.map((r) => {
            const pct = r.totale
              ? Math.round((r.canonico / r.totale) * 100)
              : 0;
            return (
              <div
                key={r.fam}
                className="rounded-md border border-rule-soft bg-paper-soft p-4"
              >
                <div className="mb-2 flex items-center justify-between gap-2">
                  <span className="font-serif text-lg font-medium capitalize text-ink">
                    {r.fam}
                  </span>
                  <span className="font-mono text-xs text-ink-faint">
                    {r.canonico}/{r.totale} canoniche
                  </span>
                </div>
                <div className="h-1.5 overflow-hidden rounded bg-rule-soft">
                  <div
                    className="h-full bg-accent transition-all"
                    style={{ width: `${pct}%` }}
                    aria-hidden
                  />
                </div>
                <dl className="mt-3 grid grid-cols-3 gap-2 font-mono text-[11px] text-ink-faint">
                  <Stat label="con prompt" value={r.conPrompt} max={r.totale} />
                  <Stat label="con img" value={r.conImmagini} max={r.totale} />
                  <Stat
                    label="provvisorie"
                    value={r.provvisorio}
                    max={r.totale}
                  />
                </dl>
              </div>
            );
          })}
        </div>
      </section>

      {conImmagini.length > 0 && (
        <section aria-label="Entità con immagini" className="space-y-3">
          <header className="flex items-end justify-between border-b border-rule-soft pb-2">
            <h2 className="font-serif text-2xl font-semibold text-ink">
              Con immagini canoniche
            </h2>
            <span className="font-mono text-xs text-ink-faint">
              top {conImmagini.length}
            </span>
          </header>
          <ul className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-8">
            {conImmagini.map((e) => {
              const first = e.images?.[0];
              return (
                <li key={e.id}>
                  <Link
                    href={`/catalogo/${e.id}`}
                    className="block space-y-1.5 rounded-md border border-rule-soft p-2 transition-colors hover:border-accent/40"
                  >
                    {first && (
                      <div className="relative aspect-square w-full overflow-hidden rounded bg-rule-soft/30">
                        <Image
                          src={imageUrl(first.path)}
                          alt={e.name}
                          fill
                          sizes="(max-width: 640px) 50vw, (max-width: 1024px) 25vw, 12vw"
                          className="object-cover"
                          unoptimized
                        />
                      </div>
                    )}
                    <p className="truncate text-xs font-medium text-ink">
                      {e.name}
                    </p>
                    <p className="font-mono text-[10px] text-ink-faint">
                      {e.n_images} img · {e.status}
                    </p>
                  </Link>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      <footer className="border-t border-rule-soft pt-6 font-mono text-[11px] text-ink-faint">
        <span className="inline-flex items-center gap-1.5">
          <Search className="h-3 w-3" aria-hidden />
          Premi ⌘K (Ctrl+K) ovunque per cercare tra entità, storie e sezioni.
        </span>
      </footer>
    </main>
  );
}

function QuickLink({
  href,
  icon,
  title,
  desc,
}: {
  href: string;
  icon: React.ReactNode;
  title: string;
  desc: string;
}) {
  return (
    <Link
      href={href}
      className="group flex items-start gap-3 rounded-md border border-rule-soft bg-paper p-4 transition-colors hover:border-accent/40 hover:bg-paper-soft"
    >
      <span className="mt-0.5 rounded bg-rule-soft/50 p-2 text-ink-soft group-hover:text-accent">
        {icon}
      </span>
      <span className="flex-1">
        <span className="block font-serif text-lg font-medium text-ink">
          {title}
        </span>
        <span className="block text-xs text-ink-soft">{desc}</span>
      </span>
      <ArrowRight
        className="h-4 w-4 shrink-0 text-ink-faint transition-transform group-hover:translate-x-0.5 group-hover:text-accent"
        aria-hidden
      />
    </Link>
  );
}

function Stat({
  label,
  value,
  max,
}: {
  label: string;
  value: number;
  max: number;
}) {
  return (
    <div>
      <dt>{label}</dt>
      <dd className="text-ink-soft">
        {value}/{max}
      </dd>
    </div>
  );
}
