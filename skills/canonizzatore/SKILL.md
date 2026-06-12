---
role: canonizzatore
trigger: canonizzazione completa di una scheda visual (scheda + prompt grok + descrizione social + immagini canoniche, fase F.2)
scope_write: "visual/ (schede della entità in lavorazione) — via flusso _visual_pipeline/"
commands: "make catalogo (dopo ogni scheda)"
order: 30
---

# Skill — Canonizzatore schede (puntatore)

> **La skill operativa vive in `_visual_pipeline/`** (pacchetto autosufficiente con canone, template, esempi validati e checklist). Questo file esiste per la trovabilità: tutte le skill si trovano in `skills/<ruolo>/SKILL.md`.

## Letture obbligatorie, nell'ordine

1. `_visual_pipeline/README.md` — entry point del pacchetto
2. `_visual_pipeline/_skill/PIPELINE.md` — flusso 6 fasi per scheda
3. `_visual_pipeline/_skill/CHECKLIST.md` — verifica finale per scheda
4. `_visual_pipeline/_canone/` — 3 doc canone saga (stylesheet, scale, palette) — **read-only**
5. Template della tipologia in `_visual_pipeline/_templates/` + un esempio validato in `_visual_pipeline/_esempi/`

## Vincoli chiave (dettaglio nel pacchetto)

- Mai modificare `_visual_pipeline/_canone/*.md` senza autorizzazione + bump versione.
- Mai inventare contenuto non derivabile dalle fonti (grafo, Bible, schede).
- Personaggi: scheda + prompt_grok + social + 4 immagini canoniche. Luoghi: BLOCCO LOCATION testuale, **niente** prompt_grok. Oggetti: scheda + prompt + 1-2 immagini.
- Dopo ogni scheda: `make catalogo` (matrice di propagazione, vedi `CLAUDE.md`).
