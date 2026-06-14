# PROJECT_STATE — Snapshot operativo

> **Questo file è uno snapshot, non un diario.** Contiene: stato corrente + ultima sessione.
> Quando inizi una nuova sessione significativa, la sessione qui sotto scivola in
> `docs/fasi/SESSIONI_ARCHIVIO.md` (in testa) e questo file si riscrive.
> Storia completa: `docs/fasi/` · Regole e routing: `CLAUDE.md` · Canone macchina: `saga_config.yaml`.

**Aggiornato al: 2026-06-12 (standard scene v1.1 + riordino router/skills)**

## Stato corrente

- **Grafo:** schema 1.4, graph 1.2.0, 12/12 storie, 120 hook, `known_issues.yaml` pulito a HEAD. Audit 1–5 attivi in CI (`make audit`), incluso `audit_5_timeline` (semi+callback).
- **Canone macchina:** `saga_config.yaml` su main (config_version 1) + loader `scripts/saga_canon.py` — single source of truth per id, marker, lessico.
- **Brief:** 12/12 generati (zero-token, `make briefs`), con §2-bis STATO DEL MONDO (proiezione world-state).
- **Prosa:** 12/12 storie finali con apparato `@hook`/`@subhook` (Vol 1 completo s01–s03).
- **Visual / fase F.2:** in corso — 101 immagini catalogate, 15 entità canoniche complete (al 2026-06-10). 116 schede esistenti.
- **Catalogo v2 (`web/`):** Next.js 15 su Vercel. ⚠️ TODO aperto: debug deploy fermo alle 16:23 UTC del 2026-06-10 (le PR successive non sono visibili sul sito).
- **Standard scene v1.1 (2026-06-12, PR #22):** minimo HD **1824×2736 px** (300 DPI reali sul fit di `build_volume.py`), metadato DPI 300, coerenza reference a 360°, quiet zone alta ~25-30% per il testo di pagina, NO-TEXT rinforzato nel NEGATIVE. Fonti vive: stylesheet + skill scenografo/illustratore. Le scene s01 (1664×2496) restano valide come v1.
- **Roadmap immediata:** cutover catalogo statico → **riordino brieffer blocchi A/B cache** (debito tecnico: `docs/TODO_BRIEFFER_CACHE_AB.md`, da chiudere prima del template) → estrazione starter kit v2 → seeding saga "Rocco e Idvara".
- **Debito derivati (2026-06-14):** `make sync` su main rigenera 12 writing_briefs (§2-bis + immagini canoniche) + entities/dashboard — derivato stale non sincronizzato, indipendente dal montaggio volume. Da chiudere in sessione manutentore dedicata: `docs/TODO_DERIVATI_STALE_MAIN.md`.

## Ultima sessione

## Sessione 2026-06-10 notte tarda — Canonizzazione + chiusura branch illustratore + fix sito

Sequenza di PR per chiudere il backlog illustratore + restituire al sito le funzionalità per Manus (illustratore AI).

### A. PR #13 — Canonizzazione 11 personaggi + 3 luoghi

- **Status canonico** per 11 schede personaggi (frontmatter `status: provvisorio` → `canonico`):
  - primari: fiamma, grunto, stria, memolo, bartolo
  - secondari: nodo, salvia, zolla
  - cuccioli: pun, bru, toba
  - Catalogo personaggi canonici: **4 → 15**
- **3 luoghi** promossi dalla branch `immagini-nuove`: `forno` (panoramica), `pascoli_alti` (era vuoto), `via_che_sale` (vista_alta).

### B. PR #14 — 4 luoghi ambigui + cronologia semi + fix copy hook

- **4 luoghi** restanti dalla branch `immagini-nuove` collocati con la mappa decisa da Ray:
  - `il_villaggio.jpg` + `il_mercato_del_mezzogiorno.jpeg` → `piazza_villaggio/` (`albero_centrale` + `mercato_mezzogiorno`)
  - `il_quartiere_di_terra.jpeg` → `orti_del_cerchio/` (orti concentrici — categoria contenitore mappata a sotto-luogo)
  - `il_quartiere_di_acqua.jpeg` → `spiaggia_conchiglie/` (spiaggia + casa)
- **Cronologia semi ricomparsa**: widget Server Component `<NarrativeChronologyBlock>` letto dal grafo. Mostra per ogni storia 🌱 piantati / 🌾 raccolti / 🌿 maturano / 🌸 sbocciati + 🔁 callback espliciti con summary. `scripts/build_storie_data.py` esteso con `load_graph_chronology()`.
- **Fix copy prompt hook narrativo**: `hook-item.tsx` riga 221 aveva `{!subhooksAnn.length && (...)}` — il pulsante "Copia prompt hook" era nascosto se la storia aveva subhook annotati. s01 (unica con subhook) non lo mostrava. Rimosso il guard.
- **Branch `immagini-nuove` completamente recuperata** (11 file totali — può essere cancellata da UI GitHub).

### C. PR #15 — Riordino layout hook per workflow Manus

Su segnalazione Ray ("sotto-hook e prompt copiabili devono essere la main visual"):

| Prima | Dopo |
|---|---|
| Luogo → Personaggi → Oggetti → Note → Subhook (prompt in `<details>` chiuso) → Prompt hook → Testo | 🎨 **Subhook + prompt VISIBILE + copy** (FULCRO) → 🎨 Prompt hook → 📍 Luogo (reference) → 👤 Personaggi (reference) → 📦 Oggetti (reference) → 📌 Note → Testo |

- Subhook card con bordo `accent/30` (in evidenza)
- Prompt scena visibile direttamente (non più `<details>` collassato)
- CopyButton già presente, ora più prominente per posizione

### D. TODO domani — Vercel non ribuilda

Stato verificato a sera:
- Codice in `origin/main`: nuovo layout ✓, cronologia semi ✓, luoghi ✓
- Codice in `origin/claude/cutover-deploy-preview`: idem (fast-forward a main) ✓
- **Vercel** sembra fermo al deploy delle 16:23 UTC (PR #11): nuove PR non visibili in produzione

Ray esamina domani. Possibili cause: branch deploy sbagliata, auto-deploy disabilitato, build silenzioso fallito, due project Vercel sovrapposti, route config in `vercel.json` che intercetta. Pushato anche un commit di trigger (`b3a6ef4`) su `main` con timestamp aggiornato (`generated_at: 2026-06-10T18:22:33`) per verificare visivamente se Vercel ribuilda.

### E. Stato repo verificato

```
catalogo            116 entità, 101 immagini (+4 luoghi rispetto a sera)
canonici            15 personaggi (era 4)
audit fast          3/3 PASS
pytest fast         78 PASS
pytest slow         6 PASS (build PDF Vol1 s01 reale)
mirror Vercel       entities + storie-dashboard + orchestra + search-index sincronizzati
```

### F. Branch illustratore obsolete (da cancellare da UI GitHub)

Tutte recuperate, niente da mergiare:
- `Modifiche-Hook-storia` (PR #4 + PR #11 hanno preso il contenuto)
- `Personaggi-modificati` (PR #4 + PR #12 hanno preso il contenuto)
- `immagini-nuove` (PR #14 ha preso gli ultimi 4 luoghi)
- `claude/show-uploaded-images-1rEQ1` (vuota)

### G. Prossimo passo Ray

1. Debug Vercel (capire perché non ribuilda)
2. Integrare 2 branch di miglioria qualità codice (preparate da Ray, ancora da pushare)

---



