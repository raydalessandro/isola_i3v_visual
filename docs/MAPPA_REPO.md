# Mappa della repo — directory per directory

> Estratta dal CLAUDE.md v2.x nel riordino router (2026-06-12) e mantenuta qui come
> riferimento di navigazione. Aggiornarla quando la **struttura** cambia (nuove directory,
> nuovi script), non per i contatori di stato (quelli vivono in `PROJECT_STATE.md`).


```
isola_i3v_visual/
│
├── pipeline_narrativa/        ⚠️ READ-ONLY (canone narrativo)
│   ├── story_graph.json              v1.2.0 schema 1.4 (post-cornice-del-mondo: world_conventions root + cornice_dettagli + path_details)
│   ├── story_graph.v0.10.0.backup.json  backup pre-migrazione fase E
│   ├── story_graph.json.pre_v1_3.backup.json  backup pre-bump schema 1.2->1.3
│   ├── story_graph.json.pre_fase_g.backup.json  backup pre-hook estesi
│   ├── story_graph.json.pre_cornice_mondo.backup.json  backup pre-Step 1+2 (2026-04-30)
│   ├── story_graph.json.pre_step4_cornici.backup.json  backup pre-Step 4 (2026-04-30)
│   ├── story_graph.json.pre_step5_sentieri.backup.json backup pre-Step 5 (2026-04-30)
│   ├── story_graph.json.pre_step6_path_details.backup.json backup pre-Step 6 (2026-04-30)
│   ├── story_graph.json.pre_step8_canonical_refs.backup.json backup pre-Step 8 (2026-06-10)
│   ├── hooks_proposals/<ciclo>/sNN.yaml  input deterministici per write_hooks_to_graph.py
│   ├── narrazione_fattuale/sNN_*.md  12/12 file narrazione fattuale derivati dal sorgente _source/
│   ├── writing_briefs/sNN_writing_brief.md  12 brief autosufficienti per agente prosa (output zero-token brieffer)
│   ├── writing_briefs/_reference/    s01_writing_brief_FINAL.md (reference Ray, validato)
│   ├── storie_finali/sNN_<slug>.md   12 testi prosa DEFINITIVI con frontmatter YAML + marker @hook (narrativo, 1..10) + marker @subhook (pagina libro fisica, 1..book_pages_total) machine-readable, consumati da scripts/build_volume.py (compositore PDF KDP, attivo dal 2026-06-08; vedi storie_finali/README.md)
│   ├── storie_finali/_annotations/   YAML autoriali Ray (sNN.yaml) — note di scena
│   ├── storie_finali/_inventory/     inventari testuali derivati (audit/QA prosa)
│   ├── storie_finali/_scene/sNN/     immagini-scena composte per pagina libro fisica (sNN_hMMx.jpg low-res, x ∈ {a,b,c,...}), referenziate dal marker @subhook ... @image. Subdir `_hd/sNN_hMMx_hd.jpg` per versione HD stampa (JPG q95 sRGB, ≥1824×2736 px, DPI metadata 300; vedi sezione 9). NON sono reference catalogo (quelle stanno in visual/<categoria>/<id>/immagini/)
│   ├── storie_finali/_volumi/        cornice editoriale 4 volumi (3 storie/volume, 1:1 con cicli A/B/C/D): soglia, introduzioni_cicli, stato_zero_e_sigilli, presentazione_completa, presentazioni_parziali, porte, congedo + _elementi_fissi/ (riferimenti read-only) + v0N/_hd/v0N_intro_<slug>_hd.jpg per illustrazioni HD intro volume. Marker ## VOLUME N interni per compositore libro
│   └── documenti_progetto/           Bible, Carta Voce, ARCHI, Glossario, EAR, Pattern AI da bandire
│
├── visual/                    ✅ scrittura su scheda.md per arricchimento (con cautela) + immagini canoniche + prompt_grok.md
│   ├── personaggi/                   24 schede (3 fratelli, 5 primari, 5 secondari, 5 cuccioli, 6 collettivi inclusi pescatori_case_basse)
│   │   │  ⚠️ NB: la Bible usa "Abitanti maggiori" per gli stessi 5 di `primari/` — stesso insieme, vocabolari diversi (narrativo vs filesystem)
│   │   ├── individuali/{bambini,primari,secondari,cuccioli}/<id>/  scheda.md + prompt_grok.md (28 prompt grok pubblicati al 2026-04-30) + immagini/
│   │   └── collettivi/{camminanti,mantenitori,coltivatori_del_cerchio,mercato_del_mezzogiorno,pastori,pescatori_case_basse}/scheda.md  con sezione `## Saluto del gruppo` (DOC_2)
│   ├── luoghi/                       74 schede (per quartiere: aria/acqua/fuoco/terra/centro + perimetro + strade)
│   │   └── 5 schede sentieri Tier A (via_dell_alba, sentiero_orti_torrente_foresta, via_che_sale, sentiero_orti_casa_salvia, viottolo_perimetrale_piazza) con `## Coerenza cross-scena` aggiornata con dettagli stabili da `path_details.paths.<id>` del grafo
│   ├── oggetti/                      14 schede (13 oggetti-simbolo + 1 oggetto_di_scena_ricorrente) — tutte con prompt_grok.md
│   ├── venti/                        3 schede (Taglio/Intreccio/Mulinello)
│   └── visual_signatures/            1 scheda (quando_acqua_trema)
│
├── _visual_pipeline/          ✅ pacchetto operativo (canone, template, esempi, skill)
│   ├── README.md                     entry point pipeline
│   ├── _canone/                      3 doc canone saga (stylesheet, scale, palette)
│   ├── _templates/                   5 template (scheda + prompt grok + descrizione social)
│   ├── _skill/                       PIPELINE.md (flusso 6 fasi) + CHECKLIST.md
│   └── _esempi/                      bartolo, fiamma, forno, grembiule_fiamma (validati)
│
├── cartografia/               ✅ scrittura tecnica
│   ├── geo/island.geojson            104 feature, sistema cartesiano locale
│   ├── geo/viewer/                   viewer Leaflet
│   └── README.md                     architettura cartografica
│
├── catalogo_web/              ⚠️  legacy: solo `data/` (contratto JSON), UI archiviata 2026-06-10
│   ├── data/entities.json            generato da `scripts/build_catalogo_web.py` (con blocco `meta` da WI-8)
│   ├── data/storie.json              storie dashboard
│   └── _archive/                     UI vanilla deprecata (catalogo v2 vive in `web/`)
│
├── web/                       ✅ catalogo v2 — app Next.js 15 (App Router, TS strict)
│   ├── app/                          home workbench, /catalogo, /storie, /mappa, /orchestra, /stato, /strade
│   ├── app/api/img/[...path]/        proxy immagini same-origin (WI-3, abilita download)
│   ├── components/catalogo/          entity-body (deep link sezioni), prompt-grok-block (copy per vista), gallery, lightbox
│   ├── components/command-palette.tsx  ⌘K navigazione veloce (WI-5)
│   ├── lib/prompt-grok.ts            parser markdown prompt grok (WI-1) + test (13/13 pass)
│   ├── scripts/build-search-index.mjs  indice cmd-K (build-time)
│   └── scripts/dev-watch.mjs         modalita' live: `npm run dev:live` (WI-7)
│
├── _porting_grafo/            🗄️  ARCHIVIO una-tantum (fase E completata 2026-04-28)
│   ├── dossier_fase_e/               kit migrazione + MIGRATION_PROMPT + schema v1.2 + INPUT_NODES (12 nodi v1.1)
│   ├── output/s01..s12/              per ogni storia: canonical, provisional, migration_notes, catalog_proposals, _p1_mapping
│   └── scripts/migrate_p1.py         script P1 (carpentiere meccanico)
│
├── _pacchetti_consegnati/     🗄️  ARCHIVIO pacchetti autoriali Ray gia integrati (2026-04-30)
│   ├── README.md                     orchestratore + pattern di integrazione futura
│   └── cornice_mondo/                pacchetto integrato 2026-04-30 (DOC_1..DOC_6 + README dedicato)
│
├── contributi/                ✅ scrittura per collaboratori esterni (proposte/aggiunte)
│   └── (file .md datati, vedi sezione 5)
│
├── _starter_kit/              ✅ template di sistema riusabile (scheletro, NO contenuto saga)
│   └── README.md                     entry point (setup nuova "isola" da zero)
│
├── scripts/                   ✅ tool Python condivisi (idempotenti)
│   ├── build_catalogo_web.py            rigenera catalogo_web/data/entities.json da visual/
│   ├── build_visual_skeleton.py         ricrea schede stub da grafo (non usare in fase F)
│   ├── compile_visual_from_graph.py     travaso meccanico grafo → schede (fase F.1)
│   ├── split_narrazione_fattuale.py     split sorgente Ciclo*.txt → 12 sNN_*.md
│   ├── migrate_graph_v1_2_to_v1_3.py    bump schema fase G (one-shot, idempotente)
│   ├── promote_visual_entities_to_graph.py  promozione catalogo visual → grafo entities
│   ├── write_hooks_to_graph.py          writer deterministico fase G (input YAML hooks_proposals/)
│   ├── build_writing_brief.py           ⭐ NEW (2026-04-30) generatore zero-token brief writing per agente prosa
│   ├── build_volume.py                  ⭐ NEW (2026-06-08, v2) compositore libro stampa KDP (A5 300 DPI bleed) — output PDF in _output/
│   ├── design_system.py                 ⭐ NEW (2026-06-08) identita visiva collana (palette tre venti + 6 quartieri, font, ornamenti, glifi, cornici, camuni)
│   ├── cornice_mondo/                   ⭐ NEW (2026-04-30) pacchetto 7 step "cornice del mondo"
│   │   ├── step1_world_conventions.py   crea nodo radice world_conventions + extends quote_tracker
│   │   ├── step4_cornici.py             scrive 24 cornice_dettagli + 8 formule + 2 cantilene
│   │   ├── step5_sentieri_fantasma.py   appende 36 sentieri a locations_secondary
│   │   ├── step6_path_details.py        popola path_details.paths con 5 sentieri Tier A
│   │   ├── step8_fix_canonical_refs.py  ⭐ NEW (2026-06-10) uniforma 7 ref ad id canonici (foresta, pontile, villaggio, who.refs)
│   │   ├── _data/                       4 YAML deterministici (refrain, cornici_24, sentieri_fantasma, path_details_tierA)
│   │   └── _audit/                      riservata audit successivi
│   └── audit/                           ⭐ NEW (2026-06-09) audit grafo+prosa IMPLEMENTATI (4 script + runner + manifest backup + baseline known_issues). `python3 scripts/audit/run_all_audits.py`
│
├── assets/                    ⭐ NEW (2026-06-08) asset condivisi per build (font collana)
│   └── fonts/                        7 TTF OFL: Fraunces, Nunito, Fredoka, Lora — usati da build_volume.py + design_system.py
│
├── tests/                     ⭐ NEW (2026-06-08) suite test impaginazione (60 test, ~4s)
│   ├── test_build_volume.py          struttura/robustezza/decori/coerenza 4 volumi/determinismo
│   ├── test_integration.py           build PDF reale + invarianti KDP (slow, ~60s)
│   └── README.md                     come eseguire i test
│
├── pytest.ini                 ⭐ NEW (2026-06-08) config pytest (marker `slow` per integration)
│
├── skills/                    ✅ skill agente IA
│   ├── README.md                     orchestratore
│   ├── cartografo.md                 manutenzione cartografia
│   ├── brieffer/                     genera writing_briefs autosufficienti (2026-04-30)
│   │   └── SKILL.md
│   ├── prosa/                        ⭐ NEW (2026-04-30) agente prosa: scrive il testo finale delle storie
│   │   └── SKILL.md                  da incollare in chat Claude.ai per attivare modalita scrittura
│   ├── illustratore/                 ⭐ NEW (2026-05-19) agente illustratore: workflow upload HD per stampa
│   │   └── SKILL.md                  pattern branch + naming + commit per immagini HD pronte al merge
│   └── visual/
│       ├── README.md                 skill visual generale
│       └── compilatore.md            sotto-skill compilazione schede
│
├── README.md                  panoramica generale
├── PROJECT_STATE.md           snapshot operativo
├── SYNC_LOG.md                log cambiamenti cross-skill
└── CLAUDE.md                  questo file
```

---
