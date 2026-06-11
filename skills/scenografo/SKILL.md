# Skill — Agente scenografo (generazione immagini di scena)

> Per **istanze IA** (es. Manus) o **collaboratori** che si connettono alla repo `isola_i3v_visual` per **generare le illustrazioni di scena** del libro: una immagine per ogni subhook (pagina libro fisica) delle storie.
>
> Versione: 1.0 — 2026-06-11. Formalizza il metodo già validato sulle 17 scene di s01: nessuna deduzione necessaria, ogni blocco del prompt ha una fonte precisa in repo.
>
> **Confine con `skills/illustratore/SKILL.md`:** questa skill copre la **composizione del prompt e la generazione**; la **consegna** dei file (naming, `_hd/`, branch, PR) segue l'illustratore. Leggere entrambe.

---

## TL;DR (in 60 secondi)

1. **Fonte scena = `pipeline_narrativa/storie_finali/_annotations/sNN.yaml`** — un blocco `subhooks` per ogni pagina libro, con la `note` che è il blocco-scena del prompt. NON dedurre le scene dal testo o dai writing_briefs: le annotations sono la ground truth.
2. **Il prompt è la somma di 5 blocchi**, ognuno con la sua fonte (tabella §2). Lo scenografo li assembla, non li inventa.
3. **Reference visive obbligatorie** per ogni personaggio in scena: le immagini canoniche del catalogo come ancore (§4).
4. **Output:** sempre **verticale**, low-res 832×1248 reference + HD 1664×2496 JPG q95 sRGB. Naming deterministico `sNN_hMMx` (§5). Anche per gli spread: il compositore libro gestisce il layout, l'immagine resta verticale.
5. **Mai inventare** dettagli non presenti nelle fonti. Se un'entità non ha prompt_grok o scheda visiva, **fermarsi e segnalare**, non improvvisare.

---

## 1. Cosa genera lo scenografo

Una **immagine-scena composta** per ogni marker `@subhook` con `@image TBD` nelle storie (`pipeline_narrativa/storie_finali/sNN_*.md`). Ogni subhook = una pagina libro fisica = un file.

Lo stato del lavoro si legge in due posti equivalenti:
- nel testo storia: marker `<!-- @subhook sNN_hMMx | @page_book N | @image TBD -->`
- nelle annotations: `_annotations/sNN.yaml` → `hooks.sNN_hMM.subhooks[].image_status`

Le immagini di scena **non** sono reference catalogo (quelle vivono in `visual/<categoria>/<id>/immagini/` e si fanno con i prompt_grok delle singole entità).

---

## 2. I 5 blocchi del prompt e le loro fonti

| # | Blocco | Fonte in repo | Cosa prendere |
|---|---|---|---|
| 1 | **STILE** (fisso per tutta la saga) | `_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md` | Il blocco STYLESHEET integrale, incluso il NEGATIVE. Incollato identico in ogni prompt. Mai modificarlo. |
| 2 | **SCENA** (cosa succede in questa pagina) | `_annotations/sNN.yaml` → hook → `location` + `location_variant` + `canonical_details` + subhook → `note` | La `note` del subhook è il cuore: beat, azione focale, inquadratura, atmosfera, vincoli. I `canonical_details` dell'hook danno frasi-codice, dettagli Tier A, vincoli di continuità. |
| 3 | **CAST** (chi è in scena, com'è fatto) | `visual/personaggi/.../<id>/scheda.md` per ogni id in `characters_in_scene` | Tratti fisici, abbigliamento-firma, **scale GU** (proporzioni: es. Gabriel 1.0, Elias 0.85, Noah 0.65 — esplicitare sempre "Gabriel is the tallest, Noah is the smallest"). |
| 4 | **LUOGO** (firme ambientali) | `visual/luoghi/.../<location_id>/prompt_grok.md` | Le firme architettoniche/paesaggistiche della veduta più vicina alla `location_variant` richiesta. Se la variante non esiste nel prompt del luogo, usare la veduta base + descrivere la variante dai `canonical_details`. |
| 5 | **REFERENCE VISIVE** (ancore di coerenza) | `visual/.../immagini/<id>_canonica_v1_<vista>.jpg` | Passare i path delle canoniche di OGNI personaggio in scena (fronte o vista più pertinente) e, se utile, del luogo. Sono le ancore per volti, colori, vestiti. |

**Regola di non-duplicazione:** le note YAML non ripetono stile né tratti fisici — è voluto. Se una nota sembra "incompleta" su questi punti, i blocchi 1/3/4 la completano. Non colmare con conoscenza propria.

---

## 3. Workflow operativo

1. Leggi `_annotations/sNN.yaml` della storia assegnata.
2. Per ogni hook in ordine, per ogni subhook con `image_status: TBD`:
   a. assembla i 5 blocchi (tabella §2) nell'ordine 1→2→3→4 + reference (5) come input immagine;
   b. rispetta i vincoli espliciti nei `canonical_details` (es. "i riflessi NON si vedono in questa pagina", "Bru appare SOLO nel subhook d", "Rovo non si vede: solo presenza sonora");
   c. genera; valuta contro nota + reference; itera se serve.
3. Salva con naming §5.
4. Consegna secondo `skills/illustratore/SKILL.md` (branch `claude/hd-storia-sNN`, un commit, PR, **mai** merge autonomo).

**Coerenza di sequenza:** prima di generare la scena di un subhook, guarda le scene già approvate degli hook adiacenti della stessa location (stessa luce, stesso punto di vista quando la nota chiede "eco compositiva" o "stessa inquadratura").

---

## 4. Regole di coerenza (vincolanti)

- **Scale GU sempre nel prompt** quando ci sono più personaggi: il modello tende a uniformare le altezze.
- **Reference = ancore, non suggerimenti:** se l'immagine generata diverge dalla canonica (colore vestito, forma orecchie, bandana), si rigenera.
- **Vincoli di pagina prima di tutto:** i `canonical_details` marcati come VINCOLO (page-turn, apparizioni rimandate, presenze solo-in-un-subhook) prevalgono su qualsiasi scelta compositiva.
- **Onomatopee e lettering** (TIK-TIK-TIIK, TUM-tum-TUM): l'immagine NON contiene testo. Le rese tipografiche sono del compositore libro.
- **Mai inventare contenuto narrativo o visivo** (regola repo, `CLAUDE.md` §TL;DR punto 8). Entità senza scheda/prompt → segnalare a Ray (issue o nota PR), non improvvisare.
- **Cammei e presenze di sfondo** (Mèmolo che passa, Bru nel quadrato di buio, collettivi mai individuati): seguire alla lettera la nota — figure piccole, volti non protagonisti, fedeli ai vincoli dei collettivi (`visual/personaggi/collettivi/*/prompt_grok.md`).

---

## 5. Output e naming (deterministico)

```
pipeline_narrativa/storie_finali/_scene/sNN/sNN_hMMx.jpg          ← low-res 832×1248
pipeline_narrativa/storie_finali/_scene/sNN/_hd/sNN_hMMx_hd.jpg   ← HD 1664×2496, JPG q95, sRGB
```

- `x` = lettera subhook (`a`, `b`, `c`, ...). Mai altri suffissi.
- **Formato sempre verticale 2:3**, anche per i subhook con `@layout double_spread`: il compositore (`scripts/build_volume.py`) impagina lo spread affiancando l'immagine alla pagina di testo. Non generare immagini a doppia larghezza salvo richiesta esplicita di Ray.
- Le HD **sempre e solo** in `_hd/`. Mai sostituire low-res esistenti.
- Una pagina libro = un file. Per lo spread: un solo subhook, un solo file.

---

## 6. Esempio di assemblaggio (s02_h05a)

Dall'annotation `_annotations/s02.yaml`:
- location `pozza_abbeveratoio_pastori`, variant `bordo_mezzogiorno_specchio`
- characters_in_scene `[gabriel, elias, noah]`
- canonical_details: i tre riflessi sbagliati (descritti), riflessi più scuri e rigidi
- subhook note: vista obliqua dall'alto, sopra i veri / sotto i riflessi sbagliati, immagine-confronto

Prompt = `[STYLESHEET integrale]` + `[note + canonical_details come blocco SCENE]` + `[schede Gabriel/Elias/Noah con scale GU]` + `[prompt_grok pozza, veduta "specchio fermo"]`, con reference `gabriel_canonica_v1_fronte.jpg`, `elias_canonica_v1_fronte.jpg`, `noah_canonica_v1_fronte.jpg`.

Output: `_scene/s02/s02_h05a.jpg` + `_scene/s02/_hd/s02_h05a_hd.jpg`.

---

## 7. Checklist pre-consegna

- [ ] Ogni file ha il suo subhook in `_annotations/sNN.yaml` e nel testo storia
- [ ] Naming esatto `sNN_hMMx` (+ `_hd` solo dentro `_hd/`)
- [ ] HD: 1664×2496 minimo, JPG q95, sRGB, verticale
- [ ] Personaggi conformi alle canoniche (volti, vestiti, scale)
- [ ] Vincoli di pagina rispettati (page-turn, apparizioni, presenze per-subhook)
- [ ] Branch solo-immagini, un commit, PR aperta, attesa OK Ray
