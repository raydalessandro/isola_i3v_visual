# Prompt Grok Imagine — `<id_personaggio>`

**Versione:** 1.0
**Data:** YYYY-MM-DD
**Scopo:** generare le illustrazioni canoniche di riferimento del personaggio. Queste immagini fissano l'aspetto canonico per tutte le illustrazioni successive.

**Numero di immagini canoniche da generare per personaggio: 4**
- Img 1: veduta principale fronte (3:4)
- Img 2: in azione (4:5) — modalità default
- Img 3: modalità alternativa (4:5) — se il personaggio ha modalità multiple visivamente distinguibili
- Img 4: turnaround 4 vedute (16:9) — style sheet

---

## 🎨 STYLESHEET CANONICA SAGA — riusare in OGNI prompt

⚠️ **Incollare INVARIATO da** `_canone/01_SAGA_STYLESHEET_v1.md`

```
[INSERIRE QUI TESTO DA 01_SAGA_STYLESHEET_v1.md]
```

---

## 📐 CANONE PERSONAGGIO — `<id_personaggio>` (riusare in TUTTI i prompt che lo includono)

Questo blocco descrive il canone fisso del personaggio. Va riusato identico in ogni prompt che lo include, in tutte le 12 storie e nei materiali di scena.

```
CHARACTER — <Nome>:
[Sintesi 2-3 righe: specie, postura, ruolo, riconoscibilità a colpo d'occhio]

[Aspetto fisico dettagliato:
- Specie e postura
- Statura relativa (con riferimento a Gabriel come 1.0 GU se rilevante)
- Corporatura
- Pelo/piume/squame: colori specifici, distribuzione
- Coda/orecchie/muso/becco/guscio (a seconda della specie)
- Occhi: colore, espressione canonica
- Mani/zampe: colore, "calzini" scuri se applicabili
- Età narrativa (giovane/adulto/anziano)]

Clothing (always present, never changes):
[Lista completa dell'outfit canonico, capo per capo, con colore + materiale + dettagli + stato d'uso]

Color palette of <Nome>: [lista colori chiave]

[Modalità comportamentali se applicabili:
- "<Mode A>": [descrizione visiva]
- "<Mode B>": [descrizione visiva]]

NEVER: [lista cliché da evitare specifici per questo personaggio]
```

---

## 🖼️ IMMAGINE 1 — Veduta canonica principale (fronte, modalità default)

**Filename suggerito:** `<id>_canonica_v1_fronte.png`
**Aspect ratio:** 3:4 (portrait)

```
[STYLESHEET CANONICA SAGA]

[CANONE PERSONAGGIO — <Nome>]

SCENE — Canonical full-body front view:
[Descrizione scena: posa, ambiente di sfondo (dimora canonica), interazione con oggetti tipici, espressione, luce, atmosfera]

Lighting: [tipo di luce coerente col quartiere/ambiente]

Composition: full body visible, head to feet, centered. Aspect ratio 3:4 (portrait). Standard reference pose.
```

---

## 🖼️ IMMAGINE 2 — Veduta in azione (modalità default)

**Filename suggerito:** `<id>_canonica_v1_azione.png`
**Aspect ratio:** 4:5 (portrait)

```
[STYLESHEET CANONICA SAGA]

[CANONE PERSONAGGIO — <Nome>]

SCENE — <Nome> in default activity:
[Descrizione scena di lavoro/azione tipica del personaggio: cosa sta facendo, ambiente, dettagli, espressione, postura]

Lighting: [coerente]

Composition: medium shot, from waist up to slightly above the head. Aspect ratio 4:5 (portrait). Captures <Nome> in their natural state.
```

---

## 🖼️ IMMAGINE 3 — Modalità alternativa (opzionale)

**Filename suggerito:** `<id>_canonica_v1_<modalità>.png`
**Aspect ratio:** 4:5 (portrait)

⚠️ **Generare solo se il personaggio ha modalità comportamentali visivamente distinguibili** (es: Fiamma chiacchiera/ferma/brace; Bartolo se ha modalità tipiche; etc.)

```
[STYLESHEET CANONICA SAGA]

[CANONE PERSONAGGIO — <Nome>]

SCENE — <Nome> in <modalità alternativa>:
[Descrizione scena specifica per questa modalità]

Lighting: [coerente con la modalità]

Composition: [coerente]
```

---

## 🖼️ IMMAGINE 4 — Style sheet / turnaround (4 vedute)

**Filename suggerito:** `<id>_turnaround_v1.png`
**Aspect ratio:** 16:9 (landscape)

```
[STYLESHEET CANONICA SAGA]

[CANONE PERSONAGGIO — <Nome>]

SCENE — Character turnaround sheet for visual consistency:
A character reference sheet showing <Nome> in 4 standard views, evenly 
spaced from left to right against a neutral cream background with a 
faint horizontal ground line. All four views show <them> in the same 
neutral standing pose: arms relaxed at sides, feet slightly apart, 
neutral attentive expression. No background scenery, no props, just 
the character clearly visible for reference.

Views from left to right:
1. FRONT view — facing viewer directly
2. THREE-QUARTER view — turned 45 degrees to <their> left
3. SIDE PROFILE — full left profile, [tail/specific feature] clearly 
   visible
4. BACK view — from behind, showing the full back, [outfit ties/back 
   detail]

The character must look IDENTICAL across all four views: same fur/feathers 
color, same outfit, same height, same proportions. This is a model sheet 
for visual consistency reference, NOT four separate illustrations.

Lighting: even neutral lighting, no dramatic shadows, soft watercolor 
wash on a cream background.

Composition: aspect ratio 16:9 (landscape), four figures side by side, 
full body each, equal spacing.
```

---

## 🚫 NEGATIVE PROMPT GLOBALE — sempre incluso

⚠️ **Incollare INVARIATO da** `_canone/01_SAGA_STYLESHEET_v1.md`

```
[INSERIRE QUI BLOCCO NEGATIVE da 01_SAGA_STYLESHEET_v1.md]
+ negative specifici per questo personaggio (sexy/glamour/disney-cute/etc. a seconda dei cliché)
```

---

## 🛠️ Note tecniche per Grok Imagine

- **Modalità consigliata**: illustrazione / acquerello / picture book.
- **Aspect ratio**: come specificato in ciascuna immagine.
- **Seed**: salvare il seed dopo la prima generazione canonica per riuso futuro.
- **Iterazione**: 4-6 varianti per immagine, selezionare migliore secondo checklist.
- **Coerenza tra le 4 immagini**: usare stesso seed o seed adiacenti, generare in sequenza.

---

## ✅ Checklist post-generazione

Per ciascuna delle 4 immagini canoniche, verificare:

- [ ] Stylesheet saga rispettata (painterly picture book, no realistic, no cartoon, no 3D)
- [ ] Postura corretta (bipede/quadrupede a seconda del canone)
- [ ] Colori del pelo/piume/etc. fedeli al canone
- [ ] Outfit canonico completo presente
- [ ] Stato d'uso corretto (sporco/pulito/infarinato/etc.)
- [ ] Occhi nel canone (colore, espressione)
- [ ] Niente cliché vietati
- [ ] Modalità comportamentale corretta per ciascuna immagine
- [ ] Sfondo coerente con dimora/quartiere
- [ ] Coerenza tra le 4 immagini (stesso personaggio riconoscibile)

Se 2+ checkbox falliscono per un'immagine, rigenerare quella singola immagine — non procedere con immagini canoniche imperfette.
