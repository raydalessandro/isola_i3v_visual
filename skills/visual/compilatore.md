# sotto-skill: compilatore (visual)

Specializzazione operativa della **skill visual**. Compila il *body* delle schede entità (`visual/<famiglia>/.../<id>/scheda.md`) tramite **travaso meccanico** dalla Bible (e dal grafo per la sezione "Storie di apparizione"). Non inferisce, non propone: lascia placeholder uniforme dove la fonte non copre.

**Premessa:** prima di operare leggi:
1. `skills/README.md` (regole comuni: isolamento `pipeline_narrativa/` read-only, comunicazione, gerarchia fonti).
2. `skills/visual/README.md` (skill visual: struttura, schema scheda, vincoli).
3. Questo file.

---

## 1. Scope di scrittura

Solo: `visual/<famiglia>/.../<id>/scheda.md`, modificando esclusivamente il **body** sotto il secondo `---`. Il frontmatter è gestito dallo script `scripts/build_visual_skeleton.py`: **non toccarlo**. Lo script preserva il body quando rigenera il frontmatter.

---

## 2. Principio fondamentale: travaso meccanico

**Tre regole:**

1. **Bible → catalogo, 1:1 dove i campi combaciano.** Copia o parafrasi diretta. Niente arricchimenti, niente inferenze, niente proposte stilistiche.
2. **Bible "in più" resta nella Bible.** I campi narrativi (Funzione narrativa, Voce tipica, archi narrativi, vincoli narrativi non visivi) **non si portano nel catalogo**. Bibbia + Grafo + Catalogo lavorano insieme; ognuno ha il suo ruolo.
3. **Sezioni del catalogo che la Bible non copre → placeholder uniforme `_da popolare dal grafo_`.** Saranno completate da Ray quando ragionerà sul grafo. La uniformità del placeholder serve a misurare a colpo d'occhio quanto è completa una scheda (e quanto manca) tramite `grep -c "_da popolare dal grafo_"`.

**Niente marcatori `[inf]`/`[prop]`** in queste schede meccaniche. Quei marcatori sono per l'autore in fase di ragionamento, non per la pipeline di travaso.

**Eccezione automatizzabile**: la sezione **"Storie / scene di apparizione"** è derivabile in modo deterministico dal grafo (lista degli `s01..s12` dove l'entità compare). La popolo dal grafo, non è inferenza.

---

## 3. Mappa Bible (§4 personaggi) → template catalogo

| Sezione catalogo | Fonte Bible (§4 personaggio) | Trattamento |
|---|---|---|
| Identità visuale (sintesi) | — | `_da popolare dal grafo_` |
| Aspetto / forma | "Aspetto." | Travaso 1:1 |
| Abbigliamento / stato d'uso | "Aspetto." (parte abbigliamento, se presente) | Travaso se presente, altrimenti `_da popolare dal grafo_` |
| Espressione / comportamento | "Comportamento operativo." | Travaso 1:1 |
| Palette e atmosfera | — | `_da popolare dal grafo_` |
| Contesto e ambientazioni ricorrenti | "Specie, ruolo." (se nomina luoghi) + "Comportamento operativo." (se nomina luoghi) | Travaso parziale se presente, altrimenti `_da popolare dal grafo_` |
| Coerenza cross-scena (cose che NON cambiano) | "Aspetto." (dettagli fisici fissi) | Travaso/derivazione 1:1 |
| Variabilità ammessa | — | `_da popolare dal grafo_` |
| Cliché da evitare | "Note e vincoli." (parte "Mai...") | Travaso 1:1 |
| Per stampa 3D | — | `_da popolare dal grafo_` |
| Per narrativa e social | — | `_da popolare dal grafo_` |
| Storie / scene di apparizione | `pipeline_narrativa/story_graph.json#stories.s0X.characters_in_scene` | Lista automatizzata dal grafo |
| Disallineamenti / domande aperte | — | Vuoto, salvo conflitti rilevati |
| Riferimenti puntuali | meta | Citazioni precise (path + ancora) di tutti i dati canonici riportati |

**NON portati nel catalogo (restano in Bible):**
- "Funzione narrativa." → strutturale, vive nel grafo + Bible.
- "Voce tipica." → narrativa.
- "Note e vincoli." parte non-cliché (es. "in 2-3 storie su 12 fa il punzecchio") → vincoli narrativi.
- "Funzione narrativa" estesa (es. "frizione necessaria") → impianto saga.

## 3-bis. Mappa Bible (§2 geografia) → template catalogo luoghi

| Sezione catalogo | Fonte Bible (§2) | Trattamento |
|---|---|---|
| Identità visuale (sintesi) | — | `_da popolare dal grafo_` |
| Aspetto / forma | descrizione fisica del luogo | Travaso 1:1 |
| Abbigliamento / stato d'uso | non applicabile (luogo) | `_da popolare dal grafo_` |
| Espressione / comportamento | dinamica (es. "vento che soffia da nord", "marea") | Travaso se presente, altrimenti `_da popolare dal grafo_` |
| Palette e atmosfera | — | `_da popolare dal grafo_` |
| Contesto | uso, abitanti, attività | Travaso 1:1 se presente |
| Coerenza cross-scena | dettagli fisici fissi | Travaso 1:1 |
| Variabilità ammessa | variazioni stagionali/temporali | Travaso se presente, altrimenti `_da popolare dal grafo_` |
| Cliché da evitare | — (raro per luoghi) | `_da popolare dal grafo_` salvo trovato |
| Per stampa 3D | — | `_da popolare dal grafo_` |
| Per narrativa e social | — | `_da popolare dal grafo_` |
| Storie | dal grafo | Lista automatizzata |
| Disallineamenti | — | Vuoto, salvo conflitti |
| Riferimenti puntuali | meta | Citazioni |

I luoghi hanno anche metadati cartografici nel frontmatter (centroide, bbox, dimensioni) gestiti dallo script.

---

## 4. Workflow per una scheda (un'entità per volta)

### Step 1 — Identifica entità

Prendi `id`, `famiglia`, `sottotipo` dal frontmatter della scheda.

### Step 2 — Estrazione mirata

Per personaggi:
```bash
# Anagrafica grafo
python3 -c "
import json
g = json.load(open('pipeline_narrativa/story_graph.json'))
print(json.dumps(g['entities']['characters']['<id>'], ensure_ascii=False, indent=2))
"

# Apparizioni nelle storie
python3 -c "
import json
g = json.load(open('pipeline_narrativa/story_graph.json'))
for sid, s in g['stories'].items():
    for c in s.get('characters_in_scene', []):
        if isinstance(c, dict) and c.get('id') == '<id>':
            print(sid, '->', c.get('scene_role') or c.get('role') or '?')
"

# Sezione Bible
grep -n -A 40 '<NOME>$' pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md
```

Per luoghi: leggi `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §2 e cerca il toponimo.

**Regola di lettura:** leggi solo quello che serve a questa entità. Niente esplorazioni dispersive.

### Step 3 — Travaso

Per ogni sezione del template:
- Cerca il campo Bible corrispondente (vedi mappa §3 / §3-bis sopra).
- Se trovi: **copia o parafrasa fedelmente**.
- Se non trovi: scrivi esattamente `_da popolare dal grafo_` come unico contenuto della sezione.
- Per "Storie / scene di apparizione": elenca le storie dal grafo, una riga ciascuna con il ruolo della scena. Esempio:
  - `s06: cammeo, frrr di apertura ("liu_frrr_messaggera_non_veggente_una_frase_breve")`.

### Step 4 — Riferimenti puntuali

Sezione finale obbligatoria. Per ogni dato canonico riportato sopra, una citazione con path + ancora YAML/sezione. Esempio:

```
- `ISOLA_TRE_VENTI_BIBLE_v2.md` §4.17: "Libellulina. Genitori non in scena..."
- `pipeline_narrativa/story_graph.json#entities.characters.liu`: `species: libellulina`, `role_saga: presenza_aerea_discreta`.
- `pipeline_narrativa/story_graph.json#stories.s12.visual_anchors.scene_hooks[0]`: "liu_appena_volata_via_frrr_oggi_suonano..."
```

### Step 5 — Disallineamenti

Se durante il travaso rilevi conflitti Bible vs grafo, ambiguità di nome (es. "Liù" Bible vs `liu` grafo), apparizioni dichiarate ma non documentate: **registra senza risolvere**. Ray valida in fase di ragionamento sul grafo.

### Step 6 — Stato compilazione

In cima al body, subito dopo `# <Nome>`:

```
> **Stato compilazione:** body provvisorio, generato dal travaso meccanico Bible→catalogo il YYYY-MM-DD. Le sezioni con `_da popolare dal grafo_` saranno completate da Ray quando ragionerà sul grafo.
```

### Step 7 — Frontmatter

Non toccare. Lo script `build_visual_skeleton.py` lo rigenera da grafo + GeoJSON, e auto-inferisce `status`:
- Body con sole righe `[stub …]` → `stub`.
- Body popolato (anche con `_da popolare dal grafo_`) → `provvisorio`.
- `canonico` rispettato se già impostato (Ray promuove manualmente).

---

## 5. Vincoli operativi

- **Italiano**, prosa fedele alla Bible.
- **Niente prompt-string pronti** per modelli specifici. Le sezioni descrittive sono fonte multi-uso.
- **Tendenzialmente la verità è nel grafo** — ma in fase di travaso, la Bible è la fonte primaria del visual perché è l'unico documento che ne parla in modo descrittivo. Se grafo e Bible contraddicono, segnala in "Disallineamenti".
- **Niente improvvisazione**: se la Bible non dice una cosa, NON la inventi. Placeholder.
- **Una entità per volta**.

---

## 6. Esempio canonico

`visual/personaggi/individuali/cuccioli/liu/scheda.md` — caso pilot del metodo meccanico (libellulina, Bible §4.17 ricca, sezioni non coperte → placeholder uniforme).

---

## 7. Disclaimer su tempi e contesto

- Il workflow richiede lettura mirata e attenzione al budget di contesto.
- Per task massivi (>10 entità) preferire la chat con la zip del repo allegata, dove l'operatore lavora a contesto unificato senza vincoli di durata.
- In Claude Code, batch suggerito: 4-6 schede per sessione, con commit dopo ogni batch.

---

**Ultimo aggiornamento:** 2026-04-26 — versione "metodo meccanico" (sostituisce la versione "completa con inferenza marcata").
