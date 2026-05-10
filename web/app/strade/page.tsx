import type { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, Map as MapIcon } from "lucide-react";

import { getEntitiesData } from "@/lib/data";
import { renderInlineHtml } from "@/lib/markdown";

export const metadata: Metadata = {
  title: "Indice strade — L'Isola dei Tre Venti",
  description:
    "Tutte le strade secondarie dell'Isola: vicoli, sentieri, viottoli — per quartiere.",
};

/**
 * Trasforma i link markdown alle schede strada in link interni `/catalogo/<id>`.
 * Pattern sorgente:
 *   `[`visual/luoghi/<...>/<id>/scheda.md`](./luoghi/<...>/<id>/scheda.md)`
 * Sostituiamo solo l'URL (mantenendo il label code-style del catalogo).
 */
function rewriteSchedaLinks(md: string): string {
  return md.replace(
    /\(\.\/luoghi\/[^()\s]*?\/([^/()\s]+)\/scheda\.md\)/g,
    (_match, id) => `(/catalogo/${id})`,
  );
}

export default async function StradeIndexPage() {
  const data = await getEntitiesData();
  const md = data.aux.strade_index_md ?? "";

  if (!md.trim()) {
    return (
      <main className="mx-auto max-w-4xl px-6 py-10 space-y-6">
        <h1 className="font-serif text-3xl font-semibold text-ink">
          Indice strade
        </h1>
        <p className="font-serif italic text-ink-soft">
          Indice non disponibile (campo <code>aux.strade_index_md</code> vuoto).
        </p>
      </main>
    );
  }

  const html = renderInlineHtml(rewriteSchedaLinks(md));

  return (
    <main className="mx-auto max-w-5xl px-6 py-10 space-y-8">
      <header className="space-y-3 border-b border-rule-soft pb-6">
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-wider text-ink-faint hover:text-accent"
        >
          <ArrowLeft className="h-3 w-3" aria-hidden />
          Home cruscotto
        </Link>
        <div className="flex items-center gap-2 text-accent">
          <MapIcon className="h-5 w-5" aria-hidden />
          <span className="font-mono text-xs uppercase tracking-wider">
            Indice strade
          </span>
        </div>
        <h1 className="font-serif text-4xl font-semibold tracking-tight text-ink">
          Strade secondarie dell&apos;Isola
        </h1>
        <p className="font-serif text-lg italic text-ink-soft max-w-2xl">
          Vicoli, sentieri e viottoli per quartiere — derivati dal grafo +
          cartografia. I link aprono la scheda corrispondente nel catalogo.
        </p>
      </header>
      <div
        className="prose-saga"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </main>
  );
}
