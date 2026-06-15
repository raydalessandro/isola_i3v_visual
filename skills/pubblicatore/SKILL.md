---
role: pubblicatore
trigger: preparare il pacchetto di pubblicazione Amazon KDP di un volume (PDF libro + PDF stampa + wrap copertina + bozza listing)
scope_write: "output/ (gitignored) + kdp/listing_volN.md (manuale). NON tocca pipeline_narrativa/, NON tocca visual/, NON pubblica su Amazon"
commands: "python3 scripts/build_volume.py --volume N · python3 scripts/build_cover.py"
order: 80
---

# Skill — Pubblicatore (kit di pubblicazione Amazon KDP per volume)

> Per chi (IA o umano) ha appena clonato la repo `isola_i3v_visual` in locale
> e deve preparare il pacchetto KDP di un volume. **Non automatizza nulla**:
> serve a sapere quali script lanciare, dove sono i sorgenti, quali sono gli
> standard. Il lavoro fine resta manuale con Ray, in locale.
>
> Versione 1.0 — 2026-06-15. Le decisioni editoriali (titoli, sottotitoli,
> categorie BISAC, keywords) restano autoriali. La skill fa la macchina.

---

## TL;DR (in 30 secondi)

Per il Volume N:

```bash
# 1) PDF libro + stampa (legge le 3 storie del volume + immagini-scena)
python3 scripts/build_volume.py --volume N

# 2) Wrap copertina (fronte + dorso + quarta + bleed)
#    Prima: vai in testa a scripts/build_cover.py e cambia CURRENT_VOLUME = N
python3 scripts/build_cover.py

# 3) Bozza listing Amazon (manuale, una per volume)
#    File: kdp/listing_volN.md  — copia/adatta da kdp/listing_vol1.md
```

Output finale (tutto in `output/` o `_output/`, **gitignored**, regenerabili):
- `vol{N}_pres-dopo_libro.pdf` — interno KDP digitale
- `vol{N}_pres-dopo_stampa.pdf` — interno KDP stampa A5 + bleed
- `output/copertina/vol{N}_wrap_<style>_<back>.png` — wrap copertina KDP
- `kdp/listing_vol{N}.md` — bozza scheda Amazon (versionata, scritta a mano)

Tutto si fa in locale, Ray controlla, eventuali ritocchi si fanno a mano. **Niente upload automatico** su Amazon.

---

## 1. I tre input (devono esistere PRIMA di lanciare gli script)

### 1a. Le 3 storie del volume

```
pipeline_narrativa/storie_finali/sNN_*.md   (3 storie per volume, x = 1..12)
pipeline_narrativa/storie_finali/_scene/sNN/{*.jpg, _hd/*.jpg}    immagini per pagina
pipeline_narrativa/storie_finali/_annotations/sNN.yaml             annotation autoriali
pipeline_narrativa/storie_finali/_volumi/v0N/                      cornice editoriale del volume
```

Le 3 storie sono fissate dal grafo + cornice editoriale. Mapping volume→storie:

| Volume | Vento | Storie |
|---|---|---|
| 1 | Taglio | s01, s02, s03 |
| 2 | Intreccio | s04, s05, s06 |
| 3 | Mulinello | s07, s08, s09 |
| 4 | Autunno | s10, s11, s12 |

### 1b. La copertina pulita del volume

```
visual/atlante/emblema/copertina_clean_vol{N}.png   (PNG, ≥1536×2304 px)
```

Vol 1 oggi: `copertina_clean_v2.png` (1536×2304, prodotto da Manus). Per i
Vol 2-4 servirà generare la copertina pulita corrispondente (illustrazione
SENZA testo — il testo lo disegna `build_cover.py` via codice).

### 1c. La mappa aerea (uguale per tutti i volumi)

```
visual/atlante/mappe/isola_aerea_v1.jpg   (vista aerea dell'isola, usata dalle quarte)
```

Resta la stessa per tutti i 4 volumi (l'isola è una sola).

---

## 2. I tre tool

| Tool | Cosa fa | Dove vive | Esiste? |
|---|---|---|---|
| `scripts/build_volume.py` | PDF libro + PDF stampa A5+bleed 300 DPI | `scripts/` | ✅ |
| `scripts/build_cover.py` | Wrap copertina (fronte+dorso+quarta+bleed) PNG | `scripts/` | ✅ |
| `scripts/design_system.py` | Palette/font/glifi camuni (usato da entrambi) | `scripts/` | ✅ |

**Non esiste** (e per ora va bene così) un orchestratore unico che chiama tutti
e tre. Si lanciano a mano in sequenza — Ray vuole tenere il controllo
ad ogni passo.

---

## 3. Workflow per un volume

### Step 0 — Verifica precondizioni

```bash
# le 3 storie del volume hanno tutti i subhook con @image risolto
grep -c "@image TBD" pipeline_narrativa/storie_finali/sNN_*.md   # deve essere 0 per ogni storia del volume

# le HD ci sono (almeno una per subhook)
ls pipeline_narrativa/storie_finali/_scene/sNN/_hd/   # confronta con i subhook

# la copertina pulita del volume esiste
ls visual/atlante/emblema/copertina_clean_*.{png,jpg}

# audit verde
make audit
```

Se anche solo uno fallisce: **fermati e segnalalo a Ray**. Non improvvisare
asset mancanti.

### Step 1 — Build PDF libro + stampa

```bash
python3 scripts/build_volume.py --volume N
# output: vol{N}_pres-dopo_libro.pdf e vol{N}_pres-dopo_stampa.pdf in cwd
```

Cosa controllare:
- `Totale facciate: M` — deve essere **pari** (parità recto/verso KDP)
- `0 troncamenti` — il testo non eccede il box pagina
- Eventuali `WARNING: Immagine ... sotto spec` — banner attivo, asset da
  rigenerare ≥ specifica (segnalare a Ray)
- `LAYOUT_WARNINGS.md` se presente — leggi e segnala

**Numero pagine effettive del PDF**: serve al passo successivo per la spina
copertina. Lo ricavi dal totale facciate stampato dallo script.

### Step 2 — Calcola la spina (mm)

La spina dipende da pagine + tipo carta KDP:

| Tipo carta | mm per pagina |
|---|---|
| Premium color (consigliato per libri illustrati) | 0.05842 |
| Standard color | 0.05842 |
| Cream paper | 0.0635 |
| White paper | 0.05842 |

```
SPINE_MM = pagine_totali × mm_per_pagina
```

**Esempio Vol 1**: ~102 pagine × 0.05842 ≈ **5.96 mm**. Default in
`build_cover.py` è 6.4 mm (provvisorio): aggiornare prima di generare il
wrap finale per la stampa.

### Step 3 — Build wrap copertina

```bash
# 1. apri scripts/build_cover.py
# 2. in testa, modifica SE NECESSARIO:
#    - CURRENT_VOLUME = N
#    - SPINE_MM = <valore calcolato al passo 2>
#    - TITLE_STYLE = "T3"   (default validato per Vol 1)
#    - BACK_STYLE  = "island_C"   (default validato per Vol 1)
# 3. esegui:
python3 scripts/build_cover.py
# output: output/copertina/vol{N}_wrap_<style>_<back>.png  (+ varianti quarta)
```

**Stili disponibili** (decisione editoriale Ray, non improvvisare):
- `TITLE_STYLE`: `T1`/`T2` Fraunces (sobrio/terracotta), **`T3`** Fredoka
  tondo (default), `T4` Fraunces + fioritura
- `BACK_STYLE`: **`island_C`** oblò (default), `island_A` cartolina,
  `island_B` veduta, `collana` vignetta personaggi
- `SUBTITLE_POS`: `"top"` (default), `"bottom"`
- `PUBLISHER_FRONT`: `"logo"` solo sigillo (default), `"none"`, `"full"`
  sigillo+testo

Per cambiare qualcosa di diverso dai default: **chiedi a Ray** (gli stili
sono stati validati visivamente, non sono opinioni libere).

### Step 4 — Bozza listing Amazon

```bash
cp kdp/listing_vol1.md kdp/listing_vol{N}.md
# editare a mano con i dati del volume N (vento, storie, descrizione)
```

Il file `kdp/listing_vol{N}.md` è **manuale**: Ray scrive descrizione,
keywords, BISAC. La skill garantisce che esista e abbia i campi minimi
(vedi §5 Checklist).

### Step 5 — Verifica finale prima della consegna a Ray

```bash
# il PDF stampa apre regolarmente
ls -la vol{N}_pres-dopo_stampa.pdf vol{N}_pres-dopo_libro.pdf

# il wrap copertina ha le dimensioni KDP attese
python3 -c "from PIL import Image; print(Image.open('output/copertina/vol{N}_wrap_T3_island_C.png').size)"
# attese: W = (back+bleed) + spina + (front+bleed); H = trim + 2*bleed

# il listing ha tutti i campi minimi (vedi §5)
cat kdp/listing_vol{N}.md
```

Consegna a Ray con un riepilogo:
- N pagine effettive
- spina calcolata
- file finali (path + size)
- warning emersi durante il build (asset sotto spec, troncamenti, ecc.)

---

## 4. Standard KDP (specifiche tecniche)

| Parametro | Valore |
|---|---|
| Trim size | **A5** (148 × 210 mm) |
| Bleed | **3.175 mm** su tutti e 4 i lati (interno + copertina) |
| DPI interno | **300** (build_volume.py target) |
| DPI copertina (proof) | **200** (default build_cover.py) — alzare a **300** per stampa finale |
| Profilo colore | **sRGB** (no CMYK, conversione la fa KDP) |
| Margine sicurezza copertina | 9 mm dai bordi (testo dentro) |
| Spazio codice a barre | KDP lo sovrappone — `build_cover.py` lascia un riquadro bianco nel posto canonico |
| Età lettura | **3-6 anni** (saga decisa da Ray) |
| Formato file finali | PDF interni, PNG wrap copertina (KDP accetta) |

---

## 5. Checklist Amazon KDP per volume

### File da preparare

- [ ] `vol{N}_pres-dopo_libro.pdf` — interno digitale
- [ ] `vol{N}_pres-dopo_stampa.pdf` — interno stampa A5+bleed
- [ ] `output/copertina/vol{N}_wrap_<style>_<back>.png` — wrap copertina
- [ ] `kdp/listing_vol{N}.md` — bozza scheda Amazon

### Campi obbligatori nel listing

Verifica che `kdp/listing_vol{N}.md` contenga tutti questi campi (la skill
**non li genera**, controlla che ci siano):

- [ ] **Serie:** L'Isola dei Tre Venti
- [ ] **Volume:** N
- [ ] **Titolo:** L'Isola dei Tre Venti
- [ ] **Sottotitolo:** Volume N — <Il vento che ...>
- [ ] **Autore:** Beatrice Mercuri (default, può cambiare per scelta Ray)
- [ ] **Editore:** Spirale Editrice
- [ ] **Età di lettura:** 3-6 anni
- [ ] **Lingua:** Italiano
- [ ] **Descrizione** (testo annuncio, 1-3 paragrafi)
- [ ] **Keywords** — esattamente 7 slot, ognuna **≤ 50 caratteri**, niente
      termini vietati KDP (es. "bestseller", nomi di altri autori/marchi)
- [ ] **BISAC** — almeno 1, max 3 categorie (default: JUVENILE FICTION / ...)
- [ ] **Bio autore** (1 paragrafo)

### Verifica file copertina

- [ ] DPI 300 in build (`DPI = 300` nello script, non 200 proof)
- [ ] Risoluzione copertina pulita ≥ 1824×2736 px (per stampa, non solo proof)
- [ ] Spina (`SPINE_MM`) ricalcolata da pagine effettive del PDF + carta KDP
- [ ] Codice a barre: spazio bianco rispettato nella quarta

---

## 6. Vincoli (cosa la skill NON fa)

| ❌ MAI | ✅ Sempre |
|---|---|
| Modificare prosa, grafo, schede visual | Legge solo, read-only su `pipeline_narrativa/` e `visual/` |
| Inventare keywords, BISAC, descrizione | Il listing è autoriale (Ray scrive, la skill verifica) |
| Improvvisare stili (TITLE_STYLE/BACK_STYLE non validati) | Default = stile validato; per cambiare → Ray |
| Caricare/pubblicare su Amazon | Upload manuale Ray |
| Saltare il calcolo spina | Sempre ricalcolata da pagine effettive |
| Generare il PDF senza fare audit prima | `make audit` deve essere verde |
| Commit di PDF/PNG generati in branch | Tutto in `output/`/`_output/` (gitignored). Niente artifact committati |
| Saltare i banner "sotto spec" | Se compare un warning, segnalalo a Ray |

---

## 7. Quando un volume è "pronto per Amazon"

1. ✅ Tutte e 3 le storie hanno HD complete (nessun `@image TBD`)
2. ✅ `make audit` 5/5 PASS
3. ✅ `pytest` fast verde
4. ✅ PDF stampa generato senza troncamenti, facciate pari
5. ✅ Copertina pulita del volume esiste (`copertina_clean_vol{N}.png`)
6. ✅ Spina ricalcolata da pagine effettive
7. ✅ Wrap copertina generato a 300 DPI
8. ✅ Listing scritto da Ray con tutti i campi minimi (§5)
9. ✅ Ray ha aperto a mano i 3 file finali e ha dato OK

Se anche uno solo manca: **non è pronto**. Segnalare cosa manca a Ray e
attendere.

---

## 8. Quando in dubbio

1. Rileggi questa skill
2. Apri `kdp/listing_vol1.md` come reference
3. Apri `scripts/build_cover.py` (testa del file = config commentata)
4. Apri `scripts/build_volume.py --help` per le opzioni
5. Se ancora dubbio: **chiedi a Ray prima di lanciare il build**

Meglio una domanda in più che un volume da rigenerare.
