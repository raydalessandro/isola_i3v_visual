# 🎨 _visual_pipeline/_api/ — Generazione immagini canoniche (workflow esterno)

> **Per chi:** la persona che si occupa di generare le immagini con Flux/OpenAI sul proprio PC.
> **Coordinamento:** Ray (autore + push su main).

---

## 🎯 Cosa fa questo modulo

Genera immagini canoniche dei personaggi e oggetti della saga **L'Isola dei Tre Venti** a partire dai prompt già preparati da Ray + Claude.

**Tu non scrivi i prompt.** Sono già pronti dentro la repo. Tu li **esegui**.

---

## 📋 Workflow operativo

```
1. git pull (sincronizzati con la repo)
2. Apri i prompt dei personaggi del batch corrente
3. Esegui Flux con quei prompt → 4 immagini per personaggio
4. (Eventuale) tuning del prompt se l'immagine non torna bene
5. Mandi le immagini in zip via Telegram a Ray
6. Ray le pusha su main al posto giusto
```

**Il tuo output sono SOLO file immagine.** Non commiti niente, non modifichi codice.

---

## ⚙️ Setup iniziale (una volta sola)

### 1. Clona la repo

```bash
git clone https://github.com/raydalessandro/isola_i3v_visual.git
cd isola_i3v_visual/_visual_pipeline/_api/
```

### 2. Installa dipendenze Python

```bash
python3 -m venv venv
source venv/bin/activate         # Linux/Mac
# venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 3. Configura le chiavi API

```bash
cp .env.example .env
```

Poi apri `.env` con un editor e compila:
- `FAL_KEY` → la tua chiave [fal.ai](https://fal.ai) (obbligatoria per Flux)
- `OPENAI_API_KEY` → chiave [OpenAI](https://platform.openai.com/api-keys) (opzionale, solo se usi `openai_image_gen.py`)

> ⚠️ **`.env` è già nel `.gitignore`** — non verrà committato. Non rimuoverlo dal gitignore mai.

### 4. Test rapido

```bash
python example_generate.py
```

Deve generare 1 immagine `output_test.png` (~$0.04). Se funziona, sei pronto.

---

## 🚀 Generare le immagini di un personaggio

### Passo 1 — Trova il prompt del personaggio

I prompt vivono in:

```
visual/personaggi/individuali/<categoria>/<id>/prompt_grok.md
```

Esempi già pronti:
- `visual/personaggi/individuali/primari/fiamma/prompt_grok.md` ✅ (4 immagini già generate)
- `visual/personaggi/individuali/primari/bartolo/prompt_grok.md` ✅ (4 immagini già generate)

Quelli da fare avranno il `prompt_grok.md` ma non avranno ancora i file in `immagini/`.

> **Nota storica:** il file si chiama `prompt_grok.md` per ragioni storiche (la pipeline è nata con Grok Imagine). Ora lo leggi tu e lo passi a Flux. Stesso contenuto, provider diverso.

### Passo 2 — Apri il prompt

Ogni `prompt_grok.md` contiene:
- Un blocco **CHARACTER** con descrizione canonica (aspetto, palette, abbigliamento, postura)
- Un blocco **STYLESHEET SAGA** (stile visivo da rispettare)
- 4 blocchi **SCENE** (uno per ogni immagine canonica: fronte, azione, modalità, turnaround)
- **Filename suggerito** per ogni immagine (es. `gabriel_canonica_v1_fronte.jpg`)
- **Aspect ratio** consigliato (3:4, 4:5, 16:9)
- **Negative prompt** generale e specifici

### Passo 3 — Genera con Flux Kontext Pro

Per ogni scena del personaggio:

```python
from dotenv import load_dotenv
load_dotenv(".env")

from flux_image_gen import generate_image

# Copia il prompt completo (CHARACTER + STYLESHEET + SCENE) dal .md
prompt = """[copia qui il blocco completo del prompt dal .md]"""

result = generate_image(
    prompt,
    tier="flux-kontext-pro",     # raccomandato per character consistency
    size="1024x1536",             # aspect 3:4 — adatto a libri
    seed=42,                      # opzionale, riproducibile
    reference_image="../../../visual/personaggi/individuali/primari/fiamma/immagini/fiamma_canonica_v1_fronte.jpg",
                                  # ⬆️ usa una immagine di Fiamma o Bartolo come reference
                                  # per allineare lo stile (importante!)
    output_path="gabriel_canonica_v1_fronte.jpg",
)
print(f"Generata. Costo: ${result.cost_usd}")
```

**Ripeti per le 4 scene del personaggio** (con filename diversi).

### Passo 4 — Coerenza stile (importante)

Per ogni nuovo personaggio, usa come `reference_image` una delle 4 immagini di Fiamma o Bartolo già validate:

```
visual/personaggi/individuali/primari/fiamma/immagini/fiamma_canonica_v1_fronte.jpg
visual/personaggi/individuali/primari/bartolo/immagini/bartolo_canonica_v1_fronte.jpg
```

Questo aiuta Flux Kontext Pro a mantenere lo stile acquerello/illustrazione della saga. Senza reference image, ogni personaggio rischia di avere un look diverso.

### Passo 5 — Verifica

Apri le 4 immagini generate e verifica con la **checklist post-generazione** in:

```
_visual_pipeline/_skill/CHECKLIST.md
```

Cose tipiche da controllare:
- ✅ Postura coerente con la scheda (es. Bartolo eretto dignitoso, mai gobbo)
- ✅ Outfit corretto (es. grembiule terracotta di Fiamma con farina)
- ✅ Colori palette saga (no neon, no saturazione AI)
- ✅ Scala coerente (Gabriel = 1.0 GU di riferimento)
- ❌ Nessun pattern AI bandito (vedi `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`)

### Passo 6 — Tuning (se serve)

Se l'immagine non torna bene:
- Cambia `seed` (genera variazione)
- Aggiusta il prompt (aggiungi dettagli specifici, rinforza palette)
- Prova `tier="flux-kontext-max"` ($0.08/img) se Pro non basta
- Per casi difficili: `openai_image_gen.edit_image()` con `input_fidelity="high"`

---

## 📤 Consegna a Ray

Quando hai le 4 immagini di un personaggio (o di un batch di personaggi):

1. **Crea una zip** chiamata `<id>_immagini.zip` o `batch_<data>_immagini.zip`
2. **Mandala a Ray via Telegram**
3. Ray le pusha su main al posto giusto (`visual/.../immagini/`)
4. Ray ti dirà quando può fare il prossimo batch

> **Naming dei file dentro la zip:** segui esattamente il "Filename suggerito" del prompt_grok.md. Convention: `<id>_canonica_v1_<vista>.jpg` + `<id>_turnaround_v1.jpg`. Tutte `.jpg` (Flux output nativo).

---

## 💰 Tier e costi

| Tier | Costo/img | Velocità | Reference image | Note |
|---|---|---|---|---|
| `flux-schnell` | $0.015 | ~2s | ❌ | Bozze rapide |
| `flux-pro` | $0.04 | ~5s | ❌ | Produzione text-to-image |
| `flux-kontext-pro` ⭐ | $0.04 | ~5s | ✅ | **Raccomandato** — character consistency nativa |
| `flux-kontext-max` | $0.08 | ~8s | ✅ | Massima qualità |

**Raccomandazione:** `flux-kontext-pro` come default. Up-grade a `flux-kontext-max` solo se Pro non rende bene su un personaggio specifico.

**Stima totale catalogo:**
- ~92 immagini personaggi/oggetti × 1 = ~92 immagini
- Con 2-3 retry per quelle difficili → ~250-300 generazioni
- Budget atteso: **~$10-12 totali** (a Kontext Pro)

---

## ⚠️ Cose da NON fare

- ❌ Non committare il file `.env` (le tue chiavi API)
- ❌ Non modificare i `prompt_grok.md` direttamente sulla repo (manda i tuning suggeriti a Ray, lui aggiorna)
- ❌ Non modificare le 4 immagini canoniche già esistenti di Fiamma/Bartolo/Forno/grembiule_fiamma (sono il riferimento di stile, intoccabili)
- ❌ Non pushare niente su main (il push lo fa Ray)
- ❌ Non rinominare le immagini diversamente dalla convention (`<id>_canonica_v1_<vista>.jpg`)

## ✅ Cose che puoi fare in autonomia

- ✅ Generare tutte le variazioni che vuoi (seed diversi) finché trovi il take giusto
- ✅ Aggiustare il prompt nelle tue prove locali (ma per modifiche permanenti scrivi a Ray)
- ✅ Usare `flux-schnell` per bozze veloci a $0.015 prima di committare il `kontext-pro`
- ✅ Mandare a Ray feedback su cosa funziona e cosa no nei prompt (così affiniamo il template)

---

## 🆘 Se qualcosa va storto

- **`FAL_KEY non trovata`** → verifica che `.env` esista e che `python-dotenv` sia installato (`pip install python-dotenv`)
- **Rate limit / 429** → il modulo ha già 3 retry automatici. Se persiste, aspetta 1 minuto e riprova
- **Output stilisticamente fuori canone** → assicurati di passare una `reference_image` di Fiamma o Bartolo
- **Costi che salgono troppo** → usa `flux-schnell` per le bozze, passa a `kontext-pro` solo quando il prompt è già stabile
- **Dubbio narrativo / interpretativo** → manda a Ray, non improvvisare

---

## 📚 Per approfondire

- `_visual_pipeline/README.md` — entry point della pipeline visual
- `_visual_pipeline/_skill/PIPELINE.md` — flusso 6 fasi completo
- `_visual_pipeline/_skill/CHECKLIST.md` — checklist passo-passo per ogni scheda
- `_visual_pipeline/_canone/` — 3 documenti canone saga (stylesheet, scale, palette)
- `_visual_pipeline/_esempi/{fiamma,bartolo}/` — esempi validati di prompt + scheda + descrizione

---

**Maintainer:** Ray
**Per dubbi:** scrivi su Telegram, non improvvisare
