# s10 — Migration Notes

**Data**: 2026-04-28
**Output**: `s10_canonical.json` (PASS verify)
**Esecuzione**: P1+P2 eseguito da agente alternativo. File migration_notes ricostruito post-zip-corruzione.

## Storia
"La Notte senza Luna" — apertura_blocco_d, ciclo cambiare, autunno pieno → autunno (REGOLA 0.10).

## Trasformazioni applicate
- `season: autunno_pieno` → `autunno` (REGOLA 0.10)
- `block_position: apertura_blocco_d` (gia' canonico)
- `attribute_dominant: cambiare` (gia' canonico)
- `key_phrase_indicative: "Ho paura.\nQui è buio."` + `key_phrase_attributed_to: "noah"` (REGOLA 0.8 — terna strato 3 DIRE 5 parole, primo della curva)
- `night_scene: true` (notte senza luna), `pattern_a_active: attivo` (variante notturna del bloom s08)
- 7 personaggi in scena
- 4 hooks
- 1 debt_opened + 6 debts_closed (debt_vero_dict)

## Auto-derivati
- `wind_active: vento_mulinello`
- `quartieri_attraversati: ["acqua_sud", "centro_villaggio"]`
- `fear_touched`: noah (paura_buio bloom pieno via 5-parole)
- `oggetti_simbolo_presenti`: include `lanterna_velata_s10` (canonical 13)

## Misalignments
Nessuno nuovo.

## Stato
PASS verify. 5 provvisori P2 (5A + 0B + 0C). I 5 `no_inference_fields` restano `null`.
