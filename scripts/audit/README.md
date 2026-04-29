# `scripts/audit/`

Script di validazione del grafo, lanciati dall'agente di estensione hook (fase G) dopo ogni scrittura per storia.

## I 4 audit (da implementare)

| Script | Cosa verifica |
|---|---|
| `audit_1_integrity.py` | JSON parseable, schema_version + graph_version coerenti, tutti i 12 stories presenti, nessuna chiave duplicata. |
| `audit_2_schema.py` | Ogni hook ha tutti i campi obbligatori (`type`, `is_signature`, `provenance`, `composition_zone`, ecc.). Enum rispettati (type, composition_zone). Esattamente 10 hook per storia, max 3 signature, max 3 hook consecutivi stesso type, almeno 4 type diversi. |
| `audit_3_navigability.py` | Tutti gli `hook.location.id` esistono in `entities.locations`. Tutti i `characters_present` esistono in `entities.characters`. Tutti i `focal_object` esistono in `entities.objects` o nel catalogo. Tutti i `quadrant` matchano `cartografia/convenzioni/orientamenti_venti.md`. |
| `audit_4_drift.py` | Coerenza con narrazione fattuale: ogni `focal_action` è ancorabile a un evento descritto in `pipeline_narrativa/narrazione_fattuale/s0X_*.md`. Drift pattern AI: nessun lessico bandito da `PATTERN_AI_DA_BANDIRE_v1.md`. |

## Stato

Da implementare prima dell'avvio della fase G. Placeholder qui per documentare il contratto.

## Convenzione output

Ogni audit:
- exit code 0 = PASS
- exit code 1 = FAIL (stampa errori in chiaro)
- output umano-leggibile, no JSON

L'agente blocca la pipeline se uno fallisce.
