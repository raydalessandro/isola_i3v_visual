# CHANGELOG — Cartografia Tecnica

Tutte le modifiche significative al canone cartografico vanno registrate qui, in ordine cronologico inverso (più recente in alto).

Formato:
- **[data] vX.Y** — descrizione cambiamento.

---

## [2026-04-28] v0.6.1 — Aggiunta `sentiero_montagne_gemelle` (porting grafo Fase E)

Modifica puntuale durante porting grafo a schema v1.2 (Fase E, sentinella catalogo P0 di s01).

- **Aggiunto** `sentiero_montagne_gemelle` (LineString, `canonico`, quartiere `aria`, `sentiero_montano`). Cengia di mezzacosta che dal Burrone (zona Grotta di Grunto) risale al colle tra le due Montagne Gemelle. Tracciato 3 punti: A=(4023,6180) presso Grotta Grunto → mid=(3993,6215) mezzacosta → B=(3993,6250) colle.
- Citato in s01 come `location_precise` di scene_hook ("sentiero_montagne_gemelle_mezzacosta_cengia_sul_burrone"): tappa del cammino dei fratelli per portare la pagnotta a Grunto e per salire alle Montagne. Status `canonico` giustificato dalla presenza diretta nella prima storia della saga.
- Le creste vere delle due Montagne Gemelle (montagna_gemella_ovest, montagna_gemella_est) si raggiungono fuori sentiero dal colle (alta montagna).

**Backward-compat:** 35/35 ID grafo coperti (invariato). Total features: 104 → 105.

---

## [2026-04-25] v0.6.0 — Sync con grafo storie v0.10.0 (S1-S12)

Allineamento alla nuova versione del grafo storie (v0.6.0 → v0.10.0, +S9-S12). S1-S8 invariate. Backward-compat 100% mantenuta.

**Modifiche puntuali:**
- **Aggiunta** `radura_dei_pini` (Polygon, `provvisorio`, quartiere `terra`) — landmark interno alla Foresta Intrecciata, margine NE verso i Pascoli Alti. Citato in S12 (threshold_moment, resolution_mode, visual_anchors hook_04).
- **Promotion** `sentiero_roccia_burrone` da `provvisorio` a `canonico`. Giustificazione S12: "la cengia che sale a Roccia Alta — i fratelli la sanno senza che nessuno la indichi".
- **Annotazione** in `roccia_alta.note`: la "cengia" di S12 coincide con `sentiero_roccia_burrone` (non entità autonoma).
- **Alias** `guado_nord` aggiunto a `guado_di_pietre_piatte` (citato in S12: "guado nord dove l'acqua trema piano").
- **Decisione richiamata:** "casa_fratelli non entity, l'isola è protagonista" (blocco_0). Il "cortile" citato in `s10.wind_notes` non è mappato per coerenza.

**Stato:** 104 feature totali. Grafo↔cartografia: 35/35 ID coperti.

**Nota operativa:** Ray ha annunciato manutenzione imminente sul grafo storie. La versione manutenuta diventerà la nuova baseline; eventuali incoerenze emerse da quella manutenzione si risolveranno in v0.6.x o v0.7.

---

## [2026-04-24] v0.5 — Mappa urbanistica completa navigabile

**Decisione (Ray):** chiusura sessione con mappa urbanistica stampabile, navigabile come Google Maps — "così posso percorrere i sentieri con la mente".

**18 sentieri aggiunti** per completare la raggiungibilità urbanistica. Tutti **provvisori** (inferiti, non canonici da storie). Principio: ogni edificio deve essere raggiungibile da almeno una via, ogni cluster ha viottoli interni, i quartieri hanno ring-road o assi.

### Nuovi sentieri per categoria

**Quartiere di Terra (4):**
- `sentiero_orti_casa_salvia`
- `sentiero_orti_casa_zolla`
- `sentiero_tana_rovo_casa_salvia`
- `sentiero_casa_zolla_tana_rovo`

**Quartiere di Fuoco (2):**
- `sentiero_forno_case_mattino` (prosecuzione Via dell'Alba)
- `sentiero_fuoco_ring` (ring road Case Mattino/Fabbro/Conceria/Essiccatoio)

**Quartiere d'Acqua (3):**
- `sentiero_scogliera_casa_amo`
- `sentiero_spiaggia_casa_amo`
- `sentiero_case_basse_bocca`

**Quartiere d'Aria (2):**
- `sentiero_capanne_pastori_pascoli`
- `sentiero_pascoli_burrone_diretto` (alternativa alla salita via Roccia Alta)

**Villaggio centrale (3):**
- `viottolo_perimetrale_piazza` (anello intorno alla Piazza che connette tutte le case)
- `viottolo_piazza_bottega_nodo`
- `viottolo_piazza_casa_memolo`

**Tangenziali inter-quartiere (3):**
- `sentiero_forno_orti_diretto` (est-ovest senza passare dal centro)
- `sentiero_roccia_orti_tangenziale` (ovest-nord)
- `sentiero_pontile_forno` (sud-est)

**Sentieri perimetrali (3):**
- `sentiero_riva_est_parziale` (Braccio Est, silente)
- `sentiero_costiero_ovest` (fascia costiera ovest)
- `sentiero_costiero_est` (fascia costiera est)

**Non aggiunto — decisione architetturale:** fascia costiera NORD è "oltre la Sorgente", praticamente inaccessibile da sentieri normali. Lasciata deliberatamente silente come zona mitica/inaccessibile.

### Viewer web completamente riscritto (Google Maps-style)

Il visualizzatore `geo/viewer/index.html` ora include:

- **Ricerca full-text** in alto (cerca per nome, ID, o alias).
- **Pannello di dettaglio** che si apre al click su un luogo, con tutti i metadati canonici (status, note, aliases, parent/children, proprietà specifiche, coordinate).
- **Navigazione tra feature**: cliccando su parent/children nel dettaglio si naviga al luogo collegato.
- **Filtri avanzati**: per categoria di strada (9 tipi), per tipo feature, per quartiere, per status.
- **Icone differenziate per tipo** (▲ cime, ◉ landmark, ✦ sorgente, ▣ edifici, ⬭ tane, ◖ grotte, ecc.).
- **Etichette permanenti** per i luoghi più importanti, toggle on/off.
- **Hover info** in tempo reale nella sidebar.
- **Pulsanti azione**: adatta vista, ripristina filtri, toggle etichette.
- **Risoluzione alias automatica**: se cerchi `villaggio_centrale` trova `piazza_villaggio`.

**Totale v0.5:** 103 feature (60 canonico · 41 provvisorio · 2 stub). 36 sentieri/vie. Ogni edificio canonico raggiungibile.

### Come usarlo

1. Scompatta il tar, apri `geo/viewer/index.html` in browser.
2. Digita nel campo ricerca per trovare un luogo → ti porta sopra.
3. Click su un punto → dettaglio completo, con link cliccabili per navigare parent/children.
4. Usa i filtri nella sidebar per focalizzarti su una categoria o quartiere.

Questa è la **mappa stampabile** della sessione di oggi. Chi scrive le storie o chi genera immagini ha ora un Google Maps dell'isola.

---

## [2026-04-24] v0.4 — Backward-compatibility ID grafo + strade dalle storie

**Decisioni (Ray):**

1. **Backward-compatibility totale con grafo storie** — il GeoJSON ora risolve tutti i 34 ID cartografici del grafo v0.6.0 (direttamente o via alias).
2. **Strade segnate dalle storie** — tracciati i sentieri impliciti dalle 8 storie canoniche. Strategia: "posizioniamo urbanistica completa partendo da strade già battute nelle storie e costruiamo quelle implicite".

**Allineamento grafo storie:**

Aggiunto campo `parent` ai sotto-tratti/componenti di feature aggregate:
- `fiume_capo`, `fiume_braccio_ovest_*`, `fiume_stretta_due_massi`, `fiume_braccio_est` → `parent: "fiume_che_gira"`.
- `montagna_gemella_est`, `montagna_gemella_ovest` → `parent: "montagne_gemelle"`.

Aggiunto campo `aliases` a feature equivalenti nel grafo:
- `piazza_villaggio.aliases: ["villaggio_centrale"]`.
- `panca_di_pietra.aliases: ["mercato_del_mezzogiorno_panca_di_pietra"]`.

Create feature aggregate (per risolvere ID grafo):
- `fiume_che_gira` come MultiLineString con `children: [6 sotto-tratti]`, `aggregate: true`.
- `montagne_gemelle` come MultiPoint con `children: [due cime]`, `aggregate: true`.

L'ID `tutta_isola_quattro_quartieri_attraversati` del grafo è **non-cartografico** (riferimento logico S6), non aggiunto al GeoJSON.

**Copertura finale ID grafo:** 34/34 (100%).

**Nuovi luoghi canonici estratti dalle storie S1-S8:**

- `pozza_dei_pascoli` — pozza d'acqua sui Pascoli Alti a metà cammino (S2).
- `noce_della_scuola` — grande noce sulla Via della Scuola che cade (S8). Stato post-S8: caduto, ma il punto resta landmark.
- `zona_di_lavoro_salvia` — area provvisoria polygon nella Foresta (S4).

**Nuovi sentieri canonici dalle storie:**

- `sentiero_foresta_traversata_ovest` — traversata Foresta est-ovest (S3: pallone oltre la Foresta).
- `sentiero_ritorno_bocca_orti` — dalla Bocca agli Orti tagliando dentro (S7 ritorno).
- `sentiero_casa_salvia_margine_foresta` — Casa Salvia → margine Foresta (S4).
- `sentiero_orti_torrente_foresta` — Orti → torrente dentro la Foresta, 20-30 min (S5).

Il "percorso circolare" di S6 (Dono per Mèmolo) è composto dall'unione di Via dell'Alba + Via degli Orti + Via che Sale che si toccano alla Piazza — non richiede nuova feature geometrica.

**Totale v0.4:** 83 feature (molte nuove aggiunte, nessuna rimossa). Backward-compat 100%.

**Strumento verifica_luogo.py aggiornato:** ora risolve automaticamente alias e riconosce feature aggregate. Esempio:

```bash
python3 verifica_luogo.py --id villaggio_centrale    # -> alias -> piazza_villaggio
python3 verifica_luogo.py --id fiume_che_gira        # -> aggregato con 6 children
```

---

## [2026-04-24] v0.3 — Posizionamento completo + Fiume a sotto-tratti

**Decisioni strutturali (Ray):**

1. **Fiume spezzato in sotto-tratti** — strategia per agganciare punti canonici narrativi alla geometria. Quando una storia nomina un punto specifico del Fiume con peso narrativo, quel tratto diventa una feature distinta. Lo script chi controlla la scrittura può verificare geometricamente se una nuova storia passa in un punto già fissato.

2. **Sorgente modellata come falda profonda, non da ruscelli.** Lascia mano libera narrativa sui ruscelli superficiali (possono cambiare, apparire/sparire stagionalmente) senza rompere il canone idraulico.

3. **Strategia "posiziona tutto, poi apri granulare"** — completato il posizionamento di tutti i luoghi canonici residui. Le schede luogo dettagliate vengono dopo.

**Fiume — struttura v0.3:**

- `fiume_capo` — Sorgente → Biforcazione (con Guado su questo tratto).
- `fiume_braccio_ovest_alto` — Biforcazione → pre-Stretta.
- `fiume_stretta_due_massi` — tratto breve dove il letto si stringe. **Punto canonico S7.**
- `fiume_braccio_ovest_medio` — post-Stretta → curva sud.
- `fiume_braccio_ovest_basso` — curva sud → Bocca.
- `fiume_braccio_est` — unico tratto (da spezzare quando emergono punti narrativi).

**Landmark canonico aggiunto: `due_massi`** (punto sul tratto Stretta, canonico S7).

**Idrografia — altre modifiche:**
- `sorgente.water_origin: "falda_profonda_infiltrazione"` — falda, non ruscelli.
- Rimosse feature `ruscello_montagna_est`, `ruscello_montagna_ovest`.
- Aggiunte `greto_montagna_est`, `greto_montagna_ovest` come `seasonal_streambed` — solcature stagionali, non idrauliche.

**Nuove feature macro polygonali:**
- `terra_interna` — polygon dentro il Fiume (tutta la terra centrale).
- `fascia_costiera` — polygon con hole (isola esterna, terra interna come buco).
- `villaggio` — polygon centrale (diametro ~500m).
- `piazza_villaggio` — polygon circolare (diametro 25m).
- 4 quartieri come polygon: `quartiere_fuoco`, `quartiere_acqua`, `quartiere_terra`, `quartiere_aria`.
- `orti_cerchio_interno`, `orti_cerchio_medio`, `orti_cerchio_esterno` — 3 anelli concentrici polygon.
- `foresta_intrecciata` — polygon irregolare.
- `pascoli_alti` — polygon.

**Nuovi edifici Villaggio centrale:**
`pozzo_piazza`, `panca_di_pietra`, `scuola_stria`, `casa_stria`, `bottega_nodo`, `casa_nodo`, `casa_memolo`, `casa_memolo_cortile`, `cespuglio_dietro_albero_vecchio`.

**Nuovi edifici Quartiere Fuoco:**
`forno_cortile`, `case_del_mattino`, `fabbro`, `conceria`, `essiccatoio`.

**Nuovi edifici Quartiere Acqua:**
`capanna_bartolo`, `scogliera_est`.

**Nuovi edifici Quartiere Aria:**
`capanne_stagionali_pastori`.

**Totale v0.3:** 74 feature (55 canonico · 17 provvisorio · 2 stub).

**Workflow operativo** (per chi controlla la scrittura delle storie):
Quando una nuova storia tocca il Fiume in un punto specifico, confrontare con i sotto-tratti esistenti. Se il punto ricade nella Stretta dei Due Massi → implica letto stretto + massi + acqua accelerata → constraint visivo e narrativo. Se ricade in un tratto generico → suggerisce di spezzare il tratto e creare il landmark nuovo.

---

## [2026-04-24] v0.2 — Fiume Variante C + rete sentieri

**Decisione strutturale (Ray):** adottata Variante C per il Fiume che Gira — due bracci asimmetrici. Risolta la questione idraulica della Bocca (foce) e del Guado (pedonale, non interruzione anello).

**Modello Fiume:**
- **Sorgente** a nord, dove i ruscelli dalle Montagne Gemelle si raccolgono.
- **Capo del Fiume:** breve tratto dalla Sorgente alla Biforcazione. Il **Guado di Pietre Piatte** sta su questo tratto (acqua bassa, pietre affioranti d'estate, unico passaggio pedonale).
- **Biforcazione** poco sotto il Guado.
- **Braccio Ovest:** più corto, più stretto (~7m), più veloce. Ruolo canonico S7 (zattera).
- **Braccio Est:** più lungo, più ampio (~12m), più lento, tortuoso. Narrativamente silente S1-S8 — candidato storie future.
- **Bocca a sud:** i due bracci si ricongiungono e sfociano nel mare.
- **Corrente:** nord → sud in entrambi i bracci. La "direzione antioraria" percepita da chi cammina lungo la riva interna ovest (S7) è coerente col modello.

**Canonicità:**
- Guado, Bocca, Sorgente, Biforcazione, Braccio Ovest, Capo: **canonico** (vincolati da S7 e Bible §8).
- Braccio Est: **canonico** nella geometria generale, **provvisorio** nel dettaglio del tracciato.
- Ruscelli dalle Montagne: **provvisorio** (esatto tracciato da raffinare).

**Verifica geometrica intersezioni Vie × Fiume:**
- Nessuna delle 4 Vie principali attraversa il Fiume. Tutti i quartieri canonici stanno dentro l'anello ("terra interna").
- Il Fiume si attraversa solo al Guado (pedonale) o in barca.
- Non servono ponti sulle Vie principali.

**Feature aggiunte rispetto a v0.1 (+28):**
- Idrografia: `sorgente`, `fiume_biforcazione`, `fiume_capo`, `fiume_braccio_ovest`, `fiume_braccio_est`, `ruscello_montagna_est`, `ruscello_montagna_ovest`, `torrente_affluente_foresta`.
- Quartiere d'Aria: `montagna_gemella_est`, `montagna_gemella_ovest` (sdoppiate da `montagne_gemelle`), `burrone`, `grotta_grunto`.
- Quartiere d'Acqua: `pontile_bocca`, `spiaggia_conchiglie`, `casa_amo`, `case_basse_pescatori`.
- Quartiere di Terra: `orti_del_cerchio`, `foresta_intrecciata`, `tana_rovo`, `casa_salvia`, `casa_zolla`.
- Quartiere di Fuoco: `forno`.
- Sentieri secondari: `via_scuola`, `sentiero_roccia_burrone`, `sentiero_al_guado`, `sentiero_riva_ovest`, `sentiero_pontile_spiaggia`, `sentiero_pontile_case_basse`, `sentiero_orti_tana_rovo`, `sentiero_casa_salvia_casa_zolla`.

**Feature rimosse:** `montagne_gemelle` (sostituita da due point separate).

**Totale v0.2:** 46 feature (17 canonico · 27 provvisorio · 2 stub).

**Workflow adottato (Ray):** ogni volta che mappiamo un luogo di secondo livello, controlliamo quali sentieri servono per arrivarci. Se non esistono, li proponiamo come `provvisorio` per conferma canonica successiva.

---

## [2026-04-24] v0.1 — Bootstrap

- Creata struttura directory `cartografia/`.
- Scritto `README.md` con regole di isolamento rispetto alla pipeline narrativa.
- Scritte convenzioni base:
  - `sistema_coordinate.md` (ancoraggio Mediterraneo centrale, centroide isola a 34.5°N 18.0°E).
  - `scala_e_proporzioni.md` (isola ~8×7 km, tre cinture, quattro quartieri).
  - `convenzioni_id.md` (snake_case, italiano).
  - `orientamenti_venti.md` (venti canonici per ora del giorno).
- Scritto `_template_scheda.md` per schede luogo.
- Creato `island.geojson` macro v0.1:
  - Polygon contorno isola (ovale irregolare ~8×7 km).
  - Polygon fascia costiera esterna.
  - LineString Fiume che Gira (anello antiorario con aperture a sud/Bocca e a nord/guado).
  - Point centroide Villaggio.
  - Point centroidi 4 quartieri.
  - Point Albero Vecchio (a coincidere col centroide Villaggio).
- Creato `geo/viewer/index.html` visualizzatore Leaflet minimo.

**Stato:** nessun luogo canonico di livello edificio ancora mappato. Prossimo passo: Passo 2 (luoghi di primo livello).

---
