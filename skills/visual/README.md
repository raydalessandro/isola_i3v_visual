# skill: visual

**Scope:** costruisci e mantieni il **serbatoio di descrizioni visive** di tutte le entità della saga (personaggi, luoghi, oggetti, venti, visual_signatures), con immagini di riferimento per modelli generativi e per stampa 3D. La repo `visual/` è la **fonte unica** per tutto ciò che è visivo: IA generative, illustrazioni di riferimento, modelli 3D, descrizioni per narrativa e campagne social.

**Scrivi in:** `visual/` (tutto), `scripts/` (tool condivisi). **Non tocchi:** `cartografia/`, `pipeline_narrativa/`, file di radice (a meno che il task non lo richieda esplicitamente).

**Premessa:** prima di operare, leggi sempre `skills/README.md` per le **regole comuni**.

---

## Sotto-skill della famiglia visual

La skill visual si articola in sotto-skill specializzate per fasi operative. Quando un task ricade in una fase precisa, indossa la sotto-skill corrispondente e segui il suo file.

| Sotto-skill | File | Scope operativo |
|---|---|---|
| **compilatore** | [`compilatore.md`](./compilatore.md) | Compila il body delle schede entità da fonti canoniche; completa i vuoti con inferenza marcata. |
| _(futuro)_ prompter | _(da creare)_ | Genera prompt operativi per IA generative a partire dalle schede. |
| _(futuro)_ generatore_immagini | _(da creare)_ | Cura immagini di riferimento (4 vedute 3D + variazioni IA). |

Aggiungi nuove sotto-skill solo quando servono effettivamente. Niente sovrapproduzione.

---

## 1. Struttura `visual/`

Ogni entità è una **cartella autocontenuta** con `scheda.md` + `immagini/` + eventuali file di espansione (prompt dedicati, varianti, riferimenti). I luoghi seguono una **struttura frattale** che rispecchia la geografia dell'isola (quartiere → luogo → sotto-luoghi).

```
visual/
├── README.md                      come usare il serbatoio
├── _template_scheda.md            template scheda
├── catalogo.md                    indice generato (rieseguibile)
│
├── personaggi/
│   ├── individuali/
│   │   ├── bambini/               (3) gabriel, elias, noah
│   │   ├── primari/               (6) fiamma, bartolo, rovo, stria, memolo, grunto
│   │   ├── cuccioli/              (5) pun, toba, bru, cardo, liu
│   │   └── secondari/             (4) salvia, nodo, amo, zolla
│   └── collettivi/                (5) coltivatori_del_cerchio, mercato_del_mezzogiorno,
│                                  mantenitori, camminanti, pastori
│
├── luoghi/                        ← FRATTALE per quartiere
│   ├── villaggio_centrale/        (centro)
│   │   ├── piazza_villaggio/
│   │   │   ├── albero_vecchio/
│   │   │   │   ├── panca_di_pietra/
│   │   │   │   └── cespuglio_dietro_albero_vecchio/
│   │   │   └── pozzo_piazza/
│   │   ├── scuola_stria/
│   │   ├── via_scuola/
│   │   └── casa_memolo_cortile/
│   ├── quartiere_terra/
│   │   ├── orti_del_cerchio/
│   │   ├── via_degli_orti/
│   │   ├── casa_salvia/
│   │   ├── casa_zolla/
│   │   └── foresta_intrecciata/
│   │       ├── radura_dei_pini/
│   │       ├── tana_rovo/
│   │       ├── torrente_affluente_foresta/
│   │       └── zona_di_lavoro_salvia/
│   ├── quartiere_fuoco/           forno, case_del_mattino, via_dell_alba
│   ├── quartiere_acqua/           pontile_bocca, bocca, spiaggia_conchiglie,
│   │                              casa_amo, case_basse_pescatori, via_del_pontile
│   ├── quartiere_aria/            pascoli_alti, roccia_alta, montagne_gemelle,
│   │                              burrone/grotta_grunto, via_che_sale
│   └── perimetro/
│       ├── fiume_che_gira/        + 6 sotto-tratti come sotto-cartelle
│       │                          (capo, braccio_ovest_alto/medio/basso, stretta_due_massi,
│       │                          braccio_est, guado_di_pietre_piatte)
│       ├── fascia_costiera/
│       └── strade/                strade perimetrali / inter-quartiere lunghe
│
│   <quartiere>/strade/            in OGNI quartiere: cartella per le strade
│                                  secondarie del quartiere (sentieri, viottoli).
│                                  Le 5 Vie principali (via_dell_alba/del_pontile/
│                                  degli_orti/che_sale/scuola) sono in entities.locations
│                                  del grafo, quindi paritetiche con i landmark — NON
│                                  in strade/. Per panoramica veloce: visual/luoghi/
│                                  _strade_index.md (auto-generato).
│
├── oggetti/                       (13) flat
├── venti/                         (3) flat — taglio, intreccio, mulinello
├── visual_signatures/             (1) quando_acqua_trema
└── sito/                          static site (futuro)
```

**Conteggio attuale:** 112 schede totali (23 personaggi + 41 luoghi + **31 strade** + 13 oggetti + 3 venti + 1 visual_signature). Le strade vivono in `<quartiere>/strade/<id>/` (basate sul campo `quarter` del GeoJSON); le **5 Vie principali** in `entities.locations` del grafo restano paritetiche con gli altri luoghi del rispettivo quartiere. Per consultazione veloce: `visual/luoghi/_strade_index.md`.

**Per le strade nel frontmatter** lo script aggiunge metadati specifici (`lunghezza_m_local`, `n_punti`, `endpoint_a_m`, `endpoint_b_m`, `endpoints_inferiti_dal_id`, `categoria_strada`).

**Avvertenza nesting:** strade che attraversano più quartieri restano alla cartella indicata da `quarter` GeoJSON (tipicamente `perimetro`). Se in futuro l'organizzazione diventa scomoda, valutiamo lo split per tratti.

**Cartella entità — contenuto canonico:**
```
<entita>/
├── scheda.md          frontmatter YAML + descrizione strutturata (italiano)
├── immagini/          riferimenti generati: viste IA + 4 vedute per stampa 3D
└── (opzionale)        prompt dedicati, varianti, materiale di espansione
```

---

## 2. Schema `scheda.md`

Frontmatter YAML strutturato (derivato da `pipeline_narrativa/story_graph.json` + `cartografia/geo/island.geojson`) + corpo Markdown a sezioni.

**Campi frontmatter sempre presenti:**
- `id`, `name`, `famiglia` (personaggio | luogo | oggetto | vento | visual_signature), `sottotipo`, `status`, `ultima_modifica`, `fonti` (lista citazioni puntuali con path + ancora), `appare_in_storie`.

**Campi specializzati:**
- Personaggio: `specie`, `tipo_grafo`, `ruolo_saga`, `relazioni.{dimora, quadrante_grafo, related_to, cross_skill.cartografia}`.
- Luogo: `quartiere`, `cartografia.{feature_id, type_geo, status_geo, quarter, category, centroid_m_local, bbox_m_local, size_m_local, altitudine_m, geometry_type, parent_geo, children_geo, aliases_geo}`. Quando l'altitudine viene aggiunta al GeoJSON, basta rilanciare lo script di scaffolding e i frontmatter si aggiornano.
- Oggetto: `relazioni.{associato_a_personaggio, associato_a_luogo}`.

**Sezioni body** (14 sezioni; popolamento meccanico Bible→catalogo — vedi sotto-skill `compilatore.md`. Sezioni non coperte dalla Bible restano con placeholder uniforme `_da popolare dal grafo_`, da completare a posteriori da Ray):
1. Identità visuale (sintesi)
2. Aspetto / forma
3. Abbigliamento / stato d'uso
4. Espressione / comportamento
5. Palette e atmosfera
6. Contesto e ambientazioni ricorrenti
7. Coerenza cross-scena (cose che NON cambiano)
8. Variabilità ammessa
9. Cliché da evitare (riferimento a `PATTERN_AI_DA_BANDIRE_v1.md`)
10. Per stampa 3D (volumi, proporzioni, scala, orientamento)
11. Per narrativa e social (registri d'uso testuale)
12. Storie / scene di apparizione
13. Disallineamenti / domande aperte
14. Riferimenti puntuali (citazioni dirette dalle fonti)

**Stati delle schede:** `stub` (header compilato, body vuoto), `provvisorio` (body popolato, in revisione), `canonico` (approvato da Ray).

---

## 3. Principi non negoziabili (specifici visual)

### Principio 1 — Niente prompt-string pronti

Non scriviamo prompt-string per IA generative come asset principale. Le schede contengono **descrizioni ricche e strutturate** che servono come **fonte** per costruire prompt al volo per qualsiasi modello (BFL FLUX, Grok, altro), per stampa 3D, e per narrativa/social. Se in futuro un'entità ha bisogno di un prompt dedicato per uno specifico modello, lo si mette nella sua cartella come file separato (es. `gabriel/prompt_flux.md`) — **non** sostituisce la scheda.

### Principio 2 — Gerarchia delle fonti (visual)

In conflitto fra fonti, **tendenzialmente prevale il grafo storie** (`pipeline_narrativa/story_graph.json`). Bible e altri documenti restano fonti primarie ma il grafo è il riferimento operativo più recente. Disallineamenti grafo↔Bible sono **debito tecnico noto** (Ray gestisce fuori repo); valutare caso per caso senza decidere in autonomia su elementi narrativi sostanziali — segnalare a Ray nella sezione "Disallineamenti / domande aperte" della scheda.

### Principio 3 — Ogni dato visivo ha una fonte citata

Niente affermazioni visive senza ancora. La sezione "Riferimenti puntuali" deve contenere la citazione esatta (path + ancora YAML, es. `pipeline_narrativa/story_graph.json#entities.characters.gabriel`). Questo permette a `cartografo` di attingere alle stesse fonti per popolare la mappa, e mantiene auditability.

### Principio 4 — Niente cliché AI

Applica `PATTERN_AI_DA_BANDIRE_v1.md` anche in dominio visivo: niente "tramonto epico", "occhi che brillano di saggezza", "antico e magico" generico. Le descrizioni visive devono essere **specifiche e situate** sull'Isola, non template fantasy.

### Principio 5 — Coerenza con cartografia

Per i luoghi: il frontmatter porta i metadati cartografici (centroide, bbox, dimensioni, quartiere, parent/children). Il body non può contraddirli. Se descrivi una "casa piccola" ma il GeoJSON dice 200m², segnalalo come domanda aperta — non riscriverla.

### Principio 6 — Immagini di riferimento, non illustrazioni finali

Le immagini in `<entita>/immagini/` sono **riferimenti** per modelli e illustratori — non illustrazioni finali del libro. Per stampa 3D, ogni entità tridimensionale (personaggi, oggetti) avrà tipicamente **4 vedute** (fronte, retro, profilo dx, profilo sx). Convenzione di naming consigliata: `<id>_<vista>_<varianteN>.jpg` (o `.png`) (es. `gabriel_fronte_v1.jpg`).

---

## 4. Workflow tipici

### Task A — Bootstrap struttura (già fatto al 2026-04-25)

```bash
python3 scripts/build_visual_skeleton.py
```

Lo script è **idempotente**:
- Crea cartelle e schede mancanti.
- Su schede esistenti, **rigenera solo il frontmatter** (derivato da fonti) e **preserva il body** (lavoro umano/agenti).
- Rigenera `visual/catalogo.md`.

### Task B — Compilare body schede (travaso meccanico)

Approccio: una famiglia per volta. Una entità per volta.

Per ogni entità l'agente (vedi `compilatore.md` per dettaglio):
1. Legge `scheda.md` esistente (frontmatter già popolato, body stub).
2. **Travasa dalla Bible** i campi che corrispondono alle sezioni del template (mappa Bible→catalogo in `compilatore.md` §3-3bis).
3. **Sezioni non coperte dalla Bible:** scrive `_da popolare dal grafo_` come unico contenuto. Niente inferenze, niente proposte.
4. **"Storie / scene di apparizione":** lista automatica dal grafo (deterministico, non inferenza).
5. **Riferimenti puntuali:** cita ogni dato canonico riportato (path + ancora).
6. **Disallineamenti:** segnala conflitti senza risolverli.
7. Stato: passa da `stub` a `provvisorio` (auto-inferito dallo script al rilancio).

### Task C — Generare immagine di riferimento

1. Scrivi prompt completo a partire dalla scheda (compositing dei campi descrittivi).
2. Genera con il modello scelto.
3. Salva in `<entita>/immagini/` con metadati (file `<id>_<vista>_<varianteN>.jpg` (o `.png`) + opzionale `<id>_<vista>_<varianteN>.meta.md` con prompt usato, modello, seed, data, stato).

### Task D — Aggiornare metadati cartografici

Quando il GeoJSON viene aggiornato (es. arriva l'altitudine):
```bash
python3 scripts/build_visual_skeleton.py
```
I frontmatter delle schede luogo si rigenerano automaticamente. Body preservato.

### Task E — Aggiornare il sito interno (futuro)

Tecnologia da decidere. Probabile static site che legge `visual/catalogo.md` + le schede e produce navigazione per famiglia/quartiere/sottotipo + viewer immagini.

---

## 5. Pattern di rifiuto (specifici visual)

Oltre alle regole comuni in `skills/README.md` §5, **rifiuta** se la richiesta:
- Ti chiede di modificare la cartografia per giustificare una scelta visual → vai in skill cartografo o segnala a Ray.
- Ti chiede di scrivere prosa narrativa o riformulare seed/callback.
- Ti chiede di pubblicare immagini come illustrazioni finali del libro (la pipeline finale è altro flusso, fuori scope di questa skill).

---

## 6. Domande specifiche da fare a Ray (visual)

- "Il modello generativo target per questa entità è X o Y? Workflow?"
- "Per i sotto-tratti del Fiume e gli altri elementi cartografici non in `entities.locations` (es. `radura_dei_pini`), li promuovo a entità grafo o restano carto-only?"
- "Per le immagini di riferimento: quale percentuale di coerenza dobbiamo raggiungere prima di considerare un personaggio 'fissato'?"
- "Per le 4 vedute 3D: convenzione fronte/retro/profilo dx/profilo sx ti va, o preferisci altre angolature canoniche?"

---

**Ultimo aggiornamento:** 2026-04-25.
