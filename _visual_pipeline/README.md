# 📦 `_visual_pipeline` — Pipeline operativa completamento catalogo visual

**Scopo:** completare le 115 schede `visual/` della saga **L'Isola dei Tre Venti** con canone chiuso e immagini canoniche generate, in modo coerente, scalabile e riproducibile.

**Per chi:** Ray (autore) + Claude (agente IA) operanti in collaborazione su `isola_i3v_visual`.

**Stato:** v1.2 (2026-04-29). ✅ Pipeline personaggi **validata su 2 specie diversissime** (Fiamma + Bartolo). ✅ Pipeline luoghi **validata su luogo complesso esterno+interno+cortile** (Forno di Fiamma). 🚀 Pronti per scaling a tutto il catalogo.

---

## 🚀 Quick Start — leggi prima questi 3 file

Se sei un agente IA che inizia una sessione di lavoro qui, leggi nell'ordine:

1. **`_skill/PIPELINE.md`** — il flusso operativo completo (cosa fare, in che ordine, come)
2. **`_skill/CHECKLIST.md`** — la checklist da seguire passo-passo per ogni scheda
3. **`_canone/01_SAGA_STYLESHEET_v1.md`** — lo stile visivo della saga (validato)

Poi, prima di lavorare su una scheda, leggi anche:
- `_canone/02_SAGA_SCALE_v1.md` (proporzioni)
- `_canone/03_SAGA_PALETTE_v1.md` (palette)
- Il template della tipologia di entità (`_templates/TEMPLATE_scheda_<famiglia>.md`)
- L'esempio già validato in `_esempi/` per la tipologia corrispondente

---

## 📁 Struttura della directory

```
_visual_pipeline/
│
├── README.md                          ← questo file (entry point)
│
├── _canone/                           ← documenti canonici saga (LEGGERE SEMPRE)
│   ├── 01_SAGA_STYLESHEET_v1.md       ← stile visivo (incollare in ogni prompt Grok)
│   ├── 02_SAGA_SCALE_v1.md            ← proporzioni canoniche (Gabriel = 1.0 GU)
│   └── 03_SAGA_PALETTE_v1.md          ← palette per quartiere e personaggio
│
├── _templates/                        ← template per nuove schede e prompt
│   ├── TEMPLATE_scheda_personaggio.md
│   ├── TEMPLATE_scheda_oggetto.md
│   ├── TEMPLATE_scheda_luogo.md
│   ├── TEMPLATE_prompt_grok_personaggio.md
│   └── TEMPLATE_descrizione_narrativa_social.md
│
├── _skill/                            ← guida operativa
│   ├── PIPELINE.md                    ← flusso completo (cosa fare, in che ordine)
│   └── CHECKLIST.md                   ← checklist passo-passo per ogni scheda
│
└── _esempi/                           ← schede validate da usare come riferimento
    ├── fiamma/                        ← ✅ personaggio (validato 2026-04-29) — STANDARD
    │   ├── scheda.md
    │   ├── prompt_grok.md
    │   ├── descrizione_narrativa_social.md
    │   └── immagini/
    │       └── README.md (convenzione naming)
    ├── bartolo/                       ← ✅ personaggio (validato 2026-04-29) — STANDARD
    │   ├── scheda.md
    │   ├── prompt_grok.md
    │   ├── descrizione_narrativa_social.md
    │   └── immagini/
    │       └── README.md
    ├── forno/                         ← ✅ luogo complesso (validato 2026-04-29) — STANDARD
    │   ├── scheda.md                  ← contiene 3 blocchi LOCATION: esterno/interno/cortile
    │   ├── descrizione_narrativa_social.md
    │   └── immagini/
    │       └── README.md (opzionale, solo establishing per atlante)
    └── grembiule_fiamma/              ← oggetto (scheda OK, prompt da rigenerare con stylesheet validata)
        ├── scheda.md
        ├── prompt_grok.md
        └── descrizione_narrativa_social.md
```

---

## 🔁 Flusso a 6 fasi (per scheda)

Per ogni scheda da completare:

| Fase | Cosa | Chi |
|---|---|---|
| 0 | Setup: leggere canone + template + fonti canoniche del personaggio | Claude |
| 1 | Compilare `scheda.md` completa | Claude |
| 2 | Compilare `prompt_grok.md` (per personaggi/oggetti) o blocco LOCATION dentro scheda (per luoghi) | Claude |
| 3 | Compilare `descrizione_narrativa_social.md` | Claude |
| 4 | Generare immagini canoniche con Grok Imagine | Ray |
| 5 | Push su GitHub (branch dedicato + merge fast-forward) | Ray |
| 6 | Aggiornare canone se necessario (con tracking) | Ray + Claude |

Dettagli in `_skill/PIPELINE.md`.

---

## 📋 Tre tipologie di entità

| Tipologia | Cosa contiene la directory finale | Note |
|---|---|---|
| **Personaggio** | `scheda.md` + `prompt_grok.md` + `descrizione_narrativa_social.md` + 4 immagini canoniche | 4 vedute: fronte / azione / modalità / turnaround |
| **Oggetto** | `scheda.md` + `prompt_grok.md` + `descrizione_narrativa_social.md` + 1-2 immagini canoniche | Più semplice |
| **Luogo** | `scheda.md` (con BLOCCO/BLOCCHI LOCATION testuali) + `descrizione_narrativa_social.md` + (opzionale) immagini establishing | ⚠️ NO prompt_grok.md per luoghi |

⚠️ **Strategia luoghi:** i luoghi vivono come **descrizione testuale** dentro la scheda, non come immagine reference. Questo perché combinare reference visivi di personaggi + reference visivi di luoghi rompe le proporzioni in scena. Il blocco LOCATION testuale + reference personaggi mantiene proporzioni stabili.

⚠️ **Luoghi complessi (esterno + interno + eventuale cortile/annessi):** la scheda contiene **PIÙ blocchi LOCATION distinti**. In ogni prompt scena si usa **un solo blocco** per scena, quello corrispondente alla sotto-area. Esempio: il Forno di Fiamma ha 3 blocchi (ESTERNO / INTERNO / CORTILE). Mai mischiare blocchi.

---

## ⚙️ Cosa cambia nelle schede esistenti

La repo ha già 115 schede in stato `provvisorio`, generate dal travaso meccanico Bible→catalogo (fase F.1). Ogni scheda ha:

- ✅ Frontmatter completo (gestito dallo script `build_visual_skeleton.py`)
- ✅ Sezioni "fonte Bible" già travasate (Aspetto, Comportamento, Palette, Coerenza, Cliché Bible)
- ❌ Sezioni con `_da popolare dal grafo_` non riempite (~805 sezioni totali)

Il lavoro di questa pipeline è **riempire i `_da popolare dal grafo_`** con derivazione autoriale dichiarata, **non rifare il travaso**.

---

## 🎯 Ordine di esecuzione consigliato

Vedi `_skill/PIPELINE.md` §"Ordine di esecuzione consigliato" per la sequenza completa. In sintesi:

1. **Test e validazione** (in corso): grembiule_fiamma + fiamma + bartolo + forno
2. **Tre fratelli** (anchor di scala): gabriel + elias + noah
3. **Personaggi primari rimanenti**: rovo, stria, memolo, grunto
4. **Personaggi secondari**: salvia, nodo, amo, zolla
5. **Cuccioli**: pun, toba, bru, cardo, liu
6. **Collettivi**: 5 gruppi
7. **Oggetti**: 14 totali
8. **Luoghi**: 74 per quartiere
9. **Strade**: 31
10. **Venti + visual signatures**: 4

---

## ⚠️ Regole non negoziabili

### NEVER
- ❌ Mai modificare `pipeline_narrativa/` (Bible, grafo, documenti progetto). READ-ONLY.
- ❌ Mai inventare contenuto non derivabile.
- ❌ Mai cambiare lo stile della saga senza autorizzazione.
- ❌ Mai pushare su main senza il via di Ray.
- ❌ Mai modificare il canone (`_canone/*.md`) senza tracciare e bumpare versione.

### ALWAYS
- ✅ Sempre leggere fonti canoniche prima di scrivere.
- ✅ Sempre dichiarare derivazioni nei "Riferimenti puntuali".
- ✅ Sempre rispettare stylesheet saga nei prompt Grok.
- ✅ Sempre verificare checklist post-generazione sulle immagini.
- ✅ Sempre rigenerare `catalogo_web/data/entities.json` dopo modifiche al `visual/`.

---

## 📚 Documenti correlati nel repo principale

Quando questa pipeline viene portata su `isola_i3v_visual`, va a integrarsi con la struttura esistente:

| Cartella repo | Relazione con la pipeline |
|---|---|
| `pipeline_narrativa/` | Read-only. Fonte di verità narrativa (Bible, grafo). |
| `visual/` | Target di scrittura. Le schede aggiornate vanno qui. |
| `cartografia/` | Read-only per la pipeline visual. Frontmatter luoghi pesca da qui. |
| `catalogo_web/` | Output rigenerabile. Si aggiorna dopo modifiche al `visual/`. |
| `skills/visual/` | Skill esistente. Questa pipeline è il "next step" del compilatore. |
| `scripts/` | Tool condivisi (idempotenti). |

### ⚠️ Convenzione naming filesystem vs narrativa

- **Bible / canone narrativo**: usa il termine "**Abitanti maggiori**" per i 5 personaggi adulti centrali (Bartolo, Fiamma, Rovo, Stria, Mèmolo).
- **Filesystem repo**: usa la cartella `visual/personaggi/individuali/`**primari**`/` per gli stessi personaggi.

I due termini designano lo **stesso insieme** ma vivono in livelli diversi (narrativo vs filesystem). **Non sono in conflitto.** Quando un pacchetto esterno arriva con path `maggiori/`, va adattato a `primari/` per coerenza con la struttura repo.

---

## 🔄 Versioning della pipeline

| Versione | Data | Cambiamenti | Validato da |
|---|---|---|---|
| v1.0 | 2026-04-29 | Creazione iniziale. Stylesheet saga validata con Fiamma. | Ray |
| v1.1 | 2026-04-29 | Validazione su seconda specie (Bartolo, tartaruga). Pipeline personaggi **considerata robusta**. Aggiunti dettagli emersi dalla generazione: "calzini scuri" volpe (Fiamma), alghe verdi su mani/piedi e bordi camicia sfilacciati (Bartolo). | Ray |
| v1.2 | 2026-04-29 | Validazione su luogo complesso (Forno di Fiamma) con 3 blocchi LOCATION distinti (esterno/interno/cortile). Aggiornato `TEMPLATE_scheda_luogo.md` per supportare luoghi-complessi tramite flag `ha_interno`/`ha_esterno`/`ha_cortile_o_annessi`. **Pipeline luoghi considerata robusta**, pronti per scaling. | Ray |

**Quando bumpare:**
- v1.x → aggiunte/modifiche minori a template/canone (mantenute backward-compatible)
- v2.0 → cambio strutturale (es: cambio stile saga, cambio sistema scala)

---

## 🏁 Punto d'arrivo

Quando tutte le 115 schede saranno chiuse, avremo:

- 115 schede canoniche complete in `visual/`
- ~80-100 immagini canoniche generate (4 per ogni personaggio + 1-2 per ogni oggetto)
- Tutti i luoghi descritti come blocchi LOCATION testuali, riusabili in pipeline scena
- Canone saga completo (stylesheet + scale + palette)
- **Pronti per la fase successiva**: pipeline di generazione delle illustrazioni delle 12 storie, scena per scena.

---

**Maintainer:** Ray + Claude
**Ultimo aggiornamento:** 2026-04-29
**Issue tracking:** se trovi conflitti / ambiguità / problemi durante il lavoro, segnalali a Ray. Mai risolvere in autonomia su contenuto narrativo.
