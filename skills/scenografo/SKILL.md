---
role: scenografo
trigger: comporre prompt e generare le immagini di scena (una per subhook/pagina libro)
scope_write: "consegna file via skill illustratore (branch claude/hd-*)"
commands: "—"
order: 60
---

# Skill — Agente scenografo (generazione immagini di scena)

> Per **istanze IA** (es. Manus) o **collaboratori** che si connettono alla repo `isola_i3v_visual` per **generare le illustrazioni di scena** del libro: una immagine per ogni subhook (pagina libro fisica) delle storie.
>
> Versione: 1.1 — 2026-06-12 (v1.0 + STORY MOMENT, blocco CHARACTER CONSISTENCY nel prompt, regola sessione fresca — lezioni del primo batch s02). Formalizza il metodo già validato sulle 17 scene di s01: nessuna deduzione necessaria, ogni blocco del prompt ha una fonte precisa in repo.
>
> **Confine con `skills/illustratore/SKILL.md`:** questa skill copre la **composizione del prompt e la generazione**; la **consegna** dei file (naming, `_hd/`, branch, PR) segue l'illustratore. Leggere entrambe.

---

## TL;DR (in 60 secondi)

1. **Fonte scena = `pipeline_narrativa/storie_finali/_annotations/sNN.yaml`** — un blocco `subhooks` per ogni pagina libro, con la `note` che è il blocco-scena del prompt. NON dedurre le scene dal testo o dai writing_briefs: le annotations sono la ground truth.
2. **Il prompt è la somma di 5 blocchi**, ognuno con la sua fonte (tabella §2). Lo scenografo li assembla, non li inventa.
3. **Reference visive obbligatorie** per ogni personaggio in scena: le immagini canoniche del catalogo come ancore (§4).
4. **Output:** sempre **verticale 2:3**, low-res 832×1248 reference + HD ≥1824×2736 JPG q95 sRGB (metadato DPI 300). Naming deterministico `sNN_hMMx` (§5). Anche per gli spread: il compositore libro gestisce il layout, l'immagine resta verticale.
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
| 2 | **SCENA** (cosa succede in questa pagina) | `_annotations/sNN.yaml` → hook → `location` + `location_variant` + `canonical_details` + subhook → `note` **+ testo della pagina** (`storie_finali/sNN_*.md`, tra i marker del subhook) | La `note` del subhook è il cuore: beat, azione focale, inquadratura, atmosfera, vincoli. Il testo della pagina è contesto per l'agente (tono, dettagli, relazioni spaziali): si distilla nello **STORY MOMENT** (§2-bis), mai incollato grezzo nel prompt. I `canonical_details` dell'hook danno frasi-codice, dettagli Tier A, vincoli di continuità. |
| 3 | **CAST** (chi è in scena, com'è fatto) | `visual/personaggi/.../<id>/scheda.md` per ogni id in `characters_in_scene` | Tratti fisici, abbigliamento-firma, **scale GU** (proporzioni: es. Gabriel 1.0, Elias 0.85, Noah 0.65 — esplicitare sempre "Gabriel is the tallest, Noah is the smallest"). |
| 4 | **LUOGO** (firme ambientali) | `visual/luoghi/.../<location_id>/prompt_grok.md` | Le firme architettoniche/paesaggistiche della veduta più vicina alla `location_variant` richiesta. Se la variante non esiste nel prompt del luogo, usare la veduta base + descrivere la variante dai `canonical_details`. |
| 5 | **REFERENCE VISIVE** (ancore di coerenza) | `visual/.../immagini/<id>_canonica_v1_<vista>.jpg` | Passare i path delle canoniche di OGNI personaggio in scena (fronte o vista più pertinente) e, se utile, del luogo. Sono le ancore per volti, colori, vestiti. |

**Regola di non-duplicazione:** le note YAML non ripetono stile né tratti fisici — è voluto. Se una nota sembra "incompleta" su questi punti, i blocchi 1/3/4 la completano. Non colmare con conoscenza propria.

## 2-bis. STORY MOMENT e blocco CHARACTER CONSISTENCY

**STORY MOMENT** — apre il blocco SCENA nel prompt: 1-2 frasi in inglese,
distillate dal testo della pagina e dalla `note`. Devono contenere: azione
in corso, emozione dominante, **relazioni spaziali esplicite** (chi è dove
rispetto a cosa: "walking ALONG the path, single file, following its
direction", "kneeling AT THE EDGE of the pool"). Mai incollare il testo
italiano grezzo: il generatore pesa male la prosa lunga e gli elementi non
visivi contaminano la scena.

**CHARACTER CONSISTENCY** — blocco fisso, incollato **identico** in coda a
ogni prompt (dopo il blocco LUOGO). È la versione permanente del rinforzo
che finora si faceva a voce nella chat di generazione: i vincoli vivono nel
prompt-file, mai solo nella conversazione.

```
CHARACTER CONSISTENCY — the attached reference images are BINDING, not
inspiration. Match them exactly for every named character: face shape and
proportions, hair color and cut, eye color, build, skin tone. Signature
neckerchiefs by name: Gabriel purple, Elias yellow, Noah light
turquoise-blue — never swapped, never missing, never replaced by scarves.
Relative heights per the GU scale (Gabriel tallest, Noah smallest).
Clothing follows the character sheets unless the subhook note explicitly
says otherwise.
```

> Fonte normativa del blocco: questa sezione. Il template delle
> tavole-atlante (`visual/atlante/prompt/_TEMPLATE_prompt_manus.md`) lo
> incolla da qui. Candidato a promozione in `_visual_pipeline/_canone/`
> come documento proprio: decisione di Ray.

---

## 3. Workflow operativo

0. Apri una chat di generazione **nuova** per la storia e ri-allega le reference (regola §4 "Sessione fresca").
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
- **Sessione di generazione fresca:** una chat di generazione NUOVA per ogni storia (o batch), con le reference ri-allegate all'inizio. Mai proseguire un batch in una chat che ha già generato molte immagini: il generatore deriva verso le proprie ultime uscite e i vincoli iniziali si diluiscono col contesto.
- **Vincoli di pagina prima di tutto:** i `canonical_details` marcati come VINCOLO (page-turn, apparizioni rimandate, presenze solo-in-un-subhook) prevalgono su qualsiasi scelta compositiva.
- **Onomatopee e lettering** (TIK-TIK-TIIK, TUM-tum-TUM): l'immagine NON contiene testo. NO text, NO lettering, NO signs, NO written words, NO captions, NO labels in nessuna parte della scena — insegne, cartelli e qualsiasi parola scritta sono aggiunti dal compositore libro. Vale per ogni lingua e per qualunque elemento riconducibile a scrittura.
- **Quiet zone alta:** vincolo compositivo dello stylesheet (sezione PAGE COMPOSITION), vale per ogni scena. Il ~25-30% superiore del frame deve restare quieto e a basso dettaglio per ospitare il testo della pagina libro. Le note subhook possono indicare COSA mettere nella fascia alta — cielo, nebbia, chiome alte, parete liscia — mai cosa metterci di importante (volti, azioni, oggetti firma).
- **Mai inventare contenuto narrativo o visivo** (regola repo, `CLAUDE.md` §TL;DR punto 8). Entità senza scheda/prompt → segnalare a Ray (issue o nota PR), non improvvisare.
- **Cammei e presenze di sfondo** (Mèmolo che passa, Bru nel quadrato di buio, collettivi mai individuati): seguire alla lettera la nota — figure piccole, volti non protagonisti, fedeli ai vincoli dei collettivi (`visual/personaggi/collettivi/*/prompt_grok.md`).
- **Coerenza a 360°:** le reference canoniche valgono da ogni angolazione. Nelle pose di spalle o di profilo, capelli (taglio e colore), colori e forme dei vestiti, oggetti-firma e proporzioni GU devono restare conformi alle canoniche frontali. Per le pose di spalle, esplicitare nel prompt i dettagli visibili da dietro ricavati dalla scheda (es. colore fazzoletto annodato sulla nuca, forma della sciarpa); in assenza di reference di retro, le canoniche frontali restano l'ancora per colori e proporzioni.

---

## 5. Output e naming (deterministico)

```
pipeline_narrativa/storie_finali/_scene/sNN/sNN_hMMx.jpg          ← low-res 832×1248
pipeline_narrativa/storie_finali/_scene/sNN/_hd/sNN_hMMx_hd.jpg   ← HD ≥1824×2736 verticale 2:3, JPG q95 sRGB, DPI metadata 300
```

Lo standard precedente 1664×2496 resta valido per le scene già consegnate di s01 (v1); dal 2026-06 nuovo minimo 1824×2736 — copre 300 DPI effettivi sul fit reale del compositore (A5 + bleed 3.175 mm in `scripts/build_volume.py`).

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
- [ ] HD: ≥1824×2736 px verticale 2:3, JPG q95, sRGB, metadato DPI a 300
- [ ] Personaggi conformi alle canoniche **da ogni angolazione** (volti, capelli, vestiti, scale GU — incluso pose di spalle/profilo)
- [ ] Blocco CHARACTER CONSISTENCY presente, identico, in coda a ogni prompt (§2-bis)
- [ ] STORY MOMENT presente: azione + emozione + relazioni spaziali esplicite, in inglese
- [ ] Chat di generazione nuova per questo batch, reference ri-allegate
- [ ] Vincoli di pagina rispettati (page-turn, apparizioni, presenze per-subhook)
- [ ] Quiet zone alta rispettata: ~25-30% superiore del frame senza dettagli importanti (cielo / nebbia / parete)
- [ ] Nessun testo, lettering, insegna o parola scritta nell'immagine
- [ ] Branch solo-immagini, un commit, PR aperta, attesa OK Ray
