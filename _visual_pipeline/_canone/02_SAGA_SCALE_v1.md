# 📏 SAGA SCALE REFERENCE v1.0 — Proporzioni canoniche

**Stato:** v1.0 fissata 2026-04-29. Aggiornabile man mano che si fissano nuovi personaggi.

**Scopo:** tabella delle altezze relative di tutti i personaggi della saga. Da incollare in ogni prompt Grok multi-personaggio per garantire proporzioni stabili. Risolve il problema delle proporzioni sballate quando si dà a Grok 5-6 reference visivi diversi.

**Unità:** `1 GU` (Gabriel Unit) = altezza canonica di Gabriel in piedi.

**Perché Gabriel come riferimento:**
- È il fratello maggiore, presente in **tutte le 12 storie**
- È umano (proporzioni stabili, non ambigue)
- È il "punto medio" naturale tra i fratelli e gli abitanti maggiori

---

## 📋 TABELLA CANONICA

| ID | Personaggio | Specie | Altezza in GU | Note proporzioni |
|---|---|---|---|---|
| `gabriel` | Gabriel | umano | **1.00** | RIFERIMENTO. Maggiore dei fratelli. |
| `elias` | Elias | umano | 0.85 | Medio dei fratelli. |
| `noah` | Noah | umano | 0.65 | Piccolo dei fratelli. |
| `bartolo` | Bartolo | tartaruga di mare anziana | **1.05** ✅ | Validato 2026-04-29. **Alto-e-largo, non basso-e-largo**: spalle simili a Gabriel, testa più alta per il collo. Gambe robuste atletiche, presenza dignitosa. Il guscio aumenta volume orizzontale ma non lo schiaccia. |
| `fiamma` | Fiamma | volpe rossa | **0.95** ✅ | Validato 2026-04-29. Poco più bassa di Gabriel. |
| `rovo` | Rovo | tasso | 0.90 | Tozzo, robusto, spalle larghe. |
| `stria` | Stria | airone cenerino | 1.40 | La più alta della saga (specie alta + collo). |
| `memolo` | Mèmolo | riccio | 0.70 | Piccolo, tondo. |
| `grunto` | Grunto | stambecco vecchio | 1.20 | Grosso. **A quattro zampe** (al garrese > 1.00 GU). Quando in piedi sulle posteriori 1.50 GU ma quasi mai. |
| `salvia` | Salvia | lepre | 0.92 | Esile, sottile. |
| `nodo` | Nodo | picchio | 0.85 | Piccolo, magro. |
| `amo` | Amo | cormorano | 1.10 | Alto magro, collo lungo. |
| `zolla` | Zolla | scoiattolo grigio anziano | 0.80 | Piccolo, leggermente curvo dall'età. |
| `pun` | Pun | riccino (figlio Mèmolo) | 0.50 | Cucciolo. Più piccolo del padre. |
| `toba` | Toba | tartarughina (figlia Bartolo) | 0.55 | Cucciolo. |
| `bru` | Bru | tassino (nipote Rovo) | 0.55 | Cucciolo. |
| `cardo` | Cardo | lupacchiotto | 0.60 | Cucciolo, già con coda folta. |
| `liu` | Liù | libellulina | 0.45 | Cucciolo, la più piccola dei cuccioli. |

---

## 🎯 BLOCCO SCALE REFERENCE — copia/incolla in prompt multi-personaggio

Quando una scena ha 2+ personaggi, include nel prompt **solo i personaggi presenti**, sempre con Gabriel come anchor (anche se non è in scena, lo si nomina come unità di riferimento):

```
SCALE REFERENCE — fixed for the saga "L'Isola dei Tre Venti":
Use Gabriel (a human boy) as the height reference (1.0 unit). 
Heights of characters in this scene relative to Gabriel:
- [character_1]: [X]× Gabriel's height — [note proporzionale specifica]
- [character_2]: [Y]× Gabriel's height — [note proporzionale specifica]
- [...]

All characters stand on the same ground line. The relative heights 
listed above MUST be preserved in this image — do not rescale 
characters to fit composition. Compose around their true relative sizes.
```

### Esempio compilato — scena con Fiamma + Mèmolo + Noah

```
SCALE REFERENCE — fixed for the saga "L'Isola dei Tre Venti":
Use Gabriel (a human boy) as the height reference (1.0 unit). 
Heights of characters in this scene relative to Gabriel:
- Fiamma (red fox baker): 0.95× Gabriel's height
- Mèmolo (hedgehog): 0.70× Gabriel's height — small and rounded
- Noah (young human boy): 0.65× Gabriel's height — youngest brother

All characters stand on the same ground line. The relative heights 
listed above MUST be preserved in this image — do not rescale 
characters to fit composition. Compose around their true relative sizes.
```

---

## 🔧 Trucchi pratici per stabilizzare proporzioni

1. **Anchor character esplicito**: nominare un personaggio come "anchor" nel prompt, contro cui tutti gli altri si misurano. Default: Gabriel (o un altro fratello se Gabriel è assente).

2. **Posizione esplicita nel frame**: non lasciare composizione al caso. Es: *"Mèmolo stands to the left of Gabriel, his head reaching Gabriel's belly. Fiamma stands behind the table, slightly taller than Mèmolo."*

3. **Inquadratura full-body o medium**: mai close-up multi-personaggio (il modello tende a "zoomare" e perde le proporzioni).

4. **Ground line condivisa**: nel prompt sempre *"All characters stand on the same ground line."* — impedisce che i personaggi "fluttuino" a quote diverse.

5. **Group shot canonico**: quando si è generata un'immagine canonica multi-personaggio coerente, salvarla come reference image **aggiuntiva** per scene future. È più efficace di mille parole.

---

## ⚠️ Note speciali per personaggi non-bipedi

**Grunto (stambecco)** — è l'unico personaggio principale che cammina **a quattro zampe**. Quando si misura la sua altezza:
- Default: altezza al garrese = 1.20 GU
- Se eretto sulle posteriori: 1.50 GU (raro, mai default)
- In tutte le scene con altri personaggi: usare altezza al garrese.

**Cuccioli volanti (Liù libellulina)** — può essere "in piedi" o "in volo". In volo, la sua altezza si misura dalla testa ai piedi-zampette ed è 0.45 GU. Se appoggiata su una superficie, idem.

---

## 📝 Aggiornamenti

| Data | Versione | Modifica | Validato da |
|---|---|---|---|
| 2026-04-29 | v1.0 | Creazione iniziale, valori derivati da Bible §4 + canone visivo Fiamma | Ray |
| 2026-04-29 | v1.0.1 | Validate visivamente: Fiamma (0.95) e Bartolo (1.05). Aggiunta nota "alto-e-largo, non basso-e-largo" per Bartolo dopo generazione canonica. | Ray |

**Quando aggiornare:**
- Quando si genera la prima scena multi-personaggio e i numeri sembrano sbagliati a occhio → ritarare.
- Quando si introduce un personaggio nuovo (mai successo nelle 12 storie, ma tieni il template aperto).
- Quando si decide che un personaggio "cresce" o "invecchia" attraverso la saga (improbabile, ma).

---

**Ultimo aggiornamento:** 2026-04-29
**Status:** v1.0 — da validare con prima scena multi-personaggio (probabilmente Fiamma + Bartolo + 1 fratello)
