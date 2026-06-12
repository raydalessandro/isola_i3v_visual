# Skill — Agente illustratore

> Per **istanze IA** o **collaboratori umani** che si connettono alla repo `isola_i3v_visual` per **caricare immagini HD** (illustrazioni di scena, ritratti, intro volume) generate via Grok Imagine o altro tool.
>
> Versione: 1.1 — 2026-06-10 (aggiunto §0 "Decisione PRIMA di tutto: dove va il file?" — i ritratti vanno SEMPRE al catalogo, mai al volume)

---

## TL;DR (in 60 secondi)

1. **§0 PRIMA DI TUTTO**: classifica ogni file in uno dei 3 contesti (sotto). Sbagliare contesto = rilavorazione + disallineamento canone.
2. **Formato:** JPEG qualità 95, RGB profilo sRGB, min **1824×2736 px** verticale 2:3, metadato DPI = 300.
3. **Dove:** SEMPRE in una subdir `_hd/`, MAI nella cartella padre. **MAI sostituire i low-res esistenti.**
4. **Branch:** una branch per scope coerente (es. `claude/hd-storia-s02`, `claude/hd-intro-v02`, `claude/hd-catalogo-primari`). Mai pushare su `main`.
5. **Commit:** **un solo commit** per branch, messaggio descrittivo. NO 34 commit atomici "Aggiunge X / Rimuove Y".
6. **NO contaminazioni:** la branch immagini contiene SOLO immagini. NO codice app web, NO modifiche a `.md`, NO altro.
7. **PR + attesa OK Ray:** apri PR verso `main`, NON mergiare in autonomia.

---

## 0. Decisione PRIMA DI TUTTO: dove va il file?

> ⚠️ Errore storico (2026-05-19 → 2026-06-10): branch dell'illustratore che caricavano **ritratti di personaggi** dentro `_volumi/v0N/_hd/` come "intro volume", quando erano in realtà **reference saga riusabili** che dovevano stare nel catalogo. Risultato: doppio canone non sincronizzato, sito che mostrava arte vecchia, recovery manuale. Da non ripetere.

**Albero decisionale** — applicare per OGNI file PRIMA di scegliere path e nome:

```
1. Il soggetto è un personaggio/oggetto/luogo del catalogo (visual/<categoria>/<id>/) ?

   ├── SÌ ─→ è un RITRATTO/VISTA del soggetto (singolo, coppia, gruppo) ?
   │        ├── SÌ ─→ contesto 1c (CATALOGO) — sempre, anche se prodotto durante
   │        │         la lavorazione di un volume specifico.
   │        │         I ritratti sono reference saga riusabili.
   │        │
   │        └── NO → è una scena specifica (azione, contesto narrativo,
   │                  illustrazione di pagina libro) ?
   │                  ├── pagina libro fisica di una storia ─→ contesto 1a (_scene/sNN/)
   │                  └── illustrazione decorativa per un volume (sigillo,
   │                       composizione narrativa intro non-ritratto, ecc.) ─→ contesto 1b (_volumi/v0N/)
   │
   └── NO ─→ è un'illustrazione narrativa specifica del libro ?
            ├── pagina hook storia ─→ contesto 1a
            ├── decoro/sigillo/intro del volume ─→ contesto 1b
            └── altro ─→ chiedi a Ray prima di pushare
```

**Casi tipici in cui ci si è sbagliati in passato:**

| Soggetto | Contesto sbagliato (storico) | Contesto giusto |
|---|---|---|
| Fiamma di fronte (ritratto) | `_volumi/v01/_hd/v01_intro_fiamma_hd.jpg` | `visual/personaggi/individuali/primari/fiamma/immagini/_hd/fiamma_canonica_v1_ritratto_hd.jpg` |
| Mèmolo che tiene Pun (coppia) | `_volumi/v01/_hd/v01_intro_memolo_pun_hd.jpg` | `visual/personaggi/individuali/primari/memolo/immagini/_hd/memolo_canonica_v1_con_pun_hd.jpg` |
| I 3 fratelli insieme | `_volumi/v01/_hd/v01_intro_bambini_hd.jpg` | `visual/personaggi/individuali/bambini/gabriel/immagini/_hd/gabriel_canonica_v1_con_fratelli_hd.jpg` (sotto il maggiore) |
| Pagina 3 di s01 (scena) | OK | `_scene/s01/_hd/s01_h02a_hd.jpg` |
| Sigillo narrativo Vol 1 (decoro) | OK | `_volumi/v01/_hd/v01_sigillo_hd.jpg` (futuro) |

**Regola operativa:** `_volumi/v0N/_hd/` contiene SOLO illustrazioni *prodotte per* il volume e non riusabili come reference. **Tutti i ritratti, anche se realizzati durante la lavorazione di un volume, vanno al catalogo.**

---

## 1. I tre contesti di destinazione

### 1a. Hook di una storia (scene composte per pagina libro fisica)

```
pipeline_narrativa/storie_finali/_scene/sNN/_hd/sNN_hMMx_hd.jpg
```

| Token | Esempio | Note |
|---|---|---|
| `sNN` | `s02` | id storia, 01..12 |
| `hMM` | `h01`..`h10` | id hook narrativo |
| `x` | `a`, `b`, `c`... | pagina libro fisica (subhook) |
| `_hd` | obbligatorio | suffisso che marca la versione stampa |

**Riferimento autorevole:** `pipeline_narrativa/storie_finali/_scene/README.md`.

**Il low-res `_scene/sNN/sNN_hMMx.jpg` resta dov'è** (NON va toccato, è il reference digitale).

### 1b. Introduzione di un volume

```
pipeline_narrativa/storie_finali/_volumi/v0N/_hd/v0N_intro_<slug>_hd.jpg
```

| Token | Esempio | Note |
|---|---|---|
| `v0N` | `v01`..`v04` | id volume (1:1 con cicli A/B/C/D) |
| `intro` | fisso | sezione del volume (oggi: solo `intro`; futuri: `porta`, `congedo`...) |
| `<slug>` | `fiamma`, `bartolo_toba` | lowercase, snake_case, univoco |

**Riferimento autorevole:** `pipeline_narrativa/storie_finali/_volumi/v01/README.md` (modello per v02..v04).

### 1c. Catalogo visual (reference canoniche personaggi/oggetti/luoghi)

```
visual/<categoria>/<sottocat>/<id>/immagini/_hd/<id>_canonica_v1_<vista>_hd.jpg
```

| Token | Esempio |
|---|---|
| `<categoria>` | `personaggi`, `oggetti`, `luoghi`, `venti`, `visual_signatures` |
| `<sottocat>` | per personaggi: `individuali/{bambini,primari,secondari,cuccioli}` o `collettivi` |
| `<id>` | id univoco entità, es. `fiamma`, `bartolo`, `grembiule_fiamma` |
| `<vista>` | `fronte`, `tre_quarti`, `profilo`, `dettaglio`, `turnaround` |

Esempio: `visual/personaggi/individuali/primari/fiamma/immagini/_hd/fiamma_canonica_v1_fronte_hd.jpg`

**Le `_canonica_v1_*.jpg` low-res esistenti restano nella cartella `immagini/` (NON toccare).** La HD va nella subdir `_hd/` con suffisso `_hd`.

---

## 2. Specifiche file

| Parametro | Valore |
|---|---|
| Formato | **JPEG** (estensione `.jpg`, MAI `.jpeg` con due caratteri) |
| Qualità JPEG | **95** (encoder Grok/Imagine/Photoshop) |
| Profilo colore | **sRGB** (RGB, NO CMYK — la conversione è dello stampatore) |
| Risoluzione minima | **1824×2736 px** verticale 2:3 (calcolata sul fit di `build_volume.py`: A5+bleed = 1824×2556 a 300 DPI, l'immagine 2:3 minima che copre è 1824×2736). Standard precedente 1664×2496 accettato per s01 v1. |
| Risoluzione ideale | **2000×3000 px** o superiore (margine per ridimensionamento stampa) |
| Peso file tipico | 300-700 KB per pagina, fino a ~1 MB se molto dettagliata |
| Metadata DPI | **impostare a 300** (informativo per lo stampatore; il rendering del compositore usa pixel + dimensione fisica) |

**Naming:**
- Sempre **lowercase** (`fiamma_hd.jpg`, mai `Fiamma_HD.JPG`)
- **snake_case** (sottolineato, mai spazi né maiuscole)
- Estensione **`.jpg`** (no `.jpeg`, no `.JPG`)
- Suffisso **`_hd`** obbligatorio per la versione HD

---

## 3. Workflow standard (passo-passo)

### Step 0 — Pull main aggiornato

```bash
git checkout main
git pull origin main
```

### Step 1 — Crea branch dedicata

Naming branch (uno scope = una branch):

| Scope | Naming branch |
|---|---|
| HD hook di una storia | `claude/hd-storia-sNN` (es. `claude/hd-storia-s02`) |
| HD intro di un volume | `claude/hd-intro-vNN` (es. `claude/hd-intro-v02`) |
| HD catalogo (un blocco logico) | `claude/hd-catalogo-<blocco>` (es. `claude/hd-catalogo-primari`, `claude/hd-catalogo-cuccioli`, `claude/hd-catalogo-oggetti`) |

```bash
git checkout -b claude/hd-storia-s02
```

### Step 2 — Crea la subdir `_hd/` e copia i file

```bash
mkdir -p pipeline_narrativa/storie_finali/_scene/s02/_hd
cp /path/to/upload/s02_h01a.jpg pipeline_narrativa/storie_finali/_scene/s02/_hd/s02_h01a_hd.jpg
cp /path/to/upload/s02_h01b.jpg pipeline_narrativa/storie_finali/_scene/s02/_hd/s02_h01b_hd.jpg
# ...etc per tutti gli hook della storia
```

**Checklist pre-commit:**
- [ ] Tutti i file sono in `_hd/`, non nella cartella padre
- [ ] Tutti i file hanno suffisso `_hd.jpg`
- [ ] I file low-res in `_scene/sNN/sNN_hMMx.jpg` sono **invariati** (`git status` non li mostra)
- [ ] Nessun file fuori dallo scope (no modifiche a `.md`, no codice app web, ecc.)
- [ ] Verifica risoluzione e formato con:
  ```bash
  python3 -c "from PIL import Image; import sys, os; \
  [print(f, Image.open(f).size, Image.open(f).mode) for f in sorted(sys.argv[1:])]" \
  pipeline_narrativa/storie_finali/_scene/s02/_hd/*.jpg
  ```

### Step 3 — Un solo commit

```bash
git add pipeline_narrativa/storie_finali/_scene/s02/_hd/
git status   # verifica che siano SOLO i file di scope
git commit -m "s02: aggiunte 17 JPG HD q95 in _scene/s02/_hd/ per stampa libro"
```

**Messaggio commit — pattern:**

| Scope | Pattern messaggio |
|---|---|
| Storia | `sNN: aggiunte N JPG HD q95 in _scene/sNN/_hd/ per stampa libro` |
| Intro volume | `volume N intro: aggiunte N JPG HD q95 in _volumi/vNN/_hd/` |
| Catalogo | `catalogo: aggiunte N JPG HD q95 (visual/<...>/_hd/) per <blocco>` |

### Step 4 — Push + PR

```bash
git push -u origin claude/hd-storia-s02
```

Apri PR verso `main`. Titolo identico al messaggio commit. Corpo: 1-2 righe descrittive + lista file aggiunti.

**NON mergiare la PR.** Aspetta che Ray (o agente in modalità review) faccia controllo + approvazione + merge.

---

## 4. Vincoli (cosa NON fare)

| ❌ MAI | ✅ Sempre |
|---|---|
| Sostituire un low-res con la HD (`_scene/sNN/sNN_hMMx.jpg` ← non toccare) | HD va in `_hd/`, low-res resta dov'è |
| Cambiare estensione dei marker `@image` nei `.md` | Marker continuano a puntare a low-res |
| `git push origin main` (push diretto) | Sempre branch dedicata + PR |
| 34 commit atomici `Aggiunge X / Rimuove Y` | Un commit per branch |
| Mischiare HD + codice app web + modifiche `.md` nella stessa branch | Una branch = uno scope |
| Naming con spazi, maiuscole, accenti, estensioni varie (`.jpeg`, `.JPG`, `.png`) | Solo `_hd.jpg` lowercase snake_case |
| Pushare PNG (5-10 MB cad.) | JPEG q95 (300-700 KB cad.) |
| `git push --force`, `--no-verify`, `--amend` su commit altrui | Push pulito sulla branch propria |
| Caricare file fuori dai 3 contesti (1a/1b/1c) | Sempre uno dei 3 contesti — se serve un 4°, chiedere prima a Ray |

---

## 5. Cosa controlla la review (Ray o agente review)

Prima del merge in `main`, verifica:

1. **§0 Classificazione contesto** — per OGNI file: è un ritratto? → catalogo (1c). È una scena? → _scene/ (1a). È un decoro specifico volume? → _volumi/ (1b). Se hai dubbio anche solo per UN file → chiedi a Ray prima del merge. **Sbagliare il contesto è il bug più comune e crea disallineamento canone difficile da recuperare.**
2. **Path corretto** — file in `_hd/` del contesto giusto
3. **Naming corretto** — `<id>_hd.jpg` lowercase snake_case
4. **Formato corretto** — JPEG q95, RGB sRGB, ≥1824×2736 px verticale 2:3, metadato DPI = 300
5. **Diff pulito** — solo file aggiunti, nessuna modifica accidentale a low-res o `.md`
6. **Commit pulito** — un solo commit con messaggio standard
7. **Nessuna contaminazione** — niente codice app web, niente file fuori scope
8. **Branch up-to-date con main** — niente conflitti
9. **CI verde** — test + audit + build (il cancello impedisce automaticamente regressioni nel canone navigabilità grafo↔immagini)

Se anche solo uno di questi fallisce, la review chiede modifiche o chiude la PR.

---

## 6. Esempi positivi

### Esempio s02 (storia)

```
Branch:  claude/hd-storia-s02
Commit:  "s02: aggiunte 17 JPG HD q95 in _scene/s02/_hd/ per stampa libro"
File:
  + pipeline_narrativa/storie_finali/_scene/s02/_hd/s02_h01a_hd.jpg
  + pipeline_narrativa/storie_finali/_scene/s02/_hd/s02_h01b_hd.jpg
  + ... (17 file totali)
```

### Esempio intro v02 (volume 2) — CASO RARO

> ⚠️ Aggiornato 2026-06-10: **i ritratti dei personaggi del Ciclo B NON vanno qui**, vanno al catalogo (vedi §0). `_volumi/v02/_hd/` contiene SOLO illustrazioni prodotte appositamente per il volume e non riusabili come reference saga (es. composizioni narrative dell'intro non-ritratto, sigilli, decori). Se la tua branch v02 contiene ritratti, riclassifica i file prima di pushare.

```
Branch:  claude/hd-intro-v02
Commit:  "volume 2 intro: aggiunte composizioni narrative HD q95"
File:
  + pipeline_narrativa/storie_finali/_volumi/v02/_hd/v02_sigillo_b_hd.jpg
  + pipeline_narrativa/storie_finali/_volumi/v02/_hd/v02_porta_intreccio_hd.jpg
  + ... (solo file specifici del volume)
```

### Esempio catalogo primari (blocco logico)

```
Branch:  claude/hd-catalogo-primari
Commit:  "catalogo: aggiunte 6 JPG HD q95 reference canoniche personaggi primari"
File:
  + visual/personaggi/individuali/primari/bartolo/immagini/_hd/bartolo_canonica_v1_fronte_hd.jpg
  + visual/personaggi/individuali/primari/fiamma/immagini/_hd/fiamma_canonica_v1_fronte_hd.jpg
  + ... (6 file)
```

---

## 7. Quando in dubbio

1. Leggi i README dei 3 contesti:
   - `pipeline_narrativa/storie_finali/_scene/README.md`
   - `pipeline_narrativa/storie_finali/_volumi/v01/README.md`
   - `_visual_pipeline/README.md` (per catalogo)
2. Leggi questa skill (`skills/illustratore/SKILL.md`) di nuovo
3. Se ancora dubbio: **chiedi a Ray prima di pushare**

Meglio una domanda in più che una PR da chiudere.

---

## 8. Stato corrente (2026-06-10)

- Standard `_hd/` introdotto 2026-05-19, regola §0 "Decisione PRIMA DI TUTTO" aggiunta 2026-06-10 dopo il recovery che ha spostato i ritratti dal `_volumi/` al catalogo.
- Applicazioni in repo:
  - `_scene/s01/_hd/` — 17 file HD storia 1 (✅), low-res sincronizzati 2026-06-10
  - `_volumi/v01/_hd/` — 1 file (Stria HOLD, attesa versione non-volante)
  - `visual/personaggi/individuali/*/immagini/_hd/` — 11 reference promossi da `_volumi/v01/` (Fiamma, Grunto, Nodo, Salvia, Zolla, Pun, Bru + 3 coppie + 3 fratelli sotto Gabriel)
- Da fare:
  - 11 storie restanti (s02..s12) — una branch per storia, naming `_scene/sNN/_hd/`
  - Reference catalogo restanti (luoghi, oggetti, signatures) — branch per blocco logico
  - Volumi v02..v04 — solo per illustrazioni NON-ritratto specifiche del volume
