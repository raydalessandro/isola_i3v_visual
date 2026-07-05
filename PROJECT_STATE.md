# PROJECT_STATE — Snapshot operativo

> **Questo file è uno snapshot, non un diario.** Contiene: stato corrente + ultima sessione.
> Quando inizi una nuova sessione significativa, la sessione qui sotto scivola in
> `docs/fasi/SESSIONI_ARCHIVIO.md` (in testa) e questo file si riscrive.
> Storia completa: `docs/fasi/` · Regole e routing: `CLAUDE.md` · Canone macchina: `saga_config.yaml`.

**Aggiornato al: 2026-07-05 (merge scene HD Vol 2 s04–s06 + fix montaggio HD-only)**

## Stato corrente

- **Grafo:** schema 1.4, graph 1.2.0, 12/12 storie, 120 hook, `known_issues.yaml` pulito a HEAD. Audit 1–5 attivi in CI (`make audit`), incluso `audit_5_timeline` (semi+callback).
- **Canone macchina:** `saga_config.yaml` su main (config_version 1) + loader `scripts/saga_canon.py` — single source of truth per id, marker, lessico.
- **Brief:** 12/12 generati (zero-token, `make briefs`), con §2-bis STATO DEL MONDO (proiezione world-state).
- **Prosa:** 12/12 storie finali con apparato `@hook`/`@subhook` (Vol 1 completo s01–s03). **Subhook Vol 2 (s04–s06)** con campo `pov` per ogni subhook (punto di vista del lettore, blocco prompt obbligatorio §2-ter).
- **Scene HD Vol 2 (2026-07-05, PR #51–53):** s04 (26 img), s05 (24), s06 (19) in `_scene/sNN/_hd/` (JPG q95). Le 58 scene dichiarate in prosa montano l'HD reale nel volume. ⚠️ Immagini a 1536×2304 (e alcune s05 inferiori), **sotto standard scene v1.1**: `build_volume` applica il banner "sotto spec" su ogni scena — accettato per questo giro, revisione immagini a fine ciclo. 11 subhook aggiunti alle annotations s04/s05 come placeholder ("da compilare"): registrati + immagine in `_hd/`, ma **non ancora in prosa** → fuori dal montaggio finché non ricevono marker `@subhook` + `page_book`.
- **Fix montaggio HD-only (2026-07-05, PR #54):** `build_volume.parse_story_md` ora sonda l'HD convenzionale `_scene/sNN/_hd/{id}_hd.jpg` quando `@image` è `TBD` e manca il proxy low-res. Sblocca il Vol 2+ (branch illustratore che consegnano solo `_hd/`); Vol 1 (path espliciti + low-res) invariato.
- **Scenografo v1.2 (2026-06-22, PR #48):** §0 contesto di sessione/cache, ordine blocchi prompt STILE → POV → SCALA GU → CAST → LUOGO → MOOD → DIVIETI, POV obbligatorio (§2-ter), blocco DIVIETI fisso, `prompt_approvati.md` come memoria viva. Template blindato in `PROMPT_TEMPLATE.md` (radice repo, v1.0).
- **Visual / fase F.2:** in corso — 101 immagini catalogate, 15 entità canoniche complete (al 2026-06-10). 116 schede esistenti.
- **Catalogo v2 (`web/`):** Next.js 15 su Vercel. ⚠️ TODO aperto: debug deploy fermo alle 16:23 UTC del 2026-06-10 (le PR successive non sono visibili sul sito).
- **Standard scene v1.1 (2026-06-12, PR #22):** minimo HD **1824×2736 px** (300 DPI reali sul fit di `build_volume.py`), metadato DPI 300, coerenza reference a 360°, quiet zone alta ~25-30% per il testo di pagina, NO-TEXT rinforzato nel NEGATIVE. Fonti vive: stylesheet + skill scenografo/illustratore. Le scene s01 (1664×2496) restano valide come v1.
- **Roadmap immediata:** cutover catalogo statico → **riordino brieffer blocchi A/B cache** (debito tecnico: `docs/TODO_BRIEFFER_CACHE_AB.md`, da chiudere prima del template) → estrazione starter kit v2 → seeding saga "Rocco e Idvara".
- **Debito derivati — CHIUSO (2026-07-05):** `make sync` post-merge Vol 2 ha rigenerato e allineato i 12 writing_briefs (§2-bis + immagini canoniche) + `entities.json` (mirror `catalogo_web/` e `web/public/`) + `dashboard.js`. Il derivato su main è ora sincronizzato con le fonti. `docs/TODO_DERIVATI_STALE_MAIN.md` può essere archiviato.

## Ultima sessione

## Sessione 2026-07-05 — Scene HD Vol 2 (s04–s06) + fix montaggio HD-only (manutentore)

Tre branch illustratore preparate da Ray (`claude/hd-storia-s04/05/06`) con le scene HD del Volume 2. Verifica tecnica → scoperta e fix di un bloccante del montaggio → build reale del Vol 2 → merge di tutto su main.

### A. Verifica delle 3 branch (tecnicamente sane)

- Immagini ↔ subhook 1:1 (s04 26/26, s05 24/24, s06 19/19), zero orfani, nessun PNG/`_v2` residuo, YAML valido, merge puliti su main HEAD.
- ⚠️ **Dimensioni sotto standard scene v1.1** (tutte 1536×2304 o inferiori; alcune s05 a 1024×1536 / 1086×1448 / 1632×2176). Ray: banner "sotto spec" accettato per questo giro, revisione a fine ciclo.
- 11 subhook placeholder aggiunti in annotations s04/s05 (`book_pages_total` 20→26 e 19→24) con `pov`/`page_book`/`text_split_marker` = "da compilare". Non in prosa → fuori dal montaggio (nessun crash). Pattern che si ripeterà nelle prossime storie.

### B. Bloccante trovato + fix (PR #54)

- **Causa:** `build_volume.parse_story_md`, con `@image TBD` in prosa, cercava solo il proxy low-res `_scene/sNN/sNN_hMMx.jpg`. Vol 1 ce l'ha; Vol 2 consegna **solo `_hd/`** → `img_path=None` → placeholder avorio su ogni scena, HD ignorati.
- **Fix:** aggiunta la sonda dell'HD convenzionale `_scene/sNN/_hd/{id}_hd.jpg` come terzo livello. Retro-compatibile (Vol 1 invariato), durevole per le prossime branch HD-only.
- **Verifica reale:** `build_volume.py --volume 2` (Pillow/reportlab installati) → **58/58 scene montate, 0 placeholder**, PDF libro (156MB) + stampa (165MB), 96 facciate. Ispezione visiva pagine confermata.

### C. Merge su main (separate 3 + fix)

- PR #51 (s04), #52 (s05), #53 (s06) — contenuto illustratore. PR #54 — fix manutentore `build_volume`. Tutte mergiate su main.
- `make sync` post-merge → chiuso il **debito derivati stale**: 12 writing_briefs + entities (mirror ×2) + dashboard rigenerati e committati.

### D. Note

- `check_image_quality` usa ancora la soglia v1 (1664×2496), non v1.1 (1824×2736): tutte le scene Vol 2 la mancano comunque. Soglia non toccata.
- Ambiente remoto: Pillow/reportlab/numpy/pymupdf installati ad hoc per il build; in CI sono già previsti.

### E. Prossimo passo Ray

1. **Cancellare da UI GitHub** (il proxy nega la delete dei ref da CLI): `claude/hd-storia-s04`, `claude/hd-storia-s05`, `claude/hd-storia-s06`, `claude/fix-build-volume-hd-only`, `claude/volume-2-branch-verify-hebg9i`.
2. Revisione immagini Vol 2 a fine ciclo (dimensioni sotto spec → sostituire HD ≥1824×2736 per togliere i banner).
3. Wiring in prosa degli 11 subhook placeholder (marker `@subhook` + `page_book`) quando decisi.
4. TODO Vercel ancora aperto (deploy fermo).

---



