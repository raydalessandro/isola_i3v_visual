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

- **Step 1 / N — skeleton (questo)**: app Next inizializzata, home placeholder, design tokens, shadcn (Button + Card), font setup. Build/lint puliti.
- **Step 2**: porta del catalogo immagini dentro l'app Next (route `/catalogo`).
- **Step 3**: route `/orchestra` (atlante saga).
- **Step 4**: orchestratrice LLM (chat con accesso al canone).
- **Step finale — cutover**: il dominio principale punta all'app Next; il catalogo statico viene archiviato.

## Vincolo

L'app Next **legge** dati dal resto del repo (`pipeline_narrativa/`, `visual/`) ma non deve **scriverci**: la pipeline narrativa resta governata da Ray + skill esistenti.

## Aggiungere componenti shadcn

```bash
npx shadcn@latest add <component>
```
