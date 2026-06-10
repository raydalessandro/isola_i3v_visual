# SPEC — Catalogo v2 (branch `claude/catalogo-v2`)

**Data:** 2026-06-10 · **Autore spec:** Claude (chat) su richiesta Ray · **Esecutore previsto:** Claude Code
**Repo:** `isola_i3v_visual` · **Prerequisito:** branch blindatura mergiata (audit + CI attivi)

---

## BRIEF — perché

Il catalogo deve diventare uno **strumento di lavoro**, non una vetrina. Due modi d'uso che guidano tutto:

1. **Fase seme (live).** Mentre Ray sviluppa il seme in chat e il grafo/le schede crescono, il catalogo deve riflettere lo stato della repo con latenza minima: vedere la storia che prende forma (entità, timeline, prime immagini) per guidare meglio la generazione.
2. **Consultazione operativa.** Chi genera le immagini deve trovare un'entità in secondi, **copiare il prompt esatto di una singola vista con un click**, scaricare le immagini canoniche, e condividere link profondi a entità/sezione. Oggi preferisce navigare i file su GitHub: il catalogo perde contro le tab del browser — questo è il bug da risolvere.

## DIAGNOSI — stato attuale (verificato sul codice)

Nella repo convivono **due** cataloghi:

| | `catalogo_web/` (statico) | `web/` (Next.js 15, v0.4.0) |
|---|---|---|
| Stack | 1131 righe vanilla JS + 1895 CSS monolitico | App Router, TS strict, shadcn/ui, 40 componenti |
| Sezioni collassabili | ✗ (scroll infinito) | ✅ già fatto (`entity-body.tsx`, default chiuse, expand/collapse all) |
| Copy prompt | ✗ | ✗ (`prompt-grok-block.tsx` rende HTML, nessuna copia) |
| Download immagini | ✗ | ✗ (gallery+lightbox senza download) |
| Deep link a sezione | ✗ | ✗ (sezioni senza hash routing) |
| Ricerca | filtro base | solo nome/id nella sidebar |
| Storie/pagine libro | ✗ | ✅ (`/storie/[sid]/pagine`, dashboard lavoro) |
| Home operativa | ✗ | parziale (card editoriali, niente stato/quick links) |
| Live su modifica repo | ✗ (rebuild CI) | ✗ (copy-data solo a predev) |

**Decisione architetturale (D1): Catalogo v2 = `web/` (Next.js).** Lo statico è congelato come legacy fino al cutover: nessun nuovo sviluppo lì, resta pubblicato finché v2 non lo sostituisce. Metà dei problemi lamentati sono *già risolti* nella app Next — il lavoro vero sono i 7 item sotto, non una riscrittura.

**Decisione (D2): `entities.json` resta il contratto dati.** Generato da `scripts/build_catalogo_web.py` (atomico, auditato, riusato dallo starter kit). La v2 non introduce un secondo formato; estensioni solo additive.

**Decisione (D3): niente backend.** Tutto SSG/static + un solo route handler per il proxy immagini (vedi WI-3). Compatibile Vercel free tier e con l'estrazione nel template.

---

## L0 — Work items

### WI-1 · Prompt copiabili a granularità di vista ⭐ (il killer feature)

`prompt_grok_md` contiene N blocchi prompt, uno per immagine canonica, in due dialetti:
- personaggi/oggetti: header `## IMMAGINE N — <titolo>` → primo fenced block ``` = prompt completo della vista; in coda blocchi globali (`## Negative prompt globale`, `## Negative prompt specifici <id>`)
- luoghi: header `## 🎨 Veduta N — <titolo>` → idem (+ `**Filename atteso:** …` nel preambolo della vista)

**Implementare:**
1. `lib/prompt-grok.ts` — parser puro: `parsePromptGrok(md) → { views: [{ title, filenameAtteso?, prompt, checklist? }], globals: [{ title, text }] }`. Regola: una "vista" = sezione H2 il cui titolo matcha `/^(🎨\s*)?(IMMAGINE|Veduta)\s+\d+/i`; il suo `prompt` = contenuto del **primo** fenced block della sezione; `filenameAtteso` = da `**Filename atteso:** \`...\`` se presente. Sezioni H2 con fenced block che non matchano il pattern vista → `globals`.
2. Refactor `prompt-grok-block.tsx`: per ogni vista una card collassabile con **CopyButton** (riusare `components/storie-dashboard/copy-button.tsx`, già pronto) che copia il prompt grezzo; pulsante "Copia con negative globale" che concatena prompt + globals; in testa "Copia tutto il file" (md grezzo).
3. **Unit test** del parser (`web/lib/__tests__` o vitest minimale) sui due dialetti reali: fixture estratte da `liu` (personaggio, 4 IMMAGINE) e `foresta_intrecciata` (luogo, Veduta + variazioni). Il parser è l'unico pezzo fragile: va blindato.

**Acceptance:** su `/catalogo/liu` la collaboratrice copia il prompt di IMMAGINE 2 in un click, con feedback visivo; il testo copiato è byte-identico al fenced block del file md.

### WI-2 · Download immagini

- `lightbox.tsx` + `entity-gallery.tsx`: pulsante download per immagine (filename canonico preservato) + "Scarica tutte" per entità (zip client-side via `jszip`, o sequenza di download se si vuole zero dipendenze — scegliere in branch, default: jszip).
- Vincolo tecnico: le immagini arrivano da `NEXT_PUBLIC_IMAGE_BASE` (origin diverso) → `download` attribute cross-origin **non funziona**. Soluzione in WI-3.

### WI-3 · Proxy immagini same-origin (sblocca WI-2 e prepara il cutover)

Route handler `app/api/img/[...path]/route.ts`:
- valida `path` contro prefisso `visual/` (no traversal, solo estensioni `IMG_EXTS`),
- fetcha da `IMAGE_BASE`, streamma con `Cache-Control: public, max-age=31536000, immutable` e, se `?download=1`, `Content-Disposition: attachment; filename="<basename>"`.
- `lib/image-url.ts`: il download usa sempre `/api/img/...?download=1`; la visualizzazione resta su IMAGE_BASE (next/image invariato).
**Acceptance:** download di `liu_canonica_v1_fronte.jpg` dal lightbox salva il file col nome canonico. Cutover futuro = cambiare una costante.

### WI-4 · Deep link e permalink

- `lib/markdown.ts`: id slug stabili per ogni sezione H2 (già esistono `MarkdownSection.id`? verificare; altrimenti slugificare il titolo, dedup con suffisso).
- `entity-body.tsx`: su mount, se `location.hash` matcha una sezione → aprirla e scrollarvi; icona "link" accanto a ogni titolo sezione che copia `/catalogo/<id>#<sezione>`. Stesso pattern per le viste prompt (`#prompt-immagine-2`).
- **Acceptance:** incollare `/catalogo/rovo#identita-visuale` in una chat apre la scheda con quella sezione espansa e a fuoco.

### WI-5 · Ricerca globale (cmd-K)

Command palette (shadcn `Dialog` + filtro, niente librerie search esterne): indicizza a build-time `{ id, label, categoria, titoli sezioni }` di tutte le entità + le 12 storie. Match su nome/id/sezione → naviga al deep link. Scope: **niente full-text del body in v2** (fuori scope, costo/beneficio sbagliato); i titoli di sezione coprono il caso "dove sta il cliché da evitare di X".
**Acceptance:** ⌘K → "salvia coer" → invio → `/catalogo/sentiero_orti_casa_salvia#coerenza-cross-scena`.

### WI-6 · Home operativa + /stato

- Home: sostituire le card editoriali con un **workbench**: contatori live da entities.json (`canonico` vs `provvisorio` per categoria — i dati ci sono già), ultime entità con immagini caricate, quick links (catalogo, storie, mappa, orchestra, stato), versione grafo (da un nuovo campo `meta` in entities.json: vedi WI-8).
- `/stato`: board F.2 — per gruppo (fratelli/primari/…/luoghi-per-quartiere): schede totali, con prompt, con immagini canoniche complete (4 per personaggi, 1-2 oggetti). Derivabile interamente da entities.json (presenza `prompt_grok_md`, conteggio `immagini`).
**Acceptance:** Ray apre la home e sa a colpo d'occhio quante schede mancano alla canonizzazione e dove.

### WI-7 · Modalità live per la fase seme

- Script `web/scripts/dev-watch.mjs`: watcher (fs.watch ricorsivo, debounce 500ms) su `../visual/**` e `../pipeline_narrativa/storie_finali/**` che rilancia `python3 ../scripts/build_catalogo_web.py` + `copy-data.mjs` + `build-storie.mjs`. Nuovo script npm `dev:live` = watcher + `next dev` in parallelo.
- Client: le pagine catalogo già rileggono al refresh; aggiungere solo un indicatore "dati aggiornati alle HH:MM" (da `meta.generated_at`).
**Acceptance:** Ray modifica una scheda in `visual/`, F5 sul browser entro ~2s vede il dato nuovo. (Hot-push automatico senza F5: fuori scope v2 — refresh manuale è sufficiente per il loop di lavoro descritto.)

### WI-8 · Estensioni additive a entities.json (unico touch su scripts/)

`build_catalogo_web.py`: aggiungere nodo root `meta: { generated_at, graph_version, schema_version, counts }` (letti dal grafo in sola lettura) — serve a WI-6/7. **Solo additivo**: lo statico legacy ignora i campi nuovi. Aggiornare il test smoke se esiste, rigenerare, commit separato.

---

## Vincoli e regole (non negoziabili)

- `pipeline_narrativa/` read-only; il catalogo **legge**, mai scrive.
- Nessuna nuova dipendenza pesante: ammessi `jszip` (WI-2) e basta. Niente librerie search, niente state manager.
- TS strict pulito, `npm run lint` verde, build SSG verde: sono il cancello della branch insieme a `make check`.
- Design tokens saga esistenti (`globals.css` / `tailwind.config.ts`): la v2 non re-inventa lo stile, lo completa.
- Ogni WI = commit dedicato COSA+PERCHÉ; WI-1 e WI-3 per primi (sbloccano il valore per la collaboratrice).
- Il parser WI-1 e il route handler WI-3 nascono **già pensati per lo starter kit**: zero riferimenti hardcoded a isola (id, palette, testi) — leggono tutto dai dati.

## Fuori scope v2 (esplicito)

Full-text search del body; editing schede da UI; auth; hot-reload push senza refresh; rifacimento `/mappa` e `/orchestra` (restano com'erano); migrazione dello statico (si spegne al cutover, non si migliora).

## Sequenza dopo il merge

1. Cutover: puntare il deploy "catalogo" alla app Next; archiviare `catalogo_web/{index.html,app.js,style.css}` (i `data/` restano: sono il contratto).
2. Estrazione **starter kit v2**: `web/` + `scripts/` + audit + CI col nuovo `saga_config.yaml` come unico punto di identità saga (nome, palette, categorie, enum) — è il passaggio "canone machine-readable" già concordato.
3. Da lì: repo Rocco e Idvara istanziata dal kit, fase seme con `dev:live` acceso.
