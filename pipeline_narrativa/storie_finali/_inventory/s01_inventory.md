# Inventario hook s01 — La Nebbia delle Montagne Gemelle

> **Scopo.** Per ciascuno dei 10 hook visivi della storia s01, mappare gli **elementi visivi** in scena (personaggi, luogo, oggetti) ai **prompt grok disponibili** e alle **immagini canoniche** già generate. Identifica i gap operativi e le aggiunte dalla prosa al canone.
>
> **Pattern riutilizzabile** per le altre 11 storie. Vedi `_inventory/README.md` per schema generale.
>
> **Stato:** primo inventario costruito a mano per validare il pattern. Successivamente automatizzabile via script.

## Riepilogo s01

| Metrica | Valore |
|---|---|
| Hook totali | 10 (h01..h10) |
| Personaggi distinti coinvolti | 5 (Fiamma, Gabriel, Elias, Noah, Grunto) + 1 anonimo (Camminante h02) |
| Luoghi attraversati | 7 (Forno, Piazza, Via che Sale, Pascoli Alti, Burrone bordo, Cengia, Montagne Gemelle in lontananza) |
| Oggetti canonici in scena | 3 (pagnotta_forno, grembiule_fiamma, cicatrice_grunto) + carriola Camminante |
| Hook con prompt completi | 10/10 (con riserva) |
| Hook con immagini canoniche luogo già caricate | 1/10 (solo Forno per h01 e h10) |
| Hook con immagini canoniche personaggi tutti pronti | 1/10 (solo h08 — Grunto+Noah; manca Gabriel+Elias) |
| Aggiunte da prosa al catalogo | 3 (vedi sezione finale) |
| Gap critici | 2 (Gabriel+Elias img mancanti, Via che Sale prompt grok mancante) |

---

## Hook per hook

### s01_h01 — Pagina 1 — Forno alba: Fiamma consegna le pagnotte

**Personaggi:**

| Personaggio | Prompt grok | Img canoniche | Note scena |
|---|---|---|---|
| Fiamma | ✅ `visual/personaggi/individuali/primari/fiamma/prompt_grok.md` | ✅ 4 (`fronte`, `impasta`, `ferma`, `turnaround`) | impasta da prima dell'alba, vapore alla finestra, velo di farina |
| Gabriel | ✅ prompt | ❌ 0 immagini | entra per primo |
| Elias | ✅ prompt | ❌ 0 immagini | dietro Gabriel |
| Noah | ✅ prompt | ✅ 4 immagini | dietro Elias |

**Luogo:** Forno (interno, sala laboratorio, alba)
- Prompt: ✅ `visual/luoghi/quartiere_fuoco/forno/prompt_grok.md` (atlante chiuso)
- Img canonica reference: ✅ `forno_canonica_v1_laboratorio_panoramica.jpg` o `forno_canonica_v1_laboratorio_dettaglio.jpg`

**Oggetti in scena:**
- pagnotta_forno → ✅ prompt + (no img canonica generata)
- grembiule_fiamma → ✅ prompt + 1 img canonica
- vapore alla finestra → 📝 dettaglio sensoriale aggiunto da prosa, **non nel canone visuale forno** — da aggiungere a scheda Forno

**Frasi-codice da preservare nella composizione:**
- «Se passate dal Burrone, una per Grunto. Una sola.»
- «Più di una se la mangia per dispetto. E poi non torna giù per giorni.»

**Status composizione:** ⏳ `image: TBD`. Pronto appena Gabriel+Elias hanno img canoniche.

---

### s01_h02 — Pagina 2 — Piazza alba con Camminante anonimo

**Personaggi:**

| Personaggio | Prompt grok | Img | Note |
|---|---|---|---|
| Gabriel, Elias, Noah | come h01 | come h01 | escono dal Forno, attraversano la Piazza |
| Camminante anonimo (sagoma) | ⚠️ collettivo `camminanti/scheda.md` (saluto canonico) — no prompt grok dedicato | — | sagoma con carriola di vimini, gesto saluto Camminanti |

**Luogo:** Piazza del Villaggio (alba, vuota)
- Prompt: ✅ `visual/luoghi/villaggio_centrale/piazza_villaggio/prompt_grok.md`
- Img: ❌ 0
- Sub-elementi: cespuglio (casetta Mèmolo dietro) opzionale di sfondo, finestra accesa di una casa (cornice C2 s01-c2 Giro A — qualcuno impasta) ✅ canonica nel grafo

**Oggetti:**
- Carriola di vimini (oggetto-simbolo Camminanti) → ⚠️ descritta in `collettivi/camminanti/scheda.md` ma no prompt grok separato. Considerare se serve creare scheda oggetto + prompt.

**Cornice del mondo applicata:**
- s01-c1 (Giro D — venti/stagioni): Camminante anonimo con carriola di vimini, mano via dal manico saluto
- s01-c2 (Giro A — cibo): finestra accesa di una casa, qualcuno impasta

**Status composizione:** ⏳ TBD. Pronto quando Piazza ha img canonica.

---

### s01_h03 — Pagina 3 — Via che Sale, salita ai Pascoli

**Personaggi:** Gabriel, Elias, Noah (in fila salgono)

**Luogo:** Via che Sale (sentiero salita, tratto medio-basso)
- Prompt: ❌ **MANCA** `visual/luoghi/quartiere_aria/via_che_sale/prompt_grok.md` (i sentieri Tier A non hanno prompt grok dedicato finora)
- La scheda esiste con dettagli stabili Tier A (`vcs_d01_pietra_dei_tre_passi`, `vcs_d02_cardo_isolato`, etc.)
- Img: ❌ 0

**Dettaglio stabile Tier A in scena:**
- `vcs_d01_pietra_dei_tre_passi` (canonica s01) — "pietra piatta posata di traverso. Tre passi prima il sentiero pianeggia, tre dopo." ✅ canonical nel grafo

**Sfondo:**
- Le Gemelle in fondo, due cime tagliate dal cielo (Montagne Gemelle in distanza)
- Villaggio sotto piccolo piccolo

**Frasi-codice:**
- «Da lassù si vede tutta l'isola» (Gabriel)
- «E forse anche più in là» (Elias)

**Gap critico:** Via che Sale prompt grok da creare per illustratore.

**Status composizione:** ⏳ TBD. Bloccato su prompt grok via_che_sale + img canoniche dei 3 fratelli.

---

### s01_h04 — Pagina 4 — Nebbia improvvisa sopra i Pascoli

**Personaggi:** Gabriel, Elias, Noah (perdono visibilità nella nebbia)

**Luogo:** Pascoli Alti, sopra il sentiero, in nebbia fitta
- Prompt: ✅ `visual/luoghi/quartiere_aria/pascoli_alti/prompt_grok.md`
- Img: ❌ 0
- **Variante atmosferica:** nebbia fitta improvvisa che cala. Il prompt esistente NON copre questa modalità "nebbia". Va aggiunta come Veduta 2 al prompt grok pascoli_alti, o creata variante dedicata nella scheda.

**Frasi-codice:**
- «Torniamo. Andiamo via di qui. Andiamo via.» (Noah)
- «Possiamo tenerci per mano» (Elias)

**Gap minore:** prompt grok Pascoli Alti necessita variante "nebbia" per s01.

**Status composizione:** ⏳ TBD.

---

### s01_h05 — Pagina 5 — I tre seduti nella nebbia, in attesa

**Personaggi:** Gabriel, Elias, Noah (seduti per terra sul sentiero)

**Luogo:** Pascoli Alti, sentiero in nebbia (continuità con h04)

**Atmosfera sonora canonica (per illustrazione: implicita, ma rappresentabile):**
- pietra che rotola tre volte (alto, oltre nebbia)
- una capra risponde a un'altra capra (sotto, oltre nebbia)
- "il vento, dietro la collina, stava ancora dormendo"

**Status composizione:** ⏳ TBD.

---

### s01_h06 — Pagina 6 — Vento aperto rivela il bordo del Burrone

**Personaggi:** Gabriel, Elias, Noah (in piedi, vedono il bordo)

**Luogo:** Bordo del Burrone, ancora con tracce di nebbia
- Prompt: ✅ `visual/luoghi/quartiere_aria/burrone/prompt_grok.md`
- Img: ❌ 0
- **Variante:** vista dal bordo con nebbia che si apre. Prompt esistente è "panoramica gola"; va considerata una vista dal ciglio del bordo.

**Status composizione:** ⏳ TBD.

---

### s01_h07 — Pagina 7 — Cengia con lichene verde verso Grunto

**Personaggi:** Gabriel, Elias, Noah (salgono lungo la cengia)

**Luogo:** Cengia tra le Montagne Gemelle (sentiero stretto in mezzaroccia)
- ⚠️ Non c'è scheda dedicata "cengia"; rientra nelle Montagne Gemelle / Burrone
- Prompt: parziale via `montagne_gemelle/prompt_grok.md` ma quel prompt è "vista da lontano". Per la cengia stretta serve un prompt close-up — può essere generato come variante della scheda Burrone o Montagne Gemelle.
- Detail: "lichene verde che faceva quasi parete", sole tocca pietra "d'oro"

**Gap minore:** prompt cengia/sentiero in mezzaroccia da considerare. Per ora si può comporre con prompt Burrone in modalità "cengia ascendente".

**Status composizione:** ⏳ TBD.

---

### s01_h08 — Pagina 8 — Incontro con Grunto + pagnotta consegnata ⭐ scena chiave

**Personaggi:**

| Personaggio | Prompt | Img canoniche |
|---|---|---|
| Gabriel, Elias, Noah | ⚠️ Gabriel/Elias img mancanti | Noah ok |
| Grunto | ✅ | ✅ 4 imm (`cengia`, `via`, `frammento`, `turnaround`) |

**Luogo:** Cengia / vicino Grotta di Grunto
- Prompt: ✅ `grotta_grunto/prompt_grok.md` (close-up alcove)
- Img: ❌ 0 (da generare con prompt)

**Oggetti in scena:**
- pagnotta_forno (consegnata) → ✅ prompt
- cicatrice_grunto (visibile sul fianco sx) → ✅ prompt + (compresa nelle img canoniche di Grunto)
- pietra piatta tra loro (oggetto naturale, prop) → no scheda

**Frasi-codice critiche:**
- *Grunt.* (Grunto, vocalizzazione)
- *Via.* (Grunto, gesto+vocalizzazione)
- «Buono.» (Grunto, dopo aver mangiato la pagnotta — frase canonica saga)

**Status composizione:** ⏳ TBD. Gap personaggi (Gabriel+Elias).

---

### s01_h09 — Pagina 9 — Discesa al tramonto, Pascoli vuoti

**Personaggi:** Gabriel, Elias, Noah (in discesa)

**Luogo:** Pascoli Alti (in discesa, tramonto, le Gemelle alle spalle "oro pallido")
- Prompt: ✅ `pascoli_alti/prompt_grok.md`
- Img: ❌ 0
- **Variante atmosferica:** tramonto/golden hour. Il prompt principale è generico "morning/afternoon". Va aggiunta variante "tramonto" o noted nel prompt scena.

**Oggetti minori:**
- bastoncino di Noah (prop temporaneo, lasciato cadere) → no scheda, prop di scena

**Status composizione:** ⏳ TBD.

---

### s01_h10 — Pagina 10 — Forno sera: Fiamma dà cornetto a Noah

**Personaggi:**
- Fiamma ✅ (modalità "ferma" o "sistema piano del forno")
- Gabriel, Elias, Noah ⚠️ (Gabriel+Elias img mancanti)

**Luogo:** Forno (interno, sera tardi)
- Prompt: ✅ atlante chiuso
- Img canonica reference: `forno_canonica_v1_dispensa_pranzo.jpg` (per scena intima sera) o `forno_canonica_v1_laboratorio_panoramica.jpg`
- **Variante atmosferica:** sera/luce candela invece di alba. Le canoniche sono mattino — la composizione finale può modulare la palette in post.

**Oggetti in scena:**
- cornetto (variante ridotta di pagnotta) → 📝 NON ha scheda dedicata. **Aggiunta da prosa al canone:** considerare se aggiungere "cornetto" come variante in `pagnotta_forno/scheda.md` (sezione Variabilità ammessa).

**Frasi-codice:**
- (silenzio: Fiamma "non chiese com'era andata" — gesto, non parola)

**Status composizione:** ⏳ TBD.

---

## Aggiunte dalla prosa al canone (catalogo/Bible — NON al grafo)

Elementi nuovi introdotti dalla prosa definitiva s01 che vanno integrati nei file canonici del catalogo. Il grafo NON va modificato (read-only); le aggiunte vanno solo nelle schede `visual/`.

### 1. 📝 Vapore alla finestra del Forno (h01)
**Dove aggiungere:** `visual/luoghi/quartiere_fuoco/forno/scheda.md`, sezione "Aspetto / forma — geografia generale" sotto-area "Esterno", o "Sala Laboratorio" (atmosfera).
**Cosa aggiungere:** "Quando Fiamma impasta nelle ore fredde (alba inverno) si vede vapore farsi strada dalle finestre — il calore del forno + l'aria fredda esterna."
**Priorità:** bassa (dettaglio atmosferico, ma utile per illustratore).

### 2. 📝 Cornetto come variante della pagnotta (h10)
**Dove aggiungere:** `visual/oggetti/pagnotta_forno/scheda.md`, sezione "Variabilità ammessa".
**Cosa aggiungere:** "Variante 'cornetto': pezzo più piccolo, forma allungata leggermente arcuata, stessa pasta. Fiamma ne fa per i cuccioli, da mangiare in piedi."
**Priorità:** media (riappare in altre storie? verificare s06 e s08).

### 3. 📝 Pietra dei tre passi conferma canonica (h03)
**Dove aggiungere:** già canonical in `world_conventions.path_details.paths.via_che_sale.details.vcs_d01_pietra_dei_tre_passi`. Nessuna aggiunta necessaria.
**Verifica:** la prosa definitiva ne legittima l'uso. ✅ Coerente.

---

## Gap operativi

### Critici (bloccano la composizione di alcuni hook)

1. **Gabriel + Elias: immagini canoniche mancanti** (per h01-h09 di s01 e per molte altre storie).
   - **Azione:** Ray genera le 8 immagini (4 per Gabriel + 4 per Elias) con i prompt grok già pubblicati.

2. **Via che Sale: prompt grok mancante** (per h03).
   - **Azione:** generare `visual/luoghi/quartiere_aria/via_che_sale/prompt_grok.md` come fatto per gli altri luoghi.

### Minori (gestibili in post-composizione)

3. **Pascoli Alti — variante "nebbia"** (h04, h05): aggiungere come Veduta 2 al prompt esistente.
4. **Burrone — variante "vista dal bordo"** (h06): aggiungere come Veduta 2.
5. **Cengia in mezzaroccia con lichene** (h07): considerare prompt close-up specifico (può rientrare in burrone o montagne_gemelle).
6. **Pascoli — variante "tramonto/golden hour"** (h09): aggiungere come variante atmosferica nei prompt esistenti.
7. **Carriola di vimini Camminante** (h02): valutare se serve scheda oggetto + prompt grok dedicato.

---

## Cosa serve per concludere s01

| Item | Tipo | Priorità |
|---|---|---|
| Generare 4 img Gabriel | personaggio | 🔴 critica |
| Generare 4 img Elias | personaggio | 🔴 critica |
| Creare prompt grok via_che_sale | luogo | 🔴 critica |
| Aggiungere variante "nebbia" pascoli_alti | luogo (scheda) | 🟡 minore |
| Aggiungere variante "vista bordo" burrone | luogo (scheda) | 🟡 minore |
| Aggiungere variante "tramonto" pascoli_alti | luogo (scheda) | 🟡 minore |
| Aggiungere "vapore finestra" forno scheda | catalogo | 🟢 bassa |
| Aggiungere "cornetto" variante pagnotta_forno | catalogo | 🟢 bassa |
| Generare 1 img canonica Piazza del Villaggio | luogo | 🟡 utile (ricorrente) |
| Generare 1 img canonica Pascoli Alti (basic) | luogo | 🟡 utile |
| Generare 1 img canonica Burrone | luogo | 🟡 utile |
| Generare 1 img canonica Grotta Grunto | luogo | 🟡 utile |
| Generare 1 img canonica Montagne Gemelle | luogo | 🟢 nice-to-have (sfondo lontano) |
| Comporre 10 immagini hook s01 (testo overlay + scena) | output finale | da definire dopo |

---

## Pattern checklist per altre storie

Questo inventario è il **modello per le altre 11 storie**. Quando ci si attacca a sNN si replica lo schema:

1. **Riepilogo** (metriche, gap)
2. **Hook per hook** con: personaggi/luogo/oggetti × stato prompt/immagini
3. **Aggiunte dalla prosa al canone** (catalog-only, mai grafo)
4. **Gap operativi** divisi per priorità
5. **Lista cosa serve per concludere**

Successivamente uno script Python potrà generare lo skeleton automaticamente parsando:
- `pipeline_narrativa/storie_finali/sNN.md` (testo)
- `pipeline_narrativa/story_graph.json` (canone)
- `visual/personaggi/.../immagini/` (audit immagini)
- `visual/luoghi/.../prompt_grok.md` + immagini (audit)

---

## Riferimenti

- Testo definitivo: `pipeline_narrativa/storie_finali/s01_la_nebbia_delle_montagne_gemelle.md`
- Brief writing: `pipeline_narrativa/writing_briefs/s01_writing_brief.md`
- Hook visivi nel grafo: `pipeline_narrativa/story_graph.json#stories.s01.visual_anchors.scene_hooks`
- Cornici: `pipeline_narrativa/story_graph.json#stories.s01.cornice_dettagli`
