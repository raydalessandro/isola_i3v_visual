# isola_i3v_visual — Cartografia e Visual

Repository di lavoro per il progetto **L'Isola dei Tre Venti** (saga di 12 storie illustrate per bambini 4-10 anni, di Ray).

Questo repo contiene **due tracce di lavoro** + un input read-only:

```
/
├── cartografia/           ← tecnica: GeoJSON, schede luogo, viewer, convenzioni
├── visual/                ← descrizioni visive, vincoli prompt, immagini, sito interno
└── pipeline_narrativa/    ← INPUT read-only: grafo storie + corpus canonico narrativo
```

---

## 1. Cartografia

Cartografia tecnica canonica dell'Isola. Alimenta la pipeline immagini con coerenza geografica e valida le storie nuove rispetto al canone fisico.

- **Stato:** v0.5 — 103 feature, 36 sentieri, viewer Leaflet, backward-compat 100% con grafo v0.6.0.
- **Punto d'ingresso umano:** `cartografia/geo/viewer/index.html` (doppio click).
- **Architettura e regole:** `cartografia/README.md`.
- **Storia versioni:** `cartografia/CHANGELOG.md`.

## 2. Visual

Serbatoio di **descrizioni visive e vincoli per prompt** per tutte le entità della storia (luoghi, personaggi, oggetti, venti-spiriti). Sarà fruibile via piccolo sito web interno ordinato per sezioni di entità, con immagini di riferimento per i modelli generativi.

- **Stato:** in bootstrap. Materiale e struttura da definire nelle prossime sessioni.

## 3. Pipeline narrativa (read-only)

Corpus narrativo canonico — Bible, Glossario, ARCHI 12 storie, voce, pattern AI da bandire, EAR, apparato — più il grafo storie aggiornato.

- **Grafo corrente:** `pipeline_narrativa/story_graph.json` v0.10.0 (S1-S12).
- **Regola:** mai modificato dalla cartografia o dal visual. Se si rilevano incoerenze, **si segnalano**, non si risolvono in autonomia.

---

## 4. Istruzioni per agenti IA

Vedi `AGENT_INSTRUCTIONS.md`. In sintesi: l'agente ha autorità su **geografia** (cartografia/) e **descrizioni visive** (visual/); non tocca mai `pipeline_narrativa/`; non decide canone narrativo; segnala invece di reinterpretare.

## 5. Stato e contesto

- **Snapshot operativo:** `PROJECT_STATE.md`.
- **Autore narrativo e proprietario:** Ray.
- **Manutenzione tecnica:** Ray + agente IA in collaborazione.

---

**Ultimo aggiornamento:** 2026-04-25
**Versione cartografia:** v0.5
**Versione grafo storie:** v0.10.0
