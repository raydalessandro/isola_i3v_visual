import Link from "next/link";
import { ArrowRight, Compass, ImageIcon } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const BUILD_DATE = "2026-05-10";
const APP_VERSION = "0.2.0";

export default function HomePage() {
  return (
    <main className="max-w-6xl mx-auto px-6 py-10 space-y-12">
      <header className="space-y-3 border-b border-rule-soft pb-8">
        <h1 className="font-serif font-semibold text-5xl tracking-tight text-ink">
          L&apos;Isola dei Tre Venti
        </h1>
        <p className="font-serif italic text-xl text-ink-soft">
          Cruscotto editoriale — migrazione in corso
        </p>
      </header>

      <section className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-accent-warm">
              <ImageIcon className="h-5 w-5" aria-hidden />
              <span className="font-mono text-xs uppercase tracking-wider">
                Catalogo
              </span>
            </div>
            <CardTitle>Catalogo immagini</CardTitle>
            <CardDescription>
              Versione statica vivente — schede personaggi, oggetti, luoghi,
              venti.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-ink-soft">
            <p>
              Catalogo entità nativo Next.js: tree gerarchico, gallerie con
              lightbox, body editoriale collassabile, prompt grok per
              personaggi e oggetti.
            </p>
          </CardContent>
          <CardFooter>
            <Button asChild variant="default">
              <Link
                href="/catalogo"
                className="inline-flex items-center gap-2"
              >
                Apri catalogo
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Link>
            </Button>
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-accent">
              <Compass className="h-5 w-5" aria-hidden />
              <span className="font-mono text-xs uppercase tracking-wider">
                Orchestra
              </span>
            </div>
            <CardTitle>Atlante saga</CardTitle>
            <CardDescription>
              Vista narrativa cross-storia: archi, cornici del mondo, sentieri,
              quote tracker.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-ink-soft">
            <p className="font-mono text-sm">Coming soon</p>
          </CardContent>
          <CardFooter>
            <Button disabled variant="ghost">
              In arrivo
            </Button>
          </CardFooter>
        </Card>
      </section>

      <footer className="border-t border-rule-soft pt-6 font-mono text-xs text-ink-faint">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span>
            v{APP_VERSION} · build {BUILD_DATE}
          </span>
          <span>Step 2/N — catalogo entità</span>
        </div>
      </footer>
    </main>
  );
}
