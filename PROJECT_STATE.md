# PROJECT_STATE — Snapshot operativo

> **Questo file è uno snapshot, non un diario.** Contiene: stato corrente + ultima sessione.
> Quando inizi una nuova sessione significativa, la sessione qui sotto scivola in
> `docs/fasi/SESSIONI_ARCHIVIO.md` (in testa) e questo file si riscrive.
> Storia completa: `docs/fasi/` · Regole e routing: `CLAUDE.md` · Canone macchina: `saga_config.yaml`.

**Aggiornato al: 2026-06-22 (merge skill scenografo v1.2 + subhook pov Vol 2)**

## Stato corrente

- **Grafo:** schema 1.4, graph 1.2.0, 12/12 storie, 120 hook, `known_issues.yaml` pulito a HEAD. Audit 1–5 attivi in CI (`make audit`), incluso `audit_5_timeline` (semi+callback).
- **Canone macchina:** `saga_config.yaml` su main (config_version 1) + loader `scripts/saga_canon.py` — single source of truth per id, marker, lessico.
- **Brief:** 12/12 generati (zero-token, `make briefs`), con §2-bis STATO DEL MONDO (proiezione world-state).
- **Prosa:** 12/12 storie finali con apparato `@hook`/`@subhook` (Vol 1 completo s01–s03). **Subhook Vol 2 (s04–s06)** con campo `pov` per ogni subhook (punto di vista del lettore, blocco prompt obbligatorio §2-ter).
- **Scenografo v1.2 (2026-06-22, PR #48):** §0 contesto di sessione/cache, ordine blocchi prompt STILE → POV → SCALA GU → CAST → LUOGO → MOOD → DIVIETI, POV obbligatorio (§2-ter), blocco DIVIETI fisso, `prompt_approvati.md` come memoria viva. Template blindato in `PROMPT_TEMPLATE.md` (radice repo, v1.0).
- **Visual / fase F.2:** in corso — 101 immagini catalogate, 15 entità canoniche complete (al 2026-06-10). 116 schede esistenti.
- **Catalogo v2 (`web/`):** Next.js 15 su Vercel. ⚠️ TODO aperto: debug deploy fermo alle 16:23 UTC del 2026-06-10 (le PR successive non sono visibili sul sito).
- **Standard scene v1.1 (2026-06-12, PR #22):** minimo HD **1824×2736 px** (300 DPI reali sul fit di `build_volume.py`), metadato DPI 300, coerenza reference a 360°, quiet zone alta ~25-30% per il testo di pagina, NO-TEXT rinforzato nel NEGATIVE. Fonti vive: stylesheet + skill scenografo/illustratore. Le scene s01 (1664×2496) restano valide come v1.
- **Roadmap immediata:** cutover catalogo statico → **riordino brieffer blocchi A/B cache** (debito tecnico: `docs/TODO_BRIEFFER_CACHE_AB.md`, da chiudere prima del template) → estrazione starter kit v2 → seeding saga "Rocco e Idvara".
- **Debito derivati (2026-06-14):** `make sync` su main rigenera 12 writing_briefs (§2-bis + immagini canoniche) + entities/dashboard — derivato stale non sincronizzato, indipendente dal montaggio volume. Da chiudere in sessione manutentore dedicata: `docs/TODO_DERIVATI_STALE_MAIN.md`. **Parzialmente recuperato (2026-06-22, PR #49):** `storie.json` + `storie-dashboard.json` rigenerati e allineati; restano writing_briefs + entities.

## Ultima sessione

## Sessione 2026-06-22 — Integrazione subhook pov Vol 2 + scenografo v1.2 (manutentore)

Due pacchetti preparati da Ray (zip), integrati come una branch per zip, verificati e mergiati su main nell'ordine richiesto (skill prima, contenuto poi). Le due modifiche sono collegate: il campo `pov` nelle annotations alimenta il blocco POV obbligatorio del prompt scena.

### A. PR #48 — skill scenografo v1.2 + PROMPT_TEMPLATE.md

- `skills/scenografo/SKILL.md` v1.1 → **v1.2**: §0 contesto di sessione/cache (invariante vs variante), riordino blocchi del prompt (STILE → POV → SCALA GU → CAST → LUOGO → MOOD → DIVIETI), POV e SCALA GU estratti come blocchi propri, **POV obbligatorio** (§2-ter), blocco DIVIETI fisso, §8 `prompt_approvati.md` (memoria viva, si popola progressivamente).
- `PROMPT_TEMPLATE.md` nuovo in **root** (v1.0): template blindato coi blocchi fissi già compilati, caselle `{{...}}` dalle fonti. Collocazione root confermata dalla skill ("radice repo").
- Verifica: `make routing` → tabella già allineata (11 skill, scope/trigger scenografo invariati).

### B. PR #49 — subhook Vol 2 campo pov (s04–s06) + derivati

- `_annotations/s04,s05,s06.yaml`: aggiunto campo `pov` (frase tecnica EN, punto di vista del lettore) a ogni subhook + riga di legenda. **Puramente additivo**, nessuna nota esistente toccata.
- `catalogo_web/data/storie.json` + `web/public/data/storie-dashboard.json`: **rigenerati** con `scripts/build_storie_data.py` (non copiati dallo zip), byte-identici alla build di Ray → idempotenza confermata.
- Verifica: `make audit` → PASS 5/5 (4 warning preesistenti sul grafo, non toccato).

### C. Incoerenze valutate (entrambe spiegate, nessuna reale)

1. `catalogo_web/` è "non toccare" ma lo zip lo modifica → non è una mano umana: `build_storie_data.py` scrive quel file come **mirror derivato**. Legittimo.
2. I due `.json` cambiano ma lo script non legge `pov` → il loro delta è solo il recupero del **debito derivati stale main** (non l'effetto del pov). Confermato: rigenerazione da fonte = quei byte.

### D. Note

- I due `.json` rigenerati chiudono **parzialmente** il debito derivati stale (restano writing_briefs + entities).
- Lo zip della skill era nominato "v12" ma l'header corretto è **v1.2**: lasciato v1.2.
- `make check` non eseguibile in ambiente remoto (`pytest` non installato): girerà in CI sul push. Audit (python puro) verde.

### E. Prossimo passo Ray

1. Cancellare da UI GitHub i branch mergiati `claude/scenografo-v12` e `claude/subhook-vol2-pov` (o farlo cancellare).
2. Debito derivati residuo: chiudere writing_briefs + entities in sessione manutentore dedicata (`docs/TODO_DERIVATI_STALE_MAIN.md`).
3. TODO Vercel ancora aperto (deploy fermo).

---



