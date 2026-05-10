import Link from "next/link";
import { ArrowRight, BookOpen, Compass, ImageIcon, Map as MapIcon } from "lucide-react";
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
const APP_VERSION = "0.4.0";

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
              <Link href="/catalogo" className="inline-flex items-center gap-2">
                Apri catalogo
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Link>
            </Button>
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-accent-warm">
              <BookOpen className="h-5 w-5" aria-hidden />
              <span className="font-mono text-xs uppercase tracking-wider">
                Storie
              </span>
            </div>
            <CardTitle>Storie del libro</CardTitle>
            <CardDescription>
              Le 12 storie illustrate — prosa definitiva + immagini-scena per
              pagina libro fisica.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-ink-soft">
            <p>
              Indice 12 storie raggruppate per ciclo (A/B/C/D), con dettaglio
              pagina-per-pagina e link alle tappe narrative.
            </p>
          </CardContent>
          <CardFooter>
            <Button asChild variant="default">
              <Link href="/storie" className="inline-flex items-center gap-2">
                Apri storie
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Link>
            </Button>
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-accent">
              <MapIcon className="h-5 w-5" aria-hidden />
              <span className="font-mono text-xs uppercase tracking-wider">
                Strade &amp; mappa
              </span>
            </div>
            <CardTitle>Indice &amp; mappa isola</CardTitle>
            <CardDescription>
              Le strade secondarie per quartiere, e la mappa illustrata
              navigabile.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-ink-soft space-y-2">
            <p>
              L&apos;indice strade dà accesso a vicoli, sentieri, viottoli con
              link alle schede catalogo.
            </p>
          </CardContent>
          <CardFooter className="flex flex-wrap gap-2">
            <Button asChild variant="default">
              <Link href="/strade" className="inline-flex items-center gap-2">
                Indice strade
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Link>
            </Button>
            <Button asChild variant="ghost">
              <Link href="/mappa" className="inline-flex items-center gap-2">
                <Compass className="h-4 w-4" aria-hidden />
                Mappa isola
              </Link>
            </Button>
          </CardFooter>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2 text-accent-warm">
              <Compass className="h-5 w-5" aria-hidden />
              <span className="font-mono text-xs uppercase tracking-wider">
                Orchestra
              </span>
            </div>
            <CardTitle>Atlante saga</CardTitle>
            <CardDescription>
              Vista narrativa cross-storia: 12 storie sull&apos;asse temporale,
              archi dei semi, presenze personaggi e luoghi.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-ink-soft">
            <p>
              Atlante a tre tracce con archi seed (planted → bloomed),
              side-panel per il dettaglio di ogni nodo, deep linking via hash.
            </p>
          </CardContent>
          <CardFooter>
            <Button asChild variant="default">
              <Link href="/orchestra" className="inline-flex items-center gap-2">
                Apri atlante
                <ArrowRight className="h-4 w-4" aria-hidden />
              </Link>
            </Button>
          </CardFooter>
        </Card>
      </section>

      <footer className="border-t border-rule-soft pt-6 font-mono text-xs text-ink-faint">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span>v{APP_VERSION} · build {BUILD_DATE}</span>
          <span>Step 4.1/N — atlante saga</span>
        </div>
      </footer>
    </main>
  );
}
