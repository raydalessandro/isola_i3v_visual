# skill: cartografo

**Scope:** manutenzione, estensione e validazione della cartografia tecnica dell'Isola.

**Scrivi in:** `cartografia/` (tutto). **Non tocchi:** `visual/`, `pipeline_narrativa/`, file di radice (a meno che il task non lo richieda esplicitamente).

**Premessa:** prima di operare, leggi sempre `skills/README.md` per le **regole comuni** (autorità, isolamento `pipeline_narrativa/` read-only, comunicazione con Ray, pattern di rifiuto).

---

## 0. Cosa leggere in ordine di priorità

### Sempre, prima di qualsiasi task cartografico

1. `skills/README.md` — regole comuni.
2. Questo file.
3. `cartografia/README.md` — architettura cartografia.
4. `cartografia/CHANGELOG.md` — storia delle decisioni cartografiche.

### Per task sul mondo / geografia

5. `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §2 (Geografia), §3 (Venti), §8 (Acqua).
6. `pipeline_narrativa/documenti_progetto/GLOSSARIO_ISOLA.md` (catalogo nomi canonici).
7. `cartografia/convenzioni/` (tutti i 4 file).

### Per task che toccano storie

8. `pipeline_narrativa/story_graph.json` — grafo corrente.
9. `pipeline_narrativa/documenti_progetto/ARCHI_12_STORIE_v1_1.md` — mappa narrativa complessiva.

---

## 1. Principi non negoziabili (specifici cartografo)

### Principio 1 — Backward-compatibility grafo ↔ cartografia

Il grafo storie e la cartografia devono sempre essere allineati sugli ID. Se il grafo usa un ID (`villaggio_centrale`, `fiume_che_gira`, ecc.), la cartografia deve risolverlo direttamente o via `aliases` / `children` (feature aggregate).

**Verifica obbligatoria dopo ogni modifica al GeoJSON:**

```bash
python3 -c "
import json
with open('pipeline_narrativa/story_graph.json') as f:
    graph_ids = set(json.load(f)['entities']['locations'].keys())
with open('cartografia/geo/island.geojson') as f:
    geo = json.load(f)
geo_ids = set(f['properties']['id'] for f in geo['features'])
for feat in geo['features']:
    for a in feat['properties'].get('aliases', []):
        geo_ids.add(a)
non_cartografici = {'tutta_isola_quattro_quartieri_attraversati'}
missing = graph_ids - geo_ids - non_cartografici
print('MISSING:', missing) if missing else print('OK backward-compat 100%')
"
```

Se manca qualche ID, **risolvi prima di qualsiasi altra cosa**.

### Principio 2 — Status corretto delle feature

Ogni feature ha `status`:
- **`canonico`** — fissato da Bible o grafo storie. Non si cambia mai, solo si sposta se si scopre una posizione migliore (e con nota in CHANGELOG).
- **`provvisorio`** — inferito dalla cartografia. Può cambiare.
- **`stub`** — menzionato ma non realmente posizionato.

**Non promuovere da `provvisorio` a `canonico` senza una fonte canonica** (Bible, grafo, decisione esplicita di Ray). Se vuoi promuoverlo, flaggalo nel CHANGELOG come domanda, non come fatto.

### Principio 3 — Commit atomici e CHANGELOG

Ogni modifica significativa:
1. Descrivi cosa cambia in `cartografia/CHANGELOG.md` con data e nuova versione.
2. Bump versione in `cartografia/geo/island.geojson` → `metadata.version`.
3. Commit con messaggio chiaro (`feat:`, `fix:`, `docs:`, `refactor:`).

### Principio 4 — Nomi e convenzioni

- ID: `snake_case` italiano, senza articoli, senza accenti. Vedi `cartografia/convenzioni/convenzioni_id.md`.
- Nomi visualizzati (`properties.name`): con maiuscole, accenti, apostrofi canonici.
- Lingua documenti: italiano.

---

## 2. Task tipici

### Task A — Nuova storia arrivata (S9-S12 e oltre)

Quando Ray aggiorna `pipeline_narrativa/story_graph.json`:

1. **Diff** vecchio vs nuovo: trova storie aggiunte e location nuove.
2. Per ogni location nuova: verifica che ne esista feature nel GeoJSON. Se no, chiedi a Ray di confermare posizione approssimata prima di crearla.
3. Per ogni storia nuova: leggi `premise`, `problem`, `threshold_moment`, `resolution_mode`, `visual_anchors`, e cerca riferimenti geografici impliciti (nomi di luogo, distanze, tempi di cammino, direzioni). Confronta con cartografia.
4. Se emergono **punti narrativi nuovi con peso canonico** (es. un albero specifico, un masso, una curva del Fiume), proponi di aggiungerli come landmark dedicati.
5. Se emergono **sentieri impliciti** non ancora mappati, proponi `sentiero_xxx_yyy` con status appropriato (`canonico` se giustificato dalla storia, `provvisorio` se inferito).
6. **NON tocchi il grafo.** Riferimenti, `pickup_history`, ecc. li gestisce Ray.
7. CHANGELOG entry con bump MINOR.

### Task B — Compilazione scheda luogo dettagliata

1. Prendi `cartografia/luoghi/_template_scheda.md`, duplica in `cartografia/luoghi/<quartiere>/<id>.md`.
2. Compila sezioni partendo da: Bible, grafo storie, apparato (come giacimento), note GeoJSON.
3. Sezioni non applicabili: **eliminale**, non lasciare vuote.
4. Dove non hai dati: scrivi `[da definire]` e registra come domanda aperta in sezione "Note e decisioni aperte".
5. Non inventare dettagli. Se la Bible non dice di che materiale è il tetto del Forno, non decidere tu — scrivilo come domanda aperta.

### Task C — Verifica coerenza geografica

Quando ti viene chiesto "questa storia/scena può avvenire qui?":

1. Estrai dall'input coordinate, ID luoghi, riferimenti direzionali, distanze.
2. Usa `cartografia/verifica_luogo.py` per trovare cosa c'è intorno.
3. Verifica:
   - L'ID esiste nel GeoJSON (direttamente o via alias)?
   - Le distanze dichiarate sono compatibili con la geometria?
   - I tempi di cammino sono coerenti (stima velocità: bambino 5 anni ~2-3 km/h, adulto ~4-5 km/h)?
   - Le direzioni sono coerenti (nord/sud/est/ovest)?
   - I dettagli del luogo (quartiere, tipo, altitudine) sono coerenti con l'azione?
4. Rispondi con: OK / Problema rilevato + dettaglio / Ambiguità da chiarire.

### Task D — Proposta sentiero nuovo (inferenza urbanistica)

Se vuoi proporre un sentiero:
1. Verifica che non esista già (nome, tracciato, funzione).
2. Verifica che **i due endpoint siano luoghi canonici** (non inventi punti nuovi solo per giustificare il sentiero).
3. Status: **`provvisorio`** se inferito, **`canonico`** solo se esplicitamente indicato da storia o Bible.
4. Categoria appropriata (vedi `cartografia/convenzioni/convenzioni_id.md` e le categorie usate in GeoJSON).

---

## 3. Domande specifiche da fare a Ray (cartografo)

(Oltre a quelle comuni in `skills/README.md` §6:)

- "La posizione che avevi in mente per X è Y? Ho stimato da Z." (prima di aggiungere feature non triviale)
- "La storia nuova implica un luogo/sentiero nuovo: dove preferisci collocarlo?"
- "Posso usare un sub-agente per estrarre riferimenti geografici da S9-S12 senza saturare il contesto?" (delega esplorativa)

---

## 4. Comandi operativi utili

### Verifica coerenza grafo ↔ cartografia

```bash
python3 -c "
import json
with open('pipeline_narrativa/story_graph.json') as f:
    graph_ids = set(json.load(f)['entities']['locations'].keys())
with open('cartografia/geo/island.geojson') as f:
    geo = json.load(f)
geo_ids = set(f['properties']['id'] for f in geo['features'])
for feat in geo['features']:
    for a in feat['properties'].get('aliases', []):
        geo_ids.add(a)
missing = graph_ids - geo_ids - {'tutta_isola_quattro_quartieri_attraversati'}
print('MISSING:' if missing else 'OK:', missing or '100% coverage')
"
```

### Verifica luogo singolo

```bash
cd cartografia/
python3 verifica_luogo.py --id <id>
python3 verifica_luogo.py --coord <east_m> <north_m>
python3 verifica_luogo.py --geo <lon> <lat>
```

### Aprire il visualizzatore

Apri `cartografia/geo/viewer/index.html` in browser (o servire la directory con un web server locale se serve CORS).

---

## 5. Stato conosciuto e limiti attuali

### Cose che funzionano bene
- Mappa navigabile, 103 feature, 36 sentieri.
- Backward-compat 100% con grafo v0.10.0 (verificata 2026-04-25).
- Visualizzatore web con ricerca/dettaglio/filtri.
- Script di verifica coerenza.

### Cose da migliorare
- Le Vie principali convergono al centro esatto dell'Albero Vecchio (coord 4000, 3500). Urbanisticamente improprio: dovrebbero fermarsi al bordo della Piazza (raggio 12.5m). Fix: v0.6, ~6 modifiche al GeoJSON.
- Le isole all'orizzonte SE/SO hanno posizioni molto arbitrarie. Da riconsiderare se diventano canoniche in Fase F.
- Il Braccio Est del Fiume è canonico come geometria generale ma silente narrativamente — se una storia futura lo tocca, probabilmente va spezzato in sotto-tratti.
- Fascia costiera NORD dichiarata inaccessibile (oltre la Sorgente). Può cambiare se il canone narrativo lo richiede.
- Le schede luogo dettagliate (in `cartografia/luoghi/*/`) **non sono ancora state compilate**. C'è solo il template.

### Debiti noti
- Sorgente: nome operativo. Ray definirà nome canonico in altra sede. Aggiornare alias quando deciso.
- Alcuni punti canonici del Villaggio (Pozzo, Panca, Cespuglio) hanno posizioni basate su inferenza da apparato. Da validare contro storie S1-S8 a una rilettura approfondita.

---

## 6. Esempio di sessione tipo

**Ray:** "È arrivata S9. Ecco il nuovo story_graph.json. Verifica coerenza."

**Tu:**
1. Leggi `skills/README.md`, `skills/cartografo.md`, `cartografia/CHANGELOG.md`.
2. Diff grafo vecchio vs nuovo. Trovi storia S9 aggiunta, eventuali location nuove.
3. Verifichi backward-compat. Se MISSING, segnali e chiedi a Ray.
4. Se ID nuovi sono varianti di luoghi esistenti, proponi `aliases` o `children`.
5. Leggi `premise`/`problem`/`resolution_mode`/`visual_anchors` di S9, estrai riferimenti geografici impliciti (può essere delegato a sub-agente per non saturare contesto), confronta con cartografia.
6. Proponi a Ray: nuove feature, nuovi sentieri, promotion `provvisorio` → `canonico`. Niente è auto-applicato.
7. Ray conferma → aggiorni GeoJSON, verifichi, commit, CHANGELOG entry, version bump.
8. Esegui validazioni generali (`verifica_luogo.py` per punti chiave S9), riporti a Ray.

Fine sessione.

---

**Ultimo aggiornamento:** 2026-04-25
