# Convenzioni di Naming e ID

**Versione:** 0.1
**Data:** 2026-04-24

---

## 1. REGOLE GENERALI

- **Lingua:** italiano (coerente col corpus narrativo).
- **Stile:** `snake_case` (minuscole, underscore come separatore, nessun apostrofo, nessun accento).
- **Articoli:** esclusi. `forno_di_fiamma`, NON `il_forno_di_fiamma`.
- **Preposizioni:** mantenute solo se canoniche al nome. `pontile_di_bartolo`, `casa_di_amo`.
- **Apostrofi e accenti:** traslitterati. `d'acqua` → `d_acqua`; `venti` → `venti`; `mèmolo` → `memolo`.
- **Maiuscole:** mai. Anche per nomi propri: `grunto`, non `Grunto`.

## 2. ID LUOGHI CANONICI (v0.1)

### Villaggio
- `villaggio` — centroide area
- `piazza` — piazza centrale
- `albero_vecchio` — albero al centro
- `pozzo` — pozzo accanto all'Albero
- `panca_di_pietra` — panca dove siedono le Vecchie
- `scuola_di_stria` — scuola a SO
- `casa_di_stria` — casa adiacente alla scuola
- `bottega_di_nodo` — bottega del picchio
- `casa_di_nodo` — casa adiacente
- `casetta_di_memolo` — casetta tonda dietro cespuglio

### Quartiere di Fuoco
- `quartiere_fuoco` — centroide area
- `via_dell_alba` — via che collega Villaggio a quartiere
- `forno_di_fiamma` — casa-forno di Fiamma
- `case_del_mattino` — gruppo case orientate a est
- `fabbro` — bottega del fabbro
- `conceria` — conceria
- `essiccatoio` — essiccatoio frutta

### Quartiere d'Acqua
- `quartiere_acqua` — centroide area
- `via_del_pontile` — via verso il Pontile
- `bocca` — foce del Fiume nel mare
- `pontile_di_bartolo` — pontile + capanna
- `spiaggia_delle_conchiglie` — spiaggia a SE della Bocca
- `casa_di_amo` — casa sulla scogliera
- `case_basse_pescatori` — case dei Pescatori sulla riva interna
- `scogliera_est` — scogliera dove sta Amo

### Quartiere di Terra
- `quartiere_terra` — centroide area
- `via_degli_orti` — via verso gli Orti
- `orti_del_cerchio` — polygon 3 anelli concentrici
- `orti_cerchio_interno` — anello interno (erbe, ortaggi)
- `orti_cerchio_medio` — anello medio (legumi, cereali)
- `orti_cerchio_esterno` — anello esterno (frutteti)
- `foresta_intrecciata` — foresta oltre gli Orti
- `tana_di_rovo` — tana del tasso
- `casa_di_salvia` — casa-tana della lepre
- `casa_di_zolla` — casa-tana dello scoiattolo

### Quartiere d'Aria
- `quartiere_aria` — centroide area
- `via_che_sale` — via verso i Pascoli
- `pascoli_alti` — pascoli in pendenza
- `capanne_stagionali_pastori` — capanne estive
- `roccia_alta` — sperone panoramico
- `montagne_gemelle` — due cime
- `burrone` — canyon tra le cime
- `grotta_di_grunto` — grotta dove vive Grunto

### Perimetro
- `fiume_che_gira` — anello d'acqua
- `guado_nord` — punto di attraversamento a nord
- `fascia_costiera` — terra tra Fiume e mare
- `mare_aperto` — oltre la costa
- `isole_orizzonte` — isole visibili all'orizzonte (soglia F)

## 3. CATEGORIE DI FEATURE (properties.type in GeoJSON)

- `island_outline` — profilo costiero isola
- `coastal_belt` — fascia costiera (polygon)
- `river` — Fiume che Gira (linestring)
- `sea` — mare (polygon implicito, fuori dall'isola)
- `quarter` — polygon quartiere
- `path` — sentiero / via
- `square` — piazza
- `landmark` — punto di riferimento naturale (Albero, Roccia Alta)
- `building` — edificio
- `burrow` — tana animale
- `cave` — grotta
- `mountain_peak` — cima
- `valley` — burrone / gola
- `forest` — foresta (polygon)
- `fields` — orti / pascoli (polygon)
- `beach` — spiaggia
- `pier` — pontile
- `cliff` — scogliera
- `ford` — guado
- `river_mouth` — foce

## 4. CATEGORIE SECONDARIE (properties.category)

Opzionali, per raffinare. Esempi:
- `building` + `category: bakery` → forno
- `building` + `category: workshop` → bottega
- `building` + `category: school` → scuola
- `building` + `category: dwelling` → casa abitata
- `building` + `category: forge` → fabbro
- `building` + `category: tanner` → conceria
- `building` + `category: drying_rack` → essiccatoio
- `building` + `category: fisher_house` → Casa Bassa pescatore

## 5. STATUS

Una feature può avere `status`:
- `canonico` — fissato con certezza, Bible o grafo storie.
- `provvisorio` — mappato ma la posizione/forma può cambiare.
- `stub` — solo menzionato, non ancora mappato con precisione.

## 6. QUARTIERI (properties.quarter)

Una feature che sta dentro un quartiere dichiara quale:
- `centro` (Villaggio)
- `fuoco`
- `acqua`
- `terra`
- `aria`
- `perimetro` (Fiume, fascia costiera, mare)

## 7. SCHEDA DI RIFERIMENTO

Una feature con scheda associata dichiara il path relativo:
- `properties.scheda: "luoghi/quartiere_fuoco/forno_di_fiamma.md"`

Se la scheda non esiste ancora, si omette il campo.

## 8. NOMI VISUALIZZATI

- `properties.id` — snake_case, per codice.
- `properties.name` — nome visualizzato, con accenti e maiuscole canoniche. Es. `"Forno di Fiamma"`, `"Albero Vecchio"`, `"Mèmolo"`.

---

**FINE convenzioni_id.md v0.1**
