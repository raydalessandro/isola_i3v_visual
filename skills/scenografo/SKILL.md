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
> Versione: 1.2 — 2026-06-22 (v1.1 + contesto di sessione/cache §0, ordine prompt rivisto con POV e SCALA GU estratti come blocchi propri, blocco DIVIETI fisso, POV obbligatorio, `PROMPT_TEMPLATE.md` — lezioni del volume 1 completo). v1.1 aveva aggiunto STORY MOMENT, CHARACTER CONSISTENCY, sessione fresca dal primo batch s02. Formalizza il metodo già validato sulle 17 scene di s01: nessuna deduzione necessaria, ogni blocco del prompt ha una fonte precisa in repo.
>
> **Confine con `skills/illustratore/SKILL.md`:** questa skill copre la **composizione del prompt e la generazione**; la **consegna** dei file (naming, `_hd/`, branch, PR) segue l'illustratore. Leggere entrambe.

---

## TL;DR (in 60 secondi)

1. **Contesto di sessione (cache) → §0.** Carica UNA volta in testa l'invariante (questa skill + `PROMPT_TEMPLATE.md` + stylesheet); per ogni subhook aggiungi solo la sua variante (note + schede). Una sessione = una storia intera.
2. **Fonte scena = `pipeline_narrativa/storie_finali/_annotations/sNN.yaml`** — un blocco `subhooks` per ogni pagina libro, con `note` e campo `pov` che sono il blocco-scena del prompt. NON dedurre le scene dal testo o dai writing_briefs: le annotations sono la ground truth.
3. **Parti da `PROMPT_TEMPLATE.md`** (radice repo): è il template blindato coi blocchi fissi già compilati. Ogni prompt è quel template con le caselle variabili riempite — non si compone da zero.
4. **Il prompt è una sequenza ordinata di blocchi** (§2), e l'ordine conta: STILE → POV → SCALA GU → CAST → LUOGO → MOOD → DIVIETI + STORY MOMENT + CHARACTER CONSISTENCY. Lo scenografo li assembla, non li inventa.
5. **POV obbligatorio:** ogni prompt apre (dopo lo stile) con il punto di vista esplicito del lettore, preso dal campo `pov` del subhook. Mai lasciarlo implicito (§2-ter).
6. **Reference visive obbligatorie** per ogni personaggio in scena: le immagini canoniche del catalogo come ancore (§4).
7. **Output:** sempre **verticale 2:3**, low-res 832×1248 reference + HD ≥1824×2736 JPG q95 sRGB (metadato DPI 300). Naming deterministico `sNN_hMMx` (§5). Anche per gli spread: il compositore libro gestisce il layout, l'immagine resta verticale.
8. **Mai inventare** dettagli non presenti nelle fonti. Se un'entità non ha prompt_grok o scheda visiva, **fermarsi e segnalare**, non improvvisare.

---

## 0. Contesto di sessione — invariante e variante (cache)

L'efficienza (cache) e la qualità (zero ricerche, zero dimenticanze) di questo
ruolo dipendono da COME carichi il contesto, non solo da cosa contiene. Il
generatore non ha memoria tra una generazione e l'altra: ogni prompt deve
essere autosufficiente. Ma il CONTESTO DELL'AGENTE che compone i prompt sì, e
va caricato una volta sola, all'inizio, nell'ordine giusto.

**Invariante di sessione** — si legge UNA volta, in quest'ordine, in testa, e
non si ritocca più (le correzioni sono nuovi messaggi, mai modifiche a monte):

1. questa SKILL
2. `PROMPT_TEMPLATE.md` (radice repo) — il template blindato coi blocchi fissi
3. `_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md` — lo stylesheet integrale
4. il blocco CHARACTER CONSISTENCY e il blocco DIVIETI (§2-bis, §2-ter): fissi,
   identici per ogni immagine del progetto

**Variante per subhook** — l'unica cosa che cambia tra una pagina e l'altra:
la `note` + il `pov` del subhook nello `sNN.yaml`, le `canonical_details`
dell'hook, e le `scheda.md` dei personaggi in `characters_in_scene` (+ le
reference immagini da allegare a Manus).

**Una sessione = una storia intera.** Componi i prompt di tutti i subhook
della storia in fila: l'invariante si paga una volta, ogni subhook aggiunge
solo le sue note e le sue schede. Non spezzare la sessione subhook per subhook.

> Due livelli da non confondere. Quest'ordine ottimizza il **contesto
> dell'agente** (è lì che lavora la cache). L'ordine dei blocchi NEL PROMPT
> per Manus è quello del §2 (stile → POV → scala → cast → luogo → mood →
> divieti): quello serve alla resa dell'immagine, non alla cache. Non
> invertirli per analogia.
>
> Nota: la "sessione fresca" del §4 (chat di generazione nuova per storia) e
> questo caricamento ordinato sono complementari — la prima protegge il
> GENERATORE dalla deriva, il secondo rende efficiente e completo l'AGENTE.

---

## 1. Cosa genera lo scenografo

Una **immagine-scena composta** per ogni marker `@subhook` con `@image TBD` nelle storie (`pipeline_narrativa/storie_finali/sNN_*.md`). Ogni subhook = una pagina libro fisica = un file.

Lo stato del lavoro si legge in due posti equivalenti:
- nel testo storia: marker `<!-- @subhook sNN_hMMx | @page_book N | @image TBD -->`
- nelle annotations: `_annotations/sNN.yaml` → `hooks.sNN_hMM.subhooks[].image_status`

Le immagini di scena **non** sono reference catalogo (quelle vivono in `visual/<categoria>/<id>/immagini/` e si fanno con i prompt_grok delle singole entità).

---

## 2. I blocchi del prompt, nell'ordine, e le loro fonti

L'ordine non è decorativo: il generatore pesa di più ciò che legge prima, e
"comprime" ciò che trova in fondo a un prompt lungo. Per questo lo **stile**
apre (non deve mai scivolare verso il digitale/fotografico), il **POV** e la
**scala GU** vengono subito dopo (sono i due vincoli che il modello viola più
spesso se lasciati impliciti o annegati nel testo), e i **divieti** chiudono
come guardia finale. Stesso ordine nel `PROMPT_TEMPLATE.md`.

| # | Blocco | Fonte in repo | Cosa prendere |
|---|---|---|---|
| 1 | **STILE** (fisso, apre sempre) | `_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md` | Il blocco STYLESHEET integrale, incluso il NEGATIVE. Incollato identico in ogni prompt, in apertura, con peso pari al contenuto. Mai modificarlo, mai sintetizzarlo. |
| 2 | **POV** (punto di vista del lettore) | `_annotations/sNN.yaml` → subhook → campo `pov` | Una frase esplicita: da dove guarda il lettore (es. "high three-quarter view looking down at the pool", "eye-level, reader outside the forest looking in", "low close-up at water level"). Obbligatorio. Dettagli §2-ter. |
| 3 | **SCALA GU** (proporzioni relative) | `visual/personaggi/.../<id>/scheda.md` (campo scala GU) + tabella base in `PROMPT_TEMPLATE.md` | Blocco esplicito con TUTTI i personaggi in scena e le altezze relative, formula esplicita: "Rovo = 0.90× Gabriel's height; all characters share the same ground line; Gabriel tallest, Noah smallest". Obbligatorio in ogni scena multi-personaggio, senza eccezioni. |
| 4 | **CAST** (chi è in scena, com'è fatto) | `visual/personaggi/.../<id>/scheda.md` per ogni id in `characters_in_scene` | Tratti fisici, colori esatti, abbigliamento-firma per nome. NON ripetere qui le altezze (stanno nel blocco SCALA GU). |
| 5 | **LUOGO** (firme ambientali) | `visual/luoghi/.../<location_id>/prompt_grok.md` | Le firme architettoniche/paesaggistiche della veduta più vicina alla `location_variant`. Se la variante non esiste, usare la veduta base + descriverla dai `canonical_details`. |
| 6 | **MOOD** (atmosfera) | `note` del subhook + `canonical_details` | Emozione dominante e luce della scena, 1 frase. Distillato, non copiato dal testo italiano. |
| 7 | **DIVIETI** (guardia finale, fisso) | §2-ter (blocco DIVIETI) + NEGATIVE dello stylesheet | Blocco fisso incollato identico in coda: NO testo, NO tracolle/borse, mantelle aperte non cappotti chiusi, ecc. Dettagli §2-ter. |

**+ STORY MOMENT** (apre il contenuto, §2-bis) e **+ CHARACTER CONSISTENCY**
(blocco fisso dopo il LUOGO, §2-bis).

**+ REFERENCE VISIVE** — non sono testo del prompt ma input immagine da
allegare a Manus: le canoniche di OGNI personaggio in scena
(`visual/.../immagini/<id>_canonica_v1_<vista>.jpg`, preferire `_hd/`) e, se
utile, del luogo. Sono le ancore per volti, colori, vestiti.

**Regola di non-duplicazione:** le note YAML non ripetono stile né tratti
fisici — è voluto. Se una nota sembra "incompleta" su questi punti, i blocchi
STILE/CAST/LUOGO la completano. Non colmare con conoscenza propria.



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

## 2-ter. POV obbligatorio e blocco DIVIETI

**POV (punto di vista) — blocco 2 del prompt, obbligatorio.** Il difetto più
insidioso del volume 1: una nota descrive la scena in modo letterario ("Rovo
di spalle, la testa appena ruotata") e il generatore è libero di scegliere da
dove inquadrarla — spesso male. La regola: ogni subhook ha un campo `pov` nello
`sNN.yaml` con la prospettiva del lettore in una frase tecnica esplicita, e
quella frase entra nel prompt subito dopo lo stile. Esempi di POV ben formati:

- `high three-quarter view looking down at the pool` (vista obliqua dall'alto)
- `eye-level, the reader stands outside the forest looking in` (campo, dal lato)
- `low close-up at water level` (primo piano basso)
- `seen from behind the three brothers, over their shoulders` (di spalle)
- `wide establishing shot from the orchard side` (campo lungo)

Se il campo `pov` manca o è vago ("una bella inquadratura"), NON generare:
distillalo prima dalla `note` (che quasi sempre lo contiene già in forma
narrativa) in una frase tecnica, e segnala a Ray che il subhook va integrato.
Tradurre la descrizione narrativa in POV tecnico è lavoro dell'agente PRIMA di
generare, mai delegato al modello.

**Blocco DIVIETI — blocco 7 del prompt, fisso, chiude sempre.** Incollato
identico in coda a ogni prompt, è la guardia finale contro gli errori
ricorrenti del volume 1 (tracolle comparse, mantelle diventate cappotti,
scritte nelle insegne). Il modello non ha memoria: questi divieti vanno
ripetuti a OGNI immagine, anche quando sembrano ovvi.

```
DO NOT INCLUDE: no text, no lettering, no signs, no written words or
letters anywhere in the image (all signage is added later by the book
compositor). No bags, no backpacks, no shoulder straps, no satchels on
any character. Cloaks and capes are OPEN and DRAPED, never closed coats
or buttoned jackets. No modern clothing, no zippers, no plastic. No 3D
render, no photographic look, no anime, no flat vector — watercolor and
ink only, as per the style block above.
```

> Il blocco DIVIETI e il NEGATIVE dello stylesheet si rinforzano a vicenda:
> il NEGATIVE copre stile e medium, i DIVIETI coprono props e abbigliamento
> specifici del progetto. Tenere entrambi: non sono ridondanti.

---

## 3. Workflow operativo

0. Apri una chat di generazione **nuova** per la storia e ri-allega le reference (regola §4 "Sessione fresca").
1. Leggi `_annotations/sNN.yaml` della storia assegnata.
2. Per ogni hook in ordine, per ogni subhook con `image_status: TBD`:
   a. parti dal `PROMPT_TEMPLATE.md` e riempi le caselle variabili coi 7 blocchi (tabella §2) NELL'ORDINE: STILE → POV → SCALA GU → CAST → LUOGO → MOOD → DIVIETI, + STORY MOMENT e CHARACTER CONSISTENCY, + reference come input immagine. Il POV (blocco 2) dal campo `pov` del subhook è obbligatorio;
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
- `pov`: "high three-quarter view looking down at the pool, the spread crossing two pages"
- canonical_details: i tre riflessi sbagliati (descritti), riflessi più scuri e rigidi
- subhook note: sopra i veri / sotto i riflessi sbagliati, immagine-confronto

Prompt (dal `PROMPT_TEMPLATE.md`, nell'ordine):
1. STILE — stylesheet integrale + NEGATIVE
2. POV — "high three-quarter view looking down at the pool"
3. SCALA GU — "Gabriel 1.0, Elias 0.85, Noah 0.65; same ground line; Gabriel tallest, Noah smallest"
4. CAST — Gabriel/Elias/Noah dai tre `scheda.md` (colori, fazzoletti per nome)
5. LUOGO — `prompt_grok` pozza, veduta "specchio fermo"
6. MOOD — "still, suspended, a mirror that shows what's wrong"
7. DIVIETI — blocco fisso (NO testo, NO tracolle, mantelle aperte…)
+ STORY MOMENT in apertura del contenuto, + CHARACTER CONSISTENCY in coda.
Reference allegate: `gabriel_canonica_v1_fronte.jpg`, `elias_canonica_v1_fronte.jpg`, `noah_canonica_v1_fronte.jpg`.

Output: `_scene/s02/s02_h05a.jpg` + `_scene/s02/_hd/s02_h05a_hd.jpg`.

---

## 7. Checklist pre-consegna

- [ ] Ogni file ha il suo subhook in `_annotations/sNN.yaml` e nel testo storia
- [ ] Prompt costruito a partire da `PROMPT_TEMPLATE.md`, blocchi nell'ordine STILE → POV → SCALA GU → CAST → LUOGO → MOOD → DIVIETI
- [ ] POV esplicito presente in apertura (dal campo `pov` del subhook): da dove guarda il lettore
- [ ] Blocco SCALA GU presente in ogni scena multi-personaggio: altezze relative con formula esplicita, stessa ground line
- [ ] Blocco DIVIETI presente, identico, in coda (NO testo, NO tracolle, mantelle aperte non cappotti chiusi) — §2-ter
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

## 8. Prompt che funzionano — `prompt_approvati.md` (memoria viva)

Quando Ray approva un'immagine ("perfetto", "monta", "gira in output"), il
prompt completo che l'ha prodotta va salvato in `prompt_approvati.md` (radice
repo), sotto la chiave del subhook (es. `s02_h05a`). Quando una scena simile
si ripresenta (stessa location, stessa configurazione di cast, stesso tipo di
POV), si parte da quel prompt invece che da zero.

È il complemento del `PROMPT_TEMPLATE.md`: il template dà i blocchi fissi a
priori, `prompt_approvati.md` accumula le compilazioni che hanno già passato
il giudizio di Ray. Insieme riducono la deriva tra una sessione e l'altra quasi
a zero. Il file si popola progressivamente: non serve precompilarlo.
