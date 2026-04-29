# PROJECT_STATE — Snapshot al 2026-04-28

> Per le sessioni precedenti (bootstrap 2026-04-25 → fase E) vedi sezioni cronologiche sotto.

## Sessione 2026-04-28 — Fase E completata + Fase G in preparazione

**Stato corrente:**
- **Grafo:** `pipeline_narrativa/story_graph.json` v1.0.0 schema 1.2 (12 storie + entities + seeds + callbacks + quote_tracker). Backup pre-fase E in `story_graph.v0.10.0.backup.json`.
- **Catalogo:** 115 entities (23 personaggi + 43 luoghi + 31 strade + 14 oggetti + 3 venti + 1 visual signature).
- **Schede `visual/`:** 115 schede tutte `provvisorio`. Compilazione meccanica fase F.1 fatta (56 sezioni stub popolate da grafo). Sezioni autoriali pure (Variabilità ammessa, Per stampa 3D, Per narrativa social) restano vuote in attesa di Ray + collaboratori esterni (`contributi/`).
- **Cartografia:** v0.6.1 (104 feature, viewer Leaflet).
- **Misalignments:** 8/8 resolved.

**Fase E (completata 2026-04-28):**
Migrazione grafo schema v1.1 → v1.2. 60 no_inference_fields decisi via Q1-Q6 autoriali Ray. 87 provvisori P2 (22A + 47B + 18C). Workspace archiviato in `_porting_grafo/`.

**Fase F (in corso):**
- F.1 ✅ travaso meccanico grafo → schede (56 sezioni popolate).
- F.2 🔄 aggiunte autoriali Ray + collaboratori (`contributi/` accoglie proposte datate).
- F.3 ⏳ travaso inverso visual → grafo.

**Fase G (in preparazione):**
Estensione hook visivi 5→10 per storia. Bump grafo v1.0.0 → v1.1.0 + schema v1.2 → v1.3 (additivo: nuovi campi `type`, `is_signature`, `provenance`, `composition_zone` su scene_hook).
- Input: `pipeline_narrativa/narrazione_fattuale/s0X_*.md` (Ray sta producendo i 12 file).
- Prompt operativo: `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md`.
- Audit: `scripts/audit/` (4 script da implementare).
- Modalità: una storia alla volta, approvazione Ray tra storia e storia.
- Output finale atteso: 120 hook validati totali (10 × 12).

**File chiave introdotti in questa sessione:**
- `CLAUDE.md` (radice) — istruzioni operative per istanze IA + collaboratori.
- `contributi/README.md` + `contributi/TEMPLATE.md` — workflow per collaboratori esterni.
- `pipeline_narrativa/narrazione_fattuale/README.md` — placeholder per le 12 narrazioni fattuali.
- `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md` — prompt fase G.
- `scripts/audit/README.md` — specs dei 4 audit.
- `scripts/compile_visual_from_graph.py` — compilatore fase F.1 (idempotente).

---

## Sessioni precedenti (storico)

# PROJECT_STATE — Snapshot al 2026-04-25

Documento riassuntivo di **dove siamo oggi**. Per il dettaglio storico vedi `cartografia/CHANGELOG.md`.

---

## Sessione 2026-04-25 — Bootstrap repo `isola_i3v_visual`

Il lavoro si sposta dal vecchio archivio `isola_tre_venti_github` al repo unificato **`isola_i3v_visual`**, che ora ospita due tracce parallele:

- **`cartografia/`** — la cartografia tecnica esistente, da continuare a espandere (sync grafo, schede luogo, sentieri).
- **`visual/`** — nuova traccia: serbatoio di descrizioni visive e vincoli prompt per tutte le entità (luoghi, personaggi, oggetti, venti-spiriti), con immagini di riferimento e piccolo sito web interno per consultazione.
- **`pipeline_narrativa/`** — INPUT read-only invariato.

**Cambiamenti operativi di oggi (bootstrap):**
- Estratto contenuto della zip `isola_tre_venti_github` nella nuova struttura.
- Rinominato `cartografia_tecnica/` → `cartografia/`. Path aggiornati nei doc.
- Sostituito `pipeline_narrativa/story_graph.json` con la versione **v0.10.0** (S1-S12, contro v0.6.0 con S1-S8 della zip).
- Creata directory `visual/` (vuota, da popolare nelle prossime sessioni dopo brief Ray).
- README di radice riscritto per riflettere il nuovo scope.
- **`AGENT_INSTRUCTIONS.md` rifattorizzato in cartella `skills/`**: orchestratore (`skills/README.md` con regole comuni), `skills/cartografo.md` (skill cartografia, scope `cartografia/`), `skills/visual.md` (skill visual, scope `visual/`, in attesa brief Ray). L'agente sceglie una skill per task e si attiene al proprio scope di scrittura.

**Cartografia v0.5 → v0.6.0 (sync grafo v0.10.0):**
- Diff grafo: S1-S8 identiche; S9-S12 nuove ma riusano i 35 ID di luogo già esistenti. 0 location aggiunte/rimosse formalmente.
- Backward-compat grafo↔cartografia: 100% verificata (pre e post modifiche).
- Estrazione esaustiva toponimi S9-S12 (24 distinti, 21 coperti, 2 orfani veri, 1 ambiguo).
- Modifiche cartografiche puntuali (vedi `cartografia/CHANGELOG.md` v0.6.0):
  - Aggiunta `radura_dei_pini` (Polygon provvisorio, dentro Foresta Intrecciata).
  - Promotion `sentiero_roccia_burrone` provvisorio→canonico.
  - Annotazione cengia su `roccia_alta.note`.
  - Alias `guado_nord` → `guado_di_pietre_piatte`.
- Creato `SYNC_LOG.md` in radice per tracciare i cambiamenti che impattano altre repo del sistema.

**Pendente (prossima sessione):**
- **Manutenzione grafo storie** (annunciata da Ray): la versione manutenuta diventerà la nuova baseline. Possibili incoerenze emerse si risolveranno in v0.6.x o v0.7.

**Visual — bootstrap (sessione 2026-04-25, stessa sessione):**
- Brief Ray ricevuto: scope = serbatoio descrizioni visive + 4 vedute 3D, fonte unica per IA generative / illustrazioni / 3D / narrativa / social. Niente prompt-string pronti, descrizioni ricche multi-uso. Verità tendenzialmente nel grafo (debito tecnico disallineamenti grafo↔Bible noto, fuori repo).
- Creati `scripts/` (tool condivisi) e `scripts/build_visual_skeleton.py` (idempotente, frontmatter rigenerato, body preservato).
- Struttura `visual/` generata: 81 schede stub in cartelle frattali.
  - Personaggi (23): individuali split in `bambini` (3) / `primari` (6) / `cuccioli` (5) / `secondari` (4) + `collettivi` (5).
  - Luoghi (41): albero geografico per quartiere (centro, terra, fuoco, acqua, aria, perimetro), nesting frattale (es. piazza→albero_vecchio→panca, foresta→radura/tana/torrente, fiume→6 sotto-tratti+guado).
  - Oggetti (13), Venti (3), Visual_signatures (1).
  - Ogni cartella ha `scheda.md` (frontmatter YAML compilato + body stub) + `immagini/` (per riferimenti IA + 4 vedute 3D).
- Schema scheda con 14 sezioni modulari; metadati cartografici nei frontmatter dei luoghi (centroide, bbox, dimensioni, quartiere, parent/children — l'altitudine si aggiungerà rilanciando lo script quando il GeoJSON la includerà).
- `skills/visual.md` aggiornato con regole concrete e workflow estrazione.
- `skills/README.md` aggiunto `scripts/` come directory condivisa.
- `visual/README.md` + `visual/_template_scheda.md` + `visual/catalogo.md` (auto-rigenerabile).

**Visual — strade aggiunte (stessa sessione):**
- Esteso `scripts/build_visual_skeleton.py` con sezione strade + funzione `path_metadata()` (lunghezza, endpoints) + generazione `visual/luoghi/_strade_index.md`.
- 31 strade secondarie create come schede stub in `<quartiere>/strade/<id>/`. Le 5 Vie principali (in `entities.locations`) restano paritetiche.
- Distribuzione: centro 4, terra 9, fuoco 2, acqua 6, aria 4, perimetro 6.
- Frontmatter strade arricchito con metadati cartografici specifici (`lunghezza_m_local`, `n_punti`, `endpoint_a_m`, `endpoint_b_m`, `categoria_strada`).
- **Totale schede visual: 112** (era 81, +31 strade).

**Visual — sotto-skill `compilatore` + cambio metodo (stessa sessione):**
- Sub-agenti general-purpose hanno avuto stream idle timeout su tutti e 3 i tentativi (gabriel/elias/noah). Estrazione manuale di **Liu** come scheda pilota. Validazione qualità: OK.
- **Cambio principio operativo** (richiesta Ray): da "sezioni non applicabili → rimuovile" a **"completa tutte le 14 sezioni con inferenza canone-coerente marcata"**. Razionale: serbatoio di proposte per narrativa futura.
- Marcatori provenienza in linea: nessun tag = canone (citato in fondo); `[inf]` = inferito dai dati canonici; `[prop]` = proposta visiva da validare con Ray.
- **`skills/visual.md` spostato in `skills/visual/README.md`** — la skill visual diventa cartella per ospitare sotto-skill specializzate.
- Nuova sotto-skill: **`skills/visual/compilatore.md`** — formalizza il metodo di compilazione (estrazione mirata, lettura fonti, completamento marcato, citazioni, vincoli, esempio Liu).
- `visual/_template_scheda.md` aggiornato col nuovo principio.
- `skills/README.md` esteso con tabella permessi sotto-skill.
- Sotto-skill future previste come placeholder: `prompter.md`, `generatore_immagini.md` (non create finché non servono).

**Catalogo web — V1 (stessa sessione):**
- Costruito sito statico interno `catalogo_web/` per consultazione di tutte le entità di `visual/` da browser.
- Stack: HTML + CSS + JS vanilla (no React, no build pipeline). Markdown via `marked.js` da CDN.
- Script `scripts/build_catalogo_web.py` (idempotente) scansiona `visual/`, parsa frontmatter YAML (PyYAML) e body MD, raccoglie immagini, costruisce albero gerarchico riflesso della struttura folder, scrive `catalogo_web/data/entities.json` (~390 KB, 112 entità).
- Funzionalità V1: sidebar ad albero navigabile (stesso nesting frattale), search testuale, pagina entità (tag, frontmatter collassabile, body MD renderizzato, gallery immagini), pagina indice strade, link al viewer cartografia esistente, hash routing.
- Deploy: GitHub Pages serve `main` da root → URL `https://raydalessandro.github.io/isola_i3v_visual/catalogo_web/`. Auto-rideploy a ogni push.
- Test locale: `python3 -m http.server` dalla radice → `http://localhost:8000/catalogo_web/`.

**Pendente:**
- Compilazione body delle restanti ~111 schede (Ray fa il bulk in chat con la zip, metodo `compilatore`). Liu è il riferimento.
- Generazione immagini di riferimento (4 vedute 3D + variazioni IA — futura sotto-skill `generatore_immagini`).
- Auto-promozione status `stub` → `provvisorio` quando il body è compilato (miglioramento allo script `build_visual_skeleton.py`, da fare).
- Auto-rebuild del catalogo web tramite GitHub Actions (opzionale, V2).

---

## Sessione 2026-04-24 — Costruzione cartografia v0.1 → v0.5

Sessione dedicata alla **nascita e costruzione della cartografia tecnica**, da zero a v0.5. Cinque release incrementali:

| Versione | Cosa introduce |
|----------|----------------|
| **v0.1** | Bootstrap: struttura directory, convenzioni base, contorno isola, Fiume preliminare come anello chiuso, 4 centroidi quartieri, 18 feature |
| **v0.2** | Risolta fisica del Fiume (Variante C: due bracci asimmetrici, Sorgente a nord, Bocca a sud). Allargata rete sentieri da grafo storie. 46 feature. |
| **v0.3** | Fiume spezzato in sotto-tratti per agganciare punti canonici. Sorgente da falda (non da ruscelli). Posizionamento completo: Piazza, Orti a 3 anelli, Foresta polygon, Pascoli, quartieri polygon, edifici Villaggio e Quartiere Fuoco. 74 feature. |
| **v0.4** | Backward-compatibility totale con grafo storie v0.6.0 (34/34 ID coperti via alias/aggregate/parent). Strade canoniche estratte dalle 8 storie. Nuovi landmark: Pozza dei Pascoli (S2), Noce della Scuola (S8), I Due Massi (S7), Zona di lavoro Salvia (S4). 83 feature. |
| **v0.5** | Urbanistica completa e navigabile. 18 sentieri nuovi per raggiungibilità di tutti gli edifici. Visualizzatore web Google Maps-style (ricerca, pannello dettaglio, filtri, navigazione parent/children). 103 feature, 36 sentieri. |

---

## Stato attuale

- **Cartografia:** `cartografia/geo/island.geojson` **v0.6.0** — 104 feature (+1 radura).
- **Grafo storie:** `pipeline_narrativa/story_graph.json` v0.10.0 — 12 storie S1-S12.
- **Visual:** `visual/` directory creata, contenuto da definire (brief Ray atteso).
- **Documenti progetto:** corpus canonico completo in `pipeline_narrativa/documenti_progetto/` (Bible, Glossario, voce, pattern AI da bandire, archi 12 storie, EAR framework, ecc.).
- **Apparato:** v0.2, trattato come giacimento di estrazione non autoritativo (vedi disclaimer).
- **Backward-compatibility grafo ↔ cartografia:** **100%** (35/35 ID coperti, verificata 2026-04-25).
- **SYNC_LOG.md:** attivo in radice per tracciare cambiamenti cross-repo.

---

## Decisioni chiave fissate oggi

1. **Fiume a Variante C:** due bracci asimmetrici (Ovest stretto e veloce, Est ampio e lento) che si uniscono a Sorgente nord e Bocca sud. Fisicamente coerente con S7 (zattera).
2. **Sorgente da falda profonda**, non da ruscelli superficiali. Lascia flessibilità narrativa su ruscelli stagionali.
3. **Sotto-tratti del Fiume** spezzati quando un punto narrativo ha peso canonico (es. Stretta dei Due Massi da S7).
4. **Backward-compatibility ID via aliases** (es. `villaggio_centrale` → `piazza_villaggio`) **e feature aggregate** (es. `fiume_che_gira` come MultiLineString con 6 children). Nessuna rottura del grafo storie.
5. **Isolamento cartografia/narrativa:** cartografia non modifica mai il corpus narrativo. Se emergono incoerenze, si segnalano, non si risolvono in autonomia.
6. **Urbanistica completa** anche oltre quella battuta dalle storie (sentieri costieri, ring road Quartiere Fuoco, viottoli Piazza). Tutto inferito è `provvisorio`.

---

## Prossimi passi naturali

### Per Ray (priorità)

1. Caricare questo repository su GitHub.
2. Configurare agente IA (Claude Agent SDK via Anthropic API) per lavorare sul repo.
3. Testare il visualizzatore web e feedback estetica/funzionalità.
4. Aggiornare `pipeline_narrativa/story_graph.json` quando arrivano nuove storie da altro autore.

### Per l'agente IA (quando Ray attiva il workflow)

1. Verificare backward-compat dopo ogni update del grafo.
2. Estrarre riferimenti geografici dalle nuove storie S9-S12.
3. Proporre feature nuove o aggiornamenti `status`.
4. Mantenere CHANGELOG aggiornato.

### Iterazione futura (non urgente)

- **Schede luogo dettagliate** — compilare `luoghi/<quartiere>/<id>.md` a partire dai luoghi-chiave (Forno, Albero Vecchio, Grotta di Grunto, Casa di Amo, Pontile).
- **Fix posizioni Vie** — fare in modo che le Vie principali si fermino al bordo della Piazza, non al centro esatto.
- **Pipeline immagini** — quando sarà ora, prompt BFL pescano automaticamente da schede + GeoJSON per garantire coerenza visiva cross-scena.
- **Mondo digitale** — base dati strutturata pronta per eventuale sito esplorabile/app.

---

## Cosa NON abbiamo toccato (volutamente)

- **Bible, Glossario, voce, pattern_ai_da_bandire, ARCHI 12 storie:** corpus narrativo intatto, solo referenziato.
- **Grafo storie:** Ray lo aggiorna manualmente. Cartografia lo legge ma non lo scrive.
- **Apparato v0.2:** pre-esistente alla cartografia, trattato come giacimento non autoritativo. Ray lo riscriverà a valle.
- **Scrittura prosa storie:** fuori dal perimetro cartografia. Gestito da Ray + altro autore.

---

## Contatti file-chiave

- **README principale:** `README.md` (radice repo)
- **Istruzioni per agenti IA:** `AGENT_INSTRUCTIONS.md`
- **Questo documento:** `PROJECT_STATE.md`
- **Storia cartografia:** `cartografia/CHANGELOG.md`
- **Architettura cartografia:** `cartografia/README.md`
- **Fonte di verità geometrica:** `cartografia/geo/island.geojson`
- **Visualizzatore:** `cartografia/geo/viewer/index.html` (doppio click)
- **Utility verifica:** `cartografia/verifica_luogo.py`

---

**Buon lavoro.**
