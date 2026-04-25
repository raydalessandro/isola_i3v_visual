# Sistema di Coordinate

**Versione:** 0.1
**Data:** 2026-04-24

---

## 1. DOPPIO SISTEMA

L'isola usa **due sistemi di coordinate simultanei**:

1. **Geografico (lat/lon, WGS84)** — per compatibilità con tutti gli strumenti GIS standard (QGIS, Leaflet, Mapbox, Google Earth). È il sistema usato dentro `geo/island.geojson`.
2. **Locale (east/north in metri)** — per leggibilità umana e per ragionamenti di scala. Usato dentro le schede luogo nei campi tipo "il Pozzo sta 3m a sud dell'Albero Vecchio".

I due sistemi convertono l'uno nell'altro con una formula semplice (vedi §4).

## 2. ANCORAGGIO GEOGRAFICO

L'Isola dei Tre Venti è ancorata a coordinate reali fittizie nel **Mar Mediterraneo centrale**, in un'area di mare aperto priva di isole reali.

**Centroide isola (centro Villaggio / Albero Vecchio):**
- **Latitudine:** 34.5000° N
- **Longitudine:** 18.0000° E

Questo punto è in mare aperto, a circa:
- 250 km a sud di Creta
- 350 km a nord della costa libica (Misurata)
- 500 km a est di Malta

L'area non ospita isole reali. L'Isola dei Tre Venti, essendo finzione, può esistere qui senza interferenze geografiche reali.

**Motivazione della scelta:**
- È compatibile con l'immaginario "mare che sta in mezzo a tutto" della Bible.
- Le isole fittizie sull'orizzonte (soglia Fase F, citate in apparato P.08) hanno senso geografico: possibili frammenti mediterranei.
- Il clima reale a quella latitudine è coerente col canone (estati calde, inverni miti, quattro stagioni nette, venti stagionali forti).
- È un'area "libera" sulla mappa reale — nessuno dirà "ma lì c'è Pantelleria".

## 3. ESTENSIONE DELL'ISOLA

L'isola ha dimensione approssimativa **8 km est-ovest × 7 km nord-sud** (Bible §2 geografia frattale).

Tradotto in gradi a latitudine 34.5°:
- 1° di latitudine ≈ 111 km → 7 km ≈ **0.063°** (estensione N-S).
- 1° di longitudine a 34.5°N ≈ 91 km → 8 km ≈ **0.088°** (estensione E-O).

**Bounding box isola (approssimato):**
- Nord: 34.5315° N
- Sud: 34.4685° N
- Est: 18.0440° E
- Ovest: 17.9560° E

La forma è ovale irregolare, non rettangolare — la bounding box è la scatola che la contiene, non il profilo reale.

## 4. SISTEMA LOCALE (EAST/NORTH METRI)

Dentro le schede luogo è scomodo ragionare in lat/lon. Usiamo un sistema locale più umano:

**Origine:** angolo sud-ovest della bounding box dell'isola (34.4685°N, 17.9560°E).
**Asse X:** east, crescente verso est, in metri.
**Asse Y:** north, crescente verso nord, in metri.

**Scala approssimativa:**
- 1 metro di longitudine locale (est) ≈ 0.0000110° a 34.5°N.
- 1 metro di latitudine locale (nord) ≈ 0.0000090° (quasi costante).

**Esempi:**
- Centroide Villaggio = (4000, 3500) in locale ≈ (18.0000°E, 34.5000°N) in geografico.
- Forno di Fiamma, se sta 80 m a est del centro Villaggio → locale (4080, 3500) → geografico (18.00088°E, 34.5000°N).

**Nelle schede luogo:** quando possibile si registrano entrambi i sistemi. Nelle prime fasi (bootstrap, luoghi macro) solo il locale basta; il geografico si calcola quando si committa sul GeoJSON.

## 5. PROIEZIONE

Per la resa web (Leaflet, Mapbox) si usa **EPSG:4326 (WGS84 geografica)** dato che il GeoJSON è nativamente in lat/lon.

Per calcoli di distanza locale a piccola scala (fino a ~10 km), l'approssimazione cartesiana (pitagora su east/north) è accurata entro l'1-2%. Non serve proiezione UTM per i nostri scopi.

Se in futuro si vuole una proiezione più accurata per export cartografico di qualità, la zona è **UTM 34N** (EPSG:32634).

## 6. PRECISIONE DICHIARATA

Cartografia a tre livelli di precisione:

- **Livello A — canonico fissato:** ±10 m. Luoghi mappati con certezza (Villaggio, Albero Vecchio, Forno, Pontile, Grotta di Grunto).
- **Livello B — canonico provvisorio:** ±50 m. Luoghi mappati ma posizione esatta rivedibile (es. esatto punto dove la Via dell'Alba esce dalla Piazza).
- **Livello C — stub:** ±200 m o più. Luoghi menzionati ma non ancora posizionati (es. singole case dei Pescatori, singoli alberi degli Orti).

Il `status` nella property della feature GeoJSON indica il livello: `canonico` = A, `provvisorio` = B, `stub` = C.

## 7. COORDINATE DEI PRINCIPALI NODI (v0.1 bootstrap)

Alcune sono ora **canoniche** grazie a S7 e Bible §8 (Sorgente, Biforcazione, Guado, Bocca). Le altre restano provvisorie.

| Nodo | Locale (E, N) | Geografico (lon, lat) | Status |
|---|---|---|---|
| Centroide isola / Villaggio / Albero Vecchio | (4000, 3500) | (18.0000, 34.5000) | canonico |
| Sorgente del Fiume | (4000, 5800) | (18.0000, 34.5207) | canonico |
| Biforcazione del Fiume | (4000, 5450) | (18.0000, 34.5176) | canonico |
| Guado di Pietre Piatte | (4000, 5600) | (18.0000, 34.5190) | canonico |
| Bocca (foce Fiume) | (4000, 900) | (18.0000, 34.4766) | canonico |
| Centroide Quartiere di Fuoco | (5500, 3500) | (18.0165, 34.5000) | provvisorio |
| Centroide Quartiere d'Acqua | (4000, 1800) | (18.0000, 34.4847) | provvisorio |
| Centroide Quartiere di Terra | (2500, 3500) | (17.9835, 34.5000) | provvisorio |
| Centroide Quartiere d'Aria | (4000, 5000) | (18.0000, 34.5135) | provvisorio |
| Roccia Alta | (4200, 5300) | (18.0022, 34.5162) | provvisorio |
| Montagna Gemella Est | (4300, 6250) | (18.0033, 34.5248) | provvisorio |
| Montagna Gemella Ovest | (3700, 6250) | (17.9967, 34.5248) | provvisorio |
| Grotta di Grunto | (4020, 6180) | (18.0002, 34.5241) | provvisorio |

## 8. CAMBIARE ANCORAGGIO

Se in futuro si decide di spostare l'ancoraggio geografico (es. per ragioni editoriali, o perché quella zona mediterranea viene citata altrove), la traslazione è uniforme: si aggiornano tutte le coordinate geografiche nel GeoJSON, le coordinate locali restano invariate. Questa è una delle ragioni per cui teniamo il sistema locale separato.

Un cambio di **orientamento** (ruotare l'isola) sarebbe invece disruptive e andrebbe evitato.

---

**FINE sistema_coordinate.md v0.1**
