import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, Compass } from "lucide-react";

import { MappaIsola } from "@/components/mappa/mappa-isola";

export const metadata: Metadata = {
  title: "Mappa isola — L'Isola dei Tre Venti",
  description:
    "Mappa illustrata navigabile dell'Isola dei Tre Venti — click su un edificio per aprire la scheda.",
};

export default function MappaPage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-10 space-y-6">
      <header className="space-y-3 border-b border-rule-soft pb-6">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-wider text-ink-faint hover:text-accent"
        >
          <ArrowLeft className="h-3 w-3" aria-hidden />
          Home cruscotto
        </Link>
        <div className="flex items-center gap-2 text-accent">
          <Compass className="h-5 w-5" aria-hidden />
          <span className="font-mono text-xs uppercase tracking-wider">
            Mappa isola
          </span>
        </div>
        <h1 className="font-serif text-4xl font-semibold tracking-tight text-ink">
          L&apos;Isola dei Tre Venti
        </h1>
        <p className="font-serif text-lg italic text-ink-soft max-w-2xl">
          Mappa illustrata sopra l&apos;acquerello base. Edifici 3D dove
          disponibili, slot tratteggiati altrove (asset 3D in arrivo).
        </p>
      </header>

      <MappaIsola />

      <div className="border-t border-rule-soft pt-4 font-mono text-[11px] text-ink-faint">
        <p>
          Viewer cartografia tecnica (Leaflet, GeoJSON):{" "}
          <a
            href="https://catalogoisola.vercel.app/cartografia/geo/viewer/index.html"
            target="_blank"
            rel="noopener noreferrer"
            className="text-accent underline underline-offset-2 hover:text-accent/80"
          >
            apri in nuova scheda
          </a>
        </p>
      </div>
    </main>
  );
}
