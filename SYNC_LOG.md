# SYNC_LOG — Cambiamenti da riflettere altrove

Questo file traccia ogni modifica fatta in `isola_i3v_visual` che **impatta o potrebbe impattare altre repo del sistema** (archivio storico `isola_tre_venti_github`, future repo prompt, sito esterno, pipeline immagini, ecc.). Ray (o un agente) parte da qui per riallineare le altre repo.

**Convenzione di entry:**
- ID univoco progressivo: `SYNC-YYYY-MM-DD-NNN`.
- Stato: `DA_RIFLETTERE` (default), `RIFLESSO` (Ray segna quando ha propagato), `SUPERATO` (entry sostituita da una successiva).
- Tipo: `bootstrap` / `cartografia` / `skills` / `visual` / `pipeline_input` / `governance`.
- Repo target: lista delle repo (o "n/a" se solo informativo).
- Cambiamento: descrizione tecnica concisa.
- File toccati: lista (gruppi se molti).

---

## SYNC-2026-04-25-001 — Bootstrap repo `isola_i3v_visual`
- **Stato:** DA_RIFLETTERE
- **Tipo:** bootstrap
- **Repo target:** archivio storico `isola_tre_venti_github` (informativo, archive-only). Eventuali repo che linkavano a `cartografia_tecnica/` come path.
- **Cambiamento:** repo unificato che ospita tre tracce:
  - `cartografia/` (ex `cartografia_tecnica/`, rinominata).
  - `pipeline_narrativa/` (input read-only invariato).
  - `visual/` (nuova directory, in attesa brief).
- **Commit:** `c863f3f`.
- **File toccati:** struttura intera + README + .gitignore + PROJECT_STATE.
- **Da riflettere altrove:** path `cartografia_tecnica/` → `cartografia/` se altre repo o documenti citano il vecchio nome.

## SYNC-2026-04-25-002 — Refactor AGENT_INSTRUCTIONS → `skills/`
- **Stato:** DA_RIFLETTERE
- **Tipo:** skills
- **Repo target:** n/a (governance interna del repo).
- **Cambiamento:** rimosso `AGENT_INSTRUCTIONS.md` monolitico, sostituito con `skills/`:
  - `skills/README.md` orchestratore + regole comuni (isolamento `pipeline_narrativa/` read-only, comunicazione, rifiuto, permessi di scrittura per skill).
  - `skills/cartografo.md` skill cartografia, scope `cartografia/`.
  - `skills/visual.md` skill visual, scope `visual/`, placeholder.
- **Commit:** `2259e5e`.
- **File toccati:** `AGENT_INSTRUCTIONS.md` (rimosso), `skills/*` (nuovi), `README.md`, `PROJECT_STATE.md`.
- **Da riflettere altrove:** se altre repo del sistema hanno un AGENT_INSTRUCTIONS analogo, considerare rifattorizzazione coerente (skill-based).

## SYNC-2026-04-25-003 — Cartografia v0.5 → v0.6.0 (sync grafo v0.10.0)
- **Stato:** DA_RIFLETTERE
- **Tipo:** cartografia
- **Repo target:** archivio storico `isola_tre_venti_github` (per allineamento copia di lavoro), eventuali repo prompt che pescano ID feature.
- **Cambiamento sintetico:**
  - **Aggiunta** feature `radura_dei_pini` (Polygon, status `provvisorio`, quartiere `terra`) — landmark interno alla Foresta Intrecciata, margine NE verso Pascoli Alti. Citato in S12.
  - **Promotion** `sentiero_roccia_burrone` da `provvisorio` a `canonico`. Giustificato da S12 (resolution_mode: "la cengia che sale a Roccia Alta — i fratelli la sanno senza che nessuno la indichi").
  - **Annotazione** in `roccia_alta.note`: la cengia di accesso da sud è `sentiero_roccia_burrone` (non entità autonoma).
  - **Alias aggiunto** `guado_nord` → `guado_di_pietre_piatte` (citato in S12 come "guado nord dove l'acqua trema piano").
  - **Bump** `metadata.version` 0.5 → 0.6.0; aggiunta `changes_from_v0_5`.
- **Backward-compat grafo↔cartografia:** 100% (verificato pre e post).
- **Grafo di riferimento:** `pipeline_narrativa/story_graph.json` v0.10.0.
- **Decisione architetturale richiamata:** "casa_fratelli non entity, l'isola è protagonista" (blocco_0). Il "cortile" citato in `s10.wind_notes` non viene mappato per coerenza con questa decisione.
- **Commit:** _da inserire dopo commit_.
- **File toccati:** `cartografia/geo/island.geojson`, `cartografia/CHANGELOG.md`, `PROJECT_STATE.md`.
- **Da riflettere altrove:** se altre repo cachano la lista feature o gli ID, rigenerare. Nessun rename di ID esistenti, solo aggiunte/promotion/alias.

---

## Note

- Ray ha annunciato che a breve farà manutenzione sul grafo storie e porterà qui la versione manutenuta come **nuova baseline**. Quando arriverà, registrarla qui come entry SYNC dedicata.
- Le entry restano come storico anche dopo essere state riflesse (mai cancellare). Cambiare solo lo stato.
