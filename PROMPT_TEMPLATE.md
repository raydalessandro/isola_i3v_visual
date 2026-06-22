# PROMPT_TEMPLATE.md — Template blindato per immagini di scena (Manus)

> Template canonico per la generazione delle immagini di scena della saga
> *L'Isola dei Tre Venti*. Si legge all'inizio di ogni sessione (è parte
> dell'invariante: vedi `skills/scenografo/SKILL.md` §0) e ogni prompt parte
> da qui — le caselle `{{...}}` si riempiono dalle fonti canoniche, i blocchi
> fissi NON si toccano.
>
> Scopo: eliminare la perdita di coerenza tra una sessione e l'altra. Il
> generatore non ha memoria; questo template garantisce che ogni immagine
> riceva TUTTI i vincoli, sempre, nello stesso ordine.
>
> Versione: 1.0 — 2026-06-22. Allineato a `skills/scenografo/SKILL.md` v1.2.

---

## Come si usa

1. Copia il blocco "PROMPT — struttura" qui sotto.
2. Riempi solo le caselle `{{...}}` dalle fonti indicate a lato.
3. NON cambiare l'ordine dei blocchi, NON rimuovere i blocchi fissi (STILE,
   DIVIETI, CHARACTER CONSISTENCY), NON sintetizzare lo stile.
4. Allega a Manus le reference immagini dei personaggi in scena.
5. Genera, valuta contro `note` + reference, itera.

L'ordine dei blocchi non è negoziabile: lo stile apre (non deve scivolare),
POV e scala GU subito dopo (i vincoli più violati), i divieti chiudono come
guardia. Dettagli e razionale in `skills/scenografo/SKILL.md` §2.

---

## PROMPT — struttura (copiare e compilare)

```
### 1. STYLE  [BLOCCO FISSO — incollare integrale da
###    _visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md, incluso NEGATIVE]
{{STYLESHEET_INTEGRALE}}

### 2. POINT OF VIEW  [dal campo `pov` del subhook in _annotations/sNN.yaml]
Point of view: {{POV}}
   (es. "high three-quarter view looking down at the pool";
        "eye-level, the reader stands outside the forest looking in";
        "low close-up at water level";
        "seen from behind the three brothers, over their shoulders")

### 3. GU SCALE  [da scheda.md di ogni personaggio in scena — OBBLIGATORIO se >1 personaggio]
Relative sizes (GU scale, anchor Gabriel = 1.0):
{{LISTA_PERSONAGGI_CON_GU}}
All characters share the SAME GROUND LINE. Gabriel is the tallest, Noah the
smallest. {{EVENTUALE_NON_FRATELLO}} = {{FATTORE}}× Gabriel's height.

### 4. CAST  [da scheda.md — tratti, colori, abbigliamento per nome; NIENTE altezze, stanno al blocco 3]
{{DESCRITTORI_PERSONAGGI}}

### 5. SETTING  [da visual/luoghi/.../<location_id>/prompt_grok.md, veduta più vicina a location_variant]
{{FIRME_AMBIENTALI_LUOGO}}

### 6. MOOD  [1 frase distillata da note + canonical_details]
{{ATMOSFERA}}

### STORY MOMENT  [1-2 frasi in inglese: azione in corso + emozione + relazioni spaziali esplicite]
{{STORY_MOMENT}}

### CHARACTER CONSISTENCY  [BLOCCO FISSO — incollare identico]
CHARACTER CONSISTENCY — the attached reference images are BINDING, not
inspiration. Match them exactly for every named character: face shape and
proportions, hair color and cut, eye color, build, skin tone. Signature
neckerchiefs by name: Gabriel purple, Elias yellow, Noah light
turquoise-blue — never swapped, never missing, never replaced by scarves.
Relative heights per the GU scale (Gabriel tallest, Noah smallest).
Clothing follows the character sheets unless the subhook note explicitly
says otherwise.

### 7. DO NOT INCLUDE  [BLOCCO FISSO — incollare identico, chiude sempre]
DO NOT INCLUDE: no text, no lettering, no signs, no written words or
letters anywhere in the image (all signage is added later by the book
compositor). No bags, no backpacks, no shoulder straps, no satchels on
any character. Cloaks and capes are OPEN and DRAPED, never closed coats
or buttoned jackets. No modern clothing, no zippers, no plastic. No 3D
render, no photographic look, no anime, no flat vector — watercolor and
ink only, as per the style block above.

### OUTPUT
Vertical 2:3 format. HD render, at least 1824×2736 px, JPEG quality 95,
sRGB. Keep the upper ~25–30% of the frame quiet and low-detail (open sky,
mist, plain wall, high foliage) for the page text — no important detail,
faces or signature objects in that top band.
```

---

## Tabella GU base (riferimento rapido — la verità è nelle schede)

I tre fratelli (anchor di scala della saga):

| Personaggio | GU | Nota |
|---|---|---|
| Gabriel | 1.0 | anchor — il più alto dei tre |
| Elias | 0.85 | il medio |
| Noah | 0.65 | il più piccolo |

Per gli altri personaggi (Rovo, Bru, Stria, Nodo, ecc.) leggere il fattore GU
dalla rispettiva `scheda.md` e includerlo nel blocco 3 con la formula esplicita
(es. "Rovo = 0.90× Gabriel's height"). Se la scheda non riporta un valore GU,
NON inventarlo: segnalare a Ray e usare un riferimento prudente coerente con le
proporzioni nelle reference canoniche.

---

## Checklist lampo prima di inviare (estratto §2-ter / §7 della skill)

- [ ] STILE in apertura, integrale, non sintetizzato
- [ ] POV esplicito (blocco 2) — da dove guarda il lettore
- [ ] SCALA GU esplicita con formula e ground line comune (se >1 personaggio)
- [ ] Colori e fazzoletti dei personaggi per nome (Gabriel viola, Elias giallo, Noah turchese)
- [ ] CHARACTER CONSISTENCY e DIVIETI incollati identici
- [ ] Reference dei personaggi in scena allegate a Manus
- [ ] Quiet zone alta + formato verticale 2:3 + ≥1824×2736 nel blocco OUTPUT
