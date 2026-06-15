# ESTRAZIONE — Ledger del template

Memoria condivisa tra le sessioni di estrazione. Ogni sessione-fase aggiorna la
sua riga: cosa è entrato nel kit (**contratto**), cosa è restato nell'isola
(**contenuto**), e il prossimo passo. È ciò che impedisce alle sessioni separate
di divergere. Regole e metodo: `SPEC_TEMPLATE.md`.

**Stati:** ⬜ da fare · 🟡 in corso/parziale · ✅ estratta nel kit

## Stato delle fasi

| # | Fase | Stato | Nel kit (contratto/scheletro) | Resta nell'isola (contenuto) | Prossimo passo |
|---|---|---|---|---|---|
| 1 | Seeding conversazionale | ⬜ | — | — | istituzionalizzare come skill (caveat repo-vuoto); deliverable = `saga_config` + doc autoriali |
| 2 | Costruzione nodo-storia | ⬜ | — | — | portare in repo la spec v0.2; aggiungere enum a `saga_config` (§2 spec) |
| 2b | Estrazione hook (Tappa 2) | ⬜ | — | — | generalizzare il prompt hook (placeholder al posto dei riferimenti isola) |
| 2c | Audit grafo (Tappa 5) | ⬜ | — | — | gli audit sono già config-driven: estrarli con `saga_config` vuoto + `known_issues` reset |
| 3 | Brief (zero-token) | ⬜ | — | — | scheletro `build_writing_brief` con sezioni a placeholder |
| 4 | Prosa (Tappa 6) | ⬜ | — | — | generalizzare `skills/prosa/SKILL.md` (voci/frasi-codice → placeholder) |
| 5 | Presentazione / build volume | ⬜ | — | — | separare identità (palette/font/glifi → config/placeholder) dalla logica |
| V | Pipeline visual | ⬜ | — | — | estrarre i template scheda/prompt (già a placeholder in `_visual_pipeline/_templates/`) |
| O | Orchestratore | ⬜ | — | — | per ultimo, montate le fasi |

## Debito da chiudere DENTRO il kit (non ereditare)

- ⬜ File generati committati con timestamp (`dashboard.js`, `entities.json`) → merge-driver `.gitattributes` o niente timestamp volatile. (Si lega alla sessione web.)
- ⬜ Enum nuovi Fase 2 in `saga_config`: `deployment_level`, `time_span.arc`, `presence.state`, `entry_point_type`, `closure_type`, `register`.
- ⬜ Confine parametrizza-vs-ri-autora di `build_volume`/`design_system` (~34 stringhe saga hardcoded da risolvere).

## Log sessioni

| Data | Fase | Cosa fatto | Branch |
|---|---|---|---|
| 2026-06-15 | (setup) | creati `SPEC_TEMPLATE.md`, `SKILL_crea_template.md`, questo ledger | `claude/template-spec-skill` |
