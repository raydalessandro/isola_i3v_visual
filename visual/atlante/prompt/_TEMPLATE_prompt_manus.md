# TEMPLATE — Prompt Manus per tavola-atlante

Ogni prompt si compone di **3 blocchi in quest'ordine**, più le reference
allegate. Compilare i campi `{{...}}` e salvare come `<slug>_prompt_manus.md`.
Prototipo di riferimento: `fiamma_prompt_manus.md`.

La variante NON si sceglie: si legge da `ATLANTE_SPEC.json` (ritmo A C B D).
Workflow completo e regole: `skills/atlantista/SKILL.md`.

---

## BLOCCO 1 — SAGA STYLESHEET v1 (fisso)

Incollare identico da `_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md`
(ART STYLE + negative prompt globale). Le tavole-atlante sono pagine del
libro: stesso stile della saga. Qualunque deroga è decisione di Ray,
versionata nello stylesheet, mai improvvisata in prompt.

## BLOCCO 2 — Soggetto e ambiente (dalle schede canoniche)

```
SUBJECT — {{descrizione fisica dalla scheda personaggio/luogo — SOLO
descrittori autorizzati: specie, pelo/piumaggio, occhi, postura,
abbigliamento, firma visiva, proporzioni rispetto alle altre specie}}

SCENE — {{il soggetto nel suo posto sull'isola: dimora o scorcio canonico
del quartiere, dalla scheda luogo. Ora del giorno plausibile, attività
caratteristica. Mai sospeso nel nulla, mai sfondi inventati.}}
```

Reference da allegare: immagini canoniche del catalogo
(`visual/<categoria>/<id>/immagini/`, preferire `_hd/`) per il personaggio
E per il luogo.

## BLOCCO 3 — Composizione (dal template della variante assegnata)

Incollare il blocco "FULL-PAGE COMPOSITION" da
`template/variante_{{X}}.md`. Definisce: dove sta il soggetto, dove resta
lo spazio quieto DIEGETICO (cielo, nebbia, muro, prato — mai carta vuota
incollata), divieto assoluto di testo, formato verticale min 1748×2480.

---

## Dopo la generazione

1. Selezione umana (checklist `skills/atlantista/SKILL.md` §3).
2. `tavole/<slug>_tavola_v1.jpg` + manifest `<slug>_tavola_v1.json`
   (schema nel template di variante).
3. `python3 scripts/ingest_tavola.py visual/atlante/tavole/<slug>_tavola_v1.json`
   — verifica meccanica (dimensioni, quiete misurata delle zone) e
   aggiorna lo spec solo se passa.
4. `python3 -m pytest tests/test_atlante.py -q`
