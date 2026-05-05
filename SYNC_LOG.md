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

## SYNC-2026-05-05-012 — Mappa illustrata isola: nuova route `#/mappa-isola` nel catalogo_web

- **Stato:** DA_RIFLETTERE
- **Tipo:** catalogo_web (additivo, no modifiche grafo / no modifiche storie / no modifiche schede) + governance
- **Repo target:** Vercel deploy (target primario) + GitHub Pages (fallback compatibile)
- **Cambiamento:**
  1. **Nuova route `#/mappa-isola`** sul `catalogo_web/` — mostra mappa illustrata navigabile dell'isola (acquerello vista dall'alto) con 30 slot interattivi posizionati dai centroidi del geojson. Click slot → naviga a `#/entity/<id>`.
  2. **Asset 3D progressivi (Travian-style):** ogni slot mostra placeholder finché non c'è il PNG corrispondente in `cartografia/assets_mappa/<id>.png`. Workflow Grok Imagine lato Ray, specs in `cartografia/assets_mappa/README.md`.
  3. **File modificati / creati:**
     - `catalogo_web/index.html` — MOD (3 righe: link CSS + link sidebar + script tag)
     - `catalogo_web/app.js` — MOD (9 righe: blocco router `#/mappa-isola` + variant `?debug`)
     - `catalogo_web/mappa_isola.js` — NEW (~280 righe, modulo isolato `window.renderMappaIsola()`)
     - `catalogo_web/mappa_isola.css` — NEW (~140 righe, stili dedicati no-interferenza con `style.css`)
     - `cartografia/assets_mappa/README.md` — NEW (specs Grok per asset 3D)
     - `cartografia/assets_mappa/_base/isola_base_v1.jpg` — NEW (illustrazione master, 1120×912, ~150 KB)
     - `vercel.json` — MERGED (settings `cleanUrls: true` + `trailingSlash: false` dal pacchetto + headers nuovi geojson/assets_mappa + headers esistenti data/visual/js/css)
  4. **Smoke test passati:** vercel.json valido, JS syntax OK (`node --check`), tutti i path rispondono 200 su server locale, 30 slot estratti dal geojson (8 tipi: building/burrow/cave/pier/landmark/water_pool/tree/square).
  5. **Anomalie attese al primo deploy** (non bloccanti, dichiarate nel pacchetto): cluster villaggio sovrapposto + Case Basse/Capanna Bartolo/Casa Amo che cadono nel mare a sud. Risolvibili spostando coordinate nel geojson o introducendo zoom-villaggio in V2. Visibili con `?debug` (griglia rossa).
  6. **Pacchetto archiviato** in `_pacchetti_consegnati/mappa_isola_v1/` con `INTEGRATION.md` originale + `preview_calibrazione_v1.jpg` + `README.md` riassunto. Zip originale eliminato (file binari ridondanti, la repo contiene già tutti i file finali).
  7. **Pulito main:** rimossi `INTEGRATION.md` e `pacchetto_mappa_isola_v1.zip` dalla root.
- **File toccati:** 7 file in `catalogo_web/` + `cartografia/assets_mappa/`, `vercel.json`, `_pacchetti_consegnati/{README.md,mappa_isola_v1/}`, `SYNC_LOG.md`. Eliminati: `INTEGRATION.md`, `pacchetto_mappa_isola_v1.zip` da root.

---

## SYNC-2026-05-05-011 — Cornice editoriale 4 volumi: archiviato pacchetto `isola_4volumi_v2`

- **Stato:** DA_RIFLETTERE
- **Tipo:** pipeline_narrativa (additivo, no modifiche grafo / no modifiche storie definitive) + governance
- **Repo target:** n/a (informativo)
- **Cambiamento:**
  1. **Nuova sotto-cartella `pipeline_narrativa/storie_finali/_volumi/`** — cornice editoriale completa dei 4 volumi del libro. Pacchetto consegnato da Ray come zip (`isola_4volumi_v2.zip`).
  2. **Strategia di archivio: opzione C (per funzione)** — un file consolidato per sezione strutturale, con marker `## VOLUME N` interni per il compositore libro. Pattern coerente con `_scene/` / `_annotations/` / `_inventory/` (underscore prefix).
  3. **Mappa volumi → cicli grafo:** Vol1=A (s01-s03), Vol2=B (s04-s06), Vol3=C (s07-s09), Vol4=D (s10-s12). 3 storie per volume.
  4. **Estratti markdown da 2 .docx** via `python-docx`: `CORNICI_Soglia_Congedo.docx` → `soglia.md` + `congedo.md`; `PRESENTAZIONE_isola_completa.docx` → `presentazione_completa.md` (sorgente unica delle 23 doppie). Originali `.docx` NON conservati (decisione Ray).
  5. **5 markdown finali del pacchetto** copiati con naming snellito: `PIANO_EDITORIALE_4VOLUMI_v1.md` (mantiene nome storico) + `introduzioni_cicli.md` + `stato_zero_e_sigilli.md` + `presentazioni_parziali.md` + `porte.md`.
  6. **`_elementi_fissi/` (read-only):** `STATO_ZERO_originale.md` + `LE_PORTE_cornice_narrativa_v2.md` (riferimenti per audit).
  7. **Decisione editoriale Ray (2026-05-05):** simboli `Δ / ⇄ / ⟳ / Integrazione` ancora presenti nei file → da sostituire con `A / B / C / D` in revisione editoriale futura (i simboli sono "troppo EAR-leggibili", e EAR resta invisibile). Nessun edit ora — Ray farà revisione completa prima della composizione libri, modificando direttamente i file qui.
  8. **README dedicato** in `_volumi/README.md`: mappa volume→ciclo, struttura 7 sezioni, file inventory, pattern compositore libro (split per `## VOLUME N`), vincoli, stato completamento.
  9. **CLAUDE.md mappa repo** aggiornata con riga `_volumi/`.
  10. **storie_finali/README.md tabella cartelle gemelle** estesa con riga `_volumi/`.
- **Lavori pendenti (Ray, prima della composizione libri):**
  - Revisione "morale" delle 4 introduzioni (segnalata dallo stesso piano editoriale)
  - Sostituzione etichette `Δ/⇄/⟳/Integrazione` → `A/B/C/D` ovunque
  - 9 tracce bambini delle Porte sono già scritte (non da-fare nonostante il piano dica "da scrivere" — il piano è stato consegnato in fase intermedia)
- **File toccati:** `pipeline_narrativa/storie_finali/_volumi/` (NEW directory + 9 file + README + 2 file `_elementi_fissi/`), `pipeline_narrativa/storie_finali/README.md`, `CLAUDE.md`, `SYNC_LOG.md`.

---

## SYNC-2026-05-05-010 — Pattern `_scene/` per immagini-scena composte + 4 reference visive

- **Stato:** DA_RIFLETTERE
- **Tipo:** visual + pipeline_narrativa (additivo, no modifiche grafo) + governance
- **Repo target:** n/a (informativo per agenti IA futuri / collaboratori esterni)
- **Cambiamento:**
  1. **Nuovo pattern cartella `pipeline_narrativa/storie_finali/_scene/sNN/sNN_hMMx.jpg`** per immagini-scena composte = una pagina libro fisica = una illustrazione. Parallelo a `_annotations/` e `_inventory/`. Naming deterministico (`sNN_hMMx.jpg`, x ∈ {a,b,c,...}). NON sostituisce `visual/<id>/immagini/<id>_canonica_v1_*.jpg` (reference catalogo) — sono livelli ortogonali: reference catalogo vs prodotto finale composto.
  2. **Marker `@subhook ... @image`** nel testo storia popolabile dal path `_scene/`. Prima entry attiva: `s01_h01b` → `_scene/s01/s01_h01b.jpg` (Fiamma consegna pagnotta a Gabriel).
  3. **4 nuove reference visuali aggiunte/sostituite:**
     - `visual/luoghi/villaggio_centrale/piazza_villaggio/immagini/piazza_villaggio_canonica_v1_panoramica.jpg` (NEW)
     - `visual/luoghi/quartiere_aria/via_che_sale/immagini/via_che_sale_canonica_v1_panoramica.jpg` (NEW)
     - `visual/luoghi/quartiere_fuoco/forno/immagini/forno_canonica_v1_esterno_alba.jpg` (sostituita)
     - `visual/luoghi/quartiere_fuoco/forno/immagini/forno_canonica_v1_laboratorio_verticale.jpg` (sostituita)
  4. **Documentazione aggiornata:**
     - `pipeline_narrativa/storie_finali/README.md` — sezione `_scene/` aggiunta + tabella cartelle gemelle + esempio parsing Python a 2 livelli (@hook + @subhook)
     - `CLAUDE.md` — mappa repo + sezione "Modalità compositore libro" aggiornate con pattern subhook + `_scene/`
- **File toccati:** `CLAUDE.md`, `SYNC_LOG.md`, `pipeline_narrativa/storie_finali/README.md`, `pipeline_narrativa/storie_finali/s01_la_nebbia_delle_montagne_gemelle.md` (1 marker @image popolato), `pipeline_narrativa/storie_finali/_scene/s01/s01_h01b.jpg` (NEW), 3 file in `visual/luoghi/.../immagini/`, `catalogo_web/data/{entities,storie}.json` (rigenerati).
- **Trail:** 2 commit in `claude/project-setup-tZsHS` → ff merge su main (`6e66dd3` Forno esterno + `4cffa77` 4 immagini).

---

## SYNC-2026-04-30-009 — Fase F.2 visual prompt grok (28 prompt) + Fase Cornice del Mondo (7 step) + Brieffer install (12 brief)

- **Stato:** DA_RIFLETTERE
- **Tipo:** visual + pipeline_narrativa (modifica autorizzata da Ray con pacchetto `cornice_mondo_pacchetto`) + governance
- **Repo target:** archivio storico `isola_tre_venti_github` (Bible/grafo riallineamento), pipeline immagini esterna (chi genera con Grok Imagine).
- **Cambiamento (3 macro-fasi nello stesso giorno):**

  **A. Visual prompt grok (Fase F.2 in corso, 28 prompt totali):**
  - 14 prompt_grok.md per personaggi: 3 fratelli (Gabriel/Elias/Noah), 4 primari (Rovo/Stria/Mèmolo/Grunto — Fiamma/Bartolo già canonizzati), 4 secondari (Salvia/Nodo/Amo/Zolla), 5 cuccioli (Pun/Toba/Bru/Cardo/Liù).
  - 13 prompt_grok.md per oggetti: tutti i 13 oggetti-simbolo + grembiule_fiamma pre-esistente + pallone_di_stoffa_cucita (oggetto di scena ricorrente).
  - Schede personaggio canonizzate per fratelli (Gabriel/Elias/Noah, opzione B "fittizio canonico"), Rovo (canonical), pescatori_case_basse (nuovo collettivo).
  - Stylesheet saga acquerello+inchiostro storybook applicato uniforme (Beatrix Potter / Brian Wildsmith). Ogni prompt = 4 immagini canoniche per personaggi (`fronte`/`modalità_X`/`modalità_Y`/`turnaround`), 1-2 per oggetti. Naming canonico `<id>_canonica_v1_<vista>.jpg`.
  - **Workflow esterno:** Ray estrae i prompt da GitHub, genera con Grok Imagine, carica le immagini negli `immagini/` di ogni entità.

  **B. Fase "Cornice del Mondo" (7 step, completata):**
  - **Step 1+2** (`c824496`): nuovo nodo radice `world_conventions` nel grafo con `refrain_animal_identification` (formula sg+pl, 6 gruppi eligibili tra cui il nuovo `pescatori_case_basse`, pool animali, vincoli) + `path_details: {paths: {}}` placeholder. Esteso `quote_tracker.refrain_animal_used_per_story: []`. Bump `schema_version 1.3 → 1.4`, `graph_version 1.1.0 → 1.2.0`.
  - **Step 3** (`a3e654e`): `## Saluto del gruppo` aggiunto in 5 schede collettivi esistenti (camminanti/mantenitori/coltivatori_del_cerchio/mercato_del_mezzogiorno/pastori) + creata nuova scheda `visual/personaggi/collettivi/pescatori_case_basse/scheda.md` (6° gruppo-istituzione, decisione Ray 2026-04-30). Catalogo: 115 → 116 entità.
  - **Step 4** (`8b70958`): 24 `cornice_dettagli` distribuite nelle 12 storie (2/storia) + 8 tuple in `quote_tracker.refrain_animal_used_per_story` (5 SG + 2 PL formule applicate, 11 animali distinti tutti unici saga) + 2 nuove entry `cantilene_coltivatori_stories` (s08 pre-crack, s09 modulazione compleanno). Distribuzione cornici per processo: A=4, B=5, C=6, D=6, E=3.
  - **Step 5** (`92e87b6`): 36 sentieri "fantasma" appesi a `locations_secondary` di 12 storie (mappa DOC_4 §4).
  - **Step 6** (`83e361e`): popolato `world_conventions.path_details.paths` con i 5 sentieri Tier A (via_dell_alba 6 dettagli, sentiero_orti_torrente_foresta 4, via_che_sale 4 incluso cardo evolvente, sentiero_orti_casa_salvia 3, viottolo_perimetrale_piazza 3 = 20 totali). Schema slot **senza campo `tipo`** (decisione Ray).
  - **Step 7** (`de87ac2` + `9b8c30e`): aggiornata sezione `## Coerenza cross-scena (cose che NON cambiano)` di 5 schede sentieri Tier A con elenco dettagli stabili (rimando al grafo via `path_details.paths.<id>`).

  **C. Brieffer install (`544d5fc` + `b7a2b6c`):**
  - Aggiunto `scripts/build_writing_brief.py` (1128 righe). Generatore meccanico (zero token LLM) di dossier autosufficiente per agente prosa: pesca da grafo + narrazione fattuale + schede catalogo + prompt grok + cornici + sentieri + saluti + formula ritornello.
  - Aggiunto `skills/brieffer/SKILL.md`.
  - Generati 12 brief in `pipeline_narrativa/writing_briefs/sNN_writing_brief.md` (16k-32k parole/brief).
  - Reference originale Ray salvato in `pipeline_narrativa/writing_briefs/_reference/s01_writing_brief_FINAL.md`.
  - Test: `s01_writing_brief.md` identico a reference (1730 righe, diff vuoto).

- **Decisioni autoriali Ray applicate (2026-04-30):**
  - 6° gruppo-istituzione `pescatori_case_basse`: SI (catalogo + grafo + 2 cornici).
  - Pattern A pre-eco s03 (conchiglia caduta): NO incremento `pattern_a_pre_eco_stories` (cornice scritta come oggetto_anomalo, minimo invasivo).
  - narrator_address s09 (cantilena modulata): NO incremento `addresses_to_reader` (resta a 4 voci).
  - Riequilibrio Giro E: SI, cornice S07-C1 spostata da Giro D a Giro E.
  - Schema slot dettaglio sentiero: campo `tipo` rimosso.
  - Vincolo DOC_1 §2 "tre nomi, mai quattro": s08-c2 plurale Mantenitori = 3 nomi (arvicola/ghiro/faina).
  - Vincolo DOC_1 §3.4 unicità saga: s12-c1 Camminanti = ermellino (sostituito da "faina" che era già usata in s08).

- **Backup chain (in `pipeline_narrativa/`):**
  - `story_graph.v0.10.0.backup.json` (pre-fase E)
  - `story_graph.json.pre_v1_3.backup.json` (pre-bump schema 1.3)
  - `story_graph.json.pre_fase_g.backup.json` (pre-hook estesi)
  - `story_graph.json.pre_cornice_mondo.backup.json` (pre-Step 1+2 oggi)
  - `story_graph.json.pre_step4_cornici.backup.json` (pre-Step 4 oggi)
  - `story_graph.json.pre_step5_sentieri.backup.json` (pre-Step 5 oggi)
  - `story_graph.json.pre_step6_path_details.backup.json` (pre-Step 6 oggi)

- **Commit principali della giornata:** `c824496` `a3e654e` `8b70958` `92e87b6` `83e361e` `de87ac2` `9b8c30e` `544d5fc` `b7a2b6c` (+ ~25 commit di prompt grok prima di pacchetto cornice del mondo).

- **File toccati (alto livello):**
  - `pipeline_narrativa/story_graph.json` (additivo) + 4 backup canonici nuovi.
  - `pipeline_narrativa/writing_briefs/` (nuova directory, 12 brief + reference).
  - `scripts/cornice_mondo/` (nuova directory: 4 script + 4 YAML + audit/ vuota).
  - `scripts/build_writing_brief.py` (nuovo).
  - `skills/brieffer/SKILL.md` (nuovo).
  - `visual/personaggi/individuali/{bambini,primari,secondari,cuccioli}/*/prompt_grok.md` (28 file totali fino a oggi).
  - `visual/personaggi/individuali/bambini/{gabriel,elias,noah}/scheda.md` (canonical, opzione B).
  - `visual/personaggi/individuali/primari/rovo/scheda.md` (canonical).
  - `visual/personaggi/collettivi/{camminanti,mantenitori,coltivatori_del_cerchio,mercato_del_mezzogiorno,pastori}/scheda.md` (Saluto del gruppo).
  - `visual/personaggi/collettivi/pescatori_case_basse/scheda.md` (nuovo).
  - `visual/oggetti/*/prompt_grok.md` (13 nuovi + grembiule preesistente).
  - 5 schede sentieri Tier A in `visual/luoghi/.../strade/.../scheda.md` con dettagli stabili.
  - DOC_1..DOC_6 e README originale del pacchetto cornice del mondo presenti in root come riferimento autoriale.
  - `catalogo_web/data/entities.json` rigenerato (115 → 116 entità).

- **Da riflettere altrove:**
  - **Pipeline immagini esterna (Grok Imagine):** chi genera ha ora 28 prompt canonici disponibili in `visual/personaggi/.../prompt_grok.md` e `visual/oggetti/.../prompt_grok.md`. Le immagini canoniche generate vanno in `immagini/<id>_canonica_v1_<vista>.jpg`.
  - **Archivio storico `isola_tre_venti_github`:** schema grafo bumpato 1.3 → 1.4 (additivo). Se la copia storica è 1.3, va sincronizzata o lasciata congelata come snapshot.
  - **Repo prompt esterne:** se cachano lista entità/animali/gruppi-istituzione, c'è ora un 6° gruppo (`pescatori_case_basse`) e nuove tuple animali assegnate alle storie (vedi `quote_tracker.refrain_animal_used_per_story` per dettaglio).
  - **GitHub Pages catalogo_web:** auto-rideploy su push main, già aggiornato. Niente azione richiesta.

---

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

## SYNC-2026-04-28-008 — Pulizia Bible: rimozione strato visivo (migrato al catalogo)

- **Stato:** DA_RIFLETTERE
- **Tipo:** governance + pipeline_narrativa (modifica eccezionale richiesta da Ray)
- **Repo target:** archivio storico `isola_tre_venti_github` (Bible duplicata altrove va riallineata).
- **Cambiamento di policy:**
  - Aggiornato `skills/README.md` §2 con eccezione esplicita: `pipeline_narrativa/` è read-only **per l'agente IA**, modificabile da Ray con SYNC_LOG entry dedicata.
  - Nuova §3 "Architettura informativa: Bibbia + Grafo + Catalogo (no ridondanze)": tabella delle 3 fonti + regola di non-duplicazione (un dato vive in una sola fonte; visivo → catalogo, narrativo → Bible, dinamico → grafo).
  - `skills/visual/compilatore.md` aggiornato con nota di chiusura del bulk e dichiarazione che dopo questa pulizia il catalogo è autoritativo per il visivo.
- **Cambiamento sostanziale (Bible v2):**
  - File da **873 → 761 righe** (~13% riduzione complessiva, ~25-35% sulle sezioni toccate).
  - **§4.4 FIAMMA** pulita come campione (rimossi blocchi Aspetto, Comportamento operativo, parte cliché di Note e vincoli, dettagli visivi della casa). Mantenuti: Specie/ruolo/residenza compatto, Voce tipica, Detti popolari, Funzione narrativa, Note e vincoli (narrativi). Aggiunto redirect compatto al catalogo.
  - **§4.3-§4.21 (18 sezioni)** stesso pattern (sub-agente).
  - **§2.2 Gabriel, §2.3 Elias, §2.4 Noah** rimossa la breve descrizione fisica ("Capelli...").
  - **§6 PALETTE VISIVA** intera sezione collassata in redirect generale (palette migrate alle schede del catalogo).
  - **§8 ATLANTE** descrizioni fisiche dei luoghi rimosse: introduzione (cintura), §8.1 Villaggio (Albero Vecchio, case, scuola), §8.2-§8.5 quartieri (rimossi odori/suoni/atmosfera/dettagli edifici), §8.6 fascia costiera (rimossi dettagli est/ovest/nord). Mantenuti: posizione, lista entità, vento di pertinenza, distanze, abitanti permanenti, regole funzionali.
  - **§1.3 venti** invariato (non conteneva descrizioni visive).
  - **§8.7-§8.9** invariate (regole temporali, mondo aperto).
- **Pattern di pulizia (validato):** redirect compatto `> *Profilo visivo → visual/...*` invece di redirect granulari per sezione. Variante A massimalista.
- **Razionale:** ottimizzazione token nella scrittura agentica. Quando l'IA pesca una scheda personaggio per scrivere una storia, non c'è ridondanza Bible/catalogo da risolvere. Routing senza ambiguità: visivo → catalogo, narrativo → Bible, dinamico → grafo.
- **Conseguenza per workflow:**
  - Da ora dettagli visivi nuovi (es. "il grembiule di Fiamma ha un cuore rosso cucito") vanno SOLO nel catalogo, mai in Bible.
  - Lo script di travaso meccanico Bible→catalogo non si rilancia (non c'è più cosa travasare). `compilatore` resta come metodo storico.
  - Se Ray modificherà la Bible in futuro (es. nuova frase di Voce tipica), la modifica resta in Bible e il catalogo non si tocca (sono già disgiunti).
- **Commit:** _da inserire dopo commit_.
- **File toccati:** `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md`, `skills/README.md`, `skills/visual/compilatore.md`.
- **Da riflettere altrove:** se altre repo del sistema hanno copia della Bible, vanno aggiornate. Se altri agenti/sistemi pescano dalla Bible per dati visivi, devono essere reindirizzati al catalogo.

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
