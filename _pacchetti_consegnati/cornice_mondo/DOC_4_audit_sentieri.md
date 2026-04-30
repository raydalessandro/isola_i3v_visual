# DOC 4 — Audit del percorrere reale (Fase 1)

> **Scopo.** Mappare i sentieri/strade effettivamente percorsi dai tre fratelli nelle 12 storie, confrontandoli con quelli dichiarati nel grafo e con quelli esistenti nel catalogo schede. Identificare i sentieri prioritari da dettagliare e segnalare i sentieri "fantasma" (percorsi ma mai dichiarati nel grafo).
>
> **Stato:** audit operativo, propedeutico alla Fase 2 (dettaglio dei sentieri prioritari).

---

## §1. Sintesi numerica

| Categoria | Numero |
|---|---|
| Sentieri totali nel catalogo schede `visual/luoghi/.../strade/` | **37** |
| Sentieri presenti come entità in `entities.locations` del grafo | **6** |
| Sentieri **realmente percorsi** dai fratelli nelle 12 storie | **22** |
| Sentieri percorsi MA mai dichiarati nel grafo (fantasma) | **18** |
| Sentieri del catalogo MAI percorsi nelle 12 storie | **15** |
| Sentieri con scheda autoriale ≥80% piena | **0** |
| Sentieri con scheda autoriale 40-80% | **5** |
| Sentieri con scheda autoriale <40% (quasi vuote) | **32** |

**Lettura sintetica.** La cartografia tecnica è completa (geometria, endpoint, lunghezza per ogni sentiero). Le sezioni autoriali delle schede sono praticamente vuote ovunque. Il grafo dichiara solo 6 sentieri delle 12 storie ma in realtà i fratelli ne percorrono almeno 22.

---

## §2. Mappa per storia: tratti percorsi → sentiero (assegnazione manuale ragionata)

Per ogni storia, lista dei tratti A→B percorsi nella narrazione fattuale, e quale sentiero del catalogo li copre. Le assegnazioni sono basate su lettura incrociata di narrazione + endpoint cartografici + buon senso geografico, non sul match automatico (che produce falsi positivi).

**Legenda colonne:**
- ✓ = sentiero esiste nel catalogo, lo possiamo associare
- ⚠ = tratto percorso ma nessun sentiero del catalogo lo copre — bisogna decidere se aggiungerne uno o riusare uno esistente con tolleranza
- ◆ = sentiero già dichiarato in `locations_secondary` o `scene_hooks` del grafo

### S01 — La Nebbia delle Montagne Gemelle

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Forno → Piazza | (interno villaggio, no sentiero) | — |
| Piazza → Via che Sale | `via_che_sale` | no |
| Via che Sale → Pascoli Alti | `via_che_sale` (continua) | no |
| Pascoli Alti → cengia/Burrone | `sentiero_montagne_gemelle` ◆ | sì |
| Pascoli Alti → Grotta di Grunto | `sentiero_montagne_gemelle` ◆ | sì |

### S02 — Il Riflesso nella Pozza

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Scuola → Piazza | (centro villaggio, no sentiero canonico) | — |
| Piazza → Via che Sale → Pascoli Alti | `via_che_sale` | no |
| Pascoli Alti → Pozza | `sentiero_capanne_pastori_pascoli` (✓ buon match) | no |
| Pozza → Radura dei Pastori | (tratto interno Pascoli, eventualmente parte di `sentiero_capanne_pastori_pascoli`) | no |

### S03 — Il Pallone oltre la Foresta

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Casa fratelli → Orti del Cerchio | (interno villaggio o `via_degli_orti`) ◆ | sì |
| Orti → margine Foresta | `sentiero_orti_torrente_foresta` (✓ buon match) | no |

### S04 — Le Radici che Parlano

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Casa Salvia → Orti del Cerchio | `sentiero_casa_salvia_margine_foresta` (deviazione) o `sentiero_orti_casa_salvia` | no |
| Orti → margine Foresta | `sentiero_orti_torrente_foresta` | no |
| (interno Foresta — Noah segue farfalla, Gabriel cerca) | ⚠ no sentiero, è esplorazione fuori sentiero |

### S05 — Il Ponte di Rami

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Margine Orti → interno Foresta (con Bru) | `sentiero_orti_torrente_foresta` | no |
| Interno Foresta → Torrente | `sentiero_orti_torrente_foresta` (continua fino al torrente) | no |
| Tratto al margine dove lavora Nodo (50m a valle del ponte) | `sentiero_foresta_traversata_ovest`? o tratto del primo | no |
| Torrente (riva opposta) → Radura dei Pini | ⚠ tratto INTERNO Foresta non coperto da sentiero esistente, è il tratto post-ponte verso radura — eventualmente `sentiero_foresta_traversata_ovest` |

### S06 — Il Dono per Mèmolo

Storia con il giro più articolato del villaggio. Tratti molteplici.

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Scuola → Piazza | (centro, vicinissimi, no sentiero) | — |
| Piazza → Forno | `via_dell_alba` ◆ | sì |
| Forno → Orti | `sentiero_forno_orti_diretto` | no |
| Orti → Casa Salvia | `sentiero_orti_casa_salvia` | no |
| Casa Salvia → Casa Zolla | `sentiero_casa_salvia_casa_zolla` | no |
| Casa Zolla → Piazza/Mercato | `sentiero_orti_casa_zolla` (in senso inverso) | no |
| Piazza → Albero Vecchio (Panca) | (interno piazza, no sentiero) | — |
| Mercato → Casetta Mèmolo | `viottolo_piazza_casa_memolo` ◆ | (parzialmente) |

### S07 — La Zattera dei Tre Rametti

Lunga discesa lungo il Fiume. Sentieri di riva.

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Casa → Guado di pietre piatte (nord) | `sentiero_al_guado` | no |
| Guado → riva ovest del Fiume (discesa) | `sentiero_riva_ovest` (lungo la riva interna) | no |
| Riva ovest → margine Foresta | `sentiero_riva_ovest` (continua) | no |
| Margine Foresta → margine Orti | `sentiero_riva_ovest` (continua) | no |
| Margine Orti → Bocca | `sentiero_ritorno_bocca_orti` (in senso inverso) | no |
| Bocca → Pontile | `sentiero_case_basse_bocca` o `sentiero_pontile_case_basse` | no |
| Ritorno: Bocca → Orti del Cerchio (taglio diretto) | `sentiero_ritorno_bocca_orti` | no |

### S08 — L'Albero che Cadde di Sera

Pochi tratti, dramma in piazza.

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Forno → margine Piazza (s'avvia attraversata) | `via_dell_alba` (continua) | no |
| Piazza → Pozzo | (interno piazza, ma c'è) `viottolo_perimetrale_piazza` (✓ buon match) | no |
| Piazza → Via Scuola | `via_scuola` ◆ | sì |
| Mantenitori che arrivano: vari tratti convergenti | `sentiero_fuoco_ring`, `viottolo_perimetrale_piazza` | no |

### S09 — Quel Pomeriggio di Ottobre

Tratti brevi del villaggio centrale.

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Scuola → Forno (Gabriel da solo) | `via_dell_alba` ◆ | sì |
| Casa fratelli → Forno (sera) | `via_dell_alba` ◆ | sì |
| Mèmolo che gira: Forno → Casa Mèmolo | `viottolo_piazza_casa_memolo` | no |
| Liù tra finestre (volo, non sentiero) | — | — |

### S10 — La Notte senza Luna

Cammino lungo, silenzioso.

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Casa fratelli → Piazza | `viottolo_piazza_casa_memolo` (analogo, partono dalla loro casa simile) | no |
| Piazza → inizio Via del Pontile | `viottolo_perimetrale_piazza` o `sentiero_pontile_forno` | no |
| Via del Pontile (discesa lunga) | `via_del_pontile` ◆ | sì |
| Bocca/Pontile → ritorno a casa | `via_dell_alba` (per la salita all'alba) | no |

### S11 — La Festa del Raccolto

Festa: tutti vanno e vengono. Sentieri minori convergono in piazza.

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Pastori che scendono: Pascoli → Piazza | `via_che_sale` (in discesa) | no |
| Coltivatori scendono dai sacchi: Orti → Piazza | `sentiero_forno_orti_diretto` (in inverso) o `via_dell_alba` | no |
| Camminanti che vanno-vengono: Piazza → quartieri vari | `sentiero_fuoco_ring`, `viottolo_perimetrale_piazza` | no |
| Bartolo arriva: Pontile → Piazza | `via_del_pontile` (in salita) | no |
| Bru/Rovo: Foresta → Piazza | `sentiero_orti_torrente_foresta` | no |

### S12 — Quando i Tre Venti Suonano Insieme

Storia più lunga di tutta la saga, percorso quasi-mandala.

| Tratto percorso | Sentiero del catalogo | In grafo |
|---|---|---|
| Casa → Forno → Pontile (passaggio) | `via_dell_alba` | no |
| Pontile → riva ovest Fiume (risalita) | `sentiero_riva_ovest` (in salita verso nord) | no |
| Riva → Guado di pietre piatte | `sentiero_al_guado` ◆ (parzialmente) | sì |
| Guado → Radura dei Pini | ⚠ tratto interno Foresta non coperto bene |
| Radura → Pascoli Alti | `sentiero_capanne_pastori_pascoli` (in salita) | no |
| Pascoli → Burrone | `sentiero_pascoli_burrone_diretto` (✓ buon match) | no |
| Burrone → Grotta Grunto → Roccia Alta | `sentiero_montagne_gemelle` ◆ | sì |
| Roccia Alta → discesa → Via che Sale → Piazza → Forno | `via_che_sale` (in discesa) | no |

---

## §3. Riepilogo: sentieri PRIORITARI da dettagliare

### §3.1 Tier A — alta priorità (percorsi in 3+ storie)

Questi sono i sentieri che il bambino vedrà più spesso. Dettaglio massimo.

| Sentiero | Storie in cui appare | Stato scheda |
|---|---|---|
| `via_dell_alba` | s06, s08, s09, s10 (ritorno), s11, s12 — **6 storie** | 64% |
| `via_che_sale` | s01, s02, s11, s12 — **4 storie** | 57% |
| `sentiero_orti_torrente_foresta` | s03, s04, s05, s07, s11 — **5 storie** | 36% |
| `viottolo_perimetrale_piazza` | s08, s10, s11 — **3 storie** | 36% |
| `sentiero_montagne_gemelle` | s01, s12 — **2 storie** ma centrale (firma di S01) | 29% |
| `via_del_pontile` | s10 — **1 storia** ma struttura della notte intera | 43% |

### §3.2 Tier B — media priorità (percorsi in 2 storie o storie chiave)

| Sentiero | Storie | Stato scheda |
|---|---|---|
| `sentiero_capanne_pastori_pascoli` | s02, s12 | 36% |
| `sentiero_riva_ovest` | s07, s12 | 36% |
| `sentiero_al_guado` | s07, s12 | 36% |
| `sentiero_pascoli_burrone_diretto` | s12 (chiusura saga) | 36% |
| `sentiero_forno_orti_diretto` | s06, s11 | 36% |
| `via_scuola` | s08 (drammatica) | 50% |
| `via_degli_orti` | s03 | 43% |
| `viottolo_piazza_casa_memolo` | s06, s09, s10 (analogo) | 36% |

### §3.3 Tier C — bassa priorità (percorsi una sola volta)

| Sentiero | Storia |
|---|---|
| `sentiero_orti_casa_salvia` | s04, s06, s09 |
| `sentiero_casa_salvia_casa_zolla` | s06 |
| `sentiero_orti_casa_zolla` | s06 |
| `sentiero_ritorno_bocca_orti` | s07 |
| `sentiero_pontile_spiaggia` | s07 |
| `sentiero_case_basse_bocca` | s07 |
| `sentiero_foresta_traversata_ovest` | s05 (post-ponte) |
| `sentiero_fuoco_ring` | s11 |
| `sentiero_pontile_forno` | s10 |

### §3.4 Tier D — sentieri del catalogo MAI percorsi

Esistono nel catalogo (geografia canonica dell'isola) ma le 12 storie non li usano. Lasciare schede vuote — non sono priorità adesso.

| Sentiero | Quartiere |
|---|---|
| `sentiero_costiero_est` | perimetro |
| `sentiero_costiero_ovest` | perimetro |
| `sentiero_riva_est_parziale` | perimetro |
| `sentiero_scogliera_casa_amo` | acqua |
| `sentiero_spiaggia_casa_amo` | acqua |
| `sentiero_pontile_case_basse` | acqua |
| `sentiero_roccia_orti_tangenziale` | perimetro |
| `sentiero_roccia_burrone` | aria |
| `viottolo_piazza_bottega_nodo` | centro |
| `sentiero_tana_rovo_casa_salvia` | terra |
| `sentiero_casa_zolla_tana_rovo` | terra |
| `sentiero_orti_tana_rovo` | terra |
| `sentiero_forno_case_mattino` | fuoco |
| `sentiero_forno_orti_diretto` (verifica: era Tier C?) | fuoco |
| (… altri minori) | |

---

## §4. Gap critici — sentieri "fantasma" che la narrazione percorre ma il grafo non dichiara

Questo è il punto operativo più importante. Quando l'agente prosa scriverà, leggerà `locations_secondary` per capire dove ambientare. Se i sentieri **percorsi nella narrazione fattuale** non sono lì, l'agente non saprà che esistono.

Lista **per storia** dei sentieri da aggiungere in `locations_secondary`:

| Storia | Sentieri da aggiungere |
|---|---|
| s01 | `via_che_sale` |
| s02 | `via_che_sale`, `sentiero_capanne_pastori_pascoli` |
| s03 | `sentiero_orti_torrente_foresta` |
| s04 | `sentiero_orti_torrente_foresta`, `sentiero_orti_casa_salvia` |
| s05 | `sentiero_orti_torrente_foresta`, (eventualmente `sentiero_foresta_traversata_ovest`) |
| s06 | `sentiero_forno_orti_diretto`, `sentiero_orti_casa_salvia`, `sentiero_casa_salvia_casa_zolla`, `sentiero_orti_casa_zolla`, `viottolo_piazza_casa_memolo` |
| s07 | `sentiero_al_guado`, `sentiero_riva_ovest`, `sentiero_ritorno_bocca_orti`, `sentiero_pontile_spiaggia`, `sentiero_case_basse_bocca` |
| s08 | `viottolo_perimetrale_piazza`, `sentiero_fuoco_ring` |
| s09 | `sentiero_orti_casa_salvia`, `viottolo_piazza_casa_memolo` |
| s10 | `viottolo_perimetrale_piazza`, `sentiero_pontile_forno`, `via_dell_alba` (per la salita all'alba) |
| s11 | `via_che_sale`, `via_dell_alba`, `sentiero_fuoco_ring`, `viottolo_perimetrale_piazza`, `sentiero_orti_torrente_foresta` |
| s12 | `sentiero_riva_ovest`, `sentiero_al_guado`, `sentiero_capanne_pastori_pascoli`, `sentiero_pascoli_burrone_diretto`, `via_che_sale`, `via_dell_alba` |

**Totale aggiunte da fare in `locations_secondary`:** circa 35-40 entry distribuite sulle 12 storie.

---

## §5. Decisioni rimaste aperte — input richiesto

Prima di passare alla Fase 2 (dettaglio dei sentieri Tier A e Tier B con micro-elementi tipo "albero con incisione, roccia a forma di mezzaluna, lucciole della sera"), ho bisogno di tre decisioni:

**1. Si fanno entrambe le operazioni?**
   - **Op. A** Aggiungere i sentieri "fantasma" alle `locations_secondary` di ogni storia (uno script idempotente lo fa in 5 minuti).
   - **Op. B** Dettagliare le schede dei sentieri Tier A + Tier B (15 sentieri totali) con sezioni autoriali.
   
   Mio suggerimento: **entrambe**, e in quest'ordine — prima A (aggiunta meccanica), poi B (lavoro autoriale).

**2. Per il dettaglio (Op. B), proseguiamo con il pattern "mercato delle idee" come per le cornici?**

   Per ogni sentiero Tier A propongo 5-8 micro-elementi candidati ("la roccia a forma di mezzaluna a due terzi del percorso", "il punto dove si vedono le lucciole d'estate", "l'incisione di un grunt sull'albero più vecchio", "la pozza piccolissima dove c'è sempre la rana", "il sasso piatto dove i fratelli si fermano sempre"). Tu scegli, scarti, modifichi. Le tue diventano canoniche.

   Mio voto: sì, stesso pattern. Funziona.

**3. Quanti micro-elementi per sentiero?**

   Dipende dal Tier:
   - **Tier A** (6 sentieri): 4-6 elementi per sentiero (sono attraversati spesso, devono essere "abitati")
   - **Tier B** (8 sentieri): 2-3 elementi per sentiero (apparizioni più rare, basta un dettaglio o due)
   - **Tier C** (~10 sentieri): 1 elemento per sentiero (apparizione singola, basta una nota distintiva)

   Totale stimato dettagli da inventare: **6×5 + 8×2.5 + 10×1 = 60 micro-elementi** circa. Lavoro grosso ma fattibile in 2-3 sessioni di "mercato delle idee" da 20 elementi a turno.

---

## §6. Proposta operativa

Se ti torna la lettura, propongo questo flusso:

1. **Adesso (Fase 1 chiusa con questo doc).** Tu rivedi il doc, mi confermi l'audit (eventualmente correggi assegnazioni dubbie — alcuni "?" della tabella §2 sono ipotesi mie).

2. **Fase 2.A — Aggiunta meccanica.** Scrivo `add_paths_to_stories_locations_secondary.py`: legge una mappatura YAML (basata sulla tabella §4) e aggiorna in batch tutti i nodi storia. Dry-run prima, poi commit. Audit di drift dopo.

3. **Fase 2.B — Dettaglio Tier A.** Una sessione "mercato delle idee" sui 6 sentieri Tier A, ~30 candidati totali (5 per sentiero). Tu scegli i tuoi.

4. **Fase 2.C — Dettaglio Tier B.** Stessa cosa per gli 8 sentieri Tier B, ~20 candidati.

5. **Fase 2.D — Dettaglio Tier C.** Una sessione veloce, 10 candidati.

6. **Fase 3 — Scrittura nelle schede.** Script che prende le decisioni e popola le sezioni vuote (`Aspetto / forma`, `Coerenza cross-scena`, `Variabilità ammessa`, `Espressione / comportamento`) di ogni scheda Tier A/B/C scelta.

7. **Fase 4 — Aggiornamento del writing_brief.** Il brief di scrittura per ogni storia includerà ora una sezione *"Sentieri attraversati e loro micro-dettagli stabili"* con i dettagli del sentiero pertinenti alla scena.

Vai?
