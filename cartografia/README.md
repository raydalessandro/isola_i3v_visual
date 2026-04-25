# CARTOGRAFIA TECNICA — L'Isola dei Tre Venti

**Versione:** 0.1 (bootstrap)
**Data inizio:** 2026-04-24
**Maintainer:** Ray + Claude (Agente Cartografo)

---

## 1. COS'È QUESTA DIRECTORY

Questa è la **cartografia tecnica canonica** dell'Isola dei Tre Venti. Contiene il database strutturato che descrive fisicamente e urbanisticamente l'isola metro per metro:

- **Geometria reale** dell'isola (GeoJSON con coordinate geografiche).
- **Schede luogo** dettagliate (Markdown) con dimensioni, materiali, orientamenti, sensorialità, stagionalità, funzione narrativa.
- **Convenzioni operative** (sistema coordinate, scale, palette, orientamenti venti).
- **Visualizzatore web** per ispezionare la mappa in tempo reale mentre si edita.

## 2. COS'È IL PUBBLICO DI QUESTA DIRECTORY

**Questa directory NON È per i lettori del libro.** Né per chi scrive le storie. Né per chi fa layout editoriale.

Il pubblico di questo corpus è:

1. **Le IA che generano illustrazioni** (BFL FLUX, Grok, successive). Ricevono dati strutturati da qui per garantire coerenza tra generazioni diverse dello stesso luogo.
2. **Le IA che validano le storie** (sequel di Claude in Fase E e successive) — confrontano i riferimenti geografici nelle storie contro il canonico qui registrato, segnalano incoerenze, propongono correzioni.
3. **Ray + il team umano** — per avere una fonte di verità unica e consultabile invece che ricostruire ogni volta il mondo a memoria.
4. **Il mondo digitale futuro dell'Isola** — qualunque forma prenda (sito esplorabile, gioco, mappa interattiva, companion app), attingerà da qui.

## 3. RELAZIONE CON LA PIPELINE NARRATIVA

**Questa directory è parallela e isolata dalla pipeline narrativa.**

```
┌─────────────────────────────┐       ┌─────────────────────────────┐
│  CARTOGRAFIA TECNICA        │       │  PIPELINE NARRATIVA         │
│  (questa directory)         │       │  (grafo storie, Bible,      │
│                             │       │   apparato, storie S1-S12)  │
│  - GeoJSON canonico         │       │                             │
│  - Schede luogo             │       │                             │
│  - Convenzioni              │       │                             │
│  - Visualizzatore           │       │                             │
└──────────────┬──────────────┘       └──────────────┬──────────────┘
               │                                     │
               │  output: dati strutturati           │
               │  consumati da pipeline immagini,    │
               │  validazione storie, generazione    │
               │  mondo digitale futuro              │
               │                                     │
               └─────────────► OUTPUT ◄──────────────┘
                          (validazione incrociata,
                           prompt immagine arricchiti,
                           coerenza canonica)
```

**Regole di isolamento:**

- Il corpus narrativo (Bible, grafo storie, apparato, schema, manoscritti storie) **non si modifica** a partire dal lavoro cartografico. Se la cartografia rileva incoerenze narrative, le segnala — la risoluzione è decisione narrativa separata.
- La cartografia **non è autoritativa sul canone narrativo primario** (caratteri, seeds, debt, terna strato 3, Pattern A, voce). Quella autorità vive nella pipeline narrativa.
- La cartografia **è autoritativa sul canone fisico e urbanistico** (coordinate, dimensioni, orientamenti, materiali, transizioni spaziali).
- Quando le due autorità si sovrappongono (es. "il Forno è a est" è narrativo *e* cartografico), il canone primario è l'apparato + Bible; la cartografia dettaglia senza contraddire.

## 4. DISCLAIMER SULL'APPARATO v0.2

L'apparato introduttivo del volume unico (`ISOLA_APPARATO_PUBBLICO.md` v0.2 e `ISOLA_APPARATO_TECNICO.md` v0.2, datati 2026-04-24) è stato prodotto **prima** di questo lavoro cartografico, per errore di sequenza di Fase E. Quell'apparato viene trattato qui come **giacimento di estrazione**, non come fonte autoritativa. Sarà riscritto a valle del consolidamento cartografico.

**Non estraete dall'apparato dati che contraddicano la Bible o il grafo storie.** Quando c'è discrepanza, Bible + grafo vincono.

## 5. STRUTTURA DELLA DIRECTORY

```
cartografia/
├── README.md                      ← questo file
├── CHANGELOG.md                   ← storia delle modifiche
├── geo/
│   ├── island.geojson             ← fonte di verità geometrica (MASTER)
│   ├── layers/                    ← opzionale, se isoliamo layer
│   └── viewer/
│       ├── index.html             ← visualizzatore web Leaflet
│       └── style.css
├── luoghi/                        ← schede Markdown per luogo canonico
│   ├── _template_scheda.md        ← template standard
│   ├── villaggio/
│   ├── quartiere_fuoco/
│   ├── quartiere_acqua/
│   ├── quartiere_terra/
│   ├── quartiere_aria/
│   └── perimetro/
└── convenzioni/
    ├── sistema_coordinate.md
    ├── scala_e_proporzioni.md
    ├── convenzioni_id.md
    └── orientamenti_venti.md
```

## 6. WORKFLOW TIPICO

**Quando si aggiunge un luogo nuovo al canonico:**

1. Si apre `_template_scheda.md`, lo si duplica nel sotto-quartiere giusto con ID snake_case.
2. Si compila ciò che è noto; sezioni non applicabili si omettono.
3. Si aggiunge una feature a `geo/island.geojson` con `status: "canonico"` o `"provvisorio"` o `"stub"`.
4. Si verifica nel visualizzatore web che la posizione sia coerente con le transizioni dichiarate nella scheda.
5. Si annota il cambiamento in `CHANGELOG.md`.

**Quando arriva una nuova storia S_NN dall'autore:**

1. Si estraggono tutti i riferimenti geografici espliciti e impliciti.
2. Si confrontano con il canonico qui registrato.
3. Se coerenti: si registrano in `funzione narrativa > storie in cui compare` delle schede toccate.
4. Se incoerenti: si flagga nel CHANGELOG e si segnala a Ray per decisione narrativa.

**Quando si genera un prompt immagine per un luogo:**

1. Si legge la scheda del luogo.
2. Si estraggono: coordinate, orientamento, materiali, dettagli firma, palette, sensorialità di ora/stagione.
3. Si compone il prompt arricchito programmaticamente (Fase E automazione).

## 7. CONVENZIONI DI NAMING

- **ID luogo:** `snake_case`, italiano, senza articoli (`forno_di_fiamma`, non `il_forno_di_fiamma`).
- **File scheda:** `luoghi/<quartiere>/<id>.md`.
- **Feature GeoJSON:** `properties.id` uguale all'ID scheda.
- **Cambiamenti:** ogni modifica significativa registrata in `CHANGELOG.md` con data.

## 8. SISTEMA COORDINATE

L'isola è ancorata a coordinate reali fittizie nel Mediterraneo centrale. Vedi `convenzioni/sistema_coordinate.md` per dettagli.

## 9. STATO

**v0.5** — Mappa urbanistica completa navigabile. 103 feature. Visualizzatore web Google Maps-style con ricerca, dettagli al click, navigazione parent/children. Ogni edificio canonico raggiungibile da almeno una via.

### Come aprire la mappa navigabile

1. Apri `cartografia/geo/viewer/index.html` con un doppio click (qualsiasi browser moderno).
2. Funzionalità disponibili:
   - **Ricerca in alto**: digita nome, ID, o alias di un luogo.
   - **Click su un punto**: apre pannello dettaglio con note canoniche, proprietà, link a luoghi collegati.
   - **Filtri nella sidebar**: per categoria, quartiere, stato.
   - **Scroll/drag**: zoom e pan come Google Maps.

### Script di utilità

`verifica_luogo.py` — interrogazione programmatica della cartografia. Utile per validare coerenza geografica delle storie:

```bash
cd cartografia/
python3 verifica_luogo.py --id due_massi           # info su luogo
python3 verifica_luogo.py --id villaggio_centrale  # risolve alias
python3 verifica_luogo.py --id fiume_che_gira      # feature aggregata
python3 verifica_luogo.py --coord 3100 5500        # cosa c'è qui
```

---

**FINE README v0.1**
