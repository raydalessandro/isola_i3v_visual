# ✅ CHECKLIST OPERATIVA — Per ogni scheda

**Scopo:** lista di controllo per Claude da seguire passo-passo durante il completamento di una scheda. Da spuntare mentalmente o esplicitamente.

---

## 🟢 PERSONAGGIO (4 immagini canoniche)

### Fase 0 — Setup
- [ ] Letto `_canone/01_SAGA_STYLESHEET_v1.md`
- [ ] Letto `_canone/02_SAGA_SCALE_v1.md`
- [ ] Letto `_canone/03_SAGA_PALETTE_v1.md`
- [ ] Letto `_templates/TEMPLATE_scheda_personaggio.md`
- [ ] Letta scheda esistente `visual/personaggi/.../<id>/scheda.md`
- [ ] Letta Bible §<X.Y> per il personaggio
- [ ] Letta Glossario §<X.Y> riga del personaggio
- [ ] Letto grafo `entities.characters.<id>` + `stories.s0X.characters_in_scene[<id>]`
- [ ] Letto `PATTERN_AI_DA_BANDIRE_v1.md`

### Fase 1 — Scheda
- [ ] Frontmatter compilato (verificare ID, name, famiglia, sottotipo, specie, ruolo, dimora, quadrante)
- [ ] **Identità visuale (sintesi)**: 1 paragrafo riassuntivo
- [ ] **Aspetto / forma**: travaso Bible + derivazione (postura, statura, pelo, occhi, mani, età)
- [ ] **Abbigliamento / stato d'uso**: firma visiva da Bible + outfit canonico completo derivato
- [ ] **Espressione / comportamento**: travaso Bible + modalità visivamente distinguibili codificate
- [ ] **Palette e atmosfera**: travaso da `03_SAGA_PALETTE_v1.md`
- [ ] **Contesto e ambientazioni ricorrenti**: travaso da Bible §8 (atlante) + grafo
- [ ] **Coerenza cross-scena**: lista bullet di tutto il fisso
- [ ] **Variabilità ammessa**: cosa varia + cosa non varia
- [ ] **Cliché da evitare**: travaso Bible "Note e vincoli" + specifici visivi
- [ ] **Per stampa 3D**: scala, postura, vedute, materiali, punti critici
- [ ] **Per narrativa e social**: registri d'uso interni
- [ ] **Storie / scene di apparizione**: lista deterministica dal grafo
- [ ] **Disallineamenti / domande aperte**: dichiarate
- [ ] **Riferimenti puntuali**: ogni dato canonico citato + ogni derivazione dichiarata

### Fase 2 — Prompt Grok
- [ ] Stylesheet canonica saga incollata invariata
- [ ] Blocco CHARACTER compilato dalla scheda
- [ ] Img 1 (fronte 3:4) scritta
- [ ] Img 2 (azione 4:5) scritta
- [ ] Img 3 (modalità alternativa 4:5) scritta — solo se applicabile
- [ ] Img 4 (turnaround 16:9) scritta
- [ ] Negative prompt globale + specifici inclusi
- [ ] Checklist post-generazione inclusa

### Fase 3 — Descrizione narrativa/social
- [ ] A: tag breve
- [ ] B: scheda riga
- [ ] C: paragrafo descrittivo
- [ ] D: paragrafo evocativo
- [ ] E: registri d'uso
- [ ] F: cosa NON dire mai
- [ ] G: frasi tipiche (se personaggio parla)

### Fase 4 — Output
- [ ] 3 file pronti: `scheda.md`, `prompt_grok.md`, `descrizione_narrativa_social.md`
- [ ] Presentati a Ray con riepilogo scelte autoriali

---

## 🟡 OGGETTO (1-2 immagini canoniche)

### Fase 0 — Setup
- [ ] Letto `_canone/01_SAGA_STYLESHEET_v1.md`
- [ ] Letto `_canone/03_SAGA_PALETTE_v1.md`
- [ ] Letto `_templates/TEMPLATE_scheda_oggetto.md`
- [ ] Letta scheda esistente
- [ ] Letta Bible §<X.Y> dove l'oggetto è citato (di solito in scheda del proprietario)
- [ ] Letto Glossario §6 (firme visive)
- [ ] Letto grafo `entities.objects.<id>`

### Fase 1 — Scheda
- [ ] Frontmatter compilato
- [ ] Identità visuale (sintesi)
- [ ] Aspetto / forma
- [ ] Abbigliamento / stato d'uso (se indossabile)
- [ ] Espressione / comportamento (come si muove con il proprietario)
- [ ] Palette
- [ ] Contesto
- [ ] Coerenza cross-scena
- [ ] Variabilità ammessa
- [ ] Cliché da evitare
- [ ] Per stampa 3D
- [ ] Per narrativa e social
- [ ] Storie di apparizione
- [ ] Disallineamenti
- [ ] Riferimenti puntuali

### Fase 2 — Prompt Grok (semplificato)
- [ ] Stylesheet saga
- [ ] Blocco OBJECT compilato
- [ ] Img 1 canonica (di solito 4:5 o 1:1)
- [ ] Img 2 in uso (se applicabile)
- [ ] Negative prompt + checklist

### Fase 3 — Descrizione narrativa/social
- [ ] A-F (G saltato, oggetti non parlano)

### Fase 4 — Output
- [ ] 3 file pronti

---

## 🔵 LUOGO (0-1 immagine establishing, blocco LOCATION testuale dentro scheda)

### Fase 0 — Setup
- [ ] Letto `_canone/03_SAGA_PALETTE_v1.md` (palette quartiere)
- [ ] Letto `_templates/TEMPLATE_scheda_luogo.md`
- [ ] Letta scheda esistente
- [ ] Letta Bible §8.<X> (atlante quartiere)
- [ ] Letto Glossario §1 (luoghi)
- [ ] Letto grafo `entities.locations.<id>`
- [ ] Letti dati cartografici `cartografia/geo/island.geojson#features.id=<id>`

### Fase 1 — Scheda
- [ ] Frontmatter compilato (incluso blocco cartografia)
- [ ] Identità visuale (sintesi)
- [ ] Aspetto / forma (struttura, materiali, dimensioni)
- [ ] Espressione / comportamento (dinamica del luogo nel tempo)
- [ ] Palette e atmosfera (palette quartiere + dettagli specifici)
- [ ] Contesto e ambientazioni ricorrenti (posizione, prossimità)
- [ ] Coerenza cross-scena
- [ ] Variabilità ammessa (stagioni, ore, meteo)
- [ ] Cliché da evitare
- [ ] **⭐ Descrizione visiva canonica per generazione** — IL BLOCCO LOCATION TESTUALE in inglese (sezione critica)
- [ ] Per stampa 3D (raro, opzionale)
- [ ] Per narrativa e social
- [ ] Storie di apparizione
- [ ] Disallineamenti
- [ ] Riferimenti puntuali

### Fase 2 — NESSUN prompt_grok.md per luoghi
⚠️ Il blocco LOCATION è dentro la scheda, NON in un file separato.

### Fase 3 — Descrizione narrativa/social
- [ ] A-F (G saltato, luoghi non parlano)

### Fase 4 — Output
- [ ] 2 file pronti: `scheda.md`, `descrizione_narrativa_social.md`
- [ ] Eventuale prompt establishing image (1 sola immagine per atlante) può essere generato ad hoc se Ray la richiede, ma NON va pushato come reference per pipeline scene

---

## 🛡️ Verifiche finali (per qualsiasi tipologia)

Prima di consegnare a Ray:

- [ ] Tutte le sezioni del template sono presenti
- [ ] Le sezioni "fonte Bible" sono fedeli al testo originale
- [ ] Le sezioni "derivazione" sono dichiarate nei Riferimenti puntuali
- [ ] Nessuna sezione `_da popolare dal grafo_` rimasta senza giustificazione esplicita
- [ ] I file sono in formato `.md` corretto, con frontmatter YAML valido
- [ ] Le citazioni alle fonti hanno path completi e corretti
- [ ] I cliché da evitare sono completi (Bible + visivi specifici)
- [ ] La stylesheet saga è incollata INVARIATA (se applicabile)
- [ ] Il negative prompt è incluso (se applicabile)
- [ ] Il filename suggerito segue convenzione `<id>_<vista>_v1.jpg`

---

## 🆘 Cosa fare se qualcosa non torna

1. **Conflitto Bible vs grafo**: vince Bible. Segnalare in "Disallineamenti / domande aperte".
2. **Dato mancante non derivabile**: lasciare `_da popolare dal grafo_` con annotazione esplicita in "Disallineamenti".
3. **Palette non in `03_SAGA_PALETTE_v1.md`**: NON inventare. Aggiornare prima il documento canone, poi compilare.
4. **Stile della saga inadeguato per un'entità specifica**: NON cambiare lo stile. Discutere con Ray.
5. **Scala non coerente con `02_SAGA_SCALE_v1.md`**: aggiornare la tabella se serve, mai compilare schede con scale incoerenti.
6. **Cliché Bible non chiaro**: applicare derivazione conservativa (più restrittivo > meno restrittivo).
7. **Immagine generata non passa checklist**: rigenerare singola immagine, non barare sul prompt.

---

**Ultimo aggiornamento:** 2026-04-29
