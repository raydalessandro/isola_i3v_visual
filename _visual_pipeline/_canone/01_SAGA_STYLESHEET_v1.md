# 🎨 SAGA STYLESHEET v1.0 — `L'Isola dei Tre Venti`

**Stato:** validato 2026-04-29 con generazione canonica di Fiamma (4 immagini di riferimento). Lo stile è fissato.

**Scopo:** questo blocco va incollato **identico** in ogni prompt Grok Imagine della saga, sia per personaggi sia per scene multi-personaggio sia per luoghi (quando si genera un'immagine canonica di luogo). Garantisce coerenza visiva tra tutte le illustrazioni della saga.

**Quando NON usarlo:** mai. È sempre necessario.

**Quando aggiornarlo:** solo se Ray decide consapevolmente di cambiare lo stile della saga. In quel caso si bumpa a v2.0 e si rigenera tutto. Cambiamenti mai impliciti, mai per tentativi.

---

## 📋 BLOCCO STYLESHEET — copia/incolla in ogni prompt

```
ART STYLE — fixed for the whole saga "L'Isola dei Tre Venti":
Children's picture book illustration. Hand-drawn ink linework with 
a fine, slightly textured pen — visible but soft, not heavy or graphic. 
Watercolor painting on top of the linework, with gentle washes, soft 
gradients, and visible paper grain texture. Earthy natural color palette: 
sage greens, warm ochres, terracotta browns, cream and ivory backgrounds, 
muted sky blue, soft gray stone tones. Saturation always restrained — 
never neon, never glossy, never plastic. 

Anthropomorphic animals in the British picture book tradition (Beatrix 
Potter, Brian Wildsmith) updated with contemporary warmth and gentle 
realism. Characters stand and walk on two legs, wear clothes, have 
expressive faces with rounded soft features. Eyes are alive but never 
huge anime-style; never disney-cute with exaggerated lashes. Naturalistic 
animal anatomy, slightly stylized for warmth, never cartoon-flat. Hands 
and feet of foxes, badgers, hedgehogs etc. retain their natural darker 
fur (black/dark brown "socks") on paws and lower limbs.

Lighting: soft natural light, warm and diffuse, gentle shadows in 
watercolor wash, no harsh contrasts, no dramatic chiaroscuro. The 
overall feeling is of a serene, lived-in world — quiet, dignified, 
slightly nostalgic but contemporary.

NEGATIVE: NO 3D render, NO photorealistic detail, NO oil painting 
heaviness, NO anime, NO manga, NO chibi, NO disney cartoon, NO pixar, 
NO flat vector illustration, NO comic book style, NO airbrush gloss, 
NO neon colors, NO dark gothic atmosphere, NO horror, NO grim. 
Aspect of a high-quality contemporary European picture book for ages 4-10.
```

---

## 🚫 NEGATIVE PROMPT GLOBALE — sempre incluso

```
3D render, photoreal, photographic, oil painting, heavy impasto, anime, 
manga, chibi, disney cartoon, pixar, dreamworks, flat vector, comic book, 
airbrushed, glossy, plastic, neon colors, fluorescent, dark gothic, horror, 
big anime eyes, long eyelashes, sparkles, fantasy magic, glowing aura, 
sparkle effects, kawaii, cute mascot, cartoon-flat
```

---

## 📐 Note operative

- **Aspect ratio**: deciso scena per scena (di solito 3:4 o 4:5 per soggetto singolo, 16:9 per turnaround o establishing shot di luogo).
- **Seed**: salvare sempre il seed di una generazione canonica riuscita per riuso in varianti.
- **Iterazione**: 4-6 varianti per immagine canonica, scegliere la migliore secondo checklist.
- **Coerenza intra-set**: usare lo stesso seed (o seed adiacenti) per tutte le immagini di un personaggio (4 vedute canoniche), per garantire identità riconoscibile.

---

## ✅ Validazione

**v1.0 — 2026-04-29 (Fiamma):** stylesheet validata con generazione canonica di **Fiamma** (4 immagini, vedi `_esempi/fiamma/`):
- Img 1: veduta fronte chiacchiera ✓
- Img 2: in azione mentre impasta ✓
- Img 3: modalità ferma/attenta ✓
- Img 4: turnaround 4 vedute ✓

Risultato: stile picture book painterly riuscito, coerente con illustrazioni di riferimento atlante/mondo già prodotte.

**v1.0 — 2026-04-29 (Bartolo):** stylesheet RI-validata su specie completamente diversa (tartaruga di mare, con guscio). Generazione canonica 4 immagini Grok:
- Img 1: fronte sul Pontile, modalità ferma ✓
- Img 2: sulla barca mentre rema (modalità in viaggio) ✓
- Img 3: ritratto seduto fuori dalla capanna ✓
- Img 4: turnaround 4 vedute con vista retro che mostra cicatrici sul guscio ✓

Risultato: stessa stylesheet, due specie diversissime (volpe + tartaruga) → entrambi escono coerenti come stesso mondo, riconoscibili come stessa saga. **Stylesheet considerata robusta su antropomorfizzazione di specie diverse.**

**Stato:** approvata come canone v1.0 della saga.

---

**Ultimo aggiornamento:** 2026-04-29
**Validato da:** Ray
