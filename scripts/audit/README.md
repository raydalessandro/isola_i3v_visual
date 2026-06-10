# `scripts/audit/`

Script di validazione del grafo e della prosa. **Implementati 2026-06-09**
(pacchetto blindatura). Lanciati:
- dall'agente di estensione hook dopo ogni scrittura per storia (fase G e successive),
- dalla CI su ogni push/PR (`.github/workflows/ci.yml`),
- a mano: `python3 scripts/audit/run_all_audits.py` (o `make audit`).

## I 4 audit

| Script | Cosa verifica | Stato |
|---|---|---|
| `audit_1_integrity.py` | JSON parseable, **chiavi duplicate intercettate**, schema_version + graph_version attesi, 12 storie presenti, migration_log cronologico, **catena backup congelata** (SHA-256 vs `_data/backup_manifest.sha256`). | ✅ |
| `audit_2_schema.py` | Hook a riposo: campi obbligatori, enum (type/provenance/composition_zone), esattamente 10 hook/storia, max 3 signature, max 3 consecutivi stesso type, ≥4 type diversi, focal_action ≤30 parole, quadrant coerente. Più: 24 cornici (schema DOC_3, who.kind ∈ {gruppo, nominato, anonimo}), world_conventions (refrain + 5 sentieri Tier A, 20 dettagli totali), quote_tracker. | ✅ |
| `audit_3_navigability.py` | Integrità referenziale: hook → entities; storia → locations/characters/objects/winds/seeds/callbacks; cornici → collettivi/characters + universo luoghi esteso (entities ∪ locations_secondary ∪ path_details ∪ schede visual/luoghi ∪ quartieri); path_details ↔ catalogo; seeds/callbacks interni. **Baseline a cricchetto** in `_data/known_issues.yaml`. | ✅ |
| `audit_4_drift.py` | Parte meccanica del drift: quote lessicali di `PATTERN_AI_DA_BANDIRE_v1.md` §6 sulla prosa di `storie_finali/` + coerenza marker `@hook`/`@subhook` ↔ grafo ↔ frontmatter ↔ immagini su disco (contratto di `build_volume.py`). Apparato subhook obbligatorio solo dove iniziato (oggi: pilota s01). | ✅ (parte grep) |

**Parte NON meccanica di audit_4** (fuori scope grep, resta review umana/agente):
ancorabilità di ogni `focal_action` alla narrazione fattuale; domande
qualitative §6 (triadi ascendenti, pugno emotivo, sguardo adulto-tenero,
voci distinguibili). Workflow consigliato: agente in chat con il brief +
`PATTERN_AI_DA_BANDIRE_v1.md`, una storia alla volta.

## Runner

```bash
python3 scripts/audit/run_all_audits.py          # tutti e 4
python3 scripts/audit/run_all_audits.py --fast   # salta audit_4 (prosa)
python3 scripts/audit/audit_4_drift.py --story s01
```

## Baseline incoerenze note (`_data/known_issues.yaml`)

Meccanismo **a cricchetto**: le incoerenze già note (in attesa di decisione
autoriale Ray) sono elencate lì e vengono declassate a `[known]`; qualunque
incoerenza NUOVA è un errore e blocca la CI. Quando il grafo viene corretto,
l'audit segnala la voce come stantia → rimuoverla. Obiettivo: file vuoto.

## Manifest backup (`_data/backup_manifest.sha256`)

I backup del grafo sono **immutabili per definizione**. Il manifest congela
i loro SHA-256: qualunque variazione = corruzione o manomissione → FAIL.
Un nuovo backup legittimo si registra con:

```bash
python3 scripts/audit/audit_1_integrity.py --update-manifest
```

(aggiunge solo voci nuove; gli hash esistenti non vengono mai sostituiti).

## Bump di versione autorizzati

`audit_1` confronta `schema_version`/`graph_version` con i valori attesi
(`EXPECTED_SCHEMA`/`EXPECTED_GRAPH` in testa allo script). Ad ogni bump
autorizzato del grafo, aggiornare quelle due costanti nello stesso commit:
così un bump non autorizzato (o un rollback accidentale) viene intercettato.

## Convenzione output

Ogni audit:
- exit code 0 = PASS
- exit code 1 = FAIL (stampa errori in chiaro)
- output umano-leggibile, no JSON
- `[known]` = incoerenza in baseline; `[warn]` = informativo non bloccante;
  `[info]` = stato di migrazione

L'agente blocca la pipeline se uno fallisce.
