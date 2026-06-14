window.DASHBOARD_DATA = {
 "generated_at": "2026-06-14T11:17:13+00:00",
 "head": {
  "sha": "d5ead04",
  "date": "2026-06-14T10:38:34+00:00"
 },
 "agent_entry": {
  "sequence": [
   {
    "path": "CLAUDE.md",
    "bytes": 12194,
    "lines": 128,
    "tokens_est": 3048,
    "mtime": "2026-06-12T13:03:53+00:00",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/CLAUDE.md",
    "role": "Router. Regole stabili + tabella di routing. Letto sempre per primo.",
    "tokens_cumulative": 3048
   },
   {
    "path": "PROJECT_STATE.md",
    "bytes": 5986,
    "lines": 95,
    "tokens_est": 1496,
    "mtime": "2026-06-12T12:49:33+00:00",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/PROJECT_STATE.md",
    "role": "Snapshot operativo: stato corrente + ultima sessione.",
    "tokens_cumulative": 4544
   },
   {
    "path": "saga_config.yaml",
    "bytes": 4534,
    "lines": 136,
    "tokens_est": 1134,
    "mtime": "2026-06-11T18:45:12+00:00",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/saga_config.yaml",
    "role": "Canone macchina: id, marker, lessico, vincoli (single source of truth).",
    "tokens_cumulative": 5678
   },
   {
    "path": "docs/MAPPA_REPO.md",
    "bytes": 11872,
    "lines": 135,
    "tokens_est": 2968,
    "mtime": "2026-06-12T12:05:54+00:00",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/MAPPA_REPO.md",
    "role": "Mappa annotata delle directory (consultata se serve navigare).",
    "tokens_cumulative": 8646
   },
   {
    "path": "Makefile",
    "bytes": 1958,
    "lines": 59,
    "tokens_est": 490,
    "mtime": "2026-06-13T08:25:42+00:00",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/Makefile",
    "role": "Comandi disponibili (make help).",
    "tokens_cumulative": 9136
   }
  ],
  "base_tokens_est": 9136,
  "note": "Dopo il router l'agente legge UNA skill pertinente (tabella di routing). Costo aggiuntivo per skill qui sotto.",
  "skills_cost": [
   {
    "role": "brieffer",
    "path": "skills/brieffer/SKILL.md",
    "bytes": 7772,
    "lines": 213,
    "tokens_est": 1943,
    "tokens_total_entry": 11079,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/brieffer/SKILL.md"
   },
   {
    "role": "prosa",
    "path": "skills/prosa/SKILL.md",
    "bytes": 11792,
    "lines": 260,
    "tokens_est": 2948,
    "tokens_total_entry": 12084,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/prosa/SKILL.md"
   },
   {
    "role": "canonizzatore",
    "path": "skills/canonizzatore/SKILL.md",
    "bytes": 1498,
    "lines": 27,
    "tokens_est": 374,
    "tokens_total_entry": 9510,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/canonizzatore/SKILL.md"
   },
   {
    "role": "visual",
    "path": "skills/visual/SKILL.md",
    "bytes": 13902,
    "lines": 239,
    "tokens_est": 3476,
    "tokens_total_entry": 12612,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/visual/SKILL.md"
   },
   {
    "role": "illustratore",
    "path": "skills/illustratore/SKILL.md",
    "bytes": 14349,
    "lines": 310,
    "tokens_est": 3587,
    "tokens_total_entry": 12723,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/illustratore/SKILL.md"
   },
   {
    "role": "atlantista",
    "path": "skills/atlantista/SKILL.md",
    "bytes": 7082,
    "lines": 152,
    "tokens_est": 1770,
    "tokens_total_entry": 10906,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/atlantista/SKILL.md"
   },
   {
    "role": "scenografo",
    "path": "skills/scenografo/SKILL.md",
    "bytes": 12390,
    "lines": 158,
    "tokens_est": 3098,
    "tokens_total_entry": 12234,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/scenografo/SKILL.md"
   },
   {
    "role": "cartografo",
    "path": "skills/cartografo/SKILL.md",
    "bytes": 10151,
    "lines": 223,
    "tokens_est": 2538,
    "tokens_total_entry": 11674,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/cartografo/SKILL.md"
   },
   {
    "role": "contributore",
    "path": "skills/contributore/SKILL.md",
    "bytes": 2652,
    "lines": 79,
    "tokens_est": 663,
    "tokens_total_entry": 9799,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/contributore/SKILL.md"
   },
   {
    "role": "manutentore",
    "path": "skills/manutentore/SKILL.md",
    "bytes": 4486,
    "lines": 83,
    "tokens_est": 1122,
    "tokens_total_entry": 10258,
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/manutentore/SKILL.md"
   }
  ]
 },
 "skills": [
  {
   "role": "brieffer",
   "trigger": "generare/aggiornare i writing brief delle 12 storie (operatore di estrazione, zero token)",
   "scope_write": "pipeline_narrativa/writing_briefs/ (solo via script)",
   "commands": "make briefs",
   "order": 10,
   "preview": "**Per l'agente che si occupa di generare/aggiornare i writing brief della saga.**  Questa skill descrive: cosa fai, quando lo fai, come lo fai, e quando NON intervenire.",
   "path": "skills/brieffer/SKILL.md",
   "bytes": 7772,
   "lines": 213,
   "tokens_est": 1943,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/brieffer/SKILL.md"
  },
  {
   "role": "prosa",
   "trigger": "scrivere il testo finale di una storia in chat collaborativa con Ray, una pagina alla volta",
   "scope_write": "solo chat — non tocca la repo",
   "commands": "—",
   "order": 20,
   "preview": "**Da incollare all'inizio di una chat del progetto \"L'Isola dei Tre Venti\" su Claude.ai per attivare la modalità scrittura.**  Questo prompt si autoinizia: leggi le istruzioni, fetcha il brief richiesto da GitHub, e cominci a scrivere insi…",
   "path": "skills/prosa/SKILL.md",
   "bytes": 11792,
   "lines": 260,
   "tokens_est": 2948,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/prosa/SKILL.md"
  },
  {
   "role": "canonizzatore",
   "trigger": "canonizzazione completa di una scheda visual (scheda + prompt grok + descrizione social + immagini canoniche, fase F.2)",
   "scope_write": "visual/ (schede della entità in lavorazione) — via flusso _visual_pipeline/",
   "commands": "make catalogo (dopo ogni scheda)",
   "order": 30,
   "preview": "**La skill operativa vive in `_visual_pipeline/`** (pacchetto autosufficiente con canone, template, esempi validati e checklist). Questo file esiste per la trovabilità: tutte le skill si trovano in `skills/<ruolo>/SKILL.md`.",
   "path": "skills/canonizzatore/SKILL.md",
   "bytes": 1498,
   "lines": 27,
   "tokens_est": 374,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/canonizzatore/SKILL.md"
  },
  {
   "role": "visual",
   "trigger": "descrizioni visive, vincoli prompt, immagini reference (famiglia visual; per la compilazione schede vedi compilatore.md)",
   "scope_write": "visual/, scripts/ (tool condivisi)",
   "commands": "make catalogo",
   "order": 40,
   "preview": "**Scope:** costruisci e mantieni il **serbatoio di descrizioni visive** di tutte le entità della saga (personaggi, luoghi, oggetti, venti, visual_signatures), con immagini di riferimento per modelli generativi e per stampa 3D. La repo `vis…",
   "path": "skills/visual/SKILL.md",
   "bytes": 13902,
   "lines": 239,
   "tokens_est": 3476,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/visual/SKILL.md"
  },
  {
   "role": "illustratore",
   "trigger": "caricamento immagini HD per stampa nei 3 contesti (scene, intro volume, catalogo)",
   "scope_write": "subdir _hd/ via branch dedicata claude/hd-* + PR (mai merge in autonomia)",
   "commands": "—",
   "order": 50,
   "preview": "Per **istanze IA** o **collaboratori umani** che si connettono alla repo `isola_i3v_visual` per **caricare immagini HD** (illustrazioni di scena, ritratti, intro volume) generate via Grok Imagine o altro tool.  Versione: 1.1 — 2026-06-10 (…",
   "path": "skills/illustratore/SKILL.md",
   "bytes": 14349,
   "lines": 310,
   "tokens_est": 3587,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/illustratore/SKILL.md"
  },
  {
   "role": "atlantista",
   "trigger": "produrre le tavole-atlante full-page (prompt Manus + selezione + ingest) per le pagine abitanti/luoghi dei volumi",
   "scope_write": "visual/atlante/ (tavole, prompt; spec SOLO via ingest_tavola.py) — branch claude/atlante-*",
   "commands": "python3 scripts/ingest_tavola.py <manifest> · pytest tests/test_atlante.py",
   "order": 55,
   "preview": "Ramificazione della skill **illustratore** (`skills/illustratore/SKILL.md`). Per istanze IA o collaboratori che producono le **tavole-atlante**: pagine full-page in cui il soggetto vive nel suo posto sull'isola (Fiamma al Forno, Grunto al …",
   "path": "skills/atlantista/SKILL.md",
   "bytes": 7082,
   "lines": 152,
   "tokens_est": 1770,
   "mtime": "2026-06-12T12:49:33+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/atlantista/SKILL.md"
  },
  {
   "role": "scenografo",
   "trigger": "comporre prompt e generare le immagini di scena (una per subhook/pagina libro)",
   "scope_write": "consegna file via skill illustratore (branch claude/hd-*)",
   "commands": "—",
   "order": 60,
   "preview": "Per **istanze IA** (es. Manus) o **collaboratori** che si connettono alla repo `isola_i3v_visual` per **generare le illustrazioni di scena** del libro: una immagine per ogni subhook (pagina libro fisica) delle storie.  Versione: 1.1 — 2026…",
   "path": "skills/scenografo/SKILL.md",
   "bytes": 12390,
   "lines": 158,
   "tokens_est": 3098,
   "mtime": "2026-06-12T17:42:59+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/scenografo/SKILL.md"
  },
  {
   "role": "cartografo",
   "trigger": "manutenzione/estensione della cartografia tecnica (geojson, viewer, convenzioni)",
   "scope_write": "cartografia/, scripts/ (tool condivisi)",
   "commands": "—",
   "order": 70,
   "preview": "**Scope:** manutenzione, estensione e validazione della cartografia tecnica dell'Isola.",
   "path": "skills/cartografo/SKILL.md",
   "bytes": 10151,
   "lines": 223,
   "tokens_est": 2538,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/cartografo/SKILL.md"
  },
  {
   "role": "contributore",
   "trigger": "collaboratore esterno che propone aggiunte/dettagli alle schede (senza permessi di modifica diretta)",
   "scope_write": "contributi/ — SOLO file nuovi datati, mai modificare esistenti",
   "commands": "—",
   "order": 80,
   "preview": "✅ **Leggere tutto** il repo (visual, cartografia, pipeline_narrativa, catalogo_web).",
   "path": "skills/contributore/SKILL.md",
   "bytes": 2652,
   "lines": 79,
   "tokens_est": 663,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/contributore/SKILL.md"
  },
  {
   "role": "manutentore",
   "trigger": "lavoro SULLA repo — refactoring, ottimizzazioni, riordini, integrazione di pacchetti/branch, governance (non un ruolo operativo della pipeline)",
   "scope_write": "trasversale ma dichiarato per intervento (perimetro scritto prima di toccare); branch claude/<scope>; MAI pipeline_narrativa/, MAI merge in autonomia",
   "commands": "make sync · make check · make routing",
   "order": 90,
   "preview": "Per chi lavora **sulla** repo invece che **dentro** un ruolo: riordini, ottimizzazioni, refactoring, integrazione pacchetti. Le regole vivono nel `CLAUDE.md` (router) e **non si duplicano qui**: questa skill codifica il PROCESSO. Versione:…",
   "path": "skills/manutentore/SKILL.md",
   "bytes": 4486,
   "lines": 83,
   "tokens_est": 1122,
   "mtime": "2026-06-12T13:03:53+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/manutentore/SKILL.md"
  }
 ],
 "pipeline": [
  {
   "n": 0,
   "title": "IDEA AUTORIALE (Ray, chat dedicata lunga)",
   "input": "testa di Ray + Bible + grafo + ARCHI",
   "output": "conversazione con i fatti della storia",
   "auto": "0% (umano puro, by design)"
  },
  {
   "n": 1,
   "title": "NARRAZIONE FATTUALE",
   "input": "conversazione tappa 0",
   "output": "pipeline_narrativa/narrazione_fattuale/sNN_*.md",
   "auto": "20% (Ray scrive; agente può fare review strutturale)"
  },
  {
   "n": 2,
   "title": "ESTRAZIONE 10 HOOK VISIVI",
   "input": "narrazione_fattuale/sNN_*.md",
   "output": "proposta 10 hook in markdown",
   "auto": "80% (agente con prompt stretto)",
   "prompt": "pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE"
  },
  {
   "n": 3,
   "title": "REVIEW HOOK (Ray)",
   "input": "proposta tappa 2",
   "output": "OK / edit",
   "auto": "0% (umano, decisioni autoriali)"
  },
  {
   "n": 4,
   "title": "SCRITTURA NEL GRAFO",
   "input": "hook approvati",
   "output": "pipeline_narrativa/story_graph.json aggiornato",
   "auto": "100% (agente: edit + bump graph_version + last_updated)"
  },
  {
   "n": 5,
   "title": "AUDIT GRAFO",
   "input": "grafo modificato",
   "output": "PASS / FAIL",
   "auto": "100% (4 script Python — implementati, `make audit`)"
  },
  {
   "n": 6,
   "title": "SCRITTURA PROSA LIBRO (voce autoriale)",
   "input": "narrazione fattuale + 10 hook canonici",
   "output": "libro/sNN_<titolo>.md (testo prosa per illustrazione)",
   "auto": "60% (agente con prompt stretto + review Ray)",
   "prompt": "pipeline_narrativa/prompts/PROMPT_AGENTE_PROSA (DA SCRIVERE)"
  },
  {
   "n": 7,
   "title": "REVIEW PROSA + COMMIT",
   "input": "testo proposto",
   "output": "commit + push su main",
   "auto": "20% (review Ray umano, commit/push automatico)"
  }
 ],
 "repo_map": {
  "tree": "isola_i3v_visual/\n│\n├── pipeline_narrativa/        ⚠️ READ-ONLY (canone narrativo)\n│   ├── story_graph.json              v1.2.0 schema 1.4 (post-cornice-del-mondo: world_conventions root + cornice_dettagli + path_details)\n│   ├── story_graph.v0.10.0.backup.json  backup pre-migrazione fase E\n│   ├── story_graph.json.pre_v1_3.backup.json  backup pre-bump schema 1.2->1.3\n│   ├── story_graph.json.pre_fase_g.backup.json  backup pre-hook estesi\n│   ├── story_graph.json.pre_cornice_mondo.backup.json  backup pre-Step 1+2 (2026-04-30)\n│   ├── story_graph.json.pre_step4_cornici.backup.json  backup pre-Step 4 (2026-04-30)\n│   ├── story_graph.json.pre_step5_sentieri.backup.json backup pre-Step 5 (2026-04-30)\n│   ├── story_graph.json.pre_step6_path_details.backup.json backup pre-Step 6 (2026-04-30)\n│   ├── story_graph.json.pre_step8_canonical_refs.backup.json backup pre-Step 8 (2026-06-10)\n│   ├── hooks_proposals/<ciclo>/sNN.yaml  input deterministici per write_hooks_to_graph.py\n│   ├── narrazione_fattuale/sNN_*.md  12/12 file narrazione fattuale derivati dal sorgente _source/\n│   ├── writing_briefs/sNN_writing_brief.md  12 brief autosufficienti per agente prosa (output zero-token brieffer)\n│   ├── writing_briefs/_reference/    s01_writing_brief_FINAL.md (reference Ray, validato)\n│   ├── storie_finali/sNN_<slug>.md   12 testi prosa DEFINITIVI con frontmatter YAML + marker @hook (narrativo, 1..10) + marker @subhook (pagina libro fisica, 1..book_pages_total) machine-readable, consumati da scripts/build_volume.py (compositore PDF KDP, attivo dal 2026-06-08; vedi storie_finali/README.md)\n│   ├── storie_finali/_annotations/   YAML autoriali Ray (sNN.yaml) — note di scena\n│   ├── storie_finali/_inventory/     inventari testuali derivati (audit/QA prosa)\n│   ├── storie_finali/_scene/sNN/     immagini-scena composte per pagina libro fisica (sNN_hMMx.jpg low-res, x ∈ {a,b,c,...}), referenziate dal marker @subhook ... @image. Subdir `_hd/sNN_hMMx_hd.jpg` per versione HD stampa (JPG q95 sRGB, ≥1824×2736 px, DPI metadata 300; vedi sezione 9). NON sono reference catalogo (quelle stanno in visual/<categoria>/<id>/immagini/)\n│   ├── storie_finali/_volumi/        cornice editoriale 4 volumi (3 storie/volume, 1:1 con cicli A/B/C/D): soglia, introduzioni_cicli, stato_zero_e_sigilli, presentazione_completa, presentazioni_parziali, porte, congedo + _elementi_fissi/ (riferimenti read-only) + v0N/_hd/v0N_intro_<slug>_hd.jpg per illustrazioni HD intro volume. Marker ## VOLUME N interni per compositore libro\n│   └── documenti_progetto/           Bible, Carta Voce, ARCHI, Glossario, EAR, Pattern AI da bandire\n│\n├── visual/                    ✅ scrittura su scheda.md per arricchimento (con cautela) + immagini canoniche + prompt_grok.md\n│   ├── personaggi/                   24 schede (3 fratelli, 5 primari, 5 secondari, 5 cuccioli, 6 collettivi inclusi pescatori_case_basse)\n│   │   │  ⚠️ NB: la Bible usa \"Abitanti maggiori\" per gli stessi 5 di `primari/` — stesso insieme, vocabolari diversi (narrativo vs filesystem)\n│   │   ├── individuali/{bambini,primari,secondari,cuccioli}/<id>/  scheda.md + prompt_grok.md (28 prompt grok pubblicati al 2026-04-30) + immagini/\n│   │   └── collettivi/{camminanti,mantenitori,coltivatori_del_cerchio,mercato_del_mezzogiorno,pastori,pescatori_case_basse}/scheda.md  con sezione `## Saluto del gruppo` (DOC_2)\n│   ├── luoghi/                       74 schede (per quartiere: aria/acqua/fuoco/terra/centro + perimetro + strade)\n│   │   └── 5 schede sentieri Tier A (via_dell_alba, sentiero_orti_torrente_foresta, via_che_sale, sentiero_orti_casa_salvia, viottolo_perimetrale_piazza) con `## Coerenza cross-scena` aggiornata con dettagli stabili da `path_details.paths.<id>` del grafo\n│   ├── oggetti/                      14 schede (13 oggetti-simbolo + 1 oggetto_di_scena_ricorrente) — tutte con prompt_grok.md\n│   ├── venti/                        3 schede (Taglio/Intreccio/Mulinello)\n│   └── visual_signatures/            1 scheda (quando_acqua_trema)\n│\n├── _visual_pipeline/          ✅ pacchetto operativo (canone, template, esempi, skill)\n│   ├── README.md                     entry point pipeline\n│   ├── _canone/                      3 doc canone saga (stylesheet, scale, palette)\n│   ├── _templates/                   5 template (scheda + prompt grok + descrizione social)\n│   ├── _skill/                       PIPELINE.md (flusso 6 fasi) + CHECKLIST.md\n│   └── _esempi/                      bartolo, fiamma, forno, grembiule_fiamma (validati)\n│\n├── cartografia/               ✅ scrittura tecnica\n│   ├── geo/island.geojson            104 feature, sistema cartesiano locale\n│   ├── geo/viewer/                   viewer Leaflet\n│   └── README.md                     architettura cartografica\n│\n├── catalogo_web/              ⚠️  legacy: solo `data/` (contratto JSON), UI archiviata 2026-06-10\n│   ├── data/entities.json            generato da `scripts/build_catalogo_web.py` (con blocco `meta` da WI-8)\n│   ├── data/storie.json              storie dashboard\n│   └── _archive/                     UI vanilla deprecata (catalogo v2 vive in `web/`)\n│\n├── web/                       ✅ catalogo v2 — app Next.js 15 (App Router, TS strict)\n│   ├── app/                          home workbench, /catalogo, /storie, /mappa, /orchestra, /stato, /strade\n│   ├── app/api/img/[...path]/        proxy immagini same-origin (WI-3, abilita download)\n│   ├── components/catalogo/          entity-body (deep link sezioni), prompt-grok-block (copy per vista), gallery, lightbox\n│   ├── components/command-palette.tsx  ⌘K navigazione veloce (WI-5)\n│   ├── lib/prompt-grok.ts            parser markdown prompt grok (WI-1) + test (13/13 pass)\n│   ├── scripts/build-search-index.mjs  indice cmd-K (build-time)\n│   └── scripts/dev-watch.mjs         modalita' live: `npm run dev:live` (WI-7)\n│\n├── _porting_grafo/            🗄️  ARCHIVIO una-tantum (fase E completata 2026-04-28)\n│   ├── dossier_fase_e/               kit migrazione + MIGRATION_PROMPT + schema v1.2 + INPUT_NODES (12 nodi v1.1)\n│   ├── output/s01..s12/              per ogni storia: canonical, provisional, migration_notes, catalog_proposals, _p1_mapping\n│   └── scripts/migrate_p1.py         script P1 (carpentiere meccanico)\n│\n├── _pacchetti_consegnati/     🗄️  ARCHIVIO pacchetti autoriali Ray gia integrati (2026-04-30)\n│   ├── README.md                     orchestratore + pattern di integrazione futura\n│   └── cornice_mondo/                pacchetto integrato 2026-04-30 (DOC_1..DOC_6 + README dedicato)\n│\n├── contributi/                ✅ scrittura per collaboratori esterni (proposte/aggiunte)\n│   └── (file .md datati, vedi sezione 5)\n│\n├── _starter_kit/              ✅ template di sistema riusabile (scheletro, NO contenuto saga)\n│   └── README.md                     entry point (setup nuova \"isola\" da zero)\n│\n├── scripts/                   ✅ tool Python condivisi (idempotenti)\n│   ├── build_catalogo_web.py            rigenera catalogo_web/data/entities.json da visual/\n│   ├── build_visual_skeleton.py         ricrea schede stub da grafo (non usare in fase F)\n│   ├── compile_visual_from_graph.py     travaso meccanico grafo → schede (fase F.1)\n│   ├── split_narrazione_fattuale.py     split sorgente Ciclo*.txt → 12 sNN_*.md\n│   ├── migrate_graph_v1_2_to_v1_3.py    bump schema fase G (one-shot, idempotente)\n│   ├── promote_visual_entities_to_graph.py  promozione catalogo visual → grafo entities\n│   ├── write_hooks_to_graph.py          writer deterministico fase G (input YAML hooks_proposals/)\n│   ├── build_writing_brief.py           ⭐ NEW (2026-04-30) generatore zero-token brief writing per agente prosa\n│   ├── build_volume.py                  ⭐ NEW (2026-06-08, v2) compositore libro stampa KDP (A5 300 DPI bleed) — output PDF in _output/\n│   ├── design_system.py                 ⭐ NEW (2026-06-08) identita visiva collana (palette tre venti + 6 quartieri, font, ornamenti, glifi, cornici, camuni)\n│   ├── cornice_mondo/                   ⭐ NEW (2026-04-30) pacchetto 7 step \"cornice del mondo\"\n│   │   ├── step1_world_conventions.py   crea nodo radice world_conventions + extends quote_tracker\n│   │   ├── step4_cornici.py             scrive 24 cornice_dettagli + 8 formule + 2 cantilene\n│   │   ├── step5_sentieri_fantasma.py   appende 36 sentieri a locations_secondary\n│   │   ├── step6_path_details.py        popola path_details.paths con 5 sentieri Tier A\n│   │   ├── step8_fix_canonical_refs.py  ⭐ NEW (2026-06-10) uniforma 7 ref ad id canonici (foresta, pontile, villaggio, who.refs)\n│   │   ├── _data/                       4 YAML deterministici (refrain, cornici_24, sentieri_fantasma, path_details_tierA)\n│   │   └── _audit/                      riservata audit successivi\n│   └── audit/                           ⭐ NEW (2026-06-09) audit grafo+prosa IMPLEMENTATI (4 script + runner + manifest backup + baseline known_issues). `python3 scripts/audit/run_all_audits.py`\n│\n├── assets/                    ⭐ NEW (2026-06-08) asset condivisi per build (font collana)\n│   └── fonts/                        7 TTF OFL: Fraunces, Nunito, Fredoka, Lora — usati da build_volume.py + design_system.py\n│\n├── tests/                     ⭐ NEW (2026-06-08) suite test impaginazione (60 test, ~4s)\n│   ├── test_build_volume.py          struttura/robustezza/decori/coerenza 4 volumi/determinismo\n│   ├── test_integration.py           build PDF reale + invarianti KDP (slow, ~60s)\n│   └── README.md                     come eseguire i test\n│\n├── pytest.ini                 ⭐ NEW (2026-06-08) config pytest (marker `slow` per integration)\n│\n├── skills/                    ✅ skill agente IA\n│   ├── README.md                     orchestratore\n│   ├── cartografo.md                 manutenzione cartografia\n│   ├── brieffer/                     genera writing_briefs autosufficienti (2026-04-30)\n│   │   └── SKILL.md\n│   ├── prosa/                        ⭐ NEW (2026-04-30) agente prosa: scrive il testo finale delle storie\n│   │   └── SKILL.md                  da incollare in chat Claude.ai per attivare modalita scrittura\n│   ├── illustratore/                 ⭐ NEW (2026-05-19) agente illustratore: workflow upload HD per stampa\n│   │   └── SKILL.md                  pattern branch + naming + commit per immagini HD pronte al merge\n│   └── visual/\n│       ├── README.md                 skill visual generale\n│       └── compilatore.md            sotto-skill compilazione schede\n│\n├── README.md                  panoramica generale\n├── PROJECT_STATE.md           snapshot operativo\n├── SYNC_LOG.md                log cambiamenti cross-skill\n└── CLAUDE.md                  questo file\n",
  "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/MAPPA_REPO.md",
  "mtime": "2026-06-12T12:05:54+00:00"
 },
 "documents": [
  {
   "path": ".pytest_cache/README.md",
   "bytes": 302,
   "lines": 9,
   "tokens_est": 76,
   "mtime": "2026-06-08T07:45:57.333629+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/.pytest_cache/README.md",
   "category": "operativo",
   "preview": "This directory contains data from the pytest's cache plugin, which provides the `--lf` and `--ff` options, as well as the `cache` fixture."
  },
  {
   "path": "CLAUDE.md",
   "bytes": 12194,
   "lines": 128,
   "tokens_est": 3048,
   "mtime": "2026-06-12T13:03:53+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/CLAUDE.md",
   "category": "core",
   "preview": "**Versione: 3.0 — 2026-06-12** · costruito su HEAD `7dadd00` (post standard-scene v1.1) (riordino router/skills: questo file contiene solo regole stabili e instradamento. Lo stato vive in `PROJECT_STATE.md`, la storia in `docs/fasi/`. Chan…"
  },
  {
   "path": "Makefile",
   "bytes": 1958,
   "lines": 59,
   "tokens_est": 490,
   "mtime": "2026-06-13T08:25:42+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/Makefile",
   "category": "core",
   "preview": ""
  },
  {
   "path": "PIPELINE_OVERVIEW.md",
   "bytes": 16076,
   "lines": 257,
   "tokens_est": 4019,
   "mtime": "2026-05-06T20:50:37+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/PIPELINE_OVERVIEW.md",
   "category": "operativo",
   "preview": "Snapshot operativo del processo end-to-end \"idea → libro illustrato\" come lo abbiamo costruito su questa repo. Non sostituisce `CLAUDE.md` / `docs/PIPELINE.md` / `PROJECT_STATE.md` — è una **lettura compatta** per guardare il sistema da fu…"
  },
  {
   "path": "PROJECT_STATE.md",
   "bytes": 5986,
   "lines": 95,
   "tokens_est": 1496,
   "mtime": "2026-06-12T12:49:33+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/PROJECT_STATE.md",
   "category": "core",
   "preview": "**Questo file è uno snapshot, non un diario.** Contiene: stato corrente + ultima sessione. Quando inizi una nuova sessione significativa, la sessione qui sotto scivola in `docs/fasi/SESSIONI_ARCHIVIO.md` (in testa) e questo file si riscriv…"
  },
  {
   "path": "README.md",
   "bytes": 7124,
   "lines": 141,
   "tokens_est": 1781,
   "mtime": "2026-05-07T12:33:28+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/README.md",
   "category": "operativo",
   "preview": "Saga di **12 storie illustrate per bambini 4-10**, autore: **Ray**."
  },
  {
   "path": "SYNC_LOG.md",
   "bytes": 51906,
   "lines": 494,
   "tokens_est": 12976,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/SYNC_LOG.md",
   "category": "core",
   "preview": "Questo file traccia ogni modifica fatta in `isola_i3v_visual` che **impatta o potrebbe impattare altre repo del sistema** (archivio storico `isola_tre_venti_github`, future repo prompt, sito esterno, pipeline immagini, ecc.). Ray (o un age…"
  },
  {
   "path": "_output/vol1_pres-dopo_s01_LAYOUT_WARNINGS.md",
   "bytes": 3464,
   "lines": 106,
   "tokens_est": 866,
   "mtime": "2026-06-14T11:16:33.213447+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_output/vol1_pres-dopo_s01_LAYOUT_WARNINGS.md",
   "category": "operativo",
   "preview": "_Generato da `build_volume.py`. Non modificare._"
  },
  {
   "path": "_output/vol1_pres-dopo_s03_LAYOUT_WARNINGS.md",
   "bytes": 3321,
   "lines": 105,
   "tokens_est": 830,
   "mtime": "2026-06-13T20:29:11.737426+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_output/vol1_pres-dopo_s03_LAYOUT_WARNINGS.md",
   "category": "operativo",
   "preview": "_Generato da `build_volume.py`. Non modificare._"
  },
  {
   "path": "_pacchetti_consegnati/README.md",
   "bytes": 2351,
   "lines": 44,
   "tokens_est": 588,
   "mtime": "2026-05-05T20:18:56+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/README.md",
   "category": "archivio",
   "preview": "**Cosa è.** Archivio dei pacchetti operativi consegnati da Ray e già integrati nel canone (grafo, schede, script). I documenti qui dentro sono **fonte autorevole delle decisioni autoriali** e servono come trail di audit + reference per pac…"
  },
  {
   "path": "_pacchetti_consegnati/cornice_mondo/DOC_1_formula_ritornello.md",
   "bytes": 7716,
   "lines": 144,
   "tokens_est": 1929,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/cornice_mondo/DOC_1_formula_ritornello.md",
   "category": "archivio",
   "preview": "**Scopo.** Definire il ritornello con cui i tre fratelli e il narratore identificano l'individuo anonimo di un gruppo-istituzione ogni volta che ne incontrano uno. È un evento ricorrente, riconoscibile a ogni storia, che il bambino impara …"
  },
  {
   "path": "_pacchetti_consegnati/cornice_mondo/DOC_2_saluti_gruppi.md",
   "bytes": 8352,
   "lines": 122,
   "tokens_est": 2088,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/cornice_mondo/DOC_2_saluti_gruppi.md",
   "category": "archivio",
   "preview": "**Scopo.** Definire un gesto/suono di saluto specifico per ciascuno dei 5 gruppi-istituzione. Il saluto è un fatto del mondo che non viene mai spiegato, ma compare nelle storie come comportamento naturale del gruppo. Funziona come marcator…"
  },
  {
   "path": "_pacchetti_consegnati/cornice_mondo/DOC_3_cornici_processi.md",
   "bytes": 26065,
   "lines": 361,
   "tokens_est": 6516,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/cornice_mondo/DOC_3_cornici_processi.md",
   "category": "archivio",
   "preview": "**Scopo.** Definire 2 cornici (= micro-apparizioni di sfondo, mai-trama) per ciascuna delle 12 storie, pensate per intrecciarsi in 5 processi che fanno girare l'isola. Quando il lettore le vede tutte insieme attraverso la saga, percepisce …"
  },
  {
   "path": "_pacchetti_consegnati/cornice_mondo/DOC_4_audit_sentieri.md",
   "bytes": 15963,
   "lines": 306,
   "tokens_est": 3991,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/cornice_mondo/DOC_4_audit_sentieri.md",
   "category": "archivio",
   "preview": "**Scopo.** Mappare i sentieri/strade effettivamente percorsi dai tre fratelli nelle 12 storie, confrontandoli con quelli dichiarati nel grafo e con quelli esistenti nel catalogo schede. Identificare i sentieri prioritari da dettagliare e s…"
  },
  {
   "path": "_pacchetti_consegnati/cornice_mondo/DOC_5_index_sentieri.md",
   "bytes": 11331,
   "lines": 235,
   "tokens_est": 2833,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/cornice_mondo/DOC_5_index_sentieri.md",
   "category": "archivio",
   "preview": "**Scopo.** Indice bidirezionale `storia ↔ sentiero` pensato per il brieffer (lo script che monta il writing_brief per l'agente prosa). Per ogni sentiero, le storie in cui appare già marcate; per ogni storia, i sentieri attraversati. I micr…"
  },
  {
   "path": "_pacchetti_consegnati/cornice_mondo/DOC_6_mercato_idee_tierA.md",
   "bytes": 13026,
   "lines": 162,
   "tokens_est": 3256,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/cornice_mondo/DOC_6_mercato_idee_tierA.md",
   "category": "archivio",
   "preview": "**Scopo.** Per ognuno dei 5 sentieri Tier A, propongo un dettaglio per ogni appariazione (storia). Sono **proposte**: tu approvi, scarti, modifichi. Le tue scelte diventano gli slot canonici del catalogo.  **Pattern di lavoro.** Ogni detta…"
  },
  {
   "path": "_pacchetti_consegnati/cornice_mondo/README.md",
   "bytes": 5772,
   "lines": 101,
   "tokens_est": 1443,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/cornice_mondo/README.md",
   "category": "archivio",
   "preview": "**Cosa contiene.** 6 documenti DOC_1..DOC_6 con le decisioni autoriali Ray sulla \"cornice del mondo\" della saga: formula ritornello, saluti dei gruppi, cornici di sfondo distribuite nelle 12 storie, audit sentieri, index sentieri, dettagli…"
  },
  {
   "path": "_pacchetti_consegnati/mappa_isola_v1/INTEGRATION.md",
   "bytes": 12717,
   "lines": 318,
   "tokens_est": 3179,
   "mtime": "2026-05-05T20:18:56+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/mappa_isola_v1/INTEGRATION.md",
   "category": "archivio",
   "preview": "**Data:** 2026-05-05 **Autore:** Claude (chat Ray) **Branch suggerito:** `claude/mappa-isola-v1` **Target deploy:** Vercel"
  },
  {
   "path": "_pacchetti_consegnati/mappa_isola_v1/README.md",
   "bytes": 4260,
   "lines": 75,
   "tokens_est": 1065,
   "mtime": "2026-05-05T20:18:56+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_pacchetti_consegnati/mappa_isola_v1/README.md",
   "category": "archivio",
   "preview": "Archivio del pacchetto consegnato da Ray come `pacchetto_mappa_isola_v1.zip` + `INTEGRATION.md` (caricati su main 2026-05-05)."
  },
  {
   "path": "_starter_kit/README.md",
   "bytes": 2350,
   "lines": 46,
   "tokens_est": 588,
   "mtime": "2026-05-07T12:40:26+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_starter_kit/README.md",
   "category": "operativo",
   "preview": "Scheletro **agnostico** per costruire una pipeline narrativa automatizzata \"racconto umano → libro illustrato\". Adatto a racconti brevi, romanzi lunghi, serie e saghe di qualsiasi lunghezza."
  },
  {
   "path": "_visual_pipeline/README.md",
   "bytes": 10957,
   "lines": 214,
   "tokens_est": 2739,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/README.md",
   "category": "operativo",
   "preview": "**Scopo:** completare le 115 schede `visual/` della saga **L'Isola dei Tre Venti** con canone chiuso e immagini canoniche generate, in modo coerente, scalabile e riproducibile."
  },
  {
   "path": "_visual_pipeline/_api/README.md",
   "bytes": 8663,
   "lines": 233,
   "tokens_est": 2166,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/_api/README.md",
   "category": "operativo",
   "preview": "**Per chi:** la persona che si occupa di generare le immagini con Flux/OpenAI sul proprio PC. **Coordinamento:** Ray (autore + push su main)."
  },
  {
   "path": "_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md",
   "bytes": 5042,
   "lines": 101,
   "tokens_est": 1260,
   "mtime": "2026-06-12T08:02:48+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md",
   "category": "operativo",
   "preview": "**Stato:** validato 2026-04-29 con generazione canonica di Fiamma (4 immagini di riferimento). Lo stile è fissato."
  },
  {
   "path": "_visual_pipeline/_canone/02_SAGA_SCALE_v1.md",
   "bytes": 6244,
   "lines": 116,
   "tokens_est": 1561,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/_canone/02_SAGA_SCALE_v1.md",
   "category": "operativo",
   "preview": "**Stato:** v1.0 fissata 2026-04-29. Aggiornabile man mano che si fissano nuovi personaggi."
  },
  {
   "path": "_visual_pipeline/_canone/03_SAGA_PALETTE_v1.md",
   "bytes": 6885,
   "lines": 165,
   "tokens_est": 1721,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/_canone/03_SAGA_PALETTE_v1.md",
   "category": "operativo",
   "preview": "**Stato:** v1.0 derivata da Bible §6 PALETTE VISIVA + immagini canoniche atlante mondo."
  },
  {
   "path": "_visual_pipeline/_skill/CHECKLIST.md",
   "bytes": 7217,
   "lines": 175,
   "tokens_est": 1804,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/_skill/CHECKLIST.md",
   "category": "operativo",
   "preview": "**Scopo:** lista di controllo per Claude da seguire passo-passo durante il completamento di una scheda. Da spuntare mentalmente o esplicitamente."
  },
  {
   "path": "_visual_pipeline/_skill/PIPELINE.md",
   "bytes": 15739,
   "lines": 327,
   "tokens_est": 3935,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/_skill/PIPELINE.md",
   "category": "operativo",
   "preview": "**Versione:** 1.2 **Data:** 2026-04-29 **Stato:** ✅ **PIPELINE PERSONAGGI VALIDATA** su 2 specie diversissime (Fiamma + Bartolo). ✅ **PIPELINE LUOGHI VALIDATA** su luogo complesso con esterno + interno + cortile (Forno di Fiamma). 🚀 Pronti…"
  },
  {
   "path": "assets/fonts/README.md",
   "bytes": 1130,
   "lines": 22,
   "tokens_est": 282,
   "mtime": "2026-06-08T07:47:32+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/assets/fonts/README.md",
   "category": "operativo",
   "preview": "Font usati dallo script `scripts/build_volume.py` + `scripts/design_system.py`. Tutti distribuiti sotto **SIL Open Font License 1.1** (OFL) — uso commerciale e ridistribuzione consentiti, copyright presso gli autori originali."
  },
  {
   "path": "cartografia/CHANGELOG.md",
   "bytes": 16856,
   "lines": 289,
   "tokens_est": 4214,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/cartografia/CHANGELOG.md",
   "category": "operativo",
   "preview": "Tutte le modifiche significative al canone cartografico vanno registrate qui, in ordine cronologico inverso (più recente in alto)."
  },
  {
   "path": "cartografia/README.md",
   "bytes": 8380,
   "lines": 157,
   "tokens_est": 2095,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/cartografia/README.md",
   "category": "operativo",
   "preview": "**Versione:** 0.1 (bootstrap) **Data inizio:** 2026-04-24 **Maintainer:** Ray + Claude (Agente Cartografo)"
  },
  {
   "path": "cartografia/assets_mappa/README.md",
   "bytes": 4812,
   "lines": 112,
   "tokens_est": 1203,
   "mtime": "2026-05-05T20:18:56+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/cartografia/assets_mappa/README.md",
   "category": "operativo",
   "preview": "Asset visivi della **Mappa dell'Isola** (vista navigabile in `catalogo_web/`, route `#/mappa-isola`)."
  },
  {
   "path": "cartografia/convenzioni/convenzioni_id.md",
   "bytes": 5002,
   "lines": 146,
   "tokens_est": 1250,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/cartografia/convenzioni/convenzioni_id.md",
   "category": "operativo",
   "preview": "**Versione:** 0.1 **Data:** 2026-04-24"
  },
  {
   "path": "cartografia/convenzioni/orientamenti_venti.md",
   "bytes": 5021,
   "lines": 99,
   "tokens_est": 1255,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/cartografia/convenzioni/orientamenti_venti.md",
   "category": "operativo",
   "preview": "**Versione:** 0.1 **Data:** 2026-04-24 **Fonte canonica primaria:** Bible §3 (venti), apparato P.02, P.04-P.07."
  },
  {
   "path": "cartografia/convenzioni/scala_e_proporzioni.md",
   "bytes": 5272,
   "lines": 121,
   "tokens_est": 1318,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/cartografia/convenzioni/scala_e_proporzioni.md",
   "category": "operativo",
   "preview": "**Versione:** 0.1 **Data:** 2026-04-24 **Fonte canonica primaria:** Bible §2 (geografia frattale)."
  },
  {
   "path": "cartografia/convenzioni/sistema_coordinate.md",
   "bytes": 5955,
   "lines": 119,
   "tokens_est": 1489,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/cartografia/convenzioni/sistema_coordinate.md",
   "category": "operativo",
   "preview": "**Versione:** 0.1 **Data:** 2026-04-24"
  },
  {
   "path": "cartografia/luoghi/_template_scheda.md",
   "bytes": 5559,
   "lines": 166,
   "tokens_est": 1390,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/cartografia/luoghi/_template_scheda.md",
   "category": "operativo",
   "preview": "<!-- ISTRUZIONI USO TEMPLATE: - Duplicare questo file in luoghi/<quartiere>/<id>.md - Sostituire tutti i placeholder [...] con i valori reali o con OMESSO se non applicabile - Sezioni non applicabili: ELIMINARE completamente (non lasciare …"
  },
  {
   "path": "dashboard/README.md",
   "bytes": 2703,
   "lines": 56,
   "tokens_est": 676,
   "mtime": "2026-06-13T08:25:42+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/dashboard/README.md",
   "category": "operativo",
   "preview": "Vista **meta** della repo: regole, ruoli, stato e debito del sistema che produce la saga — non il contenuto della saga."
  },
  {
   "path": "docs/BLINDATURA_2026-06-09.md",
   "bytes": 9158,
   "lines": 121,
   "tokens_est": 2290,
   "mtime": "2026-06-10T08:06:07+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/BLINDATURA_2026-06-09.md",
   "category": "operativo",
   "preview": "**Scope:** migliorare, ottimizzare e blindare la repo `isola_i3v_visual`. **Vincolo rispettato:** `pipeline_narrativa/` non toccata (read-only, CLAUDE.md §2). Le incoerenze trovate nel grafo sono SEGNALATE qui e nella baseline, non corrett…"
  },
  {
   "path": "docs/CANONE_NORMATIVO.md",
   "bytes": 2817,
   "lines": 58,
   "tokens_est": 704,
   "mtime": "2026-06-11T18:45:12+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/CANONE_NORMATIVO.md",
   "category": "operativo",
   "preview": "**Introdotto:** branch `claude/canone-machine-readable` (2026-06-10)"
  },
  {
   "path": "docs/MAPPA_REPO.md",
   "bytes": 11872,
   "lines": 135,
   "tokens_est": 2968,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/MAPPA_REPO.md",
   "category": "operativo",
   "preview": "Estratta dal CLAUDE.md v2.x nel riordino router (2026-06-12) e mantenuta qui come riferimento di navigazione. Aggiornarla quando la **struttura** cambia (nuove directory, nuovi script), non per i contatori di stato (quelli vivono in `PROJE…"
  },
  {
   "path": "docs/PIPELINE.md",
   "bytes": 13084,
   "lines": 162,
   "tokens_est": 3271,
   "mtime": "2026-06-10T08:06:07+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/PIPELINE.md",
   "category": "operativo",
   "preview": "Questo documento descrive il **flusso operativo** dall'idea autoriale di Ray fino al testo libro committato. Vale per ogni storia s01..s12 (e per future espansioni)."
  },
  {
   "path": "docs/SPEC_CATALOGO_V2.md",
   "bytes": 9853,
   "lines": 114,
   "tokens_est": 2463,
   "mtime": "2026-06-10T09:37:34+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/SPEC_CATALOGO_V2.md",
   "category": "operativo",
   "preview": "**Data:** 2026-06-10 · **Autore spec:** Claude (chat) su richiesta Ray · **Esecutore previsto:** Claude Code **Repo:** `isola_i3v_visual` · **Prerequisito:** branch blindatura mergiata (audit + CI attivi)"
  },
  {
   "path": "docs/TODO_BRIEFFER_CACHE_AB.md",
   "bytes": 2149,
   "lines": 44,
   "tokens_est": 537,
   "mtime": "2026-06-12T12:49:33+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/TODO_BRIEFFER_CACHE_AB.md",
   "category": "operativo",
   "preview": "**Stato:** debito tecnico aperto · registrato 2026-06-12 · priorità: prima del seeding \"Rocco e Idvara\" (il template eredita il pattern)"
  },
  {
   "path": "docs/TODO_BUILD_VOLUME_SPREAD_H07A.md",
   "bytes": 4022,
   "lines": 71,
   "tokens_est": 1006,
   "mtime": "2026-06-14T11:15:39.957018+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/TODO_BUILD_VOLUME_SPREAD_H07A.md",
   "category": "operativo",
   "preview": "**Stato:** in attesa — sessione dedicata Ray + Claude · registrato 2026-06-14 · branch `claude/illustratore-s01-hd-refresh`"
  },
  {
   "path": "docs/fasi/FASI_COMPLETATE.md",
   "bytes": 25664,
   "lines": 291,
   "tokens_est": 6416,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/fasi/FASI_COMPLETATE.md",
   "category": "archivio",
   "preview": "**Archivio storico.** Questo file conserva, senza modifiche, le sezioni cronologiche del CLAUDE.md pre-riordino (v2.x, ultima revisione 2026-06-10 notte tarda). Il CLAUDE.md attuale è un router: regole stabili + tabella di instradamento. L…"
  },
  {
   "path": "docs/fasi/SESSIONI_ARCHIVIO.md",
   "bytes": 39464,
   "lines": 620,
   "tokens_est": 9866,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/fasi/SESSIONI_ARCHIVIO.md",
   "category": "archivio",
   "preview": "**Archivio storico.** PROJECT_STATE.md è uno **snapshot**: contiene solo lo stato corrente e l'ultima sessione. Tutte le sessioni precedenti vivono qui, integrali, in ordine inverso. Quando una sessione esce dallo snapshot, si **appende qu…"
  },
  {
   "path": "pipeline_narrativa/apparato_v0_2_disclaimer/ISOLA_APPARATO_PUBBLICO.md",
   "bytes": 35093,
   "lines": 1,
   "tokens_est": 8773,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/apparato_v0_2_disclaimer/ISOLA_APPARATO_PUBBLICO.md",
   "category": "operativo",
   "preview": "\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000…"
  },
  {
   "path": "pipeline_narrativa/apparato_v0_2_disclaimer/ISOLA_APPARATO_TECNICO.md",
   "bytes": 69049,
   "lines": 1,
   "tokens_est": 17262,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/apparato_v0_2_disclaimer/ISOLA_APPARATO_TECNICO.md",
   "category": "operativo",
   "preview": "\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000…"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/APPENDIX_STYLISTIC_DERIVATION_v1.md",
   "bytes": 18170,
   "lines": 665,
   "tokens_est": 4542,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/APPENDIX_STYLISTIC_DERIVATION_v1.md",
   "category": "progetto",
   "preview": "**Version:** 1.0 **Date:** 2026-01-18 **Status:** Appendix to EAR-PERSONAGGI v2.0 **Author:** EAR Lab **Requires:** EAR-PERSONAGGI_v2.0, KERNEL_EAR_v1.md"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/ARCHI_12_STORIE_v1_1.md",
   "bytes": 113281,
   "lines": 1182,
   "tokens_est": 28320,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/ARCHI_12_STORIE_v1_1.md",
   "category": "progetto",
   "preview": "**Versione:** 1.0 **Data:** 2026-04-21 **Status:** Output Fase B2 — mappa archi narrativi delle 12 storie **Autore:** EAR Lab + Claude (Fase B2) **Si parla con:** `PROGETTO_INDICE_v1_3.md`, `ISOLA_TRE_VENTI_BIBLE_v2.md`, `CARTA_VOCE_v1_2.m…"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/CARTA_VOCE_v1_2.md",
   "bytes": 30949,
   "lines": 508,
   "tokens_est": 7737,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/CARTA_VOCE_v1_2.md",
   "category": "progetto",
   "preview": "**Versione:** 1.2 **Data:** 2026-04-21 **Stato:** Documento operativo, aggiornato post Fase A3 **Riusabile:** Sì (template per saghe future con adattamenti) **Si parla con:** `VOCE_AUTORE_ESTRATTA_v1_1.md`, `PATTERN_AI_DA_BANDIRE_v1.md`, `…"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/EAR_KERNEL_AILA_v1_0.md",
   "bytes": 11161,
   "lines": 534,
   "tokens_est": 2790,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/EAR_KERNEL_AILA_v1_0.md",
   "category": "progetto",
   "preview": "**Version:** 1.0 **Date:** 2026-01-17 **Status:** Official Specification **Author:** EAR Lab **Requires:** AILA_LINGUA_v1.0.md"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/GLOSSARIO_ISOLA.md",
   "bytes": 17963,
   "lines": 357,
   "tokens_est": 4491,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/GLOSSARIO_ISOLA.md",
   "category": "progetto",
   "preview": "**Versione:** 1.0 **Data:** 2026-04-21 **Status:** Documento operativo Fase A3 **Funzione:** Catalogo di tutti i nomi propri dell'isola (luoghi, abitanti, gruppi, oggetti, momenti rituali, modi di dire). Da consultare in scrittura per coer…"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md",
   "bytes": 47211,
   "lines": 762,
   "tokens_est": 11803,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md",
   "category": "progetto",
   "preview": "**Versione:** 2.0 **Data:** 2026-04-21 **Status:** Official Universe Specification — estesa con Fase A3 **Autore:** EAR Lab + Claude (Fase A3) **Target:** Bambini 4-6 anni (leggibili fino a 10 come iniziazione mascherata) **Si parla con:**…"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/METODO_REVISIONE_B3_v1_1.md",
   "bytes": 20399,
   "lines": 307,
   "tokens_est": 5100,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/METODO_REVISIONE_B3_v1_1.md",
   "category": "progetto",
   "preview": "**Versione:** 1.1 **Data:** 2026-04-22 **Status:** Metodo operativo cristallizzato durante Fase B3 (S4-S5), aggiornato post-B3.0.5 e dopo riflessione sul carico cognitivo. **Si parla con:** `PROGETTO_INDICE_v1_5.md`, `story_graph_v0_3_0.js…"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/MITI_FONDATORI_BREVI_v1.md",
   "bytes": 6738,
   "lines": 415,
   "tokens_est": 1684,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/MITI_FONDATORI_BREVI_v1.md",
   "category": "progetto",
   "preview": "**Versione:** 1.0 — Breve **Target:** 4-5 anni, una storia per sera **Lunghezza:** ~500-600 parole per mito **Note:** Versione semplificata con frasi corte, ripetizioni ritmiche, suoni da fare insieme."
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md",
   "bytes": 20583,
   "lines": 441,
   "tokens_est": 5146,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md",
   "category": "progetto",
   "preview": "**Versione:** 1.0 **Data:** 2026-04-21 **Stato:** Documento operativo Fase A2 **Autore:** Autodiagnosi Claude + validazione Ray **Si parla con:** CARTA_VOCE_v1.md, APPENDIX_STYLISTIC_DERIVATION_v1 **Riusabile:** Sì (lista universale per ge…"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/PROGETTO_INDICE_v1_5.md",
   "bytes": 26370,
   "lines": 339,
   "tokens_est": 6592,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/PROGETTO_INDICE_v1_5.md",
   "category": "progetto",
   "preview": "**Versione:** 1.5 **Data:** 2026-04-22 **Stato:** Documento master di navigazione e roadmap della saga **Funzione:** Visione d'insieme del progetto, fasi completate/in corso/pianificate, elenco dei file canonici con numero di versione, dec…"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/RIFERIMENTI_OPERATIVI.md",
   "bytes": 14562,
   "lines": 274,
   "tokens_est": 3640,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/RIFERIMENTI_OPERATIVI.md",
   "category": "progetto",
   "preview": "**Versione:** 1.0 **Data:** 2026-04-21 **Status:** Documento operativo Fase A3 **Funzione:** Scheda secca di consultazione veloce in scrittura (Fase D). Per ogni personaggio: specie, residenza precisa, abitudini fisse, oggetto-simbolo o fi…"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/STORIE_SCHEMA_v1_1.md",
   "bytes": 25868,
   "lines": 667,
   "tokens_est": 6467,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/STORIE_SCHEMA_v1_1.md",
   "category": "progetto",
   "preview": "**Version:** 1.1 **Date:** 2026-01-19 **Status:** Story Bible **Requires:** ISOLA_TRE_VENTI_BIBLE_v1.1.md **Changelog:** v1.1 — Modificata Storia 6, modificata Storia 7, aggiunta appendice illustrazioni Blocco A"
  },
  {
   "path": "pipeline_narrativa/documenti_progetto/VOCE_AUTORE_ESTRATTA_v1_1.md",
   "bytes": 26019,
   "lines": 356,
   "tokens_est": 6505,
   "mtime": "2026-05-04T09:10:41+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/VOCE_AUTORE_ESTRATTA_v1_1.md",
   "category": "progetto",
   "preview": "**Versione:** 1.1 **Data:** 2026-04-21 **Stato:** Documento operativo, aggiornato post Fase A3 **Funzione:** Descrivere la voce di Ray come autore — 16 tratti stilistici ricorrenti, estratti dal corpus italiano adulto e raffinati per la sc…"
  },
  {
   "path": "saga_config.yaml",
   "bytes": 4534,
   "lines": 136,
   "tokens_est": 1134,
   "mtime": "2026-06-11T18:45:12+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/saga_config.yaml",
   "category": "core",
   "preview": ""
  },
  {
   "path": "scripts/README.md",
   "bytes": 1242,
   "lines": 26,
   "tokens_est": 310,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/scripts/README.md",
   "category": "operativo",
   "preview": "Tool Python condivisi tra le skill `cartografo` e `visual`. Idempotenti: rieseguibili senza effetti collaterali su lavoro esistente."
  },
  {
   "path": "scripts/audit/README.md",
   "bytes": 4131,
   "lines": 69,
   "tokens_est": 1033,
   "mtime": "2026-06-11T18:46:28+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/scripts/audit/README.md",
   "category": "operativo",
   "preview": "Script di validazione del grafo e della prosa. **Implementati 2026-06-09** (pacchetto blindatura). Lanciati: - dall'agente di estensione hook dopo ogni scrittura per storia (fase G e successive), - dalla CI su ogni push/PR (`.github/workfl…"
  },
  {
   "path": "skills/README.md",
   "bytes": 1177,
   "lines": 21,
   "tokens_est": 294,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/README.md",
   "category": "operativo",
   "preview": "**Una sessione = una skill.** Identifica il ruolo, leggi la sua `SKILL.md`, stai nel suo scope. Le **regole comuni** (non-danno, tre fonti, comunicazione con Ray, matrice di propagazione) vivono in **un solo posto: `CLAUDE.md`** in root — …"
  },
  {
   "path": "skills/atlantista/SKILL.md",
   "bytes": 7082,
   "lines": 152,
   "tokens_est": 1770,
   "mtime": "2026-06-12T12:49:33+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/atlantista/SKILL.md",
   "category": "core",
   "preview": "Ramificazione della skill **illustratore** (`skills/illustratore/SKILL.md`). Per istanze IA o collaboratori che producono le **tavole-atlante**: pagine full-page in cui il soggetto vive nel suo posto sull'isola (Fiamma al Forno, Grunto al …"
  },
  {
   "path": "skills/brieffer/SKILL.md",
   "bytes": 7772,
   "lines": 213,
   "tokens_est": 1943,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/brieffer/SKILL.md",
   "category": "core",
   "preview": "**Per l'agente che si occupa di generare/aggiornare i writing brief della saga.**  Questa skill descrive: cosa fai, quando lo fai, come lo fai, e quando NON intervenire."
  },
  {
   "path": "skills/canonizzatore/SKILL.md",
   "bytes": 1498,
   "lines": 27,
   "tokens_est": 374,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/canonizzatore/SKILL.md",
   "category": "core",
   "preview": "**La skill operativa vive in `_visual_pipeline/`** (pacchetto autosufficiente con canone, template, esempi validati e checklist). Questo file esiste per la trovabilità: tutte le skill si trovano in `skills/<ruolo>/SKILL.md`."
  },
  {
   "path": "skills/cartografo/SKILL.md",
   "bytes": 10151,
   "lines": 223,
   "tokens_est": 2538,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/cartografo/SKILL.md",
   "category": "core",
   "preview": "**Scope:** manutenzione, estensione e validazione della cartografia tecnica dell'Isola."
  },
  {
   "path": "skills/contributore/SKILL.md",
   "bytes": 2652,
   "lines": 79,
   "tokens_est": 663,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/contributore/SKILL.md",
   "category": "core",
   "preview": "✅ **Leggere tutto** il repo (visual, cartografia, pipeline_narrativa, catalogo_web)."
  },
  {
   "path": "skills/illustratore/SKILL.md",
   "bytes": 14349,
   "lines": 310,
   "tokens_est": 3587,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/illustratore/SKILL.md",
   "category": "core",
   "preview": "Per **istanze IA** o **collaboratori umani** che si connettono alla repo `isola_i3v_visual` per **caricare immagini HD** (illustrazioni di scena, ritratti, intro volume) generate via Grok Imagine o altro tool.  Versione: 1.1 — 2026-06-10 (…"
  },
  {
   "path": "skills/manutentore/SKILL.md",
   "bytes": 4486,
   "lines": 83,
   "tokens_est": 1122,
   "mtime": "2026-06-12T13:03:53+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/manutentore/SKILL.md",
   "category": "core",
   "preview": "Per chi lavora **sulla** repo invece che **dentro** un ruolo: riordini, ottimizzazioni, refactoring, integrazione pacchetti. Le regole vivono nel `CLAUDE.md` (router) e **non si duplicano qui**: questa skill codifica il PROCESSO. Versione:…"
  },
  {
   "path": "skills/prosa/SKILL.md",
   "bytes": 11792,
   "lines": 260,
   "tokens_est": 2948,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/prosa/SKILL.md",
   "category": "core",
   "preview": "**Da incollare all'inizio di una chat del progetto \"L'Isola dei Tre Venti\" su Claude.ai per attivare la modalità scrittura.**  Questo prompt si autoinizia: leggi le istruzioni, fetcha il brief richiesto da GitHub, e cominci a scrivere insi…"
  },
  {
   "path": "skills/scenografo/SKILL.md",
   "bytes": 12390,
   "lines": 158,
   "tokens_est": 3098,
   "mtime": "2026-06-12T17:42:59+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/scenografo/SKILL.md",
   "category": "core",
   "preview": "Per **istanze IA** (es. Manus) o **collaboratori** che si connettono alla repo `isola_i3v_visual` per **generare le illustrazioni di scena** del libro: una immagine per ogni subhook (pagina libro fisica) delle storie.  Versione: 1.1 — 2026…"
  },
  {
   "path": "skills/visual/SKILL.md",
   "bytes": 13902,
   "lines": 239,
   "tokens_est": 3476,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/visual/SKILL.md",
   "category": "core",
   "preview": "**Scope:** costruisci e mantieni il **serbatoio di descrizioni visive** di tutte le entità della saga (personaggi, luoghi, oggetti, venti, visual_signatures), con immagini di riferimento per modelli generativi e per stampa 3D. La repo `vis…"
  },
  {
   "path": "skills/visual/compilatore.md",
   "bytes": 11819,
   "lines": 212,
   "tokens_est": 2955,
   "mtime": "2026-06-12T12:05:54+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/visual/compilatore.md",
   "category": "operativo",
   "preview": "**STATO 2026-04-28 — bulk concluso.** Il travaso meccanico Bible→catalogo è stato completato per tutte le 112 entità. Successivamente, su richiesta di Ray, lo strato visivo è stato **rimosso dalla Bible** (vedi `SYNC_LOG.md` entry \"pulizia…"
  },
  {
   "path": "tests/README.md",
   "bytes": 1654,
   "lines": 47,
   "tokens_est": 414,
   "mtime": "2026-06-08T07:47:32+00:00",
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/tests/README.md",
   "category": "operativo",
   "preview": "Blindano lo script che monta il libro, così funziona identico su tutti e 4 i volumi."
  }
 ],
 "todos": {
  "groups": [
   {
    "path": "skills/scenografo/SKILL.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/scenografo/SKILL.md",
    "category": "core",
    "items": [
     {
      "line": 147,
      "kind": "checklist",
      "text": "Ogni file ha il suo subhook in `_annotations/sNN.yaml` e nel testo storia"
     },
     {
      "line": 148,
      "kind": "checklist",
      "text": "Naming esatto `sNN_hMMx` (+ `_hd` solo dentro `_hd/`)"
     },
     {
      "line": 149,
      "kind": "checklist",
      "text": "HD: ≥1824×2736 px verticale 2:3, JPG q95, sRGB, metadato DPI a 300"
     },
     {
      "line": 150,
      "kind": "checklist",
      "text": "Personaggi conformi alle canoniche **da ogni angolazione** (volti, capelli, vestiti, scale GU — incluso pose di spalle/profilo)"
     },
     {
      "line": 151,
      "kind": "checklist",
      "text": "Blocco CHARACTER CONSISTENCY presente, identico, in coda a ogni prompt (§2-bis)"
     },
     {
      "line": 152,
      "kind": "checklist",
      "text": "STORY MOMENT presente: azione + emozione + relazioni spaziali esplicite, in inglese"
     },
     {
      "line": 153,
      "kind": "checklist",
      "text": "Chat di generazione nuova per questo batch, reference ri-allegate"
     },
     {
      "line": 154,
      "kind": "checklist",
      "text": "Vincoli di pagina rispettati (page-turn, apparizioni, presenze per-subhook)"
     },
     {
      "line": 155,
      "kind": "checklist",
      "text": "Quiet zone alta rispettata: ~25-30% superiore del frame senza dettagli importanti (cielo / nebbia / parete)"
     },
     {
      "line": 156,
      "kind": "checklist",
      "text": "Nessun testo, lettering, insegna o parola scritta nell'immagine"
     },
     {
      "line": 157,
      "kind": "checklist",
      "text": "Branch solo-immagini, un commit, PR aperta, attesa OK Ray"
     }
    ]
   },
   {
    "path": "skills/brieffer/SKILL.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/brieffer/SKILL.md",
    "category": "core",
    "items": [
     {
      "line": 199,
      "kind": "checklist",
      "text": "Il file esiste in `pipeline_narrativa/writing_briefs/sNN_writing_brief.md`"
     },
     {
      "line": 200,
      "kind": "checklist",
      "text": "Ha le 13 sezioni `## §1` ... `## §13`"
     },
     {
      "line": 201,
      "kind": "checklist",
      "text": "Ha la narrazione fattuale per intero in §3"
     },
     {
      "line": 202,
      "kind": "checklist",
      "text": "Ha 10 hook in §4 (verifica conteggio `### Hook`)"
     },
     {
      "line": 203,
      "kind": "checklist",
      "text": "Ha almeno 1 personaggio in §5"
     },
     {
      "line": 204,
      "kind": "checklist",
      "text": "Ha le cornici in §6 (almeno 1)"
     },
     {
      "line": 205,
      "kind": "checklist",
      "text": "Ha la formula ritornello in §9"
     },
     {
      "line": 206,
      "kind": "checklist",
      "text": "Ha PATTERN_AI_DA_BANDIRE integrale in §10.5"
     }
    ]
   },
   {
    "path": "skills/illustratore/SKILL.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/illustratore/SKILL.md",
    "category": "core",
    "items": [
     {
      "line": 31,
      "kind": "warning",
      "text": "> ⚠️ Errore storico (2026-05-19 → 2026-06-10): branch dell'illustratore che caricavano **ritratti di personaggi** dentro `_volumi/v0N/_hd/` come \"intro volume\", quando erano in realtà **reference saga"
     },
     {
      "line": 174,
      "kind": "checklist",
      "text": "Tutti i file sono in `_hd/`, non nella cartella padre"
     },
     {
      "line": 175,
      "kind": "checklist",
      "text": "Tutti i file hanno suffisso `_hd.jpg`"
     },
     {
      "line": 176,
      "kind": "checklist",
      "text": "I file low-res in `_scene/sNN/sNN_hMMx.jpg` sono **invariati** (`git status` non li mostra)"
     },
     {
      "line": 177,
      "kind": "checklist",
      "text": "Nessun file fuori dallo scope (no modifiche a `.md`, no codice app web, ecc.)"
     },
     {
      "line": 178,
      "kind": "checklist",
      "text": "Verifica risoluzione e formato con:"
     },
     {
      "line": 262,
      "kind": "warning",
      "text": "> ⚠️ Aggiornato 2026-06-10: **i ritratti dei personaggi del Ciclo B NON vanno qui**, vanno al catalogo (vedi §0). `_volumi/v02/_hd/` contiene SOLO illustrazioni prodotte appositamente per il volume e "
     }
    ]
   },
   {
    "path": "skills/visual/SKILL.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/visual/SKILL.md",
    "category": "core",
    "items": [
     {
      "line": 229,
      "kind": "sezione",
      "text": "6. Domande specifiche da fare a Ray (visual)"
     },
     {
      "line": 231,
      "kind": "voce",
      "text": "\"Il modello generativo target per questa entità è X o Y? Workflow?\""
     },
     {
      "line": 232,
      "kind": "voce",
      "text": "\"Per i sotto-tratti del Fiume e gli altri elementi cartografici non in `entities.locations` (es. `radura_dei_pini`), li promuovo a entità grafo o restano carto-only?\""
     },
     {
      "line": 233,
      "kind": "voce",
      "text": "\"Per le immagini di riferimento: quale percentuale di coerenza dobbiamo raggiungere prima di considerare un personaggio 'fissato'?\""
     },
     {
      "line": 234,
      "kind": "voce",
      "text": "\"Per le 4 vedute 3D: convenzione fronte/retro/profilo dx/profilo sx ti va, o preferisci altre angolature canoniche?\""
     },
     {
      "line": 236,
      "kind": "voce",
      "text": ""
     },
     {
      "line": 238,
      "kind": "voce",
      "text": "Ultimo aggiornamento:** 2026-04-25."
     }
    ]
   },
   {
    "path": "skills/atlantista/SKILL.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/atlantista/SKILL.md",
    "category": "core",
    "items": [
     {
      "line": 122,
      "kind": "checklist",
      "text": "Zero testo o pseudo-scrittura, ovunque, anche minuscola"
     },
     {
      "line": 123,
      "kind": "checklist",
      "text": "Zona quieta davvero quieta E diegetica (cielo/nebbia/muro, non carta"
     },
     {
      "line": 125,
      "kind": "checklist",
      "text": "Soggetto coerente con le reference canoniche (colori, firma visiva,"
     },
     {
      "line": 127,
      "kind": "checklist",
      "text": "Ambiente coerente con la scheda luogo (Forno, Burrone, ecc.)"
     },
     {
      "line": 129,
      "kind": "checklist",
      "text": "Stile = SAGA STYLESHEET (niente derive sepia/3D/flat)"
     },
     {
      "line": 130,
      "kind": "checklist",
      "text": "Risoluzione ≥ 1748×2480, verticale, JPEG q95 RGB"
     }
    ]
   },
   {
    "path": "PROJECT_STATE.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/PROJECT_STATE.md",
    "category": "core",
    "items": [
     {
      "line": 17,
      "kind": "todo",
      "text": "- **Catalogo v2 (`web/`):** Next.js 15 su Vercel. ⚠️ TODO aperto: debug deploy fermo alle 16:23 UTC del 2026-06-10 (le PR successive non sono visibili sul sito)."
     },
     {
      "line": 58,
      "kind": "sezione",
      "text": "D. TODO domani — Vercel non ribuilda"
     },
     {
      "line": 61,
      "kind": "voce",
      "text": "Codice in `origin/main`: nuovo layout ✓, cronologia semi ✓, luoghi ✓"
     },
     {
      "line": 62,
      "kind": "voce",
      "text": "Codice in `origin/claude/cutover-deploy-preview`: idem (fast-forward a main) ✓"
     },
     {
      "line": 63,
      "kind": "voce",
      "text": "Vercel** sembra fermo al deploy delle 16:23 UTC (PR #11): nuove PR non visibili in produzione"
     }
    ]
   },
   {
    "path": "skills/cartografo/SKILL.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/cartografo/SKILL.md",
    "category": "core",
    "items": [
     {
      "line": 138,
      "kind": "sezione",
      "text": "3. Domande specifiche da fare a Ray (cartografo)"
     },
     {
      "line": 142,
      "kind": "voce",
      "text": "\"La posizione che avevi in mente per X è Y? Ho stimato da Z.\" (prima di aggiungere feature non triviale)"
     },
     {
      "line": 143,
      "kind": "voce",
      "text": "\"La storia nuova implica un luogo/sentiero nuovo: dove preferisci collocarlo?\""
     },
     {
      "line": 144,
      "kind": "voce",
      "text": "\"Posso usare un sub-agente per estrarre riferimenti geografici da S9-S12 senza saturare il contesto?\" (delega esplorativa)"
     },
     {
      "line": 146,
      "kind": "voce",
      "text": ""
     }
    ]
   },
   {
    "path": "_visual_pipeline/_skill/PIPELINE.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/_skill/PIPELINE.md",
    "category": "operativo",
    "items": [
     {
      "line": 43,
      "kind": "warning",
      "text": "⚠️ **Pattern \"luogo complesso\":** alcuni luoghi (case con esterno+interno, edifici con cortile, piazze con annessi) richiedono **PIÙ blocchi LOCATION distinti** dentro la stessa scheda. Esempio: il Fo"
     },
     {
      "line": 94,
      "kind": "warning",
      "text": "⚠️ **Strategia diversa.** Per i luoghi NON si genera un prompt Grok come per i personaggi. Si scrive direttamente il blocco LOCATION testuale **DENTRO la scheda** (sezione \"Descrizione visiva canonica"
     },
     {
      "line": 208,
      "kind": "warning",
      "text": "⚠️ **I venti hanno regole speciali**: mai personificati visivamente, presenza ambientale. Si trattano come \"atmosfere\" non come \"personaggi\". Approfondire quando si arriva."
     },
     {
      "line": 271,
      "kind": "warning",
      "text": "⚠️ **I luoghi NON hanno `prompt_grok.md`** — il blocco LOCATION è dentro la scheda."
     }
    ]
   },
   {
    "path": "dashboard/README.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/dashboard/README.md",
    "category": "operativo",
    "items": [
     {
      "line": 50,
      "kind": "todo",
      "text": "- **Scansione TODO**: esclude anche `SYNC_LOG.md` (i ⚠️ sono cronaca) e"
     },
     {
      "line": 52,
      "kind": "todo",
      "text": "per tipo — `todo` (TODO/FIXME espliciti), `warning` (⚠️), `checklist`"
     },
     {
      "line": 53,
      "kind": "todo",
      "text": "(`- [ ]`), `sezione`/`voce` (header \"TODO/Aperti/Da fare\" + items) — e"
     },
     {
      "line": 55,
      "kind": "todo",
      "text": "a Ray. Word boundary su TODO (lezione: \"ME**TODO** REVISIONE\")."
     }
    ]
   },
   {
    "path": "_visual_pipeline/README.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/README.md",
    "category": "operativo",
    "items": [
     {
      "line": 108,
      "kind": "warning",
      "text": "| **Luogo** | `scheda.md` (con BLOCCO/BLOCCHI LOCATION testuali) + `descrizione_narrativa_social.md` + (opzionale) immagini establishing | ⚠️ NO prompt_grok.md per luoghi |"
     },
     {
      "line": 110,
      "kind": "warning",
      "text": "⚠️ **Strategia luoghi:** i luoghi vivono come **descrizione testuale** dentro la scheda, non come immagine reference. Questo perché combinare reference visivi di personaggi + reference visivi di luogh"
     },
     {
      "line": 112,
      "kind": "warning",
      "text": "⚠️ **Luoghi complessi (esterno + interno + eventuale cortile/annessi):** la scheda contiene **PIÙ blocchi LOCATION distinti**. In ogni prompt scena si usa **un solo blocco** per scena, quello corrispo"
     }
    ]
   },
   {
    "path": "pipeline_narrativa/documenti_progetto/CARTA_VOCE_v1_2.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/pipeline_narrativa/documenti_progetto/CARTA_VOCE_v1_2.md",
    "category": "progetto",
    "items": [
     {
      "line": 449,
      "kind": "sezione",
      "text": "§5.1 Debito tecnico segnalato (NUOVO in v1.2)"
     },
     {
      "line": 451,
      "kind": "voce",
      "text": "Taratura della saggezza nelle voci secondarie.** Emerso in Fase A3 (durante la stesura schede personaggi maggiori): le voci tipiche dei personaggi tendono a scivolare verso un registro \"saggio\" anche "
     },
     {
      "line": 455,
      "kind": "voce",
      "text": ""
     }
    ]
   },
   {
    "path": "docs/TODO_BRIEFFER_CACHE_AB.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/TODO_BRIEFFER_CACHE_AB.md",
    "category": "operativo",
    "items": [
     {
      "line": 1,
      "kind": "sezione",
      "text": "TODO — Brieffer: riordino in blocchi A/B per il prompt caching"
     },
     {
      "line": 3,
      "kind": "voce",
      "text": "Stato:** debito tecnico aperto · registrato 2026-06-12 · priorità: prima del seeding \"Rocco e Idvara\" (il template eredita il pattern)"
     }
    ]
   },
   {
    "path": "docs/TODO_BUILD_VOLUME_SPREAD_H07A.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/TODO_BUILD_VOLUME_SPREAD_H07A.md",
    "category": "operativo",
    "items": [
     {
      "line": 1,
      "kind": "sezione",
      "text": "TODO — Spread orizzontale per s01_h07 (sessione dedicata `build_volume.py`)"
     },
     {
      "line": 3,
      "kind": "voce",
      "text": "Stato:** in attesa — sessione dedicata Ray + Claude · registrato 2026-06-14 · branch `claude/illustratore-s01-hd-refresh`"
     }
    ]
   },
   {
    "path": "_visual_pipeline/_api/README.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/_visual_pipeline/_api/README.md",
    "category": "operativo",
    "items": [
     {
      "line": 59,
      "kind": "warning",
      "text": "> ⚠️ **`.env` è già nel `.gitignore`** — non verrà committato. Non rimuoverlo dal gitignore mai."
     }
    ]
   },
   {
    "path": "skills/manutentore/SKILL.md",
    "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/skills/manutentore/SKILL.md",
    "category": "core",
    "items": [
     {
      "line": 80,
      "kind": "todo",
      "text": "- Non lasciare TODO orali: un debito tecnico scoperto si registra"
     }
    ]
   }
  ],
  "total": 69,
  "known_issues": {
   "raw": "# known_issues.yaml — Incoerenze referenziali NOTE del grafo, in attesa di\n# decisione autoriale Ray.\n#\n# Meccanismo a cricchetto (audit_3_navigability.py):\n#   - le voci elencate qui vengono declassate da ERRORE a \"[known]\"\n#   - qualunque incoerenza NUOVA resta un errore e blocca la CI\n#   - quando il grafo viene corretto, l'audit segnala la voce come stantia:\n#     rimuoverla da questo file. Obiettivo: file vuoto.\n#\n# Match: (kind, where, ref) — devono coincidere con l'output dell'audit.\n#\n# STATO 2026-06-10: file svuotato. Le 7 voci rilevate il 2026-06-09 sono\n# state risolte da scripts/cornice_mondo/step8_fix_canonical_refs.py\n# (autorizzazione Ray 2026-06-10). Vedi migration_log entry\n# \"cornice_mondo_step8\" nel grafo.\n\nissues: []\n",
   "count": 0,
   "url": "https://github.com/raydalessandro/isola_i3v_visual/blob/main/scripts/audit/_data/known_issues.yaml",
   "mtime": "2026-06-10T08:06:07+00:00"
  }
 },
 "make": [
  {
   "target": "deps",
   "desc": "installa dipendenze (requirements + dev)"
  },
  {
   "target": "audit",
   "desc": "audit 1..4 (grafo + prosa)"
  },
  {
   "target": "audit-fast",
   "desc": "audit 1..3 (salta prosa)"
  },
  {
   "target": "test",
   "desc": "pytest veloce (non slow, ~3s)"
  },
  {
   "target": "test-all",
   "desc": "pytest completo (build PDF reale, ~60s)"
  },
  {
   "target": "check",
   "desc": "test + audit (il cancello pre-push)"
  },
  {
   "target": "catalogo",
   "desc": "rigenera catalogo_web/data/entities.json"
  },
  {
   "target": "briefs",
   "desc": "rigenera i 12 writing brief"
  },
  {
   "target": "volume1",
   "desc": "build PDF volume 1 in _output/"
  },
  {
   "target": "routing",
   "desc": "rigenera la tabella di routing nel CLAUDE.md dai frontmatter skill"
  },
  {
   "target": "dashboard",
   "desc": "rigenera i dati della dashboard di sistema (dashboard/)"
  },
  {
   "target": "sync",
   "desc": "rigenera tutto il derivato (catalogo+briefs+routing+dashboard); git status = report"
  }
 ],
 "counts": {
  "skills": 10,
  "documents": 77,
  "docs_by_category": {
   "core": 15,
   "operativo": 37,
   "progetto": 13,
   "archivio": 12
  }
 }
};
