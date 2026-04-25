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

**Subito dopo il bootstrap (in questa stessa sessione):**
- Diff grafo v0.6.0 → v0.10.0: storie e location nuove (S9-S12, eventuali aggiornamenti a S1-S8).
- Verificare backward-compat 100% grafo v0.10.0 ↔ cartografia v0.5.
- Estrarre riferimenti geografici da S9-S12 (sub-agente per non saturare il contesto).
- Proporre a Ray nuove feature / alias / sentieri / aggiornamenti `status`.
- Bump cartografia (probabile v0.5 → v0.6).

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

- **Cartografia:** `cartografia/geo/island.geojson` v0.5 — 103 feature.
- **Grafo storie:** `pipeline_narrativa/story_graph.json` v0.10.0 — 12 storie S1-S12 (sync con cartografia da verificare).
- **Visual:** `visual/` directory creata, contenuto da definire.
- **Documenti progetto:** corpus canonico completo in `pipeline_narrativa/documenti_progetto/` (Bible, Glossario, voce, pattern AI da bandire, archi 12 storie, EAR framework, ecc.).
- **Apparato:** v0.2, trattato come giacimento di estrazione non autoritativo (vedi disclaimer).
- **Backward-compatibility grafo ↔ cartografia:** verificata al 100% per v0.6.0; **da riverificare per v0.10.0**.

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
