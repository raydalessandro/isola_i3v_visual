# PROJECT_STATE.md — Snapshot operativo

> **Questo file è uno snapshot, non un diario.** Contiene: stato corrente + ultima sessione.
> Quando inizia una nuova sessione significativa, la sessione qui sotto scivola in
> `docs/fasi/SESSIONI_ARCHIVIO.md` in testa e questo file si riscrive.
> Storia completa: `docs/fasi/` · Regole e routing: `CLAUDE.md` · Canone macchina: `saga_config.yaml`.

**Aggiornato al: 2026-08-13 (scenografia s11 — YAML operativo e derivati)**

## Stato corrente

- **Grafo:** schema 1.4, graph 1.2.0, 12/12 storie, 120 hook; `make audit` attivo e verde. Il grafo non è stato modificato in questa sessione.
- **Canone macchina:** `saga_config.yaml` resta la single source of truth per id, marker e lessico.
- **Prosa:** 12/12 storie definitive. Il wiring di `@subhook` nella prosa è completo per il Volume 1; s07–s12 conservano al momento i soli marker `@hook` e richiederanno integrazione mirata prima del montaggio immagine-per-pagina.
- **s11 — La Festa del Raccolto:** aggiunto `_annotations/s11.yaml` con **21 subhook** ordinati su 21 pagine libro (`s11_h01a` → `s11_h10b`), ognuno con `pov`, `text_split_marker`, `image_status: TBD` e nota scenografica. I derivati `catalogo_web/data/storie.json` e `web/public/data/storie-dashboard.json` sono stati rigenerati dal parser di progetto e incorporano 21 subhook s11.
- **Decisioni necessarie prima delle immagini s11:** verificare/integrare reference e prompt canonici per la Piazza in Festa del Raccolto, il collettivo del Mercato (Vecchie), i coni dipinti, i frutti oltre mare di Bartolo e l'interno della casa dei fratelli. Sono registrati come `canon_additions_todo` nello YAML, senza promozioni canoniche autonome.
- **Standard scene v1.1:** prompt derivati dal template blindato; STILE → POV → SCALA GU → CAST → LUOGO → MOOD → DIVIETI; reference personaggi e luoghi obbligatorie; JPEG sRGB verticale 2:3, almeno 1824×2736 px, 300 DPI; quiet zone alta 25–30%; no text/lettering.
- **Scene HD Vol 2 (s04–s06):** 58 scene in `_scene/sNN/_hd/`; le immagini rimangono sotto lo standard v1.1 e richiedono revisione finale. Il compositore ora monta anche scene HD-only.
- **Cancello tecnico consegne:** `scripts/audit/audit_delivery.py` e relativo workflow CI verificano consegne immagini verso `main`; non sostituiscono la review canonica/visiva di Ray.
- **Catalogo v2 (`web/`):** Next.js 15 su Vercel; il TODO del deploy richiede ancora diagnosi separata.

## Ultima sessione

## Sessione 2026-08-13 — Scenografia s11: annotazione operativa e preflight (scenografo)

È stata avviata la preparazione professionale delle immagini di **s11 — La Festa del Raccolto** a partire da `CLAUDE.md`, `README.md`, skill `scenografo`, template prompt, stylesheet e prosa definitiva. La fonte narrativa non è stata modificata e il grafo è rimasto intatto.

- Creata la branch `claude/scenografia-s11-yaml`.
- Creato `pipeline_narrativa/storie_finali/_annotations/s11.yaml`: 10 hook canonici articolati in **21 subhook**, con pagine 1–21 continue, POV tecnici in inglese, note di scena, continuità luce/alba-mezzogiorno-pomeriggio-crepuscolo e `image_status: TBD`.
- Rigenerati da fonte `catalogo_web/data/storie.json` e `web/public/data/storie-dashboard.json`; il generatore legge e propaga tutti i 21 ID di subhook s11.
- Inseriti `canon_additions_todo` ad alta/media priorità per reference mancanti o non ancora formalizzate: variante Piazza in Festa, Vecchie del Mercato, coni dipinti, frutti oltre mare e interno casa fratelli.
- Verifiche eseguite: `git diff --check`, `make audit` (PASS 5/5) e `make check` (179 test passati, 6 deselected; audit PASS 5/5). I warning audit esistenti sul grafo sono invariati e informativi.
- Prima della generazione delle immagini è necessario il controllo di Ray sulle cinque decisioni di canone/reference annotate. Dopo il via libera: inserire i marker `@subhook` nella prosa s11, verificare le reference del cast e dei luoghi per ciascun batch, quindi comporre i prompt dal `PROMPT_TEMPLATE.md` e generare le scene in una sessione fresca dedicata a s11.
