# DOC 5 — Index sentieri navigabile

> **Scopo.** Indice bidirezionale `storia ↔ sentiero` pensato per il brieffer (lo script che monta il writing_brief per l'agente prosa). Per ogni sentiero, le storie in cui appare già marcate; per ogni storia, i sentieri attraversati. I micro-dettagli stabili saranno aggiunti **uno per appariazione**, distribuiti nelle storie del sentiero, in modo che ogni passaggio porti con sé un solo dettaglio del mondo.
>
> **Logica narrativa.** Pochi dettagli, ben distribuiti = effetto di mondo ultra-dettagliato. Un sentiero Tier A che appare in 6 storie avrà 4-6 dettagli stabili — ma il bambino li scopre uno per volta, una storia alla volta. Alla terza rilettura, riconosce il dettaglio.
>
> **Stato:** indice pronto + slot vuoti per dettagli (da popolare nella prossima sessione "mercato delle idee").

---

## §1. Indice inverso `sentiero → storie` (con tier)

| Sentiero | Tier | Storie | Già nel grafo |
|---|---|---|---|
| `via_dell_alba` | **A** | s06, s08, s09, s10, s11, s12 | s06, s09 (parz.) |
| `sentiero_orti_torrente_foresta` | **A** | s03, s04, s05, s11 | — |
| `via_che_sale` | **A** | s01, s02, s11, s12 | — |
| `sentiero_orti_casa_salvia` | **A** | s04, s06, s09 | — |
| `viottolo_perimetrale_piazza` | **A** | s08, s10, s11 | — |
| `sentiero_al_guado` | **B** | s07, s12 | — |
| `sentiero_capanne_pastori_pascoli` | **B** | s02, s12 | — |
| `sentiero_foresta_traversata_ovest` | **B** | s05, s12 | — |
| `sentiero_forno_orti_diretto` | **B** | s06, s11 | — |
| `sentiero_fuoco_ring` | **B** | s08, s11 | — |
| `sentiero_montagne_gemelle` | **B** | s01, s12 | s01 |
| `sentiero_riva_ovest` | **B** | s07, s12 | — |
| `viottolo_piazza_casa_memolo` | **B** | s06, s09 | — |
| `sentiero_casa_salvia_casa_zolla` | **C** | s06 | — |
| `sentiero_case_basse_bocca` | **C** | s07 | — |
| `sentiero_orti_casa_zolla` | **C** | s06 | — |
| `sentiero_pascoli_burrone_diretto` | **C** | s12 | — |
| `sentiero_pontile_forno` | **C** | s10 | — |
| `sentiero_pontile_spiaggia` | **C** | s07 | — |
| `sentiero_ritorno_bocca_orti` | **C** | s07 | — |
| `via_degli_orti` | **C** | s03 | s03 |
| `via_del_pontile` | **C** | s10 | s10 |
| `via_scuola` | **C** | s08 | s08 |

**Totale: 23 sentieri usati** · 5 Tier A · 8 Tier B · 10 Tier C
**Da aggiungere a `locations_secondary` del grafo: 19 sentieri** (4 sono già parzialmente dichiarati)

---

## §2. Indice diretto `storia → sentieri`

Per il brieffer: dato un `sid`, ritorna i sentieri attraversati, con tier e numero atteso di dettagli da pescare.

### S01 — La Nebbia delle Montagne Gemelle
- `via_che_sale` [Tier A] — salita iniziale dal villaggio ai Pascoli
- `sentiero_montagne_gemelle` [Tier B] — cengia di mezzacosta verso Grunto

### S02 — Il Riflesso nella Pozza
- `via_che_sale` [Tier A] — salita ai Pascoli
- `sentiero_capanne_pastori_pascoli` [Tier B] — sui Pascoli, dalla via alla pozza/radura

### S03 — Il Pallone oltre la Foresta
- `via_degli_orti` [Tier C] — uscita verso gli Orti del Cerchio
- `sentiero_orti_torrente_foresta` [Tier A] — dagli Orti al margine Foresta

### S04 — Le Radici che Parlano
- `sentiero_orti_casa_salvia` [Tier A] — passaggio per casa Salvia
- `sentiero_orti_torrente_foresta` [Tier A] — al margine Foresta

### S05 — Il Ponte di Rami
- `sentiero_orti_torrente_foresta` [Tier A] — entrata in Foresta con Bru
- `sentiero_foresta_traversata_ovest` [Tier B] — dopo il ponte, verso la Radura dei Pini

### S06 — Il Dono per Mèmolo
- `via_dell_alba` [Tier A] — Piazza → Forno
- `sentiero_forno_orti_diretto` [Tier B] — Forno → Orti
- `sentiero_orti_casa_salvia` [Tier A] — Orti → casa Salvia
- `sentiero_casa_salvia_casa_zolla` [Tier C] — Salvia → Zolla
- `sentiero_orti_casa_zolla` [Tier C] — Zolla → Piazza
- `viottolo_piazza_casa_memolo` [Tier B] — Piazza → casetta tonda

### S07 — La Zattera dei Tre Rametti
- `sentiero_al_guado` [Tier B] — discesa al guado nord
- `sentiero_riva_ovest` [Tier B] — riva interna del Fiume in discesa
- `sentiero_ritorno_bocca_orti` [Tier C] — Bocca → Orti (ritorno)
- `sentiero_case_basse_bocca` [Tier C] — verso Pontile
- `sentiero_pontile_spiaggia` [Tier C] — vista delle conchiglie

### S08 — L'Albero che Cadde di Sera
- `via_dell_alba` [Tier A] — Forno → margine piazza
- `viottolo_perimetrale_piazza` [Tier A] — verso il Pozzo
- `via_scuola` [Tier C] — la chioma cade di traverso qui
- `sentiero_fuoco_ring` [Tier B] — convergenza Mantenitori

### S09 — Quel Pomeriggio di Ottobre
- `via_dell_alba` [Tier A] — Scuola → Forno; Casa → Forno (sera)
- `sentiero_orti_casa_salvia` [Tier A] — Mèmolo che gira
- `viottolo_piazza_casa_memolo` [Tier B] — Mèmolo → casa

### S10 — La Notte senza Luna
- `viottolo_perimetrale_piazza` [Tier A] — Casa fratelli → Piazza
- `sentiero_pontile_forno` [Tier C] — discesa
- `via_del_pontile` [Tier C] — discesa lunga al Pontile
- `via_dell_alba` [Tier A] — risalita all'alba

### S11 — La Festa del Raccolto
- `via_che_sale` [Tier A] — Pastori in discesa
- `via_dell_alba` [Tier A] — Bartolo in salita
- `sentiero_orti_torrente_foresta` [Tier A] — Bru/Rovo
- `sentiero_forno_orti_diretto` [Tier B] — Coltivatori scendono coi sacchi
- `sentiero_fuoco_ring` [Tier B] — Camminanti vanno-vengono
- `viottolo_perimetrale_piazza` [Tier A] — circolazione festa

### S12 — Quando i Tre Venti Suonano Insieme
- `via_dell_alba` [Tier A] — Casa → Forno → Pontile
- `sentiero_riva_ovest` [Tier B] — risalita lungo Fiume
- `sentiero_al_guado` [Tier B] — al guado nord
- `sentiero_foresta_traversata_ovest` [Tier B] — Guado → Radura
- `sentiero_capanne_pastori_pascoli` [Tier B] — Radura → Pascoli
- `sentiero_pascoli_burrone_diretto` [Tier C] — Pascoli → Burrone
- `sentiero_montagne_gemelle` [Tier B] — Burrone → Roccia Alta
- `via_che_sale` [Tier A] — discesa al ritorno

---

## §3. Slot dettagli — distribuzione attesa

Logica: **un dettaglio per appariazione**, mai due dettagli dello stesso sentiero nella stessa storia. Così il bambino che rilegge incontra il dettaglio "nuovo" della prima volta in s06, lo riconosce in s08, ha la sorpresa-conferma in s11.

### Tier A — 5 sentieri × ~5 dettagli = ~25 dettagli totali

| Sentiero | Storie | N. dettagli da inventare | Distribuzione attesa |
|---|---|---|---|
| `via_dell_alba` | s06, s08, s09, s10, s11, s12 | **6** (uno per storia) | s06: dettaglio_1 · s08: dettaglio_2 · s09: dettaglio_3 · s10: dettaglio_4 · s11: dettaglio_5 · s12: dettaglio_6 (può essere uno già visto, in chiusura) |
| `sentiero_orti_torrente_foresta` | s03, s04, s05, s11 | **4** | s03 prima volta · s04 si conferma · s05 evento (Bru fa scegliere) · s11 ritorno |
| `via_che_sale` | s01, s02, s11, s12 | **4** | s01 prima · s02 (variante: no nebbia) · s11 (Pastori) · s12 (chiusura) |
| `sentiero_orti_casa_salvia` | s04, s06, s09 | **3** | s04 prima · s06 giro tappe · s09 (Mèmolo lo percorre) |
| `viottolo_perimetrale_piazza` | s08, s10, s11 | **3** | s08 (drammatico) · s10 (notte) · s11 (festa) |

### Tier B — 8 sentieri × ~2 dettagli = ~16 dettagli totali

| Sentiero | Storie | N. dettagli |
|---|---|---|
| `sentiero_al_guado` | s07, s12 | **2** |
| `sentiero_capanne_pastori_pascoli` | s02, s12 | **2** |
| `sentiero_foresta_traversata_ovest` | s05, s12 | **2** |
| `sentiero_forno_orti_diretto` | s06, s11 | **2** |
| `sentiero_fuoco_ring` | s08, s11 | **2** |
| `sentiero_montagne_gemelle` | s01, s12 | **2** |
| `sentiero_riva_ovest` | s07, s12 | **2** |
| `viottolo_piazza_casa_memolo` | s06, s09 | **2** |

### Tier C — 10 sentieri × 1 dettaglio = 10 dettagli totali

Un dettaglio per sentiero, applicato all'unica storia in cui appare.

| Sentiero | Storia | N. dettagli |
|---|---|---|
| `sentiero_casa_salvia_casa_zolla` | s06 | 1 |
| `sentiero_case_basse_bocca` | s07 | 1 |
| `sentiero_orti_casa_zolla` | s06 | 1 |
| `sentiero_pascoli_burrone_diretto` | s12 | 1 |
| `sentiero_pontile_forno` | s10 | 1 |
| `sentiero_pontile_spiaggia` | s07 | 1 |
| `sentiero_ritorno_bocca_orti` | s07 | 1 |
| `via_degli_orti` | s03 | 1 |
| `via_del_pontile` | s10 | 1 |
| `via_scuola` | s08 | 1 |

**Totale dettagli da inventare: ~51**

---

## §4. Schema slot dettaglio (per il grafo)

Il singolo dettaglio sarà un oggetto:

```yaml
- id: vda_d01_aratro_arrugginito
  sentiero: via_dell_alba
  tipo: oggetto_anomalo  # oggetto_anomalo | albero_marcato | roccia_forma | pozza | suono | luce | piante
  what: "Un aratro vecchio, arrugginito, appoggiato a un muretto. Nessuno lo sposta da anni."
  where_along_path: "due terzi del percorso, lato destro salendo dalla piazza"
  visibility: "visibile sempre, ma di mattina presto la luce ci batte direttamente"
  appears_in_stories: [s06, s09, s12]
  perception_pattern: "s06 prima vista (Gabriel lo nota di sfuggita); s09 di sfondo (Mèmolo ci passa); s12 chiusura (i tre lo guardano un secondo prima di scendere)"
  notes: "esempio fittizio — da approvare/sostituire"
```

**Vincolo:** ogni dettaglio appare in **almeno 1 e al massimo N storie** del sentiero, dove N è il numero totale di storie del sentiero (Tier A può avere dettagli che ricorrono in 3 storie su 6, ad esempio).

---

## §5. Ricerca veloce per il brieffer

Quando l'agente prosa scriverà s07, il brieffer deve poter chiedere al grafo:

```
GET sentieri_attraversati(s07) -> [
  sentiero_al_guado,
  sentiero_riva_ovest,
  sentiero_ritorno_bocca_orti,
  sentiero_pontile_spiaggia,
  sentiero_case_basse_bocca
]
```

E per ognuno:

```
GET dettagli(sentiero_riva_ovest, in_story=s07) -> [
  { detail_id: ..., what: ..., where_along_path: ..., perception_pattern: ... }
]
```

Questa parte la implementeremo nello script `build_writing_brief.py` quando lo costruiremo. L'index di questo doc è la base.

---

## §6. Decisioni rimaste aperte

1. **Lo schema slot di §4 va bene?** In particolare il campo `perception_pattern` (chi nota cosa, in che storia) potrebbe essere troppo prescrittivo. Alternativa: lasciarlo libero e farlo decidere all'agente prosa nel momento.

2. **`tipo` del dettaglio** — i 7 tipi proposti (`oggetto_anomalo`, `albero_marcato`, `roccia_forma`, `pozza`, `suono`, `luce`, `piante`) coprono tutto? Suggerimenti aggiuntivi: `traccia_animale`, `incisione`, `vegetazione_anomala`, `microfauna_ricorrente` (lucciole, libellule, ecc.).

3. **Dettagli "evolventi"** — un dettaglio può cambiare tra storie? Esempio: l'aratro arrugginito di sopra è uguale in s06 e s09, ma in s12 è coperto di neve (è la chiusura della saga, prima brina). Suggerimento: campo `state_by_story` opzionale dentro lo slot, per ammettere variazioni stagionali/temporali.

4. **Tipo di dettaglio "incontro umano latente"** — non sempre un dettaglio è oggetto. Può essere "qui passa sempre Liù di traverso" o "qui di pomeriggio si sente sempre la cantilena dei Coltivatori da lontano". Aggiungere tipo `presenza_ricorrente` allo schema?

---

## §7. Prossimo passo

Quando approvi schema e distribuzione, andiamo al **mercato delle idee Tier A**: 25 dettagli candidati per i 5 sentieri Tier A, in tabella compatta. Tu scegli.

Poi Tier B (16 candidati), poi Tier C (10 candidati).

Totale 3 sessioni "mercato" di lunghezza decrescente.

Vai?
