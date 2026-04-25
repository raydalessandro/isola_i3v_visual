# SYNC_LOG — Cambiamenti da riflettere altrove

Questo file traccia ogni modifica fatta in `isola_i3v_visual` che **impatta o potrebbe impattare altre repo del sistema** (archivio storico `isola_tre_venti_github`, future repo prompt, sito esterno, pipeline immagini, ecc.). Ray (o un agente) parte da qui per riallineare le altre repo.

**Convenzione di entry:**
- ID univoco progressivo: `SYNC-YYYY-MM-DD-NNN`.
- Stato: `DA_RIFLETTERE` (default), `RIFLESSO` (Ray segna quando ha propagato), `SUPERATO` (entry sostituita da una successiva).
- Tipo: `bootstrap` / `cartografia` / `skills` / `visual` / `pipeline_input` / `governance`.
- Repo target: lista delle repo (o "n/a" se solo informativo).
- Cambiamento: descrizione tecnica concisa.
- File toccati: lista (gruppi se molti).

---

## SYNC-2026-04-25-001 — Bootstrap repo `isola_i3v_visual`
- **Stato:** DA_RIFLETTERE
- **Tipo:** bootstrap
- **Repo target:** archivio storico `isola_tre_venti_github` (informativo, archive-only). Eventuali repo che linkavano a `cartografia_tecnica/` come path.
- **Cambiamento:** repo unificato che ospita tre tracce:
  - `cartografia/` (ex `cartografia_tecnica/`, rinominata).
  - `pipeline_narrativa/` (input read-only invariato).
  - `visual/` (nuova directory, in attesa brief).
- **Commit:** `c863f3f`.
- **File toccati:** struttura intera + README + .gitignore + PROJECT_STATE.
- **Da riflettere altrove:** path `cartografia_tecnica/` → `cartografia/` se altre repo o documenti citano il vecchio nome.

## SYNC-2026-04-25-002 — Refactor AGENT_INSTRUCTIONS → `skills/`
- **Stato:** DA_RIFLETTERE
- **Tipo:** skills
- **Repo target:** n/a (governance interna del repo).
- **Cambiamento:** rimosso `AGENT_INSTRUCTIONS.md` monolitico, sostituito con `skills/`:
  - `skills/README.md` orchestratore + regole comuni (isolamento `pipeline_narrativa/` read-only, comunicazione, rifiuto, permessi di scrittura per skill).
  - `skills/cartografo.md` skill cartografia, scope `cartografia/`.
  - `skills/visual.md` skill visual, scope `visual/`, placeholder.
- **Commit:** `2259e5e`.
- **File toccati:** `AGENT_INSTRUCTIONS.md` (rimosso), `skills/*` (nuovi), `README.md`, `PROJECT_STATE.md`.
- **Da riflettere altrove:** se altre repo del sistema hanno un AGENT_INSTRUCTIONS analogo, considerare rifattorizzazione coerente (skill-based).

## SYNC-2026-04-25-003 — Cartografia v0.5 → v0.6.0 (sync grafo v0.10.0)
- **Stato:** DA_RIFLETTERE
- **Tipo:** cartografia
- **Repo target:** archivio storico `isola_tre_venti_github` (per allineamento copia di lavoro), eventuali repo prompt che pescano ID feature.
- **Cambiamento sintetico:**
  - **Aggiunta** feature `radura_dei_pini` (Polygon, status `provvisorio`, quartiere `terra`) — landmark interno alla Foresta Intrecciata, margine NE verso Pascoli Alti. Citato in S12.
  - **Promotion** `sentiero_roccia_burrone` da `provvisorio` a `canonico`. Giustificato da S12 (resolution_mode: "la cengia che sale a Roccia Alta — i fratelli la sanno senza che nessuno la indichi").
  - **Annotazione** in `roccia_alta.note`: la cengia di accesso da sud è `sentiero_roccia_burrone` (non entità autonoma).
  - **Alias aggiunto** `guado_nord` → `guado_di_pietre_piatte` (citato in S12 come "guado nord dove l'acqua trema piano").
  - **Bump** `metadata.version` 0.5 → 0.6.0; aggiunta `changes_from_v0_5`.
- **Backward-compat grafo↔cartografia:** 100% (verificato pre e post).
- **Grafo di riferimento:** `pipeline_narrativa/story_graph.json` v0.10.0.
- **Decisione architetturale richiamata:** "casa_fratelli non entity, l'isola è protagonista" (blocco_0). Il "cortile" citato in `s10.wind_notes` non viene mappato per coerenza con questa decisione.
- **Commit:** _da inserire dopo commit_.
- **File toccati:** `cartografia/geo/island.geojson`, `cartografia/CHANGELOG.md`, `PROJECT_STATE.md`.
- **Da riflettere altrove:** se altre repo cachano la lista feature o gli ID, rigenerare. Nessun rename di ID esistenti, solo aggiunte/promotion/alias.

---

## SYNC-2026-04-25-007 — Catalogo web V1 (sito interno statico)
- **Stato:** DA_RIFLETTERE
- **Tipo:** governance + tool web
- **Repo target:** GitHub Pages (URL pubblico interno `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`).
- **Cambiamento:**
  - Nuova directory `catalogo_web/` con sito statico HTML+CSS+JS vanilla per consultazione di tutte le entità di `visual/`. Niente React, niente build pipeline.
  - File: `index.html`, `style.css`, `app.js`, `README.md`, `data/entities.json` (generato).
  - Nuovo script `scripts/build_catalogo_web.py`: scansiona `visual/` ricorsivamente, parsa frontmatter YAML (richiede PyYAML) + body MD, raccoglie immagini, costruisce albero gerarchico riflesso della struttura folder, sovrascrive `entities.json`. Idempotente. Da rilanciare quando schede o immagini cambiano.
- **Funzionalità V1:**
  - Sidebar ad albero navigabile (stesso nesting frattale di `visual/`), search testuale per nome/id, pagina entità con tag/frontmatter/body MD/gallery immagini, pagina indice strade, link al viewer cartografia esistente, hash routing client-side.
- **Deploy:** GitHub Pages serve `main` dalla root del repo. Da abilitare in Settings → Pages → Source: main, Folder: `/`. Auto-rideploy a ogni push. Path `catalogo_web/` accessibile direttamente.
- **Test locale:** `python3 -m http.server` dalla radice → `http://localhost:8000/catalogo_web/`.
- **Commit:** _da inserire dopo commit_.
- **File toccati:** `catalogo_web/{index.html,style.css,app.js,README.md,data/entities.json}`, `scripts/build_catalogo_web.py`, `PROJECT_STATE.md`.
- **Da riflettere altrove:** richiede PyYAML come dipendenza Python (`pip install pyyaml`). Documentato in `catalogo_web/README.md` e `scripts/README.md`.

---

## SYNC-2026-04-25-006 — Visual: introduzione sotto-skill `compilatore` + cambio metodo "completa, non rimuovere"
- **Stato:** DA_RIFLETTERE
- **Tipo:** skills + visual (governance)
- **Repo target:** n/a (interna).
- **Cambiamento di metodo (richiesto da Ray):**
  - Principio precedente: "sezioni non applicabili → rimuovile dalla scheda".
  - Principio nuovo: "completa tutte le 14 sezioni, anche con inferenza canone-coerente marcata. Niente rimozioni: una sezione vuota è un'occasione persa per la narrativa futura. Le schede diventano serbatoio di proposte che la narrativa puo' raccogliere."
  - Marcatori di provenienza in linea: nessun tag = canone (citato in fondo); `[inf]` = inferito dai dati canonici; `[prop]` = proposta visiva da validare.
- **Cambiamenti strutturali:**
  - `skills/visual.md` spostato in `skills/visual/README.md` (la skill visual diventa cartella per ospitare sotto-skill specializzate).
  - Nuova sotto-skill: `skills/visual/compilatore.md` — formalizza il metodo di compilazione body schede (estrazione mirata, lettura fonti, completamento marcato, citazioni, vincoli operativi, esempio canonico Liu).
  - `visual/_template_scheda.md` aggiornato col nuovo principio.
  - `skills/README.md` aggiornato con riferimento alle sotto-skill e tabella permessi estesa.
  - Path aggiornati in `README.md` (radice), `visual/README.md`, `scripts/README.md`.
- **Esempio applicato:** `visual/personaggi/individuali/cuccioli/liu/scheda.md` ricompilata col nuovo principio (sezione "Abbigliamento / stato d'uso" reinserita come stato ali / marcature / accessori effimeri / pulizia, marcata con `[inf]` e `[prop]`).
- **Sotto-skill future previste (placeholder, non create finche' non servono):** `prompter.md` (genera prompt da schede), `generatore_immagini.md` (4 vedute 3D + variazioni IA).
- **Commit:** _da inserire dopo commit_.
- **File toccati:** `skills/visual/{README.md,compilatore.md}`, `skills/README.md`, `visual/_template_scheda.md`, `visual/personaggi/individuali/cuccioli/liu/scheda.md`, `visual/README.md`, `README.md` (radice), `scripts/README.md`, `SYNC_LOG.md`, `PROJECT_STATE.md`.
- **Da riflettere altrove:** se in altre repo ci sono sub-flussi di compilazione visiva, allinearli al principio "completa, non rimuovere" e ai marcatori `[inf]`/`[prop]`.

---

## SYNC-2026-04-25-005 — Visual: aggiunta delle 31 strade (sentieri/viottoli)
- **Stato:** DA_RIFLETTERE
- **Tipo:** visual
- **Repo target:** n/a (interna).
- **Cambiamento:**
  - `scripts/build_visual_skeleton.py` esteso con sezione strade + helper `path_metadata()` (calcolo lunghezza euclidea, endpoint_a/b, n_punti, parsing token id).
  - 31 schede stub aggiunte in `visual/luoghi/<quartiere>/strade/<id>/`. Le 5 Vie principali (`entities.locations`) restano paritetiche con gli altri luoghi del quartiere.
  - File auto-generato `visual/luoghi/_strade_index.md` per consultazione veloce (tabella per quartiere con id, name, category, status, lunghezza, endpoints, link).
  - Frontmatter strade contiene `categoria_strada` (top-level) + metadati cartografici estesi nel sotto-dizionario `cartografia` (lunghezza, n_punti, endpoint_a_m, endpoint_b_m, endpoints_inferiti_dal_id).
- **Convenzione richiamata da Ray:** strade che attraversano piu' quartieri restano nel `quarter` indicato dal GeoJSON (tipicamente `perimetro`). Se in futuro l'organizzazione diventa scomoda, si valuta split per tratti.
- **Commit:** _da inserire dopo commit_.
- **File toccati:** `scripts/build_visual_skeleton.py`, `visual/luoghi/<vari>/strade/`, `visual/luoghi/_strade_index.md`, `visual/catalogo.md`, `skills/visual.md`, `PROJECT_STATE.md`.
- **Da riflettere altrove:** quando il sito interno verrà costruito, dovrà includere anche le strade.

---

## SYNC-2026-04-25-004 — Visual: bootstrap struttura entità + `scripts/`
- **Stato:** DA_RIFLETTERE
- **Tipo:** visual + governance
- **Repo target:** n/a (interna). Le altre repo del sistema dovranno sapere che `visual/` è la fonte unica per descrizioni visive di tutte le entità della saga.
- **Cambiamento:**
  - Creata `scripts/` (tool condivisi tra skill); aggiunto `scripts/build_visual_skeleton.py` (idempotente).
  - Generata struttura `visual/` con **81 schede stub** in cartelle frattali (personaggi diviso in bambini/primari/cuccioli/secondari + collettivi; luoghi con nesting geografico per quartiere; oggetti/venti/visual_signatures flat).
  - Ogni entità: cartella autocontenuta con `scheda.md` (frontmatter YAML + body stub a 14 sezioni) + `immagini/` (predisposta per riferimenti IA + 4 vedute 3D).
  - Frontmatter luoghi popolato con metadati cartografici (centroide, bbox, dimensioni m, quartiere, parent/children, geometry_type, altitudine quando ci sarà).
  - `visual/README.md` + `visual/_template_scheda.md` + `visual/catalogo.md` auto-rigenerabile.
  - `skills/visual.md` riscritto con workflow concreto e gerarchia fonti (verità tendenzialmente nel grafo).
  - `skills/README.md` aggiunto `scripts/` come directory condivisa.
- **Decisioni Ray richiamate:**
  - Niente prompt-string pronti come asset principale: schede contengono descrizioni ricche multi-uso (IA, 3D, narrativa, social). Eventuali prompt dedicati per modello vivono nella cartella entità come file aggiuntivi.
  - Disallineamenti grafo↔Bible: debito tecnico noto, gestito fuori repo. Per visual la verità tendenzialmente è nel grafo; caso per caso si segnala.
- **Commit:** _da inserire dopo commit_.
- **File toccati:** `scripts/`, `visual/`, `skills/visual.md`, `skills/README.md`, `PROJECT_STATE.md`.
- **Da riflettere altrove:** quando partirà la pipeline immagini effettiva, dovrà attingere da `visual/<entita>/scheda.md` come fonte; se altre repo avevano descrizioni visive isolate, considerare la migrazione qui.

---

## Note

- Ray ha annunciato che a breve farà manutenzione sul grafo storie e porterà qui la versione manutenuta come **nuova baseline**. Quando arriverà, registrarla qui come entry SYNC dedicata.
- Le entry restano come storico anche dopo essere state riflesse (mai cancellare). Cambiare solo lo stato.
