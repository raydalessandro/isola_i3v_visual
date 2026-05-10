# web/ — Cruscotto editoriale L'Isola dei Tre Venti

App **Next.js 15** (App Router) + **TypeScript strict** + **Tailwind CSS 3.4** + **shadcn/ui** (style "new-york") + **Lucide Icons**. Questa cartella è la **nuova interfaccia** del progetto, in costruzione progressiva.

---

## Cos'è

- Stack: Next.js 15, React 19, Tailwind 3.4, shadcn/ui, lucide-react
- Font via `next/font/google`: **Fraunces** (serif) e **JetBrains Mono** (mono). Nessun `<link>` Google diretto.
- Design tokens saga (`paper`, `ink`, `accent`, `accent-warm`, ...) definiti come CSS variables in `app/globals.css` e mappati in `tailwind.config.ts`.
- Path alias `@/*`.

## Avvio in dev

```bash
cd web
npm install
npm run dev
```

Apre `http://localhost:3000`. La home è `app/page.tsx`.

## Build

```bash
npm run build
npm start
```

## Lint

```bash
npm run lint
```

## Deploy su Vercel

1. Crea un **nuovo progetto** Vercel (separato dal deploy attuale del catalogo statico).
2. **Root Directory**: `web/`
3. Framework preset: auto-detect (Next.js).
4. Niente env vars per ora.
5. Deploy.

> Il `vercel.json` nella root del repo continua a servire la pagina statica `catalogo_web/` sul deploy esistente. Resta intoccato fino al cutover finale.

## Stato della migrazione

- **Step 1 / N — skeleton**: app Next inizializzata, home placeholder, design tokens, shadcn (Button + Card), font setup. Build/lint puliti.
- **Step 2 / N — catalogo entità (questo)**: route `/catalogo` + `/catalogo/[id]`, sidebar/drawer con tree gerarchico, stats + featured grid + search, gallery con lightbox keyboard/touch, body markdown a sezioni collassabili, prompt grok in `<details>`. SSG: 116 schede pre-renderizzate.
- **Step 3**: route `/orchestra` (atlante saga); strade & storie del libro nella sidebar (placeholders attivi).
- **Step 4**: orchestratrice LLM (chat con accesso al canone).
- **Step finale — cutover**: il dominio principale punta all'app Next; il catalogo statico viene archiviato.

## Dati & immagini

I dati del catalogo arrivano da `catalogo_web/data/entities.json` (1.4 MB). Lo script `scripts/copy-data.mjs` (eseguito automaticamente come `prebuild`/`predev`) li copia in `public/data/entities.json`. La cartella `public/data/` è gitignored.

Le **immagini** del catalogo NON sono copiate dentro `web/public/`. Vengono servite dal deploy statico esistente (default `https://catalogoisola.vercel.app`). Per cambiarlo, definisci la env var:

```bash
NEXT_PUBLIC_IMAGE_BASE=https://nuovo-host.example.com
```

Il default è hardcoded come fallback in `lib/image-url.ts` e in `next.config.mjs` (`images.remotePatterns`). Quando faremo il cutover, basta aggiornare quella env var (più, eventualmente, aggiungere il nuovo host ai `remotePatterns`).

L'optimization service di `next/image` non è abilitato per le immagini del catalogo (`unoptimized` nelle gallery): le servono già grandi/JPG dal CDN sorgente, non c'è guadagno a ri-trascinarle attraverso il proxy ottimizzatore.

## Vincolo

L'app Next **legge** dati dal resto del repo (`pipeline_narrativa/`, `visual/`, `catalogo_web/data/`) ma non deve **scriverci**: la pipeline narrativa resta governata da Ray + skill esistenti.

## Aggiungere componenti shadcn

```bash
npx shadcn@latest add <component>
```

> **Nota**: il registry remoto `ui.shadcn.com/r/styles/new-york/...` può richiedere autenticazione in alcuni ambienti (errore 401). In quel caso copia il sorgente del componente a mano da `https://ui.shadcn.com/docs/components/<name>` mantenendo i path alias `@/lib/utils`. I componenti `Sheet`, `Dialog`, `Input`, `Badge`, `Separator`, `Collapsible` in `components/ui/` sono stati introdotti in Step 2 in questo modo.
