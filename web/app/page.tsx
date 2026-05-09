import Link from "next/link";
import { ArrowUpRight, Compass, ImageIcon } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const BUILD_DATE = "2026-05-09";
const APP_VERSION = "0.1.0";

export default function HomePage() {
  return (
    <div className="space-y-12">
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
              Il catalogo statico esistente resta servito su Vercel finché la
              migrazione non avrà completato il cutover. Per ora il link rimanda
              al deploy attuale.
            </p>
          </CardContent>
          <CardFooter>
            <Button asChild variant="outline">
              <a
                href="/catalogo_web/"
                className="inline-flex items-center gap-2"
              >
                Apri catalogo
                <ArrowUpRight className="h-4 w-4" aria-hidden />
              </a>
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
          <span>Step 1/N — skeleton</span>
        </div>
      </footer>
    </div>
  );
}
